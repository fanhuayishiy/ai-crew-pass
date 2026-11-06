"""Browser smoke check: run against `npm run dev` on port 4321."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

out = Path(__file__).resolve().parents[1] / 'docs' / 'preview'
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    errors = []
    page = browser.new_page(viewport={'width': 1440, 'height': 960}, device_scale_factor=1)
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://127.0.0.1:4321/', wait_until='networkidle')
    page.wait_for_timeout(7500)
    assert page.locator('.badge-scene--interactive').count() == 1
    body = page.locator('[data-badge-body3d]')
    assert body.count() == 1, 'Physical 3D badge body is missing'
    assert int(body.get_attribute('data-triangles') or '0') > 0, '3D body has not rendered'
    assert page.locator('.badge-portrait img').evaluate('(e) => e.complete && e.naturalWidth > 0')
    assert page.locator('.chapter-card').count() == 9
    assert page.locator('.badge-face--front').evaluate('(e) => e.scrollHeight <= e.clientHeight + 1'), 'Front content clipped'
    page.screenshot(path=str(out / 'desktop.png'))
    badge = page.locator('.badge-card')
    # Real pointer movement exercises the physical card, rather than DOM click().
    box = badge.bounding_box()
    x, y = box['x'] + box['width']/2, box['y'] + box['height']/2
    before = badge.get_attribute('style')
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x+130, y+45, steps=18)
    page.wait_for_timeout(120)
    assert badge.get_attribute('style') != before, 'Badge did not follow pointer'
    page.mouse.up()
    page.wait_for_timeout(7500)
    badge.click()
    page.wait_for_timeout(1500)
    assert page.locator('[data-badge-face="back"]').get_attribute('aria-hidden') == 'false'
    assert abs(float(body.get_attribute('data-flip')) - 180) < 0.1, 'Body did not follow the face flip'
    page.screenshot(path=str(out / 'back.png'))
    badge.focus()
    page.keyboard.press('Enter')
    page.wait_for_timeout(1200)
    assert page.locator('[data-badge-face="front"]').get_attribute('aria-hidden') == 'false'
    page.locator('#screen2').evaluate('(e) => e.scrollIntoView()')
    page.wait_for_timeout(2200)
    assert body.is_hidden(), '3D body remained behind after the badge morphed away'
    page.screenshot(path=str(out / 'cards.png'))
    page.locator('[data-carousel-dot="2"]').click()
    page.wait_for_timeout(1000)
    assert page.locator('[data-panel-title]').inner_text().startswith('GLM')
    assert page.locator('[data-panel-cta]').get_attribute('href') == '/characters/glm/'
    for width, height, name in [(390,844,'mobile'), (375,667,'mobile-small')]:
        mobile = browser.new_page(viewport={'width':width,'height':height}, device_scale_factor=1, is_mobile=True, has_touch=True)
        mobile.on('pageerror', lambda error: errors.append(str(error)))
        mobile.goto('http://127.0.0.1:4321/',wait_until='networkidle')
        mobile.wait_for_timeout(7500)
        assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
        assert mobile.locator('.badge-face--front').evaluate('(e) => e.scrollHeight <= e.clientHeight + 1'), 'Mobile front content clipped'
        bounds = mobile.locator('.badge-card').bounding_box()
        assert bounds['y'] > 60 and bounds['y']+bounds['height'] < height-60, bounds
        mobile.screenshot(path=str(out / f'{name}.png'))
        mobile.locator('#screen2').evaluate('(e) => e.scrollIntoView()')
        mobile.wait_for_timeout(1800)
        mobile.screenshot(path=str(out / f'{name}-cards.png'))
        mobile.close()
    reduced = browser.new_page(viewport={'width':1280,'height':800}, reduced_motion='reduce', color_scheme='dark')
    reduced.goto('http://127.0.0.1:4321/',wait_until='networkidle')
    assert reduced.locator('.badge-scene--reduced').count() == 1
    assert reduced.locator('.badge-portrait img').evaluate('(e) => e.complete && e.naturalWidth > 0')
    reduced.close()
    assert not errors, errors
    print(json.dumps({'result':'PASS','checks':['portrait loaded','9 character cards','real pointer drag','keyboard flip','carousel selection and target','390px and 375px layouts','reduced motion + dark OS preference','no page errors'],'screenshots':str(out)},ensure_ascii=False))
    browser.close()
