from playwright.sync_api import sync_playwright
from pathlib import Path
from zipfile import ZipFile
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 919}, accept_downloads=True)
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://127.0.0.1:4321/characters/doubao/', wait_until='domcontentloaded')
    page.locator('[data-badge-version="tangbao"]').click(timeout=15000)
    page.wait_for_selector('[data-badge-version="tangbao"][aria-pressed="true"]', timeout=30000)
    page.wait_for_function("!document.querySelector('[data-badge-version=tangbao]').disabled", timeout=30000)
    assert '围巾围好' in page.locator('.ocean-note__title').inner_text()
    page.screenshot(path='test-results-tangbao.png')
    page.locator('[data-edit-pass]').click()
    editor=page.locator('[data-badge-editor]')
    assert editor.locator('[data-badge-face="back"] [data-edit-field="catchphrase"]').inner_text() == '“阿巴阿巴阿巴”'
    assert editor.locator('[data-badge-face="front"] [data-edit-field="name"]').inner_text() == '糖包'
    editor.locator('[data-edit-side="back"]').click()
    editor.screenshot(path='test-results-tangbao-back.png')
    editor.locator('[data-edit-done]').click()
    editor.wait_for(state='hidden')
    with page.expect_download() as info:
        page.locator('[data-download-pass]').click()
        page.locator('[data-download-zip]').click()
    download = info.value
    assert 'tangbao' in download.suggested_filename
    with ZipFile(download.path()) as z:
        assert sorted(z.namelist()) == ['doubao-zh-tangbao-back.png', 'doubao-zh-tangbao-front.png']
    page.locator('[data-download-dialog]').evaluate('(dialog) => dialog.close()')
    page.locator('[data-badge-version="original"]').click()
    page.wait_for_selector('[data-badge-version="original"][aria-pressed="true"]')
    page.wait_for_function("!document.querySelector('[data-badge-version=original]').disabled", timeout=30000)
    assert '接住日常' in page.locator('.ocean-note__title').inner_text()
    assert not errors, errors
    browser.close()
print('Tangbao switching, editor, ZIP, and restoration passed')
