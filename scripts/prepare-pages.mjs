// Keep originals in the source repository, but don't deploy unused historical art.
import { readdirSync, statSync, unlinkSync } from 'node:fs';
import { resolve, dirname, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const project = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dist = resolve(project, 'dist');
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
      if (originalArt || archivedPrint) candidates.push({ path, bytes: statSync(path).size });
    }
  }
}
inspect(dist);
// Every resolved file above is verified beneath this project's dist; no source is touched.
for (const { path } of candidates) unlinkSync(path);
console.log(`Pages output: excluded ${candidates.length} unused source images (${(candidates.reduce((n,f)=>n+f.bytes,0)/1024/1024).toFixed(1)} MiB); source, notices and downloads retained.`);
