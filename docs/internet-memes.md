# 网络梗来源与卡面改写

核对日期：2026-11-06。没有把搜索结果数量当作热度排名，也不宣称九条都是各模型“全网第一”口头禅。能核对的原句保留；用户召唤语、历史错误、网友调侃和本项目改写分开标注。英文为语境翻译，Grok 保留原英文。

| 员工 | 卡面短句 | 类型和来源 |
| --- | --- | --- |
| DeepSeek | 服务器繁忙，请稍后再试。 | 服务提示形成的网络梗。[报道](https://news.sina.com.cn/s/2026-03-30/doc-inhstpih6558659.shtml)；不代表当前服务状态。 |
| ChatGPT | 我会稳稳地接住你。 | 中文口癖与梗图，有直接报道。[爱范儿](https://www.ifanr.com/1665148) |
| GLM | 9.11 比 9.9 大。 | 历史翻车梗。[2024 年报道](https://www.thepaper.cn/newsDetail_forward_29189033)同时说明后来复测已修正；不代表当前模型能力。 |
| Qwen | 先别问模型了，奶茶什么时候到？ | 根据奶茶活动、拥堵与催单现象改写，**不是产品原话**。[报道](https://www.thepaper.cn/newsDetail_forward_32549047) |
| Gemini | 我只是一个语言模型，没法帮上忙。 | 用户直接贴出的拒答文字，取短句节选。[社区帖子](https://linux.do/t/topic/1709469) |
| Claude | 才刚开工，额度就下班了。 | 根据使用限额体验写的同人调侃，**不是官方错误提示**，也不宣称是排名第一的网络原梗。[官方限制说明](https://support.claude.com/zh-CN/articles/11647753-使用限制和长度限制如何工作) |
| Kimi | 我们换个话题吧。 | 对报道中“动不动让换个话题”的用户反馈作口语概括，不宣称是逐字原话。[36氪](https://www.36kr.com/p/3042093782597767) |
| Grok | @grok is this true? | 用户召唤 Grok 核查/解释的网络用法，**不是 Grok 的回答**。[Know Your Meme](https://knowyourmeme.com/memes/grok-explain-this) |
| Doubao | 我这就给你掰开揉碎一次性讲透。 | 用户直接吐槽并整理的高频口癖。[微博原文新浪页面](https://www.sina.cn/news/detail/5313345985971926.html) |

结构化来源、说明与中英文本位于 `src/data/memes.ts`；图鉴每张卡片背面提供对应来源链接。口头禅只作同人幽默，不是产品能力测评或实时服务状态展示。

## 本轮视觉与滚动

- 接入 React Bits 官方 ShinyText，轻微的同色系扫光，支持减少动态效果与视口可见性处理；来源与许可保存在 `src/components/react-bits/`。
- 员工选择使用原生 details/summary 头像菜单与 CSS 柔和悬停，支持键盘、Escape 和点外部收起。此控件是本项目实现，没有将其称为直接接入 GooeyNav。
- 档案卡片尺寸增大；缩短两屏间的过渡距离；署名改为原生 dialog，不再占据档案后方的滚动高度。页面最底部即档案室落点。
- 验收：`scripts/verify-locales.py` 和 `scripts/verify-polish.py`，覆盖真实页底落点、卡片尺寸、切换与翻面、双语、实际扫光变化、减少动态效果以及员工菜单。
