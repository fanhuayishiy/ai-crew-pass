"""Regression: a slow back/strap must never hold the front face blank."""
import asyncio
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
from playwright.async_api import async_playwright

root=Path(__file__).resolve().parents[1]
out=root/'docs/preview'
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True)
        page=await browser.new_page(viewport={'width':1440,'height':960},reduced_motion='reduce')
        gate=asyncio.Event()
        blocked=[]
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        async def hold(route):
            blocked.append(route.request.url)
            await gate.wait()
            await route.continue_()
        await page.route('**/*-back.webp',hold)
        await page.route('**/*-strap.svg',hold)
        await page.goto('http://127.0.0.1:4321/characters/qwen/',wait_until='domcontentloaded')
        await page.locator('.lanyard[data-front-ready="true"]').wait_for(timeout=15000)
        assert not gate.is_set() and blocked, 'Test did not hold the secondary assets'
        assert await page.locator('link[rel="preload"][as="image"]').get_attribute('href')=='/img/badges/zh/qwen-front.webp'
        await page.screenshot(path=str(out/'front-with-secondary-assets-blocked.png'))
        starts=await page.evaluate('''()=>performance.getEntriesByType('resource').filter(e=>e.name.endsWith('/qwen-front.webp')).map(e=>({type:e.initiatorType,start:e.startTime,bytes:e.encodedBodySize}))''')
        assert len(starts)==1,starts
        assert starts[0]['type']=='link',starts
        gate.set()
        await page.wait_for_load_state('networkidle')
        # A neighboring front is warmed only after the current front is ready.
        await page.wait_for_function('performance.getEntriesByType("resource").some(e=>e.name.endsWith("/gemini-front.webp"))')
        print('Front visible while back/strap blocked; one early preload request:',starts,flush=True)
        await page.close()
        # All locale/role textures exist with identical pixel dimensions.
        png_bytes=webp_bytes=0
        for locale in ['zh','en']:
            for png in (root/'public/img/badges'/locale).glob('*.png'):
                webp=png.with_suffix('.webp')
                assert Image.open(webp).size==Image.open(png).size
                assert webp.stat().st_size<png.stat().st_size,(png.name,'oversized display texture')
                png_bytes+=png.stat().st_size
                webp_bytes+=webp.stat().st_size
                difference=ImageChops.difference(Image.open(webp).convert('RGB'),Image.open(png).convert('RGB'))
                assert max(ImageStat.Stat(difference).mean)<4, (png.name,'excessive compression error')
                assert webp.stat().st_size<450*1024,(webp.name,'display texture budget exceeded')
        assert webp_bytes<png_bytes*.35, (png_bytes,webp_bytes)
        assert not errors,errors
        await browser.close()
    print('PASS: front paints independently; one HTML preload; adjacent role prefetch; 36 smaller, full-resolution display textures')

asyncio.run(main())
