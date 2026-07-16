<!-- source-sha256: 8cab21cb0bedb2cdf7c7b35d332352b8268e03e6771445637cd5a71d2e9d96cc -->
---
name: deck-swiss-international
zh_name: "瑞士国际主义演示文稿"
en_name: "Swiss International Deck"
emoji: "🟦"
description: "16 列网格 + 单一饱和强调色 + 22 个锁死版面 (Klein Blue / Lemon / Mint / Safety Orange)"
category: slides
scenario: marketing
aspect_hint: "16:9 横向翻页"
featured: 50
recommended: 2
tags: ["swiss", "grid", "international", "ikb", "editorial", "facts"]
example_id: sample-swiss-international
example_name: "瑞士国际主义 · 产品路线"
example_format: markdown
example_tagline: "Klein Blue IKB + 16 列网格"
example_desc: "S01 Cover + S06 KPI Tower 两页预览，IKB 全屏标题 + 4 柱状 KPI"
example_source_url: "https://github.com/op7418/guizang-ppt-skill"
example_source_label: "op7418/guizang-ppt-skill"
---

【模板：瑞士国际主义演示文稿 (Swiss International)】
【意图】事实、产品、分析、方法论表达。极度冷静、理性、学院派，没有任何手绘 / 噪点 / 装饰。灵感来自 op7418/guizang-ppt-skill 的 Style B。

【主题】**只能从下面 4 套中选择一套，不许混用、不许改 hex**：
- 🔵 **Klein Blue (IKB)** — 强调色 `#002FA7`，纸张色 `#fafaf8`，墨色 `#0a0a0a`。商业 / AI / 设计场景。
- 🟡 **Lemon Yellow** — 强调色 `#FFD500`，纸张色 `#f7f5ee`（淡奶油），墨色 `#0a0a0a`。年轻 / 零售 / 体育。文字必须用黑色（不能用白色）。
- 🟢 **Lemon Green / Neon** — 强调色 `#C5E803`，纸张色 `#f7f5ee`，墨色 `#0a0a0a`。可持续 / 科技初创 / Gen-Z 品牌。文字必须用黑色。
- 🟠 **Safety Orange** — 强调色 `#FF6B35`，纸张色 `#f7f5ee`，墨色 `#0a0a0a`。工业 / 汽车 / 紧急消息。文字用白色 + 粗体 ≥ 600。

【布局 — 22 个可复用版式池，不许新增或改造版式；**数量由内容决定**，把【用户内容】完整覆盖完为止（短内容 6-10 张起步，长内容应远超此范围，同一版式可在不同章节重复使用）】
- **S01 Cover** — 全屏强调色 + ASCII 呼吸点阵 + 反白标题 + 元数据界面元素（日期 / № / 主题）。
- **S02 Vertical Timeline** — 左侧虚线轴 + 圆点；右侧节点 = 年份 + KPI + 描述。
- **S03 Statement** — 9.6vw 居中巨字 + 左侧大段留白 + 底部细线 + 注释。
- **S04 Six Cells** — 2×3 网格，每格：图标 + 编号 + 短标题 + 单行描述。
- **S05 Three Sub-cards** — 左侧主视觉标题 + 右侧 3 张水平堆叠的灰色卡片。
- **S06 KPI Tower** — 4 列高度递增的蓝色柱状图；柱顶图标；柱底大数字 + 标签。
- **S07 H-Bar Chart** — 水平排名横条，宽度反映数据，末端标注数字。
- **S08 Duo Compare** — 垂直分割线；左侧改进前 / 右侧改进后。
- **S09 Closing Manifesto** — 左侧 IKB 色块 + ASCII 点阵 + 宣言；右侧白底 + 3 条要点。
- **S10 Dot Matrix Statement** — 居中宣言 + 角落几何点矩阵 / 圆环矩阵。
- **S11 Horizontal Timeline** — 顶部主标题，中部细线轴，等距节点，节点下方步骤名。
- **S12 Manifesto + Ink Banner** — 上半部主标题 + 解释；下半部全宽黑色横幅 + 反白小字。
- **S13 Three Forces Cards** — 左侧墨色主视觉块；右侧 3 张灰色卡片，每卡：大数字 + 文本。
- **S14 Loop Diagram** — 左侧编号步骤；右侧 SVG 同心环；中心 `"LOOP"` 标签。
- **S15 Image Matrix + Hero Stat** — 4×3 等高卡片（12 项）+ 底部汇总大数字 + 标签。
- **S16 Multi-card Brief** — 3×2 微型卡片；主文位于左上，注脚位于右下，单张卡片用强调色高亮。
- **S17 System Diagram** — 左侧主标题 + 3 段描述；右侧 SVG 三个同心圆 + 外部标签。
- **S18 Why Now** — 3 列，每列：类别标签 + 主标题 + 描述 + 底部数字（最后一列使用强调色）。
- **S19 Four Cards** — 顶部强调色细线 + 主标题 + 4 张等宽卡片（元数据 / 标题 / 正文）。
- **S20 Stacked KPI Ledger** — 垂直行 + 细线分隔；左侧大数字 / 中间标签 / 右侧图标。
- **S21 Tech Spec Sheet** — 左侧标题块 / 中间 3 个 KPI 细线项 / 右侧高度递增的柱状图 / 底部数据。
- **S22 Image Hero** — 上部 60% 全宽图片 + 白色标题块覆盖；下部 40% 解释 + 3 列 KPI。

【设计细节 — 绝对铁律】
- **只用直角**：全程 `border-radius: 0`。圆角 = 立刻违反。
- **1px 细线边框**，使用黑色或强调色；严禁阴影 / 渐变 / 模糊。
- **16 列网格**：`grid-template-columns: repeat(16, 1fr); gap: 0`。
- **字体**：Inter Tight（拉丁文展示字体）/ Inter（正文字体）/ Noto Sans SC（中文）/ JetBrains Mono（数据）；严禁衬线字体、严禁装饰字体。
- **字号极端反差**：封面使用 9.6vw 展示字号，正文 14-16px，标签 11px 大写字母且字间距为 0.08em。
- **键盘 ← / → 切换 + hash 同步**；角标固定：`№N/N` 位于右下角，主题标签位于左下角。
- **不许编造**：数字必须来自用户输入，图表柱高 = 真实数据按比例呈现。
- 输出单文件 HTML，不使用任何外部图片 URL；装饰几何图形（ASCII 矩阵 / 同心圆）使用纯 CSS 或内联 SVG。
