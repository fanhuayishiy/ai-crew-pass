from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page()
 page.add_init_script('''(() => {
  Object.defineProperty(navigator, 'canShare', {value: data => !!data.files?.length, configurable: true});
  Object.defineProperty(navigator, 'share', {value: async data => { window.shared = {name: data.files[0].name, type: data.files[0].type, url: data.url, text: data.text}; }, configurable: true});
 })();''')
 page.goto('http://127.0.0.1:4321/characters/doubao/?version=chibi',wait_until='domcontentloaded')
 page.wait_for_selector('[data-badge-version=chibi][aria-pressed=true]')
 page.wait_for_function("!document.querySelector('[data-badge-version=chibi]').disabled")
 page.wait_for_timeout(1500)
 page.locator('[data-share]').click()
 page.wait_for_function('window.shared !== undefined',timeout=5000)
 shared=page.evaluate('window.shared')
 assert shared['type']=='image/png' and 'chibi' in shared['name'] and 'version=chibi' in shared['url'], shared
 page.goto('http://127.0.0.1:4321/characters/doubao/?version=tangbao',wait_until='domcontentloaded')
 page.wait_for_selector('[data-badge-version=tangbao][aria-pressed=true]',timeout=30000)
 page.wait_for_function("!document.querySelector('[data-badge-version=tangbao]').disabled",timeout=30000)
 page.wait_for_timeout(1500)
 page.locator('[data-share]').click()
 page.wait_for_function('window.shared !== undefined',timeout=5000)
 shared=page.evaluate('window.shared')
 assert 'tangbao' in shared['name'] and 'version=tangbao' in shared['url'], shared
 page.locator('[data-edit-pass]').click()
 editor=page.locator('[data-badge-editor]')
 editor.locator('[data-badge-face=front] [data-edit-field=name]').click()
 editor.locator('[data-edit-text]').fill('分享测试')
 editor.locator('[data-edit-done]').click()
 editor.wait_for(state='hidden',timeout=30000)
 page.wait_for_timeout(1500)
 page.evaluate('delete window.shared')
 page.locator('[data-share]').click()
 page.wait_for_function('window.shared !== undefined',timeout=5000)
 assert 'tangbao' in page.evaluate('window.shared.name')
 fallback=b.new_page()
 fallback.add_init_script('''(() => {
  Object.defineProperty(navigator, 'share', {value: undefined, configurable: true});
  Object.defineProperty(navigator, 'clipboard', {value: {writeText: async text => window.copied = text}, configurable: true});
 })();''')
 fallback.goto('http://127.0.0.1:4321/characters/grok/',wait_until='domcontentloaded')
 fallback.locator('[data-share]').click()
 assert 'version=original' in fallback.evaluate('window.copied')
 b.close()
print('Image sharing and text fallback verified')
