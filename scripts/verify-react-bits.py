"""Exercise the real upstream canvas with pointer input, not legacy debug hooks."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

out = Path(__file__).resolve().parents[1] / 'docs/preview'
out.mkdir(parents=True, exist_ok=True)

def difference(a, b):
    return sum(ImageStat.Stat(ImageChops.difference(Image.open(BytesIO(a)).convert('RGB'), Image.open(BytesIO(b)).convert('RGB'))).mean)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width':1440,'height':960}, reduced_motion='reduce')
    errors, failed = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('response', lambda r: failed.append(r.url) if r.status >= 400 else None)
    for role in ['deepseek','gpt','glm','qwen','gemini','claude','kimi','grok','doubao']:
        page.goto('http://127.0.0.1:4321/' + ('' if role == 'deepseek' else f'characters/{role}/'), wait_until='networkidle')
        canvas = page.locator('.lanyard-canvas')
        canvas.wait_for()
        assert canvas.evaluate('(e)=>e.width>0 && e.height>0')
        assert page.locator('.legacy-badge-scene').is_hidden()
        assert page.locator('[data-profile-github]').get_attribute('href') == 'https://github.com/fanhuayishiy/ai-crew-pass'
        for face in ['front.png','back.png','strap.svg']:
            folder = '' if face == 'strap.svg' else 'zh/'
            assert page.request.get(f'http://127.0.0.1:4321/img/badges/{folder}{role}-{face}').ok
    page.goto('http://127.0.0.1:4321/', wait_until='networkidle')
    page.wait_for_timeout(3000)
    canvas = page.locator('.lanyard-canvas')
    # Discover the card through its own raycast hover response.
    def find_card():
        for y in range(350, 700, 40):
            for x in range(500, 920, 40):
                page.mouse.move(x,y)
                if canvas.evaluate('(e)=>e.style.cursor') == 'grab':
                    return x,y
        raise AssertionError('Native card raycast found no draggable surface')
    x,y = find_card()
    page.mouse.down()
    assert canvas.evaluate('(e)=>e.style.cursor') == 'grabbing'
    page.mouse.move(x+180,y-180,steps=24)
    page.wait_for_timeout(550)
    held = canvas.screenshot()
    page.mouse.up()
    page.wait_for_timeout(220)
    falling = canvas.screenshot()
    page.wait_for_timeout(700)
    swinging = canvas.screenshot()
    assert difference(held,falling)>0.5, 'Card did not move after release'
    assert difference(falling,swinging)>0.5, 'Card did not continue its free swing'
    page.wait_for_timeout(5000)
    x,y = find_card()
    before = canvas.screenshot()
    page.mouse.click(x,y)
    page.wait_for_timeout(2000)
    assert difference(before,canvas.screenshot())>1, 'Native click flip did not change card'
    page.screenshot(path=str(out/'react-bits-flipped.png'))
    page.goto('http://127.0.0.1:4321/', wait_until='networkidle')
    page.locator('#screen2').evaluate('(e)=>e.scrollIntoView()')
    page.wait_for_timeout(1500)
    page.locator('[data-carousel-dot="8"]').click()
    page.wait_for_timeout(1500)
    card=page.locator('.chapter-card[data-card-label="豆包"]')
    card.locator('.card-face--front').click()
    page.wait_for_timeout(650)
    card.locator('.card-face__cta').click()
    page.wait_for_load_state('networkidle')
    assert page.url.endswith('/characters/doubao/')
    for width,height in [(390,844),(375,667)]:
        page.set_viewport_size({'width':width,'height':height})
        page.goto('http://127.0.0.1:4321/characters/doubao/',wait_until='networkidle')
        page.wait_for_timeout(2000)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert page.locator('.lanyard-canvas').bounding_box()['width']==width
        page.screenshot(path=str(out/f'react-bits-doubao-{width}.png'))
    assert not errors, errors
    assert not failed, failed
    browser.close()
print('PASS: nine React Bits pages and textures; native grab/release/free swing/flip; gallery navigation; mobile; no browser or HTTP errors')
