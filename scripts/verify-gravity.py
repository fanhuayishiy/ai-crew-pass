"""Real-pointer gravity checks. Start `npm run dev` before running this script."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

out=Path(__file__).resolve().parents[1]/'docs/preview'
out.mkdir(exist_ok=True,parents=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for width,height,lift,side in [(1440,960,155,120),(390,844,90,30)]:
        page=browser.new_page(viewport={'width':width,'height':height})
        page.goto('http://127.0.0.1:4321/',wait_until='networkidle')
        page.wait_for_timeout(8500)
        read=lambda:page.evaluate('window.__lanyard')
        start=read()
        box=page.locator('.badge-card').bounding_box()
        x,y=box['x']+box['width']/2,box['y']+box['height']/2
        page.mouse.move(x,y)
        page.mouse.down()
        page.mouse.move(x+side,y-lift,steps=40)
        page.wait_for_timeout(1100)
        held=read()
        assert abs(held['rope']['length']-held['rope']['restLength'])<.01,'Lift shortened the strap'
        assert abs(held['com']['y']-start['com']['y']+lift)<9,'Held card drifted away from pointer'
        assert held['rope']['arc']-held['rope']['chord']>15,'Held strap did not become slack'
        hole=page.locator('.badge-hole').bounding_box()
        assert abs(hole['x']+hole['width']/2-held['clip']['x'])<3,'Clip detached horizontally'
        assert abs(hole['y']+hole['height']/2-held['clip']['y'])<3,'Clip detached vertically'
        page.screenshot(path=str(out/f'gravity-lift-{width}.png'))
        page.mouse.up()
        page.mouse.move(5,height-5)
        page.wait_for_timeout(220)
        drop=read()['com']['y']-held['com']['y']
        assert drop>25,('No gravity drop',width,drop)
        crossed=False
        for i in range(18):
            page.wait_for_timeout(200)
            if read()['com']['x']<width/2-3:crossed=True
        assert crossed,('Did not swing across centre',width)
        page.wait_for_timeout(6500)
        end=read()
        assert abs(end['com']['x']-width/2)<12,('Did not settle',end['com'])
        assert end['speed']<8,('Motion did not decay',end['speed'])
        print(json.dumps({'viewport':width,'drop_px':round(drop,1),'slack_px':round(held['rope']['arc']-held['rope']['chord'],1),'settled_speed':round(end['speed'],2)},ensure_ascii=False))
        page.close()
    browser.close()
print('PASS: desktop/mobile lift, slack, attachment, gravitational fall, swing-through and natural settling')
