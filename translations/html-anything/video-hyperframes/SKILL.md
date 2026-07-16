<!-- source-sha256: ad307163de1690493bb43e213c1e2e83d7f4bb343129a2a933be7888be7d3d27 -->
---
name: video-hyperframes
zh_name: "Hyperframes 视频脚本"
en_name: "Hyperframes 视频"
emoji: "🎞️"
description: "兼容 Hyperframes / Remotion 的连续帧动画，可自动播放"
category: video
scenario: video
aspect_hint: "1920×1080 (16:9)"
recommended: 5
tags: ["video", "hyperframes", "remotion", "视频"]
example_id: sample-hyperframes-workflow
example_name: "Hyperframes · AI 工作流视频"
example_format: markdown
example_tagline: "8 帧自动播放，含进度条 + 元数据"
example_desc: "电影感动画脚本，可直接交给 Remotion 制作成 mp4"
example_source_url: "https://github.com/heygen-com/hyperframes"
example_source_label: "heygen-com/hyperframes"
---

【模板：Hyperframes 视频帧】
- 输出 N 个连续的 `<section class="frame">`，每个为 `w-[1920px] h-[1080px]`；N 由【用户内容】的信息密度决定（短脚本从 6-10 帧起步，长脚本应使用更多帧，每帧只承载一个镜头/概念）。
- 每帧表达一个镜头/概念：文字 + 视觉构图（中央构图 / 黄金分割 / 三分法）。
- 每帧底部添加隐藏标记 `<!-- frame:N duration:3000 transition:fade -->`，供后续 Remotion / Hyperframes 渲染脚本读取。
- 顶部添加一段 JavaScript 自动播放代码：每 3 秒切换到下一帧，也支持点击 / 方向键控制；角落显示进度条。
- 第 1 帧是钩子（一个数据 / 一个反常识观点 / 一个问题），第 2-N 帧用于论证，最后一帧是结论 + 行动号召。
- 字号要巨大（text-9xl），一句话即可，不要堆砌。
- 使用统一的电影感配色方案（深色背景 + 1 个霓虹强调色）。
- 输出末尾包含一段简短注释 `<!-- HYPERFRAMES_META: ... -->`，其中包含每帧 duration / transition / sceneSummary 的 JSON 元数据，用于后续转换为 Remotion。
