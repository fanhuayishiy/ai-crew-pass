# 工牌编辑模式实测效果

以下图片来自 Chromium 实际页面操作：逐张打开当前 9 位员工的工牌，点选并替换正反面所有可见文字，再完成编辑并打开下载预览。这些截图未替换角色图片，保留了各角色原有美术和配色。

编辑模式也支持替换角色图片：点击内置的“糖包示例”或选择“上传图片”，在固定的 1∶1 裁剪框中拖动或缩放，然后选择“使用图片”和“完成编辑”。裁剪后的图片会用于工牌展示、下载预览和 PNG/ZIP；可以在原版、Q 版和自定义形象之间切换，也可以恢复原角色。本地图片不超过 20 MB，像素总数不超过 4000 万。

自定义图片和文字按员工、语言保存在当前浏览器，图片在本地处理，不会上传到服务器。分享链接不包含本地编辑内容；清除浏览器站点数据会移除本地保存的编辑内容。

![九张工牌编辑效果总览](overview.png)

| 员工 | 编辑后的正反面效果 | 实测项目 |
| --- | --- | --- |
| DeepSeek | [查看原图](deepseek.png) | 全部可见文字替换、3D 贴图更新、下载预览、正反面 PNG、ZIP |
| ChatGPT | [查看原图](gpt.png) | 同上 |
| GLM | [查看原图](glm.png) | 同上 |
| Qwen | [查看原图](qwen.png) | 同上 |
| Gemini | [查看原图](gemini.png) | 同上 |
| Claude | [查看原图](claude.png) | 同上 |
| Kimi | [查看原图](kimi.png) | 同上 |
| Grok | [查看原图](grok.png) | 同上 |
| 豆包 | [查看原图](doubao.png) | 同上 |

下载验证包括 ZIP 完整性、独立 PNG 与 ZIP 内图片逐字节一致、1200 × 1688 尺寸、透明圆角及挂孔。另验证刷新恢复、员工和语言隔离、恢复原版、WebGL 不可用时的静态展示，以及 320 / 390 像素宽度下的触屏编辑和下载。

开发服务运行时可复现完整验证：

```bash
python -X utf8 scripts/verify-edit-mode.py
```

角色图片上传、裁剪和保存的回归测试：

```bash
python -X utf8 scripts/verify-custom-portrait.py
python -X utf8 scripts/verify-example-portrait.py
```

默认截图写入 `docs/preview/edited-badges/`；更新本目录的 PR 效果图时运行：

```bash
BADGE_CAPTURE_EFFECTS=1 python -X utf8 scripts/verify-edit-mode.py
```

验证生产预览时，可用 `BADGE_TEST_URL` 指定服务地址。
