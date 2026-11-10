"""Generate lightweight transparent download previews and editor examples.

Run after updating source assets. Original PNGs and ZIP downloads are preserved.
Requires Pillow with WebP support.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def write_preview(source: Path) -> None:
    dest = ROOT / 'public' / 'img' / 'previews' / source.parent.name / f'{source.stem}.webp'
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = image.convert('RGBA')
        image.thumbnail((600, 844), Image.Resampling.LANCZOS)
        image.save(dest, 'WEBP', quality=88, method=4, exact=True)


def main() -> None:
    downloads = sorted((ROOT / 'public' / 'downloads').glob('*/*.png'))
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(write_preview, downloads))
    for name in ('tangbao', 'nailong', 'liangsheng'):
        source = ROOT / 'public' / 'img' / 'examples' / f'{name}.png'
        with Image.open(source) as image:
            image.save(source.with_suffix('.webp'), 'WEBP', quality=94, method=6, exact=True)
    print(f'Generated {len(downloads)} transparent previews and 3 editor examples.')


if __name__ == '__main__':
    main()
