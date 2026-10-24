from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'output/playwright/v2/epic-full';O.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 c=p.chromium.launch_persistent_context(str(R.parent/'qa-epic-full'),executable_path=os.environ.get('EBS_CHROMIUM') or str(Path(os.environ['LOCALAPPDATA'])/'ms-playwright/chromium-1248/chrome-win64/chrome.exe'),headless=True,viewport={'width':1280,'height':720})
 c.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:8765/','blob:','data:')) else r.abort())
 page=c.pages[0];events=[];page.on('pageerror',lambda e:events.append(str(e)));page.on('console',lambda m:events.append(m.text) if m.type=='error' else None)
 def shot(n):page.screenshot(path=str(O/(n+'.png')));print(n,flush=True)
 def click(x,y):
  b=page.locator('canvas').bounding_box();page.mouse.click(b['x']+x*b['width']/1280,b['y']+y*b['height']/720,delay=150);page.wait_for_timeout(1600)

 page.goto('http://127.0.0.1:8765/local.html');page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(18000)
 for i,x in enumerate([333,400,465,530,600,665,730,798]):
  if i:
   page.reload();page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(14000)
  click(90,550);click(705,23);click(x,80);shot('unit-'+str(i+1)+'-selected')
  click(200,420);click(300,450);click(400,500);shot('unit-'+str(i+1)+'-placed')
 (O/'errors.json').write_text(json.dumps(events,indent=2));c.close()
