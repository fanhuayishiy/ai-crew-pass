# 非人类员工 · Nonhuman Employees

[简体中文](README.md) · [English](README.en.md)

给九位 AI 同事，发一张可以晃的工牌。

[在线领取工牌](https://badge.fhysy.com/) · [English demo](https://badge.fhysy.com/en/) · [许可证与素材说明](#许可与致谢)

![项目预览](public/social/cover.png)

一个支持中文 / English 的 AI 同人工牌小项目：拖动挂绳、松手回摆、点击翻面，再把喜欢的工牌下载下来。由 **风花AI实验室** 分享。

## 关注风花AI实验室

如果你也喜欢 AI 创作、实用工具和有趣的小实验，欢迎关注微信公众号 **「风花AI实验室」**。后续项目更新与制作分享会在这里交流。

<img src="public/img/community/fenghua-ai-lab-wechat.jpg" width="220" alt="风花AI实验室微信公众号二维码" />

微信扫码关注，或保存二维码后在微信中识别。

## 可以做什么

- 九位 AI 同事：DeepSeek、ChatGPT、GLM、Qwen、Gemini、Claude、Kimi、Grok、豆包。
- React Bits 官方 Lanyard 的 3D 挂绳、拖拽回摆与翻面；同色系 ShinyText 背景扫光。
- 正面贴图在 HTML 阶段高优先级预加载，正反面与挂绳独立显示；展示纹理采用同分辨率 WebP（背面无损），PNG 下载保留原画质。当前正面显示后空闲预取相邻角色，悬停或触摸菜单时预取目标角色；省流量模式及 2G 网络跳过预取。
- 中英文切换、头像员工菜单、左右角色切换，适配手机触屏与矮屏。
- 编辑模式：点击正反面文字即可替换，完成后 3D 展示、静态预览及 PNG / ZIP 下载使用同一份编辑结果。文字按员工和语言保存在当前浏览器，可恢复原版；分享链接仍指向原版工牌。
- 下载透明背景正反面 PNG，或一次下载 ZIP；原版使用静态文件，编辑后的工牌由浏览器生成。
- WebGL 不可用时提供可翻面的静态预览；关闭脚本后仍可下载工牌。
- 翻面、松手金属声与角色切换使用实录拟音素材（Freesound，CC0），默认开启；右上角可静音并记住偏好，首次交互后启用声音。音频随项目本地托管，无背景音乐，详见[音效说明](public/audio/badge/NOTICE.md)。

卡面台词为用户指定的同人玩梗内容，不是产品能力说明。所有角色均为非官方同人形象。

## 本地运行

Node.js **22.12+**。

```bash
npm install --no-package-lock
npm run dev -- --host 127.0.0.1
npm run build
```

## 修改与部署

- 角色、配色与素材：`src/data/characters.ts`。
- 中英文文案：`src/data/i18n.ts`；口头禅：`src/data/memes.ts`。
- 共用页面：`src/components/BadgeExperience.astro`。
- 修改卡面后，开发服务运行时执行 `python -X utf8 scripts/export-badge-faces.py`，再执行 `python -X utf8 scripts/export-downloads.py` 更新下载。
- `main` 分支推送自动运行 GitHub Actions，也可手动选择分支发布。工作流按当前仓库配置的 Pages 地址构建域名与子路径，并保留编辑所需素材；fork 可使用自己的域名。手动构建未指定 `GITHUB_PAGES_URL` 时，继续使用 `public/CNAME` 或 `GITHUB_REPOSITORY` 作为默认配置。

## 访问量统计

页脚使用[不蒜子](https://busuanzi.ibruce.info/)显示全站总浏览量（PV），仅在 `badge.fhysy.com` 下加载，不统计本地开发或预览地址。刷新、切换角色和语言都会增加页面浏览量，不等同于独立访客数，也不会补算接入前的历史访问。第三方服务被拦截或加载失败时，统计项隐藏，页面和下载正常使用。

## 验证

需要 Python Playwright、Chromium、Pillow。

```bash
python -X utf8 scripts/verify-single-screen.py
python -X utf8 scripts/verify-downloads.py
python -X utf8 scripts/verify-reference-edits.py
python -X utf8 scripts/verify-optimizations.py
python -X utf8 scripts/verify-texture-loading.py
python -X utf8 scripts/verify-edit-mode.py
```

此前图鉴与旧自写物理测试保留作历史记录，不适用于当前单屏版本。

## 许可与致谢

本仓库公开源码，**各部分分别遵循其许可，不将全部素材统一标为 MIT**：

| 部分 | 来源与许可 |
| --- | --- |
| 本项目新增代码、原 Hanging Pass 代码 | [MIT](LICENSE)，保留 [xu-yaoting/hanging-pass](https://github.com/xu-yaoting/hanging-pass) 原作者署名 |
| Lanyard、ShinyText | [React Bits](https://github.com/DavidHDev/react-bits)，[MIT + Commons Clause](src/components/react-bits/LICENSE.md)，不属于无条件商业再分发许可 |
| Geist 字体 | [SIL OFL 1.1](public/fonts/LICENSE-Geist.txt) |
| 角色美术、衍生卡面与下载图片 | 各自素材声明；不随代码自动变为 MIT，仅作非商业同人展示 |

DeepSeek 原角色：**上善无形**；八位 AI 娘设计：**ZipZipPipe**。豆包是本项目生成的透明动漫同人形象。详细出处、原尺寸、哈希与改编记录见 [中文素材说明](public/img/characters/NOTICE.md)、[English credits](public/img/characters/NOTICE.en.md)、[豆包记录](docs/doubao-anime-v4.md) 和 [第三方许可汇总](THIRD_PARTY_NOTICES.md)。

角色、商标和品牌权利归各自权利人。本项目与相关 AI 公司无隶属或官方合作关系。复用或商业使用前，请分别核对对应许可。
