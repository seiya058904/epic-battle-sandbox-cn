"""Native Unity UI localization and offline auto-ad removal. No texture painting.

Replace baked-label Image references with the build's existing rounded Background
sprite; add real TMP children. Preserve Button events, navigation and hit targets.
"""
from pathlib import Path
import copy,hashlib,json,struct
import UnityPy
from UnityPy.streams import EndianBinaryReader
ROOT=Path(__file__).resolve().parents[1]
labels={int(k):v for k,v in json.loads((ROOT/'localization/native-buttons.json').read_text(encoding='utf-8')).items()}
def ptr(pid,fid=0):return {'m_FileID':fid,'m_PathID':pid}
def script(o):
    try:return o.read(check_read=False).m_Script.deref().read().m_Name
    except (ValueError,FileNotFoundError):return ''
receipts=[]
for variant in ['zh-CN','sandbox']:
    source=ROOT/f'local-generated/EBS.{variant}.data'
    manifest=json.loads((ROOT/('evidence/generated-manifest.json' if variant=='zh-CN' else 'evidence/sandbox-patch.json')).read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['data_sha256' if variant=='zh-CN' else 'outputSHA256']
    env=UnityPy.load(str(source));ledger=[]
    before={(o.assets_file.name,o.path_id):o.get_raw_data() for o in env.objects}
    # Dedicated timer GameObject: do not alter domain approval, IAP or reward callbacks.
    ads=[o for o in env.objects if o.type.name=='MonoBehaviour' and script(o)=='H5InterstitialAutoCaller']
    assert len(ads)==1
    ad=ads[0];assert (ad.assets_file.name,ad.path_id)==('level0',81)
    raw=bytearray(ad.get_raw_data());assert struct.unpack_from('<ffii',raw,32)==(5.0,300.0,3,7)
    raw[12]=0;ad.set_raw_data(bytes(raw))
    go=ad.read(check_read=False).m_GameObject.deref();gd=go.read_typetree();assert gd['m_Name']=='H5AutoAds' and len(gd['m_Component'])==2
    gd['m_IsActive']=False;go.save_typetree(gd)
    ledger.append(dict(kind='disable_auto_ad_timer',file='level0',component=81,gameObject=go.path_id,firstDelay=5,repeatInterval=300,countdown=3,breakSeconds=7))
    f=next(a for a in env.assets if a.name=='level1')
    assert f.externals[2].path=='resources.assets'
    # Results swap the restart sprite at runtime; both alternatives become the
    # same text-free background under the native 'continue battle' label.
    manager=f.objects[8169];assert script(manager)=='Ui_Manager'
    mb=bytearray(manager.get_raw_data())
    for offset,sid in [(3760,1302),(3772,1307)]:
        assert struct.unpack_from('<iq',mb,offset)==(2,sid)
        struct.pack_into('<iq',mb,offset,3,106)
    manager.set_raw_data(bytes(mb))
    template=f.objects[6326];assert script(template)=='TextMeshProUGUI'
    tmpr=template.get_raw_data();assert len(tmpr)==748 and tmpr[92:96]==b'1000'
    assert struct.unpack_from('<ii',tmpr,100)==(5,32)
    goTemplate=f.objects[8];rectTemplate=f.objects[4903];rendererTemplate=f.objects[3556]
    nextid=max(f.objects)+1
    def clone(obj):
        global nextid
        n=object.__new__(type(obj));n.__dict__.update(obj.__dict__);n.path_id=nextid;nextid+=1;n.data=None;f.objects[n.path_id]=n;return n
    images=[o for o in list(f.objects.values()) if o.type.name=='MonoBehaviour' and script(o)=='Image']
    for image in images:
        raw=bytearray(image.get_raw_data());assert len(raw)==136
        fid,sid=struct.unpack_from('<iq',raw,88)
        if fid!=2 or sid not in labels:continue
        d=image.read(check_read=False);parent=d.m_GameObject.deref();pg=parent.read_typetree()
        # OK checkmark images are indicators, not text buttons.
        if sid==1398 and pg['m_Name']!='Ok_Button':continue
        pr=next(f.objects[c['component']['m_PathID']] for c in pg['m_Component'] if f.objects[c['component']['m_PathID']].type.name=='RectTransform')
        pd=pr.read_typetree();text=labels[sid]
        struct.pack_into('<iq',raw,88,3,106) # existing rounded, text-free sprite
        struct.pack_into('<I',raw,100,1) # Sliced
        raw[104]=0 # PreserveAspect off, fill original button rectangle
        color=(0.16,0.40,0.66,1.0) if sid not in [1321,1322,1310] else (0.65,0.23,0.18,1.0)
        if sid in [1432,1433,1434,1435,1436,1440]:color=(0.55,0.24,0.12,1.0)
        struct.pack_into('<4f',raw,44,*color);image.set_raw_data(bytes(raw))
        g=clone(goTemplate);r=clone(rectTemplate);cr=clone(rendererTemplate);t=clone(template)
        gdata=copy.deepcopy(goTemplate.read_typetree());gdata.update(m_Name='LocalZh_'+str(image.path_id),m_IsActive=True,m_Component=[{'component':ptr(o.path_id)} for o in [r,cr,t]])
        g.save_typetree(gdata)
        rd=copy.deepcopy(rectTemplate.read_typetree());rd.update(m_GameObject=ptr(g.path_id),m_Father=ptr(pr.path_id),m_Children=[],m_AnchorMin={'x':0.0,'y':0.0},m_AnchorMax={'x':1.0,'y':1.0},m_AnchoredPosition={'x':0.0,'y':0.0},m_SizeDelta={'x':-6.0,'y':-4.0},m_Pivot={'x':0.5,'y':0.5})
        r.save_typetree(rd);cr.save_typetree({'m_GameObject':ptr(g.path_id),'m_CullTransparentMesh':True})
        b=bytearray(tmpr);struct.pack_into('<iq',b,0,0,g.path_id);b[60]=0 # do not intercept Button raycasts
        b[164]=0 # vertex gradient off; solid white text
        struct.pack_into('<ff',b,272,32.0,32.0);b[284]=1 # auto-size
        struct.pack_into('<ff',b,288,14.0,32.0)
        struct.pack_into('<i',b,300,514);b[304]=1 # converted TMP center/middle alignment
        b[332]=0 # no word wrapping
        encoded=text.encode('utf-8');replacement=struct.pack('<I',len(encoded))+encoded+b'\0'*((-len(encoded))%4)
        t.set_raw_data(bytes(b[:88])+replacement+bytes(b[96:]))
        pd['m_Children'].append(ptr(r.path_id));pr.save_typetree(pd)
        ledger.append(dict(kind='native_button_label',file='level1',image=image.path_id,gameObject=parent.path_id,name=pg['m_Name'],sourceSprite=sid,text=text,added=[g.path_id,r.path_id,cr.path_id,t.path_id]))
    assert len([x for x in ledger if x['kind']=='native_button_label'])>=20
    web=next(iter(env.files.values()));web.files['data.unity3d']=EndianBinaryReader(web.files['data.unity3d'].save(packer='lz4'))
    payload=web.save();check=UnityPy.load(payload);after={(o.assets_file.name,o.path_id):o.get_raw_data() for o in check.objects}
    changed=[k for k in before if before[k]!=after[k]];added=[k for k in after if k not in before]
    allowed={('level0',81),('level0',go.path_id),('level1',8169)}
    for row in ledger:
        if row['kind']!='native_button_label':continue
        allowed.add(('level1',row['image']))
        pg=f.objects[row['gameObject']].read_typetree()
        allowed.update(('level1',c['component']['m_PathID']) for c in pg['m_Component'] if f.objects[c['component']['m_PathID']].type.name=='RectTransform')
    assert set(changed)==allowed
    assert len(added)==4*(len(ledger)-1)
    # Components that own events and gameplay remain byte-identical. Check each
    # added native label's references after serializing and loading the result.
    checkedFile=next(a for a in check.assets if a.name=='level1')
    for row in ledger:
        if row['kind']!='native_button_label':continue
        gid,rid,crid,tid=row['added'];gdata=checkedFile.objects[gid].read_typetree()
        assert [c['component']['m_PathID'] for c in gdata['m_Component']]==[rid,crid,tid]
        textRaw=checkedFile.objects[tid].get_raw_data();length=struct.unpack_from('<I',textRaw,88)[0]
        assert textRaw[92:92+length].decode('utf-8')==row['text'] and textRaw[60]==0
        assert checkedFile.objects[rid].read_typetree()['m_GameObject']['m_PathID']==gid
    target=ROOT/f'local-generated/EBS.{variant}.ui.data';target.write_bytes(payload)
    receipts.append(dict(variant=variant,inputSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),outputSHA256=hashlib.sha256(payload).hexdigest(),changed=changed,addedObjects=len(added),ledger=ledger))
    print(variant,'PASS:',len(ledger)-1,'native labels;',len(changed),'changed;',len(added),'new; auto-ad object disabled')
(ROOT/'evidence/native-ui-patch.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2),encoding='utf-8')
