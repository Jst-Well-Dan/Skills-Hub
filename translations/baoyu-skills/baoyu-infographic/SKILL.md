<!-- source-sha256: 1572aaa294c5f7547889f520b6efeed979aeaaf58b4e7c4bcaaa26ace2ee3564 -->
---
name: baoyu-infographic
description: 使用 21 种布局类型和 22 种视觉风格生成专业信息图。分析内容、推荐布局×风格组合，并生成可直接发布的信息图。当用户要求创建“infographic”“信息图”“visual summary”“可视化”或“高密度信息大图”时使用。
version: 1.117.4
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-infographic
---

# 信息图生成器

两个维度：**布局**（信息结构）×**风格**（视觉美学）。可自由组合任意布局与任意风格。

## 用户输入工具

当此技能需要向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具**，即当前智能体运行时所提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **后备方案**：如果不存在此类工具，则发送带编号的纯文本消息，并要求用户针对每个问题回复所选编号/答案。
3. **批量提问**：如果工具支持单次调用提出多个问题，则将所有适用问题合并到一次调用中；如果仅支持单个问题，则按优先级逐个提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行时中请替换为本地等效工具。

## 图像生成工具

当此技能需要渲染图像时，请按以下顺序确定后端：

1. **当前请求覆盖项**——如果用户在当前消息中指定了特定后端，则使用该后端。
2. **已保存的偏好设置**——如果 `EXTEND.md` 将 `preferred_image_backend` 设置为当前可用的后端，则使用该后端。
3. **自动选择**（当偏好设置为 `auto`、未设置或固定的后端不可用时）：
   - **Codex (`imagegen`)**——首先检查可用技能/工具清单。如果列出了名为 `imagegen` 的技能，则说明你正在 Codex 中运行，并且必须使用它：通过 `Skill` 工具调用并传入 `skill: "imagegen"`，同时传递已保存提示词文件的内容（以及 Codex `imagegen` 自身参数所要求的输出路径和宽高比）。Codex `imagegen` 是该运行时中的官方光栅图像后端，优先级高于任何非原生技能（例如 `baoyu-image-gen`），除非用户明确固定了其他 `preferred_image_backend`。
   - **通过 `codex exec` 使用 Codex (`codex-imagegen`)**——如果当前运行时未提供原生 `imagegen` 技能，但 `codex` CLI 位于 `PATH` 中且存在有效的 `codex login`，则通过 `baoyu-image-gen --provider codex-cli` 路由（首选）；如果 baoyu-image-gen 不可用，则直接调用随附的包装器。详细说明、参数和运行时发现流程位于 [references/codex-imagegen.md](references/codex-imagegen.md) 中——仅在选择此分支时加载该文件。
   - **Cursor (`GenerateImage`)**——如果运行时提供原生 `GenerateImage` 工具，则说明你正在 Cursor 中运行，其优先级与 Codex `imagegen` 一样高于任何非原生技能。需注意两个严格限制：(a) 它没有宽高比参数——必须在作为 `description` 传入的提示词文本中明确说明目标宽高比/尺寸；(b) 它不接受输出目录——文件会保存到工具管理的位置，因此生成后需将文件复制/移动到技能预期的输出路径（例如 `outputs/.../NN-xxx.png`）。参考图像应放入 `reference_image_paths`。
   - **其他运行时原生工具**——如果运行时提供其他原生图像工具（例如 Hermes `image_generate`），请以相同方式使用。
   - 否则，如果仅安装了一个非原生后端（例如 `baoyu-image-gen`），则使用该后端。
   - 否则（存在多个非原生后端，但没有运行时原生工具），向用户询问一次——与其他初始问题合并提问。
4. **如果没有任何可用后端**，请告知用户并询问如何继续。

**⛔ 切勿使用 SVG、HTML、canvas 或其他基于代码的渲染方式替代光栅图像生成。** Codex `imagegen` 自身的描述指出，应在“输出应为位图资源，而不是仓库原生代码或矢量图”时使用它。如果无法通过步骤 3 确定光栅后端，请转到步骤 4 并询问用户——**不要**擅自输出 SVG、编写内联 `<svg>` 标记或生成 HTML/CSS 图像作为替代。即使文章/章节看起来“像图表”，此规则同样适用：调用此规则的上游技能已经确定其所需的是光栅图像。

**⛔ 切勿通过在已生成的位图上涂盖来修复渲染文本。** 不得使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化叠加方式来遮盖、重写、擦除、描边或替换已生成信息图中的标签、标题、标注、数据值或任何其他文本。如果文本有误或不清晰，请使用修正后的提示词重新生成、切换到图中文字更少的布局，或询问用户要保留哪个不完美的候选版本。

设置 `preferred_image_backend: ask` 会强制每次运行时都执行步骤 3 的询问，无论有哪些可用后端。用户可通过下方的 `## 更改偏好设置` 章节修改固定后端。

**提示词文件要求（强制）**：在调用任何后端之前，必须将每张图像完整、最终的提示词写入 `prompts/` 下的独立文件（命名格式：`NN-{type}-[slug].md`）。后端接收提示词文件（或其内容）；该文件是用于复现的记录，并允许在无需重新生成提示词的情况下切换后端。

上文中的具体工具名称（`imagegen`、`GenerateImage`、`image_generate`、`baoyu-image-gen`）仅为示例——请按照相同规则替换为本地等效工具。

## 参考图像

用户可以提供参考图像，用于指导风格、配色、构图或主体。

**接收方式**：通过 `--ref <files...>` 接收，或在用户于对话中提供文件路径/粘贴图像时接收。
- 文件路径 → 将文件复制到输出旁的 `refs/NN-ref-{slug}.{ext}`
- 粘贴但没有路径的图像 → 按照上方“用户输入工具”规则向用户询问路径，或将口头提取的风格特征作为文本后备方案
- 没有参考图像 → 跳过本节

**使用模式**（针对每张参考图像）：

| 用法 | 效果 |
|-------|--------|
| `direct` | 将文件作为参考图像传递给后端 |
| `style` | 提取风格特征（线条处理、纹理、氛围）并追加到提示词正文 |
| `palette` | 从图像中提取十六进制颜色并追加到提示词正文 |

存在参考图像时，**记录在 `prompts/infographic.md` 的 frontmatter 中**：

```yaml
references:
  - ref_id: 01
    filename: 01-ref-brand.png
    usage: direct
```

**生成时**：
- 验证每个引用的文件是否存在于磁盘上
- 如果 `usage: direct` 且所选后端接受参考图像（例如通过 `--ref` 使用 `baoyu-image-gen`）→ 通过后端的参考图像参数传入文件
- 否则 → 将提取出的 `style`/`palette` 特征嵌入提示词文本

## 确认策略

默认行为：**生成前确认**。

- 明确调用技能、文件路径、匹配到的关键词快捷方式、`EXTEND.md` 默认值以及文档中的默认组合，均仅视为**推荐依据**。它们都不构成跳过确认的授权。
- 在用户确认组合/宽高比/语言/后端选项之前，**不要**开始步骤 5 或步骤 6。
- 仅当当前请求明确要求跳过确认时才可跳过，例如：`--no-confirm`、“直接生成”、“不用确认”、“跳过确认”、“按默认出图”或等效表述。
- 如果用户明确要求跳过确认，则在生成前的下一条面向用户的进度更新中说明所采用的组合/宽高比/语言/后端。

## 选项

| 选项 | 值 |
|--------|--------|
| `--layout` | 21 个选项（参见布局库），默认：bento-grid |
| `--style` | 22 个选项（参见风格库），默认：craft-handmade |
| `--aspect` | 命名选项：landscape (16:9)、portrait (9:16)、square (1:1)。自定义：任意 W:H 比例（例如 3:4、4:3、2.35:1） |
| `--lang` | en、zh、ja 等 |
| `--no-confirm` | 仅当用户明确要求无需确认直接生成时，跳过步骤 4 |
| `--ref <files...>` | 用于指导风格/配色/构图/主体的参考图像（文件路径） |

## 布局库（21）

| 布局 | 最适合 |
|--------|----------|
| `linear-progression` | 时间线、流程、教程 |
| `binary-comparison` | A 与 B、前后对比、优缺点 |
| `comparison-matrix` | 多因素比较 |
| `hierarchical-layers` | 金字塔、优先级层次 |
| `tree-branching` | 类别、分类体系 |
| `hub-spoke` | 中心概念及相关项目 |
| `structural-breakdown` | 爆炸图、剖面图 |
| `bento-grid` | 多主题、概览（默认） |
| `iceberg` | 表层与隐藏层面 |
| `bridge` | 问题与解决方案 |
| `funnel` | 转化、筛选 |
| `isometric-map` | 空间关系 |
| `dashboard` | 指标、KPI |
| `periodic-table` | 分类集合 |
| `comic-strip` | 叙事、序列 |
| `story-mountain` | 情节结构、张力曲线 |
| `jigsaw` | 相互关联的组成部分 |
| `venn-diagram` | 重叠概念 |
| `winding-roadmap` | 旅程、里程碑 |
| `circular-flow` | 循环、重复发生的流程 |
| `dense-modules` | 高密度模块、数据丰富的指南 |

完整定义位于 `references/layouts/<layout>.md`。

## 风格库（22）

| 风格 | 描述 |
|-------|-------------|
| `craft-handmade` | 手绘、纸艺（默认） |
| `claymation` | 3D 黏土角色、定格动画 |
| `kawaii` | 日式可爱、柔和粉彩 |
| `storybook-watercolor` | 柔和绘画、奇思妙想 |
| `chalkboard` | 黑板粉笔画 |
| `cyberpunk-neon` | 霓虹光效、未来感 |
| `bold-graphic` | 漫画风格、半色调 |
| `aged-academia` | 复古科学、棕褐色调 |
| `corporate-memphis` | 扁平矢量、鲜艳活泼 |
| `technical-schematic` | 蓝图、工程制图 |
| `origami` | 折纸、几何造型 |
| `pixel-art` | 复古 8 位像素 |
| `ui-wireframe` | 灰度界面线框稿 |
| `subway-map` | 交通线路图 |
| `ikea-manual` | 极简线稿 |
| `knolling` | 整齐排列的平铺构图 |
| `lego-brick` | 玩具积木结构 |
| `pop-laboratory` | 蓝图网格、坐标标记、实验室般的精确感 |
| `morandi-journal` | 手绘涂鸦、温暖的莫兰迪色调 |
| `retro-pop-grid` | 20 世纪 70 年代复古波普艺术、瑞士网格、粗轮廓线 |
| `hand-drawn-edu` | 马卡龙粉彩、手绘抖动线条、火柴人 |
| `retro-popup-pop` | 复古弹窗拼贴、怀旧 UI、粗轮廓线、扁平波普色彩 |

完整定义位于 `references/styles/<style>.md`。

## 推荐组合

| 内容类型 | 布局 + 风格 |
|--------------|----------------|
| 时间线/历史 | `linear-progression` + `craft-handmade` |
| 分步说明 | `linear-progression` + `ikea-manual` |
| A 与 B | `binary-comparison` + `corporate-memphis` |
| 层级关系 | `hierarchical-layers` + `craft-handmade` |
| 重叠关系 | `venn-diagram` + `craft-handmade` |
| 转化流程 | `funnel` + `corporate-memphis` |
| 循环过程 | `circular-flow` + `craft-handmade` |
| 技术内容 | `structural-breakdown` + `technical-schematic` |
| 指标数据 | `dashboard` + `corporate-memphis` |
| 教育内容 | `bento-grid` + `chalkboard` |
| 旅程 | `winding-roadmap` + `storybook-watercolor` |
| 分类 | `periodic-table` + `bold-graphic` |
| 产品指南 | `dense-modules` + `morandi-journal` |
| 技术指南 | `dense-modules` + `pop-laboratory` |
| 潮流指南 | `dense-modules` + `retro-pop-grid` |
| 复古波普指南 | `dense-modules` + `retro-popup-pop` |
| 教育图解 | `hub-spoke` + `hand-drawn-edu` |
| 流程教程 | `linear-progression` + `hand-drawn-edu` |

默认组合：`bento-grid` + `craft-handmade`（仅作为后备推荐——根据[确认策略](#confirmation-policy)，默认值绝不会绕过步骤 4）。

## 关键词快捷方式

当用户输入包含以下关键词时，将映射的布局作为步骤 3 的首要推荐，并将列出的风格提升到步骤 3 推荐列表顶部。匹配关键词后，跳过基于内容的布局推断。将所有 `Prompt Notes` 追加到步骤 5 的提示词中。

| 用户关键词 | 布局 | 推荐风格 | 默认宽高比 | 提示词备注 |
|--------------|--------|--------------------|----------------|--------------|
| 高密度信息大图 / high-density-info | `dense-modules` | `morandi-journal`、`pop-laboratory`、`retro-pop-grid`、`retro-popup-pop` | portrait | — |
| 信息图 / infographic | `bento-grid` | `craft-handmade` | landscape | 极简主义：干净的画布、充足的留白、不使用复杂的背景纹理。仅使用简单的卡通元素和图标。 |

## 输出结构

```
infographic/{topic-slug}/
├── source-{slug}.{ext}
├── analysis.md
├── structured-content.md
├── prompts/infographic.md
└── infographic.png
```

Slug：根据主题生成 2–4 个单词的 kebab-case。发生冲突时：追加 `-YYYYMMDD-HHMMSS`。

## 核心原则

- 忠实保留源数据——不得总结或改写（但在输出中包含之前，**必须移除所有凭据、API 密钥、令牌或机密信息**）
- 在组织内容结构之前定义学习目标
- 针对视觉传播组织结构（标题、标签、视觉元素）

## 工作流程

### 步骤 1：设置与分析

**1.1 加载偏好设置（EXTEND.md）**

按以下优先级检查 EXTEND.md——使用找到的第一个文件：

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-infographic/EXTEND.md` | 项目 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-infographic/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-infographic/EXTEND.md` | 用户主目录 |

| 结果 | 操作 |
|--------|--------|
| 已找到 | 读取、解析并显示一行摘要 |
| 未找到 | 使用 `AskUserQuestion` 询问用户（参见 `references/config/first-time-setup.md`） |

**EXTEND.md 支持**：首选布局/风格、默认宽高比、语言偏好、首选图像后端、自定义风格定义。

模式：`references/config/preferences-schema.md`

**1.2 分析内容 → `analysis.md`**

1. 保存源内容（文件路径或粘贴内容 → `source.md`）
   - **备份规则**：如果 `source.md` 已存在，将其重命名为 `source-backup-YYYYMMDD-HHMMSS.md`
2. 分析：主题、数据类型、复杂度、语气、受众
3. 检测源语言和用户语言
4. 从用户输入中提取设计指示
5. 保存分析结果
   - **备份规则**：如果 `analysis.md` 已存在，将其重命名为 `analysis-backup-YYYYMMDD-HHMMSS.md`

详细格式参见 `references/analysis-framework.md`。

### 步骤 2：生成结构化内容 → `structured-content.md`

将内容转换为信息图结构：
1. 标题和学习目标
2. 各章节包含：核心概念、内容（原文）、视觉元素、文本标签
3. 数据点（所有统计数据/引文均精确复制）
4. 用户的设计指示

**规则**：仅使用 Markdown。不得添加新信息。忠实保留数据。从输出中移除所有凭据或机密信息。

详细格式参见 `references/structured-content-template.md`。

### 步骤 3：推荐组合

**3.1 首先检查关键词快捷方式**：如果用户输入匹配**关键词快捷方式**表中的关键词，则将关联布局作为首要推荐，并优先推荐关联风格。跳过基于内容的布局推断。

**3.2 否则**，根据以下因素推荐 3–5 个布局×风格组合：
- 数据结构 → 匹配的布局
- 内容语气 → 匹配的风格
- 受众期望
- 用户的设计指示

### 步骤 4：确认选项

**强制关卡**：根据[确认策略](#confirmation-policy)，此步骤为必需步骤——用户在此确认之前，步骤 5–6 不得开始（除非用户在当前请求中通过 `--no-confirm` 或等效表述明确选择退出确认）。

按照本文件顶部的[用户输入工具](#user-input-tools)规则，请用户确认以下问题（如果运行时支持多个问题，则合并到一次调用中；否则按优先级逐个提问）。

| 优先级 | 问题 | 何时询问 | 选项 |
|----------|----------|------|---------|
| 1 | **组合** | 始终 | 3 个以上布局×风格组合，并附理由 |
| 2 | **宽高比** | 始终 | 命名预设（landscape/portrait/square）或自定义 W:H 比例（例如 3:4、4:3、2.35:1） |
| 3 | **语言** | 仅当源语言 ≠ 用户语言时 | 文本内容所用语言 |
| 4 | **图像后端** | 仅当 `## 图像生成工具` 规则的步骤 3 需要询问时（没有运行时原生工具且存在多个非原生后端，或 `preferred_image_backend: ask`） | 可用后端 |

### 步骤 5：生成提示词 → `prompts/infographic.md`

**备份规则**：如果 `prompts/infographic.md` 已存在，将其重命名为 `prompts/infographic-backup-YYYYMMDD-HHMMSS.md`

组合以下内容：
1. 来自 `references/layouts/<layout>.md` 的布局定义
2. 来自 `references/styles/<style>.md` 的风格定义
3. 来自 `references/base-prompt.md` 的基础模板
4. 步骤 2 中的结构化内容
5. 所有文本均使用已确认的语言

`{{ASPECT_RATIO}}` 的**宽高比解析规则**：
- 命名预设 → 比例字符串：landscape→`16:9`、portrait→`9:16`、square→`1:1`
- 自定义 W:H 比例 → 原样使用（例如 `3:4`、`4:3`、`2.35:1`）

### 步骤 6：生成图像

1. 按照本文件顶部的 `## 图像生成工具` 规则确定后端。
2. 在调用后端之前，确保完整的最终提示词已持久化到 `prompts/infographic.md`（已在步骤 5 中写入）——该文件是用于复现的记录。
3. **检查现有文件**：生成前检查 `infographic.png` 是否存在
   - 如果存在：将其重命名为 `infographic-backup-YYYYMMDD-HHMMSS.png`
4. 使用提示词文件和输出路径调用所选后端。
   - **`codex-imagegen` 调用方式**：当规则确定使用 `codex-imagegen` 时，请参阅 [references/codex-imagegen.md](references/codex-imagegen.md) 获取调用约定（首选的 `baoyu-image-gen --provider codex-cli` 路径、运行时包装器发现方式、参数说明、stdout 模式、批处理语义）。
5. 失败时自动重试一次

文本修正策略：

- 如果标签、标题、标注、数据值或任何其他渲染文本存在拼写错误、乱码、难以阅读或视觉效果不佳，不得使用代码修补位图。
- 对于文本修正重新生成，写入新的提示词文件和新的输出路径，以便保留有缺陷的候选版本用于比较。
- 后期处理仅限裁剪、调整尺寸、压缩或格式转换，不得改变文本或主要构图。

### 步骤 7：输出摘要

报告：主题、布局、风格、宽高比、语言、图像后端、输出路径、已创建文件。

## 参考资料

- `references/analysis-framework.md` - 分析方法
- `references/structured-content-template.md` - 内容格式
- `references/base-prompt.md` - 提示词模板
- `references/layouts/<layout>.md` - 21 种布局定义
- `references/styles/<style>.md` - 21 种风格定义

## 更改偏好设置

EXTEND.md 位于步骤 1.1 中首个匹配的路径。可通过三种方式更改：

- **直接编辑**——打开 EXTEND.md 并修改字段。完整模式：`references/config/preferences-schema.md`。
- **交互式重新配置**——删除 EXTEND.md（或提出“reconfigure baoyu-infographic preferences”/“重新配置”）。下次运行时会重新触发首次设置。
- **常用单行修改**：
  - `preferred_image_backend: auto`——默认值；优先使用运行时原生工具，仅安装一个后端时回退到该后端，仅在存在多个非原生后端时询问。
  - `preferred_image_backend: codex-imagegen`——固定使用 Codex 内置后端。
  - `preferred_image_backend: baoyu-image-gen`——固定使用 baoyu-image-gen 技能。
  - `preferred_image_backend: ask`——每次运行时确认后端。
  - `preferred_layout: dense-modules`、`preferred_style: morandi-journal`、`preferred_aspect: portrait`、`language: zh`——调整步骤 3 的推荐和步骤 4 的默认值（根据[确认策略](#confirmation-policy)，这些设置绝不会绕过步骤 4）。
