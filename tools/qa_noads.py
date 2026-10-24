from pathlib import Path
import os,json,time
from playwright.sync_api import sync_playwright
O=Path(__file__).resolve().parents[1]/'output/playwright/v3/idle';O.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('EBS_CHROMIUM') or str(Path(os.environ['LOCALAPPDATA'])/'ms-playwright/chromium-1248/chrome-win64/chrome.exe'),headless=True);c=b.new_context(viewport={'width':1280,'height':720});page=c.new_page();c.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:8765/','blob:','data:')) else r.abort())
 page.add_init_script('''(()=>{const instantiate=WebAssembly.instantiate;window.adCalls=[];WebAssembly.instantiate=function(bytes,imports){if(imports)for(const module of Object.values(imports))for(const [name,fn]of Object.entries(module))if(typeof fn==='function'&&/JSShowInterstitialAd|JSShowRewardedAd/.test(fn.name)){module[name]=function(...args){window.adCalls.push({name:fn.name,at:performance.now()});return fn(...args)}}return instantiate.call(this,bytes,imports)}})()''')
 page.goto('http://127.0.0.1:8765/local.html');page.wait_for_function('Boolean(window.unityInstance)',timeout=90000)

 start=time.monotonic()
 for target in [0,5,8,12,20,60,120,180,240,295,300,305,310,315,330,360]:
  while time.monotonic()-start<target:page.wait_for_timeout(min(1000,int((target-(time.monotonic()-start))*1000)+1))
  page.screenshot(path=str(O/(str(target)+'.png')));print('idle '+str(target),flush=True)
 calls=page.evaluate('window.adCalls');assert not calls,calls
 (O/'result.json').write_text(json.dumps({'seconds':time.monotonic()-start,'adCalls':calls,'url':page.url,'title':page.title()},indent=2))
 b.close()
