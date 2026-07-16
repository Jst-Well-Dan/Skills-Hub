<!-- source-sha256: bcfe3092e297a4c6e46fe26fcbb3b9acd0b9d374b90c2900b1f38076de13ad62 -->
---
name: frame-macos-notification
zh_name: "macOS 通知横幅"
en_name: "macOS 通知横幅"
emoji: "🔔"
description: "拟真 macOS 通知横幅 + 应用图标 + 标题正文，适合视频叠加 / 产品发布预告"
category: card
scenario: video
aspect_hint: "1920×1080 视频或 480×120 横幅"
featured: 41
tags: ["macos", "notification", "banner", "overlay", "frame"]
example_id: sample-frame-macos-notification
example_name: "macOS 通知 · 新功能发布"
example_format: markdown
example_tagline: "Big Sur 磨砂玻璃横幅"
example_desc: "应用图标 + 标题 + 双行正文，适合叠加在视频角落"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · macos-notification"
---

【模板：macOS 通知横幅】
【意图】把一段公告 / 消息 / 提示渲染成 macOS Big Sur+ 风格的通知横幅，适合叠加在视频角落、制作产品发布预告和社交媒体图片。灵感来自 hyperframes macos-notification。

【画布】两种用法：
- 视频叠加 1920×1080，通知放在右上角，周围透明。
- 单独横幅 480×120，居中输出。

【横幅结构】
- 外框：圆角 14px（macOS Big Sur 标准），480×120（或更长的 480×180 以容纳正文），12-16px 内边距。
- 背景：**磨砂玻璃**效果 — `background: rgba(245,245,247,0.78)` + `backdrop-filter: blur(40px) saturate(180%)`；暗色版使用 `rgba(28,28,30,0.78)`。
- 边框：1px `rgba(0,0,0,0.06)`（浅色）/ `rgba(255,255,255,0.08)`（深色）；顶部增加 1px 高光 `rgba(255,255,255,0.5)`。
- 阴影：`0 10px 40px rgba(0,0,0,0.18), 0 2px 6px rgba(0,0,0,0.08)`。

【内容】
- 左侧：**应用图标**（44×44，圆角 10px，CSS 渐变 + 1 个表情符号或字母组合，**不用外链图片**）。
- 中间：
  - 顶部行：应用名称（SF Pro 13px，字重 600）+ `现在` 或具体时间（12px，不透明度 0.6）— 两端对齐。
  - 标题（15px，字重 600，截断为 1 行）。
  - 正文（13px，字重 400，截断为 1-2 行，行高 1.35）。
- 右侧（可选）：操作按钮“打开”或“回复”（胶囊形，浅灰色背景）。

【字体】
- 主要字体：`SF Pro Text` → 后备字体 `Inter` / `system-ui`；中文使用 `PingFang SC` / `Noto Sans SC`。

【可选附加】
- 多条通知堆叠：第一条位于最前方，后面 2 条依次向后、向下缩小（缩放 0.96 + 不透明度 0.6 + 纵向位移）。
- 入场动效：从屏幕外右侧滑入 `transform: translateX(110%)→0`，200ms 缓出；可通过 `prefers-reduced-motion` 关闭。
- 右上角控制胶囊“清除”（悬停时显示，默认不透明度为 0）。

【设计细节】
- 浅色模式使用白色磨砂背景，深色模式（推荐用于视频）使用近乎黑色的磨砂背景。
- 图标不能使用外链表情符号图片，应使用 Unicode 表情符号或 CSS 绘制的几何图形。
- 必须使用用户提供的内容；标题和正文应清晰地来自用户输入。
- 使用单文件 HTML，注意 Safari 中的 `backdrop-filter` 需要 `-webkit-` 前缀。
