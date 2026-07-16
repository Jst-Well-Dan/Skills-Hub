<!-- source-sha256: 772f7170a61f1246d7505c97539579bb4d055f21653462e8cfaaddc65a3a5b31 -->
---
name: baoyu-translate
description: >-
  当用户请求“translate”“翻译”“精翻”“translate article”“translate to Chinese”“translate to English”
  “改成中文”“改成英文”“convert to Chinese”“localize”“本地化”“refined translation”“精细翻译”
  “proofread translation”“快速翻译”“快翻”“这篇文章翻译一下”，或提供带有翻译意图的 URL/文件时，
  应使用此技能。支持三种模式（quick/normal/refined）以及自定义术语表。
version: 1.117.3
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-translate
    requires:
      anyBins:
        - bun
        - npx
---

# 翻译器

三模式翻译技能：**quick** 用于直接翻译，**normal** 用于基于分析的翻译，**refined** 用于包含审校和润色的完整出版级工作流。

## 用户输入工具

当此技能需要向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具**：使用当前智能体运行时提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何同等工具。
2. **回退方案**：如果不存在此类工具，则发送带编号的纯文本消息，请用户回复每个问题所选的编号/答案。
3. **批量提问**：如果工具支持一次调用提出多个问题，请在一次调用中合并所有适用问题；如果仅支持单个问题，则按优先级逐一提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行时中，请替换为本地同等工具。

## 脚本目录

脚本位于 `scripts/` 子目录中。`{baseDir}` = 此 SKILL.md 所在的目录路径。解析 `${BUN_X}` 运行时：如果已安装 `bun` → `bun`；如果 `npx` 可用 → `npx -y bun`；否则建议安装 bun。将 `{baseDir}` 和 `${BUN_X}` 替换为实际值。

| 脚本 | 用途 |
|--------|---------|
| `scripts/main.ts` | CLI 入口点。默认操作是将 Markdown 拆分为多个分块；也支持显式的 `chunk` 子命令 |
| `scripts/chunk.ts` | `main.ts` 使用的 Markdown 分块实现，并保持对直接调用的兼容性 |

## 偏好设置（EXTEND.md）

按以下优先级检查 EXTEND.md——找到的第一个生效：

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-translate/EXTEND.md` | 项目 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-translate/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-translate/EXTEND.md` | 用户主目录 |

| 结果 | 操作 |
|--------|--------|
| 已找到 | 读取、解析并应用。会话中首次使用时，简短提醒：“正在使用 [path] 中的偏好设置。你可以编辑 EXTEND.md 来自定义术语表、受众等。” |
| 未找到 | **必须**运行首次设置（见下文）——不得静默使用默认值 |

**EXTEND.md 支持**：默认目标语言、默认模式、目标受众、自定义术语表（内联或文件路径）、翻译风格、分块设置。

模式定义：[references/config/extend-schema.md](references/config/extend-schema.md)。

### 首次设置（阻塞）

**关键要求**：未找到 EXTEND.md 时，必须在进行任何翻译之前运行首次设置。这是一项**阻塞**操作。

完整参考：[references/config/first-time-setup.md](references/config/first-time-setup.md)

使用 `AskUserQuestion` 在一次调用中提出所有问题（目标语言、模式、受众、风格、保存位置）。用户回答后，在所选位置创建 EXTEND.md，确认“偏好设置已保存至 [path]”，然后继续。

## 默认值

所有可配置值集中列在此处。EXTEND.md 会覆盖这些值；CLI 标志会覆盖 EXTEND.md。

| 设置 | 默认值 | EXTEND.md 键 | CLI 标志 | 说明 |
|---------|---------|---------------|----------|-------------|
| 目标语言 | `zh-CN` | `target_language` | `--to` | 翻译的目标语言 |
| 模式 | `normal` | `default_mode` | `--mode` | 翻译模式 |
| 受众 | `general` | `audience` | `--audience` | 目标读者画像 |
| 风格 | `storytelling` | `style` | `--style` | 翻译风格偏好 |
| 分块阈值 | `4000` | `chunk_threshold` | — | 触发分块翻译的词数 |
| 分块最大词数 | `5000` | `chunk_max_words` | — | 每个分块的最大词数 |

## 模式

| 模式 | 标志 | 步骤 | 适用场景 |
|------|------|-------|-------------|
| 快速 | `--mode quick` | 翻译 | 短文本、非正式内容、快速任务 |
| 标准 | `--mode normal`（默认） | 分析 → 翻译 | 文章、博客文章、一般内容 |
| 精翻 | `--mode refined` | 分析 → 翻译 → 审校 → 润色 | 出版级内容、重要文档 |

**默认模式**：标准模式（可通过 EXTEND.md 的 `default_mode` 设置覆盖）。

**风格预设**——控制译文的语言风格和语气（独立于受众设置）：

| 值 | 说明 | 效果 |
|-------|-------------|--------|
| `storytelling` | 引人入胜的叙事节奏（默认） | 吸引读者、衔接流畅、措辞生动 |
| `formal` | 专业、结构严谨 | 语气中性、组织清晰、不使用口语 |
| `technical` | 精确、文档式 | 简洁、术语密集、尽量减少修饰 |
| `literal` | 贴近原文结构 | 尽量减少重构，保留原文句式 |
| `academic` | 学术、严谨 | 使用正式语体，可采用复杂从句，注意引文规范 |
| `business` | 简洁、注重结果 | 强调行动、便于管理层阅读、采用要点式思维 |
| `humorous` | 保留并调整幽默 | 机智活泼，在目标语言中重现喜剧效果 |
| `conversational` | 随意、接近口语 | 友好亲切，像向朋友讲解一样 |
| `elegant` | 文学化、文笔精致 | 审美考究、富有韵律、用词精雕细琢 |

也接受自定义风格描述，例如 `--style "poetic and lyrical"`。

**自动检测**：
- “快翻”“quick”“直接翻译” → quick 模式
- “精翻”“refined”“publication quality”“proofread” → refined 模式
- 其他情况 → 默认模式（normal）

**升级提示**：normal 模式完成后，显示：
> 翻译已保存。如需进一步审校和润色，请回复“继续润色”或“refine”。

如果用户回复，则基于现有输出继续执行审校 → 润色步骤（与 refined-workflow.md 中 refined 模式的第 4–6 步相同）。

**受众预设**：

| 值 | 说明 | 效果 |
|-------|-------------|--------|
| `general` | 一般读者（默认） | 使用浅显语言，为术语提供更多译者注 |
| `technical` | 开发者/工程师 | 减少对常见技术术语的注释 |
| `academic` | 研究人员/学者 | 使用正式语体和精确术语 |
| `business` | 商务专业人士 | 使用适合商务场景的语气，并解释技术概念 |

也接受自定义受众描述，例如 `--audience "AI感兴趣的普通读者"`。

## 工作流

### 第 1 步：加载偏好设置

1.1 检查 EXTEND.md（见上文“偏好设置”部分）

1.2 如果存在适用于该语言对的内置术语表，则加载它：
- EN→ZH：[references/glossary-en-zh.md](references/glossary-en-zh.md)

1.3 合并术语表：EXTEND.md 的 `glossary`（内联）+ EXTEND.md 的 `glossary_files`（外部文件，路径相对于 EXTEND.md 所在位置）+ 内置术语表 + `--glossary` 文件（CLI 会覆盖所有其他设置）

### 第 2 步：实体化源内容并创建输出目录

实体化源内容（文件保持原样；内联文本/URL → 保存至 `translate/{slug}.md`），然后创建输出目录：`{source-dir}/{source-basename}-{target-lang}/`。如果未指定 `--from`，则检测源语言。

完整细节：[references/workflow-mechanics.md](references/workflow-mechanics.md)

**输出目录内容**（所有中间文件和最终文件均保存在此处）：

| 文件 | 模式 | 说明 |
|------|------|-------------|
| `translation.md` | 全部 | 最终译文（始终使用此名称） |
| `01-analysis.md` | 标准、精翻 | 内容分析（领域、语气、术语） |
| `02-prompt.md` | 标准、精翻 | 组装后的翻译提示词 |
| `03-draft.md` | 精翻 | 审校前的初稿 |
| `04-critique.md` | 精翻 | 批判性审校结果（仅诊断） |
| `05-revision.md` | 精翻 | 根据审校意见修改后的译文 |
| `chunks/` | 分块翻译 | 源内容分块和已翻译分块 |

### 第 3 步：评估内容长度

quick 模式不分块——无论长度如何都直接翻译。翻译前先估算词数。如果内容超过分块阈值（默认 4000 词），主动提醒：“本文约有 {N} 词。quick 模式会一次性翻译，不进行分块——对于长篇内容，使用 `--mode normal` 能通过保持术语一致性获得更好的结果。”如果用户没有切换模式，则继续。

对于 normal 和 refined 模式：

| 内容 | 操作 |
|---------|--------|
| < 分块阈值 | 作为单个整体翻译 |
| >= 分块阈值 | 分块翻译（见第 3.1 步） |

**3.1 长篇内容准备**（仅适用于达到或超过分块阈值的 normal/refined 模式）

翻译各分块之前：

1. **提取术语**：扫描整个文档，找出专有名词、技术术语和重复出现的短语
2. **构建会话术语表**：将提取的术语与已加载的术语表合并，确定一致的译法
3. **拆分为分块**：使用 `${BUN_X} {baseDir}/scripts/main.ts <file> [--max-words <chunk_max_words>] [--output-dir <output-dir>]`
   - 解析 Markdown 块（标题、段落、列表、代码块、表格等）
   - 在 Markdown 块边界处分割，以保留结构
   - 如果单个块超过阈值，则依次回退到按行分割和按词分割
4. **组装翻译提示词**：
   - 主智能体读取 `01-analysis.md`（如果存在），并使用 [references/subagent-prompt-template.md](references/subagent-prompt-template.md) 的第 1 部分组装共享上下文——内联目标风格、内容背景、合并后的术语表以及翻译难点
   - 在输出目录中保存为 `02-prompt.md`（仅包含共享上下文，不含任务指令）
5. **通过子智能体生成翻译初稿**（如果 Agent 工具可用）：
   - 为每个分块生成一个子智能体，并全部并行运行（模板的第 2 部分）
   - 每个子智能体读取 `02-prompt.md` 获取共享上下文，接收分块位置信息（第 N/M 块，以及它在论述中所处位置的简要上下文），翻译相应分块，并保存至 `chunks/chunk-NN-draft.md`
   - 共享的 `02-prompt.md`（其中包含术语表、比喻性语言映射、理解难点、原文风格以及分析得出的翻译难点）可保证一致性
   - 如果没有分块（内容低于阈值）：为整个源文件生成一个子智能体
   - 如果 Agent 工具不可用，则使用 `02-prompt.md` 在当前上下文中依次翻译各分块
6. **合并**：所有子智能体完成后，按顺序合并已翻译的分块。如果存在 `chunks/frontmatter.md`，则将其置于开头。refined 模式保存为 `03-draft.md`，normal 模式保存为 `translation.md`
7. 所有中间文件（源内容分块和已翻译分块）均保留在 `chunks/` 中

**合并分块初稿后**，将控制权交还主智能体，以进行批判性审校、修订和润色（第 4 步）。

### 第 4 步：翻译与精修

**翻译原则**（适用于所有模式）：

- **重写，而非直译**：将内容改写为自然、引人入胜的目标语言，使其读起来仿佛由熟练的母语作者从头创作。质量检验标准：“读起来是否像原本就是用目标语言写成的？”
- **准确优先**：事实、数据和逻辑必须与原文完全一致
- **行文自然**：使用符合目标语言习惯的语序。将原文中的长句拆分为更短、更自然的句子。根据隐喻和习语的实际含义进行转换，而非逐字翻译
- **术语**：始终一致地使用标准译法。专业术语首次出现时，在括号中标注原文
- **保留格式**：保留所有 Markdown 格式（标题、粗体、斜体、图片、链接、代码块）
- **主动解释**：对于目标受众可能缺乏背景知识的术语或概念，使用**加粗括号** `（**解释**）` 添加简洁说明。尽量少加注释——仅在确实有助于理解时添加
- **Frontmatter**：如果源内容含有 YAML frontmatter，则为源元数据字段添加 `source` 前缀（camelCase：`url`→`sourceUrl`、`title`→`sourceTitle` 等），将翻译后的值作为新的顶层字段添加（如果正文包含 H1，则跳过 `title`），其他字段保持不变

#### 快速模式

直接翻译 → 保存至 `translation.md`。应用上述所有翻译原则。

#### 标准模式

1. **分析** → `01-analysis.md`（领域、语气、术语、翻译难点）
2. **组装提示词** → `02-prompt.md`（包含上下文、术语表和难点的翻译指令）
3. **翻译**（遵循 `02-prompt.md`）→ `translation.md`

完成后提示用户：“翻译已保存。如需进一步审校和润色，请回复 **继续润色** 或 **refine**。”

如果用户继续，则执行批判性审校 → 修订 → 润色（与下方 refined 模式的第 4–6 步相同），保存 `03-draft.md`（将当前的 `translation.md` 重命名）、`04-critique.md`、`05-revision.md` 以及更新后的 `translation.md`。

#### 精翻模式

用于达到出版质量的完整工作流。各步骤的详细指南见 [references/refined-workflow.md](references/refined-workflow.md)。

子智能体（如果在第 3.1 步中使用）仅处理初稿。后续所有步骤（批判性审校、修订、润色）均由主智能体处理，主智能体可酌情将任务委派给子智能体。

步骤和保存的文件（均位于输出目录中）：
1. **分析** → `01-analysis.md`（领域、语气、术语、翻译难点）
2. **组装提示词** → `02-prompt.md`（包含内联上下文的翻译指令）
3. **初稿** → `03-draft.md`（包含译者注的翻译初稿；如果分块，则来自子智能体）
4. **批判性审校** → `04-critique.md`（仅诊断：准确性、欧化语言、策略执行、表达问题）
5. **修订** → `05-revision.md`（应用所有审校意见，生成修订后的译文）
6. **润色** → `translation.md`（最终出版级译文）

每一步都会读取前一步生成的文件，并在此基础上继续处理。

### 第 5 步：输出

最终译文始终位于输出目录中的 `translation.md`。

最终译文写入后，进行一次轻量级图片语言检查：

1. 收集译文中的图片引用
2. 找出可能包含大量文字的图片，例如封面、截图、图表、示意图、框架图和信息图
3. 如果任何图片中可能使用的主要文字语言与译文语言不一致，则主动提醒用户
4. 提醒必须仅使用列表。除非用户提出要求，否则不要自动本地化这些图片

提醒格式（沿用文章已使用的图片语法——标准 Markdown 或 wikilink）：
```text
可能需要进行图片本地化：
- ![示例封面](attachments/example-cover.png)：文章现已翻译为目标语言，但图片中可能仍含有源语言文字
- ![示例图表](attachments/example-diagram.png)：可能是文字较多的框架图，请检查其中的标签是否需要翻译
```

显示摘要：
```
**翻译完成**（{mode} 模式）

源文件：{source-path}
语言：{from} → {to}
输出目录：{output-dir}/
最终文件：{output-dir}/translation.md
已应用的术语表条目：{count}
```

如果发现图片语言不匹配的候选项，请在摘要后附上一条简短说明，告知用户部分嵌入图片可能仍需进行图片文字本地化，然后列出候选项。

## 扩展支持

可通过 EXTEND.md 使用自定义配置。有关路径和支持选项，请参阅**偏好设置**部分。
