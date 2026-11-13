"""Exercise the fictional Jensen pass at the supplied local or deployed base URL."""
from pathlib import Path
from io import BytesIO
import sys
from zipfile import ZipFile

from PIL import Image
from playwright.sync_api import sync_playwright


base = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:4473').rstrip('/')

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, args=['--use-angle=swiftshader'])
    context = browser.new_context(viewport={'width': 390, 'height': 844},
                                  is_mobile=True, has_touch=True, accept_downloads=True)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(base + '/', wait_until='domcontentloaded')
    page.evaluate("localStorage.setItem('crew-pass-version-v1', 'chibi')")

    for locale, disclosure, site_name in [('', '虚构', '万物工牌'), ('en/', 'fiction', 'Anything Pass')]:
        response = page.goto(f'{base}/{locale}characters/jensen/', wait_until='domcontentloaded')
        assert response and response.ok, f'{locale}Jensen route missing: {response.status if response else "no response"}'
        page.locator('[data-edit-pass]:not([disabled])').wait_for(timeout=60000)
        page.locator('.lanyard[data-front-ready=true], .badge-fallback img').first.wait_for(timeout=60000)
        assert page.locator('[data-badge-version=original]').get_attribute('aria-pressed') == 'true', 'A previous Q-version setting changed this pass'
        assert disclosure.lower() in page.locator('.fiction-notice').inner_text().lower(), 'Fictional status missing from page'
        assert page.locator('.fiction-notice').is_visible(), 'Fictional status is not visible'
        assert page.locator('.station-brand').inner_text() == site_name, 'Project name is out of date'
        assert page.locator('.contact-link').get_attribute('href') == 'https://mp.weixin.qq.com/s/TpxEZ5w_2Y_s24RlxZrL0g', 'Background link is incorrect'
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Page overflows on mobile'
        page.wait_for_function("!document.documentElement.classList.contains('crew-first-loading')", timeout=60000)
        image = Image.open(BytesIO(page.screenshot())).convert('RGB')
        red, green, blue = image.getpixel((5, 5))
        assert red < 150 and red > green * 1.3 and red > blue * 1.2, f'Background is too pale: {(red, green, blue)}'
        page.locator('[data-download-pass]').tap()
        with page.expect_download() as download:
            page.locator('[data-download-zip]').tap()
        with ZipFile(download.value.path()) as archive:
            assert archive.testzip() is None
            names = archive.namelist()
            assert any(name.endswith('-front.png') for name in names)
            assert any(name.endswith('-back.png') for name in names)
        page.locator('[data-download-close]').tap()
        if not locale:
            page.locator('[data-edit-pass]').tap()
            page.locator('[data-edit-scene] [data-badge-face=front] [data-edit-field=role]').evaluate('(element) => element.click()')
            page.locator('[data-edit-text]').fill('显卡体验官')
            page.locator('[data-edit-done]').tap()
            page.locator('[data-badge-editor]').wait_for(state='hidden', timeout=60000)
            assert page.locator('[data-download-face=front]').get_attribute('href').startswith('blob:'), 'Edited pass was not regenerated'

    page.goto(base + '/', wait_until='domcontentloaded')
    page.locator('[data-crew-picker] summary').tap()
    assert page.locator('.crew-roster a[href$="/characters/jensen/"]').count() == 1, 'Jensen pass missing from picker'
    assert not errors, errors
    context.close()
    browser.close()

print('PASS: Jensen routes, fiction disclosure, mobile layout, downloads and roster entry')
