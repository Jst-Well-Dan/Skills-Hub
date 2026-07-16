<!-- source-sha256: 4d0679eaf9734f721e7e689623ce5a616e6277afb9155290fdd66ac0afac57b9 -->
---
name: social-x-post-card
zh_name: "X（Twitter）帖子卡"
en_name: "X / Twitter 帖子卡"
emoji: "𝕏"
description: "拟真 X 推文卡片 + 互动数据（点赞/转推/浏览量），适配视频叠加或图卡分享"
category: card
scenario: marketing
aspect_hint: "1280×720 或 1080×1080"
featured: 44
tags: ["twitter", "x", "social", "card", "overlay"]
example_id: sample-social-x-post-card
example_name: "X 帖子卡 · AlchainHust 金句"
example_format: markdown
example_tagline: "X 深色模式 + 互动数据"
example_desc: "一条金句推文 + 12.3K 次点赞 / 1.2K 次转推 + 蓝勾"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · x-post"
---

【模板：X（Twitter）帖子卡】
【意图】把一段推文内容（或用户的金句）渲染成一张拟真度极高的 X 帖子卡片，用于视频叠加、推特发图、知识沉淀。灵感来自 hyperframes x-post。

【画布】1280×720 或 1080×1080，暗背景 `#0f1419` 或亮背景 `#ffffff`（按 X 主题）；卡片居中，阴影柔和。

【卡片结构】
- 外框：圆角 16px，1px 边框 `#2f3336`（深色）/ `#eff3f4`（浅色），内边距 16px。
- 顶部行：头像（48×48 圆形，用 CSS 渐变占位）+ 用户名 + 用户标识 `@username` + 蓝色认证勾 + 时间（等宽字体，12px，灰色）。
- 正文：17-22px，字重 400；链接用 X 蓝 `#1d9bf0`；话题标签同色；用户提及同色；段落间空 0.6em。
- 可选：引用卡（小卡内嵌，灰底，圆角 12px）。
- 可选：1 张图（CSS 渐变 + 描述占位，不能外链图片），比例 16:9，圆角 12px。
- 互动行：4 个图标 + 数字（回复 / 转推 / 引用 / 点赞），图标用内联 SVG（X 官方风格），灰色，悬停时变色。
- 顶部右上角放置 X 标志的单线 SVG。
- 浏览量行：👁️ + 数字（小字）。

【字体】
- 西文：`Chirp`（X 的字体）→ 后备字体 `Inter` 或 `Segoe UI`。
- 中文：`Noto Sans SC` / `PingFang SC`。
- 数字：同主字体，不用等宽字体。

【设计细节】
- 浅色配色：背景 `#fff`，文字 `#0f1419`，次要文字 `#536471`，边框 `#eff3f4`，强调色 `#1d9bf0`。
- 深色配色（推荐，用于视频叠加）：背景 `#000`，文字 `#e7e9ea`，次要文字 `#71767b`，边框 `#2f3336`，强调色 `#1d9bf0`。
- 数字格式化：1.2K / 4.5M（不要原始 1234）。
- 内容必须来自用户输入，不能编造推文。
- 若用户输入是数据 → 自动总结成一句“金句”推文（≤ 280 字符）。
- 单文件 HTML；图标使用内联 SVG；不要任何外部图片 URL。
- 可选：卡片背后加微妙的径向高光 `radial-gradient(...)`，增加视频叠加时的可读性。
