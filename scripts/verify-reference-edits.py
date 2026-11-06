"""Verify user-supplied catchphrases, clean card backs and centered close icons."""
from pathlib import Path
from playwright.sync_api import sync_playwright

out=Path(__file__).resolve().parents[1]/'docs/preview'
expected={
 'deepseek':'嗯，用户想要……', 'gpt':'You’re absolutely right!（你完全正确！）',
 'glm':'我是智谱 AI 训练的 GLM', 'qwen':'Okay, let me think...',
 'gemini':'That’s a great question!（这是个绝妙的问题！）',
 'claude':'I apologize for the confusion.（抱歉，这是我的误解。）',
 'kimi':'我是 Claude', 'grok':'马斯克比勒布朗更强壮。', 'doubao':'对不起，你说得对！',
}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(java_script_enabled=False)
 for locale in ['zh','en']:
  for role,phrase in expected.items():
   path=('' if locale=='zh' else '/en')+('/' if role=='deepseek' else f'/characters/{role}/')
   assert page.goto('http://127.0.0.1:4321'+path).ok
   assert page.locator('.badge-back-credit').count()==0
   if locale=='zh': assert phrase in page.locator('.badge-catchphrase').text_content(),role
   assert page.locator('.station-heading .collection-heading').count()==1
   page.evaluate('''()=>{
    const e=document.querySelector('.legacy-badge-scene');e.classList.remove('legacy-badge-scene');e.classList.add('texture-export');
    e.style.cssText='position:fixed;top:0;left:0;width:324px;height:455.625px;visibility:visible';
    const card=e.querySelector('.badge-card');card.style.cssText='position:absolute;top:0;left:0;transform:none;width:324px;height:455.625px';
    e.querySelector('.badge-face--front').hidden=true;e.querySelector('.badge-face--back').hidden=false;
   }''')
   assert page.locator('.badge-face--back').evaluate('(e)=>e.scrollHeight<=e.clientHeight+1'),(role,locale,'clipped back')
 page.close()
 errors=[]
 for width,height in [(1440,960),(375,667)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4321/characters/glm/',wait_until='networkidle')
  page.wait_for_timeout(700)
  page.screenshot(path=str(out/f'reference-home-{width}.png'))
  for trigger,selector,name in [('[data-open-credits]','[data-close-credits]','credits'),('[data-download-pass]','[data-download-close]','download')]:
   page.locator(trigger).click()
   button=page.locator(selector).bounding_box();icon=page.locator(selector+' svg').bounding_box()
   assert abs(button['x']+button['width']/2-icon['x']-icon['width']/2)<.5
   assert abs(button['y']+button['height']/2-icon['y']-icon['height']/2)<.5
   page.screenshot(path=str(out/f'reference-{name}-{width}.png'))
   page.locator(selector).click()
  page.close()
 assert not errors,errors
 browser.close()
print('PASS: nine user-specified catchphrases, 18 unclipped card backs without credit blocks; compact identity; both dialog close icons centered on desktop and mobile')
