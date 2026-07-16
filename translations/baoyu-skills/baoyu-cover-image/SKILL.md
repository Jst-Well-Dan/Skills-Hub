<!-- source-sha256: 36804fce98bcb9ebe4a51c26f6f276a807805aab980ca4a0718daa40a5cc7fda -->
---
name: baoyu-cover-image
description: 通过 5 个维度（类型、配色、渲染、文本、氛围）生成文章封面图，组合使用 11 种配色方案和 7 种渲染风格。支持电影画幅（2.35:1）、宽屏（16:9）和正方形（1:1）宽高比。当用户要求“生成封面图”“创建文章封面”或“制作封面”时使用。
version: 1.117.5
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-cover-image
---

# 封面图生成器

通过 5 个维度的自定义，为文章生成精美的封面图。

## 用户输入工具

当此技能需要向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置的用户输入工具**，即当前智能体运行时提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果不存在此类工具，则发送带编号的纯文本消息，并要求用户针对每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持单次调用提出多个问题，则将所有适用的问题合并到一次调用中；如果仅支持单个问题，则按优先级依次提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行时中请替换为当地的等效工具。

## 图像生成工具

当此技能需要渲染图像时，请按以下顺序确定后端：

1. **当前请求覆盖设置**——如果用户在当前消息中指定了特定后端，请使用该后端。
2. **已保存的偏好设置**——如果 `EXTEND.md` 将 `preferred_image_backend` 设置为当前可用的后端，请使用该后端。
3. **自动选择**（当偏好设置为 `auto`、未设置或固定的后端不可用时）：
   - **Codex（`imagegen`）**——首先检查可用技能/工具清单。如果列出了名为 `imagegen` 的技能，则表示你正在 Codex 中运行，并且必须使用它：通过 `Skill` 工具调用，传入 `skill: "imagegen"`，并提供已保存提示词文件的内容（以及 Codex `imagegen` 自身参数所要求的输出路径和宽高比）。Codex `imagegen` 是该运行时中的官方光栅图像后端，其优先级高于任何非原生技能（例如 `baoyu-image-gen`），除非用户明确将 `preferred_image_backend` 固定为其他后端。
   - **通过 `codex exec` 使用 Codex（`codex-imagegen`）**——如果当前运行时没有提供原生 `imagegen` 技能，但 `codex` CLI 位于 `PATH` 中且已通过有效的 `codex login` 登录，则通过 `baoyu-image-gen --provider codex-cli` 调用（首选）；如果 `baoyu-image-gen` 不可用，则直接调用捆绑的包装器。详细信息、参数和运行时发现流程位于 [references/codex-imagegen.md](references/codex-imagegen.md)——仅在选择此分支时加载该文件。
   - **Cursor（`GenerateImage`）**——如果运行时提供原生 `GenerateImage` 工具，则表示你正在 Cursor 中运行；与 Codex `imagegen` 一样，它的优先级高于所有非原生技能。需要注意两个严格限制：(a) 它没有宽高比参数——必须在作为 `description` 传入的提示词文本中明确说明目标宽高比/尺寸；(b) 它不接受输出目录——文件会保存到工具管理的位置，因此生成后需要将文件复制/移动到技能预期的输出路径（例如 `outputs/.../NN-xxx.png`）。参考图像应放入 `reference_image_paths`。
   - **其他运行时原生工具**——如果运行时提供其他原生图像工具（例如 Hermes `image_generate`），请以相同方式使用。
   - 否则，如果只安装了一个非原生后端（例如 `baoyu-image-gen`），请使用它。
   - 否则（存在多个非原生后端且没有运行时原生工具），向用户询问一次——与其他初始问题合并提问。
4. **如果没有任何可用后端**，请告知用户并询问如何继续。

**⛔ 绝不可使用 SVG、HTML、canvas 或其他基于代码的渲染方式替代光栅图像生成。** Codex `imagegen` 自身的说明指出，当“输出应为位图资源，而不是仓库原生代码或矢量图”时，应使用该工具。如果无法通过第 3 步确定光栅图像后端，请转到第 4 步并询问用户——不要擅自输出 SVG、编写内联 `<svg>` 标记或生成 HTML/CSS 艺术图作为替代方案。即使文章/章节看起来“类似图表”，此规则仍然适用：调用此规则的上游技能已经决定其需要的是光栅图像。

**⛔ 绝不可通过在生成的位图上覆盖绘制来修复渲染文本。** 不得使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化叠加方式，在已生成的封面图中遮盖、重写、擦除、描边或替换标题/副标题文本。如果文本错误或不清晰，请使用修正后的提示词重新生成、切换到文本更少或无标题的版本，或者询问用户要保留哪个不完美的候选图。

将 `preferred_image_backend: ask` 设置为该值，会强制每次运行时都执行第 3 步的询问，无论有哪些后端可用。用户可以通过下方的 `## 更改偏好设置` 章节更改固定后端。

**提示词文件要求（强制）**：在调用任何后端之前，必须将每张图像完整、最终的提示词写入 `prompts/` 下的独立文件中（命名格式：`NN-{type}-[slug].md`）。后端接收提示词文件（或其内容）；该文件是可复现性记录，使你可以在不重新生成提示词的情况下切换后端。

上文中的具体工具名称（`imagegen`、`GenerateImage`、`image_generate`、`baoyu-image-gen`）仅为示例——请按照相同规则替换为当地的等效工具。

## 确认策略

默认行为：**生成前进行确认**。

- 明确调用技能、文件路径、匹配的关键词/预设、`EXTEND.md` 默认值以及任何已记录的自动选择，都只能视为**推荐依据**。这些条件均不授权跳过确认。
- 在用户确认尺寸、宽高比、语言和后端选项之前，**不得**开始第 3 步或第 4 步。
- 仅当当前请求明确要求跳过确认时才可跳过，例如：`--quick`、“直接生成”、“不用确认”、“跳过确认”、“按默认出图”或等效表述。`EXTEND.md` 中的 `quick_mode: true` 视为长期有效的明确退出确认设置——仅在希望每次运行都跳过第 2 步时才设置该值。
- 如果明确跳过确认，则在生成前的下一条面向用户的进度消息中说明假定的尺寸、宽高比、语言和后端。

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--type <name>` | hero、conceptual、typography、metaphor、scene、minimal |
| `--palette <name>` | warm、elegant、cool、dark、earth、vivid、pastel、mono、retro、duotone、macaron |
| `--rendering <name>` | flat-vector、hand-drawn、painterly、digital、pixel、chalk、screen-print |
| `--style <name>` | 预设简写（参见[风格预设](references/style-presets.md)） |
| `--text <level>` | none、title-only、title-subtitle、text-rich |
| `--mood <level>` | subtle、balanced、bold |
| `--font <name>` | clean、handwritten、serif、display |
| `--aspect <ratio>` | 16:9（默认）、2.35:1、4:3、3:2、1:1、3:4 |
| `--lang <code>` | 标题语言（en、zh、ja 等） |
| `--no-title` | `--text none` 的别名 |
| `--quick` | 跳过确认，使用自动选择 |
| `--ref <files...>` | 用于指导风格/构图的参考图像 |

## 五个维度

| 维度 | 可选值 | 默认值 |
|-----------|--------|---------|
| **类型** | hero、conceptual、typography、metaphor、scene、minimal | auto |
| **配色** | warm、elegant、cool、dark、earth、vivid、pastel、mono、retro、duotone、macaron | auto |
| **渲染** | flat-vector、hand-drawn、painterly、digital、pixel、chalk、screen-print | auto |
| **文本** | none、title-only、title-subtitle、text-rich | title-only |
| **氛围** | subtle、balanced、bold | balanced |
| **字体** | clean、handwritten、serif、display | clean |

自动选择规则：[references/auto-selection.md](references/auto-selection.md)

## 图库

**类型**：hero、conceptual、typography、metaphor、scene、minimal
→ 详情：[references/types.md](references/types.md)

**配色**：warm、elegant、cool、dark、earth、vivid、pastel、mono、retro、duotone、macaron
→ 详情：[references/palettes/](references/palettes/)

**渲染**：flat-vector、hand-drawn、painterly、digital、pixel、chalk、screen-print
→ 详情：[references/renderings/](references/renderings/)

**文本级别**：none（纯视觉）| title-only（默认）| title-subtitle | text-rich（带标签）
→ 详情：[references/dimensions/text.md](references/dimensions/text.md)

**氛围级别**：subtle（低对比度）| balanced（默认）| bold（高对比度）
→ 详情：[references/dimensions/mood.md](references/dimensions/mood.md)

**字体**：clean（无衬线）| handwritten | serif | display（粗体装饰字体）
→ 详情：[references/dimensions/font.md](references/dimensions/font.md)

## 文件结构

根据 `default_output_dir` 偏好设置确定输出目录：
- `same-dir`：`{article-dir}/`
- `imgs-subdir`：`{article-dir}/imgs/`
- `independent`（默认）：`cover-image/{topic-slug}/`

```
<output-dir>/
├── source-{slug}.{ext}    # 源文件
├── refs/                  # 参考图像（如有提供）
│   ├── ref-01-{slug}.{ext}
│   └── ref-01-{slug}.md   # 描述文件
├── prompts/cover.md       # 生成提示词
└── cover.png              # 输出图像
```

**Slug**：2–4 个单词，采用 kebab-case。发生冲突时：追加 `-YYYYMMDD-HHMMSS`

## 工作流程

### 进度检查清单

```
封面图进度：
- [ ] 第 0 步：检查偏好设置（EXTEND.md）⛔ 阻塞项
- [ ] 第 1 步：分析内容 + 保存参考文件 + 确定输出目录
- [ ] 第 2 步：确认选项（6 个维度）⚠️ 使用 --quick 时除外
- [ ] 第 3 步：创建提示词
- [ ] 第 4 步：生成图像
- [ ] 第 5 步：完成报告
```

### 流程

```
输入 → [第 0 步：偏好设置] ─┬─ 已找到 → 继续
                             └─ 未找到 → 首次设置 ⛔ 阻塞项 → 保存 EXTEND.md → 继续
        ↓
分析 + 保存参考文件 → [输出目录] → [确认：6 个维度] → 提示词 → 生成 → 完成
                                              ↓
                                  （使用 --quick 或全部指定时跳过）
```

### 第 0 步：加载偏好设置 ⛔ 阻塞项

按优先级顺序检查 EXTEND.md——使用找到的第一个文件：

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-cover-image/EXTEND.md` | 项目 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-cover-image/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-cover-image/EXTEND.md` | 用户主目录 |

| 结果 | 操作 |
|--------|--------|
| 已找到 | 加载并显示摘要 → 继续 |
| 未找到 | ⛔ 执行首次设置（[references/config/first-time-setup.md](references/config/first-time-setup.md)）→ 保存 → 继续 |

**关键要求**：如果未找到，则必须先完成设置，再执行任何其他步骤或提出任何其他问题。

### 第 1 步：分析内容

1. **保存参考图像**（如有提供）→ [references/workflow/reference-images.md](references/workflow/reference-images.md)
2. **保存源内容**（如果是粘贴的内容，则保存到 `source.md`）
3. **分析内容**：主题、语气、关键词、视觉隐喻
4. **深入分析参考资料** ⚠️：提取具体、明确的元素（参见 reference-images.md）
5. **检测语言**：比较源内容、用户输入和 EXTEND.md 偏好设置
6. **确定输出目录**：遵循“文件结构”规则

**⚠️ 参考图像中的人物：**

如果参考图像包含应该出现在封面中的**人物**：

- **模型支持 `--ref`**（默认）：将图像复制到 `refs/`，生成时通过 `--ref` 传入。无需描述文件——模型可以直接看到面部。
- **模型不支持 `--ref`**（Jimeng、Seedream 3.0）：创建 `refs/ref-NN-{slug}.md`，为每个角色提供描述（头发、眼镜、肤色、服装）。将其作为 MUST/REQUIRED 指令嵌入提示词文本。

完整决策表请参见 [reference-images.md](references/workflow/reference-images.md)。

### 第 2 步：确认选项 ⚠️

**强制关卡**：根据[确认策略](#确认策略)，此步骤是必需的——在用户于此确认之前，第 3–4 步不得开始（除非用户通过 `--quick`、`quick_mode: true` 或当前请求中的等效表述明确选择退出确认）。

**必须使用 `AskUserQuestion` 工具**以交互式选择的形式展示选项——不得使用纯文本表格。单次 `AskUserQuestion` 调用最多展示 4 个问题（类型、配色、渲染、字体 + 设置）。每个问题应首先显示推荐选项及其理由，然后列出其他选项。

完整确认流程和问题格式：[references/workflow/confirm-options.md](references/workflow/confirm-options.md)

| 条件 | 跳过 | 仍需询问 |
|-----------|---------|-------------|
| `--quick` 或 `quick_mode: true` | 6 个维度 | 宽高比（除非已指定 `--aspect`） |
| 已指定全部 6 项及 `--aspect` | 全部 | 无 |

### 第 3 步：创建提示词

保存到 `prompts/cover.md`。模板：[references/workflow/prompt-template.md](references/workflow/prompt-template.md)

**关键要求——Frontmatter 中的参考文件**：
- 保存到 `refs/` 的文件 → 添加到 frontmatter 的 `references` 列表
- 以文字方式提取的风格（无文件）→ 省略 `references`，在正文中描述
- 写入前 → 验证：`test -f refs/ref-NN-{slug}.{ext}`

正文中的**参考元素**必须详细说明，以 “MUST”/“REQUIRED” 为前缀，并包含整合方式。

### 第 4 步：生成图像

1. 如果是重新生成，**备份现有的** `cover.png`
2. 根据顶部的 `## 图像生成工具` 规则**选择后端**：使用任何可用后端；如果有多个，则向用户询问一次。每个会话在首次生成前执行一次即可。
3. 在调用后端之前，必须将完整的最终提示词写入 `prompts/01-cover-[slug].md`（强制要求）。
4. **处理提示词 frontmatter 中的参考文件**：
   - `direct` 用法 → 通过 `--ref` 传入（使用支持参考图像的后端）
   - `style`/`palette` → 提取特征并追加到提示词
5. **生成**：使用提示词文件、输出路径和宽高比调用选定的后端。
   - **`codex-imagegen`**：调用约定（首选的 `baoyu-image-gen --provider codex-cli` 路径、运行时包装器发现方式、参数说明、stdout schema、批处理语义）参见 [references/codex-imagegen.md](references/codex-imagegen.md)。
   - **Codex `imagegen`（原生）**或其他运行时原生工具/`baoyu-image-gen` 技能：遵循上方 `## 图像生成工具` 中的规则。
6. 失败时：自动重试一次

### 第 5 步：完成报告

```
封面图已生成！

主题：[topic]
类型：[type] | 配色：[palette] | 渲染：[rendering]
文本：[text] | 氛围：[mood] | 字体：[font] | 宽高比：[ratio]
标题：[title or "纯视觉"]
语言：[lang] | 水印：[已启用/已禁用]
参考资料：[N 张图像或“已提取风格”或“无”]
位置：[directory path]

文件：
✓ source-{slug}.{ext}
✓ prompts/cover.md
✓ cover.png
```

## 图像修改

| 操作 | 步骤 |
|--------|-------|
| **重新生成** | 备份 → 先更新提示词文件 → 重新生成 |
| **更改维度** | 备份 → 确认新值 → 更新提示词 → 重新生成 |

文本修正策略：

- 如果标题/副标题拼写错误、出现乱码、难以辨认或视觉效果较弱，不得使用代码修补位图。
- 进行文本修正并重新生成时，应写入新的提示词文件和新的输出路径，以便保留有缺陷的候选图进行比较。
- 后期处理仅限裁剪、调整尺寸、压缩或格式转换，不得改变文本或主要构图。

## 构图原则

- **留白**：保留 40–60% 的呼吸空间
- **视觉锚点**：主要元素居中或向左偏移
- **人物**：使用简化的剪影；不得使用写实人物
- **标题**：使用用户/源内容中的确切标题；不得自行编造

## 更改偏好设置

EXTEND.md 位于**第 0 步**中所述的路径。可通过三种方式更改：

- **直接编辑**——打开 EXTEND.md 并修改字段。完整 schema：[references/config/preferences-schema.md](references/config/preferences-schema.md)。
- **交互式重新配置**——删除 EXTEND.md（或要求“reconfigure baoyu-cover-image preferences”/“重新配置”）。下次运行时会重新触发首次设置。
- **常用单行修改**：
  - `preferred_image_backend: auto`——默认值；优先使用运行时原生工具，然后回退到唯一已安装的后端，仅当存在多个非原生后端时才询问。
  - `preferred_image_backend: codex-imagegen`——固定使用 Codex 内置后端。
  - `preferred_image_backend: baoyu-image-gen`——固定使用 baoyu-image-gen 技能。
  - `preferred_image_backend: ask`——每次运行都确认后端。
  - `watermark.enabled: true`、`preferred_type`、`preferred_palette`、`preferred_rendering`、`default_aspect`、`quick_mode: true`、`language`——调整自动选择默认值和确认流程。

## 参考资料

**维度**：[text.md](references/dimensions/text.md) | [mood.md](references/dimensions/mood.md) | [font.md](references/dimensions/font.md)
**配色**：[references/palettes/](references/palettes/)
**渲染**：[references/renderings/](references/renderings/)
**类型**：[references/types.md](references/types.md)
**自动选择**：[references/auto-selection.md](references/auto-selection.md)
**风格预设**：[references/style-presets.md](references/style-presets.md)
**兼容性**：[references/compatibility.md](references/compatibility.md)
**视觉元素**：[references/visual-elements.md](references/visual-elements.md)
**工作流程**：[confirm-options.md](references/workflow/confirm-options.md) | [prompt-template.md](references/workflow/prompt-template.md) | [reference-images.md](references/workflow/reference-images.md)
**配置**：[preferences-schema.md](references/config/preferences-schema.md) | [first-time-setup.md](references/config/first-time-setup.md) | [watermark-guide.md](references/config/watermark-guide.md)
