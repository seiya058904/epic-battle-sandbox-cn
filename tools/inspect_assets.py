import UnityPy, json, collections, struct, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/'analysis'; OUT.mkdir(parents=True,exist_ok=True)
env=UnityPy.load(str(ROOT/'Build/EBS.data'))
report={'types':dict(collections.Counter(o.type.name for o in env.objects)),'assets':[], 'scripts':[], 'texts':[], 'fonts':[], 'mono_strings':[]}
for f in env.assets:
    report['assets'].append({'name':f.name,'version':f.unity_version})
for o in env.objects:
    base={'file':o.assets_file.name,'id':o.path_id}
    if o.type.name=='MonoScript':
        d=o.read(); report['scripts'].append(dict(base,name=d.m_Name,assembly=d.m_AssemblyName,namespace=d.m_Namespace))
    if o.type.name=='TextAsset':
        d=o.read(); report['texts'].append(dict(base,name=d.m_Name,text=str(d.m_Script)[:1000]))
    if o.type.name=='Font':
        d=o.read_typetree(); report['fonts'].append(dict(base,**{k:v for k,v in d.items() if k not in ('m_FontData','m_KerningValues','m_CharacterRects')}))
    if o.type.name=='MonoBehaviour':
        raw=o.get_raw_data()
        found=[]
        for m in re.finditer(rb'[\x20-\x7e]{3,}',raw):
            off=m.start()
            if off>=4 and struct.unpack_from('<I',raw,off-4)[0]==len(m[0]): found.append({'offset':off-4,'text':m[0].decode()})
        if found: report['mono_strings'].append(dict(base,strings=found,bytes=len(raw)))
(OUT/'assets.json').write_text(json.dumps(report,ensure_ascii=True,indent=2),encoding='utf-8')
web=next(iter(env.files.values()))
meta=web.files['Il2CppData/Metadata/global-metadata.dat'].bytes
(OUT/'global-metadata.dat').write_bytes(meta)
# IL2CPP metadata string literals are indexed length + byte offset, not blind byte scans.
magic,version,litoff,litsize,dataoff,datasize=struct.unpack_from('<6I',meta)
assert magic==0xFAB11BAF
literals=[]
for i in range(litsize//8):
    length,offset=struct.unpack_from('<II',meta,litoff+i*8)
    s=meta[dataoff+offset:dataoff+offset+length].decode('utf-8',errors='replace')
    literals.append({'index':i,'text':s})
(OUT/'literals.json').write_text(json.dumps(literals,ensure_ascii=True,indent=2),encoding='utf-8')
print(json.dumps({'metadata_version':version,'literal_count':len(literals),'mono_strings':len(report['mono_strings']),'fonts':report['fonts'],'textassets':report['texts']},ensure_ascii=True)[:6000])
