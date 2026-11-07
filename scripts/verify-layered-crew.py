"""Check all layered exports, real render readiness, download alpha and image traffic."""
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
from playwright.sync_api import sync_playwright
import json
import sys

root=Path(__file__).resolve().parents[1]
base=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4321').rstrip('/')
roles=['deepseek','gpt','glm','qwen','gemini','claude','kimi','grok','doubao']
preview=root/'docs/preview'
preview.mkdir(exist_ok=True)
report=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':960},reduced_motion='reduce')
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    for locale in ['zh','en']:
        for role in roles:
            route=('/en' if locale=='en' else '')+('/' if role=='deepseek' else f'/characters/{role}/')
            page.goto(base+route,wait_until='domcontentloaded')
            page.locator('.lanyard[data-front-ready="true"]').wait_for(timeout=20000)
            assert page.locator('.badge-face--ocean').count()==1,(role,'missing layered front')
            assert page.locator('.badge-face--ocean-back').count()==1,(role,'missing layered back')
            assert page.locator('.badge-card img[src]').count()==0,(role,'raw art loaded')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            original_requests=page.evaluate('''()=>performance.getEntriesByType('resource').filter(e=>/\\/img\\/(characters|deepseek|gpt|glm|qwen|gemini|claude|kimi|grok|doubao)\\//.test(e.name)).map(e=>e.name)''')
            assert not original_requests,original_requests
            if locale=='zh' and role in ['glm','doubao','grok']:
                page.wait_for_timeout(1300)
                page.screenshot(path=str(preview/f'{role}-layered-desktop.png'))
            for face in ['front','back']:
                path=root/f'public/downloads/{locale}/{role}-{face}.png'
                with Image.open(path) as im:
                    assert im.size==(1200,1688) and im.mode=='RGBA'
                    assert im.getpixel((0,0))[3]==0 and im.getpixel((600,85))[3]==0
                    assert im.getpixel((600,800))[3]==255
                texture=root/f'public/img/badges/{locale}/{role}-{face}.webp'
                assert Image.open(texture).size==(1296,1824)
            with ZipFile(root/f'public/downloads/{locale}/{role}-crew-pass.zip') as archive:
                assert archive.testzip() is None and len(archive.namelist())==2
            report.append({'role':role,'locale':locale,'frontKiB':round((root/f'public/img/badges/{locale}/{role}-front.webp').stat().st_size/1024),'backKiB':round((root/f'public/img/badges/{locale}/{role}-back.webp').stat().st_size/1024)})
    page.set_viewport_size({'width':390,'height':844})
    page.goto(base+'/en/characters/doubao/',wait_until='networkidle')
    page.locator('.lanyard[data-front-ready="true"]').wait_for()
    page.wait_for_timeout(1000)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(preview/'doubao-layered-mobile.png'))
    # Inspect a stable series contact sheet at real card layout proportions.
    page.set_viewport_size({'width':1620,'height':1100})
    images=''.join(f'<figure><img src="{base}/img/badges/zh/{r}-front.webp"><img src="{base}/img/badges/zh/{r}-back.webp"><figcaption>{r}</figcaption></figure>' for r in roles)
    page.set_content('<style>body{margin:20px;background:#ebedf2;font:14px sans-serif}main{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}figure{margin:0}img{width:48%;border-radius:8px}figcaption{padding:8px}</style><main>'+images+'</main>')
    page.locator('img').evaluate_all('images=>Promise.all(images.map(i=>i.decode()))')
    page.screenshot(path=str(preview/'all-layered-crew.png'),full_page=True)
    assert not errors,errors
    browser.close()
(preview/'layered-crew-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS: 18 role/language renders, 36 native-resolution faces, no raw art requests, transparent downloads and 18 valid ZIPs; desktop/mobile previews saved.')
print(json.dumps(report))
