"""Smoke-test a built or deployed site at its actual base path."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import sys
from playwright.sync_api import sync_playwright

base=sys.argv[1].rstrip('/')+'/'
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce',accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    for locale in ['', 'en/']:
        for role in ['deepseek','gpt','glm','qwen','gemini','claude','kimi','grok','doubao']:
            route=locale+('' if role=='deepseek' else f'characters/{role}/')
            response=page.request.get(base+route)
            assert response.ok,(route,response.status)
            assert 'data-download-pass' in response.text(),route
    assert page.goto(base,wait_until='networkidle').ok
    assert page.locator('.lanyard-canvas,.badge-fallback').count()>=1
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('[data-open-community]').tap()
    qr=page.locator('.community-qrcode')
    assert qr.evaluate('async e=>{await e.decode();return e.naturalWidth===258}')
    with page.expect_download() as capture:
        page.locator('.community-save').tap()
    actual=Path(capture.value.path()).read_bytes()
    original=(root/'public/img/community/fenghua-ai-lab-wechat.jpg').read_bytes()
    assert hashlib.sha256(actual).digest()==hashlib.sha256(original).digest()
    page.locator('[data-close-community]').tap()
    page.locator('[data-language="en"]').tap()
    page.wait_for_url(base+'en/')
    assert page.locator('html').get_attribute('lang')=='en'
    page.locator('[data-role-next]').tap()
    page.wait_for_url(base+'en/characters/gpt/')
    page.locator('[data-download-pass]').tap()
    with page.expect_download() as capture:
        page.locator('[data-download-zip]').tap()
    assert capture.value.suggested_filename=='gpt-en-crew-pass.zip'
    with ZipFile(capture.value.path()) as archive:
        assert archive.testzip() is None
        assert archive.namelist()==['gpt-en-front.png','gpt-en-back.png']
    page.locator('[data-download-close]').tap()
    assert page.request.get(base+'social/cover.png').ok
    assert not errors,errors
    page.screenshot(path=str(root/'docs/preview/published-mobile.png'))
    browser.close()
print('PASS: '+base+' — 18 routes, actual base-path assets, mobile rendering, WeChat QR identity/download, language and character navigation, valid PNG ZIP, social cover, no page errors')
