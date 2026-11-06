"""Build same-origin PNG and ZIP downloads; browsers do no image processing."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parents[1]
size=(1200,1688)
mask=Image.new('L',size,0)
draw=ImageDraw.Draw(mask)
draw.rounded_rectangle((0,0,1199,1687),radius=50,fill=255)
draw.rounded_rectangle((468,64,731,111),radius=24,fill=0)
for locale in ['zh','en']:
    target=root/'public/downloads'/locale
    target.mkdir(exist_ok=True,parents=True)
    for front in (root/'public/img/badges'/locale).glob('*-front.png'):
        role=front.name.removesuffix('-front.png')
        paths=[]
        for face in ['front','back']:
            image=Image.open(front.with_name(f'{role}-{face}.png')).convert('RGBA').resize(size,Image.Resampling.LANCZOS)
            image.putalpha(mask)
            path=target/f'{role}-{face}.png'
            image.save(path,optimize=True)
            paths.append(path)
        with ZipFile(target/f'{role}-crew-pass.zip','w',ZIP_DEFLATED) as archive:
            for path in paths:
                archive.write(path,arcname=f'{role}-{locale}-{path.stem.rsplit("-",1)[1]}.png')
        print(locale,role,flush=True)
