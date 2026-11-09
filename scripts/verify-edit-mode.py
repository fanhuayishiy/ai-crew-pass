"""Exercise edited artwork through 3D, fallback, persistence and real downloads."""
import os
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageChops, ImageOps
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
out = root / 'docs/preview'
out.mkdir(parents=True, exist_ok=True)
base = os.environ.get('BADGE_TEST_URL', 'http://127.0.0.1:4321')


def wait_applied(page):
    page.wait_for_function("document.querySelector('[data-download-face=front]').href.startsWith('blob:')")
    page.locator('[data-edit-pass]:not([disabled])').wait_for()


def replace(page, field, text):
    page.locator(f'[data-edit-scene] [data-edit-field="{field}"]:visible').click()
    page.locator('[data-edit-text]').fill(text)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 960}, reduced_motion='reduce', accept_downloads=True)
    page = context.new_page()
    errors = []
    requests = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('request', lambda request: requests.append(request.url))
    page.goto(base + '/characters/gpt/', wait_until='networkidle')
    page.locator('.lanyard[data-front-ready="true"]').wait_for()
    page.locator('[data-edit-pass]').click()
    # Audit every text node and actually edit every visible field on both sides.
    for side in ['front', 'back']:
        page.locator(f'[data-edit-side={side}]').click()
        missing = page.locator(f'[data-edit-scene] [data-badge-face={side}]').evaluate('''face => {
            const walker = document.createTreeWalker(face, NodeFilter.SHOW_TEXT);
            const missing = [];
            while (walker.nextNode()) {
                const node = walker.currentNode;
                if (node.textContent.trim() && !node.parentElement.closest('[data-edit-field], [aria-hidden=true]')) missing.push(node.textContent);
            }
            return missing;
        }''')
        assert not missing, (side, 'Uneditable text', missing)
        fields = page.locator(f'[data-edit-scene] [data-badge-face={side}] [data-edit-field]:visible')
        for field in fields.all():
            before = field.inner_text()
            if not before:
                continue
            css = field.evaluate("element => { const s = getComputedStyle(element); return [s.fontFamily, s.fontSize, s.color, s.letterSpacing, s.lineHeight]; }")
            field.click()
            page.locator('[data-edit-text]').fill('测试' if side == 'front' else 'Test')
            assert field.inner_text() == ('测试' if side == 'front' else 'Test')
            assert field.evaluate("element => { const s = getComputedStyle(element); return [s.fontFamily, s.fontSize, s.color, s.letterSpacing, s.lineHeight]; }") == css
            page.locator('[data-edit-text]').fill(before)
    page.locator('[data-edit-side=front]').click()
    replace(page, 'name', '摸鱼搭子')
    replace(page, 'role', '<script>alert(1)</script>')
    assert page.locator('[data-edit-scene] .badge-role').inner_text() == '<script>alert(1)</script>'
    assert page.locator('[data-edit-scene] script').count() == 0
    replace(page, 'role', '创意部 / 摸鱼搭子')
    page.locator('[data-edit-side=back]').click()
    replace(page, 'kicker', 'Keep creating.')
    page.screenshot(path=str(out / 'edit-mode-back.png'))
    page.locator('[data-edit-done]').click()
    page.wait_for_function("!document.querySelector('[data-badge-editor]').open")
    wait_applied(page)
    page.locator('.lanyard[data-front-ready="true"][data-back-ready="true"]').wait_for()
    page.locator('[data-download-pass]').click()
    sources = page.locator('[data-print-preview]').evaluate_all('(images) => images.map(image => image.src)')
    assert all(source.startswith('blob:') for source in sources)
    assert all(source in requests for source in sources), '3D did not load the edited textures'
    page.screenshot(path=str(out / 'edited-downloads.png'))
    with page.expect_download() as captured:
        page.locator('[data-download-zip]').click()
    with ZipFile(captured.value.path()) as archive:
        assert archive.testzip() is None
        assert archive.namelist() == ['gpt-zh-front.png', 'gpt-zh-back.png']
        for side in ['front', 'back']:
            expected = archive.read(f'gpt-zh-{side}.png')
            image = Image.open(BytesIO(expected)).convert('RGBA')
            assert image.size == (1200, 1688)
            assert image.getpixel((0, 0))[3] == 0
            assert image.getpixel((600, 88))[3] == 0
            assert image.getpixel((600, 800))[3] == 255
            original = Image.open(root / f'public/downloads/zh/gpt-{side}.png').convert('RGBA')
            region = (80, 1100, 800, 1250) if side == 'front' else (90, 270, 1100, 450)
            assert ImageChops.difference(image.crop(region), original.crop(region)).convert('RGB').getbbox(), f'{side} text did not change'
            with page.expect_download() as single:
                page.locator(f'[data-download-face={side}]').click()
            assert Path(single.value.path()).read_bytes() == expected
            preview_bytes = page.evaluate('(url) => fetch(url).then(response => response.arrayBuffer()).then(buffer => Array.from(new Uint8Array(buffer)))', sources[0 if side == 'front' else 1])
            assert bytes(preview_bytes) == expected, 'Preview and download differ'
    page.keyboard.press('Escape')
    page.reload(wait_until='networkidle')
    wait_applied(page)
    page.locator('[data-edit-pass]').click()
    assert page.locator('[data-edit-scene] [data-edit-field=name]').inner_text() == '摸鱼搭子'
    page.keyboard.press('Escape')
    page.locator('[data-badge-editor]').wait_for(state='hidden')

    # Each locale and employee keeps its own content.
    page.goto(base + '/en/characters/gpt/', wait_until='networkidle')
    assert not page.locator('[data-download-face=front]').get_attribute('href').startswith('blob:')
    page.goto(base + '/characters/glm/', wait_until='networkidle')
    assert not page.locator('[data-download-face=front]').get_attribute('href').startswith('blob:')

    # The non-WebGL display consumes exactly the same images as download previews.
    fallback = context.new_page()
    fallback.add_init_script("""const original = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function(type, ...args) {
          return type.startsWith('webgl') ? null : original.call(this, type, ...args);
        };""")
    fallback.goto(base + '/characters/gpt/', wait_until='networkidle')
    wait_applied(fallback)
    fallback.locator('.badge-fallback').wait_for()
    assert fallback.locator('.badge-fallback img').get_attribute('src') == fallback.locator('[data-print-preview=front]').get_attribute('src')
    fallback.locator('[data-static-flip]').click()
    assert fallback.locator('.badge-fallback img').get_attribute('src') == fallback.locator('[data-print-preview=back]').get_attribute('src')
    fallback.close()
    page.goto(base + '/characters/gpt/', wait_until='networkidle')
    wait_applied(page)
    page.locator('[data-edit-pass]').click()
    page.locator('[data-edit-reset]').click()
    page.locator('[data-edit-done]').click()
    page.locator('[data-badge-editor]').wait_for(state='hidden')
    assert page.locator('[data-download-face=front]').get_attribute('href').endswith('/downloads/zh/gpt-front.png')
    assert page.evaluate("localStorage.getItem('crew-pass-edits-v1:gpt:zh')") is None

    for width, height in [(320, 568), (390, 844)]:
        mobile = browser.new_context(viewport={'width': width, 'height': height}, is_mobile=True, has_touch=True, reduced_motion='reduce', accept_downloads=True)
        touch = mobile.new_page()
        touch.goto(base + '/en/characters/gpt/', wait_until='networkidle')
        assert touch.evaluate('document.documentElement.scrollWidth <= innerWidth')
        touch.locator('[data-edit-pass]').tap()
        touch.locator('[data-edit-scene] [data-edit-field=name]').tap()
        touch.locator('[data-edit-text]').fill('My crew')
        touch.screenshot(path=str(out / f'edit-mode-mobile-{width}.png'))
        assert touch.locator('[data-badge-editor]').evaluate('element => element.scrollWidth <= element.clientWidth')
        touch.locator('[data-edit-done]').tap()
        touch.locator('[data-badge-editor]').wait_for(state='hidden')
        wait_applied(touch)
        touch.locator('[data-download-pass]').tap()
        with touch.expect_download() as download:
            touch.locator('[data-download-zip]').tap()
        assert download.value.suggested_filename == 'gpt-en-crew-pass.zip'
        mobile.close()

    effects = root / 'docs/edit-mode' if os.environ.get('BADGE_CAPTURE_EFFECTS') == '1' else out / 'edited-badges'
    effects.mkdir(parents=True, exist_ok=True)
    roles = [('deepseek', '鲸鱼同事'), ('gpt', '小白同事'), ('glm', '智谱同事'), ('qwen', '通义同事'), ('gemini', '星光同事'), ('claude', '暖橘同事'), ('kimi', '月光同事'), ('grok', '星际同事'), ('doubao', '元气同事')]
    for role, name in roles:
        card = context.new_page()
        card.set_viewport_size({'width': 1440, 'height': 1200})
        card.on('pageerror', lambda error: errors.append(str(error)))
        loaded = []
        card.on('request', lambda request: loaded.append(request.url))
        card.goto(base + ('/' if role == 'deepseek' else f'/characters/{role}/'), wait_until='networkidle')
        card.locator('[data-edit-pass]').click()
        for side in ['front', 'back']:
            card.locator(f'[data-edit-side={side}]').click()
            for field in card.locator(f'[data-edit-scene] [data-badge-face={side}] [data-edit-field]:visible').all():
                original = field.inner_text()
                if not original:
                    continue
                key = field.get_attribute('data-edit-field')
                replacements = {
                    'brand': original + '+', 'pass-type': 'TEAM PASS', 'name': name,
                    'alias': 'Teammate', 'role': '创意协作部 / 专属伙伴',
                    'portrait-label': f'CREW · {name}', 'seal': 'MY CREW',
                    'motto-0': '保持好奇，认真创造。', 'motto-1': '每个好点子，都值得实现。',
                    'code': 'CREW PASS · 创意协作部 · CUSTOM—001', 'unofficial': '个人定制工牌',
                    'kicker': 'Hello, teammate.', 'title-0': '一起创造，', 'title-1': '让灵感落地。',
                    'catchphrase-label': '我的宣言', 'catchphrase': '“保持好奇，一起创造。”',
                }
                value = replacements.get(key, '专属团队 · 携手创作')
                field.click()
                card.locator('[data-edit-text]').fill(value)
                assert field.inner_text() == value
        card.locator('[data-edit-done]').click()
        card.locator('[data-badge-editor]').wait_for(state='hidden')
        wait_applied(card)
        card.locator('.lanyard[data-front-ready="true"][data-back-ready="true"]').wait_for()
        card.locator('[data-download-pass]').click()
        preview_urls = card.locator('[data-print-preview]').evaluate_all('(images) => images.map(image => image.src)')
        assert all(url in loaded for url in preview_urls), (role, '3D did not use the edited faces')
        card.locator('[data-print-preview]').evaluate_all('(images) => Promise.all(images.map(image => image.decode()))')
        card.locator('[data-download-dialog]').screenshot(path=str(effects / f'{role}.png'))
        with card.expect_download() as zip_download:
            card.locator('[data-download-zip]').click()
        with ZipFile(zip_download.value.path()) as archive:
            assert archive.testzip() is None
            assert archive.namelist() == [f'{role}-zh-front.png', f'{role}-zh-back.png']
            for side in ['front', 'back']:
                with card.expect_download() as png_download:
                    card.locator(f'[data-download-face={side}]').click()
                assert Path(png_download.value.path()).read_bytes() == archive.read(f'{role}-zh-{side}.png')
                edited = Image.open(BytesIO(archive.read(f'{role}-zh-{side}.png'))).convert('RGBA')
                assert edited.size == (1200, 1688)
                assert edited.getpixel((0, 0))[3] == 0 and edited.getpixel((600, 88))[3] == 0
        print(f'PASS: {role}: every visible front/back field edited; 3D textures, preview, PNG and ZIP verified', flush=True)
        card.close()
    contact = Image.new('RGB', (1500, 2100), '#f5f4fa')
    for index, (role, _) in enumerate(roles):
        shot = ImageOps.contain(Image.open(effects / f'{role}.png').convert('RGB'), (480, 680))
        contact.paste(shot, ((index % 3) * 500 + (500 - shot.width) // 2, (index // 3) * 700 + 10))
    contact.save(effects / 'overview.png', optimize=True)

    assert not errors, errors
    context.close()
    browser.close()

print('PASS: front/back edits, literal text, shared 3D/fallback/preview artwork, real PNG/ZIP byte equality, alpha, reload, locale/employee isolation, reset and mobile touch downloads')
