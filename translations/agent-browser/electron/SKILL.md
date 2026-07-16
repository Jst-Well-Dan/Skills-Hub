<!-- source-sha256: d97a2bc221b5044184ad0af51376b07bcb94f259622f2af254fb3701e6f01861 -->
---
name: electron
description: 使用 agent-browser 通过 Chrome DevTools Protocol 自动化 Electron 桌面应用（VS Code、Slack、Discord、Figma、Notion、Spotify 等）。当用户需要与 Electron 应用交互、自动化桌面应用、连接到正在运行的应用、控制原生应用或测试 Electron 应用程序时使用。触发场景包括“自动化 Slack 应用”“控制 VS Code”“与 Discord 应用交互”“测试此 Electron 应用”“连接到桌面应用”，或任何需要自动化原生 Electron 应用程序的任务。
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Electron 应用自动化

使用 agent-browser 自动化任何 Electron 桌面应用。Electron 应用基于 Chromium 构建，并会暴露一个 agent-browser 可连接的 Chrome DevTools Protocol（CDP）端口，从而能够使用与网页相同的“快照—交互”工作流。

## 核心工作流

1. **启动**启用了远程调试的 Electron 应用
2. **连接** agent-browser 到 CDP 端口
3. **生成快照**以发现可交互元素
4. 使用元素引用进行**交互**
5. 在导航或状态更改后**重新生成快照**

```bash
# 启动启用了远程调试的 Electron 应用
open -a "Slack" --args --remote-debugging-port=9222

# 将 agent-browser 连接到应用
agent-browser connect 9222

# 从这里开始使用标准工作流
agent-browser snapshot -i
agent-browser click @e5
agent-browser screenshot slack-desktop.png
```

## 使用 CDP 启动 Electron 应用

由于 `--remote-debugging-port` 标志内置于 Chromium，因此每个 Electron 应用都支持该标志。

### macOS

```bash
# Slack
open -a "Slack" --args --remote-debugging-port=9222

# VS Code
open -a "Visual Studio Code" --args --remote-debugging-port=9223

# Discord
open -a "Discord" --args --remote-debugging-port=9224

# Figma
open -a "Figma" --args --remote-debugging-port=9225

# Notion
open -a "Notion" --args --remote-debugging-port=9226

# Spotify
open -a "Spotify" --args --remote-debugging-port=9227
```

### Linux

```bash
slack --remote-debugging-port=9222
code --remote-debugging-port=9223
discord --remote-debugging-port=9224
```

### Windows

```bash
"C:\Users\%USERNAME%\AppData\Local\slack\slack.exe" --remote-debugging-port=9222
"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe" --remote-debugging-port=9223
```

**重要：**如果应用已经在运行，请先退出，然后使用该标志重新启动。启动时必须包含 `--remote-debugging-port` 标志。

## 连接

```bash
# 连接到指定端口
agent-browser connect 9222

# 或在每条命令中使用 --cdp
agent-browser --cdp 9222 snapshot -i

# 自动发现正在运行的 Chromium 应用
agent-browser --auto-connect snapshot -i
```

执行 `connect` 后，所有后续命令都会以已连接的应用为目标，无需再指定 `--cdp`。

## 标签页管理

Electron 应用通常包含多个窗口或 webview。使用标签页命令列出并在它们之间切换：

```bash
# 列出所有可用目标（窗口、webview 等）
agent-browser tab

# 按索引切换到指定标签页
agent-browser tab 2

# 按 URL 模式切换
agent-browser tab --url "*settings*"
```

## Webview 支持

Electron `<webview>` 元素会被自动发现，并且可以像普通页面一样进行控制。Webview 会作为独立目标出现在标签页列表中，并带有 `type: "webview"`：

```bash
# 连接到正在运行的 Electron 应用
agent-browser connect 9222

# 列出目标——webview 会与页面一起显示
agent-browser tab
# 示例输出：
#   0: [page]    Slack - Main Window     https://app.slack.com/
#   1: [webview] Embedded Content        https://example.com/widget

# 切换到 webview
agent-browser tab 1

# 正常与 webview 交互
agent-browser snapshot -i
agent-browser click @e3
agent-browser screenshot webview.png
```

**注意：**Webview 支持通过原始 CDP 连接实现。

## 常见模式

### 检查应用并进行导航

```bash
open -a "Slack" --args --remote-debugging-port=9222
sleep 3  # 等待应用启动
agent-browser connect 9222
agent-browser snapshot -i
# 阅读快照输出以识别 UI 元素
agent-browser click @e10  # 导航到某个区域
agent-browser snapshot -i  # 导航后重新生成快照
```

### 截取桌面应用的屏幕截图

```bash
agent-browser connect 9222
agent-browser screenshot app-state.png
agent-browser screenshot --full full-app.png
agent-browser screenshot --annotate annotated-app.png
```

### 从桌面应用中提取数据

```bash
agent-browser connect 9222
agent-browser snapshot -i
agent-browser get text @e5
agent-browser snapshot --json > app-state.json
```

### 在桌面应用中填写表单

```bash
agent-browser connect 9222
agent-browser snapshot -i
agent-browser fill @e3 "search query"
agent-browser press Enter
agent-browser wait 1000
agent-browser snapshot -i
```

### 同时运行多个应用

使用命名会话同时控制多个 Electron 应用：

```bash
# 连接到 Slack
agent-browser --session slack connect 9222

# 连接到 VS Code
agent-browser --session vscode connect 9223

# 分别与每个应用交互
agent-browser --session slack snapshot -i
agent-browser --session vscode snapshot -i
```

## 配色方案

通过 CDP 连接时，默认配色方案可能为 `light`。若要保留深色模式：

```bash
agent-browser connect 9222
agent-browser --color-scheme dark snapshot -i
```

或者进行全局设置：

```bash
AGENT_BROWSER_COLOR_SCHEME=dark agent-browser connect 9222
```

## 故障排除

### “Connection refused”或“Cannot connect”

- 确保应用是使用 `--remote-debugging-port=NNNN` 启动的
- 如果应用已经在运行，请退出并使用该标志重新启动
- 检查端口是否被其他进程占用：`lsof -i :9222`

### 应用已启动，但连接失败

- 启动后等待几秒再连接（`sleep 3`）
- 某些应用需要一些时间来初始化其 webview

### 元素未出现在快照中

- 应用可能使用了多个 webview。使用 `agent-browser tab` 列出目标并切换到正确的目标

### 无法在输入字段中输入

- 尝试使用 `agent-browser keyboard type "text"`，无需选择器即可在当前焦点位置输入
- 某些 Electron 应用使用自定义输入组件；使用 `agent-browser keyboard inserttext "text"` 绕过按键事件

## 支持的应用

任何基于 Electron 构建的应用都可以使用，包括：

- **通信：**Slack、Discord、Microsoft Teams、Signal、Telegram Desktop
- **开发：**VS Code、GitHub Desktop、Postman、Insomnia
- **设计：**Figma、Notion、Obsidian
- **媒体：**Spotify、Tidal
- **效率工具：**Todoist、Linear、1Password

如果应用基于 Electron 构建，它就支持 `--remote-debugging-port`，并且可以使用 agent-browser 实现自动化。
