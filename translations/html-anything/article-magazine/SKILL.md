<!-- source-sha256: 1b580ad6e9cbf22f46e4dbb0cce88290cb4ba74500753f360139397d5ca43da3 -->
---
name: article-magazine
zh_name: "杂志文章"
en_name: "杂志文章"
emoji: "📖"
description: "Substack / Medium 高级感长文排版，适合公众号、博客发布"
category: article
scenario: marketing
aspect_hint: "A4 / 长页面"
featured: 11
tags: ["博客", "随笔", "新闻通讯", "公众号", "博客", "文章"]
example_id: sample-article-trq212-html
example_name: "杂志文章 · HTML 取代 Markdown"
example_format: markdown
example_tagline: "灵感来自 @trq212 的推文"
example_desc: "围绕「AI 时代 HTML > Markdown」的延伸评论，含原推附注与可点击链接"
example_source_url: "https://x.com/trq212/status/2052809885763747935"
example_source_label: "@trq212 / x.com"
---

【模板：杂志文章】
- 顶部主视觉区：大标题 (text-5xl/6xl) + 可选副标题 + 作者 / 阅读时间 / 日期元数据。
- 正文：单栏，最大宽度约 700px，居中。段落 `text-lg leading-relaxed text-neutral-700 dark:text-neutral-300`。
- H2 / H3 标题使用衬线字体，让正文与标题形成视觉对比。
- 引用块使用左侧粗强调色边线 + 斜体。
- 代码块：圆角 + 深色背景 + 浅色文字，显示语言标签。
- 列表项使用自定义项目符号（小方块 / 强调色圆点）。
- 章节之间用 `<hr>` 分隔，但样式设计成中央居中的小装饰。
- 文末添加一个简单的“如果觉得有用，欢迎转发”行动卡片。
