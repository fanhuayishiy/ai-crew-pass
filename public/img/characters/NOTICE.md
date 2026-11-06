# AI Crew Pass · 角色美术来源

本项目是非官方、非商业同人工牌展示，不代表各 AI 产品官方。

## 八位 AI 娘

使用 [ZipZipPipe 原始角色动态](https://www.bilibili.com/opus/1233069202138464289) 中的原尺寸图片，未使用网页的 264px 九宫格缩略图，未修改下载图片字节。文件仅重命名，页面通过 CSS 裁切、缩放展示。

- DeepSeek 鲸鱼娘：上善无形（原角色）→ ZipZipPipe（女仆二次设计），CC BY-NC-SA 4.0。
- DeepSeek 主工牌另使用此前存档的透明底 `../deepseek/maid.webp`，其 Small-tailqwq / JAdpp 整理与改编署名、来源及哈希记录见 [原素材说明](../deepseek/NOTICE.md)。图鉴仍使用原帖 PNG。
- GPT、Kimi、GLM、千问、Gemini、Claude、Grok：ZipZipPipe。依作者分享声明作署名、非商业同人展示，不声称第三方角色权利归本项目所有，也不一概将其重新许可为 MIT。
- 人设文案、工号与部门是本项目为工牌创作的展示内容，不是官方设定或产品能力保证。
- 原帖第二张角色图是 Kimi，第七张是 GPT 白龙娘；按 K 字徽、乐器，以及 GPT 龙角、绳结标识核对身份。

逐文件来源 URL、原始尺寸、SHA-256 见 [sources.json](./sources.json)。

## 豆包

当前 v4 使用与其他角色统一的精细动漫立绘，保留棕色短发、红围巾、黑西装短裙、腰链、长靴与手提包。非官方角色设计，不是 ZipZipPipe 发布的豆包原稿。

- 当前展示文件：`doubao-anime-v4.png`，941 × 1672，RGBA 透明底，内置 image_gen 生成。
- 外观参考沿用用户截图对应的 v3，画风参考 DeepSeek 原图；保留上善无形 / ZipZipPipe 的参考署名链。
- 完整提示词：仓库 `docs/doubao-anime-v4.md`；来源记录：`doubao-anime-v4.source.json`。
- v2、v3 文件仅作历史版本保留，当前页面已切换为 v4。
- 品牌及参考形象权利归原权利人，仅用于非商业同人展示，不将其纳入代码 MIT 许可。

## 代码与美术分开许可

图鉴代码基于 MIT 许可的 [xu-yaoting/hanging-pass](https://github.com/xu-yaoting/hanging-pass)，保留其 LICENSE。工牌直接使用 [React Bits Lanyard](https://github.com/DavidHDev/react-bits)，采用 MIT + Commons Clause，完整许可保存在 `src/components/react-bits/LICENSE.md`。美术不因随代码分发而自动变为 MIT；商业使用需另行取得对应权利人的授权。
