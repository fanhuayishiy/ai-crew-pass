"""Measure a cold load and navigation with constrained network bandwidth."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    static=browser.new_page(java_script_enabled=False)
    static.goto('http://127.0.0.1:4397/characters/qwen/',wait_until='networkidle')
    assert static.locator('.badge-loading-preview').is_visible()
    assert static.locator('.badge-loading-preview img').evaluate('e=>e.complete&&e.naturalWidth===1296')
    static.close()
    context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
    page=context.new_page()
    cdp=context.new_cdp_session(page)
    cdp.send('Network.enable')
    cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':80,'downloadThroughput':3_000_000/8,'uploadThroughput':750_000/8})
    result=[]
    for role in ['qwen','gemini']:
        if role=='qwen':
            page.goto('http://127.0.0.1:4397/characters/qwen/',wait_until='domcontentloaded')
        else:
            page.locator('[data-role-next]').click()
            page.wait_for_url('**/characters/gemini/')
        page.locator('.lanyard[data-front-ready="true"]').wait_for(timeout=30000)
        assert not page.locator('.badge-loading-preview').is_visible()
        metrics=page.evaluate('''()=>({readyMs:Math.round(performance.now()),images:performance.getEntriesByType('resource').filter(e=>e.name.endsWith('-front.webp')).map(e=>({name:e.name.split('/').pop(),startMs:Math.round(e.startTime),durationMs:Math.round(e.duration),bytes:e.encodedBodySize}))})''')
        metrics['role']=role
        assert metrics['images'] and metrics['images'][0]['bytes']<450*1024
        result.append(metrics)
        if role=='qwen':
            # Allow the real adjacent-front idle warmup to finish before clicking.
            page.wait_for_function('performance.getEntriesByType("resource").some(e=>e.name.endsWith("/gemini-front.webp")&&e.responseEnd>0)')
    browser.close()
(root/'docs/preview/crew-network-report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
