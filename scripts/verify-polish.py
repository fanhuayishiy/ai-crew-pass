"""Verify actual motion, compact roster and bottom-of-page archive landing."""
from pathlib import Path
from playwright.sync_api import sync_playwright

out=Path(__file__).resolve().parents[1]/'docs/preview'
out.mkdir(exist_ok=True,parents=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':960})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:4321/characters/glm/',wait_until='networkidle')
    shiny=page.locator('.home-watermark .shiny-text')
    shiny.wait_for()
    initial=shiny.evaluate('(e)=>e.style.backgroundImage')
    page.wait_for_function('(initial)=>document.querySelector(".home-watermark .shiny-text").style.backgroundImage!==initial',arg=initial,timeout=12000)
    page.screenshot(path=str(out/'polish-home.png'))
    picker=page.locator('[data-crew-picker]')
    assert not picker.evaluate('(e)=>e.open')
    picker.locator('summary').click()
    assert picker.evaluate('(e)=>e.open')
    assert page.locator('.crew-roster a:visible').count()==9
    assert page.locator('.crew-roster [aria-current="page"]').inner_text()=='GLM'
    page.locator('.crew-roster a').nth(4).hover()
    page.wait_for_timeout(400)
    page.screenshot(path=str(out/'polish-roster.png'))
    page.keyboard.press('Escape')
    assert not picker.evaluate('(e)=>e.open')
    page.keyboard.press('End')
    page.wait_for_function('Math.abs(document.querySelector("#screen2").getBoundingClientRect().y)<2', timeout=10000)
    assert abs(page.locator('#screen2').bounding_box()['y'])<2
    center=page.locator('.chapter-card[data-chapter-index="1"]')
    assert center.bounding_box()['width']>380
    page.screenshot(path=str(out/'polish-archive.png'))
    page.locator('[data-carousel-next]').click()
    page.wait_for_timeout(900)
    assert page.locator('[data-carousel-count]').inner_text()=='02 / 09'
    page.locator('[data-carousel-dot="0"]').click()
    page.wait_for_timeout(700)
    center.locator('.card-face--front').click()
    page.wait_for_timeout(700)
    assert center.evaluate('(e)=>e.classList.contains("is-flipped")')
    assert '服务器繁忙' in center.locator('.card-catchphrase').inner_text()
    page.screenshot(path=str(out/'polish-meme.png'))
    reduced=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
    reduced.on('pageerror',lambda e:errors.append(str(e)))
    reduced.goto('http://127.0.0.1:4321/en/characters/glm/',wait_until='networkidle')
    reduced.wait_for_timeout(500)
    quiet=reduced.locator('.home-watermark .shiny-text')
    still=quiet.evaluate('(e)=>e.style.backgroundImage')
    reduced.wait_for_timeout(800)
    assert quiet.evaluate('(e)=>e.style.backgroundImage')==still
    reduced.locator('[data-crew-picker] summary').click()
    reduced.screenshot(path=str(out/'polish-roster-mobile.png'))
    reduced.mouse.click(12,300)
    assert not reduced.locator('[data-crew-picker]').evaluate('(e)=>e.open')
    assert reduced.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert not errors,errors
    browser.close()
print('PASS: actual ShinyText motion; reduced motion; compact nine-person roster, hover and dismissal; End-key archive landing, larger cards, navigation and sourced memes')
