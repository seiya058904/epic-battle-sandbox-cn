"""Build an independent offline simulation data file; original code/assets untouched.

Field schema recovered read-only from IL2CPP v31 metadata + WASM data segments.
Original metadata registration 3902828; type count 8845; no native code patch.
"""
import hashlib,json,struct
from pathlib import Path
import UnityPy
from UnityPy.streams import EndianBinaryReader
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'local-generated/EBS.zh-CN.data'
assert hashlib.sha256(source.read_bytes()).hexdigest()==json.loads((ROOT/'evidence/generated-manifest.json').read_text())['data_sha256']
assert hashlib.sha256((ROOT/'Build/EBS.data').read_bytes()).hexdigest()=='04ec370550c3fb4935c65d103d6a56cbccb40a88243fec81d0d89d90f52220b5'
schema=json.loads((ROOT/'evidence/sandbox-field-schema.json').read_text())
env=UnityPy.load(str(source));ledger=[];align=lambda n:(n+3)&~3
inline={'ArmyInspector','LevelValues','StatsValues','LevelDesignValues','ArmyBalance'}
enums={'Army','LevelDesign','LayerMask'}
def parse(b,p,t,path,rows):
    start=p
    if t.endswith('[]'):
        n=struct.unpack_from('<I',b,p)[0];p+=4;assert n<5000,(path,n)
        for i in range(n):p=parse(b,p,t[:-2],path+f'[{i}]',rows)
    elif t in inline:
        for f in schema[t]:p=parse(b,p,f['type'],path+'.'+f['name'],rows)
    elif t=='string':
        n=struct.unpack_from('<I',b,p)[0];p+=4;assert n<1024
        b[p:p+n].decode('utf-8');p=align(p+n)
    elif t in {'int','uint','float','bool','Color32'}|enums:
        value=struct.unpack_from('<f' if t=='float' else '<i',b,p)[0];p+=4
        rows.append((path,start,value))
    else:p+=12 # UnityEngine.Object PPtr, including LevelSetUp ScriptableObject.
    assert p<=len(b)
    return p
before={(o.assets_file.name,o.path_id):o.get_raw_data() for o in env.objects}
for o in env.objects:
    if (o.assets_file.name,o.path_id)!=('level1',8170):continue
    assert o.read(check_read=False).m_Script.deref().read().m_Name=='Level_Manager'
    b=bytearray(o.get_raw_data());p=align(32+struct.unpack_from('<I',b,28)[0]);rows=[]
    for f in schema['Level_Manager']:p=parse(b,p,f['type'],f['name'],rows)
    fields={name:(offset,value) for name,offset,value in rows}
    assert fields['customArmyNumber'][1]==120
    assert fields['LevelsValues[0].availableGold'][1]==300
    assert fields['LevelsValues[0].availableArmy'][1]==8
    assert len([n for n in fields if n.startswith('LevelsValues[') and n.endswith('.availableGold')])==105
    assert len([n for n in fields if n.startswith('EpicLevelsValues[') and n.endswith('.availableGold')])==10
    for name,(offset,value) in fields.items():
        new=None
        if name.endswith('.availableGold'):new=999999999
        elif name.endswith(('.availableArmy','.counterMax')) or name=='customArmyNumber':new=1000
        if new is not None:
            struct.pack_into('<i',b,offset,new)
            ledger.append(dict(field=name,offset=offset,before=value,after=new))
    assert len(ledger)==268
    o.set_raw_data(bytes(b))
assert ledger
web=next(iter(env.files.values()));web.files['data.unity3d']=EndianBinaryReader(web.files['data.unity3d'].save(packer='lz4'))
payload=web.save();check=UnityPy.load(payload)
after={(o.assets_file.name,o.path_id):o.get_raw_data() for o in check.objects}
assert before.keys()==after.keys()
assert [k for k in before if before[k]!=after[k]]==[('level1',8170)]
expected=bytearray(before[('level1',8170)])
for row in ledger:struct.pack_into('<i',expected,row['offset'],row['after'])
assert bytes(expected)==after[('level1',8170)]
target=ROOT/'local-generated/EBS.sandbox.data';target.write_bytes(payload)
receipt=dict(version='0.2.0',sourceSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),outputSHA256=hashlib.sha256(target.read_bytes()).hexdigest(),changedObject=['level1',8170],unchangedObjects=len(before)-1,fields=ledger)
(ROOT/'evidence/sandbox-patch.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: one object,',len(ledger),'validated fields;',target.name)
