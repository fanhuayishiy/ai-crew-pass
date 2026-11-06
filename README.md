# 非人类员工 · Nonhuman Employees

九位 AI 模型的非官方同人工牌领取页，支持中文 / English。当前只保留单屏“工牌领取处”；员工图鉴、第二屏过渡区和品牌副题已移除。

- 直接使用 React Bits 官方 Lanyard，提供拖拽、回摆、点击翻面；背景使用官方 ShinyText。上游源码及完整许可保存在 `src/components/react-bits/`。
- 通过头像菜单或下方切换按钮选择九位角色，保留当前语言。箭头与下载入口集中到独立操作栏，矮屏手机使用较小卡片。
- 正反面透明背景 PNG 与 ZIP 是同源静态文件，位于 `public/downloads/{zh,en}/`。手机无需实时绘制图片或创建 Blob URL，JavaScript 未加载时主下载链接仍可下载 ZIP。
- PNG 分辨率 1200 × 1688，圆角外侧和挂孔透明，保留卡面印刷。下载弹窗支持分别保存或打包下载。
- Star 链接预留为 `https://github.com/fanhuayishiy/ai-crew-pass`；个人署名链接到用户主页。项目目前仅在本地 Git 保存，未推送。

```powershell
npm install --no-package-lock
npm run dev -- --host 127.0.0.1
npm run build
```

Node.js 22.12+。GitHub Pages 的子路径由 `GITHUB_REPOSITORY` 自动推导。

角色文案与配色：`src/data/characters.ts`；英文和 UI 翻译：`src/data/i18n.ts`；网络梗来源与改写说明：`src/data/memes.ts`、[来源说明](docs/internet-memes.md)。共用页面：`src/components/BadgeExperience.astro`。

修改卡面后，运行中的开发服务可供 `python -X utf8 scripts/export-badge-faces.py` 导出双语卡面，再执行 `python -X utf8 scripts/export-downloads.py` 生成静态下载。

口头禅现按用户提供的九角色对照图设置，卡背移除说明区，署名保留在页面弹窗；品牌与“工牌领取处”合为紧凑标题组合。

当前验收：`python -X utf8 scripts/verify-reference-edits.py`、`python -X utf8 scripts/verify-downloads.py`、`python -X utf8 scripts/verify-single-screen.py`。需要 Python Playwright、Chromium、Pillow。此前的图鉴、形变和旧自写物理测试保留作历史记录，不适用于当前单屏页面。

美术来源与署名：[素材说明](public/img/characters/NOTICE.md)、[English credits](public/img/characters/NOTICE.en.md)。前八位原帖立绘来自 ZipZipPipe；DeepSeek 原角色为上善无形；豆包使用本项目生成的透明动漫 v4，详情见 [生成记录](docs/doubao-anime-v4.md)。

**许可分别保留：原 Hanging Pass 为 MIT；React Bits 为 MIT + Commons Clause；美术按各自来源声明使用，不随代码自动变成 MIT。** 本项目仅作非商业同人展示，不是任何 AI 品牌的官方工作牌。

以下保留原项目历史说明，其中无 React、自写物理与实时滚动形变的描述不适用于当前首页。

---

<h1 align="center">Hanging Pass</h1>

<p align="center">A hand-built lanyard &amp; badge interaction for the web —<br />
Verlet rope physics · a scroll-driven coverflow morph · a real 3D twisted ribbon.</p>

<p align="center"><code>Astro</code> · <code>TypeScript</code> · <code>Three.js</code> · zero UI framework</p>

> **Demo media:** no screenshot is bundled on purpose. Screen 1's badge is
> positioned by JavaScript on the first frame, and the motion only reads as motion —
> so a still frame of it is misleading, and a trustworthy capture needs a real
> compositor. Record one yourself in ~30 seconds: open the demo, reload, and
> capture the first 8 seconds (badge entrance → swing), then scroll to screen 2.
> Drop the file in `docs/` and reference it here.

## What it is

Two screens, one continuous interaction:

1. **Screen 1 — the badge.** A hanging ID badge on a woven lanyard. It is not an
   animation loop: the strap is a Verlet/PBD rope simulated at a fixed 120 Hz timestep,
   the clip and O-ring are rigid bodies riding the rope's tail, and the card
   hangs from them by a punched hole. Drag it, let go, and it swings.
2. **Screen 2 — the cards.** Scrolling morphs the badge into a coverflow row of
   cards. Each card flips on a short click, and the strap keeps printing along
   its length while the cards drift.

Everything is plain TypeScript and CSS — no React, no GSAP, no animation library.

## What's inside

| System | File | What it does |
| --- | --- | --- |
| Rope | `src/scripts/lanyard-physics.ts` | Verlet chain + PBD constraints, gravity from a target period, grab/drag/release, entrance swing |
| Badge render | `src/scripts/lanyard-pass.ts` | Projects the rope into SVG: strap, clip plate, O-ring, punched hole; entrance animation; drag handling |
| Morph | `src/scripts/lanyard-morph.ts` | Scroll-driven coverflow, panel wiring, click-to-flip, auto-drift carousel, the runway that stages the transition |
| 3D ribbon | `src/scripts/strap-ribbon3d.ts` | The strap as a real 3D ribbon in Three.js: 72 quads, width·cos θ / width·sin θ, canvas-printed texture, self-occlusion by the z-buffer |
| Print glyphs | `src/scripts/strap-glyphs.ts` | A 5×7 bitmap font (A–Z, digits, `.`) for the woven print |

`src/scripts/strap-ribbon.ts` holds the 2D fallback geometry for the strap
(kept in the repo because the 2D path is still used for the outline and the
`prefers-reduced-motion` variant).

## Quick start

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in dist/
```

> **No lockfile on purpose.** `npm install` resolves platform-specific optional
> binaries (e.g. rolldown's native bindings) for whichever OS you are on. A
> lockfile generated on macOS makes CI (`npm ci`) fail on Linux with
> `Cannot find module './rolldown-binding.wasi.cjs'`. If you want a lockfile,
> generate it on the same OS your CI runs on.

Requires **Node 22.12 or newer** — Astro 7 refuses to run on older Node, and CI will
fail with a version error rather than a helpful build error. No other services,
no build-time data.

## Make it yours

| What | Where |
| --- | --- |
| Card titles, chapters, back copy | `src/data/cards.demo.ts` |
| Badge text (name, line, motto, back headline) | `src/pages/index.astro` (search for `Your Name`) |
| Strap print (front / back) | `src/scripts/lanyard-pass.ts` — `LABEL_TEXT` and the `{ front, back }` argument to `setViewport` |
| Card covers | put images in `public/img/` and set `front.image` per card; they render full-bleed with the title on top |
| Colours, type, spacing | `src/styles/tokens.css` |
| Font | Geist is self-hosted in `public/fonts/` — see [`public/fonts/README.md`](public/fonts/README.md), or swap it for a system stack |

## Project structure

```
src/scripts/      the three systems + the 3D ribbon and its bitmap glyphs
src/data/         demo card content (this is the file you edit first)
src/pages/        one page: screen 1 + screen 2
src/styles/       tokens.css (design tokens and all component styles)
docs/             how-it-works.md — read this before changing the physics
.github/workflows/deploy.yml   GitHub Pages deployment
```

## Notes on behaviour (by design)

- **Reduced motion is respected.** With `prefers-reduced-motion: reduce` the
  entrance swing, the auto-drift carousel and the morph tweens are disabled.
- **The carousel only auto-advances while the pointer is over the card row**
  (`AUTO.onHover` in `lanyard-morph.ts`). Set `AUTO.always = true` to let it run
  unattended. A click pauses it, and the pause expires after 9 s
  (`AUTO.resumePauseAfterMs`) so it never gets stuck.
- **Dragging never selects text.** The drag surfaces set `user-select: none`
  (the side panel keeps `user-select: text`, so its links stay copyable).
- **Three.js costs ~138 KB gzip.** It is the only runtime dependency. If you
  don't need the 3D ribbon, `strap-ribbon.ts` renders the same strap in SVG.

## Browser support

Chromium, Safari and Firefox, current versions. The physics uses `requestAnimationFrame`
with a fixed timestep, so motion speed does not change with frame rate. WebGL 2
is used for the ribbon; the SVG strap remains as the fallback path.

## 中文说明

这是一个**零框架**的「悬挂工牌 + 卡片轮播」交互模板：第一屏是物理吊绳上的工牌
（Verlet 绳 + 刚体夹片/圆环，固定 120Hz 步长），第二屏是滚动形变出来的 coverflow 卡片，
吊绳本身是一条**真正的 3D 缎带**（Three.js，带自遮挡与印花贴图）。

- 卡片内容改 `src/data/cards.demo.ts`；牌子上的文字改 `src/pages/index.astro`
- 吊绳印花文案改 `src/scripts/lanyard-pass.ts` 里的 `LABEL_TEXT` 与 `{ front, back }`
- 已处理 `prefers-reduced-motion`；拖拽时不会选中文字

## License

MIT — see [LICENSE](LICENSE). Bundled font: Geist (see `public/fonts/README.md`).
