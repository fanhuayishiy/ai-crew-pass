# 豆包 3D CG v3 · 历史版本

- 图片：`public/img/characters/doubao-3d-v3.png`，941 × 1672，RGBA，保留透明 Alpha（0–255）。
- 工具：内置 `image_gen`，未使用 CLI/API 回退。
- 唯一外观参考：用户本轮提供的视频截图。棕色短发、红色长围巾、黑色西装短裙、银色腰链、黑色长靴与手提包。
- 本项目生成的非官方同人形象，不是官方发布的 3D 模型。该文件是有 3D CG 体积感的透明底栅格立绘；可交互工牌卡身另用真实 Three.js 几何体渲染。
- 不再使用 v2 的女仆裙、围裙或蕾丝头饰。v2 文件和记录留作历史版本，页面已替换为 v3。

## 最终提示词

Create a premium high-resolution full-body 3D CG character cutout based closely on the provided reference screenshot, for a Doubao AI fan employee badge. Use the screenshot only for character identity, facial features, hairstyle, proportions and exact outfit; discard the screenshot UI and room. One clearly adult young woman, polished stylized-realistic 3D game/cinematic character, natural adult proportions, friendly composed face, large but realistically proportioned brown eyes, smooth chestnut brown asymmetrical chin-length bob. EXACT OUTFIT: fitted tailored black blazer with structured shoulders and satin black lapels, black turtleneck, short black pleated skirt, fine silver chain draped from a small waist clasp, sheer black tights, tall fitted black leather knee-high boots. A vivid red knitted scarf wrapped around her neck, one long broad end hanging down the front to around the knees, accurate knit folds and tassel ends. Carry a small black leather handbag naturally in one hand, other hand relaxed. Front-facing neutral standing pose with a slight natural weight shift, both legs and BOTH BOOTS completely visible, no cropped head or feet, modest professional fashion styling. Beautiful credible 3D volume: soft key light from upper left and narrow rim light, physically based skin with subtle subsurface scattering, fine hair strands, sharply tailored cloth folds, leather highlights and metal clasp reflections. Crisp silhouette, clearly resolved hands and fabric contours, no motion blur, no soft focus. Preserve black and red palette and reference resemblance. Genuine transparent alpha background, isolated figure only; no room, no white backdrop, no ground plane, no cast ground shadow, no caption or watermark. Tall portrait about 9:16. This is NOT an anime drawing, NOT a maid, no maid headband, no apron, no fantasy ornaments.

## 工牌几何与渲染

- `src/scripts/badge-body3d.ts`：圆角挤出几何，8px 主体加 2px 双面倒角，总厚度约 12px；实际穿孔，正反面印刷层与独立侧面材质。
- 与原物理工牌共用位置、孔位枢轴、旋转与翻面角度；匹配 DOM 卡面的 1400px 透视。
- 实体卡身有半球光、主光、轮廓光和物理材质，直接使用原物理帧循环，没有新增持续的动画循环。
- 默认轻微转向以露出侧边，鼠标悬停可改变转角；尊重减少动态效果设置。
- 工牌取消白底和白色照片框，使用角色配色。豆包用真实透明底，其他原始白底美术以页面混合模式融入同色背景，不修改原始图片字节。
