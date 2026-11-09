"""Regression checks for empty and oversized edited badge text."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 960})
    page.goto('http://127.0.0.1:4321/characters/gpt/', wait_until='networkidle')
    page.locator('[data-edit-pass]').click()
    alias = page.locator('[data-edit-scene] [data-edit-field=alias]')
    alias.click()
    page.locator('[data-edit-text]').fill('')
    page.locator('[data-edit-done]').click()
    page.locator('[data-badge-editor]').wait_for(state='hidden')
    page.reload(wait_until='networkidle')
    page.locator('[data-edit-pass]:not([disabled])').wait_for()
    page.locator('[data-edit-pass]').click()
    assert alias.is_visible(), 'Cleared alias cannot be selected again'
    alias.click()
    page.locator('[data-edit-text]').fill('新别名')
    name = page.locator('[data-edit-scene] [data-edit-field=name]')
    name.click()
    page.locator('[data-edit-text]').fill('这是一段比较长的自定义工牌名字用于测试显示效果')
    page.locator('[data-edit-done]').click()
    assert page.locator('[data-badge-editor]').evaluate('(e) => e.open'), 'Oversized name was exported'
    assert page.locator('[data-edit-status]').inner_text().strip(), 'No guidance for oversized name'
    page.locator('[data-edit-text]').fill('新名字')
    page.locator('[data-edit-side=back]').click()
    page.locator('[data-edit-scene] [data-edit-field=title-0]').click()
    page.locator('[data-edit-text]').fill('很长的标题内容' * 12)
    page.locator('[data-edit-done]').click()
    assert page.locator('[data-badge-editor]').evaluate('(e) => e.open'), 'Oversized back title was exported'
    page.locator('[data-edit-text]').fill('一起创造')
    page.locator('[data-edit-done]').click()
    page.locator('[data-badge-editor]').wait_for(state='hidden')
    page.reload(wait_until='networkidle')
    page.locator('[data-edit-pass]:not([disabled])').wait_for()
    page.locator('[data-edit-pass]').click()
    assert alias.inner_text() == '新别名'
    assert name.inner_text() == '新名字'
    browser.close()
print('PASS: cleared alias remains editable; oversized name blocks export; corrected text persists')
