"""Render Q-version fronts from the existing layered card on the local dev server."""
from io import BytesIO
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
IDS = ['deepseek', 'gpt', 'glm', 'qwen', 'gemini', 'claude', 'kimi', 'grok', 'doubao']
selected = sys.argv[1:] or IDS
if any(character not in IDS for character in selected):
    raise SystemExit('Unknown character ID')
mask = Image.new('L', (1200, 1688), 0)
draw = ImageDraw.Draw(mask)
draw.rounded_rectangle((0, 0, 1199, 1687), radius=50, fill=255)
draw.rounded_rectangle((468, 64, 731, 111), radius=24, fill=0)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 960}, device_scale_factor=4,
                            reduced_motion='reduce', java_script_enabled=False)
    for locale in ['zh', 'en']:
        for character in selected:
            route = '/' if character == 'deepseek' else f'/characters/{character}/'
            page.goto('http://127.0.0.1:4321' + ('/en' if locale == 'en' else '') + route,
                      wait_until='domcontentloaded')
            page.evaluate('''async () => {
              await document.fonts.ready;
              const scene = document.createElement('div');
              scene.className = 'badge-scene badge-scene--interactive texture-export';
              scene.style.cssText = 'position:fixed;top:10px;left:10px;width:324px;height:455.625px;z-index:2147483647;visibility:visible;pointer-events:none';
              const card = document.querySelector('.legacy-badge-scene .badge-card').cloneNode(true);
              card.dataset.version = 'chibi';
              card.style.cssText = 'position:absolute;top:0;left:0;transform:none;width:324px;height:455.625px;opacity:1;visibility:visible';
              card.querySelector('.badge-hole')?.remove();
              card.querySelector('.badge-portrait img').dataset.printSrc = card.querySelector('.badge-portrait img').dataset.chibiSrc;
              scene.append(card); document.querySelector('.home-experience').append(scene);
              await Promise.all([...card.querySelectorAll('img[data-print-src]')].map(async img => { img.src = img.dataset.printSrc; await img.decode(); }));
            }''')
            data = page.locator('.texture-export .badge-face--front').screenshot()
            image = Image.open(BytesIO(data)).convert('RGB')
            display = ROOT / 'public' / 'img' / 'badges' / locale / f'{character}-chibi-front.webp'
            image.save(display, 'WEBP', quality=92, method=6)
            download = ROOT / 'public' / 'downloads' / locale
            front = download / f'{character}-chibi-front.png'
            cutout = image.resize((1200, 1688), Image.Resampling.LANCZOS).convert('RGBA')
            cutout.putalpha(mask)
            cutout.save(front, optimize=True)
            with ZipFile(download / f'{character}-chibi-crew-pass.zip', 'w', ZIP_DEFLATED) as archive:
                archive.write(front, f'{character}-{locale}-chibi-front.png')
                archive.write(download / f'{character}-back.png', f'{character}-{locale}-back.png')
            print(locale, character, flush=True)
    browser.close()
