<!-- source-sha256: f1b11d1b97b66d480cb40b04c8a10043db8f54ffd4b5f8d76e2b2773ad023a04 -->
---
name: frame-liquid-bg-hero
zh_name: "流体背景主视觉帧"
en_name: "流体背景主视觉"
emoji: "🌊"
description: "WebGL 风格流体置换背景 + 顶部叠加金句，适合视频片头 / 落地页主视觉 / 海报"
category: poster
scenario: video
aspect_hint: "1920×1080 (16:9) 或 1080×1920 (9:16)"
featured: 39
tags: ["liquid", "fluid", "background", "hero", "html-in-canvas", "vfx"]
example_id: sample-frame-liquid-bg-hero
example_name: "流体背景主视觉 · 金句"
example_format: markdown
example_tagline: "极光紫流体"
example_desc: "多层 radial-gradient 呼吸背景 + difference 文字"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · vfx-liquid-background"
---

【模板：流体背景主视觉】
【意图】可作为视频片头帧、SaaS 落地页顶部主视觉、海报底图。呈现 WebGL 流体质感，但使用 CSS / canvas 降级绘制，确保单文件可双击打开。灵感来自 hyperframes vfx-liquid-background。

【画布】1920×1080（横）或 1080×1920（竖），二选一。背景铺满画布。

【流体背景 — 3 种实现方式，按用户偏好选择】
1. **CSS 多层 radial-gradient 错位呼吸**（最稳定，默认推荐）：
   - 使用 3-5 个大型椭圆 `radial-gradient(...)`，颜色取自调色板。
   - 每个椭圆应用 `@keyframes` 平移 + scale + hue-rotate，周期为 8-14s，错峰播放；整个画面叠加 `mix-blend-mode: screen` 或 `overlay`。
   - 顶层增加一层 `backdrop-filter: blur(80px)`，让边缘更加模糊。
2. **Canvas + 简单柏林噪声**（中阶）：
   - 使用 80 行内联 JS，通过 `requestAnimationFrame` 绘制元球或单纯形噪声场。
   - 性能允许时启用；开启 `prefers-reduced-motion` 时降级为静态截图。
3. **WebGL 片元着色器**（高阶，慎用）：
   - 通过 jsdelivr CDN 引入 `regl`，或使用内联原生 WebGL。
   - 着色器编写域扭曲噪声；使用单个四边形和一个 uniform `u_time`。

【顶层文字层】
- 居中或左下：一句巨型金句（5-7vw，衬线体或粗体无衬线体），字体：`Source Serif Pro` / `Inter Tight` / `Manrope Black`。
- 文字颜色使用纸白色 `#fafaf8` 或墨色，具体取决于背景明暗；添加 `mix-blend-mode: difference`，确保文字在任何流体颜色上都清晰可读。
- 副标题使用一行小号无衬线体，opacity 0.7。
- 底部可选行动号召标签，或细线 + 元数据行。

【调色 — 4 选 1，不要使用彩虹色】
- 🌅 **暖阳蜜桃** — `#ffb18a` + `#f78b4c` + `#d97757`，暖橙桃色。
- 🌊 **海洋水蓝** — `#5ac8fa` + `#0a84ff` + `#1e3a8a`，海蓝色。
- 🌌 **极光紫** — `#a78bfa` + `#7c5cff` + `#1e1b4b`，极光紫色。
- 🌿 **森林薄荷** — `#86efac` + `#34d399` + `#065f46`，苔藓森林色。

【设计细节】
- 严禁：多色彩虹（>4 个色相）、PowerPoint 式渐变、霓虹荧光叠加。
- 字体：中文使用 `Noto Serif SC`（展示字体）/ `Noto Sans SC`（副标题）。
- 严禁使用外链图片；全部使用 CSS + SVG + 可选 canvas。
- 必须使用用户提供的金句 / 标题；如果用户输入的是数据，则提炼一句 ≤ 18 字的金句。
- 使用单文件 HTML，可通过 `prefers-reduced-motion` 关闭动效。
