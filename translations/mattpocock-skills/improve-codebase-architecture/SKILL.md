<!-- source-sha256: 0026900866ed2a542af0559cef11dd7ae707633b75cc6f668c2e7c0a33e35032 -->
---
name: improve-codebase-architecture
description: 扫描代码库中可进一步深化的机会，将其以可视化 HTML 报告呈现，然后针对你选择的任一项进行深入追问。
disable-model-invocation: true
---

# 改进代码库架构

揭示架构摩擦，并提出**深化机会**（**deepening opportunities**）——将浅层模块重构为深层模块。目标是提高可测试性和 AI 可导航性。

此命令以项目的领域模型为依据，并建立在一套共享的设计词汇之上：

- 运行 `/codebase-design` skill，获取架构词汇（**module**、**interface**、**depth**、**seam**、**adapter**、**leverage**、**locality**）及其原则（删除测试、“interface 就是测试表面”、“一个 adapter = 假想 seam，两个 = 真实 seam”）。在每条建议中准确使用这些术语——不要偏移到 “component”、“service”、“API” 或 “boundary”。
- `CONTEXT.md` 中的领域语言为良好的 seam 提供名称；`docs/adr/` 中的 ADR 记录了此命令不应重新争论的决策。

## 流程

### 1. 探索

首先阅读项目的领域术语表（`CONTEXT.md`），以及与你正在处理的区域相关的所有 ADR。

然后使用 Agent 工具并设置 `subagent_type=Explore` 来遍历代码库。不要遵循僵化的启发式规则——自然地探索，并记录你遇到摩擦的位置：

- 理解一个概念时，哪些地方需要在许多小型 module 之间反复跳转？
- 哪些 module 是**浅层的**——interface 几乎和实现一样复杂？
- 哪些纯函数只是为了可测试性而被提取出来，但真正的 bug 隐藏在它们的调用方式中（缺乏 **locality**）？
- 哪些紧密耦合的 module 会跨越其 seam 泄漏？
- 代码库的哪些部分未经测试，或者很难通过当前 interface 进行测试？

对任何你怀疑是浅层的对象应用**删除测试**：删除它会集中复杂性，还是仅仅转移复杂性？你要寻找的信号是“是的，会集中复杂性”。

### 2. 将候选项呈现为 HTML 报告

将一个自包含的 HTML 文件写入操作系统临时目录，避免在仓库中产生任何文件。临时目录从 `$TMPDIR` 解析，若不可用则回退到 `/tmp`（Windows 上为 `%TEMP%`），并写入 `<tmpdir>/architecture-review-<timestamp>.html`，确保每次运行都生成新文件。为用户打开该文件——Linux 上使用 `xdg-open <path>`，macOS 上使用 `open <path>`，Windows 上使用 `start <path>`——并告知用户其绝对路径。

报告使用通过 CDN 引入的 **Tailwind** 进行布局和样式设计，并在图、流程或时序能够可靠表达结构时，使用通过 CDN 引入的 **Mermaid** 绘制图表。将 Mermaid 与手工编写的 CSS/SVG 视觉元素结合使用——当关系呈图结构时（调用图、依赖关系、时序）使用 Mermaid；当你想要更具编辑表达力的效果时（质量图、剖面图、折叠动画），使用手工构建的 div/SVG。每个候选项都要提供一份**前后对比可视化**。突出视觉表达。

为每个候选项渲染一张卡片，其中包含：

- **文件**——涉及哪些文件/module
- **问题**——当前架构为何造成摩擦
- **解决方案**——用通俗语言描述将发生哪些变化
- **收益**——从 locality 和 leverage 的角度说明，并解释测试将如何改善
- **改造前 / 改造后图表**——并排展示、自定义绘制，用于说明当前的浅层特征及深化后的效果
- **推荐强度**——从 `Strong`、`Worth exploring`、`Speculative` 中选择一项，并渲染为徽章

报告末尾添加一个**首要推荐**部分：说明你会优先处理哪个候选项，以及原因。

**领域部分使用 CONTEXT.md 中的词汇，架构部分使用 `/codebase-design` 中的词汇。** 如果 `CONTEXT.md` 定义了 “Order”，就称其为“Order 接入 module”——不要称为 “FooBarHandler”，也不要称为 “Order service”。

**ADR 冲突**：如果某个候选项与现有 ADR 相矛盾，只有当摩擦真实且严重到足以重新审视该 ADR 时，才将其列出。在卡片中清楚标记该冲突（例如使用警告提示：_“与 ADR-0007 冲突——但值得重新讨论，因为……”_）。不要列出 ADR 所禁止的每一种理论上的重构。

完整的 HTML 脚手架、图表模式和样式指南请参阅 [HTML-REPORT.md](HTML-REPORT.md)。

此时不要提出 interface。文件写入完成后，询问用户：“你想探索其中哪一项？”

### 3. 深入追问循环

用户选择候选项后，运行 `/grilling` skill，与用户一起遍历设计决策树——约束、依赖关系、深化后 module 的形态、seam 背后包含什么，以及哪些测试能够保留。

随着决策逐渐明确，副作用会同步发生——在此过程中运行 `/domain-modeling` skill，持续保持领域模型为最新状态：

- **要以 `CONTEXT.md` 中不存在的概念为深化后的 module 命名？** 将该术语添加到 `CONTEXT.md`。如果文件不存在，则按需创建。
- **在对话过程中明确了一个含糊术语？** 立即更新 `CONTEXT.md`。
- **用户以一个影响架构根基的理由拒绝候选项？** 提议创建 ADR，并这样表述：_“要我将此记录为 ADR 吗？这样未来的架构审查就不会再次提出它。”_ 只有当未来的探索者确实需要知道该理由，才能避免再次提出相同建议时，才进行提议——跳过临时性理由（“现在不值得做”）和不言自明的理由。
- **想为深化后的 module 探索其他 interface？** 运行 `/codebase-design` skill，并使用其中的设计两次并行 sub-agent 模式。
