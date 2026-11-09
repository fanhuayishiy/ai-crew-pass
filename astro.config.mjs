// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import { existsSync, readFileSync } from 'node:fs';

// Derive Pages paths from the future repository; local development stays at /.
const pages = process.env.GITHUB_PAGES === '1';
const cnameFile = new URL('./public/CNAME', import.meta.url);
const customDomain = existsSync(cnameFile) ? readFileSync(cnameFile, 'utf8').trim() : '';
const [owner = 'fanhuayishiy', repository = 'ai-crew-pass'] = (process.env.GITHUB_REPOSITORY || 'fanhuayishiy/ai-crew-pass').split('/');
const pagesUrl = pages && process.env.GITHUB_PAGES_URL ? new URL(process.env.GITHUB_PAGES_URL) : undefined;

export default defineConfig({
  integrations: [react()],
  // 关掉 Astro 自带的 dev toolbar：它会明显拖慢帧率（实测首页 2fps ↔ 关闭后 50fps+），
  // 帧率被压到个位数时，吊牌翻转与滚动形变会被误判成 bug。
  devToolbar: { enabled: false },
  site: pagesUrl ? pagesUrl.origin : pages ? `https://${customDomain || `${owner}.github.io`}` : undefined,
  base: pagesUrl ? pagesUrl.pathname.replace(/\/$/, '') || '/' : pages ? (customDomain || repository === `${owner}.github.io` ? '/' : `/${repository}`) : undefined,
  // 样式全部内联：这样字体用相对路径 url('fonts/…') 也能在任意 base 下解析对
  build: { inlineStylesheets: 'always' },
  // Three.js 是唯一的重依赖（minify 后 ~500KB / gzip ~138KB），
  // Vite 默认 500KB 的 chunk 警告会把构建日志刷脏 —— 这里显式放宽并说明原因。
  vite: { build: { chunkSizeWarningLimit: 900 } },
});
