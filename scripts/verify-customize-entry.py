from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':390,'height':844})
 page.goto('http://127.0.0.1:4321/characters/grok/',wait_until='domcontentloaded')
 button=page.locator('.badge-controls [data-edit-pass]')
 button.click(timeout=15000)
 assert page.locator('[data-badge-editor]').evaluate('(d) => d.open')
 page.locator('[data-edit-done]').click()
 page.locator('[data-badge-editor]').wait_for(state='hidden')
 page.locator('[data-download-pass]').click()
 page.locator('[data-download-dialog] [data-open-customize]').click()
 assert not page.locator('[data-download-dialog]').evaluate('(d) => d.open')
 assert page.locator('[data-badge-editor]').evaluate('(d) => d.open')
 b.close()
print('Customization entry points verified')

