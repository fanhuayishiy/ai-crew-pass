# 非人类员工 · Nonhuman Employees

最新交互：移除“人事档案室”标题和官网导航；突出 Star on GitHub；主工牌左右按钮循环切换九位角色，并保留语言。下载工牌可预览及分别保存 1200 × 1688 的正反面透明背景 PNG，也可一次下载 ZIP；圆角外侧和挂孔透明，卡面印刷保留。下载全程在浏览器本地生成。

员工菜单改用专用 WebP 头像（九张共约 26 KB）并去掉大面积 backdrop blur。Star 项目地址预留为 `https://github.com/fanhuayishiy/ai-crew-pass`；当前仅本地 Git 管理，没有向该远程仓库推送。个人署名仍链接到用户主页。

下载验收：`python -X utf8 scripts/verify-downloads.py`，检查实际浏览器下载、ZIP CRC、两张 PNG 的尺寸与透明像素、单张下载一致性，以及中英文左右切换和手机按钮。

当前版本：图鉴采用更大的居中卡片；页面最底部直接落在人事档案室，署名通过底部弹窗查看。背景字使用 React Bits ShinyText 的低对比扫光；员工选择收为带头像的菜单。口头禅改用有出处的网络梗与明确标注的吐槽改写，详见 [梗来源与视觉说明](docs/internet-memes.md)。

新增验收：`python -X utf8 scripts/verify-polish.py`，检查实际文字动效、减少动态效果、员工菜单与页底落位。

基于 [xu-yaoting/hanging-pass](https://github.com/xu-yaoting/hanging-pass) 改造的九角色同人工牌项目。保留物理吊绳、拖拽摇摆、点击翻面、滚动卡片轮播，增加独立角色页面、九宫格角色切换和随角色变化的整页配色。

角色包括 DeepSeek 鲸鱼娘、GPT 白龙娘、GLM 阔耳狐娘、千问、Gemini、Claude、Kimi、Grok 和豆包。前八位使用 [ZipZipPipe 原帖](https://www.bilibili.com/opus/1233069202138464289) 中的原尺寸立绘；豆包 v4 保留用户参考图的棕色短发、红围巾、黑西装短裙与长靴，改为与其余角色统一的透明底动漫立绘，牌面裁切与人物、姓名栏位置采用共用布局。图片和完整提示词见 [豆包动漫 v4](docs/doubao-anime-v4.md)。

卡面保留清爽的浅色、大幅立绘、圆形细线。九位角色的正反面由共用卡面导出为高清贴图。

右上角支持中文 / EN 切换。中文入口 `/`，英文入口 `/en/`，角色页和图鉴跳转保留所选语言；页面文案、角色资料、SEO 标题和工牌正反面均有英文版本。翻译集中在 `src/data/i18n.ts`，36 张双语贴图位于 `public/img/badges/zh/` 和 `public/img/badges/en/`。贴图按卡身比例导出，印刷铺满卡面；挂绳重复品牌字样，图鉴标题以小号背景字放在右上角。

首页直接接入 [React Bits 官方 Lanyard](https://github.com/DavidHDev/react-bits/blob/main/src/content/Components/Lanyard/Lanyard.jsx)，源码保存在 src/components/react-bits/，不修改其物理实现。React 包装组件只传入角色贴图、挂绳配色、尺寸等公开参数，旧 initLanyardPass 已停用。图鉴移除右侧资料栏，采用居中的全宽卡片轮播，支持鼠标拖动、滚轮、方向键和左右按钮；介绍与同人设定口头禅收进卡片背面。站名为“非人类员工”，首页标识为“工牌领取处”，图鉴分区为“人事档案室”。图鉴沿用 Hanging Pass 的轮播基础；首页组件随页面滚出，不再将实时吊牌姿态接入旧图鉴形变。

卡面更新后启动开发服务，执行 python -X utf8 scripts/export-badge-faces.py 重新导出贴图。交互验收执行 python -X utf8 scripts/verify-react-bits.py，旧重力测试只针对已停用实现，不作为当前效果的验收依据。

项目主页 GitHub 链接指向 [fanhuayishiy](https://github.com/fanhuayishiy)。本地工作分支为 `codex/ai-crew-pass`，原作者仓库保留为 `upstream`，尚未创建或推送新的 GitHub 远程仓库。

```powershell
npm install --no-package-lock
npm run dev -- --host 127.0.0.1
npm run build
```

Node.js 22.12+。启动脚本兼容 Windows。

- 角色、颜色、署名与官网链接：`src/data/characters.ts`。
- 工牌共用视图：`src/components/BadgeExperience.astro`。
- 首页 `/` 为 DeepSeek；其余角色在 `/characters/gpt/`、`/characters/doubao/` 等路径。
- 视觉样式：`src/styles/deepseek.css`；主题变量由角色数据生成。
- 图鉴卡片：`src/data/cards.demo.ts`；每张卡片背面可打开对应角色的工作牌。
- 浏览器验收：启动服务后运行 `python -X utf8 scripts/verify-react-bits.py`（需安装 Python Playwright、Pillow 及 Chromium）。旧 `verify-ui.py` 和 `verify-gravity.py` 仅针对已停用的自写物理实现。
- 双语验收：`python -X utf8 scripts/verify-locales.py`，覆盖 18 条路由、语言保留、36 张贴图比例和文字边界、图鉴跳转及窄屏。
- GitHub Pages 部署路径从 `GITHUB_REPOSITORY` 自动推导，不再固定为原作者的 `hanging-pass`。

**原 Hanging Pass 代码沿用 MIT；React Bits 组件采用 MIT + Commons Clause，完整许可见 src/components/react-bits/LICENSE.md；美术按各自来源声明使用。** 本项目仅作非商用同人展示。署名、使用说明与来源记录见 [角色素材说明](public/img/characters/NOTICE.md) 和 [逐文件来源记录](public/img/characters/sources.json)。页面也保留署名。本项目不是各 AI 品牌的官方工作牌。

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
