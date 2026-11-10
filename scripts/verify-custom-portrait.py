"""Exercise local portrait cropping, persistence, switching, and downloads."""
import os
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright


BASE = os.environ.get('BADGE_TEST_URL', 'http://127.0.0.1:4321').rstrip('/')


def fixture():
    image = Image.new('RGB', (1200, 600), (20, 225, 45))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 399, 599), fill=(245, 20, 35))
    draw.rectangle((800, 0, 1199, 599), fill=(20, 35, 245))
    data = BytesIO()
    image.save(data, 'PNG')
    return {'name': 'portrait.png', 'mimeType': 'image/png', 'buffer': data.getvalue()}


def wait_ready(page):
    page.locator('[data-edit-pass]:not([disabled])').wait_for(timeout=30000)


def upload(page):
    page.locator('[data-portrait-file]').set_input_files(fixture())
    page.locator('[data-portrait-crop][open]').wait_for()


def finish(page):
    page.locator('[data-edit-done]').click()
    page.locator('[data-badge-editor]').wait_for(state='hidden', timeout=30000)
    wait_ready(page)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 960}, accept_downloads=True)
    race = context.new_page()
    race.add_init_script("""const decode = HTMLImageElement.prototype.decode;
        HTMLImageElement.prototype.decode = function() {
          if (!this.src.startsWith('blob:')) return decode.call(this);
          const image = this;
          return new Promise((resolve, reject) => {
            window.releasePortraitDecode = () => {
              decode.call(image).then(() => { resolve(); window.portraitDecodeFinished = true; }, reject);
            };
          });
        };""")
    race.goto(BASE + '/characters/gpt/', wait_until='networkidle')
    wait_ready(race)
    race.locator('[data-edit-pass]').click()
    race.locator('[data-portrait-file]').set_input_files(fixture())
    race.wait_for_function("typeof window.releasePortraitDecode === 'function'")
    race.locator('[data-edit-done]').click()
    assert race.locator('[data-badge-editor]').evaluate('dialog => dialog.open')
    assert '正在读取' in race.locator('[data-edit-status]').inner_text()
    race.locator('[data-badge-editor]').evaluate('dialog => dialog.close()')
    race.evaluate('window.releasePortraitDecode()')
    race.wait_for_function('window.portraitDecodeFinished === true')
    assert not race.locator('[data-portrait-crop]').evaluate('dialog => dialog.open'), 'Crop opened after the editor was closed'
    race.close()

    # Finishing while an image is loading waits for its crop instead of exporting the old portrait.
    race = context.new_page()
    race.add_init_script("""const decode = HTMLImageElement.prototype.decode;
        HTMLImageElement.prototype.decode = function() {
          if (!this.src.startsWith('blob:')) return decode.call(this);
          const image = this;
          return new Promise((resolve, reject) => {
            window.releasePortraitDecode = () => {
              decode.call(image).then(() => { resolve(); window.portraitDecodeFinished = true; }, reject);
            };
          });
        };""")
    race.goto(BASE + '/characters/gpt/', wait_until='networkidle')
    wait_ready(race)
    race.locator('[data-edit-pass]').click()
    race.locator('[data-edit-scene] [data-edit-field=name]').click()
    race.locator('[data-edit-text]').fill('测试')
    race.locator('[data-portrait-file]').set_input_files(fixture())
    race.wait_for_function("typeof window.releasePortraitDecode === 'function'")
    race.locator('[data-edit-done]').click()
    assert race.locator('[data-badge-editor]').evaluate('dialog => dialog.open')
    assert '正在读取' in race.locator('[data-edit-status]').inner_text()
    assert not race.locator('[data-download-face=front]').get_attribute('href').startswith('blob:')
    race.evaluate('window.releasePortraitDecode()')
    race.wait_for_function('window.portraitDecodeFinished === true')
    race.locator('[data-portrait-crop][open]').wait_for()
    race.locator('[data-crop-cancel]').click()
    finish(race)
    assert race.locator('[data-badge-version=custom]').is_hidden()
    race.close()
    page = context.new_page()
    errors, uploads = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('request', lambda request: uploads.append(request.url) if request.method in ('POST', 'PUT', 'PATCH') else None)
    page.goto(BASE + '/characters/gpt/', wait_until='networkidle')
    wait_ready(page)
    page.locator('[data-edit-pass]').click()
    assert page.locator('[data-edit-upload]').count() == 1, 'Editor has no local portrait upload control'
    original_src = page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src')

    # Cancelling a crop leaves the original portrait in place.
    upload(page)
    page.locator('[data-crop-cancel]').click()
    assert page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src') == original_src

    # Invalid images give feedback and do not replace the current portrait.
    page.locator('[data-portrait-file]').set_input_files({'name': 'not-image.txt', 'mimeType': 'text/plain', 'buffer': b'not an image'})
    assert page.locator('[data-edit-status]').inner_text().strip()
    assert page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src') == original_src

    upload(page)
    canvas = page.locator('[data-crop-canvas]')
    assert canvas.evaluate('c => c.width === c.height && Math.abs(c.getBoundingClientRect().width - c.getBoundingClientRect().height) < 1')
    page.locator('[data-crop-zoom]').evaluate("e => { e.value = '2'; e.dispatchEvent(new Event('input', { bubbles: true })); }")
    before = canvas.evaluate('c => c.toDataURL()')
    box = canvas.bounding_box()
    page.mouse.move(box['x'] + box['width'] * .82, box['y'] + box['height'] / 2)
    page.mouse.down()
    page.mouse.move(box['x'] + box['width'] * .08, box['y'] + box['height'] / 2, steps=8)
    page.mouse.up()
    assert canvas.evaluate('c => c.toDataURL()') != before, 'Dragging did not move the crop'
    page.locator('[data-crop-apply]').click()
    page.locator('[data-portrait-crop]').wait_for(state='hidden')
    portrait = page.locator('[data-edit-scene] .badge-portrait img')
    assert portrait.get_attribute('data-print-src').startswith('data:image/png')
    page.locator('[data-edit-scene] [data-edit-field=name]').click()
    page.locator('[data-edit-text]').fill('我的搭子')
    finish(page)
    page.locator('[data-badge-version=custom][aria-pressed=true]').wait_for()
    page.wait_for_function("document.querySelector('[data-download-face=front]').href.startsWith('blob:')")
    page.locator('.lanyard[data-front-ready=true]').wait_for(timeout=30000)
    page.locator('[data-download-pass]').click()
    front_url = page.locator('[data-print-preview=front]').get_attribute('src')
    with page.expect_download() as single:
        page.locator('[data-download-face=front]').click()
    front_bytes = Path(single.value.path()).read_bytes()
    with page.expect_download() as zipped:
        page.locator('[data-download-zip]').click()
    with ZipFile(zipped.value.path()) as archive:
        front_name = next(name for name in archive.namelist() if name.endswith('-front.png'))
        assert archive.read(front_name) == front_bytes
    image = Image.open(BytesIO(front_bytes)).convert('RGBA')
    assert image.size == (1200, 1688)
    counts = image.convert('RGB').getcolors(image.width * image.height)
    assert any(count > 10000 and color == (20, 35, 245) for count, color in counts), 'Cropped blue area missing from PNG'
    assert any(count > 10000 and color == (20, 225, 45) for count, color in counts), 'Cropped green area missing from PNG'
    preview = page.evaluate('url => fetch(url).then(r => r.arrayBuffer()).then(b => Array.from(new Uint8Array(b)))', front_url)
    assert bytes(preview) == front_bytes, 'Preview and download do not match'
    page.locator('[data-download-close]').click()

    # Reload restores both custom artwork and edited text for this employee and locale.
    page.reload(wait_until='networkidle')
    wait_ready(page)
    page.locator('[data-badge-version=custom][aria-pressed=true]').wait_for(timeout=30000)
    page.locator('[data-edit-pass]').click()
    assert page.locator('[data-edit-scene] [data-edit-field=name]').inner_text() == '我的搭子'
    assert page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src').startswith('data:image/png')
    finish(page)

    # Original and chibi remain usable, and the custom portrait can be selected again.
    for style in ('original', 'chibi', 'custom'):
        button = page.locator(f'[data-badge-version={style}]')
        button.click()
        page.locator(f'[data-badge-version={style}][aria-pressed=true]:not([disabled])').wait_for(timeout=30000)
        page.locator('[data-edit-pass]').click()
        src = page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src')
        assert src.startswith('data:image/png') == (style == 'custom'), style
        if style == 'custom':
            assert page.locator('[data-edit-scene] .badge-portrait img').evaluate("e => getComputedStyle(e).transform === 'none'")
        finish(page)

    # A temporary storage failure during switching must be visible and retryable.
    page.evaluate("window.realIndexedDB = window.indexedDB; Object.defineProperty(window, 'indexedDB', { configurable: true, value: undefined })")
    page.locator('[data-badge-version=original]').click()
    page.locator('[data-badge-version=original][aria-pressed=true]:not([disabled])').wait_for(timeout=30000)
    assert '未能保存' in page.locator('[data-version-status]').inner_text(), 'A failed version save was not shown'
    page.evaluate("Object.defineProperty(window, 'indexedDB', { configurable: true, value: window.realIndexedDB })")
    page.locator('[data-edit-pass]').click()
    finish(page)
    page.reload(wait_until='networkidle')
    wait_ready(page)
    assert page.locator('[data-badge-version=original]').get_attribute('aria-pressed') == 'true'
    assert page.locator('[data-badge-version=custom]').is_visible(), 'Saved portrait disappeared after switching away'
    page.locator('[data-badge-version=custom]').click()
    page.locator('[data-badge-version=custom][aria-pressed=true]:not([disabled])').wait_for(timeout=30000)

    page.goto(BASE + '/en/characters/gpt/', wait_until='networkidle')
    wait_ready(page)
    assert page.locator('[data-badge-version=custom]').is_hidden(), 'Custom image leaked across locales'
    page.goto(BASE + '/characters/glm/', wait_until='networkidle')
    wait_ready(page)
    assert page.locator('[data-badge-version=custom]').is_hidden(), 'Custom image leaked across employees'
    page.goto(BASE + '/characters/gpt/', wait_until='networkidle')
    wait_ready(page)
    page.locator('[data-edit-pass]').click()
    page.locator('[data-portrait-reset]').click()
    assert not page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src').startswith('data:image/png')
    assert page.locator('[data-edit-scene] [data-edit-field=name]').inner_text() == '我的搭子'
    finish(page)
    assert page.locator('[data-badge-version=custom]').is_hidden()
    page.reload(wait_until='networkidle')
    wait_ready(page)
    assert page.locator('[data-badge-version=custom]').is_hidden(), 'Restored portrait returned after reload'

    # Touch-size layout and crop controls remain usable on a narrow screen.
    mobile = browser.new_context(viewport={'width': 320, 'height': 568}, is_mobile=True, has_touch=True)
    touch = mobile.new_page()
    touch.goto(BASE + '/en/characters/gpt/', wait_until='networkidle')
    wait_ready(touch)
    touch.locator('[data-edit-pass]').tap()
    upload(touch)
    assert touch.locator('[data-portrait-crop]').evaluate('e => e.scrollWidth <= e.clientWidth')
    touch.locator('[data-crop-zoom]').evaluate("e => { e.value = '2'; e.dispatchEvent(new Event('input', { bubbles: true })); }")
    touch_canvas = touch.locator('[data-crop-canvas]')
    before_touch = touch_canvas.evaluate('c => c.toDataURL()')
    box = touch_canvas.bounding_box()
    cdp = mobile.new_cdp_session(touch)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': box['x'] + box['width'] * .8, 'y': box['y'] + box['height'] / 2}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': box['x'] + box['width'] * .15, 'y': box['y'] + box['height'] / 2}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    assert touch_canvas.evaluate('c => c.toDataURL()') != before_touch, 'Touch dragging did not move the crop'
    touch.locator('[data-crop-apply]').tap()
    finish(touch)
    touch.locator('[data-badge-version=custom][aria-pressed=true]').wait_for()
    mobile.close()

    # A blocked browser database does not lose the current edit or hide the warning.
    blocked = browser.new_context(viewport={'width': 1440, 'height': 960})
    blocked.add_init_script("""if (!sessionStorage.getItem('allow-portrait-storage')) {
        window.realIndexedDB = window.indexedDB;
        Object.defineProperty(window, 'indexedDB', { configurable: true, value: undefined });
    }""")
    limited = blocked.new_page()
    limited.goto(BASE + '/characters/gpt/', wait_until='networkidle')
    wait_ready(limited)
    limited.locator('[data-edit-pass]').click()
    upload(limited)
    limited.locator('[data-crop-apply]').click()
    limited.locator('[data-edit-done]').click()
    limited.wait_for_function("!document.querySelector('[data-edit-pass]').disabled", timeout=30000)
    assert limited.locator('[data-badge-editor]').evaluate('e => e.open')
    assert '未能保存' in limited.locator('[data-edit-status]').inner_text()
    assert limited.locator('[data-download-face=front]').get_attribute('href').startswith('blob:')
    limited.evaluate("sessionStorage.setItem('allow-portrait-storage', '1'); Object.defineProperty(window, 'indexedDB', { configurable: true, value: window.realIndexedDB })")
    finish(limited)
    limited.reload(wait_until='networkidle')
    wait_ready(limited)
    limited.locator('[data-badge-version=custom][aria-pressed=true]').wait_for(timeout=30000)
    blocked.close()

    # If storage stays unavailable, the warning is shown before continuing for this visit.
    blocked = browser.new_context(viewport={'width': 1440, 'height': 960})
    blocked.add_init_script("Object.defineProperty(window, 'indexedDB', { value: undefined });")
    limited = blocked.new_page()
    limited.goto(BASE + '/characters/gpt/', wait_until='networkidle')
    wait_ready(limited)
    limited.locator('[data-edit-pass]').click()
    upload(limited)
    limited.locator('[data-crop-apply]').click()
    limited.locator('[data-edit-done]').click()
    limited.wait_for_function("!document.querySelector('[data-edit-pass]').disabled", timeout=30000)
    assert '未能保存' in limited.locator('[data-edit-status]').inner_text()
    finish(limited)
    assert limited.locator('[data-download-face=front]').get_attribute('href').startswith('blob:')
    blocked.close()

    assert not uploads, f'Local image operation made a write request: {uploads}'
    assert not errors, errors
    context.close()
    browser.close()

print('PASS: local upload, fixed-ratio crop, cancellation, invalid file, PNG/ZIP, persistence, style switching, isolation, restore, and mobile')
