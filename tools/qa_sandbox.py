"""Isolated end-to-end v0.2 offline simulation checks; never uses player-profile."""
import json,os,sys,time,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];mobile='mobile' in sys.argv
OUT=ROOT/'output/playwright/v2'/('mobile' if mobile else 'desktop');OUT.mkdir(parents=True,exist_ok=True)
events=[]
def emit(kind,**data):events.append(dict(time=time.time(),kind=kind,**data))
with sync_playwright() as p:
    context=p.chromium.launch_persistent_context(str(ROOT.parent/('qa-v2-mobile' if mobile else 'qa-v2-final')),
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
        load('local.html?sandbox=0');normal=prefs('normal-before');shot('normal')
        load();shot('default');save=prefs('default')
        troops=page.evaluate('LocalPrefs.troops')
        assert all(save.get(k)==2 for k in troops),{k:save.get(k) for k in troops if save.get(k)!=2}
        assert all(save.get(k+'Boss')==2 for k in ['Spartan','Sentinel','SamuraiNEW','FireDragonNEW','Minigun','Rhino','Guardian','Wolf'])
        assert save['Consumables']>=999999999
        assert save.get('HasBoughtIAP',0)==normal.get('HasBoughtIAP',0)==0
        assert save.get('HasSubscriptionGoogle',0)==normal.get('HasSubscriptionGoogle',0)==0
        # Direct native DB opening avoids the sandbox alias; only read the ordinary save.
        ordinary=page.evaluate('''async()=>{
          const d=await new Promise(r=>{const q=nativeOpen('/idbfs');q.onsuccess=()=>r(q.result)});
          const a=await new Promise(r=>{const q=d.transaction('FILE_DATA').objectStore('FILE_DATA').getAll();q.onsuccess=()=>r(q.result)});d.close();
          const f=a.find(v=>v.contents&&v.contents[0]===85);return Object.fromEntries(LocalPrefs.entries(f.contents).entries.map(e=>[e.key,e.value]));
        }''')
        assert ordinary==normal
        click(1070,670);shot('max-upgrades-top');page.mouse.move(800,500);page.mouse.wheel(0,850);page.wait_for_timeout(1800);shot('max-upgrades-bottom')
        load();click(90,497)
        shot('level-budget')
        click(400,80)
        for i,(x,y) in enumerate([(400,360),(440,360),(480,360),(520,360),(560,360),(400,420),(440,420),(480,420),(520,420),(560,420),(440,480),(480,480)]):click(x,y,350)
        shot('level-spending')
        load();click(90,550);click(705,23);shot('epic-available')
        positions=[(180,280),(340,280),(500,280),(180,430),(340,430),(500,470),(180,580),(440,590)]
        for i,x in enumerate([333,400,465,530,600,665,730,798]):
            if i:click(640,7,300);click(705,23,300)
            click(x,80,650);shot('epic-selected-'+str(i+1))
            px,py=positions[i];click(px,py,650);click(px+15,py+15,650)
            shot('epic-'+str(i+1))
        # Same selected wolf is placed on the opposite team to exercise combat.
        click(800,410,700);shot('formation');click(1230,675,2500);click(1200,62,1000);shot('pause');click(640,360,1000)
        page.wait_for_timeout(25000);shot('battle-result');click(640,520,1000);shot('battle-result-dismissed');prefs('post-battle')
        page.reload();page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(16000);shot('refresh');assert prefs('refresh')['Man']==2
        page.close();page=context.new_page();load();shot('reopen');assert prefs('reopen')['Wolf']==2
        load('local.html?sandbox=0')
        off=prefs('off');assert off['Man']==normal['Man'];assert off['Wolf']==normal['Wolf'];shot('off')
        emit('checks',default=True,all37Level3=True,ordinarySaveUnchanged=True,reload=True,reopen=True,off=True,viewport=page.viewport_size,touch=mobile)
    finally:
        (OUT/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf-8');context.close()
