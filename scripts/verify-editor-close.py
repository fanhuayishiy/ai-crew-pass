from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':1280,'height':900})
 page.goto('http://127.0.0.1:4321/characters/doubao/',wait_until='domcontentloaded')
 page.locator('[data-edit-pass]').click(timeout=15000)
 editor=page.locator('[data-badge-editor]')
 editor.locator('[data-badge-face=front] [data-edit-field=name]').click()
 editor.locator('[data-edit-text]').fill('测试名字')
 editor.locator('[data-edit-close]').click(timeout=10000)
 editor.wait_for(state='hidden',timeout=30000)
 page.locator('[data-edit-pass]').click()
 assert editor.locator('[data-badge-face=front] [data-edit-field=name]').inner_text() == '测试名字'
 b.close()
print('Close saves changes and reopens')
