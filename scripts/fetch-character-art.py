"""Download original artwork from the referenced creator post, preserving provenance."""
import hashlib
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parents[1]
assets = {
    'deepseek': '1d6f202c991dbfb75b57fd68732d75e84168597.png',
    'gpt': '6e1c4e1bf7889d4da8455316b616c24b4168597.jpg',
    'glm': 'bd4e1c7e49fbb563549dc805c39cfb4c4168597.png',
    'qwen': '6c76a9b82a5885d5d08e4669833f06bf4168597.jpg',
    'gemini': '52eda1bac50135bd7aeae392c30cd6b24168597.jpg',
    'claude': '6736ad7d38500b04446144110a4451644168597.jpg',
    'kimi': '1f099083c8f81427754a9306733239164168597.png',
    'grok': 'b812d87ec38b8b13a6a6ef148b3aef3b4168597.jpg',
}

def download(item):
    name, remote = item
    url = 'https://i0.hdslb.com/bfs/new_dyn/' + remote
    target = root / 'public/img/characters' / (name + Path(remote).suffix)
    if not target.exists():
        with urlopen(Request(url, headers={'Referer':'https://www.bilibili.com/','User-Agent':'Mozilla/5.0'}),timeout=90) as response:
            content = response.read()
        target.write_bytes(content)
    from PIL import Image
    image = Image.open(target)
    return dict(id=name, file=target.name, source_url='https://www.bilibili.com/opus/1233069202138464289',
                download_url=url, author='上善无形 / ZipZipPipe' if name=='deepseek' else 'ZipZipPipe',
                license='See creator sharing statement; non-commercial fan use, retain attribution. DeepSeek: CC BY-NC-SA 4.0.',
                modifications='Original downloaded bytes; CSS display crop only.',width=image.width,height=image.height,
                sha256=hashlib.sha256(target.read_bytes()).hexdigest())

with ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(download, assets.items()))
doubao = root / 'public/img/characters/doubao-store.png'
generated_record = root / 'public/img/characters/doubao-anime-v4.source.json'
if not generated_record.exists():
    generated_record = root / 'public/img/characters/doubao-3d-v3.source.json'
if not generated_record.exists():
    generated_record = root / 'public/img/characters/doubao-anime-v2.source.json'
if generated_record.exists():
    records.append(json.loads(generated_record.read_text(encoding='utf-8')))
elif doubao.exists():
    from PIL import Image
    artwork = Image.open(doubao)
    records.append(dict(id='doubao', file=doubao.name,
        source_url='https://apps.microsoft.com/detail/xp99jw18tlbk06?gl=CN&hl=zh-CN',
        author='字节跳动 / 豆包', license='Brand artwork; rights reserved by original owner. Non-commercial product identification; not MIT.',
        modifications='Original downloaded bytes; CSS display crop only.',
        width=artwork.width,height=artwork.height,sha256=hashlib.sha256(doubao.read_bytes()).hexdigest()))
(root / 'public/img/characters/sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for record in records:
    print(record['id'],record['width'],record['height'])
