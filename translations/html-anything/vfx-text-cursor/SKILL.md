<!-- source-sha256: 9e71d760910de732f5ad0ff7ed229330eec84fbe1825caaaab8dd4d10c2cf082 -->
---
name: vfx-text-cursor
zh_name: "VFX 文字光标"
en_name: "VFX Text Cursor"
emoji: "✨"
description: "光标拖光 + 彩色像散射线 + 定向光斑, 适合视频片头逐字揭示金句"
category: video
scenario: video
aspect_hint: "1920×1080 (16:9)"
featured: 38
recommended: 7
tags: ["vfx", "text", "cursor", "chromatic", "reveal", "frame"]
example_id: sample-vfx-text-cursor
example_name: "VFX 光标 · 开场金句"
example_format: markdown
example_tagline: "逐字揭示 + 彩色像散拖光"
example_desc: "光标打字采用亮粉色 + 青色像散, 用于视频开场"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · vfx-text-cursor"
---

【模板: VFX 文字光标 (Text Cursor)】
【意图】视频开场/主视觉帧 —— 光标在画布上“打字”, 文字逐字浮现, 后面拖着彩色像散尾迹 + 定向光斑。灵感来自 hyperframes vfx-text-cursor。

【画布】1920×1080, 背景 `#06070a` 暗哑黑 或 `#0a0d12` (带暖调的蓝色); 加微妙暗角。

【内容】
- 一句金句 (中英不限), 居中, 字号 6-8vw, 字重 700, 字体 `Inter Tight` / `Source Sans 3` / `Noto Sans SC`。
- 逐字揭示, 每个字符间隔 80ms; 当前字符后面跟着一个光标 `▍` (或细竖线)。
- 已揭示文字默认白色 `#f5f5f7`, 不透明度 1; 即将揭示位置加彩色像散残影: 在揭示瞬间应用一份 `text-shadow: 2px 0 #ff3b6f, -2px 0 #00d4ff`, 200ms 内收敛回正常。
- 光标本身: 16px 宽矩形, 颜色 = 强调色 (取 1: 亮粉色 `#ff3b6f` / 青色 `#00d4ff` / 琥珀色 `#ffb547`), 以 `@keyframes` 实现 1.0s 周期闪烁; 后面拖一条 60-120px 的运动模糊尾迹 (径向渐变至透明)。

【光斑 / 射线】
- 在打字位置附近随机生成 3-5 道**定向光斑** (漏光): 使用 `linear-gradient(45deg, transparent, accent20, transparent)` 的细长矩形 + `mix-blend-mode: screen`, 角度不规则。
- 当文字打完, 整段文字添加 0.5s 微光扫过效果 (光带横扫)。

【字段】
- 顶部说明文字 (大写字母间距 0.18em, 11px, 不透明度 0.5): "FRAME 01 · OPENING"。
- 文字下方副标题 (24-28px, 不透明度 0.6): 来源 / 章节。
- 右下角时间码 (`00:03:21` 等宽字体)。

【设计细节】
- **绝不**: 使用多色彩虹式彩色像散 (只用 1 组亮粉色 + 青色这样的二元像散, 不要 R/G/B 全色)。
- 字体: 西文 `Inter Tight` 粗体; 中文 `Noto Sans SC` 粗体; 严禁衬线。
- 动效使用 `@keyframes` + JS 计时器 (`setTimeout` 逐字), 可通过 `prefers-reduced-motion` 关闭 (直接显示所有文字)。
- 必须使用用户提供的金句; 不要捏造。
- 单文件 HTML, 除字体外不要外链资源。
