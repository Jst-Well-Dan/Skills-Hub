<!-- source-sha256: 31133676d2a66875b5369e91ce67bc6efc3410c4df9c7cdba673c3ef9414c9a6 -->
---
name: frame-glitch-title
zh_name: "故障艺术标题帧"
en_name: "Glitch Title Frame"
emoji: "⚡"
description: "数字故障 / 像散偏移 / 数据腐败标题，适合视频转场 / 赛博朋克主视觉"
category: video
scenario: video
aspect_hint: "1920×1080 (16:9)"
featured: 37
recommended: 6
tags: ["glitch", "cyberpunk", "title", "transition", "vfx", "frame"]
example_id: sample-frame-glitch-title
example_name: "故障标题 · SIGNAL_LOST"
example_format: markdown
example_tagline: "青色 / 品红色像散 + CRT 扫描线"
example_desc: "巨大标题 + 数据腐败伪影 + 角落 ASCII 噪点块"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · 故障艺术"
---

【模板：故障艺术标题帧 (Glitch Title)】  
【意图】单帧主视觉 / 视频转场 / 赛博朋克风格标题。灵感来自 hyperframes 故障艺术。

【画布】1920×1080，背景 `#070708` 近黑或 CRT 暗灰 `#0d0e10`；添加 56px 网格（透明度 5%）+ 扫描横线（透明度 8%，间隔 2px）。

【主标题】

- 居中，6-9vw，字重 800/900，字体 `Space Grotesk Bold` / `Inter Tight Black` / `JetBrains Mono Bold`。
- 颜色：主层 `#f5f5f7`；后面叠加 2 层伪影：
  - 青色 `#00f0ff` translate(`-3px`, `1px`)。
  - 品红色 `#ff2bd6` translate(`3px`, `-1px`)。
- 整层添加 clip-path 切片 5-8 段，每段使用 `@keyframes` 随机 translateX -10px → 10px，持续 80-160ms，错峰播放，营造“数据腐败”像散效果。
- 每隔 1.5s 触发一次“重故障”——整个标题被水平拖影 1 帧，使用 `filter: url(#displacementFilter)` 或简单 CSS 平移。

【附加层】

- 顶部一行说明文字（大写等宽字体，11px，透明度 0.6）：`>> SIGNAL_LOST · CH-04 · 14:32:08`。
- 标题下方一行副标题（24-28px，等宽字体，透明度 0.7），偶尔被 ` ̶▒̶` 字符替换（模拟乱码）。
- 角落随机点缀 `█▓▒░` ASCII 噪点块。
- 底部时间码（等宽字体，透明度 0.4）。
- 整个画面叠加噪点颗粒层 `background-image: url("data:image/svg+xml,...turbulence...")`，透明度 6%，mix-blend-mode overlay。

【SVG 滤镜（可选）】

- 定义 `<filter id="rgbShift">`，使用 `feColorMatrix` + `feOffset` + `feMerge` 偏移 R/G/B 三个通道；在故障瞬间为整层应用 `filter: url(#rgbShift)`。

【设计细节】

- 仅使用以下颜色：黑 / 白 / 青色 / 品红色 / 少量琥珀色警告色；严禁使用全彩虹配色。
- 字体：西文使用 `Space Grotesk` 或 `JetBrains Mono` Bold；中文使用 `Noto Sans Mono CJK SC` 或 `Noto Sans SC` Bold。
- 严禁使用 lorem ipsum；必须使用用户的标题 + 副标题。
- 动效使用 `@keyframes`，并可通过 `prefers-reduced-motion` 关闭（回退为静态色差分离效果）。
- 单文件 HTML。
