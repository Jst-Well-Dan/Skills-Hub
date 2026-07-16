<!-- source-sha256: 290c0f8b3957a21de068f8732f324aa6c05a72bc2bf23f962fe9fa874b2c0271 -->
---
name: baoyu-danger-gemini-web
description: 通过逆向工程的 Gemini Web API 生成图像和文本。支持文本生成、根据提示词生成图像、使用参考图像作为视觉输入，以及多轮对话。当其他技能需要图像生成后端，或用户请求“使用 Gemini 生成图像”“Gemini 文本生成”，或需要具备视觉能力的 AI 生成时使用。
version: 1.56.2
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-danger-gemini-web
    requires:
      anyBins:
        - bun
        - npx
---

# Gemini Web 客户端

通过 Gemini Web API 生成文本/图像。支持参考图像和多轮对话。

## 用户输入工具

当此技能向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具**，即当前智能体运行时提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果不存在此类工具，则发送带编号的纯文本消息，并要求用户针对每个问题回复所选编号/答案。
3. **批量提问**：如果工具支持单次调用提出多个问题，请将所有适用问题合并到一次调用中；如果仅支持单个问题，则按优先级顺序逐一提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行时中请替换为本地等效工具。

## 脚本目录

**重要**：所有脚本均位于此技能的 `scripts/` 子目录中。

**智能体执行说明**：
1. 确定此 SKILL.md 文件的目录路径，并记为 `{baseDir}`
2. 脚本路径 = `{baseDir}/scripts/<script-name>.ts`
3. 解析 `${BUN_X}` 运行时：如果已安装 `bun` → `bun`；如果 `npx` 可用 → `npx -y bun`；否则建议安装 bun
4. 将本文档中的所有 `{baseDir}` 和 `${BUN_X}` 替换为实际值

**脚本参考**：
| 脚本 | 用途 |
|--------|---------|
| `scripts/main.ts` | 用于生成文本/图像的 CLI 入口点 |
| `scripts/gemini-webapi/*` | `gemini_webapi` 的 TypeScript 移植版（GeminiClient、类型、工具函数） |

## 同意检查（必需）

首次使用前，请确认用户同意使用逆向工程 API。

**同意文件位置**：
- macOS：`~/Library/Application Support/baoyu-skills/gemini-web/consent.json`
- Linux：`~/.local/share/baoyu-skills/gemini-web/consent.json`
- Windows：`%APPDATA%\baoyu-skills\gemini-web\consent.json`

**流程**：
1. 检查同意文件是否存在，并包含 `accepted: true` 和 `disclaimerVersion: "1.0"`
2. 如果存在有效同意记录 → 输出包含 `acceptedAt` 日期的警告，然后继续
3. 如果没有同意记录 → 显示免责声明，并通过 `AskUserQuestion` 询问用户：
   - “是，我接受” → 创建包含 ISO 时间戳的同意文件，然后继续
   - “否，我拒绝” → 输出拒绝消息并停止
4. 同意文件格式：`{"version":1,"accepted":true,"acceptedAt":"<ISO>","disclaimerVersion":"1.0"}`

---

## 偏好设置（EXTEND.md）

按优先级顺序检查 EXTEND.md——以找到的第一个为准：

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-danger-gemini-web/EXTEND.md` | 项目 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-danger-gemini-web/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-danger-gemini-web/EXTEND.md` | 用户主目录 |

如果均未找到，则使用默认设置。

**EXTEND.md 支持**：默认模型、代理设置、自定义数据目录。

## 用法

```bash
# 文本生成
${BUN_X} {baseDir}/scripts/main.ts "Your prompt"
${BUN_X} {baseDir}/scripts/main.ts --prompt "Your prompt" --model gemini-3-flash

# 图像生成
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cute cat" --image cat.png
${BUN_X} {baseDir}/scripts/main.ts --promptfiles system.md content.md --image out.png

# 视觉输入（参考图像）
${BUN_X} {baseDir}/scripts/main.ts --prompt "Describe this" --reference image.png
${BUN_X} {baseDir}/scripts/main.ts --prompt "Create variation" --reference a.png --image out.png

# 多轮对话
${BUN_X} {baseDir}/scripts/main.ts "Remember: 42" --sessionId session-abc
${BUN_X} {baseDir}/scripts/main.ts "What number?" --sessionId session-abc

# JSON 输出
${BUN_X} {baseDir}/scripts/main.ts "Hello" --json
```

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--prompt`, `-p` | 提示文本 |
| `--promptfiles` | 从文件中读取提示内容（拼接） |
| `--model`, `-m` | 模型：gemini-3-pro（默认）、gemini-3-flash、gemini-3-flash-thinking、gemini-3.1-pro-preview |
| `--image [path]` | 生成图像（默认：generated.png） |
| `--reference`, `--ref` | 用于视觉输入的参考图像 |
| `--sessionId` | 多轮对话的会话 ID |
| `--list-sessions` | 列出已保存的会话 |
| `--json` | 以 JSON 格式输出 |
| `--login` | 刷新 Cookie，然后退出 |
| `--cookie-path` | 自定义 Cookie 文件路径 |
| `--profile-dir` | Chrome 配置文件目录 |

## 模型

| 模型 | 说明 |
|-------|-------------|
| `gemini-3-pro` | 默认模型，最新的 3.0 Pro |
| `gemini-3-flash` | 快速、轻量的 3.0 Flash |
| `gemini-3-flash-thinking` | 具备思考能力的 3.0 Flash |
| `gemini-3.1-pro-preview` | 3.1 Pro 预览版（空请求头，自动路由） |

## 身份验证

首次运行时会打开浏览器进行 Google 身份验证。Cookie 会自动缓存。

如果未显式设置配置文件目录，刷新 Cookie 时可能会复用已在运行的本地 Chrome/Chromium 调试会话，该会话关联标准用户数据目录。
设置 `--profile-dir` 或 `GEMINI_WEB_CHROME_PROFILE_DIR` 可强制使用专用配置文件，并跳过现有会话复用。
这是一个尽力而为的 CDP 会话复用路径，并非 Chrome 官方文档中描述的基于 Chrome DevTools MCP 提示的 `--autoConnect` 流程。

支持的浏览器（自动检测）：Chrome、Chrome Canary/Beta、Chromium、Edge。

强制刷新：使用 `--login` 标志。覆盖浏览器：使用 `GEMINI_WEB_CHROME_PATH` 环境变量。

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `GEMINI_WEB_DATA_DIR` | 数据目录 |
| `GEMINI_WEB_COOKIE_PATH` | Cookie 文件路径 |
| `GEMINI_WEB_CHROME_PROFILE_DIR` | Chrome 配置文件目录 |
| `GEMINI_WEB_CHROME_PATH` | Chrome 可执行文件路径 |
| `HTTP_PROXY`, `HTTPS_PROXY` | 用于访问 Google 的代理（与命令内联设置） |

## 会话

会话文件存储在数据目录下的 `sessions/<id>.json` 中。

包含：`id`、`metadata`（Gemini 聊天状态）、`messages` 数组、时间戳。

## 扩展支持

可通过 EXTEND.md 提供自定义配置。路径和支持的选项请参阅**偏好设置**部分。
