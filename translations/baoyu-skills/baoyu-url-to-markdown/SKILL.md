<!-- source-sha256: 40913749b0e95165b02771bdf17bb8ed9fa0a72787d3e09571341ab7148359d0 -->
---
name: baoyu-url-to-markdown
description: 使用 baoyu-fetch CLI（通过带有站点专用适配器的 Chrome CDP）获取任意 URL 并转换为 Markdown。内置适用于 X/Twitter、YouTube 字幕、Hacker News 讨论串以及通过 Defuddle 处理的通用页面的适配器。通过交互等待模式处理登录/CAPTCHA。当用户希望将网页保存为 Markdown 时使用。
version: 1.61.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-url-to-markdown
    requires:
      anyBins:
        - bun
---

# URL 转 Markdown

通过 `baoyu-fetch` CLI（Chrome CDP + 站点专用适配器）获取任意 URL，并将其转换为整洁的 Markdown。

## 用户输入工具

当此技能需要询问用户时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用当前智能体运行环境提供的内置用户输入工具**——例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **后备方案**：如果不存在此类工具，则发送带编号的纯文本消息，并要求用户针对每个问题回复所选编号/答案。
3. **批量提问**：如果工具支持单次调用提出多个问题，请将所有适用问题合并到一次调用中；如果仅支持单个问题，则按优先级顺序逐一询问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行环境中请替换为本地等效工具。

## CLI 设置

**重要**：CLI 源码内置于 `{baseDir}/scripts/lib`。`scripts/package.json` 仅安装第三方运行时依赖项。

**智能体执行说明**：
1. 确定此 SKILL.md 文件所在目录的路径，并将其作为 `{baseDir}`
2. 解析 `${BUN}` 运行时：如果已安装 `bun` → 使用 `bun`；否则建议安装 Bun
3. 如果 `{baseDir}/scripts/node_modules` 不存在，运行 `${BUN} install --cwd {baseDir}/scripts`
4. `${READER}` = `{baseDir}/scripts/baoyu-fetch`
5. 将本文档中的所有 `${READER}` 替换为解析后的值

## 偏好设置（EXTEND.md）

按以下优先级顺序检查 EXTEND.md——使用第一个找到的文件：

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-url-to-markdown/EXTEND.md` | 项目 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-url-to-markdown/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-url-to-markdown/EXTEND.md` | 用户主目录 |

| 结果 | 操作 |
|--------|--------|
| 已找到 | 读取、解析并应用设置 |
| 未找到 | **必须**运行首次设置（见下文）——不得静默创建默认设置 |

**EXTEND.md 支持的设置**：默认下载媒体、默认输出目录。

### 首次设置 ⛔ 阻塞

未找到 EXTEND.md 时，你**必须**使用 `AskUserQuestion` 收集偏好设置，然后才能创建 EXTEND.md。**绝不允许**使用静默默认值创建 EXTEND.md。在设置完成前，生成操作处于阻塞状态。将以下三个问题合并到一次调用中：

- **Q1 — 媒体**（标题 `"Media"`）：“如何处理页面中的图片和视频？”
  - `"Ask each time (Recommended)"`——每次保存后询问
  - `"Always download"`——下载到本地 `imgs/` 和 `videos/`
  - `"Never download"`——保留远程 URL
- **Q2 — 输出**（标题 `"Output"`）：“默认输出目录？”
  - `"url-to-markdown (Recommended)"`——保存到 `./url-to-markdown/{domain}/{slug}.md`
  - 用户可以选择 `"Other"` 并输入自定义路径
- **Q3 — 保存**（标题 `"Save"`）：“将偏好设置保存到哪里？”
  - `"User (Recommended)"`——`~/.baoyu-skills/`（所有项目）
  - `"Project"`——`.baoyu-skills/`（仅此项目）

获得回答后，写入 EXTEND.md，确认 `"Preferences saved to [path]"`，然后继续。

完整模板：[references/config/first-time-setup.md](references/config/first-time-setup.md)。

### 支持的键

| 键 | 默认值 | 可选值 | 说明 |
|-----|---------|--------|-------------|
| `download_media` | `ask` | `ask` / `1` / `0` | `ask` = 每次询问，`1` = 始终下载，`0` = 从不下载 |
| `default_output_dir` | 空 | 路径或空 | 默认输出目录（空 = `./url-to-markdown/`） |

**EXTEND.md → CLI 映射**：

| EXTEND.md 键 | CLI 参数 | 备注 |
|---------------|-------------|-------|
| `download_media: 1` | `--download-media` | 要求设置 `--output` |
| `default_output_dir: ./posts/` | 智能体构造 `--output ./posts/{domain}/{slug}.md` | 路径由智能体生成，不是直接使用的标志 |

**值的优先级**：CLI 参数 → EXTEND.md → 技能默认值。

## 用法

```bash
# Default: headless capture, markdown to stdout
${READER} <url>

# Save to file
${READER} <url> --output article.md

# Save with media download
${READER} <url> --output article.md --download-media

# Wait for interaction (login/CAPTCHA) — auto-detect and continue
${READER} <url> --wait-for interaction --output article.md

# Wait for interaction — manual control (Enter to continue)
${READER} <url> --wait-for force --output article.md

# JSON output
${READER} <url> --format json --output article.json

# Force specific adapter
${READER} <url> --adapter youtube --output transcript.md
```

## 选项

| 选项 | 说明 |
|--------|-------------|
| `<url>` | 要获取的 URL |
| `--output <path>` | 输出文件路径（默认：stdout） |
| `--format <type>` | 输出格式：`markdown`（默认）或 `json` |
| `--json` | `--format json` 的简写 |
| `--adapter <name>` | 强制使用适配器：`x`、`youtube`、`hn` 或 `generic`（默认：自动检测） |
| `--headless` | 强制使用无头 Chrome（不显示窗口） |
| `--wait-for <mode>` | 交互等待模式：`none`（默认）、`interaction` 或 `force` |
| `--wait-for-interaction` | `--wait-for interaction` 的别名 |
| `--wait-for-login` | `--wait-for interaction` 的别名 |
| `--timeout <ms>` | 页面加载超时时间（默认：30000） |
| `--interaction-timeout <ms>` | 登录/CAPTCHA 等待超时时间（默认：600000 = 10 分钟） |
| `--interaction-poll-interval <ms>` | 交互检查的轮询间隔（默认：1500） |
| `--download-media` | 将图片/视频下载到本地 `imgs/` 和 `videos/`，并重写 Markdown 链接。要求设置 `--output` |
| `--media-dir <dir>` | 下载媒体的基础目录（默认：与 `--output` 所在目录相同） |
| `--cdp-url <url>` | 复用现有的 Chrome DevTools Protocol 端点 |
| `--browser-path <path>` | 自定义 Chrome/Chromium 二进制文件路径 |
| `--chrome-profile-dir <path>` | Chrome 用户数据目录（默认：`BAOYU_CHROME_PROFILE_DIR` 环境变量或 `./baoyu-skills/chrome-profile`） |
| `--debug-dir <dir>` | 写入调试产物（document.json、markdown.md、page.html、network.json） |

## 智能体质量关卡

**关键**：将默认的无头抓取结果视为临时结果。某些站点在无头模式下的渲染方式不同，可能在 CLI 未报错的情况下静默返回低质量内容。

每次无头运行后，都要检查保存的 Markdown。完整检查清单、恢复工作流和抓取模式表请参阅 [references/quality-gate.md](references/quality-gate.md)。当运行结果看起来可疑，或用户询问登录/CAPTCHA 处理方式时，请阅读该文件。

## 输出路径生成

智能体必须构造输出文件路径——`baoyu-fetch` 不会自动生成路径。

**算法**：
1. 从 EXTEND.md 的 `default_output_dir` 确定基础目录，或使用默认值 `./url-to-markdown/`
2. 从 URL 中提取域名（例如 `example.com`）
3. 根据 URL 路径或页面标题生成 slug（kebab-case，2-6 个单词）
4. 构造：`{base_dir}/{domain}/{slug}/{slug}.md`——每个 URL 使用独立目录，以确保媒体文件彼此隔离
5. 冲突解决：追加时间戳 `{slug}-YYYYMMDD-HHMMSS/{slug}-YYYYMMDD-HHMMSS.md`

将构造出的路径传给 `--output`。媒体文件（`--download-media`）会保存到 Markdown 文件旁的子目录中，使每个 URL 的资源保持自包含。

## 适配器与媒体

适配器目录（X、YouTube、Hacker News、通用页面）、各适配器注意事项、媒体下载流程（`ask` / 始终 / 从不）以及 JSON 输出结构，请参阅 [references/adapters.md](references/adapters.md)。回答特定适配器相关问题或处理媒体提示之前，请先阅读该文件。

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `BAOYU_CHROME_PROFILE_DIR` | Chrome 用户数据目录（也可以使用 `--chrome-profile-dir`） |

**故障排除**：找不到 Chrome → 使用 `--browser-path`。超时 → 增大 `--timeout`。登录/CAPTCHA → 使用 `--wait-for interaction`。调试 → 使用 `--debug-dir` 检查抓取的 HTML 和网络日志。

## 扩展支持

通过 EXTEND.md 提供自定义配置。有关路径和支持的键，请参阅上方的**偏好设置**部分。
