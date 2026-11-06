"""Mobile touch downloads, a single screen, safe controls and no-script fallback."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from zipfile import ZipFile

root=Path(__file__).resolve().parents[1]
out=root/'docs/preview'
out.mkdir(exist_ok=True,parents=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    errors=[]
    for width,height in [(320,568),(375,667),(390,844),(430,932)]:
        context=browser.new_context(viewport={'width':width,'height':height},is_mobile=True,has_touch=True,reduced_motion='reduce',accept_downloads=True)
        page=context.new_page()
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('http://127.0.0.1:4321/en/characters/gpt/',wait_until='networkidle')
        page.wait_for_timeout(700)
        assert page.locator('#screen2,.morph-runway,.morph-plane,.chapter-card,.brand-caption').count()==0
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert page.evaluate('document.documentElement.scrollHeight<=innerHeight+1')
        dock=page.locator('.badge-controls').bounding_box()
        foot=page.locator('.home-footer').bounding_box()
        assert dock['x']>=0 and dock['x']+dock['width']<=width
        assert dock['y']+dock['height']<foot['y'],(width,dock,foot)
        for selector in ['[data-role-previous]','[data-role-next]','[data-download-pass]']:
            assert page.locator(selector).evaluate('''e=>{const r=e.getBoundingClientRect();const hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return e.contains(hit)}'''),(width,selector,'blocked target')
        page.screenshot(path=str(out/f'single-screen-{width}.png'))
        page.locator('[data-download-pass]').tap()
        assert page.locator('[data-download-dialog]').evaluate('(e)=>e.open')
        with page.expect_download() as capture:
            page.locator('[data-download-zip]').tap()
        file=capture.value
        assert file.suggested_filename=='gpt-en-crew-pass.zip'
        with ZipFile(file.path()) as archive:
            assert archive.testzip() is None and len(archive.namelist())==2
        page.locator('[data-download-close]').tap()
        page.locator('[data-role-next]').tap()
        page.wait_for_url('**/en/characters/glm/')
        assert page.url.endswith('/en/characters/glm/')
        context.close()
        print('touch',width,height,flush=True)
    # Even blocked JavaScript must not turn the main download into a dead button.
    page=browser.new_page(java_script_enabled=False,accept_downloads=True)
    for language in ['zh','en']:
        for role in ['deepseek','gpt','glm','qwen','gemini','claude','kimi','grok','doubao']:
            route=('' if language=='zh' else '/en')+('/' if role=='deepseek' else f'/characters/{role}/')
            assert page.goto('http://127.0.0.1:4321'+route).ok
            assert page.locator('.collection-heading').count()==1
            assert page.locator('#screen2,.brand-caption').count()==0
            link=page.locator('[data-download-pass]')
            assert page.request.get('http://127.0.0.1:4321'+link.get_attribute('href')).ok
    with page.expect_download() as capture:
        page.locator('[data-download-pass]').click()
    assert capture.value.suggested_filename=='doubao-en-crew-pass.zip'
    assert not errors,errors
    browser.close()
print('PASS: four mobile sizes, actual touch ZIP downloads, unobstructed controls, locale-preserving arrows, 18 single-screen routes and download without JavaScript')
