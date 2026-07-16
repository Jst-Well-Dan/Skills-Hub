<!-- source-sha256: 5a13f7e217ef352887ae0045c09dcedf18a01ea2094d7a6ab5d4329271670ad7 -->
---
name: ppt-keynote
zh_name: "Keynote 风格 PPT"
en_name: "Keynote 风格幻灯片"
emoji: "🎬"
description: "苹果 Keynote 级别幻灯片，一屏一卡，键盘左右切换"
category: slides
scenario: marketing
aspect_hint: "16:9 (1280×720)"
featured: 19
tags: ["slides", "deck", "presentation", "幻灯片", "演讲"]
example_id: sample-ppt-html-anything
example_name: "Keynote PPT · 产品介绍"
example_format: markdown
example_tagline: "用 7 张幻灯片讲清产品"
example_desc: "苹果 Keynote 风格的产品介绍，使用 ←/→ 切换"
---

【模板：Keynote 风格 PPT】

- 每张幻灯片都是一个 `<section class="slide">`，整体宽 1280、高 720，居中显示，使用渐变背景。
- 单页内容极简：大标题 + 1～3 行辅助文字；或一张数据图；或一句金句。
- 字号：标题使用 `text-7xl font-semibold tracking-tight`，副标题使用 `text-2xl text-neutral-500`。
- 第一页是封面（主题 + 演讲者 / 日期），最后一页是“谢谢。”或行动号召。
- 右上角放置小型指示器：当前页 / 总页数。
- 添加一段 JavaScript，监听 ArrowLeft / ArrowRight / 空格键以切换 slide；同时维护 hash（#/3）。
- 每页之间使用 fade-in 动画。
- 保持充足留白，数据卡片使用 grid 布局对齐，配色克制。
