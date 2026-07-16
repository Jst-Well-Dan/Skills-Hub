<!-- source-sha256: 0e988f065a1886224a501614d059e90019360ccce9fc5f5417e8719e5777efd8 -->
---
name: baoyu-slide-deck
description: 根据内容生成专业的幻灯片组图片。创建包含风格说明的大纲，然后生成每张独立的幻灯片图片。当用户要求“创建幻灯片”“制作演示文稿”“生成演示稿”“幻灯片组”或“PPT”时使用。
version: 1.117.4
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-slide-deck
    requires:
      anyBins:
        - bun
        - npx
---

# 幻灯片组生成器

将内容转换为专业的幻灯片组图片。幻灯片组专为**阅读和分享**而设计（内容自解释、滚动浏览逻辑清晰、适合社交媒体），而非现场演示——这一假设决定了下文所有布局和信息密度的选择。

## 用户输入工具

当此 skill 需要向用户提问时，请按以下优先顺序选择工具：

1. **优先使用内置用户输入工具**：使用当前 agent 运行时提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果不存在此类工具，则发送一条带编号的纯文本消息，并请用户为每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持在一次调用中提出多个问题，则将所有适用问题合并为一次调用；如果仅支持单个问题，则按优先顺序逐一提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行时中，请替换为本地等效工具。

## 图片生成工具

当此 skill 需要渲染图片时，请按以下顺序确定后端：

1. **当前请求覆盖设置**——如果用户在当前消息中指定了某个后端，则使用该后端。
2. **已保存的偏好设置**——如果 `EXTEND.md` 将 `preferred_image_backend` 设置为当前可用的后端，则使用该后端。
3. **自动选择**（当偏好设置为 `auto`、未设置或固定的后端不可用时）：
   - **Codex（`imagegen`）**——首先检查可用 skills / 工具清单。如果列出了名为 `imagegen` 的 skill，说明你正在 Codex 中运行，并且必须使用它：通过 `Skill` 工具调用，设置 `skill: "imagegen"`，传入已保存的提示词文件内容（以及 Codex `imagegen` 自身参数所需的输出路径和宽高比）。Codex `imagegen` 是该运行时的官方栅格图像后端，优先级高于任何非原生 skill（例如 `baoyu-image-gen`），除非用户明确固定了其他 `preferred_image_backend`。
   - **通过 `codex exec` 使用 Codex（`codex-imagegen`）**——如果当前运行时没有提供原生 `imagegen` skill，但 `codex` CLI 位于 `PATH` 中且已有有效的 `codex login`，则通过 `baoyu-image-gen --provider codex-cli` 调用（首选）；如果 baoyu-image-gen 不可用，则直接调用随附的包装器。详细信息、参数和运行时发现流程位于 [references/codex-imagegen.md](references/codex-imagegen.md)——仅在选择此分支时加载该文件。
   - **Cursor（`GenerateImage`）**——如果运行时提供原生 `GenerateImage` 工具，说明你正在 Cursor 中运行；与 Codex `imagegen` 一样，它的优先级高于任何非原生 skill。需要注意两个严格限制：(a) 它没有宽高比参数——必须在作为 `description` 传入的提示词文本中明确说明目标宽高比/尺寸；(b) 它不接受输出目录——图片会保存到工具管理的位置，因此生成后需要将文件复制/移动到此 skill 预期的输出路径（例如 `outputs/.../NN-xxx.png`）。参考图片放入 `reference_image_paths`。
   - **其他运行时原生工具**——如果运行时提供其他原生图片工具（例如 Hermes `image_generate`），请按相同方式使用。
   - 否则，如果只安装了一个非原生后端（例如 `baoyu-image-gen`），则使用该后端。
   - 否则（存在多个非原生后端且没有运行时原生工具），向用户询问一次——与其他初始问题合并提问。
4. **如果没有任何可用后端**，请告知用户并询问如何继续。

**⛔ 绝不可使用 SVG、HTML、canvas 或其他基于代码的渲染方式替代栅格图片生成。** Codex `imagegen` 自身的说明指出，当“输出应为位图资源，而不是仓库原生代码或矢量图”时应使用它。如果无法通过第 3 步确定栅格后端，则转到第 4 步并询问用户——**不要**静默输出 SVG、编写内联 `<svg>` 标记，或使用 HTML/CSS 图形作为替代方案。即使文章/章节看起来“类似图表”，此规则也同样适用：调用此规则的上游 skill 已经决定其需要的是栅格图片。

**⛔ 绝不可通过在已生成位图上覆盖绘制来修复渲染文本。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化叠加方式来遮盖、改写、擦除、描边或替换已生成幻灯片图片中的标题、项目符号或任何其他文本。如果文本错误或不清晰，请使用修正后的提示词重新生成、简化幻灯片图片中的文本，或询问用户要保留哪个不完美的候选版本。

设置 `preferred_image_backend: ask` 会强制每次运行时都执行第 3 步中的询问，无论有哪些可用后端。用户可以通过下文的 `## 更改偏好设置` 章节修改固定后端。

**提示词文件要求（严格）**：在调用任何后端之前，必须将每张图片完整的最终提示词写入 `prompts/` 下的独立文件（命名格式：`NN-slide-[slug].md`）。该文件是可复现性记录，也使你能够在不重新生成提示词的情况下切换后端。

上述具体工具名称（`imagegen`、`GenerateImage`、`image_generate`、`baoyu-image-gen`）仅为示例——请按照相同规则替换为本地等效工具。

## 批量生成策略

当前生成组的所有提示词文件均已保存并验证后，默认分批生成幻灯片图片。

优先顺序：

1. 如果所选后端提供原生批处理/多任务接口，请使用该接口。每个任务必须保留各自的提示词文件、输出路径、宽高比、会话 ID 和直接参考图片。
2. 如果不存在原生批处理接口，但运行时可以并行调用工具，则每次最多并发生成 `generation_batch_size` 张幻灯片图片。默认值：`4`。当前消息中用户明确提出的请求（例如 `--batch-size 4` 或“并行4张一起生成”）会覆盖 EXTEND.md。
3. 如果既不支持原生批处理，也不支持并行工具调用，则按顺序生成。

规则：

- 在所有选定幻灯片的提示词文件都已存在于磁盘上之前，绝不可启动第一批生成。
- 失败的项目重试一次，不要重新生成已经成功的项目。
- 不要仅仅为了并行渲染图片而使用 subagents。仅将 subagents 用于独立的提示词迭代或创意探索。
- 仅在所有选定幻灯片图片都生成完成后合并 PPTX/PDF。

## 确认策略

默认行为：**生成前确认**。

- 明确调用 skill、文件路径、匹配的信号/预设以及 `EXTEND.md` 默认值均只能视为**推荐依据**。它们都不构成跳过确认的授权。
- 在用户完成第 2 步之前，**不要**开始第 3 步或后续步骤。
- 只有当前请求明确要求跳过确认时才能跳过，例如：“直接生成”“不用确认”“跳过确认”“按默认出幻灯片”或同等表述。
- 如果用户明确跳过确认，则在生成前的下一条面向用户的进度消息中说明假定的风格/受众/幻灯片数量/语言/后端。

## 语言

在提问、进度报告、错误消息和完成摘要中使用用户的语言。技术标记（风格名称、文件路径、代码）保持英文。

## 脚本目录

`{baseDir}` = 此 SKILL.md 所在的目录。解析 `${BUN_X}`：优先使用 `bun`；否则使用 `npx -y bun`；否则建议运行 `brew install oven-sh/bun/bun`。

| 脚本 | 用途 |
|--------|---------|
| `scripts/merge-to-pptx.ts` | 将幻灯片合并为 PowerPoint |
| `scripts/merge-to-pdf.ts` | 将幻灯片合并为 PDF |

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--style <name>` | 预设（参见下文“预设”）、`custom` 或自定义风格名称 |
| `--audience <type>` | beginners / intermediate / experts / executives / general |
| `--lang <code>` | 输出语言（en、zh、ja……） |
| `--slides <N>` | 目标幻灯片数量（建议 8-25，最多 30） |
| `--ref <files...>` | 应用于每张幻灯片的参考图片（风格/调色板/构图/主体） |
| `--batch-size <n>` | 本次运行临时使用的幻灯片图片生成批次大小。默认值：EXTEND.md 中的 `generation_batch_size`，否则为 4。限制在 1-8。 |
| `--outline-only` | 生成大纲后停止 |
| `--prompts-only` | 生成提示词后停止（跳过图片生成） |
| `--images-only` | 跳到第 7 步；要求已有 `prompts/` |
| `--regenerate <N>` | 重新生成指定幻灯片：`3` 或 `2,5,8` |

## 风格系统

17 种预设，覆盖技术/教育/生活方式/编辑类使用场景。每种预设都是四个维度（纹理/氛围/字体排印/密度）的组合。如果用户在第 1 轮中选择“自定义维度”，第 2 轮确认将针对每个维度各提出一个问题——选项和逐字文本位于 `references/confirmation.md`。

### 预设（17 种）

| 预设 | 维度 | 最适合 |
|--------|------------|----------|
| `blueprint`（默认） | grid + cool + technical + balanced | 架构、系统设计 |
| `chalkboard` | organic + warm + handwritten + balanced | 教育、教程 |
| `corporate` | clean + professional + geometric + balanced | 投资者演示稿、提案 |
| `minimal` | clean + neutral + geometric + minimal | 高管简报 |
| `sketch-notes` | organic + warm + handwritten + balanced | 教育、教程 |
| `hand-drawn-edu` | organic + macaron + handwritten + balanced | 教育图示、流程讲解 |
| `watercolor` | organic + warm + humanist + minimal | 生活方式、健康 |
| `dark-atmospheric` | clean + dark + editorial + balanced | 娱乐、游戏 |
| `notion` | clean + neutral + geometric + dense | 产品演示、SaaS |
| `bold-editorial` | clean + vibrant + editorial + balanced | 产品发布、主题演讲 |
| `editorial-infographic` | clean + cool + editorial + dense | 技术讲解、研究 |
| `fantasy-animation` | organic + vibrant + handwritten + minimal | 教育故事 |
| `intuition-machine` | clean + cool + technical + dense | 技术文档、学术内容 |
| `pixel-art` | pixel + vibrant + technical + balanced | 游戏、开发者演讲 |
| `scientific` | clean + cool + technical + dense | 生物学、化学、医学 |
| `vector-illustration` | clean + vibrant + humanist + balanced | 创意、儿童内容 |
| `vintage` | paper + warm + editorial + balanced | 历史、文化传承 |

各预设的详细规范：`references/styles/<preset>.md`。预设 → 维度映射：`references/dimensions/presets.md`。

### 维度（选择“自定义维度”时）

| 维度 | 选项 | 用途 |
|-----------|---------|---------|
| **纹理** | clean, grid, organic, pixel, paper | 背景处理 |
| **氛围** | professional, warm, cool, vibrant, dark, neutral, macaron | 色温 |
| **字体排印** | geometric, humanist, handwritten, editorial, technical | 标题/正文样式 |
| **密度** | minimal, balanced, dense | 每张幻灯片的信息量 |

各维度的完整规范：`references/dimensions/*.md`。

### 自动选择

将内容信号与预设匹配。选择源内容中出现其信号关键词的第一行；如果没有匹配项，则回退到 `blueprint`。

| 源内容中的信号 | 预设 |
|-------------------|--------|
| tutorial, learn, education, guide, beginner | `sketch-notes` |
| hand-drawn, infographic, diagram, process, onboarding | `hand-drawn-edu` |
| classroom, teaching, school, chalkboard | `chalkboard` |
| architecture, system, data, analysis, technical | `blueprint` |
| creative, children, kids, cute | `vector-illustration` |
| briefing, academic, research, bilingual | `intuition-machine` |
| executive, minimal, clean, simple | `minimal` |
| saas, product, dashboard, metrics | `notion` |
| investor, quarterly, business, corporate | `corporate` |
| launch, marketing, keynote, magazine | `bold-editorial` |
| entertainment, music, gaming, atmospheric | `dark-atmospheric` |
| explainer, journalism, science communication | `editorial-infographic` |
| story, fantasy, animation, magical | `fantasy-animation` |
| gaming, retro, pixel, developer | `pixel-art` |
| biology, chemistry, medical, scientific | `scientific` |
| history, heritage, vintage, expedition | `vintage` |
| lifestyle, wellness, travel, artistic | `watercolor` |

### 幻灯片数量启发规则

| 源内容长度 | 建议幻灯片数量 |
|---------------|--------------------|
| < 1000 词 | 5-10 |
| 1000-3000 词 | 10-18 |
| 3000-5000 词 | 15-25 |
| > 5000 词 | 20-30（考虑拆分） |

## 参考图片

用户可以提供参考图片，用于指导风格、调色板、布局或主体。

**接收方式**：通过 `--ref <files...>` 接收，或在用户提供文件路径/将图片粘贴到对话中时接收。
- 文件路径 → 复制到 `{slide-deck-dir}/refs/NN-ref-{slug}.{ext}`
- 没有路径的粘贴图片 → 询问路径，或将口头描述的风格特征作为文本回退方案

**使用模式**（针对每张参考图片）：

| 用法 | 效果 |
|-------|--------|
| `direct` | 将文件作为每张幻灯片的参考图片传递给后端 |
| `style` | 提取风格特征（线条处理、纹理、氛围）并附加到每张幻灯片的提示词正文中 |
| `palette` | 提取十六进制颜色，并附加到每张幻灯片的提示词正文中 |

在每张幻灯片的提示词 front matter 中记录参考图片：

```yaml
references:
  - ref_id: 01
    filename: 01-ref-brand.png
    usage: direct
```

生成时验证文件是否存在。如果 `usage: direct` 且后端接受参考图片（例如 `baoyu-image-gen --ref`），则将该文件传给每张幻灯片。否则，将提取的 `style`/`palette` 特征嵌入提示词文本中。

## 文件布局

```
slide-deck/{topic-slug}/
├── source-{slug}.{ext}
├── outline.md
├── prompts/NN-slide-{slug}.md
├── NN-slide-{slug}.png
├── {topic-slug}.pptx
└── {topic-slug}.pdf
```

**Slug**：2-4 个单词，使用 kebab-case，从主题中提取。“Introduction to Machine Learning”→ `intro-machine-learning`。

**备份规则**（适用于所有步骤）：如果即将写入的文件已经存在，请先将其重命名为 `<name>-backup-YYYYMMDD-HHMMSS.<ext>`，再写入新文件。这可以保护用户的编辑内容并支持回滚。

## 工作流程

复制此检查清单，并在完成各项后勾选：

```
- [ ] 第 1 步：设置与分析
- [ ] 第 2 步：确认 ⚠️ 必需（第 1 轮；仅在选择“自定义维度”时进行第 2 轮）
- [ ] 第 3 步：生成大纲
- [ ] 第 4 步：审查大纲（有条件）
- [ ] 第 5 步：生成提示词
- [ ] 第 6 步：审查提示词（有条件）
- [ ] 第 7 步：生成图片
- [ ] 第 8 步：合并为 PPTX/PDF
- [ ] 第 9 步：输出摘要
```

### 第 1 步：设置与分析

**1.1 加载 EXTEND.md**——按顺序检查以下路径；使用第一个匹配项：

| 路径 | 作用域 |
|------|-------|
| `.baoyu-skills/baoyu-slide-deck/EXTEND.md` | 项目 |
| `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-slide-deck/EXTEND.md` | XDG |
| `$HOME/.baoyu-skills/baoyu-slide-deck/EXTEND.md` | 用户主目录 |

如果找到，请读取、解析并输出摘要（风格/受众/语言/审查/生成批次大小）。如果未找到，则使用默认值继续——首次设置不会阻塞此 skill。Schema：`references/config/preferences-schema.md`。

**1.2 分析内容**——遵循 `references/analysis-framework.md`：对内容进行分类、检测语言、记录用于选择风格的信号、根据长度估算幻灯片数量（参见上文风格系统中的**幻灯片数量启发规则**）、生成主题 slug。将源内容保存为 `source.md`（如果已存在，请遵守备份规则）。

**1.3 检查现有输出** ⚠️ 第 2 步之前必须执行。如果 `slide-deck/{topic-slug}/` 已存在，请询问如何继续——四个选项（重新生成大纲/重新生成图片/备份并重新生成/退出），逐字文本位于 `references/confirmation.md`。

将分析结果保存到 `analysis.md`：主题、受众、信号、推荐风格和幻灯片数量、语言检测结果。

### 第 2 步：确认 ⚠️ 必需

**严格关卡**：根据[确认策略](#确认策略)，此步骤为必需步骤——在用户于此处确认之前，不得开始第 3 步及后续步骤（除非用户在当前请求中明确使用“直接生成”或同等表述选择跳过）。

**第 1 轮（始终执行）**——通过一次 `AskUserQuestion` 调用批量提出五个问题：风格、受众、幻灯片数量、是否审查大纲？、是否审查提示词？逐字选项位于 `references/confirmation.md`。

提问前显示的摘要：
- 内容类型 + 主题
- 检测到的语言
- 推荐风格（根据信号）
- 建议幻灯片数量（根据长度）

**第 2 轮（仅当第 1 轮选择“自定义维度”时）**——批量提出四个问题：纹理、氛围、字体排印、密度。逐字选项位于 `references/confirmation.md`。这四个答案将替代预设。

**确认后**：使用最终选择更新 `analysis.md`，并存储由 Q4/Q5 决定的 `skip_outline_review` / `skip_prompt_review` 标志。

### 第 3 步：生成大纲

解析风格：预设 → `references/styles/{preset}.md`；自定义维度 → 组合 `references/dimensions/` 中的文件。根据解析后的风格构建 `STYLE_INSTRUCTIONS`，应用已确认的受众、语言和幻灯片数量，遵循 `references/outline-template.md`，并保存为 `outline.md`。

如果指定 `--outline-only`，则在此停止。如果设置了 `skip_outline_review`，则跳过第 4 步。

### 第 4 步：审查大纲（有条件）

显示逐张幻灯片表格（`# | 标题 | 类型 | 布局`），以及总数和解析后的风格。询问：继续/先编辑大纲/重新生成——逐字文本位于 `references/confirmation.md`。

如果选择“先编辑大纲”，请用户编辑 `outline.md`，并让其准备好后再次确认。如果选择“重新生成大纲”，返回第 3 步。

### 第 5 步：生成提示词

对于大纲中的每张幻灯片：
1. 读取 `references/base-prompt.md`
2. 从大纲中提取 `STYLE_INSTRUCTIONS`（不要重新读取风格文件）
3. 添加该幻灯片的内容
4. 如果指定了 `Layout:`，则加入 `references/layouts.md` 中的指导
5. 保存到 `prompts/NN-slide-{slug}.md`（适用备份规则）

如果指定 `--prompts-only`，则在此停止。如果设置了 `skip_prompt_review`，则跳过第 6 步。

### 第 6 步：审查提示词（有条件）

显示提示词索引（`# | 文件名 | 幻灯片标题`），并询问：继续/先编辑提示词/重新生成——逐字文本位于 `references/confirmation.md`。分支逻辑与第 4 步相同。

### 第 7 步：生成图片

1. 按照顶部的图片生成工具规则确定图片后端——如果安装了多个后端，则询问一次。
   - **`codex-imagegen` 调用**：当规则确定使用 `codex-imagegen` 时，请参阅 [references/codex-imagegen.md](references/codex-imagegen.md) 了解调用约定（首选的 `baoyu-image-gen --provider codex-cli` 路径、运行时包装器发现、参数说明、stdout schema、批处理语义——每次调用 n=1，因此幻灯片批次必须为每张幻灯片分别发起一次包装器调用）。
2. 确认每个 `prompts/NN-slide-{slug}.md` 都存在（严格要求；无论使用何种后端，提示词文件都是可复现性记录）。
3. 会话 ID：`slides-{topic-slug}-{timestamp}`——仅在后端支持会话时传入。
4. 为选定幻灯片构建任务列表，其中每项包含该幻灯片的提示词文件、输出 PNG 路径、宽高比、会话 ID 和已验证的直接参考图片。
5. 根据 `## 批量生成策略` 分批调度幻灯片图片：优先使用后端原生批处理，其次使用运行时并行工具调用，只有在前两者不可用时才按顺序生成。调度前对 PNG 文件应用备份规则。使用 `已生成 X/N` 报告进度。仅对失败项目重试一次，然后再报告错误。

`--regenerate N` 会针对指定幻灯片直接跳到此步骤。`--images-only` 使用现有提示词从此步骤开始。

### 第 8 步：合并

```bash
${BUN_X} {baseDir}/scripts/merge-to-pptx.ts <slide-deck-dir>
${BUN_X} {baseDir}/scripts/merge-to-pdf.ts <slide-deck-dir>
```

### 第 9 步：摘要

```
幻灯片组已完成！
主题：[topic]
风格：[preset or "custom: texture+mood+typography+density"]
位置：[directory]
幻灯片：N

- 01-slide-cover.png
- ...
- NN-slide-back-cover.png

大纲：outline.md
PPTX：{topic-slug}.pptx
PDF：{topic-slug}.pdf
```

## 修改幻灯片

| 操作 | 方法 |
|--------|-----|
| 编辑 | **首先**更新 `prompts/NN-slide-{slug}.md`，然后执行 `--regenerate N` |
| 添加 | 在目标位置创建新提示词、生成图片、为后续 `NN` 重新编号（slug 保持不变）、更新 `outline.md`、重新合并 |
| 删除 | 删除 PNG + 提示词、为后续项目重新编号、更新 `outline.md`、重新合并 |

重新生成图片前，始终先更新提示词文件——这样可以使 prompts 目录保持为事实来源，并确保更改可复现。重新编号时仅更改 `NN`；slug 保持稳定，以确保引用仍然有效。

文本修正策略：

- 如果幻灯片的标题、项目符号或任何其他渲染文本存在拼写错误、乱码、难以阅读或视觉效果不佳，请勿使用代码修补位图。
- 对于文本修正后的重新生成，请写入新的提示词文件和新的输出路径，以保留有缺陷的候选版本供比较。
- 后处理仅限于裁剪、调整大小、压缩或格式转换，不得改变文本或主要构图。

完整详情请参阅 `references/modification-guide.md`。

## 参考文件

| 文件 | 内容 |
|------|---------|
| `references/confirmation.md` | 每次确认使用的 AskUserQuestion 选项逐字文本 |
| `references/analysis-framework.md` | 内容分析框架 |
| `references/outline-template.md` | 大纲结构 |
| `references/base-prompt.md` | 图片生成的基础提示词正文 |
| `references/layouts.md` | 布局选项 |
| `references/design-guidelines.md` | 受众、字体排印、颜色选择 |
| `references/content-rules.md` | 内容指南 |
| `references/modification-guide.md` | 编辑/添加/删除工作流程 |
| `references/styles/<preset>.md` | 各预设的规范 |
| `references/dimensions/*.md` | 各维度的规范 |
| `references/config/preferences-schema.md` | EXTEND.md schema |

## 注意事项

- 每张幻灯片的图片生成大约需要 10-30 秒；请在生成期间报告进度。
- 对于敏感公众人物，优先使用风格化替代方案，以避免肖像相似性问题。
- 当后端支持会话 ID 时，使用它保持视觉一致性。

## 更改偏好设置

EXTEND.md 位于第 1.1 步列出的第一个匹配路径中。有两种更改方式：

- **直接编辑**——打开 EXTEND.md 并修改字段。完整 schema：`references/config/preferences-schema.md`。
- **常见单行编辑**：
  - `preferred_image_backend: auto`——默认值；优先使用运行时原生工具，否则回退到唯一已安装的后端；仅在存在多个非原生后端时询问。
  - `preferred_image_backend: codex-imagegen`——固定使用 Codex 内置后端。
  - `preferred_image_backend: baoyu-image-gen`——固定使用 baoyu-image-gen skill。
  - `preferred_image_backend: ask`——每次运行都确认后端。
  - `generation_batch_size: 4`——当后端/运行时支持批处理或并行生成时，同时渲染的默认幻灯片图片数量。
  - `preferred_style: blueprint`、`preferred_audience: experts`、`language: zh`。
