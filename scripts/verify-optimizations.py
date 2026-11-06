"""Verify the load-cost fix, print workflow and unsupported-WebGL fallback."""
from pathlib import Path
from playwright.sync_api import sync_playwright

out=Path(__file__).resolve().parents[1]/'docs/preview'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':960},reduced_motion='reduce')
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:4321/characters/claude/',wait_until='networkidle')
    assert page.locator('.lanyard-canvas').count()==1
    originals=page.evaluate('performance.getEntriesByType("resource").filter(e=>e.name.includes("/img/characters/")).map(e=>e.name)')
    assert not originals,originals
    # The hidden export source must still work when explicitly requested.
    assert page.locator('.badge-portrait img').evaluate('async e=>{e.src=e.dataset.printSrc;await e.decode();return e.naturalWidth>900}')
    page.locator('[data-open-credits]').click()
    for selector in ['[data-close-credits]']:
        button=page.locator(selector).bounding_box()
        icon=page.locator(selector+' svg').bounding_box()
        assert button['width']>=44 and button['height']>=44
        assert abs(button['x']+22-icon['x']-icon['width']/2)<.5
        assert abs(button['y']+22-icon['y']-icon['height']/2)<.5
    page.locator('[data-close-credits]').click()
    page.screenshot(path=str(out/'review-after.png'))
    page.close()
    for width,height in [(1440,960),(375,667)]:
        page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
        page.add_init_script('''() => {
            const get=HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext=function(type,...args) {
                return type==='webgl'||type==='webgl2'||type==='experimental-webgl' ? null : get.call(this,type,...args);
            };
        }'''.replace('() => {','(()=>{',1)+')();')
        page.goto('http://127.0.0.1:4321/en/characters/claude/',wait_until='networkidle')
        preview=page.locator('.badge-fallback > img')
        preview.wait_for()
        assert preview.get_attribute('src').endswith('claude-front.png')
        page.locator('[data-static-flip]').click()
        assert preview.get_attribute('src').endswith('claude-back.png')
        assert preview.evaluate('async e=>{await e.decode();return e.naturalWidth===1200}')
        page.screenshot(path=str(out/f'review-fallback-{width}.png'))
        flip=page.locator('[data-static-flip]').bounding_box()
        dock=page.locator('.badge-controls').bounding_box()
        assert flip['y']+flip['height']<dock['y'],(width,flip,dock)
        page.locator('[data-download-pass]').click()
        with page.expect_download() as capture:
            page.locator('[data-download-zip]').click()
        assert capture.value.suggested_filename=='claude-en-crew-pass.zip'
        page.close()
    assert not errors,errors
    browser.close()
print('PASS: no hidden full-resolution art request; explicit print source still decodes; centered 44px close target; WebGL-disabled fallback flips and downloads on desktop and mobile')
