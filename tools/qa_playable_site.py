"""Exercise the actual playable site in temporary contexts, never player-profile."""
import argparse
import json
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('url',nargs='?',default='http://127.0.0.1:8766/')
parser.add_argument('--mobile',action='store_true')
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/playwright/v4'/('live' if args.url.startswith('https:') else 'preview')/('mobile' if args.mobile else 'desktop')
OUT.mkdir(parents=True,exist_ok=True)
events=[]
def emit(kind,**data):
    events.append(dict(time=time.time(),kind=kind,**data))
    if kind in ('shot','complete'):print(kind,data,flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('EBS_CHROMIUM') or str(Path(os.environ['LOCALAPPDATA'])/'ms-playwright/chromium-1248/chrome-win64/chrome.exe'))
    context=browser.new_context(viewport={'width':844 if args.mobile else 1280,'height':390 if args.mobile else 720},has_touch=args.mobile,is_mobile=args.mobile)
    page=context.new_page()
    def observe(page):
        page.on('pageerror',lambda e:emit('pageerror',message=str(e)))
        page.on('console',lambda m:emit('console',level=m.type,text=m.text) if m.type in ('error','warning') else None)
        page.on('requestfailed',lambda r:emit('requestfailed',url=r.url,error=r.failure))
    observe(page)
    def load(suffix=''):
        response=page.goto(args.url+suffix,wait_until='domcontentloaded',timeout=60000)
        assert response.status==200
        page.wait_for_function('Boolean(window.unityInstance)',timeout=240000)
        page.wait_for_timeout(4000)
        assert page.locator('#loading').is_hidden()
        assert page.locator('header,#toggle').count()==0
    def shot(name):
        page.screenshot(path=str(OUT/(name+'.png')));emit('shot',name=name)
    def click(x,y,wait=700):
        box=page.locator('canvas').bounding_box();x=box['x']+x*box['width']/1280;y=box['y']+y*box['height']/720
        if args.mobile:page.touchscreen.tap(x,y)
        else:page.mouse.click(x,y,delay=120)
        page.wait_for_timeout(wait)
    def prefs(label):
        values=page.evaluate('''async()=>{
          const db=await new Promise(r=>{const q=indexedDB.open('/idbfs');q.onsuccess=()=>r(q.result)});
          const name=db.name;const files=await new Promise(r=>{const q=db.transaction('FILE_DATA').objectStore('FILE_DATA').getAll();q.onsuccess=()=>r(q.result)});db.close();
          const f=files.find(v=>v.contents&&v.contents[0]===85);
          return {database:name,values:Object.fromEntries(LocalPrefs.entries(f.contents).entries.map(e=>[e.key,e.value]))};
        }''')
        emit('prefs',label=label,**values);return values
    try:
        load();shot('home');initial=prefs('initial')
        assert initial['database']=='/idbfs-ebs-pages-sandbox-v1'
        assert initial['values']['Consumables']>=999999999 and initial['values']['WolfBoss']==2
        click(1070,670,1000);shot('upgrades')
        load();click(90,550,1200);shot('custom-empty')
        for x,y in [(300,420),(400,440),(800,400)]:click(x,y)
        shot('formation');click(1230,675,1500);shot('battle')
        click(1200,62,800);shot('pause');click(640,360,800)
        page.wait_for_timeout(22000);shot('result');click(640,520,1000);shot('result-dismissed');prefs('result')
        load();shot('refresh');assert prefs('refresh')['values']['WolfBoss']==2
        page.close();page=context.new_page();observe(page);load();shot('reopen');assert prefs('reopen')['values']['WolfBoss']==2
        load('?sandbox=0');shot('normal');normal=prefs('normal')
        assert normal['database']=='/idbfs-ebs-pages-standard-v1'
        assert normal['values'].get('WolfBoss',0)!=2
        assert not any(e['kind']=='pageerror' for e in events)
        emit('complete',url=page.url,viewport=page.viewport_size,temporaryContext=True)
    finally:
        (OUT/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf-8')
        browser.close()
