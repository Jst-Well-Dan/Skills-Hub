<!-- source-sha256: 61e081c3c046530f544c7738c0acbe5a647b2009699a4bf72f50a23eb6c381bc -->
---
name: deck-guizang-editorial
zh_name: "贵赞编辑墨水 Deck"
en_name: "Guizang Editorial E-Ink Deck"
emoji: "🖋️"
description: "电子杂志 × 电子墨水; 10 个版面 + 5 套调色板 (墨水/靛蓝瓷/森林墨/牛皮纸/沙丘)"
category: slides
scenario: marketing
aspect_hint: "16:9 横向翻页"
featured: 49
recommended: 1
tags: ["editorial", "e-ink", "magazine", "narrative", "guizang"]
example_id: sample-guizang-editorial
example_name: "贵赞编辑墨水 · 章节封页"
example_format: markdown
example_tagline: "墨水经典调色板 + 衬线展示字体"
example_desc: "L02 章节分隔页 + L03 大数字网格数据格，纸感印刷"
example_source_url: "https://github.com/op7418/guizang-ppt-skill"
example_source_label: "op7418/guizang-ppt-skill"
---

【模板：贵赞编辑墨水幻灯片（编辑风格 × 电子墨水）】
【意图】叙事、观点、分享、个人风格表达。墨纸印刷感，不要科技感。灵感源自 op7418/guizang-ppt-skill Style A。

【调色板 — 5 选 1，严禁改 hex、严禁混用】
- 🖋 **墨水经典 Monocle** — 墨色 `#0a0a0b`，纸色 `#f1efea`，浅纸色 `#e8e5de`，浅墨色 `#18181a`。默认 / 通用商业 / 科技。
- 🌊 **靛蓝瓷 Indigo Porcelain** — 墨色 `#0a1f3d`，纸色 `#f1f3f5`，浅纸色 `#e4e8ec`，浅墨色 `#152a4a`。科技 / 研究 / 数据。
- 🌿 **森林墨 Forest Ink** — 墨色 `#1a2e1f`，纸色 `#f5f1e8`，浅纸色 `#ece7da`，浅墨色 `#253d2c`。自然 / 可持续 / 文化。
- 🍂 **牛皮纸 Kraft Paper** — 墨色 `#2a1e13`，纸色 `#eedfc7`，浅纸色 `#e0d0b6`，浅墨色 `#3a2a1d`。怀旧 / 人文 / 文学。
- 🌙 **沙丘 Dune** — 墨色 `#1f1a14`，纸色 `#f0e6d2`，浅纸色 `#e3d7bf`，浅墨色 `#2d2620`。艺术 / 设计 / 时尚。

【布局 — 10 个磁带式版式池，可复用；**数量由【用户内容】决定**，完整覆盖每个要点；短内容 6-12 张起步，长内容应更多（同一版式可在不同章节重复使用）】
- **L01 主视觉封面** — 居中大字主视觉排版 + 引题 + 副标题 + 导语段落 + 底部元数据行。
- **L02 章节分隔页** — 引题 + 8.5-10vw 巨大标题 + 一句引言；章节切换可反色（墨色 ↔ 纸色）。
- **L03 大数字网格** — 3×2 数据卡（标签 / 大数字 / 注释）。
- **L04 引文 + 图片** — 左侧引题 + 标题 + 正文 + 强调文字；右侧 16:10 图片（按基线对齐，而非顶部对齐）。
- **L05 图片网格** — 3×2 或 3×1 等高图片网格（26vh 或 22vh）；严格统一高度。
- **L06 流程 / 步骤流** — 横向编号步骤组，每步：№X + 标题 + 描述；支持键盘逐步推进。
- **L07 核心问题** — 7vw 全屏单一问句，按语义断行，周围极简。
- **L08 大型引文** — 5.8vw 巨大衬线引文 + 英文翻译 + 署名 + 日期。
- **L09 前后对比** — 1:1 分栏；左列 opacity .55（旧/之前）；右列全亮度（新/之后）。
- **L10 混合媒体** — 8:4 比例；左侧大段文字（引题 / 标题 / 正文 / 强调文字）+ 右侧 3:4 竖图作辅助。

【设计细节】
- **严禁**：渐变 / 投影 / 圆角 / 圆形装饰 / 模糊 / SVG 图标库 / emoji 装饰。
- **字体**：展示字体用 `Playfair Display`（英）/ `Noto Serif SC`（中）；正文字体用 `Inter` / `Noto Sans SC`；编号 / 数字偶尔可用斜体衬线。
- **杂志感细节**：引题用 11px 大写字母，letterspacing 0.12em；页码右下角 `01 / 12`；顶部细发丝线 + 期刊标志 / 主题。
- **不许**：数据捏造、Lorem ipsum、占位图片 URL。所有图片请用纯 CSS / SVG 内联描绘（色块 + 简笔）。
- 键盘 ← / → 切换；hash 同步；单文件 HTML。
