"""The front must never masquerade as the back during a slow image load."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, reduced_motion='reduce')
        gate = asyncio.Event()
        errors = []
        async def hold(route):
            await gate.wait()
            await route.continue_()
        await page.route('**/deepseek-back.webp', hold)
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.goto('http://127.0.0.1:4397/', wait_until='domcontentloaded')
        await page.locator('.lanyard[data-front-ready=true]').wait_for(timeout=20000)
        await page.locator('[data-crew-loading]').wait_for(state='hidden', timeout=10000)
        await page.wait_for_timeout(1000)
        await page.evaluate("document.addEventListener('badge-sound',e=>{if(e.detail==='flip')window.testFlip=(window.testFlip||0)+1})")
        await page.mouse.click(195,400)
        status = page.locator('[data-badge-back-status]')
        await status.wait_for(state='visible', timeout=5000)
        assert '加载工牌背面' in await status.inner_text()
        assert await page.evaluate('window.testFlip||0') == 0
        assert await page.locator('.lanyard').get_attribute('data-back-ready') == 'loading'
        gate.set()
        await page.wait_for_function('window.testFlip===1', timeout=12000)
        assert await page.locator('.lanyard').get_attribute('data-back-ready') == 'true'
        assert '背面已就绪' in await status.inner_text()
        await status.wait_for(state='hidden', timeout=3000)
        assert not errors, errors
        await page.close()
        page = await browser.new_page(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, reduced_motion='reduce')
        attempts = 0
        async def fail_first(route):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                await route.abort()
            else:
                await route.continue_()
        await page.route('**/deepseek-back.webp', fail_first)
        await page.goto('http://127.0.0.1:4397/', wait_until='domcontentloaded')
        await page.locator('.lanyard[data-back-ready=error]').wait_for(timeout=20000)
        await page.locator('[data-crew-loading]').wait_for(state='hidden', timeout=10000)
        await page.wait_for_timeout(1000)
        await page.mouse.click(195,400)
        await page.locator('.lanyard[data-back-ready=true]').wait_for(timeout=12000)
        assert attempts >= 2
        await browser.close()
    print('PASS: delayed back waits to flip, and a failed back reloads on the next tap')

asyncio.run(main())
