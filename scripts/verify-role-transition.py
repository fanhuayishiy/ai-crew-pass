"""A role switch must not leave an unmoving preview over the entry animation."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, reduced_motion='no-preference')
        await context.add_init_script("localStorage.setItem('crew-pass-sound','off'); window.badgeArrived=0; document.addEventListener('badge-arrive',()=>window.badgeArrived++);")
        page = await context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.goto('http://127.0.0.1:4397/', wait_until='domcontentloaded')
        await page.locator('.lanyard[data-front-ready=true]').wait_for(timeout=20000)
        await page.locator('[data-crew-loading]').wait_for(state='hidden',timeout=10000)
        gate = asyncio.Event()
        async def hold_engine(route):
            await gate.wait()
            await route.continue_()
        await page.route('**/ReactBitsBadge.*.js', hold_engine)
        await page.locator('[data-role-next]').tap()
        await page.wait_for_url('**/characters/gpt/')
        await page.locator('.badge-loading-preview img[data-decoded=true]').wait_for(state='attached',timeout=20000)
        assert await page.locator('.badge-loading-preview').is_hidden()
        assert await page.locator('.badge-stage-loading').is_visible()
        assert await page.evaluate("document.documentElement.classList.contains('crew-role-switching')")
        gate.set()
        await page.locator('.lanyard[data-front-ready=true] .lanyard-canvas').wait_for(state='visible',timeout=20000)
        await page.wait_for_function('window.badgeArrived > 0',timeout=12000)
        assert await page.locator('.badge-loading-preview').is_hidden()
        assert await page.locator('.badge-stage-loading').is_hidden()
        assert not errors, errors
        await browser.close()
    print('PASS: muted role switch skips the frozen preview, waits for 3D, and plays the visible arrival')

asyncio.run(main())
