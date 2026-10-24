"""Isolated end-to-end v0.3 native UI checks; never uses player-profile."""
import json,os,sys,time,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];mobile='mobile' in sys.argv
OUT=ROOT/'output/playwright/v3'/('mobile' if mobile else 'desktop');OUT.mkdir(parents=True,exist_ok=True)
events=[]
def emit(kind,**data):events.append(dict(time=time.time(),kind=kind,**data))
with sync_playwright() as p:
    context=p.chromium.launch_persistent_context(str(ROOT.parent/('qa-v3-mobile' if mobile else 'qa-v3-desktop')),
        executable_path=os.environ.get('EBS_CHROMIUM') or str(Path(os.environ['LOCALAPPDATA'])/'ms-playwright/chromium-1248/chrome-win64/chrome.exe'),
        headless=True,viewport={'width':844 if mobile else 1280,'height':390 if mobile else 720},has_touch=mobile,is_mobile=mobile)
    context.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:8765/','blob:','data:')) else (emit('external-blocked',url=r.request.url),r.abort())[1])
    page=context.pages[0]
    page.on('pageerror',lambda e:emit('pageerror',text=str(e)))
    page.on('console',lambda m:emit('console-error',text=m.text) if m.type=='error' else None)
    def shot(name):page.screenshot(path=str(OUT/(name+'.png')));print(name,flush=True)
    def click(x,y,wait=650):
        b=page.locator('canvas').bounding_box();x=b['x']+x*b['width']/1280;y=b['y']+y*b['height']/720
        if mobile:page.touchscreen.tap(x,y)
        else:page.mouse.click(x,y,delay=120)
        page.wait_for_timeout(wait)
    def load(path='local.html'):
        page.goto('http://127.0.0.1:8765/'+path);page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(16000)
    def prefs(name,db='/idbfs'):
        data=page.evaluate('''async name=>{
          const db=await new Promise((resolve,reject)=>{const r=indexedDB.open(name);r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
          const values=await new Promise(r=>{const q=db.transaction('FILE_DATA').objectStore('FILE_DATA').getAll();q.onsuccess=()=>r(q.result)});db.close();
          const file=values.find(v=>v.contents&&v.contents[0]===85&&v.contents[1]===110);if(!file)return null;
          return Object.fromEntries(LocalPrefs.entries(file.contents).entries.map(e=>[e.key,e.value]));
        }''',db)
        emit('prefs',name=name,values=data);return data

    try:
        load();shot('home');initial=prefs('initial')
        assert initial['Man']==2 and initial['WolfBoss']==2 and initial['Consumables']>=999999999
        click(1238,38,1200);shot('settings');click(78,58,1200)
        click(1070,670,1200);shot('upgrades');click(310,232,1000)
        load();click(1230,670,1200);shot('shop')
        load();click(90,497,1500);shot('levels')
        load();click(90,550,1500);shot('custom-empty')
        for x,y in [(300,420),(400,440),(800,400)]:click(x,y,900)
        shot('formation')
        click(640,7,600);click(880,23,1200);shot('clear')
        for x,y in [(300,420),(400,440),(800,400)]:click(x,y,900)
        click(1230,675,2500);shot('battle');click(1200,62,1000);shot('pause');click(640,360,1000);shot('resume')
        page.wait_for_timeout(22000);shot('result');prefs('result')
        # First-run rating prompt can cover results. Dismiss it; external navigation is blocked by local mode and test routing.
        click(640,520,1000);shot('result-after-dismiss')
        load();shot('refresh');assert prefs('refresh')['WolfBoss']==2
        load('local.html?sandbox=0');shot('normal-mode');prefs('normal-mode')
        emit('checks',url=page.url,title=page.title(),viewport=page.viewport_size,touch=mobile,complete=True)
    finally:
        (OUT/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf-8');context.close()
