"""A decoded first card can appear while the 3D engine is still downloading."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
        gate = asyncio.Event()
        errors = []
        async def hold(route):
            await gate.wait()
            await route.continue_()
        await page.route('**/ReactBitsBadge.*.js', hold)
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.goto('http://127.0.0.1:4397/', wait_until='domcontentloaded')
        await page.locator('[data-crew-loading]').wait_for(state='hidden', timeout=15000)
        assert await page.locator('.badge-loading-preview').is_visible()
        assert await page.locator('.badge-loading-preview img').evaluate('e=>e.complete&&e.naturalWidth===1296')
        assert await page.locator('.lanyard[data-front-ready=true]').count() == 0
        assert not await page.evaluate("performance.getEntriesByType('resource').some(e=>e.initiatorType==='fetch'&&e.name.includes('/img/badges/'))")
        gate.set()
        await page.locator('.lanyard[data-front-ready=true]').wait_for(timeout=20000)
        assert await page.locator('.badge-loading-preview').is_hidden()
        assert not errors, errors
        await page.close()
        page = await browser.new_page(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
        await page.add_init_script("sessionStorage.setItem('crew-first-ready','1')")
        image_gate = asyncio.Event()
        async def hold_image(route):
            await image_gate.wait()
            await route.continue_()
        await page.route('**/glm-front.webp', hold_image)
        await page.goto('http://127.0.0.1:4397/characters/glm/', wait_until='domcontentloaded')
        await page.locator('.lanyard-canvas').wait_for(state='attached', timeout=15000)
        assert await page.locator('.badge-stage-loading').is_visible()
        assert await page.locator('.badge-loading-preview img').is_hidden()
        assert await page.locator('.lanyard-canvas').is_hidden()
        image_gate.set()
        await page.locator('.lanyard[data-front-ready=true] .lanyard-canvas').wait_for(state='visible', timeout=20000)
        assert await page.locator('.badge-stage-loading').is_hidden()
        assert await page.locator('.badge-loading-preview').is_hidden()
        await page.close()
        page = await browser.new_page(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
        await page.add_init_script("sessionStorage.setItem('crew-first-ready','1')")
        await page.route('**/glm-front.webp', lambda route: route.fulfill(status=404, body=''))
        await page.goto('http://127.0.0.1:4397/characters/glm/', wait_until='domcontentloaded')
        await page.locator('[data-stage-retry]').wait_for(state='visible', timeout=15000)
        assert '加载失败' in await page.locator('[data-stage-loading-label]').inner_text()
        assert await page.locator('.lanyard-canvas').is_hidden()
        await browser.close()
    print('PASS: first preview, delayed image, and failed image with retry; unready card layers stay hidden')

asyncio.run(main())
