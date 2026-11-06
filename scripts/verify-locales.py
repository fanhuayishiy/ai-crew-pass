"""Verify bilingual routes, language-preserving links, print bounds and actual UI."""
from pathlib import Path
import re
from PIL import Image
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
out=root/'docs/preview'
out.mkdir(parents=True,exist_ok=True)
roles=['deepseek','gpt','glm','qwen','gemini','claude','kimi','grok','doubao']
strap_names=['DEEPSEEK','CHATGPT','GLM','QWEN','GEMINI','CLAUDE','KIMI','GROK','DOUBAO']
for role,name in zip(roles,strap_names):
    svg=ET.parse(root/f'public/img/badges/{role}-strap.svg')
    assert [el.text for el in svg.findall('.//{http://www.w3.org/2000/svg}text')]==[name,name],role
base='http://127.0.0.1:4321'
def route(role,lang):
    return ('/en' if lang=='en' else '')+('/' if role=='deepseek' else f'/characters/{role}/')

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    # Static text checks avoid spending GPU cycles on eighteen simultaneous simulations.
    page=browser.new_page(java_script_enabled=False,viewport={'width':1440,'height':960})
    for lang in ['zh','en']:
        for role in roles:
            assert page.goto(base+route(role,lang)).ok
            assert page.locator('html').get_attribute('lang')==('en' if lang=='en' else 'zh-CN')
            assert page.locator(f'[data-language="{lang}"]').get_attribute('aria-current')=='true'
            for other in ['zh','en']:
                assert page.locator(f'[data-language="{other}"]').get_attribute('href')==route(role,other)
            for link in page.locator('.character-switch a').all():
                assert link.get_attribute('href').startswith('/en/')==(lang=='en')
            for link in page.locator('.card-face__cta').all():
                assert link.get_attribute('href').startswith('/en/')==(lang=='en')
            if lang=='en':
                visible=page.locator('body').inner_text().replace('中文','')
                assert not re.search(r'[\u4e00-\u9fff]',visible),(role,visible)
            # Examine rendered print content, not the hidden legacy source.
            page.evaluate('''() => {
              const scene=document.createElement('div');scene.className='texture-export badge-scene badge-scene--interactive';
              scene.style.cssText='position:fixed;top:0;left:0;width:324px;height:455.625px';
              const card=document.querySelector('.badge-card').cloneNode(true);
              card.style.cssText='position:absolute;inset:0;transform:none;width:324px;height:455.625px';
              scene.append(card);document.body.append(scene);
            }''')
            for face in ['front','back']:
                if face=='back':
                    page.locator('.texture-export').evaluate('''e=>{e.querySelector('.badge-face--front').hidden=true;e.querySelector('.badge-face--back').hidden=false}''')
                el=page.locator(f'.texture-export .badge-face--{face}')
                assert el.evaluate('(e)=>e.scrollHeight<=e.clientHeight+1'),(lang,role,face,'clipped print')
                image=Image.open(root/f'public/img/badges/{lang}/{role}-{face}.png')
                assert abs(image.width/image.height-1.6/2.25)<.002,(lang,role,face,image.size)
            print(lang,role,flush=True)
    page.close()
    page=browser.new_page(viewport={'width':1440,'height':960},reduced_motion='reduce')
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(base+'/characters/doubao/',wait_until='networkidle')
    page.locator('[data-language="en"]').click()
    page.wait_for_load_state('networkidle')
    assert page.url.endswith('/en/characters/doubao/')
    page.locator('[data-crew-picker] summary').click()
    page.locator('.character-switch a').first.click()
    page.wait_for_load_state('networkidle')
    assert page.url.endswith('/en/')
    page.wait_for_timeout(2000)
    assert page.locator('.lanyard-canvas').count()==1
    page.screenshot(path=str(out/'bilingual-en-desktop.png'))
    page.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)')
    page.wait_for_timeout(1500)
    title=page.locator('.chapter-card[data-chapter-index="1"] .card-face--front > h3')
    assert title.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)<=15')
    assert title.evaluate('(e)=>getComputedStyle(e).zIndex')=='0'
    assert title.evaluate('(e)=>getComputedStyle(e).right')=='14px'
    assert page.locator('[data-chapter-panel]').count()==0
    assert abs(page.locator('#screen2').bounding_box()['y'])<2, 'Bottom scroll did not land at the archive'
    assert page.locator('.card-catchphrase > a').count()==9
    assert page.locator('.chapter-card[data-chapter-index="1"]').bounding_box()['width']>380
    page.locator('[data-open-credits]').click()
    assert page.locator('#credits').evaluate('(e)=>e.open')
    page.keyboard.press('Escape')
    assert not page.locator('#credits').evaluate('(e)=>e.open')
    box=page.locator('.chapter-card[data-chapter-index="1"]').bounding_box()
    assert abs(box['x']+box['width']/2-720)<2,box
    assert page.locator('.card-catchphrase').count()==9
    assert page.locator('.station-brand').inner_text().startswith('Nonhuman Employees')
    assert page.locator('.collection-heading').inner_text()=='Crew Pass Collection Desk'
    # Exercise both explicit navigation and direct horizontal dragging.
    page.locator('[data-carousel-next]').click()
    page.wait_for_timeout(700)
    assert page.locator('[data-carousel-count]').inner_text()=='02 / 09'
    page.locator('[data-carousel-previous]').click()
    page.wait_for_timeout(700)
    assert page.locator('[data-carousel-count]').inner_text()=='01 / 09'
    page.mouse.move(720,480)
    page.mouse.wheel(0,150)
    page.wait_for_timeout(700)
    assert page.locator('[data-carousel-count]').inner_text()=='02 / 09'
    page.locator('[data-carousel-dot="0"]').click()
    page.wait_for_timeout(700)
    page.mouse.move(720,480)
    page.mouse.down()
    page.mouse.move(370,480,steps=18)
    page.mouse.up()
    page.wait_for_timeout(900)
    assert page.locator('[data-carousel-count]').inner_text()!='01 / 09'
    page.locator('[data-carousel-dot="0"]').click()
    page.wait_for_timeout(700)
    page.screenshot(path=str(out/'bilingual-gallery.png'))
    page.locator('.chapter-card[data-chapter-index="1"] .card-face--front').click()
    page.wait_for_timeout(650)
    assert page.locator('.chapter-card[data-chapter-index="1"]').evaluate('(e)=>e.classList.contains("is-flipped")')
    assert 'server is busy' in page.locator('.chapter-card[data-chapter-index="1"] .card-catchphrase').inner_text()
    page.screenshot(path=str(out/'personnel-back-en.png'))
    page.locator('[data-carousel-dot="8"]').click()
    page.wait_for_timeout(1000)
    card=page.locator('.chapter-card[data-card-label="Doubao"]')
    card.locator('.card-face--front').click()
    page.wait_for_timeout(650)
    card.locator('.card-face__cta').click()
    page.wait_for_load_state('networkidle')
    assert page.url.endswith('/en/characters/doubao/')
    for width,height in [(390,844),(375,667)]:
        page.set_viewport_size({'width':width,'height':height})
        page.goto(base+'/en/',wait_until='networkidle')
        page.wait_for_timeout(1500)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert page.locator('[data-language="en"]').is_visible()
        page.screenshot(path=str(out/f'bilingual-en-{width}.png'))
        page.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)')
        page.wait_for_timeout(900)
        assert abs(page.locator('#screen2').bounding_box()['y'])<2, (width,'bottom landing')
        box=page.locator('.chapter-card[data-chapter-index="1"]').bounding_box()
        assert abs(box['x']+box['width']/2-width/2)<2,box
        assert box['y']>20
        page.locator('.chapter-card[data-chapter-index="1"] .card-face--front').click()
        page.wait_for_timeout(650)
        page.screenshot(path=str(out/f'personnel-back-{width}.png'))
        assert page.locator('.chapter-card[data-chapter-index="1"] .card-catchphrase').is_visible()
    assert not errors,errors
    browser.close()
print('PASS: 18 localized routes; 36 full-bleed print textures without clipped content; language/character/gallery navigation; small background titles; desktop and mobile')
