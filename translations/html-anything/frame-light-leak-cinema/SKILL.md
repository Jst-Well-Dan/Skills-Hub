<!-- source-sha256: 8762e5951a80c3a152d0a9e10b2dfe61e1cca1b7d4e31b759ff982b0dbad247c -->
---
name: frame-light-leak-cinema
zh_name: "胶片漏光电影帧"
en_name: "漏光电影帧"
emoji: "🎞️"
description: "胶片漏光 + 颗粒噪点 + 16:9 黑边画幅 + 衬线大字, 电影感开场 / 章节卡"
category: video
scenario: video
aspect_hint: "2.39:1 黑边画幅 (1920×800) 或 16:9 (1920×1080)"
featured: 36
tags: ["cinema", "film", "light-leak", "grain", "letterbox", "frame"]
example_id: sample-frame-light-leak-cinema
example_name: "胶片漏光 · 胶卷 03"
example_format: markdown
example_tagline: "暖橙漏光 + 35mm 颗粒"
example_desc: "2.39:1 黑边画幅 + 衬线斜体大字 + 胶片齿孔"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · 漏光"
---

【模板: 胶片漏光电影帧】
【意图】纪录片 / 个人短片 / 视频章节卡的开场单帧 —— 暖橙漏光 + 35mm 颗粒 + 衬线大字, 古典胶片质感。灵感源自 hyperframes 漏光效果。

【画布】
- **2.39:1 黑边画幅** (推荐): 1920×800, 上下黑边各 140px (`#000`)。
- 或 16:9: 1920×1080, 无黑边。

【背景】
- 底层: 深暖色 (深红棕 `#1a0d08` / 墨绿 `#0a1410` / 蓝紫 `#0d0e1a`) 或场景描绘 (CSS gradient 模拟天空 / 室内 / 室外)。
- **胶片漏光**: 2-3 个大 `radial-gradient(ellipse at top right, #ffb547 0%, transparent 50%)` + 1 个底部 `linear-gradient(to top, #d97757 0%, transparent 30%)`; 颜色取暖橙 / 桃 / 玫红 / 暗黄, **不要冷蓝**。
- **35mm 颗粒**: 全屏覆盖 SVG turbulence noise 图层, opacity 14%, `mix-blend-mode: overlay`; 也可用 `background-image: url("data:image/svg+xml,...feTurbulence...")`。
- 可选: 1 道 `feDisplacementMap` 模拟胶片摆动 (慎用)。

【文字】
- 中央或左下: 大字衬线 (Source Serif Pro / Playfair Display / EB Garamond) 5-8vw, weight 500 italic; 颜色暖白 `#f5e9d6` 或奶油色。
- 副标 (24-28px) 一行, opacity 0.7, 同样衬线。
- 角落说明文字 (大写字母、字距 0.18em, 10-11px, 等宽字体, opacity 0.5): "胶卷 03 · 第一章 · 1985"。
- 底部时间码 + 拍摄地 + 日期 (等宽字体, opacity 0.4)。

【可选附加】
- "胶片划痕": 几条 1-2px 竖向白线, opacity 0.2, 不规则间距 (用 `box-shadow` 多重 inset 或多个 `<div>`)。
- "胶片齿孔": 黑边内, 等距小白方块 (CSS repeating-linear-gradient)。
- 入场动效: 整画面从欠曝 (brightness 0.3) → 正常, 800ms 内; 漏光位置缓慢漂移 12s 一个周期。

【设计细节】
- 颜色绝不超过 4 个色相 (深背景 + 2 个暖漏光色 + 文字奶油色)。
- 严禁: 蓝紫漏光 (违反胶片质感)、emoji、霓虹色、几何仪表盘装饰。
- 中文: `Noto Serif SC` italic 不存在 → 用 `Noto Serif SC` regular + 字距加大。
- 必须用用户提供的标题; 自动估算合理"年份 / 章节 / 地点" 元数据 (但来源用户内容)。
- 单文件 HTML, 用 `prefers-reduced-motion` 关动效。
