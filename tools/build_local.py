"""Hash-locked, object-scoped localization. Never writes original Build files."""
import hashlib, json, struct, math
from pathlib import Path
import UnityPy
from UnityPy.streams import EndianBinaryReader
from UnityPy.enums import TextureFormat
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy.ndimage import distance_transform_edt
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'local-generated'; OUT.mkdir(exist_ok=True)
MAP=json.loads((ROOT/'localization/translations.json').read_text(encoding='utf-8'))
manifest=json.loads((ROOT/'evidence/baseline-manifest.json').read_text())
for row in manifest['files']:
    assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'], row['path']+' differs from baseline'
FONT=ROOT.parent/'tool-cache/NotoSansCJKsc-Regular.otf'
assert FONT.exists(), 'Download the documented OFL font first'
assert hashlib.sha256(FONT.read_bytes()).hexdigest()=='2c76254f6fc379fddfce0a7e84fb5385bb135d3e399294f6eeb6680d0365b74b', 'Unexpected font bytes'
chars=sorted({c for text in MAP.values() for c in text if ord(c)>127})
cmap=TTFont(FONT).getBestCmap(); assert all(ord(c) in cmap for c in chars)
env=UnityPy.load(str(ROOT/'Build/EBS.data'))
original_object_count=len(env.objects)
ledger=[]
u32=lambda b,p:struct.unpack_from('<I',b,p)[0]
f32=lambda b,p:struct.unpack_from('<f',b,p)[0]
align=lambda n:(n+3)&~3
def script_name(o):
    try:return o.read(check_read=False).m_Script.deref().read().m_Name
    except (ValueError,FileNotFoundError):return ''
def pptr(o,b,pos):
    fid,pid=struct.unpack_from('<iq',b,pos)
    if fid==0: return o.assets_file.objects[pid]
    name=o.assets_file.externals[fid-1].path.replace('\\','/').split('/')[-1]
    return next(f for f in env.assets if f.name==name).objects[pid]

for o in env.objects:
    if o.type.name!='MonoBehaviour': continue
    name=script_name(o); raw=o.get_raw_data()
    if name in ('TextMeshProUGUI','Text','Level_Manager'):
        # Serialized UnityEngine.UI.Text and legacy TMP: select only validated string fields.
        offsets=[]
        for en,zh in MAP.items():
            needle=struct.pack('<I',len(en.encode()))+en.encode()
            p=raw.find(needle)
            while p>=0:
                if p%4==0 and (name!='TextMeshProUGUI' or p==88): offsets.append((p,en,zh))
                p=raw.find(needle,p+len(needle))
        for p,en,zh in sorted(offsets,reverse=True):
            end=align(p+4+len(en.encode())); new=zh.encode(); encoded=struct.pack('<I',len(new))+new
            raw=raw[:p]+encoded+b'\0'*(align(len(encoded))-len(encoded))+raw[end:]
            ledger.append(dict(kind='display_name' if name=='Level_Manager' else 'serialized_text',file=o.assets_file.name,id=o.path_id,offset=p,source=en,target=zh))
        if offsets:o.set_raw_data(raw)
    elif name=='TMP_FontAsset':
        # All 534 TMP UI components resolve to these two fonts. Leave unused demo fonts intact.
        if (o.assets_file.name,o.path_id) not in {('sharedassets0.assets',32),('sharedassets0.assets',33)}:continue
        # Old TMP FontAsset layout, verified against Unity TMP 1.4.1 FaceInfo_Legacy/TMP_Glyph.
        b=bytearray(raw); base=align(32+u32(b,28)); face=base+24
        p=align(face+4+u32(b,face)) # PointSize
        glyph_count_pos=p+92; count=u32(b,glyph_count_pos); glyph_start=glyph_count_pos+4
        assert count==u32(b,p+8) and 0<count<2000
        oldw,oldh=map(int,(f32(b,p+72),f32(b,p+76)))
        atlas_obj=pptr(o,b,p+80); atlas=atlas_obj.read()
        assert (atlas.m_Width,atlas.m_Height)==(oldw,oldh)
        # Keep all original glyphs and the original atlas pixels; append only missing Chinese.
        existing={u32(b,glyph_start+i*36) for i in range(count)}
        add=[c for c in chars if ord(c) not in existing]
        original_size=f32(b,p); size=round(original_size)
        pad=max(3,math.ceil(f32(b,p+68))); cell=size+2*pad+8
        width=max(oldw,4096); cols=width//cell; rows=math.ceil(len(add)/cols)
        height=2**math.ceil(math.log2(oldh+rows*cell+cell))
        assert height<=8192
        img=Image.new('RGBA',(width,height),(255,255,255,0)); img.paste(atlas.image,(0,0))
        font=ImageFont.truetype(str(FONT),size)
        entries=[]
        for i,c in enumerate(add):
            left,top,right,bottom=font.getbbox(c,anchor='ls'); w,h=right-left,bottom-top
            tile=Image.new('L',(w+2*pad+4,h+2*pad+4)); draw=ImageDraw.Draw(tile)
            draw.text((pad+2-left,pad+2-top),c,font=font,fill=255,anchor='ls')
            mask=np.asarray(tile)>127
            distance=distance_transform_edt(mask)-distance_transform_edt(~mask)
            alpha=Image.fromarray(np.uint8(np.clip(127.5+distance*127.5/(pad+1),0,255)))
            rgba=Image.new('RGBA',tile.size,'white'); rgba.putalpha(alpha)
            x=(i%cols)*cell; y=oldh+(i//cols)*cell
            img.paste(rgba,(x,y))
            entries.append(struct.pack('<i8f',ord(c),x+pad+2,y+pad+2,w,h,left,-top,font.getlength(c),original_size/size))
        struct.pack_into('<I',b,p+8,count+len(entries))
        struct.pack_into('<ff',b,p+72,width,height)
        struct.pack_into('<I',b,glyph_count_pos,count+len(entries))
        end=glyph_start+count*36
        o.set_raw_data(bytes(b[:end])+b''.join(entries)+bytes(b[end:]))
        atlas.set_image(img,target_format=TextureFormat.Alpha8); atlas.save()
        ledger.append(dict(kind='font_atlas',file=atlas_obj.assets_file.name,id=atlas_obj.path_id,size=[width,height],format='Alpha8'))
        # All material variants referencing this atlas need matching UV dimensions.
        for mat in env.objects:
            if mat.type.name!='Material':continue
            d=mat.read_typetree(); props=d['m_SavedProperties']
            matches=False
            for key,tex in props['m_TexEnvs']:
                ptr=tex['m_Texture']
                if ptr['m_PathID']==atlas_obj.path_id:
                    try: matches=pptr(mat,struct.pack('<iq',ptr['m_FileID'],ptr['m_PathID']),0) is atlas_obj
                    except (StopIteration,KeyError): pass
                if matches:break
            if matches:
                props['m_Floats']=[(k,float(width) if k=='_TextureWidth' else float(height) if k=='_TextureHeight' else v) for k,v in props['m_Floats']]
                mat.save_typetree(d)
                ledger.append(dict(kind='font_material',file=mat.assets_file.name,id=mat.path_id,atlas=[width,height]))
        ledger.append(dict(kind='font',file=o.assets_file.name,id=o.path_id,name=o.read(check_read=False).m_Name,glyphs_added=len(entries),atlas=[width,height]))

web=next(iter(env.files.values()))
meta=bytearray(web.files['Il2CppData/Metadata/global-metadata.dat'].bytes)
magic,version,litoff,litsize,dataoff,datasize=struct.unpack_from('<6I',meta)
assert magic==0xFAB11BAF and version==31
# Exclude unit names / identifiers that may double as PlayerPrefs keys.
safe={'You need more gems','Add Some Troops First!','Blue Team Has No Troops!','Red Team Has No Troops!','Upgrade Required','LVL ','Level ','Epic Level ','MAX',' (MAX)'}
safe.update({'Blue Team Won The Battle!','Red Team Won The Battle!',' Wins The Battle!','First Time Win Reward - ','Regular Win Reward - ','First Win All Previous Levels','First Win All Previous Epic Levels'})
literal_data=bytearray(meta[dataoff:dataoff+datasize])
for i in range(litsize//8):
    length,off=struct.unpack_from('<II',meta,litoff+i*8)
    text=meta[dataoff+off:dataoff+off+length].decode('utf-8',errors='replace')
    if text in safe:
        new=MAP[text].encode(); struct.pack_into('<II',meta,litoff+i*8,len(new),len(literal_data)); literal_data.extend(new)
        ledger.append(dict(kind='literal',index=i,source=text,target=MAP[text]))
struct.pack_into('<II',meta,16,len(meta),len(literal_data)); meta.extend(literal_data)
web.files['Il2CppData/Metadata/global-metadata.dat']=EndianBinaryReader(bytes(meta))
web.files['data.unity3d']=EndianBinaryReader(web.files['data.unity3d'].save(packer='lz4'))
payload=web.save()
(OUT/'EBS.zh-CN.data').write_bytes(payload)
check=UnityPy.load(payload)
assert len(check.objects)==original_object_count
(ROOT/'evidence/patch-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'evidence/generated-manifest.json').write_text(json.dumps({'data_sha256':hashlib.sha256(payload).hexdigest(),'font_sha256':hashlib.sha256(FONT.read_bytes()).hexdigest(),'bytes':len(payload),'entries':len(ledger)},indent=2))
print('Generated',len(payload),'bytes;',len(ledger),'controlled edits')
# Remove the upstream fake rewarded-ad completion callback in the local variant.
framework=(ROOT/'Build/EBS.framework.js').read_text(encoding='utf-8')
assert framework.count('unityInstance.SendMessage("H5GamesAds","OnRewardedAdCompleted")')==2
framework=framework.replace('unityInstance.SendMessage("H5GamesAds","OnRewardedAdCompleted");','')
(OUT/'EBS.local.framework.js').write_text(framework,encoding='utf-8')
generated=json.loads((ROOT/'evidence/generated-manifest.json').read_text())
generated['framework_sha256']=hashlib.sha256((OUT/'EBS.local.framework.js').read_bytes()).hexdigest()
(ROOT/'evidence/generated-manifest.json').write_text(json.dumps(generated,indent=2))
