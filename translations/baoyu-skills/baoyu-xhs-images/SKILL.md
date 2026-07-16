<!-- source-sha256: 17bf5498641cc60cb98f0cc15fbea27fd42777d119a39fb54fd6418840442bba -->
---
name: baoyu-xhs-images
description: 生成信息图图片卡片系列，提供 12 种视觉风格、8 种布局和 3 种配色方案。将内容拆分为 1-10 张针对社交媒体互动优化的卡通风格图片卡片。当用户提到“小红书图片”“小红书种草”“小绿书”“微信图文”“微信贴图”“image cards”“图片卡片”、baoyu-xhs-images，或希望制作社交媒体信息图系列时使用。
version: 2.0.1
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-xhs-images
---

# 图片卡片系列生成器

将复杂内容拆分为吸睛的图片卡片系列，并提供多种风格选项。

## 用户输入工具

当此 skill 提示用户输入时，遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具**，即当前 agent 运行时所提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果不存在此类工具，则发送带编号的纯文本消息，并要求用户为每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持单次调用提出多个问题，则将所有适用问题合并到一次调用中；如果仅支持单个问题，则按优先级逐个询问。

下文对 `AskUserQuestion` 的具体引用仅为示例——在其他运行时中请替换为本地等效工具。

## 图片生成工具

当此 skill 需要渲染图片时，按以下顺序确定后端：

1. **当前请求覆盖设置**——如果用户在当前消息中指定了特定后端，则使用该后端。
2. **已保存的偏好**——如果 `EXTEND.md` 将 `preferred_image_backend` 设置为当前可用的后端，则使用该后端。
3. **自动选择**（当偏好为 `auto`、未设置或指定的后端不可用时）：
   - **Codex（`imagegen`）**——首先检查可用 skills / 工具清单。如果列出了名为 `imagegen` 的 skill，则说明你正在 Codex 中运行，并且必须使用它：通过 `Skill` 工具调用，设置 `skill: "imagegen"`，传入已保存提示词文件的内容（并按照 Codex `imagegen` 自身的参数传入输出路径和宽高比）。Codex `imagegen` 是该运行时中的官方光栅图像后端；除非用户明确指定了其他 `preferred_image_backend`，否则其优先级高于任何非原生 skill（例如 `baoyu-image-gen`）。
   - **通过 `codex exec` 使用 Codex（`codex-imagegen`）**——如果当前运行时未提供原生 `imagegen` skill，但 `codex` CLI 位于 `PATH` 中且存在有效的 `codex login`，则通过 `baoyu-image-gen --provider codex-cli` 调用（首选）；如果 baoyu-image-gen 不可用，则直接调用随附的包装器。详细信息、参数和运行时发现流程位于 [references/codex-imagegen.md](references/codex-imagegen.md)——仅在选择此分支时加载该文件。
   - **Cursor（`GenerateImage`）**——如果运行时提供原生 `GenerateImage` 工具，则说明你正在 Cursor 中运行；它与 Codex `imagegen` 一样，优先于任何非原生 skill。需要特别注意两个限制：(a) 它没有宽高比参数——必须在作为 `description` 传入的提示词文本中明确说明目标宽高比或尺寸；(b) 它不接受输出目录——文件会保存到工具管理的位置，因此生成后需要将文件复制或移动到此 skill 预期的输出路径（例如 `outputs/.../NN-xxx.png`）。参考图片通过 `reference_image_paths` 传入。
   - **其他运行时原生工具**——如果运行时提供其他原生图片工具（例如 Hermes `image_generate`），则以相同方式使用。
   - 否则，如果只安装了一个非原生后端（例如 `baoyu-image-gen`），则使用它。
   - 否则（存在多个非原生后端且没有运行时原生工具），询问用户一次——与其他初始问题合并提问。
4. **如果没有任何后端可用**，告知用户并询问如何继续。

**⛔ 绝不能使用 SVG、HTML、canvas 或其他基于代码的渲染方式替代光栅图片生成。** Codex `imagegen` 自身的说明指出，当“输出应为位图资源，而非仓库原生代码或矢量图”时应使用它。如果无法通过第 3 步确定光栅后端，则回退到第 4 步并询问用户——不要悄悄输出 SVG、编写内联 `<svg>` 标记或生成 HTML/CSS 图像作为替代方案。即使文章或章节看起来“像图表”，此规则仍然适用：调用此规则的上游 skill 已经确定其需要的是光栅图片。

**⛔ 绝不能通过覆盖已生成位图的方式修复其中的文字。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化叠加方式，来遮盖、重写、擦除、描边或替换已生成图片卡片中的标题、正文、标签或任何其他文字。如果文字错误或不清晰，应使用修正后的提示词重新生成、切换到卡片文字更少的布局，或询问用户要保留哪个不完美的候选版本。

设置 `preferred_image_backend: ask` 会强制每次运行都执行第 3 步中的询问，无论有哪些可用后端。用户可通过下文的 `## 更改偏好设置` 部分修改指定后端。

**提示词文件要求（强制）**：在调用任何后端之前，必须将每张图片完整、最终的提示词写入 `prompts/` 下的独立文件（命名格式：`NN-{type}-[slug].md`）。该文件是用于复现结果的记录，也让你能够在无需重新生成提示词的情况下切换后端。

上文中的具体工具名称（`imagegen`、`GenerateImage`、`image_generate`、`baoyu-image-gen`）仅为示例——请按照相同规则替换为本地等效工具。

## 批量生成策略

保存并验证当前生成组的所有提示词文件后，默认以批次方式生成图片。

优先级顺序：

1. 如果所选后端提供原生批处理或多任务接口，则使用该接口。每个任务必须保留各自的提示词文件、输出路径、宽高比、会话 ID 和直接参考图片。
2. 如果没有原生批处理接口，但运行时可以并行调用工具，则每次最多分派 `generation_batch_size` 张图片。默认值：`4`。当前消息中的明确用户请求（例如 `--batch-size 4` 或“并行 4 张一起生成”）会覆盖 EXTEND.md。
3. 如果原生批处理和并行工具调用均不可用，则按顺序生成。

规则：

- 遵循图片 1 锚点链：先生成图片 1，再以图片 1 为参考批量生成图片 2 及之后的图片。
- 在当前批次中所有选定的提示词文件都已存在于磁盘之前，绝不能开始该批次。
- 失败项重试一次，不要重新生成成功项。
- 不要仅为了并行渲染图片而使用 subagents。仅将 subagents 用于独立的提示词迭代或创意探索。

## 确认策略

默认行为：**生成前确认**。

- 将明确调用 skill、文件路径、匹配到的信号或预设，以及 `EXTEND.md` 默认值，全部视为**仅供推荐使用的输入**。它们均不授权跳过确认。
- 在用户完成第 2 步之前，**不要**开始第 3 步。
- 仅当当前请求明确要求跳过确认时才可跳过，例如：`--yes`、“直接生成”“不用确认”“跳过确认”“按默认出图”或同等表达。
- 如果用户明确跳过确认，则在生成前的下一条面向用户的进度消息中，说明采用的策略、风格、布局、配色、数量和后端。

## 语言

在提问、进度、错误和完成摘要中使用用户的语言。技术标记（风格名称、文件路径、代码）保持英文。

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--style <name>` | 视觉风格（参见下文“风格”） |
| `--layout <name>` | 信息布局（参见下文“布局”） |
| `--palette <name>` | 配色覆盖：macaron / warm / neon |
| `--preset <name>` | 风格 + 布局 + 可选配色的简写（参见下文“预设”；各预设的提示词片段位于 `references/style-presets.md`） |
| `--ref <files...>` | 应用于图片 1、作为系列锚点的参考图片 |
| `--batch-size <n>` | 本次运行的临时生成批次大小。默认使用 EXTEND.md 中的 `generation_batch_size`，否则为 4。限制在 1-8。 |
| `--yes` | 非交互模式：跳过所有确认，使用 EXTEND.md 或内置默认值，并自动确认推荐方案（路径 A） |

## 维度

三个独立选项可自由组合：

| 维度 | 控制内容 | 选项 |
|-----------|----------|---------|
| **风格** | 视觉美学（线条、装饰、渲染） | 12 种风格（参见下文“风格”） |
| **布局** | 信息结构（密度、排列） | 8 种布局（参见下文“布局”） |
| **配色**（可选） | 覆盖颜色，替换风格的默认颜色 | macaron / warm / neon（参见下文“配色”） |

示例：`--style notion --layout dense` 会生成一张知性知识卡片；添加 `--palette macaron` 可以柔化色彩，而不改变 notion 的渲染规则。`--preset` 是风格 + 布局（+ 可选配色）的简写。

**配色行为**：不指定 `--palette` → 使用风格内置颜色；指定 `--palette <name>` → 仅覆盖颜色，渲染规则保持不变。部分风格声明了 `default_palette`（例如 sketch-notes 默认使用 macaron）。

## 风格（12 种）

| 风格 | 说明 |
|-------|-------------|
| `cute`（默认） | 甜美、可爱、少女感美学 |
| `fresh` | 干净、清新、自然 |
| `warm` | 温馨、友好、亲切 |
| `bold` | 强冲击力、吸引注意 |
| `minimal` | 极度简洁、精致 |
| `retro` | 复古、怀旧、时髦 |
| `pop` | 鲜艳、活力、吸睛 |
| `notion` | 极简手绘线稿，知性感 |
| `chalkboard` | 黑板上的彩色粉笔风，富有教育感 |
| `study-notes` | 逼真的手写笔记照片风格，蓝色笔迹 + 红色批注 + 黄色荧光笔 |
| `screen-print` | 大胆的海报艺术、半色调纹理、有限配色、象征性叙事 |
| `sketch-notes` | 手绘教育信息图，暖奶油底色上的马卡龙粉彩，摇曳线条 |

各风格规范：`references/presets/<style>.md`。

## 布局（8 种）

| 布局 | 说明 |
|--------|-------------|
| `sparse`（默认） | 1-2 个要点，最大化冲击力 |
| `balanced` | 3-4 个要点，标准布局 |
| `dense` | 5-8 个要点，知识卡片风格 |
| `list` | 列举／排名（4-7 项） |
| `comparison` | 并排对比 |
| `flow` | 流程／时间线（3-6 步） |
| `mindmap` | 中心放射式（4-8 个分支） |
| `quadrant` | 四象限／环形分区 |

布局规范：`references/elements/canvas.md`。

## 配色（可选覆盖）

替换风格的颜色，同时保持渲染规则（线条处理、纹理）不变。

| 配色 | 背景 | 分区颜色 | 强调色 | 感受 |
|---------|------------|-------------|--------|------|
| `macaron` | 暖奶油色 #F5F0E8 | 蓝色 #A8D8EA、薰衣草紫 #D5C6E0、薄荷绿 #B5E5CF、蜜桃色 #F8D5C4 | 珊瑚色 #E8655A | 柔和、教育感 |
| `warm` | 柔和蜜桃色 #FFECD2 | 橙色 #ED8936、陶土色 #C05621、金色 #F6AD55、玫瑰色 #D4A09A | 赭色 #A0522D | 大地色调、温馨 |
| `neon` | 深紫色 #1A1025 | 青色 #00F5FF、品红色 #FF00FF、绿色 #39FF14、粉色 #FF6EC7 | 黄色 #FFFF00 | 高能、未来感 |

配色规范：`references/palettes/<palette>.md`。

## 预设（风格 + 布局快捷方式）

按场景分组的快速入门组合。使用 `--preset <name>`，或在第 2 步中推荐。

**知识与学习**：

| 预设 | 风格 | 布局 | 最适合 |
|--------|-------|--------|----------|
| `knowledge-card` | notion | dense | 干货知识卡、概念科普 |
| `checklist` | notion | list | 清单、排行榜 |
| `concept-map` | notion | mindmap | 概念图、知识脉络 |
| `swot` | notion | quadrant | SWOT 分析、四象限 |
| `tutorial` | chalkboard | flow | 教程步骤、操作流程 |
| `classroom` | chalkboard | balanced | 课堂笔记、知识讲解 |
| `study-guide` | study-notes | dense | 学习笔记、考试重点 |
| `hand-drawn-edu` | sketch-notes | flow | 手绘教程、流程图解 |
| `sketch-card` | sketch-notes | dense | 手绘知识卡 |
| `sketch-summary` | sketch-notes | balanced | 手绘总结、图文笔记 |

**生活方式与分享**：

| 预设 | 风格 | 布局 | 最适合 |
|--------|-------|--------|----------|
| `cute-share` | cute | balanced | 少女风分享、日常种草 |
| `girly` | cute | sparse | 甜美封面、氛围感 |
| `cozy-story` | warm | balanced | 生活故事、情感分享 |
| `product-review` | fresh | comparison | 产品对比、测评 |
| `nature-flow` | fresh | flow | 健康流程、自然主题 |

**冲击力与观点**：

| 预设 | 风格 | 布局 | 最适合 |
|--------|-------|--------|----------|
| `warning` | bold | list | 避坑指南、重要提醒 |
| `versus` | bold | comparison | 正反对比 |
| `clean-quote` | minimal | sparse | 金句、极简封面 |
| `pro-summary` | minimal | balanced | 专业总结、商务内容 |

**潮流与娱乐**：

| 预设 | 风格 | 布局 | 最适合 |
|--------|-------|--------|----------|
| `retro-ranking` | retro | list | 复古排行、经典盘点 |
| `throwback` | retro | balanced | 怀旧分享 |
| `pop-facts` | pop | list | 趣味冷知识 |
| `hype` | pop | sparse | 炸裂封面、惊叹分享 |

**海报与编辑设计**：

| 预设 | 风格 | 布局 | 最适合 |
|--------|-------|--------|----------|
| `poster` | screen-print | sparse | 海报风封面、影评书评 |
| `editorial` | screen-print | balanced | 观点文章、文化评论 |
| `cinematic` | screen-print | comparison | 电影对比、戏剧张力 |

完整提示词片段定义：`references/style-presets.md`。

## 自动选择

将内容信号匹配到最佳组合。第一个关键词匹配的行优先；如果没有匹配项，则回退到 `cute-share`。

| 来源中的信号 | 风格 | 布局 | 推荐预设 |
|-------------------|-------|--------|--------------------|
| 美妆、时尚、可爱、女孩、粉色 | `cute` | sparse/balanced | `cute-share`、`girly` |
| 健康、自然、清新、有机 | `fresh` | balanced/flow | `product-review`、`nature-flow` |
| 生活、故事、情感、温暖 | `warm` | balanced | `cozy-story` |
| 警告、重要、必须、关键 | `bold` | list/comparison | `warning`、`versus` |
| 专业、商务、优雅 | `minimal` | sparse/balanced | `clean-quote`、`pro-summary` |
| 经典、复古、传统 | `retro` | balanced | `throwback`、`retro-ranking` |
| 有趣、刺激、惊叹、精彩 | `pop` | sparse/list | `hype`、`pop-facts` |
| 知识、概念、生产力、SaaS | `notion` | dense/list | `knowledge-card`、`checklist` |
| 教育、教程、学习、课堂 | `chalkboard` | balanced/dense | `tutorial`、`classroom` |
| 笔记、手写、学习指南、逼真 | `study-notes` | dense/list/mindmap | `study-guide` |
| 电影、海报、观点、编辑设计、电影感 | `screen-print` | sparse/comparison | `poster`、`editorial`、`cinematic` |
| 手绘、信息图、工作流、手绘，图解 | `sketch-notes` | flow/balanced/dense | `hand-drawn-edu`、`sketch-card`、`sketch-summary` |

## 风格 × 布局矩阵

兼容性评分（✓✓ 强烈推荐，✓ 效果良好，✗ 避免）。当用户选择非默认组合且你想提示匹配不佳时使用。

|              | sparse | balanced | dense | list | comparison | flow | mindmap | quadrant |
|--------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| cute         | ✓✓ | ✓✓ | ✓  | ✓✓ | ✓  | ✓  | ✓  | ✓  |
| fresh        | ✓✓ | ✓✓ | ✓  | ✓  | ✓  | ✓✓ | ✓  | ✓  |
| warm         | ✓✓ | ✓✓ | ✓  | ✓  | ✓✓ | ✓  | ✓  | ✓  |
| bold         | ✓✓ | ✓  | ✓  | ✓✓ | ✓✓ | ✓  | ✓  | ✓✓ |
| minimal      | ✓✓ | ✓✓ | ✓✓ | ✓  | ✓  | ✓  | ✓  | ✓  |
| retro        | ✓✓ | ✓✓ | ✓  | ✓✓ | ✓  | ✓  | ✓  | ✓  |
| pop          | ✓✓ | ✓✓ | ✓  | ✓✓ | ✓✓ | ✓  | ✓  | ✓  |
| notion       | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ |
| chalkboard   | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓  | ✓✓ | ✓✓ | ✓  |
| study-notes  | ✗  | ✓  | ✓✓ | ✓✓ | ✓  | ✓  | ✓✓ | ✓  |
| screen-print | ✓✓ | ✓✓ | ✗  | ✓  | ✓✓ | ✓  | ✗  | ✓✓ |
| sketch-notes | ✓  | ✓✓ | ✓✓ | ✓✓ | ✓  | ✓✓ | ✓✓ | ✓  |

## 大纲策略

三种差异化方案——每种都会生成结构不同的大纲。工作流会推荐其中一种；路径 C 会生成全部三种并让用户选择。

| 策略 | 概念 | 最适合 | 结构 |
|----------|---------|----------|-----------|
| **A — 故事驱动** | 以个人经历为主线，优先建立情感共鸣 | 测评、个人分享、转变经历 | 钩子 → 问题 → 发现 → 体验 → 结论 |
| **B — 信息密集** | 价值优先，高效传递信息 | 教程、对比、清单 | 核心结论 → 信息卡 → 优点／缺点 → 建议 |
| **C — 视觉优先** | 以视觉冲击力为核心，文字最少 | 高审美产品、生活方式、氛围内容 | 主视觉 → 细节图 → 生活场景 → 行动号召 |

## 参考图片

用户提供的参考图片与内部“以图片 1 为锚点”的链（第 3 步）**相互独立**——二者会叠加使用。

**接收方式**：通过 `--ref <files...>` 或粘贴到对话中的路径。
- 文件路径 → 复制到 `refs/NN-ref-{slug}.{ext}`
- 仅粘贴图片但没有路径 → 询问路径，或提取风格特征作为文本回退方案

**使用模式**（每张参考图片分别设置）：

| 用法 | 效果 |
|-------|--------|
| `direct` | 将文件传给后端（通常仅用于图片 1，使锚点通过链传递） |
| `style` | 提取风格特征并追加到每张卡片的提示词正文 |
| `palette` | 提取十六进制颜色并追加到每张卡片的提示词正文 |

在每张受影响卡片的提示词 frontmatter 中记录参考图片：

```yaml
references:
  - ref_id: 01
    filename: 01-ref-brand.png
    usage: direct
```

生成时：验证文件存在。如果图片 1 使用 `usage: direct` 且后端接受参考图片 → 通过后端的参考图片参数传入（成为链的锚点）。图片 2 及之后的图片继续按照第 3 步，以图片 1 作为 `--ref`——不要再次叠加用户参考图片（避免信号冲突）。对于 `style`/`palette`，将提取出的特征嵌入每条提示词。

## 文件布局

```
image-cards/{topic-slug}/
├── source-{slug}.{ext}
├── analysis.md
├── outline-strategy-{a,b,c}.md    # Path C only
├── outline.md
├── prompts/NN-{type}-{slug}.md
├── NN-{type}-{slug}.png
└── refs/                          # only if --ref used
```

**Slug**：2-4 个单词，使用 kebab-case。 “AI 工具推荐” → `ai-tools-recommend`。如果发生冲突，则追加 `-YYYYMMDD-HHMMSS`。

**备份规则**（全流程适用）：覆盖任何文件之前——包括源文件、大纲、提示词、图片——将已有文件重命名为 `<name>-backup-YYYYMMDD-HHMMSS.<ext>`。这可以保护用户的编辑。

## 工作流

```
- [ ] Step 0: Load EXTEND.md ⛔ BLOCKING (interactive only)
- [ ] Step 1: Analyze content → analysis.md
- [ ] Step 2: Smart Confirm ⚠️ REQUIRED (Path A / B / C)
- [ ] Step 3: Generate images
- [ ] Step 4: Completion report
```

### 第 0 步：加载 EXTEND.md ⛔ 阻塞步骤

按顺序检查以下路径；使用第一个命中的文件：

| 路径 | 作用域 |
|------|-------|
| `.baoyu-skills/baoyu-xhs-images/EXTEND.md` | 项目 |
| `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-xhs-images/EXTEND.md` | XDG |
| `$HOME/.baoyu-skills/baoyu-xhs-images/EXTEND.md` | 用户主目录 |

- **找到** → 读取、解析并输出摘要（风格／布局／水印／语言），然后继续。
- **未找到 + 交互模式** → 执行首次设置（参见 `references/config/first-time-setup.md`），并在执行任何其他操作前保存。偏好设置存在之前，不要分析内容或询问风格问题——这能让首次运行行为保持可预测。
- **未找到 + `--yes`** → 跳过设置，使用内置默认值（无水印、自动选择风格／布局、语言取自内容）。不要提问，也不要创建 EXTEND.md。

**EXTEND.md 键**：水印、首选风格／布局、自定义风格定义、语言偏好、首选图片后端、生成批次大小。Schema：`references/config/preferences-schema.md`。

### 第 1 步：分析内容 → `analysis.md`

1. 保存源内容（如果 `source.md` 已存在，则应用备份规则）。
2. 按照 `references/workflows/analysis-framework.md` 执行深度分析：内容类型、钩子潜力、受众、互动信号、视觉机会图、滑动浏览流程。
3. 检测源语言，选择推荐图片数量（2-10）。
4. 使用上面的**自动选择**表，自动推荐策略 + 风格 + 布局 + 配色。
5. 将所有内容写入 `analysis.md`。

### 第 2 步：智能确认 ⚠️ 必需

**强制关卡**：根据[确认策略](#确认策略)，此步骤为必需步骤——用户在此确认之前（或在当前请求中通过 `--yes`／同等表达明确选择跳过之前），不能开始第 3 步。

目标：展示自动推荐方案，并让用户确认或调整。在 `--yes` 模式下完全跳过此步骤——使用分析结果和所有 CLI 覆盖选项，按照路径 A 继续。

**提问前显示摘要**：

```
📋 内容分析
  主题：[topic] | 类型：[content_type]
  要点：[key points]
  受众：[audience]

🎨 推荐方案（自动匹配）
  策略：[A/B/C] [name]（[reason]）
  风格：[style] · 布局：[layout] · 配色：[palette or 默认] · 预设：[preset]
  图片：[N]张（封面+[N-2]内容+结尾）
  元素：[background] / [decorations] / [emphasis]
```

然后提出一个问题——提供三条路径。选项文案必须逐字复制：`references/confirmation.md`。

**路径 A——快速确认**（信任自动推荐）：使用推荐的策略 + 风格生成一个大纲 → 保存到 `outline.md` → 第 3 步。

**路径 B——自定义**：提出五个问题（策略／风格、布局、配色、数量、可选备注），并预先填入推荐值——留空则保留推荐值。使用用户的选择生成一个大纲 → `outline.md` → 第 3 步。参见 `references/confirmation.md`。

**路径 C——详细模式**：包含两轮子确认。

- *第 2a 步——内容理解*：询问卖点（多选）、受众、风格偏好（真实／专业／审美／自动）以及可选背景信息。更新 `analysis.md`。
- *第 2b 步——三个大纲变体*：生成 `outline-strategy-a.md`、`outline-strategy-b.md`、`outline-strategy-c.md`。每个大纲必须具有不同的结构和不同的推荐风格——在 frontmatter 中包含 `style_reason`。页数启发式规则：A 约 4-6 页，B 约 3-5 页，C 约 3-4 页。模板：`references/workflows/outline-template.md`；frontmatter 示例位于 `references/confirmation.md`。
- *第 2c 步——选择*：提出三个问题（大纲 A/B/C/Combined、风格、视觉元素）。将选定或合并后的大纲保存到 `outline.md` → 第 3 步。

### 第 3 步：生成图片

使用已确认的大纲 + 风格 + 布局 + 配色：

**视觉一致性——图片 1 锚点链**：如果不设置锚点，角色、吉祥物和色彩渲染会在不同调用之间发生漂移。先生成图片 1（封面），不使用 `--ref`；然后将图片 1 作为 `--ref` 传给后续每张图片。这是此 skill 保持一致性最重要的技巧——即使后端还支持会话 ID，也不要跳过。

生成流程：

1. 使用用户的首选语言，将每张图片的完整提示词写入 `prompts/NN-{type}-{slug}.md`（应用备份规则），然后验证所有选定的提示词文件都已存在。
2. 首先生成**图片 1**，不使用 `--ref`；PNG 文件适用备份规则。这将建立锚点。
3. 为**图片 2 及之后的图片**建立任务列表，使用图片 1 作为 `--ref <path-to-image-01.png>`。
4. 按照 `## 批量生成策略` 分批分派图片 2 及之后的图片：优先使用后端原生批处理，其次使用运行时并行工具调用，仅在无法使用二者时按顺序生成。
5. 每完成一张图片后报告进度。失败时，仅使用同一个已保存的提示词文件重试失败项一次。

**水印**（如果在 EXTEND.md 中启用）：将以下内容追加到生成提示词：

```
Include a subtle watermark "[content]" positioned at [position].
The watermark should be legible but not distracting.
```

参见 `references/config/watermark-guide.md`。

**后端选择**：遵循顶部的图片生成工具规则——使用任何可用后端；如果有多个后端，则在生成任何图片前询问一次。在 `--yes` 模式下，使用 EXTEND.md 偏好，并回退到第一个可用后端。调用任何后端之前，提示词文件必须存在。

**`codex-imagegen` 调用**：当规则确定使用 `codex-imagegen` 时，请参阅 [references/codex-imagegen.md](references/codex-imagegen.md) 了解调用约定（首选 `baoyu-image-gen --provider codex-cli` 路径、运行时包装器发现、参数说明、stdout schema、批处理语义——每次调用 n=1，因此卡片批次必须为每张卡片分别分派一次包装器调用；包装器不接受 `--sessionId`，所以链式一致性必须来自上述第 3 步中的 `--ref`）。

**会话 ID**（如果后端支持 `--sessionId`）：每张图片都使用 `cards-{topic-slug}-{timestamp}`；将它与参考图片链结合，可获得最佳一致性。

### 第 4 步：完成报告

```
Image Card Series Complete!

Topic: [topic]
Mode: [Quick / Custom / Detailed]
Strategy: [A/B/C/Combined]
Style: [name]
Palette: [name or "default"]
Layout: [name or "varies"]
Location: [directory]
Images: N total

✓ analysis.md
✓ outline.md
✓ outline-strategy-a/b/c.md (detailed mode only)

- 01-cover-[slug].png ✓ Cover (sparse)
- 02-content-[slug].png ✓ Content (balanced)
- ...
- NN-ending-[slug].png ✓ Ending (sparse)
```

## 内容拆分原则

| 位置 | 目的 | 典型布局 |
|----------|---------|----------------|
| 封面（图片 1） | 钩子 + 视觉冲击力 | `sparse` |
| 内容（中间） | 每张图片承载一个核心价值点 | `balanced` / `dense` / `list` / `comparison` / `flow` |
| 结尾（最后一张） | 行动号召／总结 | `sparse` 或 `balanced` |

有关风格 × 布局兼容性矩阵，请参阅上面的**风格 × 布局矩阵**。

## 图片修改

| 操作 | 方法 |
|--------|-----|
| 编辑 | **先**更新 `prompts/NN-{type}-{slug}.md`，然后使用相同的会话 ID 重新生成 |
| 添加 | 指定位置、创建提示词、生成图片，将后续文件重新编号为 `NN+1`，更新大纲 |
| 删除 | 删除文件，将后续文件重新编号为 `NN-1`，更新大纲 |

重新生成之前，始终先更新提示词文件——它是事实来源，并确保修改可复现。

文字修正策略：

- 如果卡片的标题、正文、标签或任何其他渲染文字存在拼写错误、乱码、难以阅读或视觉效果不佳，不要使用代码修补位图。
- 对于文字修正型重新生成，应写入新的提示词文件和新的输出路径，以便保留有缺陷的候选版本供比较。
- 后期处理仅限于裁剪、调整尺寸、压缩或格式转换，不得更改文字或主体构图。

## 参考文件

| 文件 | 内容 |
|------|---------|
| `references/confirmation.md` | 每条确认路径所需的 AskUserQuestion 原文 |
| `references/style-presets.md` | 完整的预设快捷方式定义 |
| `references/presets/<style>.md` | 各风格的元素定义 |
| `references/palettes/<name>.md` | 各配色的颜色定义 |
| `references/elements/canvas.md` | 宽高比、安全区域、网格布局 |
| `references/elements/image-effects.md` | 抠图、描边、滤镜 |
| `references/elements/typography.md` | 装饰文字、标签、文字方向 |
| `references/elements/decorations.md` | 强调标记、背景、涂鸦、边框 |
| `references/workflows/analysis-framework.md` | 内容分析框架 |
| `references/workflows/outline-template.md` | 包含布局指南的大纲模板 |
| `references/workflows/prompt-assembly.md` | 提示词组装指南 |
| `references/config/preferences-schema.md` | EXTEND.md schema |
| `references/config/first-time-setup.md` | 首次设置流程 |
| `references/config/watermark-guide.md` | 水印配置 |

## 注意事项

- 生成失败时，在报告错误前自动重试一次。
- 对敏感公众人物，使用风格化的卡通替代形象。
- 智能确认（第 2 步）为必需步骤；详细模式会增加第二轮确认（2a + 2c）。

## 更改偏好设置

EXTEND.md 位于第 0 步所列路径中第一个匹配的位置。可通过三种方式更改：

- **直接编辑**——打开 EXTEND.md 并修改字段。完整 schema：`references/config/preferences-schema.md`。
- **交互式重新配置**——删除 EXTEND.md（或提出“reconfigure baoyu-xhs-images preferences”／“重新配置”）。下次运行时将重新触发首次设置。
- **常用单行修改**：
  - `preferred_image_backend: auto`——默认值；运行时原生工具优先，如果仅安装了一个后端则回退到该后端，仅当存在多个非原生后端时才询问。
  - `preferred_image_backend: codex-imagegen`——固定使用 Codex 内置后端。
  - `preferred_image_backend: baoyu-image-gen`——固定使用 baoyu-image-gen skill。
  - `preferred_image_backend: ask`——每次运行都确认后端。
  - `generation_batch_size: 4`——后端或运行时支持批处理或并行生成时，默认并发渲染的图片数量。
  - `preferred_style: notion`、`preferred_layout: dense`、`preferred_palette: macaron`、`language: zh`。
  - `watermark.enabled: true` + `watermark.content: "@handle"`——添加水印。
