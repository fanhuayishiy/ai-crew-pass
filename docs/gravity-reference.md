# React Bits Lanyard 直接接入

当前首页直接使用官方 React Bits Lanyard 源码，替代此前自写的重力实现。中文镜像无法连接，取用官方仓库同名组件。上游源码与 CSS 保持原样，来源、许可见 `src/components/react-bits/`。

Astro 通过 React island 加载 `ReactBitsBadge.jsx`。包装层仅传角色正反面贴图、挂绳配色和 size=0.51 等公开参数；重力、阻尼、弹性、风力、抓取、释放与翻面均沿用组件默认行为。旧 initLanyardPass 已停止调用。

九位角色统一使用高清卡面贴图，保留浅色设计与现有动漫人物。图鉴仍使用 Hanging Pass 轮播，滚动时不再沿用实时工牌姿态进行形变。

验收：启动开发服务后运行 `python -X utf8 scripts/verify-react-bits.py`。通过真实鼠标抓取、抬起、释放及后续画面差异确认运动，通过短按检查翻面，同时检查九页贴图、图鉴导航和窄屏。旧 verify-gravity.py 与 lanyard-physics.test.ts 针对停用的实现。
