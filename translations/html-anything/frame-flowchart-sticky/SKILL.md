<!-- source-sha256: b8374d83cf03093d534c578127771281080337f8703cfbdc79af77751cfefa69 -->
---
name: frame-flowchart-sticky
zh_name: "便利贴流程图帧"
en_name: "Sticky Flowchart Frame"
emoji: "📝"
description: "SVG 曲线连接 + 便利贴节点 + 光标交互，呈现白板头脑风暴效果"
category: video
scenario: operations
aspect_hint: "1920×1080 (16:9)"
featured: 45
tags: ["flowchart", "diagram", "sticky", "whiteboard", "frame"]
example_id: sample-frame-flowchart-sticky
example_name: "便利贴流程图 · 用户引导"
example_format: markdown
example_tagline: "SVG 曲线 + 4 色便利贴"
example_desc: "6 节点用户引导流程，手写体 + 白板纸底"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · 流程图"
---

【模板：便利贴流程图帧 (Sticky Flowchart)】
【意图】把一个流程 / 系统 / 工作流画成“白板 + 便利贴”的样子，适合用户引导视频、运营流程说明、系统架构讲解。灵感来自 hyperframes 流程图。

【画布】1920×1080。背景：米黄白板纸 `#f4ede1` 或冷灰白板 `#f0f2f4`；添加非常浅的六边形网格 `rgba(0,0,0,0.04)`，营造白板质感。

【节点（便利贴）】
- 每个节点 = 一张 240×180px 便利贴，随机分配 4 套颜色：黄 `#fcd34d` / 桃 `#fca5a5` / 薄荷 `#a7f3d0` / 天蓝 `#a5b4fc`。
- 便利贴采用不一致的轻微旋转 `transform: rotate(±2deg)`，投影 `drop-shadow(0 6px 14px rgba(0,0,0,0.12))`，顶部使用胶带 `linear-gradient(...)` 装饰。
- 节点内容：1 个表情符号或单线 SVG 图标 + 大字标题（16-20px）+ 一行描述（12px）。
- 节点字体：`Kalam` / `Caveat` / `Patrick Hand` 等具有手写感的字体（中文使用 `霞鹜文楷` 或 `LXGW WenKai Screen`）。

【连接线（SVG）】
- 使用 `<path>` 贝塞尔曲线连接节点，描边 `#2a2a2a`，宽度 2.5，`stroke-linecap: round`，`stroke-dasharray: 0`（实线）或 `8 6`（虚线 = 条件分支）。
- 箭头末端使用 `marker-end`，采用黑色三角形小箭头。
- 复杂节点可以包含循环或分支：同一节点连出 2 条线（分叉），或 2 条线进入同一节点（合并）。

【可选交互】
- 顶部说明文字（无衬线字体、12px、大写）：”流程 · 迁移 · 2026“。
- 鼠标悬停节点：增强浮起阴影 + `scale 1.05`，使用 CSS 过渡。
- 添加一个“光标”装饰（`<svg>` 箭头 + 名称标签），悬浮在某个节点旁，模拟 Figma 协作光标。

【设计细节】
- 至少 5 个节点，最多 12 个。
- 节点排布不要全部居中对齐，要有一点白板风格的“随手贴”感，但需保证连接线清晰且不交叉。
- 严禁：全屏深色背景、霓虹色、企业仪表盘风格。
- 字体不能使用 Inter / 衬线字体，必须具有手写感。
- 使用单文件 HTML，不要使用外部图标库（使用内联 SVG）。
- 必须使用用户的真实流程内容；节点文字直接来自用户输入。
