"""Ensure Pages never imports another game's shared-origin /idbfs database."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://seiya058904.github.io/epic-battle-sandbox-cn/'
browser_path = os.environ.get('EBS_CHROMIUM') or str(Path(os.environ['LOCALAPPDATA']) / 'ms-playwright/chromium-1248/chrome-win64/chrome.exe')
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=browser_path)
    for mode in ('sandbox', 'normal'):
        context = browser.new_context()
        page = context.new_page()
        def route(r):
            if r.request.url.endswith('prefs-codec.js'):
                r.fulfill(content_type='text/javascript', body=(ROOT/'prefs-codec.js').read_text(encoding='utf-8'))
            else:
                r.fulfill(content_type='text/html', body='<script src="prefs-codec.js"></script>')
        context.route('**/*', route)
        page.goto(BASE + ('?sandbox=0' if mode == 'normal' else ''))
        before = page.evaluate('''async()=>{
          window.fixtureOpen=name=>new Promise(r=>{const q=indexedDB.open(name,21);q.onupgradeneeded=()=>q.result.createObjectStore('FILE_DATA').createIndex('timestamp','timestamp');q.onsuccess=()=>r(q.result)});
          window.fixtureRead=async name=>{const d=await fixtureOpen(name);const a=await new Promise(r=>{const q=d.transaction('FILE_DATA').objectStore('FILE_DATA').getAll();q.onsuccess=()=>r(q.result)});d.close();return a.filter(v=>v.contents).map(v=>Array.from(v.contents))};
          for(const name of ['/idbfs','/idbfs-ebs-local-sandbox-v1','/idbfs-ebs-local-sandbox-v2']){
            const d=await fixtureOpen(name);await new Promise(r=>{const t=d.transaction('FILE_DATA','readwrite');t.objectStore('FILE_DATA').put({contents:new Uint8Array([91,92,93]),timestamp:new Date()},'unrelated-save');t.oncomplete=r});d.close();
          }
          return Promise.all(['/idbfs','/idbfs-ebs-local-sandbox-v1','/idbfs-ebs-local-sandbox-v2'].map(fixtureRead));
        }''')
        page.add_script_tag(content=(ROOT/'local-mode.js').read_text(encoding='utf-8'))
        page.evaluate('localReady')
        assert page.evaluate('hosted') is True
        assert page.evaluate('prefsDirectory') == '/idbfs/f8be888972dce20dba59ea4b998503f0'
        alias = page.evaluate("async()=>{const d=await new Promise(r=>{const q=indexedDB.open('/idbfs',21);q.onsuccess=()=>r(q.result)});const n=d.name;d.close();return n}")
        assert alias == '/idbfs-ebs-pages-' + ('sandbox' if mode == 'sandbox' else 'standard') + '-v1'
        after = page.evaluate('''async()=>{
          const read=async name=>{const d=await new Promise(r=>{const q=nativeOpen(name);q.onsuccess=()=>r(q.result)});const a=await new Promise(r=>{const q=d.transaction('FILE_DATA').objectStore('FILE_DATA').getAll();q.onsuccess=()=>r(q.result)});d.close();return a.map(v=>Array.from(v.contents))};
          return Promise.all(['/idbfs','/idbfs-ebs-local-sandbox-v1','/idbfs-ebs-local-sandbox-v2'].map(read));
        }''')
        assert before == after
        if mode == 'sandbox':
            gems = page.evaluate("async()=>{const a=await fixtureRead(SANDBOX);const f=a.find(b=>b[0]===85);return Object.fromEntries(LocalPrefs.entries(new Uint8Array(f)).entries.map(e=>[e.key,e.value])).Consumables}")
            assert gems == 999999999
        results.append({'mode': mode, 'mappedDatabase': alias, 'foreignDatabasesUnchanged': True})
        context.close()
    browser.close()
print(json.dumps(results, indent=2))
