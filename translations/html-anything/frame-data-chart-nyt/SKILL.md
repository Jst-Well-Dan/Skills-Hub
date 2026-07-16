<!-- source-sha256: 8536e1ce1ea4a6b877f940e46235c175a3358a42c8970bb8decc65dace92b847 -->
---
name: frame-data-chart-nyt
zh_name: "NYT 风数据图表帧"
en_name: "NYT 风格数据图表帧"
emoji: "📈"
description: "NYT 新闻编辑室排版 + 错峰揭示动画 + 编辑级图表（折线/柱状/范围带）"
category: video
scenario: video
aspect_hint: "1920×1080 (16:9)"
featured: 46
tags: ["data", "chart", "nyt", "editorial", "frame"]
example_id: sample-frame-data-chart-nyt
example_name: "NYT 风折线图 · 全球用户量"
example_format: markdown
example_tagline: "编辑级图表 + 错峰揭示"
example_desc: "8 年周活跃用户折线 + NYT 红色强调色 + 等宽字体注释"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · data-chart"
---

【模板：NYT 风数据图表帧】
【意图】把一段数据（CSV / JSON / 一句结论）做成《纽约时报》专栏感的单帧/动画图表，适合视频片段或推特卡。灵感来自 hyperframes data-chart。

【画布】1920×1080，暖白底 `#f7f5ee` 或墨黑底 `#0e0e0e` 二选一；文字色和背景相反。

【布局】
- **顶部眉题**（11px 大写字母，字距 0.14em，颜色 = 强调红 `#a91d1d` 或薄荷绿 `#5fb38a`）：数据来源 + 类目，如“全球 · 周活跃用户 · 2018–2026”。
- **大字标题**（Cheltenham / Playfair / Source Serif Pro，5.6vw，可选斜体副标题）：一句结论。**结论必须从用户数据中提炼**，不是描述图。
- **图表区**（占画布 55-65%）：
  - 折线：1-2 条线，主线用墨色实线 2.5px，次线用虚线 1.5px；数据点用 6px 实心圆；关键点旁标注 `2024 · 412M` 黑色等宽小字。
  - 柱状：全部使用墨色单色，或加 1 道强调色高亮柱；柱顶大数字；柱底类目使用斜体（Cheltenham italic）。
  - 范围带（range band）：浅灰填充 `#e6e2d2` 包络 + 墨色中线。
- **底部来源 + 脚注**（10px 等宽字体，opacity 0.6）：“来源：用户数据 · 图表由 html-anything 制作”。
- **错峰揭示动画**：标题淡入（0s），眉题（200ms），折线 `stroke-dashoffset` 动画 1.2s `ease-out`（400ms），数据标签依次间隔 100ms。可被 `prefers-reduced-motion` 关闭。

【设计细节】
- **绝不**：使用 chart.js / d3 库（除非通过 jsdelivr CDN 引入）；推荐手写 SVG，行内代码不超过 80 行。
- 字体：标题 `Source Serif Pro` 或 `Cheltenham`（无则用 `Playfair Display`）；正文 `IBM Plex Sans` 或 `Inter`；数据标签 `IBM Plex Mono`。
- 1 个主色（墨色）+ 1 个强调色（NYT 红 `#a91d1d` / 编辑薄荷绿 `#5fb38a` / 暖橙 `#d97757` 三选一）。
- Y 轴刻度仅使用细线 + 3-4 个刻度，标签使用等宽字体并置于轴外侧。
- 严禁全屏铺设网格线、阴影、3D 立体柱；严禁表情符号。
- 必须用用户提供的数据。如果输入是文本结论，自动估算合理坐标（但要标注“示意图”）；如果是 CSV/JSON，直接绘制。
- 单文件 HTML；数据点旁注释格式：`<text class="annot">2024 · 412M</text>`。
