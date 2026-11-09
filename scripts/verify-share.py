from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.add_init_script("Object.defineProperty(navigator, 'clipboard', {value: {writeText: async text => { window.copiedShare = text; }}, configurable: true})")
    for path, expected in [('/characters/gpt/', 'GPT'), ('/en/characters/gpt/', 'GPT')]:
        page.goto('http://127.0.0.1:4321' + path, wait_until='domcontentloaded')
        button = page.locator('[data-share]')
        assert button.is_visible()
        button.click()
        page.wait_for_function('window.copiedShare')
        copied = page.evaluate('window.copiedShare')
        assert copied == '\u4ee5\u5927\u80a5\u9c7c\u7684\u5de5\u724c\u505a\u597d\u4e86\uff0c\u5feb\u6765\u9886\u53d6\uff01\uff01\uff01\nhttp://127.0.0.1:4321' + path
        assert page.locator('[data-share-status]').inner_text()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    fallback = browser.new_page(viewport={'width': 375, 'height': 667})
    fallback.add_init_script("""Object.defineProperty(navigator, 'clipboard', {value: {writeText: async () => { throw new Error('denied'); }}, configurable: true});
      document.execCommand = command => { window.fallbackShare = document.activeElement.value; return command === 'copy'; };""")
    fallback.goto('http://127.0.0.1:4321/characters/gpt/', wait_until='domcontentloaded')
    fallback.locator('[data-share]').click()
    fallback.wait_for_function('window.fallbackShare')
    assert '/characters/gpt/' in fallback.evaluate('window.fallbackShare')
    browser.close()
print('PASS: localized share copies character text and current link on mobile')

