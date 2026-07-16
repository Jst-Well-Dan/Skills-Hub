<!-- source-sha256: f4a5bb1697f9387557897a9c58b6406765728089a8d84cfbb6c40a93c3d136f7 -->
---
name: baoyu-markdown-to-html
description: 将 Markdown 转换为带样式的 HTML，并提供兼容微信的主题。支持代码高亮、数学公式、Mermaid（通过无头 Chrome 渲染为 PNG）、PlantUML、脚注、提示块、信息图，以及可选的外部链接底部引用。当用户要求“markdown to html”“convert md to html”“md 转 html”“微信外链转底部引用”，或需要从 Markdown 生成带样式的 HTML 输出时使用。
version: 1.117.3
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-markdown-to-html
    requires:
      anyBins:
        - bun
        - npx
---

# Markdown 转 HTML 转换器

将 Markdown 文件转换为具有精美样式和内联 CSS 的 HTML，并针对微信公众号及其他平台进行优化。

## 用户输入工具

当此技能需要向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置的用户输入工具**，即当前代理运行时提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **后备方式**：如果不存在此类工具，则发送一条带编号的纯文本消息，并要求用户针对每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持每次调用提出多个问题，请将所有适用问题合并到一次调用中；如果仅支持单个问题，则按优先级逐一提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行时中，请替换为本地等效工具。

## 脚本目录

**代理执行**：将此 SKILL.md 所在目录确定为 `{baseDir}`。解析 `${BUN_X}` 运行时：如果已安装 `bun` → 使用 `bun`；如果 `npx` 可用 → 使用 `npx -y bun`；否则建议安装 bun。将 `{baseDir}` 和 `${BUN_X}` 替换为实际值。

| 脚本 | 用途 |
|--------|---------|
| `scripts/main.ts` | 主入口点 |

## 偏好设置（EXTEND.md）

按以下优先级检查 EXTEND.md——找到的第一个生效：

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-markdown-to-html/EXTEND.md` | 项目 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-markdown-to-html/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-markdown-to-html/EXTEND.md` | 用户主目录 |

如果均未找到，则使用默认值。

**EXTEND.md 支持**：默认主题、自定义 CSS 变量、代码块样式、Mermaid 默认设置（`mermaid_theme`、`mermaid_scale`、`mermaid_background`）。

## 工作流程

### 步骤 0：预检查（中文内容）

**条件**：仅当输入文件包含中文文本时执行。

**检测方法**：
1. 读取输入 Markdown 文件
2. 检查内容是否包含 CJK 字符（中文/日文/韩文）
3. 如果不包含 CJK 内容 → 跳至步骤 1

**格式化建议**：

如果检测到 CJK 内容，并且 `baoyu-format-markdown` 技能可用：

使用 `AskUserQuestion` 询问是否先进行格式化。格式化可以修复：
- 标点符号位于粗体标记内部，导致 `**` 解析失败
- CJK 与英文之间的空格问题

**如果用户同意**：调用 `baoyu-format-markdown` 技能格式化文件，然后使用格式化后的文件作为输入。

**如果用户拒绝**：继续使用原始文件。

### 步骤 1：确定主题

**主题解析顺序**（第一个匹配项生效）：
1. 用户明确指定的主题（CLI `--theme` 或对话中指定）
2. EXTEND.md 中的 `default_theme`（此技能自己的 EXTEND.md，已在步骤 0 中检查）
3. `baoyu-post-to-wechat` EXTEND.md 中的 `default_theme`（跨技能后备）
4. 如果均未找到 → 使用 AskUserQuestion 进行确认

**跨技能 EXTEND.md 检查**（仅当此技能的 EXTEND.md 中没有 `default_theme` 时）：

如果 `$HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md` 存在，则读取该文件并查找 `default_theme:` 行。如果存在则使用其值；否则继续执行后续流程。

**如果主题从 EXTEND.md 解析得到**：直接使用，不要询问用户。

**如果未找到默认主题**：使用 `AskUserQuestion`，让用户从下方的[主题](#主题)表格中确认一个主题。

### 步骤 1.5：确定引用模式

**默认值**：关闭。默认情况下不要询问。

**仅当用户明确要求**“微信外链转底部引用”“底部引用”“文末引用”，或传入 `--cite` 时启用。

**启用后的行为**：
- 普通外部链接会渲染为带编号的上标，并集中收集到末尾的 `引用链接` 部分。
- `https://mp.weixin.qq.com/...` 链接保持为直接链接，不移动到底部。
- 链接文本与 URL 相同的裸链接保持内联。

### 步骤 2：转换

```bash
${BUN_X} {baseDir}/scripts/main.ts <markdown_file> --theme <theme> [--cite]
```

### 步骤 3：报告结果

显示 JSON 结果中的输出路径。如果创建了备份，请一并说明。

## 用法

```bash
${BUN_X} {baseDir}/scripts/main.ts <markdown_file> [options]
```

**选项：**

| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--theme <name>` | 主题名称（default、grace、simple、modern） | default |
| `--color <name\|hex>` | 主色：预设名称或十六进制值 | 主题默认值 |
| `--font-family <name>` | 字体：sans、serif、serif-cjk、mono 或 CSS 值 | 主题默认值 |
| `--font-size <N>` | 字号：14px、15px、16px、17px、18px | 16px |
| `--title <title>` | 覆盖 frontmatter 中的标题 | |
| `--cite` | 将外部链接转换为底部引用，并追加 `引用链接` 部分 | false（关闭） |
| `--keep-title` | 在内容中保留第一个标题 | false（移除） |
| `--mermaid-theme <name>` | Mermaid 主题：`default`、`forest`、`dark`、`neutral`、`base` | default |
| `--mermaid-scale <N>` | Mermaid 渲染比例（不大于 4 的正数） | 2 |
| `--mermaid-width <N>` | Mermaid 目标显示宽度，以 CSS px 为单位；当图表宽度小于此值时，PNG 将以 `width × scale` 像素渲染 | 860 |
| `--mermaid-bg <value>` | Mermaid 背景：`white`、`transparent` 或 `#hex` | white |
| `--no-mermaid` | 跳过 Mermaid PNG 渲染；输出 `<pre class="mermaid">` 后备内容 | false |
| `--help` | 显示帮助 | |

**颜色预设：**

| 名称 | 十六进制值 | 标签 |
|------|-----|-------|
| blue | #0F4C81 | 经典蓝 |
| green | #009874 | 翡翠绿 |
| vermilion | #FA5151 | 鲜艳朱红 |
| yellow | #FECE00 | 柠檬黄 |
| purple | #92617E | 薰衣草紫 |
| sky | #55C9EA | 天空蓝 |
| rose | #B76E79 | 玫瑰金 |
| olive | #556B2F | 橄榄绿 |
| black | #333333 | 石墨黑 |
| gray | #A9A9A9 | 烟灰色 |
| pink | #FFB7C5 | 樱花粉 |
| red | #A93226 | 中国红 |
| orange | #D97757 | 暖橙色（modern 默认值） |

**示例：**

```bash
# 基本转换（使用默认主题并移除第一个标题）
${BUN_X} {baseDir}/scripts/main.ts article.md

# 使用指定主题
${BUN_X} {baseDir}/scripts/main.ts article.md --theme grace

# 使用自定义颜色的主题
${BUN_X} {baseDir}/scripts/main.ts article.md --theme modern --color red

# 为普通外部链接启用底部引用
${BUN_X} {baseDir}/scripts/main.ts article.md --cite

# 在内容中保留第一个标题
${BUN_X} {baseDir}/scripts/main.ts article.md --keep-title

# 覆盖标题
${BUN_X} {baseDir}/scripts/main.ts article.md --title "My Article"
```

## 输出

**文件位置**：与输入 Markdown 文件位于同一目录。
- 输入：`/path/to/article.md`
- 输出：`/path/to/article.html`

**冲突处理**：如果 HTML 文件已存在，将先进行备份：
- 备份：`/path/to/article.html.bak-YYYYMMDDHHMMSS`

**输出到 stdout 的 JSON：**

```json
{
  "title": "Article Title",
  "author": "Author Name",
  "summary": "Article summary...",
  "htmlPath": "/path/to/article.html",
  "backupPath": "/path/to/article.html.bak-20260128180000",
  "contentImages": [
    {
      "placeholder": "MDTOHTMLIMGPH_1",
      "localPath": "/path/to/img.png",
      "originalPath": "imgs/image.png"
    }
  ],
  "mermaidImages": [
    {
      "hash": "a1b2c3d4e5f6",
      "localPath": "/path/to/imgs/.mermaid-cache/mermaid-a1b2c3d4e5f6.png",
      "cached": false
    }
  ]
}
```

**Mermaid 渲染**：以 ` ```mermaid ` 围栏标记的代码块会通过无头 Chrome（CDP）渲染为 PNG，并缓存到 `imgs/.mermaid-cache/mermaid-<hash>.png`。缓存键包含代码、主题、比例、目标宽度、背景和 Mermaid 版本。如果不希望将生成的图表提交到版本库，请将 `imgs/.mermaid-cache/` 添加到 `.gitignore`。系统需要安装 Chrome/Chromium/Edge；否则代码块会回退为 `<pre class="mermaid">…</pre>`，转换仍会成功。

## 主题

| 主题 | 说明 |
|-------|-------------|
| `default` | 经典——传统布局，标题居中并带有底部边框，H2 使用彩色背景和白色文字 |
| `grace` | 优雅——文字阴影、圆角卡片、精致的引用块（作者：@brzhang） |
| `simple` | 简约——现代极简风格、非对称圆角、清爽留白（作者：@okooo5km） |
| `modern` | 现代——大圆角、胶囊形标题、宽松行高（搭配 `--color red` 可呈现传统红金风格） |

## 支持的 Markdown 功能

| 功能 | 语法 |
|---------|--------|
| 标题 | `# H1` 到 `###### H6` |
| 粗体/斜体 | `**bold**`、`*italic*` |
| 代码块 | 使用 ` ```lang ` 并支持语法高亮 |
| 行内代码 | `` `code` `` |
| 表格 | GitHub 风格 Markdown 表格 |
| 图片 | `![alt](src)` |
| 链接 | `[text](url)`；添加 `--cite` 可将普通外部链接移至底部引用 |
| 引用块 | `> quote` |
| 列表 | `-` 表示无序列表，`1.` 表示有序列表 |
| 提示块 | `> [!NOTE]`、`> [!WARNING]` 等 |
| 脚注 | `[^1]` 引用 |
| 注音文本 | `{base|annotation}` |
| Mermaid | ` ```mermaid ` 代码块通过无头 Chrome 渲染为本地 PNG（缓存在 `imgs/.mermaid-cache/` 下）；如果 Chrome 不可用或渲染失败，则回退为 `<pre class="mermaid">` |
| PlantUML | ` ```plantuml ` 图表 |

## Frontmatter

支持使用 YAML frontmatter 提供元数据：

```yaml
---
title: Article Title
author: Author Name
description: Article summary
---
```

如果未找到标题，则从第一个 H1/H2 标题中提取，或使用文件名。

## 扩展支持

可通过 EXTEND.md 自定义配置。路径和支持的选项请参阅**偏好设置**部分。
