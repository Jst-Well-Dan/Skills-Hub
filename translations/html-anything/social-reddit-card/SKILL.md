<!-- source-sha256: 7bbb1639ee11bf9ba5121702d17ade1eaa242bd6f5d3a495113f27ed31b0fae9 -->
---
name: social-reddit-card
zh_name: "Reddit 帖子卡"
en_name: "Reddit Post Card"
emoji: "🔺"
description: "拟真 Reddit 帖子卡 + 上下投票 + 评论数，适合视频叠加 / 故事分享"
category: card
scenario: marketing
aspect_hint: "1280×720 或 800×600"
featured: 42
tags: ["reddit", "social", "card", "overlay", "story"]
example_id: sample-social-reddit-card
example_name: "Reddit 帖子 · r/programming"
example_format: markdown
example_tagline: "Reddit 深色模式 + 投票栏"
example_desc: "一条 AITA 风格故事 + 12.3k 次赞成票 + 1.2k 条评论"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · reddit-post"
---

【模板：Reddit 帖子卡】
【意图】把一段故事 / 提问 / 段子，渲染成 Reddit 帖子卡片，用于视频叠加、社媒故事分享。灵感来自 hyperframes reddit-post。

【画布】1280×720（视频叠加）或 800×600（单卡分享）；背景透明或暗色 `#0b1416`。

【卡片结构】
- 外框：圆角 16px，背景为白色 `#ffffff`（浅色）或 `#1a1a1b`（深色，推荐用于视频叠加），边框 1px `#edeff1` / `#343536`。
- 左侧 **投票栏**（40-56px 宽）：
  - 上箭头 ▲（16px，`#878a8c`，悬停时变为橙色 `#ff4500`）。
  - 票数（Inter，17px，字重 700，居中，颜色：0 为灰色 / 正数为橙色 / 负数为蓝色）；大数字使用 `12.3k` 格式。
  - 下箭头 ▼（悬停时变为蓝色 `#7193ff`）。
- 主体区：
  - 顶部元信息行：子版块图标（CSS 圆形 + 字母）+ `r/subreddit`（粗体）+ `· 发布者 u/username · 3 小时前`（小号灰字）。
  - **标题**（Inter / IBM Plex Sans，22-28px，字重 500，深色文字）。
  - 内容：16px 正文、引用块或 1 张图片（CSS 渐变占位）。
  - 底部操作行：💬 `1.2k 条评论` · 🏆 奖项 · ⤴️ 分享 · ⋯ 图标。
- 顶部右上角放置 Reddit Snoo 徽标（内联 SVG，橙色 `#ff4500`）。

【字体】
- 主字体：`IBM Plex Sans` → 后备字体 `Inter`，字重 400/500/700。
- 数字：与主字体相同。
- 中文：`Noto Sans SC`。

【设计细节】
- 浅色模式：背景 `#fff`，文字 `#1c1c1c`，次要文字 `#7c7c7c`。
- 深色模式（推荐）：背景 `#1a1a1b`，文字 `#d7dadc`，次要文字 `#818384`，边框 `#343536`。
- 票数颜色：正数 = `#ff4500`，负数 = `#7193ff`，0 = `#878a8c`。
- 标题点击区域可添加微妙的悬停背景效果。
- 严禁使用外链图片；图片占位使用 CSS 渐变 + 描述。
- 必须使用用户提供的内容；自动生成合理的 subreddit / username / 票数。
- 单文件 HTML；图标使用内联 SVG（上下箭头、评论气泡、奖杯）。
