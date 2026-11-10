from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page()
 page.goto('http://127.0.0.1:4321/characters/doubao/',wait_until='domcontentloaded')
 page.locator('[data-edit-pass]').wait_for(state='visible')
 assert page.locator('[data-print-preview=front]').get_attribute('src').endswith('.webp')
 assert page.locator('[data-download-face=front]').get_attribute('href').endswith('.png')
 assert page.locator('[data-portrait-example]').first.get_attribute('data-example-src').endswith('.webp')
 page.locator('[data-edit-pass]').click()
 page.locator('[data-portrait-example]').first.click()
 assert page.locator('[data-portrait-crop]').evaluate('(d)=>d.open')
 b.close()
print('Optimized previews and full-resolution downloads verified')
