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
        await browser.close()
    print('PASS: first card appears while 3D code is blocked; prefetch waits and 3D replaces preview')

asyncio.run(main())
