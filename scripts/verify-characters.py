"""Verify all nine character pages, links, artwork, themes, and small screens."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
out=root/'docs/preview'
out.mkdir(exist_ok=True,parents=True)
ids=['deepseek','gpt','glm','qwen','gemini','claude','kimi','grok','doubao']
colors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    errors=[]
    page=browser.new_page(viewport={'width':1440,'height':960},device_scale_factor=2,reduced_motion='reduce')
    page.on('pageerror',lambda e:errors.append(str(e)))
    for id in ids:
        path='/' if id=='deepseek' else f'/characters/{id}/'
        response=page.goto('http://127.0.0.1:4321'+path,wait_until='networkidle')
        assert response.status==200,(id,response.status)
        assert page.locator('[data-character-id]').get_attribute('data-character-id')==id
        assert page.locator('[data-profile-github]').get_attribute('href')=='https://github.com/fanhuayishiy'
        assert page.locator('.character-switch a').count()==9
        assert page.locator('.chapter-card').count()==9
        assert page.locator('.badge-portrait img').evaluate('(e)=>e.complete && e.naturalWidth>=900'),id
        assert page.locator('.badge-face--front').evaluate('(e)=>e.scrollHeight<=e.clientHeight+1'),id
        colors.append(page.evaluate('getComputedStyle(document.documentElement).getPropertyValue("--theme-brand").trim()'))
        page.screenshot(path=str(out/f'{id}-desktop.png'))
    assert len(set(colors))==9,colors
    # Navigate from the gallery, using a real card-back CTA.
    page.goto('http://127.0.0.1:4321/',wait_until='networkidle')
    page.locator('.character-switch a').last.click()
    page.wait_for_load_state('networkidle')
    assert page.url.endswith('/characters/doubao/')
    page.goto('http://127.0.0.1:4321/',wait_until='networkidle')
    page.locator('#screen2').evaluate('(e)=>e.scrollIntoView()')
    page.wait_for_timeout(1500)
    assert page.locator('[data-badge-body3d]').is_hidden(), 'Idle body remained during the gallery'
    page.locator('[data-carousel-dot="8"]').click()
    page.wait_for_timeout(1500)
    doubao=page.locator('.chapter-card[data-card-label="豆包"]')
    doubao.locator('.card-face--front').click()
    page.wait_for_timeout(650)
    doubao.locator('.card-face__cta').click()
    page.wait_for_load_state('networkidle')
    assert page.url.endswith('/characters/doubao/')
    for id in ['deepseek','gpt','doubao']:
        for width,height in [(390,844),(375,667)]:
            page.set_viewport_size({'width':width,'height':height})
            path='/' if id=='deepseek' else f'/characters/{id}/'
            page.goto('http://127.0.0.1:4321'+path,wait_until='networkidle')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(id,width)
            selected=page.locator('.character-switch [aria-current="page"]').bounding_box()
            switcher=page.locator('.character-switch').bounding_box()
            assert selected['x']>=switcher['x']-1 and selected['x']+selected['width']<=switcher['x']+switcher['width']+1,(id,width,selected)
            assert page.locator('.badge-face--front').evaluate('(e)=>e.scrollHeight<=e.clientHeight+1'),(id,width)
            page.screenshot(path=str(out/f'{id}-{width}.png'))
    assert not errors,errors
    browser.close()
print('PASS: nine character routes, nine distinct themes, original-resolution art, owner GitHub, character navigation, mobile layouts, no page errors')
