<!-- source-sha256: ce1c7bfe9b93e5afac1dbeac95a03f8abf8c102aeecc34a33d8f13dc10e64acd -->
---
name: baoyu-article-illustrator
description: 分析文章结构，识别需要视觉辅助的位置，并采用「类型 × 风格 × 配色」三维方法生成插图。当用户要求“为文章配图”“添加图片”“为文章生成图片”或“为文章配图”时使用。
version: 1.117.4
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator
---

# 文章插图生成器

分析文章、识别插图位置，并以一致的「类型 × 风格 × 配色」生成图片。

## 用户输入工具

当此技能需要向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具**，即当前智能体运行时提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果不存在此类工具，则发送带编号的纯文本消息，并要求用户针对每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持一次调用提出多个问题，则将所有适用问题合并到一次调用中；如果仅支持单个问题，则按优先级逐一提问。

下文中具体的 `AskUserQuestion` 引用仅作为示例——在其他运行时中请替换为本地等效工具。

## 图像生成工具

当此技能需要渲染图像时，请按以下顺序确定后端：

1. **当前请求覆盖设置**——如果用户在当前消息中指定了某个后端，则使用该后端。
2. **已保存的偏好设置**——如果 `EXTEND.md` 将 `preferred_image_backend` 设置为当前可用的后端，则使用该后端。
3. **自动选择**（当偏好设置为 `auto`、未设置或固定的后端不可用时）：
   - **Codex（`imagegen`）**——首先检查可用技能/工具清单。如果列出了名为 `imagegen` 的技能，则说明你正在 Codex 中运行，并且必须使用它：通过 `Skill` 工具调用，传入 `skill: "imagegen"`，并按照 Codex `imagegen` 自身的参数要求传入已保存提示词文件的内容（以及输出路径和宽高比）。Codex `imagegen` 是该运行时中的官方光栅图像后端；除非用户明确固定了其他 `preferred_image_backend`，否则其优先级高于任何非原生技能（例如 `baoyu-image-gen`）。
   - **通过 `codex exec` 使用 Codex（`codex-imagegen`）**——如果当前运行时未提供原生 `imagegen` 技能，但 `codex` CLI 位于 `PATH` 中且存在有效的 `codex login`，则通过 `baoyu-image-gen --provider codex-cli` 调用（优先）；如果 baoyu-image-gen 不可用，则直接调用随附的包装器。详细信息、参数及运行时发现流程位于 [references/codex-imagegen.md](references/codex-imagegen.md)——仅在选择此分支时加载该文件。
   - **Cursor（`GenerateImage`）**——如果运行时提供原生 `GenerateImage` 工具，则说明你正在 Cursor 中运行；与 Codex `imagegen` 一样，它的优先级高于任何非原生技能。存在两个必须注意的限制：(a) 它没有宽高比参数——必须在作为 `description` 传入的提示词文本中明确说明目标宽高比/尺寸；(b) 它不接受输出目录——生成结果会保存到工具管理的位置，因此生成后需要将文件复制/移动到技能预期的输出路径（例如 `outputs/.../NN-xxx.png`）。参考图像通过 `reference_image_paths` 传入。
   - **其他运行时原生工具**——如果运行时提供其他原生图像工具（例如 Hermes `image_generate`），则以相同方式使用。
   - 否则，如果只安装了一个非原生后端（例如 `baoyu-image-gen`），则使用它。
   - 否则（存在多个非原生后端且没有运行时原生工具），询问用户一次——与其他初始问题合并提问。
4. **如果没有任何可用后端**，告知用户并询问如何继续。

**⛔ 绝不能用 SVG、HTML、canvas 或其他基于代码的渲染方式替代光栅图像生成。** Codex `imagegen` 自身的描述指出，当“输出应为位图资源，而不是仓库原生代码或矢量图”时应使用它。如果无法通过步骤 3 确定光栅图像后端，则进入步骤 4 并询问用户——**不要**静默输出 SVG、编写内联 `<svg>` 标记，或生成 HTML/CSS 艺术作品作为替代方案。即使文章/章节看起来“像图表”，此规则仍然适用：调用此规则的上游技能已经确定它需要的是光栅图像。

**⛔ 绝不能通过在生成的位图上覆盖绘制来修复已渲染的文字。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化叠加方式，来遮盖、重写、擦除、描边或替换已生成插图中的标签、说明文字或任何其他文字。如果文字错误或不清晰，应使用修正后的提示词重新生成、以更少或不包含图中文字的方式重绘，或者询问用户保留哪个不完美的候选版本。

将 `preferred_image_backend: ask` 设置为此值，会强制每次运行时都执行步骤 3 的询问，而不考虑可用后端。用户可通过下方的 `## 更改偏好设置` 章节修改固定的后端。

**提示词文件要求（强制）**：在调用任何后端之前，必须将每张图像完整的最终提示词写入 `prompts/` 下的独立文件（命名方式：`NN-{type}-[slug].md`）。后端接收提示词文件（或其内容）；该文件是可复现性记录，使你能够在不重新生成提示词的情况下切换后端。

以上具体工具名称（`imagegen`、`GenerateImage`、`image_generate`、`baoyu-image-gen`）仅作为示例——请按照相同规则替换为本地等效工具。

## 批量生成策略

本次运行的所有提示词文件均保存并验证后，默认分批生成图像。

优先级顺序：

1. 如果所选后端提供原生批处理/多任务接口，则使用该接口。每个任务必须保留各自的提示词文件、输出路径、宽高比和直接参考图像。
2. 如果不存在原生批处理接口，但运行时可以并行调用工具，则每次最多分发 `generation_batch_size` 张图像。默认值：`4`。当前消息中的用户明确请求（例如 `--batch-size 4` 或“并行4张一起生成”）优先于 EXTEND.md。
3. 如果原生批处理和并行工具调用均不可用，则按顺序生成。

规则：

- 在某一批次的所有提示词文件均已写入磁盘之前，绝不能开始该批次。
- 失败项目重试一次，不要重新生成已成功的项目。
- 不要仅为并行渲染图像而使用子智能体。仅在需要独立迭代提示词或进行创意探索时使用子智能体。

## 确认策略

默认行为：**生成前确认**。

- 明确调用技能、文件路径、匹配到的信号/预设及 `EXTEND.md` 默认值都只能视为**推荐依据**。它们均不能授权跳过确认。
- 在用户完成步骤 3 之前，**不要**开始步骤 4 或后续步骤。
- 仅当当前请求明确要求跳过确认时才可跳过，例如：“直接生成”“不用确认”“跳过确认”“按默认出图”或含义相同的措辞。
- 如果用户明确要求跳过确认，则在生成前的下一条面向用户的进度更新中，说明所假定的类型/密度/风格/配色/语言/后端。

## 参考图像

用户可通过 `--ref <files...>` 提供参考图像，也可以在对话中提供文件路径或粘贴图像。参考图用于指导特定插图的风格、配色、构图或主体。

完整的检测、存储和处理规则位于 [references/workflow.md](references/workflow.md) 中（步骤 1.0 保存至 `references/NN-ref-{slug}.{ext}`；步骤 5.3 按每张插图处理 `direct | style | palette` 用途）。当所选后端支持批量输入时，应将每个提示词文件 `references:` 前置元数据中的 `direct` 用途条目传递到其批处理负载中，以便后端能够透传这些条目（例如 `baoyu-image-gen` 接受每个任务的 `ref`）。

## 三个维度

| 维度 | 控制内容 | 示例 |
|-----------|----------|----------|
| **类型** | 信息结构 | 信息图、场景、流程图、对比、框架、时间线 |
| **风格** | 渲染方式 | notion、温暖、极简、蓝图、水彩、优雅 |
| **配色** | 色彩方案（可选） | 马卡龙、暖色、霓虹——覆盖风格的默认颜色 |

可自由组合：`--type infographic --style vector-illustration --palette macaron`

也可使用预设：`--preset edu-visual` → 使用一个参数同时指定类型 + 风格 + 配色。参见[风格预设](references/style-presets.md)。

## 类型

| 类型 | 最适合 |
|------|----------|
| `infographic` | 数据、指标、技术内容 |
| `scene` | 叙事、情感内容 |
| `flowchart` | 流程、工作流 |
| `comparison` | 并列比较、选项 |
| `framework` | 模型、架构 |
| `timeline` | 历史、演变 |

## 风格

有关核心风格、完整图库以及「类型 × 风格」兼容性，请参见 [references/styles.md](references/styles.md)。

## 工作流

```
- [ ] 步骤 1：预检查（EXTEND.md、参考图、配置）
- [ ] 步骤 2：分析内容
- [ ] 步骤 3：确认设置（AskUserQuestion）
- [ ] 步骤 4：生成大纲
- [ ] 步骤 5：生成图像
- [ ] 步骤 6：完成处理
```

### 步骤 1：预检查

**1.5 加载偏好设置（EXTEND.md）⛔ 阻塞步骤**

按优先级顺序检查 EXTEND.md——使用找到的第一个文件：

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-article-illustrator/EXTEND.md` | 项目 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-article-illustrator/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-article-illustrator/EXTEND.md` | 用户主目录 |

| 结果 | 操作 |
|--------|--------|
| 已找到 | 读取、解析并显示摘要 |
| 未找到 | ⛔ 运行 [首次设置](references/config/first-time-setup.md) |

完整流程：[references/workflow.md](references/workflow.md#step-1-pre-check)

### 步骤 2：分析

| 分析项 | 输出 |
|----------|--------|
| 内容类型 | 技术 / 教程 / 方法论 / 叙事 |
| 目的 | 信息传达 / 可视化 / 想象 |
| 核心论点 | 2-5 个要点 |
| 位置 | 插图能够增加价值的位置 |

**关键要求**：遇到隐喻时，应将其背后的概念可视化，**不要**绘制字面图像。

完整流程：[references/workflow.md](references/workflow.md#step-2-setup--analyze)

### 步骤 3：确认设置 ⚠️

**强制关卡**：根据[确认策略](#确认策略)，此步骤为必需步骤——在用户于此处确认之前，不得开始步骤 4 及后续步骤（除非用户在当前请求中使用“直接生成”或含义相同的措辞明确选择跳过）。

**仅进行一次 AskUserQuestion，最多 4 个问题。Q1-Q2 为必答项。除非选择了预设，否则 Q3 为必答项。**

| 问题 | 选项 |
|---|---------|
| **Q1：预设或类型** | [推荐预设]、[备选预设]，或手动选择：infographic、scene、flowchart、comparison、framework、timeline、mixed |
| **Q2：密度** | minimal（1-2）、balanced（3-5）、per-section（推荐）、rich（6+） |
| **Q3：风格** | [推荐]、minimal-flat、sci-fi、hand-drawn、editorial、scene、poster、Other——**如果选择了预设则跳过** |
| Q4：配色 | Default（风格默认颜色）、macaron、warm、neon——**如果预设已包含配色或已设置 preferred_palette，则跳过** |
| Q5：语言 | 当文章语言与 EXTEND.md 设置不一致时询问 |

完整流程：[references/workflow.md](references/workflow.md#step-3-confirm-settings-)

### 步骤 4：生成大纲

保存包含前置元数据（type、density、style、palette、image_count）及以下条目的 `outline.md`：

```yaml
## 插图 1
**位置**：[章节/段落]
**目的**：[原因]
**视觉内容**：[内容]
**文件名**：01-infographic-concept-name.png
```

完整模板：[references/workflow.md](references/workflow.md#step-4-generate-outline)

### 步骤 5：生成图像

⛔ **阻塞要求：在生成任何图像之前，必须保存提示词文件。** 无论选择哪个后端，这都是强制要求——提示词文件是可复现性记录。

1. 根据 [references/prompt-construction.md](references/prompt-construction.md) 为每张插图创建提示词文件
2. 使用 YAML 前置元数据保存至 `prompts/NN-{type}-{slug}.md`
3. 提示词**必须**使用包含结构化章节（ZONES / LABELS / COLORS / STYLE / ASPECT）的类型专用模板
4. LABELS **必须**包含文章特有的数据：实际数字、术语、指标、引文
5. 在先保存提示词文件之前，**不要**通过 `--prompt` 传入临时的内联提示词
6. 根据顶部的 `## 图像生成工具` 规则选择后端：使用任何可用后端；如果存在多个后端，则询问用户一次。每个会话仅执行一次，并且必须在生成任何图像之前完成。
   - **调用 `codex-imagegen`**：当规则确定使用 `codex-imagegen` 时，请参阅 [references/codex-imagegen.md](references/codex-imagegen.md) 了解调用契约（优先使用 `baoyu-image-gen --provider codex-cli` 路径、运行时包装器发现方式、参数说明、stdout 架构及批处理语义）。
7. **执行策略**：按照 `## 批量生成策略` 分批生成：优先使用后端原生批处理，其次使用运行时并行工具调用，仅在无法使用前两者时顺序生成。除非 EXTEND.md 或当前请求覆盖该设置，否则默认批次大小为 4。
8. 根据提示词的前置元数据处理参考图（`direct`/`style`/`palette`）
9. 如果 EXTEND.md 已启用水印，则应用水印
10. 从已保存的提示词文件生成；失败时重试一次

完整流程：[references/workflow.md](references/workflow.md#step-5-generate-images)

### 步骤 6：完成处理

在段落后插入 `![描述]({relative-path}/NN-{type}-{slug}.png)`。路径根据输出目录设置，相对于文章文件计算。

```
文章插图生成完成！
文章：[path] | 类型：[type] | 密度：[level] | 风格：[style] | 配色：[palette or default]
图像：已生成 X/N
```

## 输出目录

输出目录由 EXTEND.md 中的 `default_output_dir` 决定（在首次设置期间配置）：

| `default_output_dir` | 输出路径 | Markdown 插入路径 |
|----------------------|-------------|----------------------|
| `imgs-subdir`（默认） | `{article-dir}/imgs/` | `imgs/NN-{type}-{slug}.png` |
| `same-dir` | `{article-dir}/` | `NN-{type}-{slug}.png` |
| `illustrations-subdir` | `{article-dir}/illustrations/` | `illustrations/NN-{type}-{slug}.png` |
| `independent` | `illustrations/{topic-slug}/` | `illustrations/{topic-slug}/NN-{type}-{slug}.png`（相对于 cwd） |

所有辅助文件（大纲、提示词）均保存在输出目录中：

```
{output-dir}/
├── outline.md
├── prompts/
│   └── NN-{type}-{slug}.md
└── NN-{type}-{slug}.png
```

当输入为**粘贴的内容**（没有文件路径）时，始终使用 `illustrations/{topic-slug}/`，并将 `source-{slug}.{ext}` 保存于同一位置。

**Slug**：2-4 个单词，使用 kebab-case。**冲突处理**：追加 `-YYYYMMDD-HHMMSS`。

## 修改

| 操作 | 步骤 |
|--------|-------|
| 编辑 | 更新提示词 → 重新生成 → 更新引用 |
| 添加 | 确定位置 → 编写提示词 → 生成 → 更新大纲 → 插入 |
| 删除 | 删除文件 → 移除引用 → 更新大纲 |

文字修正策略：

- 如果任何已渲染的文字（标签、说明文字等）存在拼写错误、乱码、难以辨认或视觉效果不佳，请勿使用代码修补位图。
- 对于文字修正型重新生成，应编写新的提示词文件并使用新的输出路径，以保留有缺陷的候选版本供比较。
- 后期处理仅限于裁剪、调整尺寸、压缩或格式转换，不得修改文字或主要构图。

## 参考资料

| 文件 | 内容 |
|------|---------|
| [references/workflow.md](references/workflow.md) | 详细流程 |
| [references/usage.md](references/usage.md) | 命令语法 |
| [references/styles.md](references/styles.md) | 风格图库 + 配色图库 |
| [references/style-presets.md](references/style-presets.md) | 预设快捷方式（类型 + 风格 + 配色） |
| [references/prompt-construction.md](references/prompt-construction.md) | 提示词模板 |
| [references/config/first-time-setup.md](references/config/first-time-setup.md) | 首次设置 |

## 更改偏好设置

EXTEND.md 位于步骤 1.5 所列路径中第一个匹配的位置。可通过以下三种方式更改：

- **直接编辑**——打开 EXTEND.md 并修改字段。完整架构：`references/config/preferences-schema.md`。
- **交互式重新配置**——删除 EXTEND.md（或提出“reconfigure baoyu-article-illustrator preferences”/“重新配置”）。下次运行时将重新触发首次设置。
- **常用单行修改**：
  - `preferred_image_backend: auto`——默认值；运行时原生工具优先，然后回退到唯一已安装的后端，仅当存在多个非原生后端时才询问。
  - `preferred_image_backend: codex-imagegen`——固定使用 Codex 的内置后端。
  - `preferred_image_backend: baoyu-image-gen`——固定使用 baoyu-image-gen 技能。
  - `preferred_image_backend: ask`——每次运行都确认后端。
  - `generation_batch_size: 4`——当运行时支持并行生成调用时，默认并发渲染的图像数量。
  - `preferred_type: infographic`、`preferred_style: notion`、`preferred_palette: macaron`、`language: zh`。
  - `default_output_dir: imgs-subdir`——相对于文章写入生成图像的位置。
