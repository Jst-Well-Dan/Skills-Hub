<!-- source-sha256: c6e899b8ba90c5c86172817b6f658bef920956eb4d7a779e4c1cdae55d87e4ba -->
---
name: frame-logo-outro
zh_name: "品牌 Logo 收尾帧"
en_name: "Logo Outro Frame"
emoji: "🎬"
description: "Logo 分块组装入场 + 光晕绽放 + 标语揭示，适合视频片尾 / 品牌闭幕"
category: video
scenario: video
aspect_hint: "1920×1080 (16:9)"
featured: 40
recommended: 8
tags: ["logo", "outro", "branding", "end-card", "frame"]
example_id: sample-frame-logo-outro
example_name: "品牌 Logo 收尾 · HTML Anything"
example_format: markdown
example_tagline: "午夜靛蓝 + 光晕绽放"
example_desc: "Logo 装配 + 品牌名 + 标语 + 行动号召，用于视频片尾"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · logo-outro"
---

【模板：Logo 收尾帧（Logo Outro）】
【意图】视频结尾的品牌揭示帧 —— Logo 分块拼装 + 光晕绽放 + 标语上浮 + 行动号召。灵感来自 hyperframes logo-outro。

【画布】1920×1080，黑色 `#08090c` 或品牌深色背景；添加微妙的暗角 `radial-gradient(...)`，让中心更亮。

【布局】
- **中心 Logo**：用 CSS / 内联 SVG 绘制；由 4-8 个几何块（圆 / 方 / 三角 / 细线）组成。
  - 入场动画：每个块从屏幕外滑入（不同方向 ±100px）+ scale 1.4→1.0 + opacity 0→1，错峰 80ms；总时长 1.2s。
  - 入场完成后，整个 Logo 添加光晕绽放：`filter: drop-shadow(0 0 24px <accent>40)`；同时用 `mask-image` 制作一道微光横扫 Logo（500ms）。
- **品牌名**：位于 Logo 下方 6-8% 处，大字（Inter Tight / SF Pro Display，48-72px，weight 700，letter-spacing -0.02em），入场：打字机效果或上浮淡入，在 Logo 光晕绽放后出现（1.4s 开始）。
- **标语**：品牌名下方一行（24-28px，weight 400，opacity 0.7），淡入（1.8s）。
- **底部行动号召 + 元数据**：底部双行布局，例如 `htmlanything.dev · @htmlanything · 2026`，11px 大写字母，letter-spacing 0.16em，颜色 opacity 0.4，细线分隔。

【调色 — 4 选 1，不混用】
- 🌌 **午夜靛蓝** — bg `#08090c`，accent `#7c5cff`（霓虹紫蓝光晕）。
- 🌅 **日光琥珀** — bg `#0e0a08`，accent `#ffb547`（暖琥珀色）。
- 🌿 **森林薄荷** — bg `#0a1410`，accent `#5fb38a`（薄荷绿）。
- ⚪ **骨白与墨黑** — bg `#f1efea`，accent `#0a0a0b`（无霓虹，采用编辑设计风格，将光晕改为阴影）。

【设计细节】
- **绝不**：使用外链 Logo 图片；Logo 必须用纯 CSS / 内联 SVG 几何图形绘制。
- 入场动画使用 `@keyframes` + `animation-delay`；可由 `prefers-reduced-motion` 关闭。
- 字体：西文 `Inter Tight` / `SF Pro Display` / `Manrope`；中文 `Noto Sans SC` weight 700。
- 必须使用用户提供的品牌名 + 标语；若没有，则采用备用内容 "HTML Anything" / "Anything → beautiful HTML"。
- 单文件 HTML；整个动画完成后定格（不要循环，这是视频结尾帧）。
- 顶部可选添加 5px 饰带（accent 色），增强品牌识别度。
