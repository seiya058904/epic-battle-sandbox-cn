"""Compare every serialized object against original bytes; reject unlisted changes."""
import UnityPy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
baseline=UnityPy.load(str(ROOT/'Build/EBS.data'))
candidate=UnityPy.load(str(ROOT/'local-generated/EBS.zh-CN.data'))
ledger=json.loads((ROOT/'evidence/patch-ledger.json').read_text(encoding='utf-8'))
allowed={(r['file'],r['id']) for r in ledger if 'file' in r}
before={(o.assets_file.name,o.path_id):o for o in baseline.objects}
after={(o.assets_file.name,o.path_id):o for o in candidate.objects}
assert before.keys()==after.keys()
changed=[]
for key,obj in before.items():
    new=after[key]
    assert obj.type==new.type
    if obj.get_raw_data()!=new.get_raw_data():
        assert key in allowed, f'Unexpected changed object: {key}'
        changed.append(dict(file=key[0],id=key[1],type=obj.type.name))
original_web=next(iter(baseline.files.values()));new_web=next(iter(candidate.files.values()))
for key,obj in original_web.files.items():
    if key not in ('data.unity3d','Il2CppData/Metadata/global-metadata.dat'):
        old=obj.bytes if hasattr(obj,'bytes') else obj.save();new=new_web.files[key];new=new.bytes if hasattr(new,'bytes') else new.save()
        assert old==new,key
result=dict(total_objects=len(before),changed_objects=len(changed),unchanged_objects=len(before)-len(changed),unlisted_changes=0,changes=changed)
(ROOT/'evidence/object-verification.json').write_text(json.dumps(result,indent=2))
print('PASS:',len(before),'objects;',len(changed),'listed changes;',len(before)-len(changed),'byte-identical objects')
