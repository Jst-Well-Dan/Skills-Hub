<!-- source-sha256: 98d5de8650a3401c1ee97b3f78ebacef72f3f570ef7fe7290b192ac7d24330bc -->
---
name: baoyu-comic
description: 支持多种艺术风格与基调的知识漫画创作工具。可创作原创教育漫画，提供详细的分镜布局，并支持批量生成图像。当用户要求创作“知识漫画”“教育漫画”“biography comic”“tutorial comic”或“Logicomix-style comic”时使用。
version: 1.117.4
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-comic
    requires:
      anyBins:
        - bun
        - npx
---

# 知识漫画创作工具

使用灵活的艺术风格 × 基调组合创作原创知识漫画。

## 用户输入工具

当此技能需要向用户提问时，请按以下优先顺序选择工具：

1. **优先使用内置用户输入工具**，即当前智能体运行时提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果不存在此类工具，则发送带编号的纯文本消息，并请用户针对每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持一次调用提出多个问题，请将所有适用问题合并到一次调用中；如果仅支持单个问题，则按优先顺序逐一提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行时中请替换为当地等效工具。

## 图像生成工具

当此技能需要渲染图像时，请按以下顺序确定后端：

1. **当前请求覆盖设置**——如果用户在当前消息中指定了特定后端，请使用该后端。
2. **已保存的偏好设置**——如果 `EXTEND.md` 将 `preferred_image_backend` 设置为当前可用的后端，请使用该后端。
3. **自动选择**（当偏好设置为 `auto`、未设置或固定的后端不可用时）：
   - **Codex（`imagegen`）**——首先检查可用技能/工具清单。如果列出了名为 `imagegen` 的技能，则表示你正在 Codex 内运行，并且必须使用它：通过 `Skill` 工具调用，传入 `skill: "imagegen"`，并提供已保存提示词文件的内容（以及按照 Codex `imagegen` 自身参数要求提供输出路径和宽高比）。Codex `imagegen` 是该运行时中的官方光栅图像后端；除非用户明确固定了其他 `preferred_image_backend`，否则其优先级高于任何非原生技能（例如 `baoyu-image-gen`）。
   - **通过 `codex exec` 使用 Codex（`codex-imagegen`）**——如果当前运行时未提供原生 `imagegen` 技能，但 `PATH` 中存在 `codex` CLI，且已有有效的 `codex login` 登录状态，请通过 `baoyu-image-gen --provider codex-cli` 进行调用（首选）；或者，如果 `baoyu-image-gen` 不可用，则直接调用随附的包装器。详细信息、参数和运行时发现流程位于 [references/codex-imagegen.md](references/codex-imagegen.md)——仅在选择此分支时加载该文件。
   - **Cursor（`GenerateImage`）**——如果运行时提供原生 `GenerateImage` 工具，则表示你正在 Cursor 内运行；与 Codex `imagegen` 相同，它的优先级高于任何非原生技能。需注意两个严格限制：(a) 它没有宽高比参数——必须在作为 `description` 传入的提示词文本中明确写出目标宽高比/尺寸；(b) 它不接受输出目录——文件会保存到工具管理的位置，因此生成后需将文件复制/移动到技能预期的输出路径（例如 `outputs/.../NN-xxx.png`）。参考图像应放入 `reference_image_paths`。
   - **其他运行时原生工具**——如果运行时提供其他原生图像工具（例如 Hermes `image_generate`），请以相同方式使用。
   - 否则，如果恰好安装了一个非原生后端（例如 `baoyu-image-gen`），请使用它。
   - 否则（存在多个非原生后端，且没有运行时原生工具），请向用户询问一次——并与其他初始问题一起批量提问。
4. **如果没有任何可用后端**，请告知用户并询问如何继续。

**⛔ 绝不使用 SVG、HTML、canvas 或其他基于代码的渲染方式来替代光栅图像生成。** Codex `imagegen` 自身的描述指出，应在“输出应为位图资源，而不是仓库原生代码或矢量图”时使用它。如果无法通过步骤 3 确定光栅图像后端，请转到步骤 4 并询问用户——**不要**擅自输出 SVG、编写内联 `<svg>` 标记或生成 HTML/CSS 图像作为替代。即使文章/章节看起来“类似图表”，此规则依然适用：调用此规则的上游技能已经确定其需要的是光栅图像。

**⛔ 绝不通过在已生成位图上覆盖绘制来修复渲染文本。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化叠加方式，去遮盖、重写、擦除、描边或替换已生成漫画页面中的对话、音效、分镜标签或任何其他文本。如果文本错误或不清晰，请使用修正后的提示词重新生成，以更少或不含图内文字的方式重绘页面，或者询问用户保留哪个不完美的候选版本。

设置 `preferred_image_backend: ask` 会强制每次运行都执行步骤 3 的询问，无论有哪些可用后端。用户可通过下方的 `## 更改偏好设置` 章节更改固定后端。

**提示词文件要求（强制）**：在调用任何后端之前，必须将每张图像完整的最终提示词写入 `prompts/` 下的独立文件（命名：`NN-{type}-[slug].md`）。后端接收提示词文件（或其内容）；该文件是可复现性记录，并允许在不重新生成提示词的情况下切换后端。

上文中的具体工具名称（`imagegen`、`GenerateImage`、`image_generate`、`baoyu-image-gen`）仅为示例——请按照相同规则替换为当地等效工具。

## 批量生成策略

在当前生成组的所有提示词文件均已保存并验证后，默认以批量方式生成图像。

优先顺序：

1. 如果所选后端提供原生批处理/多任务接口，请使用该接口。每个任务必须保留各自的提示词文件、输出路径、宽高比、会话 ID 和直接参考图像。
2. 如果没有原生批处理接口，但运行时可以并行发起工具调用，则每次最多分派 `generation_batch_size` 张图像。默认值：`4`。当前消息中的明确用户请求，例如 `--batch-size 4` 或“并行4张一起生成”，会覆盖 EXTEND.md。
3. 如果原生批处理和并行工具调用均不可用，则按顺序生成。

规则：

- 优先遵守工作流依赖关系：先生成 `characters/characters.png`，再生成将其作为参考图的页面。
- 在所有选定页面的提示词文件均已存在于磁盘之前，绝不启动第一批页面生成。
- 失败项重试一次，不要重新生成成功项。
- 不要仅为并行渲染图像而使用子智能体。仅将子智能体用于独立的提示词迭代或创意探索。

## 参考图像

用户可以提供参考图像，用于指导艺术风格、调色板、场景构图或主体表现。这与自动生成的角色设定表（步骤 7.1）**彼此独立**——两者可以共存：用户参考图指导整体视觉效果，角色设定表则固定重复出现角色的身份特征。

**接收方式**：通过 `--ref <files...>` 接收，或者在用户于对话中提供文件路径/粘贴图像时接收。
- 文件路径 → 复制到漫画输出目录旁的 `refs/NN-ref-{slug}.{ext}`
- 粘贴的图像没有路径 → 向用户询问路径（遵循上方“用户输入工具”规则），或采用文本回退方式，以语言描述提取风格特征
- 没有参考图 → 跳过本节

**使用模式**（针对每张参考图）：

| 用途 | 效果 |
|-------|--------|
| `direct` | 在每个页面（或选定页面）中将文件作为参考图像传递给后端 |
| `style` | 提取风格特征（线条处理、纹理、氛围）并附加到每个页面的提示词正文中 |
| `palette` | 提取十六进制颜色并附加到每个页面的提示词正文中 |

存在参考图时，**在每个页面提示词的 front matter 中记录**：

```yaml
references:
  - ref_id: 01
    filename: 01-ref-scene.png
    usage: direct
```

**生成时**：
- 验证每个被引用的文件都存在于磁盘
- 如果 `usage: direct` 且所选后端接受多张参考图像 → 通过后端的参考图参数同时传入角色设定表（步骤 7.2）和用户参考图；按照步骤 7.1 的指导先压缩图像，以避免载荷失败
- 如果后端只接受一张参考图 → 对包含重复出现角色的页面优先使用角色设定表；改为将用户参考图的特征嵌入提示词正文
- 对于 `style`/`palette` 用途 → 将提取的特征嵌入每个页面的提示词文本（无论后端能力如何，均适用）

## 选项

### 视觉维度

| 选项 | 值 | 描述 |
|--------|--------|-------------|
| `--art` | ligne-claire（默认）、manga、realistic、ink-brush、chalk、minimalist | 艺术风格/渲染技法 |
| `--tone` | neutral（默认）、warm、dramatic、romantic、energetic、vintage、action | 情绪/氛围 |
| `--layout` | standard（默认）、cinematic、dense、splash、mixed、webtoon、four-panel | 分镜排列 |
| `--aspect` | 3:4（默认，纵向）、4:3（横向）、16:9（宽屏） | 页面宽高比 |
| `--lang` | auto（默认）、zh、en、ja 等 | 输出语言 |
| `--ref <files...>` | 文件路径 | 应用于每个页面的参考图像，用于提供风格/调色板/场景指导。请参阅上方的[参考图像](#reference-images)。 |
| `--batch-size <n>` | 1-8 | 本次运行临时使用的页面生成批次大小。默认使用 EXTEND.md 中的 `generation_batch_size`，否则为 4。 |

### 部分工作流选项

| 选项 | 描述 |
|--------|-------------|
| `--storyboard-only` | 仅生成故事板，跳过提示词和图像 |
| `--prompts-only` | 生成故事板和提示词，跳过图像 |
| `--images-only` | 使用现有提示词目录生成图像 |
| `--regenerate N` | 仅重新生成指定页面（例如 `3` 或 `2,5,8`） |

详情：[references/partial-workflows.md](references/partial-workflows.md)

### 艺术风格、基调与预设目录

- **艺术风格**（6 种）：`ligne-claire`、`manga`、`realistic`、`ink-brush`、`chalk`、`minimalist`。完整定义位于 `references/art-styles/<style>.md`。
- **基调**（7 种）：`neutral`、`warm`、`dramatic`、`romantic`、`energetic`、`vintage`、`action`。完整定义位于 `references/tones/<tone>.md`。
- **预设**（5 种），包含超出普通艺术风格+基调组合的特殊规则：

  | 预设 | 等效组合 | 特有规则 |
  |--------|-----------|------|
  | `ohmsha` | manga + neutral | 视觉隐喻、避免只让人物对话、揭示小装置 |
  | `wuxia` | ink-brush + action | 气劲效果、战斗视觉、氛围感 |
  | `shoujo` | manga + romantic | 装饰元素、眼部细节、浪漫节拍 |
  | `concept-story` | manga + warm | 视觉符号系统、成长弧线、对话与动作平衡 |
  | `four-panel` | minimalist + neutral + four-panel 布局 | 起承转合结构、黑白 + 强调色、火柴人角色 |

  完整规则位于 `references/presets/<preset>.md`——选择预设后加载对应文件。

- **兼容性矩阵**和**内容信号 → 预设**表位于 [references/auto-selection.md](references/auto-selection.md)。在步骤 2 推荐组合之前阅读该文件。

## 脚本目录

**重要**：所有脚本均位于此技能的 `scripts/` 子目录中。

**智能体执行说明**：
1. 将此 SKILL.md 文件所在目录确定为 `{baseDir}`
2. 脚本路径 = `{baseDir}/scripts/<script-name>.ts`
3. 将本文档中的所有 `{baseDir}` 替换为实际路径
4. 确定 `${BUN_X}` 运行时：如果已安装 `bun` → 使用 `bun`；如果 `npx` 可用 → 使用 `npx -y bun`；否则建议安装 bun

**脚本参考**：

| 脚本 | 用途 |
|--------|---------|
| `scripts/merge-to-pdf.ts` | 将漫画页面合并为 PDF |

## 文件结构

输出目录：`comic/{topic-slug}/`
- Slug：根据主题生成 2-4 个单词的 kebab-case（例如 `alan-turing-bio`）
- 冲突：附加时间戳（例如 `turing-story-20260118-143052`）

**内容**：

| 文件 | 描述 |
|------|-------------|
| `source-{slug}.{ext}` | 源文件 |
| `analysis.md` | 内容分析 |
| `storyboard.md` | 包含分镜拆解的故事板 |
| `characters/characters.md` | 角色定义 |
| `characters/characters.png` | 角色参考设定表 |
| `prompts/NN-{cover\|page}-[slug].md` | 生成提示词 |
| `NN-{cover\|page}-[slug].png` | 已生成图像 |
| `{topic-slug}.pdf` | 最终合并的 PDF |

## 语言处理

**检测优先级**：
1. `--lang` 标志（显式）
2. EXTEND.md 的 `language` 设置
3. 用户的对话语言
4. 源内容语言

**规则**：所有交互均使用用户的输入语言或已保存的语言偏好：
- 故事板大纲和场景描述
- 图像生成提示词
- 用户选择选项和确认信息
- 进度更新、问题、错误和摘要

技术术语保留英文。

## 工作流

### 进度检查清单

```
漫画进度：
- [ ] 步骤 1：设置与分析
  - [ ] 1.1 偏好设置（EXTEND.md）⛔ 阻塞
    - [ ] 已找到 → 加载偏好设置 → 继续
    - [ ] 未找到 → 执行首次设置 → 必须先完成才能执行其他步骤
  - [ ] 1.2 分析，1.3 检查现有内容
- [ ] 步骤 2：确认——风格与选项 ⚠️ 必需
- [ ] 步骤 3：生成故事板和角色
- [ ] 步骤 4：审阅大纲（有条件）
- [ ] 步骤 5：生成提示词
- [ ] 步骤 6：审阅提示词（有条件）
- [ ] 步骤 7：生成图像
  - [ ] 7.1 生成角色设定表（如需要）→ characters/characters.png
  - [ ] 7.2 生成页面（如果角色设定表存在，则使用 --ref）
- [ ] 步骤 8：合并为 PDF
- [ ] 步骤 9：完成报告
```

### 流程

```
输入 → [偏好设置] ─┬─ 已找到 → 继续
                     │
                     └─ 未找到 → 首次设置 ⛔ 阻塞
                                    │
                                    └─ 完成设置 → 保存 EXTEND.md → 继续
                                                                            │
        ┌───────────────────────────────────────────────────────────────────┘
        ↓
分析 → [检查现有内容？] → [确认：风格 + 审阅] → 故事板 → [审阅？] → 提示词 → [审阅？] → 图像 → PDF → 完成
```

### 步骤摘要

| 步骤 | 操作 | 关键输出 |
|------|--------|------------|
| 1.1 | 加载 EXTEND.md 偏好设置；未找到时 ⛔ 阻塞 | 配置已加载 |
| 1.2 | 分析内容 | `analysis.md` |
| 1.3 | 检查现有目录 | 处理冲突 |
| 2 | 确认风格、重点、受众和审阅设置 | 用户偏好 |
| 3 | 生成故事板和角色 | `storyboard.md`、`characters/` |
| 4 | 审阅大纲（如已请求） | 用户批准 |
| 5 | 生成提示词 | `prompts/*.md` |
| 6 | 审阅提示词（如已请求） | 用户批准 |
| 7.1 | 生成角色设定表（如需要） | `characters/characters.png` |
| 7.2 | 生成页面（如有角色参考图，则使用它） | `*.png` 文件 |
| 8 | 合并为 PDF | `{slug}.pdf` |
| 9 | 完成报告 | 摘要 |

### 步骤 7：图像生成

按照顶部的 `## 图像生成工具` 规则，**每个会话仅选择一次后端**。如果后端是仓库技能（例如 `baoyu-image-gen`），请读取其 `SKILL.md`，并使用文档规定的接口，而不是其脚本。

**`codex-imagegen` 调用**：当规则选择 `codex-imagegen` 时，请参阅 [references/codex-imagegen.md](references/codex-imagegen.md) 了解调用约定（首选的 `baoyu-image-gen --provider codex-cli` 路径、运行时包装器发现方式、参数说明、stdout 架构、批处理语义——每次调用 n=1，因此页面批次必须为每个页面分别分派一次包装器调用）。

**7.1 角色设定表**——当漫画为多页且包含重复出现的角色时，生成角色设定表（保存到 `characters/characters.png`，宽高比为 `4:3`）。对于简单预设（例如 four-panel minimalist）或单页漫画，可跳过此步骤。在作为 `--ref` 使用前压缩为 JPEG（macOS 上使用 `sips -s format jpeg -s formatOptions 80 …`，其他平台使用 `pngquant --quality=65-80 …`），以避免载荷失败。调用后端之前，提示词文件 `characters/characters.md` 必须存在。

**7.2 页面**——调用后端之前，每个页面的提示词必须已存在于 `prompts/NN-{cover|page}-[slug].md`；该文件是可复现性记录。策略取决于角色设定表：

| 角色设定表 | 后端 `--ref` | 策略 |
|-----------------|-----------------|----------|
| 存在 | 支持 | 在每个页面中将设定表作为 `--ref` 传入 |
| 存在 | 不支持 | 在每个提示词文件开头添加角色描述 |
| 已跳过 | — | 在提示词中内联所有描述 |

**执行策略**：需要角色设定表时，先生成角色设定表。然后根据已保存的提示词文件构建选定页面任务列表，并按照 `## 批量生成策略` 分批分派页面：首先使用后端原生批处理，其次使用运行时并行工具调用，仅在回退时按顺序执行。`--regenerate N` 和 `--images-only` 对选定的现有提示词采用相同的批处理规则。

**备份规则**：重新生成前，将现有 `prompts/…md` 和 `…png` 文件重命名，添加 `-backup-YYYYMMDD-HHMMSS` 后缀。宽高比取自故事板（默认为 `3:4`；预设可能覆盖）。

**`--ref` 失败恢复**：压缩设定表 → 重试 → 仍然失败 → 移除 `--ref`，并将角色描述嵌入提示词文本。

完整的分步工作流（分析、故事板、审阅门控、重新生成变体）：[references/workflow.md](references/workflow.md)。

### EXTEND.md 路径 ⛔ 阻塞

如果未找到 EXTEND.md，则首次设置为**阻塞步骤**——必须在任何内容分析或风格/基调问题之前完成。

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-comic/EXTEND.md` | 项目 |
| 2 | `$HOME/.baoyu-skills/baoyu-comic/EXTEND.md` | 用户主目录 |

| 结果 | 操作 |
|--------|--------|
| 已找到 | 读取、解析并显示摘要 → 继续 |
| 未找到 | ⛔ 执行首次设置（[references/config/first-time-setup.md](references/config/first-time-setup.md)）→ 保存 EXTEND.md → 继续 |

**EXTEND.md 支持的设置**：水印、首选艺术风格/基调/布局、自定义风格定义、角色预设、语言偏好、首选图像后端、生成批次大小。架构：[references/config/preferences-schema.md](references/config/preferences-schema.md)。

## 参考资料

**核心模板**：
- [analysis-framework.md](references/analysis-framework.md) - 深度内容分析
- [character-template.md](references/character-template.md) - 角色定义格式
- [storyboard-template.md](references/storyboard-template.md) - 故事板结构
- [ohmsha-guide.md](references/ohmsha-guide.md) - Ohmsha 漫画细则

**风格定义**：
- `references/art-styles/` - 艺术风格（ligne-claire、manga、realistic、ink-brush、chalk、minimalist）
- `references/tones/` - 基调（neutral、warm、dramatic、romantic、energetic、vintage、action）
- `references/presets/` - 包含特殊规则的预设（ohmsha、wuxia、shoujo、concept-story、four-panel）
- `references/layouts/` - 布局（standard、cinematic、dense、splash、mixed、webtoon、four-panel）

**工作流**：
- [workflow.md](references/workflow.md) - 完整工作流详情
- [auto-selection.md](references/auto-selection.md) - 内容信号分析
- [partial-workflows.md](references/partial-workflows.md) - 部分工作流选项

**配置**：
- [config/preferences-schema.md](references/config/preferences-schema.md) - EXTEND.md 架构
- [config/first-time-setup.md](references/config/first-time-setup.md) - 首次设置
- [config/watermark-guide.md](references/config/watermark-guide.md) - 水印配置

## 页面修改

| 操作 | 步骤 |
|--------|-------|
| **编辑** | **首先更新提示词文件** → `--regenerate N` → 重新生成 PDF |
| **添加** | 在指定位置创建提示词 → 使用角色参考图生成 → 重新编号后续页面 → 更新故事板 → 重新生成 PDF |
| **删除** | 删除文件 → 重新编号后续页面 → 更新故事板 → 重新生成 PDF |

**重要**：更新页面时，务必先更新提示词文件（`prompts/NN-{cover|page}-[slug].md`），然后再重新生成。这样可以确保更改有记录且可复现。

文本修正策略：

- 如果对话、音效、分镜标签或任何其他渲染文本存在拼写错误、乱码、难以阅读或视觉效果不佳，请勿使用代码修补位图。
- 对于文本修正型重新生成，请写入新的提示词文件和新的输出路径，以保留有缺陷的候选版本供比较。
- 后期处理仅限于裁剪、调整尺寸、压缩或格式转换，不得改变文本或主要构图。

## 说明

- 图像生成：每页 10-30 秒
- 生成失败时自动重试一次
- 对敏感公众人物使用风格化替代方案
- 通过会话 ID 保持风格一致性
- **步骤 2 必须确认**——不得跳过
- **步骤 4/6 有条件执行**——仅在用户于步骤 2 中提出要求时执行
- **步骤 7.1 角色设定表**——建议用于多页漫画，对于简单预设可选
- **步骤 7.2 角色参考图**——如果设定表存在，则使用 `--ref`；失败时压缩/转换；最后回退为仅使用提示词
- 水印/语言只需在 EXTEND.md 中配置一次

## 更改偏好设置

EXTEND.md 位于 `.baoyu-skills/baoyu-comic/EXTEND.md`（项目）或 `~/.baoyu-skills/baoyu-comic/EXTEND.md`（用户）。有三种更改方式：

- **直接编辑**——打开 EXTEND.md 并修改字段。完整架构：`references/config/preferences-schema.md`。
- **交互式重新配置**——删除 EXTEND.md（或提出“reconfigure baoyu-comic preferences”/“重新配置”）。下次运行时会重新触发首次设置。
- **常见单行修改**：
  - `preferred_image_backend: auto`——默认值；运行时原生工具优先，否则回退到唯一已安装的后端；仅在存在多个非原生后端时询问。
  - `preferred_image_backend: codex-imagegen`——固定使用 Codex 内置后端。
  - `preferred_image_backend: baoyu-image-gen`——固定使用 baoyu-image-gen 技能。
  - `preferred_image_backend: ask`——每次运行都确认后端。
  - `generation_batch_size: 4`——当后端/运行时支持批处理或并行生成时，并发渲染的默认页面图像数量。
  - `watermark.enabled: true`、`preferred_art`、`preferred_tone`、`preferred_layout`、`language`——调整自动选择的默认设置和视觉选项。
