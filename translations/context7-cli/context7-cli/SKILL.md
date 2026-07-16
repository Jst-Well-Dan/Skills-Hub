<!-- source-sha256: d7b70ba126d9f55d7dc014f95a8264c6c402f351574317909b8c6d14b85c829d -->
---
name: context7-cli
description: 使用 ctx7 CLI 获取库文档、管理 AI 编码技能以及配置 Context7 MCP。当用户提到“ctx7”或“context7”、需要任何库的最新文档、希望安装/搜索/生成技能，或需要为其 AI 编码代理设置 Context7 时启用。
---

# ctx7 CLI

Context7 CLI 可完成三项任务：获取最新的库文档、管理 AI 编码技能，以及为你的编辑器设置 Context7 MCP。

运行命令前，请确保 CLI 已更新至最新版本：

```bash
npm install -g ctx7@latest
```

也可以不安装，直接运行：

```bash
npx ctx7@latest <command>
```

## 此技能涵盖的内容

- **[文档](references/docs.md)** — 获取任何库的最新文档。在编写代码、验证 API 签名或训练数据可能已过时时使用。
- **[技能管理](references/skills.md)** — 安装、搜索、推荐、列出、移除和生成 AI 编码技能。
- **[设置](references/setup.md)** — 为 Claude Code / Cursor / OpenCode 配置 Context7 MCP。

## 快速参考

```bash
# Documentation
ctx7 library <name> <query>           # Step 1: resolve library ID
ctx7 docs <libraryId> <query>         # Step 2: fetch docs

# Skills
ctx7 skills install /owner/repo       # Install from a repo (interactive)
ctx7 skills install /owner/repo name  # Install a specific skill
ctx7 skills search <keywords>         # Search the registry
ctx7 skills suggest                   # Auto-suggest based on project deps
ctx7 skills list                      # List installed skills
ctx7 skills remove <name>             # Uninstall a skill
ctx7 skills generate                  # Generate a custom skill with AI (requires login)

# Setup
ctx7 setup                            # Configure Context7 MCP (interactive)
ctx7 login                            # Log in for higher rate limits + skill generation
ctx7 whoami                           # Check current login status
```

## 身份验证

```bash
ctx7 login               # Opens browser for OAuth
ctx7 login --no-browser  # Prints URL instead of opening browser
ctx7 logout              # Clear stored tokens
ctx7 whoami              # Show current login status (name + email)
```

大多数命令无需登录即可使用。例外情况：`skills generate` 始终需要登录；除非传入 `--api-key` 或 `--oauth`，否则 `ctx7 setup` 也需要登录。登录还可提高文档命令的速率限制。

通过环境变量设置 API 密钥，即可完全跳过交互式登录：

```bash
export CONTEXT7_API_KEY=your_key
```

## 常见错误

- 库 ID 必须带有 `/` 前缀——应使用 `/facebook/react`，而不是 `facebook/react`
- 始终先运行 `ctx7 library`——如果没有有效 ID，`ctx7 docs react "hooks"` 将会失败
- 技能的仓库格式为 `/owner/repo`——例如 `ctx7 skills install /anthropics/skills`
- `skills generate` 需要登录——请先运行 `ctx7 login`
