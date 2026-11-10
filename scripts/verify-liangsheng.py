from playwright.sync_api import sync_playwright
from zipfile import ZipFile
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':1280,'height':900},accept_downloads=True)
 page.goto('http://127.0.0.1:4321/?version=liangsheng',wait_until='domcontentloaded')
 page.wait_for_selector('[data-badge-version=liangsheng][aria-pressed=true]',timeout=15000)
 page.wait_for_function("!document.querySelector('[data-badge-version=liangsheng]').disabled",timeout=30000)
 assert '梁圣一出' in page.locator('.ocean-note__title').inner_text()
 page.locator('[data-edit-pass]').click()
 editor=page.locator('[data-badge-editor]')
 assert editor.locator('[data-badge-face=front] [data-edit-field=name]').inner_text() == '梁圣'
 assert editor.locator('[data-badge-face=front] [data-edit-field=motto-1]').inner_text() == '嘘，正在深度思考。'
 assert editor.locator('[data-badge-face=back] [data-edit-field=catchphrase-label]').inner_text() == '社区梗'
 assert editor.locator('[data-badge-face=back] [data-edit-field=catchphrase]').inner_text() == '“梁圣的恩情还不完！”'
 editor.locator('[data-edit-done]').click(); editor.wait_for(state='hidden')
 page.locator('[data-download-pass]').click()
 with page.expect_download() as info: page.locator('[data-download-zip]').click()
 with ZipFile(info.value.path()) as z: assert sorted(z.namelist()) == ['deepseek-zh-liangsheng-back.png','deepseek-zh-liangsheng-front.png']
 page.locator('[data-download-dialog]').evaluate('(d) => d.close()')
 page.locator('[data-badge-version=original]').click()
 page.wait_for_function("!document.querySelector('[data-badge-version=original]').disabled",timeout=30000)
 assert 'liangsheng' not in page.locator('[data-download-zip]').get_attribute('download')
 b.close()
print('Liangsheng faces, link, downloads, and switching verified')
