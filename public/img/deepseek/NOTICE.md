# DeepSeek 鲸鱼娘角色素材

本目录使用已有社区形象，非 DeepSeek 官方形象或官方工作牌。

- 原角色：上善无形（溟月）。
- 女仆二次设计：ZipZipPipe。
- `whale-girl.jpg`：ZipZipPipe 初始正常比例立绘，Pixiv 148186519 p00。
- `whale-chibi.png`：作者视频 BV1tE9XBbErS 的 5 秒展示截帧，不冒充原始立绘。
- `maid.webp`、`whale-serious.webp`、`whale-starry.webp`、`whale-cheerful.webp`：Small-tailqwq / dsh-deep-whale 上游素材，JAdpp / dsh-whale-galgame 整理或表情改编。
- 下载供应方：HABAI182 / ai-girls-atlas。下载原文件，未修改图片字节；展示时由 CSS 缩放、裁切。

素材许可：CC BY-NC-SA 4.0。署名、仅限非商业使用；改编后的美术须以相同协议共享。第三方品牌及角色权利不由代码 MIT 许可转授。

来源、许可声明证据、供应仓库提交及 SHA-256 逐文件记录于 [sources.json](./sources.json)。

- [角色来源汇总](https://github.com/HABAI182/ai-girls-atlas/blob/main/characters/deepseek/README.md)
- [作者角色动态](https://www.bilibili.com/opus/1233069202138464289)
- [作者 Q 版展示视频](https://www.bilibili.com/video/BV1tE9XBbErS/)
- [JAdpp 美术许可](https://github.com/JAdpp/dsh-whale-galgame/blob/046b848f244450e6e636335766276bf3343fe84b/LICENSE.md)
- [CC BY-NC-SA 4.0 中文摘要](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)


## DeepSeek 正面生成卡面 v2（本地试稿）

`crew-pass-ocean-v2.png` / `.webp` 为基于用户提供的工牌参考图和项目 `maid.webp` 生成的衍生卡面，使用内置 image_gen。原角色与女仆设计署名及同人素材使用范围沿用本说明，不因生成改编而变为 MIT。生成提示词、输入与输出记录见 `docs/deepseek-generated-front-v2.md`（仓库根目录）。


## DeepSeek 分层生成素材 v3（本地试稿）

`front-background-v3`、`portrait-cutout-v3`、`back-background-v3` 各自保存为独立 PNG / WebP，分别由内置 image_gen 生成；人物 PNG 保留真实透明通道。背景、人物与文字在页面导出模板里独立组合。原角色与女仆设计署名及同人使用范围继续沿用，不因生成改编而变为 MIT。三组完整提示词、素材尺寸及组合方式见仓库 `docs/deepseek-separated-art-v3.md`。


## DeepSeek 参考图卡面 v4（本地试稿）

`front-background-v4.png/.webp` 与 `back-background-v4.png/.webp` 分别依据用户的正面、背面参考图，由内置 image_gen 生成。透明人物继续使用独立的 v3 立绘；文字单独排版。原角色与素材使用限制沿用本说明，生成记录与完整提示词见仓库 `docs/deepseek-reference-cards-v4.md`。
