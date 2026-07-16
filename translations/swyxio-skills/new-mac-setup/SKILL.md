<!-- source-sha256: c3e0749290c7d48c0f8da65f76387916d31dc1e410e2ed10809fea36032eb636 -->
---
name: new-mac-setup
description: |
  面向全栈 Web 开发者和 AI 工程师的全自动新 Mac 配置。生成并执行幂等 Shell 脚本，通过 Homebrew、fnm、uv 和 defaults 命令安装开发工具、CLI 实用程序、GUI 应用、AI/ML 工具、Shell 配置和 macOS 偏好设置。只要有人说“配置我的 Mac”“新 Mac 配置”“配置我的开发机器”“安装我的开发工具”“全新安装 Mac”“开发环境配置”，或提到任何为开发用途初始化 macOS 机器的内容，就使用此技能。当有人提到在新 Mac 上配置 Homebrew、Oh-My-ZSH、Node.js、Python、Docker 或终端配置时，也应触发此技能——即使他们没有将其称为“配置”。此技能具有明确的偏好取向，基于为全栈 JS/TS + Python + AI 开发配置 M 系列 Mac 的真实经验。
license: MIT
compatibility: |
  需要搭载 Apple Silicon（M1/M2/M3/M4）的 macOS。脚本使用 Homebrew，由其处理所有依赖项。Bash 3.2+（macOS 自带）。下载软件包需要互联网连接。
metadata:
  author: swyxio
  version: "2.0"
  last-updated: "2026-05-20"
  hardware: Apple Silicon (M-series)
  primary-stack: TypeScript, Python, AI/ML
---

# 新 Mac 配置

此技能会为全栈 Web 开发和 AI 工程生成并运行一套完整、幂等的 Mac 配置。它会生成 8 个 Shell 脚本，这些脚本既可单独运行，也可通过主运行脚本执行；此外还包括 dotfiles 和 macOS 偏好设置自动化。

这些脚本可重复运行——在尝试安装之前，它们会检查每个工具是否已经安装，因此即使中途出现故障，你也可以放心地重新运行它们。

## 设计理念

此配置具有明确的偏好取向。核心观点如下：

- **终端**：Ghostty（快速、GPU 加速、使用 Zig）+ cmux（垂直标签页、拆分窗格、供 AI 智能体使用的 Socket API）。cmux 会读取 Ghostty 的配置，因此两者共用一个配置文件。
- **Shell**：使用 Oh-My-ZSH、powerlevel10k 主题、zsh-autosuggestions 和 zsh-syntax-highlighting 的 ZSH
- **Node**：fnm（不使用 nvm——fnm 更快），并使用 pnpm 和 bun 进行软件包管理/运行
- **Python**：Astral 的 uv（不使用 pyenv、pip 或 conda——uv 快得多，并且可同时处理虚拟环境和软件包安装）
- **Docker**：Colima（不使用 Docker Desktop——更轻量、原生支持 CLI、免费）
- **编辑器**：Cursor（AI 原生编辑器）
- **AI 工具**：Claude Code、Codex CLI、Antigravity CLI（通过 `antigravity` Homebrew cask 提供 `agy`）、Railway CLI，以及用于本地模型的 Ollama
- **智能体通知**：Claude Code、Codex 和 Cursor 共用 peon-ping，并经过调整，仅在有用时发出通知
- **浏览器**：Dia（来自 The Browser Company，是 Arc 的继任者）
- **启动器**：Raycast（替代 Alfred、Spotlight、Caffeine 和窗口管理工具）
- **语音**：用于语音转文字的 Wispr Flow
- **截图**：默认使用 Shottr（包含 OCR）；同时推荐 [Screendrop](https://github.com/fayazara/Screendrop)，它采用本地优先设计，支持截图/录屏、标注、捕获历史记录和可选的 Cloudflare 支持分享。

## 如何使用此技能

### 第 1 步：询问用户

在生成脚本之前，询问用户几个问题以定制配置。需要了解的关键信息：

1. **Git 身份信息**：用于 `git config` 的姓名和电子邮件
2. **硬件**：哪款 Mac / 内存多大？（影响要拉取哪些 Ollama 模型）
3. **要跳过的内容**：他们想要安装所有内容，还是应排除某些类别？（例如“不安装 Elixir”“不安装 PostgreSQL”“我使用 Docker Desktop，不使用 Colima”）
4. **额外内容**：默认列表中是否缺少他们需要的应用或工具？
5. **终端偏好**：默认使用 Ghostty + cmux，但他们可能想使用其他工具

基于内存的 Ollama 模型建议：
- **8GB**：qwen3.5:4b、qwen2.5-coder:3b
- **16GB**：qwen3.5:9b、qwen2.5-coder:7b
- **24GB**：qwen3.5:27b、qwen2.5-coder:14b（最佳平衡点）
- **32GB+**：qwen3.5:35b、qwen2.5-coder:32b

### 第 2 步：生成脚本

在用户选择的目录中生成 8 个脚本。每个脚本都可独立运行且具有幂等性。以 `scripts/` 中的模板为基础，根据用户的回答进行定制。

脚本应按以下顺序运行：

```
01-xcode-and-homebrew.sh   # Xcode CLI 工具 + Homebrew（15-25 分钟）
02-shell-setup.sh          # Oh-My-ZSH + 插件 + 字体
03-brew-packages.sh        # 所有 brew formulae + cask 应用
04-dev-environment.sh      # Node (fnm)、Python (uv)、Git、Docker
05-ai-tools.sh             # Claude Code、Codex CLI、Antigravity CLI、Ollama 模型、llama.cpp
06-dotfiles.sh             # .zshrc + Ghostty 配置
07-macos-settings.sh       # 通过 defaults 命令配置系统偏好设置
00-run-all.sh              # 主运行脚本（按顺序运行 01-07）
```

### 第 3 步：执行

如果可能，直接执行这些脚本。如果运行环境是无法访问用户 Mac 的 VM/沙盒，则将脚本写入工作区文件夹，并将以下单行命令放入剪贴板：

```bash
cd /path/to/scripts && chmod +x ./*.sh && bash ./00-run-all.sh
```

## 经验教训（需要避免的错误）

以下是测试期间遇到的真实问题。`scripts/` 中的脚本已经包含这些修复，但如果你要生成全新的脚本，请牢记：

1. **在 npm 能够正常工作之前，需要先加载 fnm。** 通过 fnm 安装 Node 后，当前 Shell 的 PATH 中还没有 `npm`，直到运行 `eval "$(fnm env --use-on-cd)"`。每个使用 npm/node 的脚本都必须先加载 fnm。

2. **不要在主运行脚本中使用 `set -e`。** 如果某个脚本失败（例如某个 brew cask 返回 404），`set -e` 会终止整个流水线。如果单个脚本能够妥善处理错误，则可以使用 `set -e`，但主运行脚本不应使用。

3. **在主运行脚本中加载 brew 和 fnm。** 在 `00-run-all.sh` 顶部附近添加以下内容，以便所有子脚本继承它们：
   ```bash
   eval "$(/opt/homebrew/bin/brew shellenv)" 2>/dev/null || true
   eval "$(fnm env --use-on-cd)" 2>/dev/null || true
   ```

4. **智能引号会破坏 Shell 命令。** 如果将命令写入剪贴板，请避免使用弯引号/智能引号。仅使用简单的 ASCII 引号，或者尽可能完全避免使用引号。最安全的剪贴板命令是单个简单语句，例如 `bash ./07-macos-settings.sh`。

5. **Zoom 和某些 cask 需要 sudo。** Zoom 安装程序会触发 `Password:` 提示。需要提醒用户，某些 cask 安装过程会暂停并要求输入密码。

6. 如果 Node 由 fnm（而非 brew）管理，则需要使用 **brew install yarn --ignore-dependencies**。否则，brew 会尝试安装自己的 Node 作为 yarn 的依赖项。

7. **Ghostty 配置位置**：`~/.config/ghostty/config`。cmux 会读取同一个文件。

## 默认软件包列表

### Homebrew Formulae（CLI 工具）

```
# 核心开发工具
gh, git, fnm, pnpm, bun, z, diff-so-fancy

# 语言与运行时
elixir, erlang, python@3.13

# Docker（不使用 Docker Desktop）
colima, docker, docker-completion

# 媒体与处理
ffmpeg, yt-dlp, tesseract

# 构建依赖项
openssl@3, readline, sqlite, xz, zstd

# 数据库
postgresql@14, rabbitmq

# 其他 CLI
honcho, pipx, flyctl, entr, tig, mas, terminal-notifier, googleworkspace-cli

# Google Workspace
googleworkspace-cli 会安装 `gws` 二进制文件；身份验证仍需执行 `gws auth setup` 和 `gws auth login`。

# 库
cairo, glib, harfbuzz, libvmaf, webp
```

### Homebrew Casks（GUI 应用）

```
# 终端
ghostty

# 编辑器
cursor, visual-studio-code

# 浏览器
thebrowsercompany-dia

# 通信
slack, discord, zoom

# 生产力工具
raycast, rectangle, obsidian, notion, notion-calendar

# AI 与 ML
ollama, antigravity

# 媒体
vlc, audacity, tella, descript

# 实用工具
shottr, notunes, caffeine, stretchly, quickshade, pure-paste, 1password

# 开发工具
beeper, superhuman, gcloud-cli
```

另外通过以下命令安装 cmux：`brew tap manaflow-ai/cmux && brew install --cask cmux`

`gcloud-cli` 会安装 Google Cloud CLI（`gcloud`）。请将 `/opt/homebrew/share/google-cloud-sdk/bin` 保留在 PATH 中，以便安装后可以使用其他 SDK 组件。

## Claude 建议添加的工具（2026 年 3 月）

这些工具由 Claude 在初始配置会话期间提出，并被用户接受。它们现在已成为 `03-brew-packages.sh` 默认安装的一部分：

1. **fzf** — 模糊查找器，可彻底改善 Shell 历史记录（Ctrl+R）、文件搜索和 Git 分支选择。与 zsh-autosuggestions 完美搭配。`brew install fzf`
2. **ripgrep**（`rg`）— 快如闪电的 grep 替代工具。遵循 .gitignore，默认递归搜索。对任何开发者都不可或缺。`brew install ripgrep`
3. **bat** — 带有语法高亮、行号和 Git 集成的 `cat`。让在终端中阅读代码文件更加美观。`brew install bat`
4. **zoxide** — 可直接替代 `z`，具有更智能的频率与新近度算法和模糊匹配功能。操作习惯相同，结果更好。`brew install zoxide`
5. **Orbstack** — 用于 Docker 容器和 Linux VM，甚至比 Colima 更轻量。拥有友好的 GUI，且几乎可以即时启动。`brew install --cask orbstack`

### 全局 npm 软件包

```
undollar, npm-check-updates, trash-cli,
@anthropic-ai/claude-code, @openai/codex, @railway/cli
```

### Antigravity CLI

通过 Homebrew 安装 Google Antigravity：

```bash
brew install --cask antigravity
```

该 cask 会安装桌面应用，并将 `agy` 作为 Antigravity CLI 提供。对于新配置，应优先选择它而不是 Gemini CLI：Google 于 2026 年 5 月 19 日宣布，面向免费用户、Google AI Pro 用户和 Ultra 用户的 Gemini CLI 消费者访问权限将于 2026 年 6 月 18 日停止处理请求。企业版和使用付费 API 密钥的 Gemini CLI 访问权限仍可继续使用，但这套新 Mac 配置路径应默认使用 Antigravity CLI。

### peon-ping 默认设置

在新 Mac 上配置 AI 工具时，还应使用以下默认设置安装并配置 `peon-ping`：

- 使用 `~/.claude/hooks/peon-ping/` 下的共享运行时进行全局安装，使 Claude Code、Codex 和 Cursor 可以共用同一安装。
- 通过安装程序正常注册 Claude Code 钩子。
- 在 `~/.codex/config.toml` 中手动注册 Codex：
  ```toml
  notify = ["bash", "/Users/$USER/.claude/hooks/peon-ping/adapters/codex.sh"]
  ```
- 如果 `~/.cursor/` 存在，则保持 Cursor 的钩子连接。
- 使用 `default_pack: "peon"` 作为备用包。
- 安装以下轮换池：
  `glados`, `jarvis`, `r2d2`, `peasant`, `sc_kerrigan`, `sc_scv`, `sc_marine`, `sc_raynor`, `sc_ghost`, `sc_terran`, `protoss`, `sc2_alarak`, `sc2_abathur`, `ra2_eva_commander`, `ra2_kirov`, `ra2_yuri`, `ra_soviet`, `ccg_gla_worker`, `ccg_us_dozer`, `ccg_china_dozer`
- 将 `pack_rotation_mode` 设置为 `round-robin`。
- 将 `volume` 设置为 `0.2`。
- 保持启用 `desktop_notifications`，但使用 `notification_style: "standard"`，而不是大型浮层。
- 通过 Homebrew 安装 `terminal-notifier`，确保标准 macOS 通知可靠工作并支持点击聚焦行为。
- 设置 `suppress_sound_when_tab_focused: true`。
- 设置 `silent_window_seconds: 30`，使 `task.complete` 仅针对运行时间较长的工作触发。
- 类别：
  - `session.start: false`
  - `task.acknowledge: false`
  - `task.complete: true`
  - `task.error: true`
  - `input.required: true`
  - `resource.limit: true`
  - `user.spam: false`
- 目标：仅针对真正需要注意的事件发出提醒，并且只为耗时足以值得关注的工作播放完成音效。

### Ollama 模型（适用于 24GB 内存）

```
qwen3.5:27b                    # 通用（256K 上下文，多模态）
qwen2.5-coder:14b              # 专注代码
deepseek-r1:8b                 # 推理
```

### macOS 默认设置（自动化）

```bash
# Finder：显示扩展名、显示隐藏文件、显示路径栏、使用列表视图
# Dock：自动隐藏、不显示最近项目、无延迟、最小化至应用图标
# 键盘：关闭自动更正、关闭智能引号、快速重复、关闭按住按键弹出菜单
# 触控板：关闭自然滚动、轻点来点按
# 截图：PNG、保存到桌面、无阴影
# 菜单栏：自动隐藏
```

### macOS 设置（手动——指导用户操作）

以下设置无法通过 `defaults write` 自动完成：
1. Spotlight：除“应用程序”+“系统设置”外全部禁用
2. Siri：禁用
3. 截图快捷键：重新映射为 Cmd+E
4. Cmd+Q：重新映射为双击（防止意外退出）
5. 触控板：禁用词典查询
6. Finder：将新窗口位置设置为 ~/Work
7. Dock：移除除 Finder 和废纸篓以外的所有图标
8. 光标大小：在辅助功能中设置为大号（适合演示）

## 需要手动下载的应用

以下应用不在 Homebrew 中或需要手动安装：
- [Wispr Flow](https://wispr.com) — 语音转文字（2025 年推荐）
- [SuperWhisper](https://superwhisper.com) — 语音转文字（2024 年推荐，仍然很好用）
- [Screendrop](https://github.com/fayazara/Screendrop) — 本地优先的截图、录屏、标注、捕获历史记录和可选的 Cloudflare 支持分享；建议与 Shottr 搭配使用
- [Screenflow 11](https://www.telestream.net/screenflow/) — 屏幕录制
- [Tella.tv](https://www.tella.tv/) — 屏幕录制；首选的 Loom 替代品
- [App Quitter](https://appquitter.com) — 窗口关闭时退出应用
- [Clipbook](https://clipbook.app) 或 Alfred — 剪贴板管理器

## 安装后：打开需要登录的应用

所有脚本完成后，打开以下应用进行登录和配置。此技能应为用户自动打开这些应用：

```bash
# 安装后需要登录/激活的应用
open -a "Slack"
open -a "Discord"
open -a "Raycast"
open -a "Shottr"
open -a "1Password"
open -a "Spotify"
open -a "Zoom"
open -a "Dia"
open -a "GitHub Desktop" 2>/dev/null
open -a "Claude" 2>/dev/null
echo "🔑 请登录上面的每个应用，然后继续配置。"
```

## 浏览器扩展（安装到 Dia/Chrome）

必备：
- uBlock Origin、Privacy Badger、Video Speed Controller（强烈推荐）
- Refined GitHub、React Developer Tools、Code Copy
- 1Password / LastPass

锦上添花：
- Morpheon Dark、bypass-paywalls-chrome、Twitter-Links-beta
- enhanced-history、Display Anchors、Octolinker、little-rat、RescueTime

## 建议添加的工具

以下工具不在原始博客文章中，但值得考虑，并且与此配置相得益彰：

1. **mise**（mise.jdx.dev）— 用于 Node、Python、Ruby、Go 等的通用版本管理器。可在版本管理方面替代 fnm + uv（swyx 曾提到正在探索此工具）
2. **zoxide** — 带模糊匹配功能的更智能 `z` 替代工具
3. **bat** — 带语法高亮的 `cat` 替代工具
4. **eza** — 现代化的 `ls` 替代工具
5. **fd** — 更快的 `find` 替代工具
6. **ripgrep** — 更快的 `grep`（rg）
7. **fzf** — 用于 Shell 历史记录、文件等一切内容的模糊查找器
8. **starship** — 跨 Shell 提示符（powerlevel10k 的替代方案，也适用于 fish）
9. **Bartender** 或 **Ice** — 菜单栏图标管理（减少杂乱）
11. **Hand Mirror** — 从菜单栏快速检查摄像头（通话前非常实用）
12. **Tailscale** — 用于访问家中机器的网状 VPN
13. **Orbstack** — 另一个 Docker Desktop 替代方案（甚至比 Colima 更轻量）
14. **Aerospace** — 平铺式窗口管理器（当 Rectangle 不够用时）

## Dotfiles 参考

.zshrc 应包含：
- 使用 powerlevel10k 主题的 Oh-My-ZSH
- 插件：git、zsh-autosuggestions、zsh-syntax-highlighting、z
- Homebrew、fnm 和 uv PATH 配置
- z 目录跳转的 source 配置
- Git 别名（gs、gd、gc、gp、gl、gco、gcb）
- npm/pnpm 别名（ni、nr、pi、pr、ncu）
- Python 别名（pip → uv pip、venv → uv venv）
- Docker 别名（dstart → colima start、dstop → colima stop）
- 将编辑器设置为 Cursor

Ghostty 配置应包含：
- 字体：14pt 的 "Meslo LG M for Powerline"
- 主题：dark:GruvboxDark,light:GruvboxLight
- Shell 集成：zsh
- 块状光标，不闪烁
- 全局快捷键：Cmd+`，用于快速打开终端
- 启用剪贴板读写
- 输入时隐藏鼠标
