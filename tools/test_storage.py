"""Exercise migration/fresh IDB initialization without running Unity or touching player profiles."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('EBS_CHROMIUM') or str(Path(os.environ['LOCALAPPDATA'])/'ms-playwright/chromium-1248/chrome-win64/chrome.exe'))
    results=[]
    for case in ['fresh','empty-v1','valid-v1']:
        context=browser.new_context();page=context.new_page()
        page.route('**/local.html',lambda r:r.fulfill(content_type='text/html',body='<span id="mode"></span><button id="toggle"></button><script src="prefs-codec.js"></script>'))
        page.goto('http://127.0.0.1:8765/local.html')
        before=page.evaluate('''async mode=>{
          const open=name=>new Promise(r=>{const q=indexedDB.open(name,21);q.onupgradeneeded=()=>q.result.createObjectStore('FILE_DATA').createIndex('timestamp','timestamp');q.onsuccess=()=>r(q.result)});
          const put=async(name,value)=>{const d=await open(name);if(value!==null){const data=LocalPrefs.fullSandbox(), key=new TextEncoder().encode('AuditMarker'),entry=new Uint8Array(key.length+6);entry[0]=key.length;entry.set(key,1);entry[key.length+1]=254;new DataView(entry.buffer).setInt32(key.length+2,value,true);const bytes=new Uint8Array(data.length+entry.length);bytes.set(data);bytes.set(entry,data.length);await new Promise(r=>{const t=d.transaction('FILE_DATA','readwrite');t.objectStore('FILE_DATA').put({contents:bytes,mode:33206,timestamp:new Date()},'/idbfs/573c4e13a250a56ce7a0928edd2dcd62/PlayerPrefs');t.oncomplete=r})}d.close()};
          window.readNative=async name=>{const d=await open(name);const a=await new Promise(r=>{const q=d.transaction('FILE_DATA').objectStore('FILE_DATA').getAll();q.onsuccess=()=>r(q.result)});d.close();return a.map(v=>v.contents?Array.from(v.contents):null)};
          if(mode!=='fresh'){await put('/idbfs',11);await put('/idbfs-ebs-local-sandbox-v1',mode==='valid-v1'?99:null)}
          return {normal:await readNative('/idbfs'),old:await readNative('/idbfs-ebs-local-sandbox-v1')};
        }''',case)
        page.add_script_tag(url='http://127.0.0.1:8765/local-mode.js');page.evaluate('localReady')
        current=page.evaluate("readNative('/idbfs-ebs-local-sandbox-v2')")
        # Read the source with nativeOpen, bypassing the game's /idbfs alias.
        original=page.evaluate('''async()=>{const read=async name=>{const d=await new Promise(r=>{const q=nativeOpen(name);q.onsuccess=()=>r(q.result)});const a=await new Promise(r=>{const q=d.transaction('FILE_DATA').objectStore('FILE_DATA').getAll();q.onsuccess=()=>r(q.result)});d.close();return a.map(v=>v.contents?Array.from(v.contents):null)};return {normal:await read('/idbfs'),old:await read('/idbfs-ebs-local-sandbox-v1')}}''')
        assert original==before
        data=page.evaluate('''files=>{const f=files.find(v=>v&&v[0]===85);return Object.fromEntries(LocalPrefs.entries(f).entries.map(e=>[e.key,e.value]))}''',current)
        assert data['Consumables']==999999999 and data['WolfBoss']==2
        assert data.get('AuditMarker')==({'fresh':None,'empty-v1':11,'valid-v1':99}[case])
        results.append(dict(case=case,sourceUnchanged=True,marker=data.get('AuditMarker'),gems=data['Consumables'],wolfLevel=data['WolfBoss']))
        context.close()
    browser.close()
(ROOT/'evidence/storage-validation.json').write_text(json.dumps(results,indent=2))
print('PASS: fresh seed, empty-v1 fallback, valid-v1 migration, both source DBs unchanged')
