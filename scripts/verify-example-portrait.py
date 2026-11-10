"""Verify the bundled example portrait through crop, export, and reload."""
import os
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('BADGE_TEST_URL', 'http://127.0.0.1:4321').rstrip('/')


def ready(page):
    page.locator('[data-edit-pass]:not([disabled])').wait_for(timeout=30000)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 960}, accept_downloads=True)
    page = context.new_page()
    requests, errors = [], []
    page.on('request', lambda request: requests.append(request.url))
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(BASE + '/characters/doubao/', wait_until='networkidle')
    ready(page)
    assert page.locator('[data-portrait-example]').count() == 1, 'Editor has no default example portrait'
    assert not any('/img/examples/tangbao.png' in url for url in requests), 'Example loaded before opening the editor'
    page.locator('[data-edit-pass]').click()
    example = page.locator('[data-portrait-example]')
    assert example.is_visible()
    assert '糖包' in example.inner_text()
    thumbnail = example.locator('img')
    thumbnail.evaluate('image => image.decode()')
    assert thumbnail.evaluate('image => image.naturalWidth > 0')
    original = page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src')

    example.click()
    page.locator('[data-portrait-crop][open]').wait_for()
    canvas = page.locator('[data-crop-canvas]')
    assert canvas.evaluate('canvas => canvas.getContext("2d").getImageData(0, 0, 1, 1).data[3]') == 0
    assert canvas.evaluate('''async canvas => {
      const img = new Image();
      img.src = document.querySelector('[data-portrait-example]').dataset.exampleSrc;
      await img.decode();
      const expected = document.createElement('canvas');
      expected.width = canvas.width; expected.height = canvas.height;
      expected.getContext('2d').drawImage(img, 0, 0, expected.width, expected.height);
      return expected.toDataURL() === canvas.toDataURL();
    }'''), 'The crop does not show the bundled example'
    page.locator('[data-crop-cancel]').click()
    assert page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src') == original

    example.click()
    page.locator('[data-portrait-crop][open]').wait_for()
    page.locator('[data-crop-zoom]').evaluate("e => { e.value = '1.5'; e.dispatchEvent(new Event('input', { bubbles: true })); }")
    before = canvas.evaluate('c => c.toDataURL()')
    box = canvas.bounding_box()
    page.mouse.move(box['x'] + box['width'] * .7, box['y'] + box['height'] * .5)
    page.mouse.down()
    page.mouse.move(box['x'] + box['width'] * .3, box['y'] + box['height'] * .5, steps=8)
    page.mouse.up()
    assert canvas.evaluate('c => c.toDataURL()') != before, 'The example crop could not be adjusted'
    page.locator('[data-crop-apply]').click()
    assert page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src').startswith('data:image/png')
    page.locator('[data-edit-done]').click()
    page.locator('[data-badge-editor]').wait_for(state='hidden', timeout=30000)
    ready(page)
    page.locator('[data-badge-version=custom][aria-pressed=true]').wait_for()
    page.locator('[data-download-pass]').click()
    with page.expect_download() as single:
        page.locator('[data-download-face=front]').click()
    front_bytes = Path(single.value.path()).read_bytes()
    with page.expect_download() as zipped:
        page.locator('[data-download-zip]').click()
    with ZipFile(zipped.value.path()) as archive:
        front_name = next(name for name in archive.namelist() if name.endswith('-front.png'))
        assert archive.read(front_name) == front_bytes
    edited = Image.open(BytesIO(front_bytes)).convert('RGBA')
    original_image = Image.open(ROOT / 'public/downloads/zh/doubao-front.png').convert('RGBA')
    assert edited.size == (1200, 1688)
    assert ImageChops.difference(edited.crop((150, 150, 1050, 1150)), original_image.crop((150, 150, 1050, 1150))).convert('RGB').getbbox(), 'Example portrait did not reach the download'
    page.locator('[data-download-close]').click()
    page.reload(wait_until='networkidle')
    ready(page)
    page.locator('[data-badge-version=custom][aria-pressed=true]').wait_for(timeout=30000)
    page.locator('[data-edit-pass]').click()
    assert page.locator('[data-edit-scene] .badge-portrait img').get_attribute('data-print-src').startswith('data:image/png')
    page.locator('[data-portrait-reset]').click()
    page.locator('[data-edit-done]').click()
    page.locator('[data-badge-editor]').wait_for(state='hidden', timeout=30000)
    assert page.locator('[data-badge-version=custom]').is_hidden()

    mobile = browser.new_context(viewport={'width': 320, 'height': 568}, is_mobile=True, has_touch=True)
    touch = mobile.new_page()
    touch.goto(BASE + '/en/characters/doubao/', wait_until='networkidle')
    ready(touch)
    touch.locator('[data-edit-pass]').tap()
    assert touch.locator('[data-badge-editor]').evaluate('e => e.scrollWidth <= e.clientWidth')
    assert 'Tangbao' in touch.locator('[data-portrait-example]').inner_text()
    touch.locator('[data-portrait-example]').tap()
    touch.locator('[data-portrait-crop][open]').wait_for()
    touch.locator('[data-crop-cancel]').tap()
    mobile.close()

    # Finishing while the sample is still loading waits for the crop.
    pending = context.new_page()
    pending.add_init_script("""const decode = HTMLImageElement.prototype.decode;
      HTMLImageElement.prototype.decode = function() {
        if (!this.src.includes('/img/examples/tangbao.png')) return decode.call(this);
        const image = this;
        return new Promise((resolve, reject) => {
          window.releaseExampleDecode = () => decode.call(image).then(resolve, reject);
        });
      };""")
    pending.goto(BASE + '/characters/glm/', wait_until='networkidle')
    ready(pending)
    pending.locator('[data-edit-pass]').click()
    pending.locator('[data-portrait-example]').click()
    pending.wait_for_function("typeof window.releaseExampleDecode === 'function'")
    pending.locator('[data-edit-done]').click()
    assert pending.locator('[data-badge-editor]').evaluate('dialog => dialog.open')
    assert '正在读取' in pending.locator('[data-edit-status]').inner_text()
    pending.evaluate('window.releaseExampleDecode()')
    pending.locator('[data-portrait-crop][open]').wait_for()
    pending.locator('[data-crop-cancel]').click()
    pending.locator('[data-edit-done]').click()
    pending.locator('[data-badge-editor]').wait_for(state='hidden')
    pending.close()

    # A failed sample request gives feedback and local upload remains available.
    unavailable = context.new_page()
    unavailable.route('**/img/examples/tangbao.png', lambda route: route.abort())
    unavailable.goto(BASE + '/characters/qwen/', wait_until='networkidle')
    ready(unavailable)
    unavailable.locator('[data-edit-pass]').click()
    unavailable.locator('[data-portrait-example]').click()
    unavailable.wait_for_function("document.querySelector('[data-edit-status]').textContent.includes('示例图片加载失败')")
    assert not unavailable.locator('[data-portrait-crop]').evaluate('dialog => dialog.open')
    data = BytesIO()
    Image.new('RGB', (100, 100), 'green').save(data, 'PNG')
    unavailable.locator('[data-portrait-file]').set_input_files({'name': 'local.png', 'mimeType': 'image/png', 'buffer': data.getvalue()})
    unavailable.locator('[data-portrait-crop][open]').wait_for()
    unavailable.locator('[data-crop-cancel]').click()
    unavailable.close()

    assert not errors, errors
    context.close()
    browser.close()

print('PASS: bundled example, lazy loading, transparent crop, cancel, adjust, PNG/ZIP, reload, restore and mobile')
