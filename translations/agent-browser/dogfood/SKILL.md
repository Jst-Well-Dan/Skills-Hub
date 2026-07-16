<!-- source-sha256: c86db6b33c8f92e2a074d7f5b7eb9629e333d0fb287eca4421782266b1e76257 -->
---
name: dogfood
description: 系统化探索并测试 Web 应用程序，以发现缺陷、用户体验问题及其他问题。当用户要求“dogfood”“QA”“探索性测试”“查找问题”“缺陷搜寻”“测试此应用/网站/平台”或评审 Web 应用程序质量时使用。生成包含完整复现证据的结构化报告——包括分步截图、复现视频，以及每个问题的详细复现步骤——以便将发现直接移交给负责团队。
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Dogfood

系统化探索 Web 应用程序，发现问题，并为每项发现生成包含完整复现证据的报告。

## 设置

只需提供**目标 URL**。其他所有参数均有合理的默认值——除非用户明确要求覆盖，否则请使用默认值。

| 参数 | 默认值 | 覆盖示例 |
|-----------|---------|-----------------|
| **目标 URL** | _（必填）_ | `vercel.com`、`http://localhost:3000` |
| **会话名称** | 将域名转换为 slug（例如，`vercel.com` -> `vercel-com`） | `--session my-session` |
| **输出目录** | `./dogfood-output/` | `输出目录：/tmp/qa` |
| **范围** | 完整应用 | `重点测试计费页面` |
| **身份验证** | 无 | `登录 user@example.com` |

如果用户说类似“dogfood vercel.com”的话，请立即使用默认值开始。除非提到了身份验证但缺少凭据，否则不要提出澄清问题。

始终直接使用 `agent-browser`——切勿使用 `npx agent-browser`。直接运行的二进制文件使用快速的 Rust 客户端。`npx` 会通过 Node.js 路由，速度明显更慢。

## 工作流程

```
1. 初始化      设置会话、输出目录和报告文件
2. 身份验证    如有需要则登录并保存状态
3. 熟悉应用    导航至起点并获取初始快照
4. 探索        系统化访问页面并测试功能
5. 记录        发现每个问题时进行截图和录制
6. 收尾        更新汇总数量并关闭会话
```

### 1. 初始化

```bash
mkdir -p {OUTPUT_DIR}/screenshots {OUTPUT_DIR}/videos
```

将报告模板复制到输出目录并填写标题字段：

```bash
cp {SKILL_DIR}/templates/dogfood-report-template.md {OUTPUT_DIR}/report.md
```

启动一个命名会话：

```bash
agent-browser --session {SESSION} open {TARGET_URL}
agent-browser --session {SESSION} wait --load networkidle
```

### 2. 身份验证

如果应用要求登录：

```bash
agent-browser --session {SESSION} snapshot -i
# 识别登录表单引用并填写凭据
agent-browser --session {SESSION} fill @e1 "{EMAIL}"
agent-browser --session {SESSION} fill @e2 "{PASSWORD}"
agent-browser --session {SESSION} click @e3
agent-browser --session {SESSION} wait --load networkidle
```

对于 OTP/电子邮件验证码：向用户询问，等待其回复，然后输入验证码。

成功登录后，保存状态以供后续复用：

```bash
agent-browser --session {SESSION} state save {OUTPUT_DIR}/auth-state.json
```

### 3. 熟悉应用

获取初始标注截图和快照，以了解应用结构：

```bash
agent-browser --session {SESSION} screenshot --annotate {OUTPUT_DIR}/screenshots/initial.png
agent-browser --session {SESSION} snapshot -i
```

识别主要导航元素，并列出需要访问的各个部分。

### 4. 探索

阅读 [references/issue-taxonomy.md](references/issue-taxonomy.md)，了解需要查找的完整问题列表和探索检查清单。

**策略——系统化检查整个应用：**

- 从主导航开始。访问每个顶层部分。
- 在每个部分中测试交互元素：点击按钮、填写表单、打开下拉菜单/模态框。
- 检查边界情况：空状态、错误处理、边界输入。
- 尝试真实的端到端工作流（创建、编辑、删除流程）。
- 定期检查浏览器控制台是否有错误。

**在每个页面中：**

```bash
agent-browser --session {SESSION} snapshot -i
agent-browser --session {SESSION} screenshot --annotate {OUTPUT_DIR}/screenshots/{page-name}.png
agent-browser --session {SESSION} errors
agent-browser --session {SESSION} console
```

自行判断探索深度。将更多时间投入核心功能，减少在次要页面上花费的时间。如果在某一区域发现一组问题，请深入调查。

### 5. 记录问题（复现优先）

步骤 4 和步骤 5 同时进行——在一次流程中完成探索和记录。发现问题时，请停止探索并立即记录，然后再继续。不要先探索完整个应用，之后再统一记录。

每个问题都必须可复现。发现异常时，不要只是记下来——要用证据证明。目标是让阅读报告的人能够准确看到发生了什么，并重现整个过程。

**根据问题选择合适的证据级别：**

#### 交互/行为问题（功能、用户体验、操作触发的控制台错误）

这些问题需要用户交互才能复现——请使用包含视频和分步截图的完整复现过程：

1. **开始录制复现视频**，并确保在复现问题_之前_开始：

```bash
agent-browser --session {SESSION} record start {OUTPUT_DIR}/videos/issue-{NNN}-repro.webm
```

2. **以符合人类观看习惯的速度执行步骤。** 每次操作之间暂停 1-2 秒，使视频易于观看。每一步都要截图：

```bash
agent-browser --session {SESSION} screenshot {OUTPUT_DIR}/screenshots/issue-{NNN}-step-1.png
sleep 1
# 执行操作（点击、填写等）
sleep 1
agent-browser --session {SESSION} screenshot {OUTPUT_DIR}/screenshots/issue-{NNN}-step-2.png
sleep 1
# ……继续操作，直到问题出现
```

3. **捕获异常状态。** 暂停片刻，让观看者能够看清，然后获取一张标注截图：

```bash
sleep 2
agent-browser --session {SESSION} screenshot --annotate {OUTPUT_DIR}/screenshots/issue-{NNN}-result.png
```

4. **停止录制视频：**

```bash
agent-browser --session {SESSION} record stop
```

5. 在报告中写出带编号的复现步骤，每一步都引用相应的截图。

#### 静态/加载时可见的问题（拼写错误、占位符文本、文本被截断、对齐错误、加载时出现的控制台错误）

这些问题无需交互即可看到——一张标注截图就足够。无需视频，也无需多步复现：

```bash
agent-browser --session {SESSION} screenshot --annotate {OUTPUT_DIR}/screenshots/issue-{NNN}.png
```

在报告中写一段简短说明并引用该截图。将**复现视频**设置为 `N/A`。

---

**对于所有问题：**

1. **立即追加到报告中。** 不要将问题留到以后批量记录。发现一个就记录一个，以免会话中断时丢失信息。

2. **递增问题计数器**（ISSUE-001、ISSUE-002、……）。

### 6. 收尾

目标是找到 **5-10 个记录完善的问题**，然后收尾。证据深度比总数更重要——5 个拥有完整复现过程的问题，胜过 20 个描述含糊的问题。

探索完成后：

1. 重新阅读报告并更新汇总中的严重程度数量，确保其与实际问题一致。每个 `### ISSUE-` 块都必须计入总数。
2. 关闭会话：

```bash
agent-browser --session {SESSION} close
```

3. 告知用户报告已准备完毕，并汇总发现：问题总数、按严重程度划分的数量，以及最关键的问题。

## 指导原则

- **复现证据就是一切。** 每个问题都需要证据——但证据应与问题匹配。交互式缺陷需要视频和分步截图。静态缺陷（拼写错误、占位符文本、加载时可见的视觉问题）只需要一张标注截图。
- **收集证据前验证可复现性。** 在录制视频或截图前，至少重试一次以确认问题能够复现。如果无法稳定复现，就不能视为有效问题。
- **不要为静态问题录制视频。** 拼写错误或文本被截断不会因视频而获得更多价值。将视频用于涉及用户交互、时间因素或状态变化的问题。
- **对于交互问题，每一步都要截图。** 捕获操作前、操作过程和操作后的状态——让他人能够看到完整顺序。
- **编写与截图对应的复现步骤。** 报告中的每个编号步骤都应引用对应的截图。读者无需操作浏览器，也应能通过视觉材料了解整个流程。
- **使用正确的快照命令。**
  - `snapshot -i` — 用于查找可点击/可填写的元素（按钮、输入框、链接）
  - `snapshot`（无标志）— 用于读取页面内容（文本、标题、数据列表）
- **要全面，但也要运用判断力。** 你不是在照着测试脚本执行——而是像真实用户一样探索。如果感觉某处不对，请展开调查。
- **逐步记录发现。** 每发现一个问题，就将其追加到报告中。即使会话中断，发现也能得到保留。切勿等到最后才批量记录所有问题。
- **切勿删除输出文件。** 会话过程中不要 `rm` 截图、视频或报告。不要关闭会话后重新开始。持续向前推进，不要回退。
- **切勿读取目标应用的源代码。** 你是在以用户身份进行测试，而不是审计代码。不要读取受测应用的 HTML、JS 或配置文件。所有发现都必须来自你在浏览器中的观察。
- **检查控制台。** 许多问题在 UI 中不可见，但会以 JS 错误或请求失败的形式出现在控制台中。
- **像用户一样测试，而不是像机器人。** 尝试常见的端到端工作流。点击真实用户会点击的内容。输入符合现实情况的数据。
- **像人一样输入。** 在录制视频期间填写表单字段时，请使用 `type` 而不是 `fill`——它会逐字符输入。仅在不录制视频且速度更重要时使用 `fill`。
- **控制复现视频的节奏，使其适合人类观看。** 在操作之间添加 `sleep 1`，并在最终结果截图前添加 `sleep 2`。视频应能以 1 倍速顺畅观看——审阅报告的人需要看清发生了什么，而不是看到一连串瞬间变化的模糊画面。
- **高效使用命令。** 当多个 `agent-browser` 命令相互独立时，将它们合并到一次 shell 调用中（例如，`agent-browser ... screenshot ... && agent-browser ... console`）。滚动时使用 `agent-browser --session {SESSION} scroll down 300`——不要使用 `key` 或 `evaluate` 进行滚动。

## 参考资料

| 参考资料 | 何时阅读 |
|-----------|--------------|
| [references/issue-taxonomy.md](references/issue-taxonomy.md) | 会话开始时——校准要查找的问题、严重程度级别和探索检查清单 |

## 模板

| 模板 | 用途 |
|----------|---------|
| [templates/dogfood-report-template.md](templates/dogfood-report-template.md) | 复制到输出目录中作为报告文件 |
