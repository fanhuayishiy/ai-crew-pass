"""Create full-resolution display textures; keep original PNG downloads unchanged."""
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[1]/'public/img/badges'
before=after=0
for locale in ['zh','en']:
    for source in (root/locale).glob('*.png'):
        target=source.with_suffix('.webp')
        with Image.open(source) as image:
            # Keep native resolution for fine type; bounded high-quality compression
            # avoids carrying generated background noise in a lossless texture.
            temporary=target.with_suffix('.tmp.webp')
            image.save(temporary,'WEBP',quality=90 if source.stem.endswith('-back') else 92,method=6)
            temporary.replace(target)
        before+=source.stat().st_size
        after+=target.stat().st_size
print(f'Display textures: {before:,} -> {after:,} bytes ({(1-after/before)*100:.1f}% smaller); dimensions unchanged')
