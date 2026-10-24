from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'output/playwright/v2/capacity';O.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 c=p.chromium.launch_persistent_context(str(R.parent/'qa-capacity'),executable_path=os.environ.get('EBS_CHROMIUM') or str(Path(os.environ['LOCALAPPDATA'])/'ms-playwright/chromium-1248/chrome-win64/chrome.exe'),headless=True,viewport={'width':1280,'height':720})
 c.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:8765/','blob:','data:')) else r.abort())
 page=c.pages[0];events=[];page.on('pageerror',lambda e:events.append(str(e)));page.on('console',lambda m:events.append(m.text) if m.type=='error' else None)
 def shot(n):page.screenshot(path=str(O/(n+'.png')));print(n,flush=True)
 def click(x,y):
  b=page.locator('canvas').bounding_box();page.mouse.click(b['x']+x*b['width']/1280,b['y']+y*b['height']/720,delay=150);page.wait_for_timeout(1600)


 page.goto('http://127.0.0.1:8765/local.html');page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(16000)
 click(90,497);click(705,23);click(333,80);shot('level105-budget-before')
 for y in [260,350,440,530]:
  for x in [170,280,390,500]:click(x,y)
 shot('level105-spent-over-6000')
 page.reload();page.wait_for_function('Boolean(window.unityInstance)',timeout=90000);page.wait_for_timeout(16000)
 click(90,550);click(150,250)
 for y in range(240,591,35):
  for x in range(130,581,30):
   b=page.locator('canvas').bounding_box();page.mouse.click(b['x']+x*b['width']/1280,b['y']+y*b['height']/720,delay=90);page.wait_for_timeout(120)
 shot('custom-over-120')
 (O/'errors.json').write_text(json.dumps(events,indent=2));c.close()
