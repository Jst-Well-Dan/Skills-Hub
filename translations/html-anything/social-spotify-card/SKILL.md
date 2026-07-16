<!-- source-sha256: 7ce215d2eb580cf939b7826d34893e8d37adb5e2608526871952b9ced33136af -->
---
name: social-spotify-card
zh_name: "Spotify 正在播放卡"
en_name: "Spotify Now-Playing Card"
emoji: "🎵"
description: "Spotify 正在播放风格卡片：专辑封面 + 进度条 + 播放控制，适配视频叠加层 / 个人主页"
category: card
scenario: personal
aspect_hint: "1280×720 或 600×200"
featured: 43
tags: ["spotify", "music", "now-playing", "card", "overlay"]
example_id: sample-social-spotify-card
example_name: "Spotify 正在播放 · Lo-Fi"
example_format: markdown
example_tagline: "Spotify 经典深色卡片"
example_desc: "Lo-Fi Beats · Chillhop 进度条 1:24 / 3:42 + 控制行"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · spotify-card"
---

【模板：Spotify 正在播放卡】
【意图】把一首歌、一段播客或一段个人介绍渲染成 Spotify 正在播放卡，适合视频叠加层 / 个人介绍页面 / 创作者首屏。灵感来自 hyperframes spotify-card。

【画布】两种尺寸：
- 横版视频叠加层：1280×720，卡片居中或悬浮在左下角。
- 紧凑横条组件：600×200，可嵌入任何首屏区域。

【卡片结构】
- 外框：圆角 12-16px；背景使用从专辑封面提取颜色形成的暗色渐变（例如 `linear-gradient(135deg, #1e3264 0%, #0d1f3d 100%)`），或使用 Spotify 经典 `#121212`；边缘带有 1px 淡雅边框。
- 左侧：**专辑封面**（使用 CSS 渐变 + 大号字母组合或抽象几何图形绘制，不能使用外链图片），圆角 6px，60-200px 方形。
- 右侧：
  - 顶部 `NOW PLAYING`（大写，字间距 0.14em，11px，绿色 `#1DB954`）。
  - **歌名 / 标题**（Inter / Spotify Circular，22-28px，字重 700，白色）。
  - **艺人 / 副标题**（16px，字重 400，不透明度 0.7）。
  - 进度条：高 4px，圆角，灰色背景 + 白色已播放部分（`width: 38%`）；两端时间戳 `1:24 / 3:42`（等宽字体，11px，灰色）。
  - 控制行：⏮ ⏯ ⏭ 图标（内联 SVG，24px，白色填充），随机播放 / 循环播放图标稍小。
- 右上角：Spotify 标志（内联 SVG，绿色 `#1DB954` 圆形 + 三道白色波纹）。
- 可选：右下角小型音波动画（3 个柱条，使用 `@keyframes`）。

【字体】
- 主要字体：`Spotify Circular` → 后备字体 `Inter` / `Inter Tight`，字重 400 / 700。
- 数字：使用与主要字体相同的字体，避免过多使用等宽字体。

【设计细节】
- Spotify 经典深色模式：`#121212` 背景，`#1DB954` 强调色，`#b3b3b3` 次要文本。
- 若用户输入是文本/标题 → 将“标题”作为歌名，将“副标题/作者”作为艺人，默认估算“时长”为 3:42。
- 若用户输入与音乐相关 → 直接对应。
- 严禁使用外链图片；封面使用 CSS 渐变 + 文字标志 / 几何图形绘制。
- 微动画：音波动画使用 `@keyframes`，并可通过 `prefers-reduced-motion` 关闭。
- 使用单文件 HTML。
