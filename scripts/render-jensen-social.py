"""Render the 1200 × 630 share card from the approved Jensen pass."""
import base64
from pathlib import Path

from playwright.sync_api import sync_playwright


root = Path(__file__).resolve().parents[1]
front = root / 'public/downloads/zh/jensen-front.png'
encoded = base64.b64encode(front.read_bytes()).decode('ascii')
html = f'''<!doctype html>
<meta charset="utf-8">
<style>
  * {{ box-sizing:border-box }}
  html,body {{ margin:0; width:1200px; height:630px; overflow:hidden; }}
  body {{ font-family:"Microsoft YaHei",sans-serif; color:#fff6f3;
    background:radial-gradient(circle at 73% 34%,#74202c 0,#3c111a 36%,#1c0c13 80%); }}
  .grid {{ position:absolute; inset:0; opacity:.15; background-image:linear-gradient(#f28d981e 1px,transparent 1px),linear-gradient(90deg,#f28d981e 1px,transparent 1px); background-size:36px 36px; }}
  .orbit {{ position:absolute; left:690px; top:-180px; width:760px; height:760px; border:1px solid #ffb0ad44; border-radius:50%; }}
  .copy {{ position:absolute; top:70px; left:76px; width:625px; }}
  .tag {{ display:inline-block; padding:9px 15px; border:1px solid #eea3a5; border-radius:50px; color:#ffd4ce; font-size:18px; font-weight:700; letter-spacing:.1em; }}
  h1 {{ margin:43px 0 20px; font-size:72px; line-height:1.1; letter-spacing:.015em; }}
  .sub {{ margin:0; color:#ffd9d4; font-size:30px; font-weight:600; }}
  .detail {{ margin:20px 0 0; color:#e6afb0; font-size:19px; }}
  .site {{ position:absolute; left:76px; bottom:66px; color:#e9adad; font-size:19px; letter-spacing:.1em; }}
  img {{ position:absolute; right:64px; top:30px; height:570px; width:auto; transform:rotate(5deg); filter:drop-shadow(0 22px 35px #0009); }}
</style>
<div class="grid"></div><div class="orbit"></div>
<div class="copy"><div class="tag">虚构玩梗 · 非真实入职</div><h1>老黄返厂了？</h1>
<p class="sub">出走半生，归来仍是打工人。</p><p class="detail">黑皮衣不换，这次换张红卡。</p></div>
<div class="site">BADGE.FHYSY.COM / AMD FAN PASS</div>
<img src="data:image/png;base64,{encoded}" alt="黄仁勋虚构 AMD 工牌">
'''
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
    page.set_content(html, wait_until='load')
    page.evaluate('document.fonts.ready')
    page.screenshot(path=str(root / 'public/social/jensen-cover.png'))
    browser.close()
print('Rendered public/social/jensen-cover.png')
