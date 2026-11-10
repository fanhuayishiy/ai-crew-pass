"""Exercise the selected version, downloadable faces and persisted preference."""
from io import BytesIO
import os
from pathlib import Path
from zipfile import ZipFile

from PIL import Image
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
base = os.environ.get('CREW_PASS_TEST_URL', 'http://127.0.0.1:4321').rstrip('/')
ids = ['deepseek', 'gpt', 'glm', 'qwen', 'gemini', 'claude', 'kimi', 'grok', 'doubao']
for locale in ('zh', 'en'):
    for character in ids:
        directory = root / 'public' / 'downloads' / locale
        front = directory / f'{character}-chibi-front.png'
        with Image.open(front) as im:
            assert im.size == (1200, 1688) and im.getpixel((0, 0))[3] == 0
            assert im.getpixel((600, 85))[3] == 0  # strap slot
        with ZipFile(directory / f'{character}-chibi-crew-pass.zip') as archive:
            assert archive.read(f'{character}-{locale}-chibi-front.png') == front.read_bytes()
            assert archive.read(f'{character}-{locale}-back.png') == (directory / f'{character}-back.png').read_bytes()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(base + '/', wait_until="domcontentloaded")
    for locale in ('zh', 'en'):
        for character in ids:
            for path in (f'/img/badges/{locale}/{character}-chibi-front.webp',
                         f'/downloads/{locale}/{character}-chibi-front.png',
                         f'/downloads/{locale}/{character}-chibi-crew-pass.zip'):
                assert page.request.head(base + path).status == 200, path
    page.locator('[data-badge-version="chibi"]').click(timeout=15000)
    page.locator('[data-badge-version="chibi"][aria-pressed="true"]').wait_for()
    page.locator('[data-download-pass]').click()
    page.locator('[data-download-dialog][open]').wait_for()
    assert 'chibi' in page.locator('[data-download-face="front"]').get_attribute('href')
    assert 'chibi' in page.locator('[data-download-zip]').get_attribute('href')
    page.locator('[data-download-close]').click()
    page.locator('[data-edit-pass]').click()
    page.locator('[data-badge-editor] [data-badge-face="front"] [data-edit-field="name"]').click()
    page.locator('[data-edit-text]').fill('小鱼')
    page.locator('[data-edit-done]').click()
    page.locator('[data-badge-editor]').wait_for(state='hidden', timeout=30000)
    page.locator('[data-download-pass]').click()
    front_url = page.locator('[data-download-face="front"]').get_attribute('href')
    assert front_url.startswith('blob:')
    with page.expect_download() as download_info:
        page.locator('[data-download-zip]').click()
    download = download_info.value
    assert 'chibi' in download.suggested_filename
    with ZipFile(download.path()) as archive:
        assert sorted(archive.namelist()) == ['deepseek-zh-chibi-back.png', 'deepseek-zh-chibi-front.png']
        with Image.open(BytesIO(archive.read('deepseek-zh-chibi-front.png'))) as im:
            assert im.size == (1200, 1688) and im.getpixel((0, 0))[3] == 0
    page.locator('[data-download-close]').click()
    page.locator('[data-badge-version="original"]').click()
    page.locator('[data-badge-version="original"][aria-pressed="true"]').wait_for(timeout=30000)
    page.wait_for_function("document.querySelector('[data-badge-version=original]').disabled === false", timeout=30000)
    page.locator('[data-download-pass]').click()
    assert 'chibi' not in page.locator('[data-download-zip]').get_attribute('download')
    assert page.locator('[data-download-face="front"]').get_attribute('href') != front_url
    page.locator('[data-download-close]').click()
    page.locator('[data-badge-version="chibi"]').click()
    page.wait_for_function("document.querySelector('[data-badge-version=chibi]').disabled === false", timeout=30000)
    page.reload(wait_until="domcontentloaded")
    page.locator('[data-badge-version="chibi"][aria-pressed="true"]').wait_for(timeout=15000)
    page.goto(base + '/en/characters/gemini/', wait_until='domcontentloaded')
    page.locator('[data-badge-version="chibi"][aria-pressed="true"]').wait_for(timeout=15000)
    page.locator('[data-download-pass]').click()
    assert 'gemini' in page.locator('[data-download-face="front"]').get_attribute('href')
    assert 'chibi' in page.locator('[data-download-face="front"]').get_attribute('href')
    assert not errors, errors
    browser.close()
print('Q version switching and downloads verified')
