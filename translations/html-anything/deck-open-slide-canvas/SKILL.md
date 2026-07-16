<!-- source-sha256: 3e072c6fcd09e7dfe6bf5d33bf62c9ed55de5fcd4c4e475500ab1c1059a0076e -->
---
name: deck-open-slide-canvas
zh_name: "1920 画布自由幻灯片"
en_name: "开放式幻灯片 1920 画布演示文稿"
emoji: "🎨"
description: "锁死 1920×1080 画布，React 组件级自由组合，不绑模板"
category: slides
scenario: design
aspect_hint: "1920×1080 (16:9)"
featured: 35
recommended: 9
tags: ["canvas", "open-slide", "freeform", "1920", "react"]
example_id: sample-deck-open-slide-canvas
example_name: "1920 自由画布 · 海靛蓝"
example_format: markdown
example_tagline: "锁死 1920×1080 + 自由组合"
example_desc: "海靛蓝调色 + 一页大字提问 + 角标"
example_source_url: "https://github.com/1weiho/open-slide"
example_source_label: "1weiho/open-slide"
---

【模板：1920 画布自由幻灯片】
【意图】适用于不想被模板束缚的场景（个人作品集、奇特演讲、艺术 / 设计课演示文稿）。提供一个固定的 1920×1080 画布，加上极强的类型 / 调色约束，让智能体像编写 React 组件一样，根据内容自由排布每一页。灵感来自 1weiho/open-slide。

【硬性技术规格】
- 画布：每页严格使用 `width: 1920px; height: 1080px;`，通过 `transform: scale(...)` 适配视窗（默认使用 `scale(0.7)` 居中）。
- **绝对禁止溢出**：每页内容必须完整容纳在 1920×1080 范围内，不允许出现滚动条。
- 字号比例（px）：`2xs:18 · xs:22 · sm:28 · md:36 · lg:48 · xl:64 · 2xl:88 · 3xl:120 · 4xl:160 · 5xl:220`。
- 内边距：从 96 / 128 / 160 三档中选择一档。
- 每页包含 `<section class="slide" data-slide-id="<n>">`。

【调色板——每份演示文稿选择 1 套，全程不变】
- 🌫 **灰烬与青柠**——背景 `#f1efea`，文字 `#161616`，强调色 `#c5e803`。
- 🌌 **海靛蓝**——背景 `#0a0e1a`，文字 `#f5f5f7`，强调色 `#5ac8fa`。
- 🧉 **马黛摩卡**——背景 `#1a1411`，文字 `#f5e9d6`，强调色 `#d97757`。
- 🌸 **珍珠玫瑰**——背景 `#fdf6f3`，文字 `#1a1015`，强调色 `#ff5d8f`。

【布局自由度——这是核心】
- 不强制使用模板，每页根据**内容性质**自行选择布局：封面 / 提问 / 引语 / 图文 / 三列 / 五列 / 列表 / 数据卡片 / 满版图片。
- 但每页**必须遵守一条规则**：视觉层级中只能有 1 个重心——一句金句、一个数字或一张图片，不要“什么都强调”。
- 不允许塞入两段权重相同的文字；如果确实需要并列，就使用三列等权重网格。

【字体】
- 西文：`Inter Tight`（展示字体）+ `Inter`（正文字体）；或在采用编辑风格时使用 `Source Serif Pro`。
- 中文：`Noto Sans SC`（无衬线风格）或 `Noto Serif SC`（编辑风格）；不要混用无衬线体和衬线体。
- 等宽字体：数据 / 时间戳使用 `JetBrains Mono`。

【设计细节】
- 严禁使用 emoji 作为装饰（内容中的 emoji 允许使用）；严禁使用多色彩虹效果；强调色只能使用一种。
- 严禁套用 lucide / feather 等通用库中的 SVG 图标（自行编写内联 SVG）。
- 添加键盘 ← / → 切换和 hash 同步；角标固定：右下角显示 `№N/M`，左下角显示演示文稿标题。
- 必须使用用户的真实内容；严禁使用 lorem ipsum。
- 使用单文件 HTML；使用 Tailwind CDN；不要使用外链图片。
