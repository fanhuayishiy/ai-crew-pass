"""Check real browser downloads, ZIP integrity, alpha and role navigation."""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from PIL import Image
from playwright.sync_api import sync_playwright

out=Path(__file__).resolve().parents[1]/'docs/preview'
out.mkdir(exist_ok=True,parents=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':960},reduced_motion='reduce',accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:4321/characters/gpt/',wait_until='networkidle')
    assert '人事档案室' not in page.locator('body').inner_text()
    assert page.locator('.social-links').get_by_text('官网',exact=True).count()==0
    star=page.locator('[data-project-star]')
    assert star.is_visible() and star.get_attribute('href')=='https://github.com/fanhuayishiy/ai-crew-pass'
    assert page.locator('[data-role-previous]').get_attribute('href')=='/'
    assert page.locator('[data-role-next]').get_attribute('href')=='/characters/glm/'
    page.locator('[data-download-pass]').click()
    page.locator('[data-download-zip]:not([aria-disabled])').wait_for()
    page.screenshot(path=str(out/'download-dialog.png'))
    with page.expect_download() as captured:
        page.locator('[data-download-zip]').click()
    download=captured.value
    assert download.suggested_filename=='gpt-zh-crew-pass.zip'
    download.save_as(str(out/'test-badge.zip'))
    with ZipFile(out/'test-badge.zip') as archive:
        assert archive.testzip() is None
        assert archive.namelist()==['gpt-zh-front.png','gpt-zh-back.png']
        for name in archive.namelist():
            im=Image.open(BytesIO(archive.read(name))).convert('RGBA')
            assert im.size==(1200,1688)
            assert im.getpixel((0,0))[3]==0, 'Corner was not transparent'
            assert im.getpixel((600,88))[3]==0, 'Punched slot was not transparent'
            assert im.getpixel((600,800))[3]==255, 'Card content was incorrectly transparent'
        with page.expect_download() as captured:
            page.locator('[data-download-face="front"]').click()
        single=captured.value
        assert single.suggested_filename=='gpt-zh-front.png'
        assert Path(single.path()).read_bytes()==archive.read('gpt-zh-front.png')
    page.keyboard.press('Escape')
    page.locator('[data-role-next]').click()
    page.wait_for_load_state('networkidle')
    assert page.url.endswith('/characters/glm/')
    page.locator('[data-language="en"]').click()
    page.wait_for_load_state('networkidle')
    assert page.locator('[data-role-next]').get_attribute('href')=='/en/characters/qwen/'
    assert page.locator('[data-role-previous]').get_attribute('href')=='/en/characters/gpt/'
    for width,height in [(390,844),(375,667)]:
        page.set_viewport_size({'width':width,'height':height})
        page.goto('http://127.0.0.1:4321/en/characters/glm/',wait_until='networkidle')
        assert page.locator('[data-project-star]').is_visible()
        assert page.locator('[data-role-next]').is_visible()
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=str(out/f'controls-mobile-{width}.png'))
        page.locator('[data-crew-picker] summary').click()
        assert page.locator('.crew-roster a:visible').count()==9
        assert page.locator('.crew-roster img').evaluate_all('(els)=>els.every(e=>e.src.includes("/img/avatars/"))')
        page.keyboard.press('Escape')
    assert not errors,errors
    browser.close()
print('PASS: front/back transparent PNGs, valid ZIP and matching individual download; prominent Star; removed archive heading/official link; role arrows and locale preservation; mobile and compact avatars')
