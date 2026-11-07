"""Export the existing card artwork as front/back textures for React Bits Lanyard."""
from pathlib import Path
import subprocess
import sys
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
out=root/'public/img/badges'
out.mkdir(exist_ok=True,parents=True)
ids=['deepseek','gpt','glm','qwen','gemini','claude','kimi','grok','doubao']
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':960},device_scale_factor=4,reduced_motion='reduce',java_script_enabled=False)
    for locale in ['zh','en']:
        target=out/locale
        target.mkdir(exist_ok=True)
        for id in ids:
            path='/' if id=='deepseek' else f'/characters/{id}/'
            page.goto('http://127.0.0.1:4321'+('/en' if locale=='en' else '')+path,wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            page.evaluate('''async () => {
                const image = document.querySelector('.badge-portrait img');
                image.src = image.dataset.printSrc;
                await image.decode();
            }''')
            page.wait_for_timeout(200)
            page.evaluate('''() => {
                const scene=document.createElement('div');
                scene.className='badge-scene badge-scene--interactive texture-export';
                scene.style.cssText='position:fixed;inset:auto;top:10px;left:10px;width:324px;height:455.625px;z-index:2147483647;visibility:visible;pointer-events:none';
                const card=document.querySelector('.badge-card').cloneNode(true);
                card.style.cssText='position:absolute;top:0;left:0;transform:none;width:324px;height:455.625px;opacity:1;visibility:visible';
                card.removeAttribute('hidden');
                card.querySelector('.badge-tilt').style.transform='none';
                card.querySelector('.badge-flip').style.transform='none';
                card.querySelector('.badge-hole')?.remove();
                scene.append(card);document.body.append(scene);
            }''')
            export=page.locator('.texture-export')
            export.locator('.badge-face--front').screenshot(path=str(target/f'{id}-front.png'))
            export.evaluate('''e=>{e.querySelector('.badge-face--front').style.display='none';const back=e.querySelector('.badge-face--back');back.hidden=false;back.style.transform='none';back.style.display='flex'}''')
            export.locator('.badge-face--back').screenshot(path=str(target/f'{id}-back.png'))
            brand=page.locator('.legacy-badge-scene').get_attribute('data-strap-label-text')
            color=page.locator('.badge-scene').first.get_attribute('data-strap-color')
            # A short seamless repeat: multiple brand names are visible along the strap.
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="288" height="128"><rect width="288" height="128" fill="{color}"/><text x="144" y="77" text-anchor="middle" font-family="monospace" font-size="34" letter-spacing="4" fill="#edf3fb">{brand}</text></svg>'
            # Shift the seamless print so the page edge can cut through a word.
            label=svg[svg.index('<text'):svg.index('</text>')+7]
            svg=svg.replace(label,label.replace('x="144"','x="-80"')+label.replace('x="144"','x="208"'))
            (out/f'{id}-strap.svg').write_text(svg,encoding='utf-8')
            print(locale,id,flush=True)
    browser.close()
subprocess.run([sys.executable,str(root/'scripts/export-web-textures.py')],check=True)
