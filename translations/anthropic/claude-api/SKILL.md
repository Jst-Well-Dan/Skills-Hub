<!-- source-sha256: 290beaca25c5938cb94355ff3a452712e4e32d1b202cc6af75991160af147e3d -->
---
name: claude-api
description: |-
  Claude API / Anthropic SDK 参考资料——涵盖模型 ID、定价、参数、流式传输、工具使用、MCP、智能体、缓存、令牌计数和模型迁移。
  触发条件——在打开目标文件之前阅读；不要因为它“看起来只需一行”就跳过——以下情况均应触发：提示以任何形式提到 Claude/Anthropic（Claude、Anthropic、Fable、Opus、Sonnet、Haiku、`anthropic`、`@anthropic-ai`、`claude-*`、`us.anthropic.*`、`[1m]`）；用户询问 LLM（定价/模型选择/限制/缓存）——绝不能凭记忆回答；或者任务具有 LLM 特征但未说明提供商（智能体/MCP/工具定义/多智能体/RAG/LLM 评判器/计算机使用；针对自然语言进行生成/摘要/提取/分类/改写/对话；调试拒绝/截断/流式传输/工具调用/令牌问题）。
  仅在正在处理其他提供商时跳过（覆盖所有触发条件）：查询中提到 OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama；或者在项目中运行 `grep -rE 'openai|langchain_openai|google.generativeai|genai|mistralai|cohere|ollama'` 有匹配结果（如果未指定提供商，首先运行此 grep——不要读取文件）。
license: 完整条款见 LICENSE.txt
---

# 使用 Claude 构建由 LLM 驱动的应用程序

此技能可帮助你使用 Claude 构建由 LLM 驱动的应用程序。请根据需求选择正确的使用层面，检测项目语言，然后阅读相关的语言专属文档。

## 开始之前

扫描目标文件（如果没有目标文件，则扫描提示和项目），查找非 Anthropic 提供商标记——`import openai`、`from openai`、`langchain_openai`、`OpenAI(`、`gpt-4`、`gpt-5`，类似 `agent-openai.py` 或 `*-generic.py` 的文件名，或任何明确要求保持代码提供商中立的指令。如果发现任何此类标记，请停止并告知用户，此技能会生成 Claude/Anthropic SDK 代码；询问他们是想将该文件切换到 Claude，还是想要非 Claude 实现。不要使用 Anthropic SDK 调用修改非 Anthropic 文件。

## 输出要求

当用户要求你添加、修改或实现 Claude 功能时，你的代码必须通过以下方式之一调用 Claude：

1. 项目语言对应的**官方 Anthropic SDK**（`anthropic`、`@anthropic-ai/sdk`、`com.anthropic.*` 等）。只要项目存在受支持的 SDK，默认就使用此方式。
2. **原始 HTTP**（`curl`、`requests`、`fetch`、`httpx` 等）——仅当用户明确要求 cURL/REST/原始 HTTP、项目本身是 shell/cURL 项目，或该语言没有官方 SDK 时使用。

绝不要混用两者——不要仅仅因为觉得更轻量，就在 Python 或 TypeScript 项目中改用 `requests`/`fetch`。绝不要退回到 OpenAI 兼容垫片。

**绝不要猜测 SDK 用法。**函数名、类名、命名空间、方法签名和导入路径必须来自明确的文档——可以是此技能中的 `{lang}/` 文件，也可以是 `shared/live-sources.md` 中列出的官方 SDK 仓库或文档链接。如果所需绑定未在技能文件中明确记录，请在编写代码前，通过 WebFetch 获取 `shared/live-sources.md` 中相关 SDK 仓库的内容。不要根据 cURL 形式或另一种语言的 SDK 推断 Ruby/Java/Go/PHP/C# API。

## 默认值

除非用户另有要求：

对于 Claude 模型版本，请使用 Claude Opus 4.8，可通过精确模型字符串 `claude-opus-4-8` 访问。对于任何稍显复杂的任务，默认使用自适应思考（`thinking: {type: "adaptive"}`）。最后，对于可能涉及长输入、长输出或较高 `max_tokens` 的请求，默认使用流式传输——这可以避免达到请求超时。如果不需要单独处理各个流事件，请使用 SDK 的 `.get_final_message()` / `.finalMessage()` 辅助方法获取完整响应。

---

## 子命令

如果此提示底部的用户请求是一个纯子命令字符串（不含说明性文字），请搜索本文档中的每个 **Subcommands** 表——包括下方追加章节中的表——并直接执行匹配的 Action 列。这样用户便可通过 `/claude-api <subcommand>` 调用特定流程。如果文档中没有表与其匹配，则将请求视为普通自然语言。

| 子命令 | 操作 |
|---|---|
| `migrate` | 将现有 Claude API 代码迁移到较新的模型。**立即阅读 `shared/model-migration.md`**，并按顺序执行：步骤 0（确认范围——进行任何编辑前先询问要处理哪些文件/目录）、步骤 1（对每个文件分类），然后执行每个目标对应的破坏性变更章节。不要概述指南——直接执行。如果用户没有指定目标模型，请在询问范围的同一轮中询问要迁移到哪个模型。 |

---

## 语言检测

在阅读代码示例之前，确定用户正在使用哪种语言：

1. **查看项目文件**以推断语言：

   - `*.py`、`requirements.txt`、`pyproject.toml`、`setup.py`、`Pipfile` → **Python**——从 `python/` 中读取
   - `*.ts`、`*.tsx`、`package.json`、`tsconfig.json` → **TypeScript**——从 `typescript/` 中读取
   - `*.js`、`*.jsx`（不存在 `.ts` 文件）→ **TypeScript**——JS 使用相同的 SDK，从 `typescript/` 中读取
   - `*.java`、`pom.xml`、`build.gradle` → **Java**——从 `java/` 中读取
   - `*.kt`、`*.kts`、`build.gradle.kts` → **Java**——Kotlin 使用 Java SDK，从 `java/` 中读取
   - `*.scala`、`build.sbt` → **Java**——Scala 使用 Java SDK，从 `java/` 中读取
   - `*.go`、`go.mod` → **Go**——从 `go/` 中读取
   - `*.rb`、`Gemfile` → **Ruby**——从 `ruby/` 中读取
   - `*.cs`、`*.csproj` → **C#**——从 `csharp/` 中读取
   - `*.php`、`composer.json` → **PHP**——从 `php/` 中读取

2. **如果检测到多种语言**（例如同时存在 Python 和 TypeScript 文件）：

   - 检查用户当前文件或问题涉及哪种语言
   - 如果仍不明确，请询问：“我检测到 Python 和 TypeScript 文件。你使用哪种语言进行 Claude API 集成？”

3. **如果无法推断语言**（空项目、没有源文件或语言不受支持）：

   - 使用 AskUserQuestion，并提供以下选项：Python、TypeScript、Java、Go、Ruby、cURL/raw HTTP、C#、PHP
   - 如果 AskUserQuestion 不可用，则默认展示 Python 示例，并注明：“以下展示 Python 示例。如果你需要其他语言，请告诉我。”

4. **如果检测到不受支持的语言**（Rust、Swift、C++、Elixir 等）：

   - 建议使用 `curl/` 中的 cURL/原始 HTTP 示例，并注明可能存在社区 SDK
   - 提议展示 Python 或 TypeScript 示例作为参考实现

5. **如果用户需要 cURL/原始 HTTP 示例**，请从 `curl/` 中读取。

### 各语言功能支持情况

| 语言       | 工具运行器 | 托管式智能体 | 说明                                  |
| ---------- | ---------- | ------------ | ------------------------------------- |
| Python     | 是（测试版） | 是（测试版） | 完整支持——`@beta_tool` 装饰器         |
| TypeScript | 是（测试版） | 是（测试版） | 完整支持——`betaZodTool` + Zod         |
| Java       | 是（测试版） | 是（测试版） | 使用注解类的测试版工具使用功能        |
| Go         | 是（测试版） | 是（测试版） | `toolrunner` 包中的 `BetaToolRunner`  |
| Ruby       | 是（测试版） | 是（测试版） | 测试版中的 `BaseTool` + `tool_runner` |
| C#         | 是（测试版） | 是（测试版） | `BetaToolRunner` + 原始 JSON schema   |
| PHP        | 是（测试版） | 是（测试版） | `BetaRunnableTool` + `toolRunner()`   |
| cURL       | 不适用     | 是（测试版） | 原始 HTTP，无 SDK 功能                |

> **托管式智能体代码示例**：为 Python、TypeScript、Go、Ruby、PHP、Java 和 cURL 提供了专用的语言特定 README（`{lang}/managed-agents/README.md`、`curl/managed-agents.md`）。请阅读对应语言的 README，以及与语言无关的 `shared/managed-agents-*.md` 概念文件。**智能体具有持久性——只创建一次，之后通过 ID 引用。**保存 `agents.create` 返回的智能体 ID，并将其传给后续每次 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是通过纳入版本控制的 YAML 创建智能体和环境的一种便捷方式——参见 `shared/anthropic-cli.md`。如果 README 中没有展示所需绑定，请通过 WebFetch 获取 `shared/live-sources.md` 中的相关条目，而不要猜测。C# 通过 `client.Beta.Agents` 及相关命名空间提供测试版托管式智能体支持。

---

## 应该使用哪种使用层面？

> **从简单开始。**默认选择能够满足需求的最简单层级。单次 API 调用和工作流足以处理大多数用例——只有当任务确实需要开放式、由模型驱动的探索时，才使用智能体。

| 用例                                            | 层级          | 推荐使用层面              | 原因                                                         |
| ----------------------------------------------- | ------------- | ------------------------- | ------------------------------------------------------------ |
| 分类、摘要、提取、问答                          | 单次 LLM 调用 | **Claude API**            | 一次请求，一次响应                                           |
| 批处理或嵌入                                    | 单次 LLM 调用 | **Claude API**            | 专用端点                                                     |
| 由代码控制逻辑的多步骤流水线                    | 工作流        | **Claude API + 工具使用** | 由你编排循环                                                 |
| 使用自有工具的自定义智能体                      | 智能体        | **Claude API + 工具使用** | 灵活性最高                                                   |
| 带有工作区、由服务器管理状态的智能体            | 智能体        | **托管式智能体**          | Anthropic 运行循环并托管工具执行沙箱                         |
| 持久化、带版本的智能体配置                      | 智能体        | **托管式智能体**          | 智能体是存储对象；会话固定到某个版本                         |
| 挂载文件的长时间运行多轮智能体                  | 智能体        | **托管式智能体**          | 每会话容器、SSE 事件流、Skills + MCP                         |

> **注意：**如果你希望 Anthropic 既运行智能体循环，*又*托管执行工具的容器，托管式智能体就是正确选择——文件操作、bash 和代码执行都在每会话工作区中运行。如果你希望自行托管计算资源或运行自己的自定义工具运行时，则应选择 Claude API + 工具使用——可使用工具运行器自动处理循环，也可使用手动循环进行精细控制（审批关卡、自定义日志、条件执行）。

> **云提供商访问。****AWS 上的 Claude Platform** 由 Anthropic 运营，并具有当日 API 功能一致性——除**自托管沙箱**外，此技能中的托管式智能体及所有功能均可用（参见 `shared/claude-platform-on-aws.md`）。**Amazon Bedrock**、**Google Vertex AI** 和 **Microsoft Foundry** 不支持托管式智能体或 Anthropic 服务端工具；在这些平台上请使用 **Claude API + 工具使用**。

### 决策树

```
你的应用程序需要什么？

0. 使用哪个提供商？
   ├── 第一方 API 或 AWS 上的 Claude Platform → 继续（全部使用层面均可用）。
   └── Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry → Claude API（智能体使用工具功能）；这些平台不提供托管式智能体。

1. 单次 LLM 调用（分类、摘要、提取、问答）
   └── Claude API——一次请求，一次响应

2. 你是否希望 Anthropic 运行智能体循环，并托管一个每会话
   容器，让 Claude 在其中执行工具（bash、文件操作、代码）？
   └── 是 → 托管式智能体——服务器管理的会话、持久化智能体配置、
       SSE 事件流、Skills + MCP、文件挂载。
       示例：“每个任务都有独立工作区的有状态编码智能体”、
             “将事件流式传输到 UI 的长时间运行研究智能体”、
             “使用持久化、带版本配置并跨多个会话复用的智能体”

3. 工作流（多步骤、由代码编排、使用自有工具）
   └── 使用工具功能的 Claude API——由你控制循环

4. 开放式智能体（模型自行决定行动轨迹、使用你的工具、由你托管计算资源）
   └── Claude API 智能体循环（灵活性最高）
```

### 应该构建智能体吗？

在选择智能体层级之前，请检查以下四项标准：

- **复杂度**——任务是否包含多个步骤，并且难以预先完整说明？（例如，“将这份设计文档转化为 PR”与“从这份 PDF 中提取标题”）
- **价值**——结果是否足以证明更高的成本和延迟是合理的？
- **可行性**——Claude 是否擅长此类任务？
- **错误成本**——能否发现错误并从中恢复？（测试、审查、回滚）

如果其中任何一项的答案是“否”，请继续使用更简单的层级（单次调用或工作流）。

---

## 架构

所有功能都通过 `POST /v1/messages` 实现。工具和输出约束是这一个端点的功能——并不是独立的 API。

**用户定义工具**——你定义工具（通过装饰器、Zod schema 或原始 JSON），SDK 的工具运行器负责调用 API、执行你的函数并循环，直到 Claude 完成任务。若要完全掌控，也可以手动编写循环。

**服务端工具**——由 Anthropic 托管、在 Anthropic 基础设施上运行的工具。代码执行完全在服务端完成（在 `tools` 中声明，Claude 会自动运行代码）。计算机使用功能可由服务器托管，也可自行托管。

**结构化输出**——约束 Messages API 的响应格式（`output_config.format`）和/或工具参数验证（`strict: true`）。推荐使用 `client.messages.parse()`，它会根据你的 schema 自动验证响应。注意：旧的 `output_format` 参数已弃用；请在 `messages.create()` 上使用 `output_config: {format: {...}}`。

**辅助端点**——批处理（`POST /v1/messages/batches`）、文件（`POST /v1/files`）、令牌计数（`POST /v1/messages/count_tokens`——参见 `shared/token-counting.md`）和模型（`GET /v1/models`、`GET /v1/models/{id}`——实时发现能力/上下文窗口）为 Messages API 请求提供输入或支持。

---

## 当前模型（缓存日期：2026-06-04）

| 模型              | 模型 ID             | 上下文         | 输入 $/1M | 输出 $/1M |
| ----------------- | ------------------- | -------------- | --------- | --------- |
| Claude Fable 5    | `claude-fable-5`    | 1M             | $10.00    | $50.00    |
| Claude Mythos 5（仅限 Project Glasswing） | `claude-mythos-5` | 1M | $10.00 | $50.00 |
| Claude Opus 4.8   | `claude-opus-4-8`   | 1M             | $5.00     | $25.00    |
| Claude Opus 4.7   | `claude-opus-4-7`   | 1M             | $5.00     | $25.00    |
| Claude Opus 4.6   | `claude-opus-4-6`   | 1M             | $5.00     | $25.00    |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M             | $3.00     | $15.00    |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00     | $5.00     |

**除非用户明确指定其他模型，否则始终使用 `claude-opus-4-8`。**此项不可协商。除非用户确切说出“use sonnet”或“use haiku”，否则不要使用 `claude-sonnet-4-6`、`claude-sonnet-4-5` 或任何其他模型。绝不要为了成本而降级——这是用户的决定，不是你的决定。仅当用户明确要求 Claude Fable 5、“fable”或 Anthropic 最强模型时，才使用 `claude-fable-5`——它的 API 行为与 Opus 系列不同（见下文），定价也高于 Opus 层级。

### Claude Fable 5（`claude-fable-5`）——已广泛发布的最强模型

Claude Fable 5 是 Anthropic 已广泛发布的最强模型，适合要求最高的推理任务和长周期智能体工作。**Claude Mythos 5**（`claude-mythos-5`）通过 Project Glasswing 提供相同的能力、定价和 API 使用层面（参与该项目是唯一访问方式），接替仅限邀请的 Claude Mythos Preview（`claude-mythos-preview`）——以下所有内容均适用于这两个模型。上下文窗口为 1M（最大值也是默认值），最大输出为 128K。与 Opus 层级相比的关键 API 差异如下——详情参见 `shared/model-migration.md` → Migrating to Claude Fable 5：

- **思考始终开启**——完全省略 `thinking` 参数（或发送 `{type: "adaptive"}`）。其他任何显式配置都会被拒绝：`{type: "disabled"}` 和 `{type: "enabled", budget_tokens: N}` 都会返回 400。使用 `output_config.effort` 控制深度（支持从 `low` 到 `xhigh` 以及 `max`）。
- **受保护的思考内容是原始思维链，而不是摘要**——响应携带普通 `thinking` 块（而非 `redacted_thinking`）：`display: "summarized"` 返回可读摘要；`"omitted"`（默认值）使 `thinking` 字段保留为空字符串；任何模型都绝不会暴露原始思维链。重放规则：在同一模型上，将接收到的思考块原样传回（包括空文本块——API 拒绝的是*被修改的*块，而非读取过的块）；**不同**模型会**静默忽略**它们（不会报错），但被忽略的块仍按输入令牌计费——永久切换模型时应移除它们。
- **新分词器**——相同内容产生的令牌数比 Opus 层级模型多约 30%。不要复用在其他模型上测得的令牌计数或 `max_tokens` 设置；请使用 `count_tokens` 重新建立基准。
- **`refusal` 停止原因**——安全分类器可能拒绝请求（HTTP 200、`stop_reason: "refusal"`，并带有 `stop_details` 类别）。输出前拒绝时，`content` 数组为空，且完全不计费；流式传输中途拒绝时，已经流式输出的内容会计费——请丢弃部分输出。读取 `content` 前始终检查 `stop_reason`。若要在其他模型上重试：测试版 `fallbacks` 参数（Claude API 和 AWS 上的 Claude Platform）可在一次往返中由服务器重试；GA SDK 的 `BetaRefusalFallbackMiddleware` + `BetaFallbackState` 可在其他所有平台（包括 Bedrock/Vertex）进行客户端重试；回退额度会补偿客户端重试导致的缓存切换成本。参见迁移指南的拒绝章节。
- **不支持 assistant 预填充**——与其余 4.6+ 系列相同。
- **要求保留数据 30 天**——Claude Fable 5 不适用于零数据保留；如果组织的保留配置不满足要求，请求将返回 `400 invalid_request_error`。
- **更长的轮次、不同的提示方式**——困难任务的单次请求可能运行数分钟（请规划超时/流式传输/进度体验）；常规工作进行 effort 扫描时应包含 low/medium；为以往模型编写的提示通常过于规定化，会降低输出质量。有关推荐的提示片段（避免过度规划、不做无关整理、基于事实报告进度、边界、异步子智能体、记忆、`send_to_user`），请参见 `shared/model-migration.md` → Migrating to Claude Fable 5 → Behavioral shifts (prompt-tunable)。

**关键要求：仅使用上表中的精确模型 ID 字符串——它们本身就是完整的。不要附加日期后缀。**例如，使用 `claude-sonnet-4-6`，绝不要使用 `claude-sonnet-4-6-20251114` 或你可能从训练数据中记得的任何其他带日期后缀的变体。如果用户要求使用表中没有的旧模型（例如“opus 4.5”“sonnet 3.7”），请阅读 `shared/models.md` 获取精确 ID——不要自行构造。

注意：如果上面某些模型字符串对你来说很陌生，这是正常现象——这只表示它们是在你的训练数据截止日期之后发布的。请放心，它们是真实存在的模型；我们不会拿这种事情捉弄你。

**实时能力查询：**上表是缓存数据。当用户询问“X 的上下文窗口是多少”“X 是否支持视觉/思考/effort”或“哪些模型支持 Y”时，请查询 Models API（`client.models.retrieve(id)` / `client.models.list()`）——字段参考和能力筛选示例参见 `shared/models.md`。

---

## 思考与 Effort（快速参考）

**Fable 5 / Opus 4.8 / 4.7——仅支持自适应思考：**使用 `thinking: {type: "adaptive"}`。`thinking: {type: "enabled", budget_tokens: N}` 会返回 400——自适应是唯一的开启模式。在 Opus 4.8 和 4.7 上，`{type: "disabled"}` 和省略 `thinking` 均可使用；在 Fable 5 上，显式使用 `{type: "disabled"}` 会返回 400——应完全省略 `thinking` 参数。采样参数（`temperature`、`top_p`、`top_k`）也已移除，使用时会返回 400。Opus 4.8 的请求使用层面与 4.7 相同（没有新的破坏性变更）——有关行为重新调优，请参见 `shared/model-migration.md` → Migrating to Opus 4.8；从 4.6 或更早版本迁移时，请参见 → Migrating to Opus 4.7 获取完整的破坏性变更列表。注意：禁用 `thinking` 后，Opus 4.8 可能在可见响应中写出更长的推理过程——请保持启用自适应思考，或添加仅输出最终答案的指令（参见迁移指南）。
**Opus 4.6——自适应思考（推荐）：**使用 `thinking: {type: "adaptive"}`。Claude 会动态决定何时思考以及思考多少。无需 `budget_tokens`——`budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上已弃用，不应在新代码中使用。自适应思考还会自动启用交错思考（无需测试版标头）。**当用户要求“extended thinking”、一个“thinking budget”或 `budget_tokens` 时：始终使用 Fable 5、Opus 4.8、4.7 或 4.6，并设置 `thinking: {type: "adaptive"}`。固定思考令牌预算这一概念已弃用——由自适应思考取代。不要在新的 4.6/4.7/4.8 代码中使用 `budget_tokens`，也不要切换到旧模型。***渐进式迁移例外：*`budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上仍可作为过渡性应急方案使用——如果正在迁移现有代码，并且在完成 `effort` 调优前需要硬性令牌上限，请参见 `shared/model-migration.md` → Transitional escape hatch。注意：此例外**不**适用于 Fable 5、Opus 4.7 或 4.8——这些模型已完全移除 `budget_tokens`。
**Effort 参数（GA，无需测试版标头）：**通过 `output_config: {effort: "low"|"medium"|"high"|"max"}`（位于 `output_config` 内，而非顶层）控制思考深度和总体令牌消耗。默认值是 `high`（等同于省略该参数）。Fable 5、Opus 4.6 及更高版本和 Sonnet 4.6 支持 `max`（Haiku 或更早版本的 Sonnet 不支持）。Opus 4.7 新增了 `"xhigh"`（位于 `high` 和 `max` 之间）——对于 Fable 5 / Opus 4.7/4.8 上的大多数编码和智能体用例，这是最佳设置，也是 Claude Code 的默认设置；对于大多数对智能水平敏感的工作，最低使用 `high`。适用于 Fable 5、Opus 4.5、Opus 4.6、Opus 4.7、Opus 4.8 和 Sonnet 4.6。在 Sonnet 4.5 / Haiku 4.5 上会报错。在 Fable 5、Opus 4.7 和 4.8 上，effort 比在任何以前的 Opus 模型上都更重要——迁移时请重新调优；对于长周期/智能体任务，请使用 `high`/`xhigh`，并预先提供完整任务说明。与自适应思考结合，可获得最佳成本与质量权衡。较低的 effort 意味着更少且更集中的工具调用、更少的前言和更简短的确认——`high` 通常是在质量和令牌效率之间取得平衡的最佳点；当正确性比成本更重要时使用 `max`；对子智能体或简单任务使用 `low`。

**思考显示——Fable 5 / Mythos 5 / Opus 4.8 / 4.7 默认为 `"omitted"`：**`display: "summarized"` 返回可读的推理摘要；`"omitted"`（这四个模型的默认值——与 Opus 4.6 的 `"summarized"` 相比属于静默变更）会流式传输文本为空的 `thinking` 块。`display` 仅控制可见性——所有设置下都会同样进行思考并计费；任何模型都绝不会暴露原始思维链。如果将推理过程流式传输给用户，默认行为看起来会像输出前长时间停顿——请显式设置 `thinking: {type: "adaptive", display: "summarized"}`。（无论 display 如何设置，在同一模型上继续时，都应原样回传思考块；其他模型会静默忽略它们——参见迁移指南。）

**任务预算（测试版，Fable 5 / Opus 4.7 / 4.8）：**`output_config: {task_budget: {type: "tokens", total: N}}` 告诉模型整个智能体循环可使用多少令牌——模型会看到持续更新的倒计时并自行控制（最低 20,000；测试版标头 `task-budgets-2026-03-13`）。这与 `max_tokens` 不同，后者是模型无法感知的、强制执行的单次响应上限。参见 `shared/model-migration.md` → Task Budgets。

**Sonnet 4.6：**支持自适应思考（`thinking: {type: "adaptive"}`）。`budget_tokens` 在 Sonnet 4.6 上已弃用——请改用自适应思考。

**旧模型（仅在明确要求时）：**如果用户明确要求 Sonnet 4.5 或其他旧模型，请使用 `thinking: {type: "enabled", budget_tokens: N}`。`budget_tokens` 必须小于 `max_tokens`（最低为 1024）。绝不要仅仅因为用户提到 `budget_tokens` 就选择旧模型——应改用 Opus 4.8 和自适应思考。

---

## 压缩（快速参考）

**测试版，支持 Fable 5、Opus 4.8、Opus 4.7、Opus 4.6 和 Sonnet 4.6。**对于可能超过 1M 上下文窗口的长时间运行对话，请启用服务端压缩。API 会在接近触发阈值时自动总结较早的上下文（默认值：150K 令牌）。需要测试版标头 `compact-2026-01-12`。

**关键要求：**每轮都要将 `response.content`（而不仅是文本）追加回 messages。必须保留响应中的压缩块——API 会在下一次请求中使用它们替换已压缩的历史记录。如果只提取文本字符串并将其追加，会在不发出提示的情况下丢失压缩状态。

代码示例参见 `{lang}/claude-api/README.md`（Compaction 章节）。完整文档可通过 WebFetch 从 `shared/live-sources.md` 获取。

---

## 提示缓存（快速参考）

**前缀匹配。**前缀中任何位置发生任何字节变化，都会使其后的所有内容失效。渲染顺序为 `tools` → `system` → `messages`。将稳定内容放在前面（冻结的系统提示、确定性工具列表），将易变内容（时间戳、每请求 ID、变化的问题）放在最后一个 `cache_control` 断点之后。

**对话中途的操作员指令**（测试版标头 `mid-conversation-system-2026-04-07`，适用于支持的模型）：将 `{"role": "system", ...}` 追加到 `messages[]`，而不是编辑顶层 `system`。这样既能保留已缓存的历史记录前缀，又能提供防提示注入的操作员通道。参见 `shared/prompt-caching.md` § Mid-conversation system messages。

当不需要精细控制放置位置时，**顶层自动缓存**（在 `messages.create()` 上使用 `cache_control: {type: "ephemeral"}`）是最简单的选择。每个请求最多 4 个断点。可缓存前缀的最小长度约为 1024 个令牌——更短的前缀不会缓存，也不会提示。

**使用 `usage.cache_read_input_tokens` 验证**——如果重复请求时该值始终为零，则存在无提示失效因素（系统提示中的 `datetime.now()`、未排序的 JSON、变化的工具集）。

有关放置模式、架构指导和无提示失效因素审计清单，请阅读 `shared/prompt-caching.md`。特定语言语法：`{lang}/claude-api/README.md`（Prompt Caching 章节）。

---

## 托管式智能体（测试版）

**托管式智能体**是第三种使用层面：由服务器管理、带状态，并由 Anthropic 托管工具执行的智能体。你创建一个持久化、带版本的 Agent 配置（`POST /v1/agents`），然后启动引用该配置的 Sessions。每个会话都会预配一个容器作为智能体工作区——bash、文件操作和代码执行都在其中运行；智能体循环本身运行在 Anthropic 的编排层上，并通过工具操作容器。会话会流式传输事件；你需要将消息和工具结果发回。

**托管式智能体可用于第一方 API 和 AWS 上的 Claude Platform。**它**不**适用于 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry——在这些平台上构建智能体时，请使用 Claude API + 工具使用。

**强制流程：**Agent（一次）→ Session（每次运行）。`model`/`system`/`tools` 属于 agent，绝不属于 session。完整阅读指南、测试版标头和陷阱参见 `shared/managed-agents-overview.md`。

**测试版标头：**`managed-agents-2026-04-01`——对于所有 `client.beta.{agents,environments,sessions,vaults,memory_stores,deployments,deployment_runs}.*` 调用，SDK 会自动设置此标头。Skills API 使用 `skills-2025-10-02`，Files API 使用 `files-api-2025-04-14`，但除 `/v1/skills` 和 `/v1/files` 端点外，无需显式传入这些标头。

**子命令**——可通过 `/claude-api <subcommand>` 直接调用：

| 子命令 | 操作 |
|---|---|
| `managed-agents-onboard` | 引导用户从头设置托管式智能体。**立即阅读 `shared/managed-agents-onboarding.md`**，并遵循其访谈脚本：心智模型 → 已知或探索分支 → 模板配置 → 会话设置 → **飞行前可行性检查** → 输出代码。可行性检查会将所述工作与已配置的工具/凭据/数据进行核对，在智能体消耗预算前发现资源不足的配置——缺少工具、凭据或数据访问权限。不要概述——直接进行访谈。 |

**阅读指南：**首先阅读 `shared/managed-agents-overview.md`，然后阅读专题 `shared/managed-agents-*.md` 文件（core、environments、tools、events、outcomes、multiagent、webhooks、memory、scheduled-deployments、client-patterns、onboarding、api-reference）。对于 Python、TypeScript、Go、Ruby、PHP 和 Java，请阅读 `{lang}/managed-agents/README.md` 获取代码示例。对于 cURL，请阅读 `curl/managed-agents.md`。**智能体具有持久性——只创建一次，之后通过 ID 引用。**保存 `agents.create` 返回的智能体 ID，并将其传给后续每次 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是通过纳入版本控制的 YAML 创建智能体和环境的一种便捷方式——参见 `shared/anthropic-cli.md`。如果语言 README 中未展示所需绑定，请通过 WebFetch 获取 `shared/live-sources.md` 中的相关条目，而不要猜测。C# 通过 `client.Beta.Agents` 及相关命名空间提供测试版托管式智能体支持。

**当用户想从头设置托管式智能体时**（例如“如何开始”“带我创建一个”“设置一个新智能体”）：阅读 `shared/managed-agents-onboarding.md` 并进行其中的访谈——流程与 `managed-agents-onboard` 子命令相同。

**当用户询问“如何为 X 编写客户端代码”时：**使用 `shared/managed-agents-client-patterns.md`——其中涵盖无损流重连、`processed_at` 排队/已处理关卡、中断、`tool_confirmation` 往返、正确的空闲/终止退出关卡、空闲后状态竞争、流优先顺序、文件挂载陷阱、通过自定义工具将凭据保留在主机端等。

**当用户希望智能体按计划运行时**（cron、“每天晚上”“每周报告”）：阅读 `shared/managed-agents-scheduled-deployments.md`——部署会按 cron 周期自主启动会话，并提供运行记录、重试和自动暂停功能。

---

## 阅读指南

检测语言后，根据用户需求阅读相关文件：

### 快速任务参考

**单次文本分类/摘要/提取/问答：**
→ 仅阅读 `{lang}/claude-api/README.md`

**聊天 UI 或实时响应显示：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/streaming.md`

**长时间运行的对话（可能超过上下文窗口）：**
→ 阅读 `{lang}/claude-api/README.md`——参见 Compaction 章节
**迁移到较新的模型（Fable 5 / Opus 4.8 / Opus 4.7 / Opus 4.6 / Sonnet 4.6）或替换已退役模型：**
→ 阅读 `shared/model-migration.md`
**为 Fable 5 编写或调优提示（长轮次、effort、详细程度、自主运行、子智能体）：**
→ 阅读 `shared/model-migration.md` → Migrating to Fable 5 → Behavioral shifts (prompt-tunable) + Long-running agent recommendations
**提示缓存/优化缓存/“为什么我的缓存命中率很低”：**
→ 阅读 `shared/prompt-caching.md` + `{lang}/claude-api/README.md`（Prompt Caching 章节）
**计算文件/提示/diff 中的令牌数（“X 有多少令牌”）：**
→ 阅读 `shared/token-counting.md`——使用 `messages.count_tokens`，绝不要使用 `tiktoken`

**函数调用/工具使用/智能体：**
→ 阅读 `{lang}/claude-api/README.md` + `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`

**智能体设计（工具使用层面、上下文管理、缓存策略）：**
→ 阅读 `shared/agent-design.md`

**批处理（对延迟不敏感）：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/batches.md`

**跨多个请求上传文件：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/files-api.md`

**托管式智能体（带工作区、由服务器管理的有状态智能体）：**
→ 阅读 `shared/managed-agents-overview.md` + 其余 `shared/managed-agents-*.md` 文件。对于 Python、TypeScript、Go、Ruby、PHP 和 Java，请阅读 `{lang}/managed-agents/README.md` 获取代码示例。对于 cURL，请阅读 `curl/managed-agents.md`。**智能体具有持久性——只创建一次，之后通过 ID 引用。**保存 `agents.create` 返回的智能体 ID，并将其传给后续每次 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是通过纳入版本控制的 YAML 创建智能体和环境的一种便捷方式——参见 `shared/anthropic-cli.md`。如果语言 README 中未展示所需绑定，请通过 WebFetch 获取 `shared/live-sources.md` 中的相关条目，而不要猜测。C# 提供测试版托管式智能体支持——详情参见 `csharp/claude-api.md`，或参见 `curl/managed-agents.md` 获取原始 HTTP 参考。

### Claude API（完整文件参考）

阅读**语言特定的 Claude API 文件夹**（`{language}/claude-api/`）：

1. **`{language}/claude-api/README.md`**——**首先阅读此文件。**安装、快速开始、常用模式、错误处理。
2. **`shared/tool-use-concepts.md`**——当用户需要函数调用、代码执行、记忆或结构化输出时阅读。涵盖概念基础。
3. **`shared/agent-design.md`**——设计智能体时阅读：bash 与专用工具、程序化工具调用、工具搜索/技能、上下文编辑与压缩及记忆的比较、缓存原则。
4. **`{language}/claude-api/tool-use.md`**——用于阅读语言特定的工具使用代码示例（工具运行器、手动循环、代码执行、记忆、结构化输出）。
5. **`{language}/claude-api/streaming.md`**——构建聊天 UI 或增量显示响应的界面时阅读。
6. **`{language}/claude-api/batches.md`**——离线处理大量请求（对延迟不敏感）时阅读。异步运行，成本为正常价格的 50%。
7. **`{language}/claude-api/files-api.md`**——跨多个请求发送同一个文件而不重复上传时阅读。
8. **`shared/prompt-caching.md`**——添加或优化提示缓存时阅读。涵盖前缀稳定性设计、断点放置，以及会悄然使缓存失效的反模式。
9. **`shared/error-codes.md`**——调试 HTTP 错误或实现错误处理时阅读。
10. **`shared/model-migration.md`**——升级到较新模型、替换已退役模型，或将 `budget_tokens` / 预填充模式转换为当前 API 时阅读。
11. **`shared/live-sources.md`**——用于获取最新官方文档的 WebFetch URL。

> **注意：**Java、Go、Ruby、C#、PHP 和 cURL 各有一个涵盖所有基础内容的单一文件。根据需要阅读该文件以及 `shared/tool-use-concepts.md` 和 `shared/error-codes.md`。

> **注意：**有关托管式智能体的文件参考，请参见上方的 `## Managed Agents (Beta)` 章节——其中列出了所有 `shared/managed-agents-*.md` 文件和语言特定 README。

---

## 何时使用 WebFetch

在以下情况下使用 WebFetch 获取最新文档：

- 用户要求“最新”或“当前”信息
- 缓存数据看起来不正确
- 用户询问此处未涵盖的功能

实时文档 URL 位于 `shared/live-sources.md`。

## 常见陷阱

- 将文件或内容传给 API 时不要截断输入。如果内容太长，无法放入上下文窗口，请通知用户并讨论可选方案（分块、摘要等），而不是悄然截断。
- **Fable 5 / Opus 4.8 / 4.7 思考：**仅支持自适应模式。`thinking: {type: "enabled", budget_tokens: N}` 返回 400——`budget_tokens` 已被完全移除（`temperature`、`top_p`、`top_k` 也一并移除）。请使用 `thinking: {type: "adaptive"}`。Opus 4.8 继承了 4.7 的使用层面，没有新的破坏性变更；Fable 5 增加了一项——显式使用 `thinking: {type: "disabled"}` 会返回 400（4.7/4.8 接受该设置）；请改为省略该参数。
- **Opus 4.6 / Sonnet 4.6 思考：**使用 `thinking: {type: "adaptive"}`——不要在新的 4.6 代码中使用 `budget_tokens`（该参数在 Opus 4.6 和 Sonnet 4.6 上均已弃用；如要渐进迁移现有代码，请参见 `shared/model-migration.md` 中的过渡性应急方案——注意，此例外不适用于 Fable 5、Opus 4.7 或 4.8）。对于旧模型，`budget_tokens` 必须小于 `max_tokens`（最低为 1024）。如果设置错误，将会抛出异常。
- **已移除预填充（Fable 5 和 4.6/4.7/4.8 系列）：**assistant 消息预填充（最后一轮 assistant 预填充）在 Fable 5、Opus 4.6、Opus 4.7、Opus 4.8 和 Sonnet 4.6 上会返回 400 错误。请改用结构化输出（`output_config.format`）或系统提示指令控制响应格式。（有一个例外：回退额度预填充声明——使用 `fallback_has_prefill_claim: true` 兑换额度时，服务器会接受回显的 assistant 消息；参见迁移指南的拒绝章节。）
- **Fable 5 的 `refusal` 停止原因：**安全分类器可能拒绝请求——表现为成功的 HTTP 200 响应，并带有 `stop_reason: "refusal"`（输出前：`content` 为空，不计费；流式传输中途：部分输出计费——请丢弃）。读取 `response.content[0]` 前检查 `stop_reason`，否则拒绝请求会导致索引错误。若要在其他模型上重试，可原样重放历史记录——其他模型会静默忽略被拒模型的思考块——但被忽略的块仍按输入令牌计费，因此永久切换时应移除它们（例外：兑换回退额度时必须原样回显被拒绝的响应正文，包括思考块）。
- **Fable 5 分词器：**相同内容的令牌数比 Opus 层级模型多约 30%。在其他模型上测得的令牌计数、上下文窗口预算和 `max_tokens` 值不能直接沿用——请调用 `count_tokens` 并传入 `model: "claude-fable-5"` 重新测量（响应会包含两种分词器下的计数）。
- **编辑前确认迁移范围：**当用户要求将代码迁移到较新的 Claude 模型，却没有指定具体文件、目录或文件列表时，**首先询问要应用的范围**——整个工作目录、某个特定子目录，还是一组特定文件。在用户确认前不要开始编辑。“migrate my codebase”“move my project to X”“upgrade to Sonnet 4.6”或纯命令式的“migrate to Opus 4.8”之类措辞**仍然含糊**——它们说明了做什么，却没有说明在哪里做，因此必须询问。只有当提示指定了确切文件、特定目录或明确的文件列表（“migrate `app.py`”“migrate everything under `services/`”“update `a.py` and `b.py`”）时，才无需询问即可继续。参见 `shared/model-migration.md` 步骤 0。
- **`max_tokens` 默认值：**不要把 `max_tokens` 设得过低——达到上限会在思考中途截断输出，并需要重试。对于非流式请求，默认为 `~16000`（使响应保持在 SDK HTTP 超时范围内）。对于流式请求，默认为 `~64000`（无需担心超时，因此给模型足够空间）。只有在有明确理由时才降低：分类（`~256`）、成本上限、刻意要求短输出，或用于缓存预热的 **`max_tokens: 0`**（参见 `shared/prompt-caching.md` → Pre-warming）。
- **128K 输出令牌：**Fable 5、Opus 4.6、Opus 4.7 和 Opus 4.8 支持最高 128K 的 `max_tokens`，但为避免 HTTP 超时，SDK 要求对如此大的值使用流式传输。请使用 `.stream()` 和 `.get_final_message()` / `.finalMessage()`。
- **工具调用 JSON 解析（Fable 5 和 4.6/4.7/4.8 系列）：**Fable 5、Opus 4.6、Opus 4.7、Opus 4.8 和 Sonnet 4.6 可能在工具调用 `input` 字段中生成不同的 JSON 字符串转义形式（例如 Unicode 或正斜杠转义）。始终使用 `json.loads()` / `JSON.parse()` 解析工具输入——绝不要对序列化输入进行原始字符串匹配。
- **结构化输出（所有模型）：**在 `messages.create()` 上使用 `output_config: {format: {...}}`，而不是已弃用的 `output_format` 参数。这是通用 API 变更，并非 4.6 特有。
- **不要重新实现 SDK 功能：**SDK 提供高级辅助方法——请使用它们，不要从头构建。具体而言：使用 `stream.finalMessage()`，而不是将 `.on()` 事件包装在 `new Promise()` 中；使用带类型的异常类（`Anthropic.RateLimitError` 等），而不是对错误消息进行字符串匹配；使用 SDK 类型（`Anthropic.MessageParam`、`Anthropic.Tool`、`Anthropic.Message` 等），而不是重新定义等价接口。
- **不要为 SDK 数据结构定义自定义类型：**SDK 导出了所有 API 对象的类型。消息使用 `Anthropic.MessageParam`，工具定义使用 `Anthropic.Tool`，工具结果使用 `Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam`，响应使用 `Anthropic.Message`。自行定义 `interface ChatMessage { role: string; content: unknown }` 会重复 SDK 已提供的内容，并降低类型安全性。
- **报告和文档输出：**对于生成报告、文档或可视化的任务，代码执行沙箱已预装 `python-docx`、`python-pptx`、`matplotlib`、`pillow` 和 `pypdf`。Claude 可以生成格式化文件（DOCX、PDF、图表）并通过 Files API 返回——对于“报告”或“文档”类请求，请考虑使用这种方式，而不是仅输出纯 stdout 文本。
