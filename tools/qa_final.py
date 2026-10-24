"""Reproducible local Chromium scenarios; screenshots require visual review."""
import json,os,sys,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output/playwright/final';OUT.mkdir(parents=True,exist_ok=True)
mode=sys.argv[1] if len(sys.argv)>1 else 'baseline'
mobile=mode=='mobile'
events=[]
def emit(kind,**data):events.append(dict(time=time.time(),kind=kind,**data))
with sync_playwright() as p:
    candidates=sorted((Path(os.environ['LOCALAPPDATA'])/'ms-playwright').glob('chromium-*/chrome-win64/chrome.exe'))
    executable=os.environ.get('EBS_CHROMIUM') or str(candidates[-1])
    context=p.chromium.launch_persistent_context(str(ROOT.parent/('qa-mobile-profile' if mobile else 'qa-desktop-profile')),
        executable_path=executable,headless=True,viewport={'width':844 if mobile else 1280,'height':390 if mobile else 720},
        has_touch=mobile,is_mobile=mobile,device_scale_factor=1,
        user_agent='Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36' if mobile else None)
    context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(('http://127.0.0.1:8765/','blob:','data:')) else (emit('blocked_external',url=route.request.url),route.abort())[1])
    page=context.pages[0]
    page.on('console',lambda msg:emit('console',level=msg.type,text=msg.text))
    page.on('pageerror',lambda err:emit('pageerror',text=str(err)))
    page.on('response',lambda res:emit('response',status=res.status,url=res.url))
    page.on('requestfailed',lambda req:emit('requestfailed',url=req.url,error=req.failure))
    def shot(name):
        page.screenshot(path=str(OUT/(mode+'-'+name+'.png')));emit('screenshot',name=name);print(mode+' '+name,flush=True)
    def render_sample(name):
        sample=page.evaluate('''()=>new Promise(resolve=>{
          let drew=false,frames=0;const patches=[];
          for(const cls of [window.WebGLRenderingContext,window.WebGL2RenderingContext])if(cls)for(const key of ['drawArrays','drawElements','drawArraysInstanced','drawElementsInstanced']){
            const proto=cls.prototype,fn=proto[key];if(typeof fn!=='function')continue;
            patches.push([proto,key,fn]);proto[key]=function(...args){drew=true;return fn.apply(this,args)};
          }
          const start=performance.now();function tick(){if(drew)frames++;drew=false;const ms=performance.now()-start;
            if(ms<2500)requestAnimationFrame(tick);else{for(const [p,k,f]of patches)p[k]=f;resolve({drawFrames:frames,durationMs:ms,renderFps:frames*1000/ms})}}
          requestAnimationFrame(tick);
        })''');emit('render-sample',name=name,values=sample)
    def load(path):
        page.goto('http://127.0.0.1:8765/'+path)
        page.wait_for_function('Boolean(window.unityInstance)',timeout=90000)
        page.wait_for_timeout(16000)
    def click(x,y,delay=2500):
        b=page.locator('canvas').bounding_box();x=b['x']+x/1280*b['width'];y=b['y']+y/720*b['height']
        if mobile:page.touchscreen.tap(x,y)
        else:page.mouse.click(x,y,delay=150)
        page.wait_for_timeout(delay)
    def prefs(name):
        result=page.evaluate('''async()=>{
          const db=await new Promise(r=>{let q=indexedDB.open('/idbfs');q.onsuccess=()=>r(q.result)});
          const s=db.transaction('FILE_DATA').objectStore('FILE_DATA');const q=s.openCursor();
          return await new Promise(r=>{q.onsuccess=()=>{const c=q.result;if(!c){r(null);return}if(!String(c.key).endsWith('/PlayerPrefs')){c.continue();return}
           const b=new Uint8Array(c.value.contents),d=new DataView(b.buffer),t=new TextDecoder();let p=16,o={};while(p<b.length){let n=b[p++],k=t.decode(b.slice(p,p+n));p+=n;let ty=b[p++];let v=ty===254?d.getInt32(p,true):ty===255?d.getFloat32(p,true):t.decode(b.slice(p,p+ty));p+=ty>=254?4:ty;if(['Consumables','Man','Crossbow','Archer','SpearMan','AxeMan','HasBoughtIAP','HasSubscriptionGoogle','LevelsCompleted'].includes(k))o[k]=v}r(o)}})
        }''');emit('prefs',name=name,values=result)
    try:
        path='' if mode=='baseline' else 'local.html?sandbox=1' if mode=='probe' else 'local.html'
        load(path);shot('home');prefs('initial');render_sample('home')
        if mode=='probe':
            click(90,497,3000);shot('budget-before')
            page.evaluate("unityInstance.SendMessage('Level_Manager','set_tempUserAvailableGold',999999999)")
            for x,y in [(500,400),(510,430),(520,460)]:click(x,y,1000)
            shot('budget-after')
            click(640,7,1000);click(400,80,1000);shot('costly-unit')
            for x,y in [(400,350),(420,390),(440,430),(460,470),(480,510),(500,550)]:click(x,y,800)
            shot('budget-limit')
        elif mode=='menus':
            click(90,497,3000);shot('levels')
            # Return by reloading, preserving the exact origin and local save.
            load('local.html');click(1230,670,3000);shot('shop')
            load('local.html');click(1070,670,3000);shot('upgrades')
        elif mode=='resources':
            click(1070,670);shot('normal-upgrades')
            page.get_by_role('button',name='开启沙盒').click();page.wait_for_url('**sandbox=1');page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(16000)
            click(1070,670);shot('sandbox-before');prefs('sandbox-before')
            for i,(x,y) in enumerate([(480,185),(677,185),(878,185)],1):click(x,y,1500);shot('spend-'+str(i));prefs('spend-'+str(i))
            page.reload();page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(16000);click(1070,670);shot('refresh');prefs('refresh')
            page.goto('about:blank');load('local.html?sandbox=1');click(1070,670);shot('reopen');prefs('reopen')
            page.get_by_role('button',name='关闭沙盒').click();page.wait_for_url('**/local.html');page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(16000);click(1070,670);shot('off');prefs('off')
        else:
            click(1238,38);shot('settings');click(78,58)
            click(90,550,4000);shot('custom')
            for x,y in [(540,390),(550,420),(710,400)]:click(x,y,800)
            shot('formation');click(1230,675,2500);shot('battle')
            click(1200,62,1500);shot('pause')
            # Pause menu resume is the central round play button; review screenshot before certifying.
            click(640,360,1500);shot('resume')
            page.wait_for_timeout(18000);shot('result');prefs('after-battle')
            click(640,520,2000);shot('result-dismissed')
        emit('identity',url=page.url,title=page.title(),viewport=page.viewport_size,chromium=context.browser.version,
             runtime=page.evaluate('({wasmMemoryBytes:window.unityInstance?.Module?.HEAPU8?.length,jsHeapBytes:performance.memory?.usedJSHeapSize,maxTouchPoints:navigator.maxTouchPoints})'))
    finally:
        (OUT/(mode+'-events.json')).write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf-8');context.close()
