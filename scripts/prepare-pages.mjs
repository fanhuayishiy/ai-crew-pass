// Keep originals in the source repository, but don't deploy unused historical art.
import { existsSync, readdirSync, statSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve, dirname, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import artwork from '../src/data/badge-artwork.json' with { type: 'json' };

const project = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dist = resolve(project, 'dist');
const editorImages = new Set(Object.values(artwork).flatMap(({ front, back, portrait }) => [front, back, portrait]));
editorImages.add('img/examples/tangbao.png');
for (const image of editorImages) {
  if (!existsSync(resolve(dist, image))) throw new Error(`Missing editor artwork: ${image}`);
}
if (process.env.GITHUB_PAGES_URL) {
  const hostname = new URL(process.env.GITHUB_PAGES_URL).hostname;
  const cname = resolve(dist, 'CNAME');
  if (hostname.endsWith('.github.io')) {
    if (existsSync(cname)) unlinkSync(cname);
  } else writeFileSync(cname, `${hostname}\n`);
}
const candidates = [];
function inspect(directory) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    const rel = relative(dist, path);
    if (rel.startsWith(`..${sep}`) || rel === '..' || path === dist) throw new Error('Invalid publish path');
    if (entry.isSymbolicLink()) throw new Error('Unexpected symlink in publish output');
    if (entry.isDirectory()) inspect(path);
    else {
      const webPath = rel.split(sep).join('/');
      const originalArt = /^img\/(characters|deepseek|gpt|glm|qwen|gemini|claude|kimi|grok|doubao)\/.+\.(png|jpe?g|webp)$/i.test(webPath);
      const archivedPrint = /^img\/badges\/(?:[^/]+\/)?[^/]+\.png$/i.test(webPath);
      if ((originalArt && !editorImages.has(webPath)) || archivedPrint) candidates.push({ path, bytes: statSync(path).size });
    }
  }
}
inspect(dist);
// Every resolved file above is verified beneath this project's dist; no source is touched.
for (const { path } of candidates) unlinkSync(path);
console.log(`Pages output: retained ${editorImages.size} editor images; excluded ${candidates.length} unused source images (${(candidates.reduce((n,f)=>n+f.bytes,0)/1024/1024).toFixed(1)} MiB); notices and downloads retained.`);
