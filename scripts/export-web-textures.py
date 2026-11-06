"""Create full-resolution display textures; keep original PNG downloads unchanged."""
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[1]/'public/img/badges'
before=after=0
for locale in ['zh','en']:
    for source in (root/locale).glob('*.png'):
        target=source.with_suffix('.webp')
        with Image.open(source) as image:
            # Flat back-side typography compresses best losslessly.
            image.save(target,'WEBP',quality=94,method=6,lossless=source.stem.endswith('-back'))
        before+=source.stat().st_size
        after+=target.stat().st_size
print(f'Display textures: {before:,} -> {after:,} bytes ({(1-after/before)*100:.1f}% smaller); dimensions unchanged')
