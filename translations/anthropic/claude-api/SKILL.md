<!-- source-sha256: 1d08b3be1c02b6bd2d8c966b1645e234fbb36454d2dd4cbd39802d2f321bd0f4 -->
---
name: claude-api
description: |-
  Claude API / Anthropic SDK 参考资料——涵盖模型 ID、定价、参数、流式传输、工具使用、MCP、智能体、缓存、Token 计数和模型迁移。
  触发条件——在打开目标文件之前阅读；不要因为它“看起来只有一行”就跳过——适用于以下任何情况：提示以任何形式提及 Claude/Anthropic（Claude、Anthropic、Fable、Opus、Sonnet、Haiku、`anthropic`、`@anthropic-ai`、`claude-*`、`us.anthropic.*`、`[1m]`）；用户询问 LLM（定价/模型选择/限制/缓存）——绝不要凭记忆回答；或者任务具有 LLM 特征但未说明提供商（智能体/MCP/工具定义/多智能体/RAG/LLM 评判器/计算机使用；对自然语言进行生成/总结/提取/分类/改写/对话；调试拒绝/截断/流式传输/工具调用/Token）。
  仅在处理其他提供商时跳过（优先于所有触发条件）：查询中提及 OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama；或者对项目运行 `grep -rE 'openai|langchain_openai|google.generativeai|genai|mistralai|cohere|ollama'` 有匹配结果（如果未指定提供商，先运行此 grep——不要读取文件）。
license: 完整条款见 LICENSE.txt
---

# 使用 Claude 构建 LLM 驱动的应用程序

此技能帮助你使用 Claude 构建 LLM 驱动的应用程序。根据需求选择合适的使用界面，检测项目语言，然后阅读相关的语言专用文档。

## 开始之前

扫描目标文件（如果没有目标文件，则扫描提示和项目），寻找非 Anthropic 提供商标记——`import openai`、`from openai`、`langchain_openai`、`OpenAI(`、`gpt-4`、`gpt-5`、类似 `agent-openai.py` 或 `*-generic.py` 的文件名，或者任何明确要求代码保持提供商中立的指令。如果发现任何此类标记，请停止并告诉用户此技能会生成 Claude/Anthropic SDK 代码；询问他们是希望将文件切换到 Claude，还是需要非 Claude 实现。不要使用 Anthropic SDK 调用编辑非 Anthropic 文件。

## 输出要求

当用户要求添加、修改或实现 Claude 功能时，你的代码必须通过以下方式之一调用 Claude：

1. 项目语言对应的**官方 Anthropic SDK**（`anthropic`、`@anthropic-ai/sdk`、`com.anthropic.*` 等）。只要项目存在受支持的 SDK，就默认使用此方式。
2. **原始 HTTP**（`curl`、`requests`、`fetch`、`httpx` 等）——仅当用户明确要求 cURL/REST/原始 HTTP、项目本身是 shell/cURL 项目，或者该语言没有官方 SDK 时使用。

绝不要混用两者——不要仅仅因为 `requests`/`fetch` 看起来更轻量，就在 Python 或 TypeScript 项目中使用它们。绝不要退回到 OpenAI 兼容垫片。

**绝不要猜测 SDK 用法。**函数名、类名、命名空间、方法签名和导入路径必须来自明确的文档——可以是此技能中的 `{lang}/` 文件，也可以是 `shared/live-sources.md` 中列出的官方 SDK 仓库或文档链接。如果所需的语言绑定未在技能文件中明确记录，请在编写代码前通过 WebFetch 获取 `shared/live-sources.md` 中对应的 SDK 仓库。不要根据 cURL 结构或其他语言的 SDK 推断 Ruby/Java/Go/PHP/C# API。

**如果 WebFetch 或仓库访问失败**（网络受限、超时、克隆被阻止）：不要持续重试——根据 `{lang}/` 文件中的模式和命名空间/包表编写代码，使用编译器或解释器运行它，并根据错误输出迭代。对于静态类型 SDK（C#、Java、Go），根据本地错误进行编译修复循环，比受阻的网络调研更快得到可运行代码。

## 默认设置

除非用户另有要求：

Claude 模型版本请使用 Claude Opus 4.8，其精确模型字符串为 `claude-opus-4-8`。对于任何稍显复杂的任务，请默认使用自适应思考（`thinking: {type: "adaptive"}`）。最后，对于可能涉及长输入、长输出或较高 `max_tokens` 的请求，请默认使用流式传输——这可以避免请求超时。如果不需要处理单独的流事件，请使用 SDK 的 `.get_final_message()` / `.finalMessage()` 辅助方法获取完整响应。

## ⚠️ API 演变——你的训练先验可能已经过时

Claude API 的若干常见形式在 2025–2026 年发生了变化。如果你从训练中记得某种模式，请在编写代码前对照此技能中的 `{lang}/` 文件进行验证——下表列出了最常见的变化点：

| 领域 | 过时的先验 | 当前 API |
|---|---|---|
| 扩展思考 | `thinking: {type: "enabled", budget_tokens: N}` | 在 Claude 4.6+ 模型上：`thinking: {type: "adaptive"}`。`budget_tokens` 在 Opus 4.6 / Sonnet 4.6 上已弃用，并且在 Fable 5 / Sonnet 5 / Opus 4.8 / 4.7 上会**以 400 错误被拒绝**。4.6 之前的模型仍使用 `budget_tokens`。 |
| Web 搜索/Web 获取工具类型 | `web_search_20250305`、`web_fetch_20250910` | Opus 4.8/4.7/4.6、Sonnet 5 和 Sonnet 4.6 使用 `web_search_20260209`、`web_fetch_20260209`（动态过滤）。旧模型继续使用基础变体；Vertex AI 仅提供基础 `web_search_20250305`（Vertex 不提供 Web 获取）——参见下方的服务器工具快速参考。 |
| PHP 参数名 | 使用 snake_case 传输字段作为命名参数（`max_tokens`） | 顶层命名参数使用 camelCase（`maxTokens`）。嵌套数组键因功能而异（例如 `'taskBudget'`、`'skillID'`、`'mcp_server_name'`）——请从文档示例中复制精确键名；不要批量转换。 |

此技能中的 `{lang}/` 文件优先于记忆中的模式。

---

## 子命令

如果此提示底部的用户请求只是一个裸子命令字符串（没有说明文字），请搜索本文档中的每个 **Subcommands** 表——包括下方追加章节中的表——并直接执行匹配的 Action 列。这样用户可以通过 `/claude-api <subcommand>` 调用特定流程。如果文档中的表均不匹配，则将请求视为普通说明文字。

| 子命令 | 操作 |
|---|---|
| `migrate` | 将现有 Claude API 代码迁移到更新的模型。**立即阅读 `shared/model-migration.md`**并按顺序执行：步骤 0（确认范围——进行任何编辑前先询问要处理哪些文件/目录）、步骤 1（对每个文件分类），然后执行每个目标对应的破坏性变更章节。不要总结指南——直接执行。如果用户未指定目标模型，请在询问范围的同一轮中询问要迁移到哪个模型。 |

---

## 语言检测

阅读代码示例前，先确定用户正在使用哪种语言：

1. **查看项目文件**以推断语言：

   - `*.py`、`requirements.txt`、`pyproject.toml`、`setup.py`、`Pipfile` → **Python**——读取 `python/`
   - `*.ts`、`*.tsx`、`package.json`、`tsconfig.json` → **TypeScript**——读取 `typescript/`
   - `*.js`、`*.jsx`（不存在 `.ts` 文件）→ **TypeScript**——JS 使用相同的 SDK，读取 `typescript/`
   - `*.java`、`pom.xml`、`build.gradle` → **Java**——读取 `java/`
   - `*.kt`、`*.kts`、`build.gradle.kts` → **Java**——Kotlin 使用 Java SDK，读取 `java/`
   - `*.scala`、`build.sbt` → **Java**——Scala 使用 Java SDK，读取 `java/`
   - `*.go`、`go.mod` → **Go**——读取 `go/`
   - `*.rb`、`Gemfile` → **Ruby**——读取 `ruby/`
   - `*.cs`、`*.csproj` → **C#**——读取 `csharp/`
   - `*.php`、`composer.json` → **PHP**——读取 `php/`

2. **如果检测到多种语言**（例如同时存在 Python 和 TypeScript 文件）：

   - 检查用户当前文件或问题涉及哪种语言
   - 如果仍不明确，请询问：“我同时检测到了 Python 和 TypeScript 文件。你使用哪种语言进行 Claude API 集成？”

3. **如果无法推断语言**（空项目、没有源文件或语言不受支持）：

   - 使用 AskUserQuestion，并提供以下选项：Python、TypeScript、Java、Go、Ruby、cURL/raw HTTP、C#、PHP
   - 如果 AskUserQuestion 不可用，则默认使用 Python 示例，并注明：“以下展示 Python 示例。如果你需要其他语言，请告诉我。”

4. **如果检测到不受支持的语言**（Rust、Swift、C++、Elixir 等）：

   - 建议使用 `curl/` 中的 cURL/原始 HTTP 示例，并说明可能存在社区 SDK
   - 提议提供 Python 或 TypeScript 示例作为参考实现

5. **如果用户需要 cURL/原始 HTTP 示例**，读取 `curl/`。

### 各语言功能支持

| 语言       | 工具运行器 | 托管智能体 | 备注                                  |
| ---------- | ---------- | ---------- | ------------------------------------- |
| Python     | 是（Beta） | 是（Beta） | 完整支持——`@beta_tool` 装饰器         |
| TypeScript | 是（Beta） | 是（Beta） | 完整支持——`betaZodTool` + Zod         |
| Java       | 是（Beta） | 是（Beta） | 使用注解类的 Beta 工具调用            |
| Go         | 是（Beta） | 是（Beta） | `toolrunner` 包中的 `BetaToolRunner`  |
| Ruby       | 是（Beta） | 是（Beta） | Beta 中的 `BaseTool` + `tool_runner`  |
| C#         | 是（Beta） | 是（Beta） | `BetaToolRunner` + 原始 JSON schema   |
| PHP        | 是（Beta） | 是（Beta） | `BetaRunnableTool` + `toolRunner()`   |
| cURL       | 不适用     | 是（Beta） | 原始 HTTP，无 SDK 功能                |

> **托管智能体代码示例**：为 Python、TypeScript、Go、Ruby、PHP、Java 和 cURL 提供了专用的语言特定 README（`{lang}/managed-agents/README.md`、`curl/managed-agents.md`）。请阅读对应语言的 README，以及与语言无关的 `shared/managed-agents-*.md` 概念文件。**智能体是持久化的——创建一次，之后通过 ID 引用。**保存 `agents.create` 返回的智能体 ID，并将其传给之后的每次 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是通过版本控制的 YAML 创建智能体和环境的一种便捷方式——参见 `shared/anthropic-cli.md`。如果 README 中没有展示所需的语言绑定，请通过 WebFetch 获取 `shared/live-sources.md` 中的相关条目，不要猜测。C# 通过 `client.Beta.Agents` 和相关命名空间提供 Beta 托管智能体支持。

---

## 我应该使用哪种使用界面？

> **从简单开始。**默认选择能够满足需求的最简单层级。单次 API 调用和工作流可以处理大多数用例——只有当任务确实需要开放式、模型驱动的探索时，才使用智能体。

| 用例                                            | 层级         | 推荐使用界面               | 原因                                                         |
| ----------------------------------------------- | ------------ | -------------------------- | ------------------------------------------------------------ |
| 分类、总结、提取、问答                          | 单次 LLM 调用 | **Claude API**             | 一次请求，一次响应                                           |
| 批处理或嵌入                                    | 单次 LLM 调用 | **Claude API**             | 专用端点                                                     |
| 使用代码控制逻辑的多步骤流水线                  | 工作流       | **Claude API + 工具使用**  | 由你编排循环                                                 |
| 使用自有工具的自定义智能体                      | 智能体       | **Claude API + 工具使用**  | 灵活性最高                                                   |
| 具有工作区、由服务器管理的有状态智能体          | 智能体       | **托管智能体**             | Anthropic 运行循环并托管工具执行沙箱                         |
| 持久化且带版本的智能体配置                      | 智能体       | **托管智能体**             | 智能体是已存储的对象；会话固定到某个版本                     |
| 带有文件挂载的长时间运行多轮智能体              | 智能体       | **托管智能体**             | 每会话容器、SSE 事件流、Skills + MCP                         |

> **注意：**当你希望 Anthropic 既运行智能体循环，**又**托管执行工具的容器时，托管智能体是正确选择——文件操作、bash、代码执行都在每会话工作区中运行。如果你希望自行托管计算资源或运行自己的自定义工具运行时，则 Claude API + 工具使用是正确选择——可以使用工具运行器自动处理循环，也可以使用手动循环实现细粒度控制（审批门、定制日志、条件执行）。

> **云提供商访问。****AWS 上的 Claude Platform** 由 Anthropic 运营，可在同一天实现 API 功能对齐——客户端设置参见 `shared/claude-platform-on-aws.md`。有关 **AWS 上的 Claude Platform**、**Amazon Bedrock**、**Google Vertex AI** 和 **Microsoft Foundry** 中各功能的可用性，请参阅 `shared/platform-availability.md`——该表是此技能中的唯一事实来源；不要从其他地方推断可用性。

### 决策树

```
你的应用程序需要什么？

0. 使用哪个提供商？
   ├── 第一方 API 或 AWS 上的 Claude Platform → 继续（完整使用界面可用；各功能例外见 shared/platform-availability.md）。
   └── Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry → Claude API（智能体使用工具调用）；各功能支持见 shared/platform-availability.md。

1. 单次 LLM 调用（分类、总结、提取、问答）
   └── Claude API——一次请求，一次响应

2. 你是否希望 Anthropic 运行智能体循环并托管每会话
   容器，让 Claude 在其中执行工具（bash、文件操作、代码）？
   └── 是 → 托管智能体——服务器管理的会话、持久化智能体配置、
       SSE 事件流、Skills + MCP、文件挂载。
       示例：“每个任务都有一个工作区的有状态编码智能体”、
             “向 UI 流式发送事件的长时间运行研究智能体”、
             “具有持久化、带版本配置并供多个会话使用的智能体”

3. 工作流（多步骤、由代码编排、使用你自己的工具）
   └── 使用工具调用的 Claude API——由你控制循环

4. 开放式智能体（模型决定自己的行动轨迹、使用你自己的工具、由你托管计算资源）
   └── Claude API 智能体循环（灵活性最高）
```

### 我应该构建智能体吗？

选择智能体层级之前，请检查以下四项标准：

- **复杂性**——任务是否包含多个步骤，且难以提前完整规定？（例如“把这份设计文档变成 PR”，而不是“从这个 PDF 中提取标题”）
- **价值**——结果是否值得更高的成本和延迟？
- **可行性**——Claude 是否擅长此类任务？
- **错误成本**——错误能否被发现并恢复？（测试、审查、回滚）

如果其中任何一项的答案为“否”，请继续使用更简单的层级（单次调用或工作流）。

---

## 架构

所有内容都通过 `POST /v1/messages`。工具和输出约束都是这一端点的功能——不是独立的 API。

**用户定义的工具**——你通过装饰器、Zod schema 或原始 JSON 定义工具，SDK 的工具运行器负责调用 API、执行函数并循环，直到 Claude 完成。若需要完全控制，也可以手动编写循环。

**服务器端工具**——由 Anthropic 托管并在 Anthropic 基础设施上运行的工具。代码执行完全在服务器端完成（在 `tools` 中声明，Claude 会自动运行代码）。计算机使用既可以由服务器托管，也可以自行托管。

**结构化输出**——约束 Messages API 的响应格式（`output_config.format`）和/或工具参数验证（`strict: true`）。推荐使用 `client.messages.parse()`，它会自动根据你的 schema 验证响应。注意：旧的 `output_format` 参数已弃用；请在 `messages.create()` 上使用 `output_config: {format: {...}}`。

**辅助端点**——批处理（`POST /v1/messages/batches`）、文件（`POST /v1/files`）、Token 计数（`POST /v1/messages/count_tokens`——参见 `shared/token-counting.md`）和模型（`GET /v1/models`、`GET /v1/models/{id}`——实时发现能力/上下文窗口）为 Messages API 请求提供数据或支持。

---

## 当前模型（缓存日期：2026-06-24）

| 模型              | 模型 ID             | 上下文         | 输入 $/1M | 输出 $/1M |
| ----------------- | ------------------- | -------------- | --------- | --------- |
| Claude Fable 5    | `claude-fable-5`    | 1M             | $10.00    | $50.00    |
| Claude Mythos 5（仅限 Project Glasswing） | `claude-mythos-5` | 1M | $10.00 | $50.00 |
| Claude Opus 4.8   | `claude-opus-4-8`   | 1M             | $5.00     | $25.00    |
| Claude Opus 4.7   | `claude-opus-4-7`   | 1M             | $5.00     | $25.00    |
| Claude Opus 4.6   | `claude-opus-4-6`   | 1M             | $5.00     | $25.00    |
| Claude Sonnet 5   | `claude-sonnet-5`   | 1M             | $3.00（截至 2026-08-31 的首发价为 $2.00） | $15.00（首发价为 $10.00） |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M             | $3.00     | $15.00    |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00     | $5.00     |

**除非用户明确指定其他模型，否则始终使用 `claude-opus-4-8`。**这一点不可妥协。除非用户明确说“use sonnet”或“use haiku”，否则不要使用 `claude-sonnet-5`、`claude-sonnet-4-6` 或任何其他模型。绝不要为了成本而降级——这是用户的决定，不是你的决定。仅当用户明确要求 Claude Fable 5、“fable”或 Anthropic 最强大的模型时，才使用 `claude-fable-5`——它与 Opus 系列有不同的 API 行为（见下文），且价格高于 Opus 层级。

### Claude Fable 5（`claude-fable-5`）——公开广泛发布的最强大模型

Claude Fable 5 是 Anthropic 公开广泛发布的最强大模型，适用于要求最高的推理和长周期智能体工作。**Claude Mythos 5**（`claude-mythos-5`）通过 Project Glasswing 提供相同的能力、定价和 API 使用界面（参与该项目是唯一的访问方式），接替仅限邀请的 Claude Mythos Preview（`claude-mythos-preview`）——以下所有内容均适用于这两个模型。上下文窗口为 1M（最大值同时也是默认值），最大输出为 128K。与 Opus 层级相比的主要 API 差异如下——详情参见 `shared/model-migration.md` → Migrating to Claude Fable 5：

- **思考始终开启**——完全省略 `thinking` 参数（或发送 `{type: "adaptive"}`）。任何其他显式配置都会被拒绝：`{type: "disabled"}` 和 `{type: "enabled", budget_tokens: N}` 都会返回 400。使用 `output_config.effort` 控制深度（支持从 `low` 到 `xhigh` 以及 `max`）。
- **永远不会返回原始思维链**——响应携带常规 `thinking` 块（不是 `redacted_thinking`）：`display: "summarized"` 返回可读的推理摘要，`"omitted"`（默认值）会将 `thinking` 字段留为空字符串。重放规则：在同一模型上，将思考块完全按收到的样子传回（包括空文本块——API 拒绝的是被修改的块，而不是已读取的块）；**不同**模型会将它们从提示中**丢弃**（通常静默进行——不会报错；丢弃发生在计费前，因此被丢弃的块不计费，也无需手动移除）。其他模型的常规思考块可以在模型之间自由重放。
- **分词器**——与 Opus 4.8 使用相同的分词器（在 Opus 4.7 中引入）。从 Opus 4.7/4.8 迁移时，Token 数量大致不变；每 Token 定价不同。从 Opus 4.6、Sonnet、Haiku 或更早模型迁移时，请使用 `count_tokens` 重新建立基线。
- **`refusal` 停止原因——处理它，并默认选择加入回退机制**——安全分类器可能拒绝请求（HTTP 200，`stop_reason: "refusal"`，并带有 `stop_details` 类别）。输出前拒绝的 `content` 数组为空，且完全不计费；流式传输中途拒绝会对已经传输的输出计费——请丢弃部分输出。读取 `content` 前始终检查 `stop_reason`。恢复机制在 **API 中是选择加入的**：大多数 Claude 消费端使用界面内置 Claude Opus 4.8 回退，但未选择加入的 API 请求在遇到拒绝时会直接停止——而针对无害的相邻领域工作（安全工具、生命科学任务）的误报确实可能发生。**编写 `claude-fable-5` 代码时，默认包含服务器端 `fallbacks` 参数**（`betas: ["server-side-fallback-2026-06-01"]` + `fallbacks: [{"model": "claude-opus-4-8"}]`；适用于 Claude API 和 AWS 上的 Claude Platform）：被拒绝的请求会在同一次调用中由回退模型透明地重新处理，并自动应用抵扣式重新计价（输出前拒绝不计费；救援请求按回退模型自身费率计费）。告诉用户你已启用该功能；仅当用户拒绝时才移除。GA SDK 的客户端 `BetaRefusalFallbackMiddleware` + `BetaFallbackState` 可在所有不支持服务器端回退的平台上处理重试（包括 Amazon Bedrock、Vertex AI、Microsoft Foundry）；回退额度会退还客户端重试中因切换缓存产生的成本。代码示例参见对应语言 claude-api 文档中的 Refusal Fallbacks 章节；完整语义参见迁移指南的拒绝章节。
- **不支持 assistant 预填充**——与 4.6+ 系列的其他模型相同。
- **要求保留数据 30 天**——Claude Fable 5 不适用于零数据保留；如果组织的保留配置不满足要求，请求会返回 `400 invalid_request_error`。
- **更长的轮次、不同的提示方式**——困难任务的单次请求可能运行数分钟（请规划超时/流式传输/进度用户体验）；常规工作的 effort 扫描应包含 low/medium；为旧模型编写的提示往往过于规定性，会降低输出质量。推荐的提示片段（避免过度规划、不整理无关内容、基于事实报告进度、边界、异步子智能体、记忆、`send_to_user`）参见 `shared/model-migration.md` → Migrating to Claude Fable 5 → Behavioral shifts (prompt-tunable)。

**关键：只能使用上表中的精确模型 ID 字符串——它们本身就是完整的。不要追加日期后缀。**例如，使用 `claude-sonnet-4-6`，绝不要使用 `claude-sonnet-4-6-20251114` 或训练数据中可能记得的任何其他带日期后缀的变体。如果用户要求使用表中没有的旧模型（例如“opus 4.5”“sonnet 3.7”），请读取 `shared/models.md` 获取精确 ID——不要自行构造。

注意：如果上面的某些模型字符串对你来说很陌生，这是正常的——这只说明它们是在你的训练数据截止日期之后发布的。请放心，它们都是真实模型；我们不会拿这种事开玩笑。

**实时能力查询：**上表是缓存数据。当用户询问“X 的上下文窗口是多少”“X 是否支持视觉/思考/effort”或“哪些模型支持 Y”时，请查询 Models API（`client.models.retrieve(id)` / `client.models.list()`）——字段参考和能力筛选示例见 `shared/models.md`。

---

## 身份验证（快速参考）

**未设置 `ANTHROPIC_API_KEY` 并不意味着没有凭据。**SDK 和 `ant` CLI 按以下顺序解析凭据（第一个匹配项优先）：`ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → 由 `ANTHROPIC_PROFILE` 选择或通过 `ant auth login` 激活的 OAuth 配置文件 → Workload Identity Federation 环境变量 → 磁盘上的默认配置文件。执行 `ant auth login` 后，无需设置环境变量，裸 `Anthropic()` / `new Anthropic()` / `anthropic.NewClient()` 即可工作。

**当你需要调用 API 而 `ANTHROPIC_API_KEY` 未设置时，不要向用户索要密钥。**先运行 `ant auth status`——它会显示当前使用的凭据来源和配置文件。如果它报告存在活动配置文件：

- **SDK 代码或 `ant` CLI：**直接运行。零参数客户端构造函数和每个 `ant …` 子命令都会自动读取该配置文件——不需要环境变量。
- **原始 `curl` / HTTP：**使用 `ant auth print-credentials --access-token` 获取短期 Token，并将其作为 `Authorization: Bearer <token>` 发送，**同时**添加请求头 `anthropic-beta: oauth-2025-04-20`（OAuth Token 放在 `Authorization: Bearer` 中，而不是 `x-api-key:` 中——将 curl 从 API 密钥转换为 OAuth 是更改请求头，而不是替换密钥）。始终传入 `--access-token`；不带标志的形式输出 JSON，而不是裸 Token。

只有当 `ant auth status` 报告没有活动凭据来源（或者根本未安装 `ant`）时，才向用户索要密钥。优先建议使用 `ant auth login`——它会将配置文件存储在 `~/.config/anthropic/` 下，SDK 会自动读取——也可选择导出 `ANTHROPIC_API_KEY`。

完整身份验证细节（命名配置文件、作用域、API 密钥遮蔽配置文件的陷阱、刷新 Token 过期）：`shared/anthropic-cli.md`。

---

## 思考与 Effort（快速参考）

**Fable 5 / Opus 4.8 / 4.7 / Sonnet 5——仅支持自适应思考：**使用 `thinking: {type: "adaptive"}`。`thinking: {type: "enabled", budget_tokens: N}` 会返回 400——adaptive 是唯一的开启模式。在 Opus 4.8、Opus 4.7 和 Sonnet 5 上，`{type: "disabled"}` 和省略 `thinking` 都可用（在 Sonnet 5 上，省略后会运行 adaptive；在 Opus 4.7/4.8 上，省略后不进行思考——请显式设置 `{type: "adaptive"}`）；在 Fable 5 上，显式 `{type: "disabled"}` 会返回 400——应完全省略 `thinking` 参数。采样参数（`temperature`、`top_p`、`top_k`）也已移除，使用时会返回 400。Opus 4.8 保持与 4.7 相同的请求使用界面（没有新的破坏性变更）——从 4.6 或更早版本迁移时，行为重新调优见 `shared/model-migration.md` → Migrating to Opus 4.8，完整破坏性变更列表见 → Migrating to Opus 4.7。注意：禁用 `thinking` 后，Opus 4.8 可能会在可见响应中写出更长的推理过程——请保持开启自适应思考，或添加仅输出最终答案的指令（参见迁移指南）。

**Opus 4.6——自适应思考（推荐）：**使用 `thinking: {type: "adaptive"}`。Claude 会动态决定何时思考以及思考多少。不需要 `budget_tokens`——`budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上已弃用，不应在新代码中使用。自适应思考也会自动启用交错思考（无需 Beta 请求头）。**当用户要求“扩展思考”“思考预算”或 `budget_tokens` 时：始终使用 Fable 5、Opus 4.8、4.7 或 4.6，并设置 `thinking: {type: "adaptive"}`。固定思考 Token 预算的概念已弃用——由自适应思考取代。不要在新的 4.6/4.7/4.8 代码中使用 `budget_tokens`，也不要切换到旧模型。** *渐进迁移例外：*作为过渡性逃生口，`budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上仍然有效——如果正在迁移现有代码，并且在调优 `effort` 前需要硬性 Token 上限，请参阅 `shared/model-migration.md` → Transitional escape hatch。注意：此例外**不适用于** Fable 5、Opus 4.7 或 4.8——这些模型已完全移除 `budget_tokens`。

**Effort 参数（GA，无需 Beta 请求头）：**通过 `output_config: {effort: "low"|"medium"|"high"|"max"}` 控制思考深度和总体 Token 消耗（位于 `output_config` 内，而不是顶层）。默认值是 `high`（等同于省略）。Fable 5、Opus 4.6 及更高版本、Sonnet 5 和 Sonnet 4.6 支持 `max`（Haiku 或更早的 Sonnet 不支持）。Opus 4.7 新增了 `"xhigh"`（位于 `high` 和 `max` 之间）——对于 Fable 5 / Opus 4.7/4.8 / Sonnet 5 上的大多数编码和智能体用例，这是最佳设置，也是 Claude Code 的默认值；对于大多数对智能水平敏感的工作，至少使用 `high`。适用于 Fable 5、Opus 4.5、Opus 4.6、Opus 4.7、Opus 4.8、Sonnet 5 和 Sonnet 4.6。在 Sonnet 4.5 / Haiku 4.5 上会报错。在 Fable 5、Opus 4.7/4.8 和 Sonnet 5 上，effort 的影响比其层级中任何旧模型都更大——迁移时请重新调优，并使用 `high`/`xhigh` 运行长周期/智能体任务，同时预先提供完整任务说明。与自适应思考结合可获得最佳成本质量权衡。较低 effort 意味着更少且更合并的工具调用、更少的前言和更简短的确认——`high` 通常是平衡质量和 Token 效率的最佳点；当正确性比成本更重要时使用 `max`；对子智能体或简单任务使用 `low`。

**思考显示——Fable 5 / Mythos 5 / Opus 4.8 / 4.7 / Sonnet 5 默认为 `"omitted"`：**`display: "summarized"` 返回可读的推理摘要；`"omitted"`（这五个模型的默认值——与 Opus 4.6 和 Sonnet 4.6 默认为 `"summarized"` 相比，这是一次静默变更）会流式发送文本为空的 `thinking` 块。`display` 只控制可见性——无论采用何种设置，思考都会进行且计费相同；任何模型都不会公开原始思维链。如果向用户流式传输推理，默认行为看起来会像输出前长时间停顿——请显式设置 `thinking: {type: "adaptive", display: "summarized"}`。（与显示设置无关，在同一模型上继续时请原样回传思考块；其他模型会静默忽略它们——参见迁移指南。）

**任务预算（Beta，Fable 5 / Opus 4.7 / 4.8 / Sonnet 5）：**`output_config: {task_budget: {type: "tokens", total: N}}` 告诉模型整个智能体循环可使用多少 Token——模型会看到持续倒计时并自我调节（最少 20,000；Beta 请求头 `task-budgets-2026-03-13`）。这与 `max_tokens` 不同，后者是模型无法感知的、对每次响应强制执行的上限。参见 `shared/model-migration.md` → Task Budgets。

**Sonnet 4.6：**支持自适应思考（`thinking: {type: "adaptive"}`）。`budget_tokens` 在 Sonnet 4.6 上已弃用——请改用自适应思考。

**旧模型（仅在明确要求时）：**如果用户明确要求 Sonnet 4.5 或其他旧模型，请使用 `thinking: {type: "enabled", budget_tokens: N}`。`budget_tokens` 必须小于 `max_tokens`（最小值为 1024）。绝不要因为用户提到 `budget_tokens` 就选择旧模型——应改用带自适应思考的 Opus 4.8。

---

## 压缩（快速参考）

**Beta，适用于 Fable 5、Opus 4.8、Opus 4.7、Opus 4.6、Sonnet 5 和 Sonnet 4.6。**对于可能超过 1M 上下文窗口的长时间运行对话，请启用服务器端压缩。当接近触发阈值（默认 150K Token）时，API 会自动总结较早的上下文。需要 Beta 请求头 `compact-2026-01-12`。

**关键：**每一轮都要将 `response.content`（而不只是文本）追加回消息。必须保留响应中的压缩块——API 会在下一次请求中使用它们替换已压缩的历史记录。仅提取文本字符串并追加，会静默丢失压缩状态。

代码示例见 `{lang}/claude-api/README.md`（Compaction 章节）。完整文档可通过 WebFetch 从 `shared/live-sources.md` 获取。

---

## 提示缓存（快速参考）

**前缀匹配。**前缀中任何位置的任意字节变化，都会使其后所有内容失效。渲染顺序是 `tools` → `system` → `messages`。将稳定内容放在前面（固定的 system prompt、确定性的工具列表），将易变内容（时间戳、每请求 ID、变化的问题）放在最后一个 `cache_control` 断点之后。

**对话中途操作员指令**（仅 Claude Opus 4.8；无需 Beta 请求头）：将 `{"role": "system", ...}` 追加到 `messages[]`，不要编辑顶层 `system`。这样可以保留已缓存的历史前缀，并提供防提示注入的操作员通道。参见 `shared/prompt-caching.md` § Mid-conversation system messages。

当不需要精细放置时，**顶层自动缓存**（在 `messages.create()` 上设置 `cache_control: {type: "ephemeral"}`）是最简单的选择。每个请求最多 4 个断点。可缓存前缀最少约为 1024 Token——更短的前缀不会缓存，且不会报错。

**使用 `usage.cache_read_input_tokens` 验证**——如果重复请求时它始终为零，则存在静默失效因素（system prompt 中的 `datetime.now()`、未排序 JSON、变化的工具集）。

有关放置模式、架构指导和静默失效因素审计检查表，请阅读 `shared/prompt-caching.md`。语言特定语法见 `{lang}/claude-api/README.md`（Prompt Caching 章节）。

---

## 快速模式（快速参考）

**研究预览，仅限 Opus 4.8 / 4.7。**Opus 4.7 的快速模式已弃用——移除后，在 4.7 上设置 `speed: "fast"` 会返回错误。Opus 4.8 是持久支持快速模式的层级。快速模式运行相同模型，输出 Token 速度最高可提高至 2.5 倍，但按溢价计费。每个请求都必须满足三项要求：使用 **Beta** messages 端点（`client.beta.messages.…`）、传入 Beta 标志 `fast-mode-2026-02-01`，并将 `speed: "fast"` 设置为顶层请求参数（不是请求头，也不在 `extra_body` 中）。

```python
client.beta.messages.create(
    model="claude-opus-4-8", max_tokens=4096,
    speed="fast", betas=["fast-mode-2026-02-01"],
    messages=[...],
)
```

| 语言 | Beta 标志 | Speed 参数 |
|---|---|---|
| Python | `betas=["fast-mode-2026-02-01"]` | `speed="fast"` |
| TypeScript / Ruby | `betas: ["fast-mode-2026-02-01"]` | `speed: "fast"` |
| Go | `[]anthropic.AnthropicBeta{anthropic.AnthropicBetaFastMode2026_02_01}` | `Speed: anthropic.BetaMessageNewParamsSpeedFast` |
| Java | `.addBeta(AnthropicBeta.FAST_MODE_2026_02_01)` | `.speed(MessageCreateParams.Speed.FAST)` |
| C# | `Betas = ["fast-mode-2026-02-01"]` | `Speed = Speed.Fast`（`Anthropic.Models.Beta.Messages`） |
| PHP | `betas: ['fast-mode-2026-02-01']` | `speed: 'fast'` |
| cURL | `anthropic-beta: fast-mode-2026-02-01` 请求头 | 请求体中的 `"speed": "fast"` |

`response.usage.speed` 会报告实际使用的速度。快速模式有独立于标准 Opus 的速率限制；遇到 429 时，可以等待 `retry-after` 指定的延迟后重试，也可以移除 `speed` 并回退到标准模式（注意：切换速度会使提示缓存失效）。不适用于 Batch API、Priority Tier、AWS 上的 Claude Platform 或第三方平台。

---

## 任务预算（快速参考）

**Beta，适用于 Fable 5 / Sonnet 5 / Opus 4.8 / 4.7。**任务预算为 Claude 的智能体循环提供 Token 上限，使其能够调整节奏并妥善完成，而不是被突然截断。在 `client.beta.messages.stream(...)` 的 `output_config` 中设置 `task_budget`，并使用 Beta 标志 `task-budgets-2026-03-13`——请使用流式传输，以免较大的 `max_tokens` 导致 HTTP 超时：

```python
with client.beta.messages.stream(
    model="claude-opus-4-8", max_tokens=128000,
    output_config={"effort": "high", "task_budget": {"type": "tokens", "total": 64000}},
    betas=["task-budgets-2026-03-13"],
    messages=[...], tools=[...],
) as stream:
    response = stream.get_final_message()
```

`task_budget` 字段包括：`type`（始终为 `"tokens"`）、`total`，以及可选的 `remaining`（默认为 `total`）。服务器会注入 Claude 在生成期间可见的倒计时标记；预算计算的是 Claude 生成的内容和它本轮读取的工具结果——**不是**每次请求重新发送的完整历史记录。

**观察消耗：**如果要显示进度，请在循环迭代间累计 `response.usage.output_tokens`（再加上你追加的工具结果块的 Token 数量）。在正常循环中不要设置 `remaining`——服务器会自行跟踪倒计时；如果既传入客户端计算的 `remaining`，又重新发送完整历史记录，预算会被低估。**只有当你在请求之间压缩或重写历史记录、导致服务器无法再推导先前消耗时，才传入 `remaining`。**

---

## 提供商客户端（快速参考）

在第三方平台上使用 Claude 时，请使用该平台专用的客户端类——不要使用带 `base_url` 覆盖的第一方 `Anthropic()` 客户端。构造后，客户端会公开与第一方 SDK 相同的 `messages.create` / `.stream` 使用界面。

### Amazon Bedrock

使用 **Mantle** 客户端（Messages API Bedrock 端点）。Bedrock 模型 ID 带有 `anthropic.` 前缀（例如 `"anthropic.claude-opus-4-8"`）。必须指定区域。

| 语言 | 客户端 |
|---|---|
| Python | `from anthropic import AnthropicBedrockMantle` → `AnthropicBedrockMantle(aws_region="…")` |
| TypeScript | `import { AnthropicBedrockMantle } from "@anthropic-ai/bedrock-sdk"` → `new AnthropicBedrockMantle({ awsRegion: "…" })` |
| Go | `bedrock.NewMantleClient(ctx, bedrock.MantleClientConfig{ AWSRegion: "…" })` |
| Java | `AnthropicOkHttpClient.builder().backend(BedrockMantleBackend.fromEnv()).build()`（来自 `com.anthropic.bedrock.backends`） |
| C# | `new AnthropicBedrockMantleClient(new() { AwsRegion = "…" })`（包 `Anthropic.Bedrock`） |
| PHP | `use Anthropic\Bedrock\MantleClient;` → `new MantleClient(awsRegion: '…')` |
| Ruby | `Anthropic::BedrockMantleClient.new(aws_region: "…")` |

`AnthropicBedrock` / `BedrockClient` / `BedrockBackend`（不含 `Mantle`）是旧版 `bedrock-runtime` InvokeModel 路径——新代码应优先使用 Mantle 客户端。

### Microsoft Foundry

| 语言 | 客户端 |
|---|---|
| Python | `from anthropic import AnthropicFoundry` → `AnthropicFoundry(api_key=…, resource="…")` |
| TypeScript | `import AnthropicFoundry from "@anthropic-ai/foundry-sdk"` → `new AnthropicFoundry({ … })` |
| Java | `AnthropicOkHttpClient.builder().backend(FoundryBackend.fromEnv()).build()`（来自 `com.anthropic.foundry.backends`） |
| C# | `new AnthropicFoundryClient(new AnthropicFoundryApiKeyCredentials(…))`（包 `Anthropic.Foundry`） |
| PHP | `Foundry\Client::withCredentials(…)` |

Go 和 Ruby SDK 当前不支持 Foundry。Ruby 可回退使用标准的 `Anthropic::Client.new(base_url: "<foundry endpoint>")`（未内置 Entra ID 身份验证）。AWS 上的 Claude Platform 参见 `shared/claude-platform-on-aws.md`。

### Google Cloud Vertex AI

需要两个构造函数参数：GCP `project_id` 和 `region`。Vertex 模型 ID **不带前缀**——当前代模型（Opus 4.8/4.7/4.6、Sonnet 5、Sonnet 4.6）使用裸的第一方 ID（例如 `"claude-opus-4-8"`）；带日期的快照模型使用 `@` 作为版本分隔符（例如 `claude-opus-4-5@20251101`，**不是** `claude-opus-4-5-20251101`）。身份验证使用 GCP ADC（`gcloud auth application-default login`）；不需要 Anthropic API 密钥。`region` 可以是 `"global"`（推荐）、多区域（`"us"`/`"eu"`）或特定区域。构造后，使用相同的 `messages.create` / `.stream` 使用界面。

| 语言 | 客户端 |
|---|---|
| Python | `from anthropic import AnthropicVertex` → `AnthropicVertex(project_id="…", region="…")`（安装 `"anthropic[vertex]"`） |
| TypeScript | `import { AnthropicVertex } from "@anthropic-ai/vertex-sdk"` → `new AnthropicVertex({ projectId, region })` |
| Go | `import "github.com/anthropics/anthropic-sdk-go/vertex"` → `anthropic.NewClient(vertex.WithGoogleAuth(ctx, region, projectID))` |
| Java | `AnthropicOkHttpClient.builder().backend(VertexBackend.builder().region("…").project("…").build()).build()`（来自 `com.anthropic.vertex.backends`） |
| C# | `new AnthropicClient { Backend = new VertexBackend(projectId, region) }`（包 `Anthropic.Vertex`） |
| PHP | `use Anthropic\Vertex;` → `Vertex\Client::fromEnvironment(location: '…', projectId: '…')`——注意是 `location`，不是 `region` |
| Ruby | `Anthropic::VertexClient.new(region: "…", project_id: "…")` |

---

## 上下文编辑（快速参考）

**Beta。**上下文编辑会在模型看到对话之前**清除**旧工具结果或思考块；它**不是压缩**（压缩会进行总结）。在带有 Beta `context-management-2025-06-27` 的 `client.beta.messages.*` 上，通过 `context_management.edits` 传入策略类型：

```python
client.beta.messages.create(
    model="claude-opus-4-8", max_tokens=4096,
    betas=["context-management-2025-06-27"],
    context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
    tools=[...], messages=[...],
)
```

策略类型：`clear_tool_uses_20250919`（清除旧工具结果；可选的 `clear_tool_inputs: true` 还会清除 `tool_use` 参数）和 `clear_thinking_20251015`（清除思考块）。不要使用 `compact_20260112` 或 Beta `compact-2026-01-12`——它们属于独立的压缩功能。

---

## 对话中途 System 消息（快速参考）

**仅限 Claude Opus 4.8；无需 Beta 请求头。**将 `{"role": "system", "content": "…"}` 追加到 `messages` 数组（而不是顶层 `system` 字段），可以在不使缓存前缀失效的情况下，在对话中途添加操作员指令。使用常规的 `client.messages.create`——没有 Beta。对话中途 system 消息必须跟在 `user` 消息之后（或跟在以服务器工具使用结束的 `assistant` 消息之后），并且必须是 `messages` 的最后一项，或者后面紧跟一个 `assistant` 轮次——它不能是 `messages[0]`。可用性见 `shared/platform-availability.md`。参见 `shared/prompt-caching.md` § Mid-conversation system messages。

---

## 托管智能体（Beta）

**托管智能体**是第三种使用界面：由服务器管理、具有状态且由 Anthropic 托管工具执行的智能体。你创建一个持久化且带版本的 Agent 配置（`POST /v1/agents`），然后启动引用该配置的 Session。每个会话都会配置一个容器作为智能体工作区——bash、文件操作和代码执行都在其中运行；智能体循环本身运行在 Anthropic 的编排层，并通过工具操作容器。会话会流式发送事件；你将消息和工具结果发送回去。

可用性见 `shared/platform-availability.md`。对于 Bedrock / Vertex / Foundry 上的智能体（这些平台不支持托管智能体），请使用 Claude API + 工具使用。

**强制流程：**Agent（一次）→ Session（每次运行）。`model`/`system`/`tools` 属于 agent，绝不属于 session。完整阅读指南、Beta 请求头和陷阱见 `shared/managed-agents-overview.md`。

**Beta 请求头：**`managed-agents-2026-04-01`——对于所有 `client.beta.{agents,environments,sessions,vaults,memory_stores,deployments,deployment_runs}.*` 调用，SDK 会自动设置它。Skills API 使用 `skills-2025-10-02`，Files API 使用 `files-api-2025-04-14`，但除 `/v1/skills` 和 `/v1/files` 端点外，无需显式传入这些请求头。

**子命令**——通过 `/claude-api <subcommand>` 直接调用：

| 子命令 | 操作 |
|---|---|
| `managed-agents-onboard` | 引导用户从头设置托管智能体。**立即阅读 `shared/managed-agents-onboarding.md`**并遵循其访谈脚本：**描述 → 配置智能体（提出方案，不要盘问）→ 环境 → 会话**（与 Console 快速入门采用相同流程，身份验证推迟到会话步骤）——通过默认值和内联建议完成工作，并在输出任何代码前进行静默可行性检查（工作与工具/凭据/数据是否匹配）。不要总结——执行访谈。 |

**阅读指南：**从 `shared/managed-agents-overview.md` 开始，然后阅读主题相关的 `shared/managed-agents-*.md` 文件（core、environments、tools、events、outcomes、multiagent、webhooks、memory、scheduled-deployments、client-patterns、onboarding、api-reference）。对于 Python、TypeScript、Go、Ruby、PHP 和 Java，请阅读 `{lang}/managed-agents/README.md` 获取代码示例。对于 cURL，请阅读 `curl/managed-agents.md`。**智能体是持久化的——创建一次，之后通过 ID 引用。**保存 `agents.create` 返回的智能体 ID，并将其传给之后的每次 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是通过版本控制的 YAML 创建智能体和环境的一种便捷方式——参见 `shared/anthropic-cli.md`。如果对应语言的 README 中没有展示所需绑定，请通过 WebFetch 获取 `shared/live-sources.md` 中的相关条目，不要猜测。C# 通过 `client.Beta.Agents` 和相关命名空间提供 Beta 托管智能体支持。

**当用户希望从头设置托管智能体时**（例如“如何开始”“带我创建一个”“设置一个新智能体”）：读取 `shared/managed-agents-onboarding.md` 并执行其访谈——流程与 `managed-agents-onboard` 子命令相同。

**当用户询问“如何为 X 编写客户端代码”时：**使用 `shared/managed-agents-client-patterns.md`——其中涵盖无损流重连、`processed_at` 排队/已处理门控、中断、`tool_confirmation` 往返、正确的空闲/终止中断门控、空闲后状态竞态、流优先顺序、文件挂载陷阱、通过自定义工具将凭据保留在主机端等。

**当用户希望智能体按计划运行时**（cron、“每晚”“每周报告”）：读取 `shared/managed-agents-scheduled-deployments.md`——部署会按照 cron 周期自主触发会话，提供每次触发的运行记录和生命周期控制（暂停/恢复/归档）。

---

## 服务器工具（快速参考）

服务器端工具在 Anthropic 基础设施上运行——无需客户端执行循环。在 `tools` 中声明；结果以内容块形式出现在同一响应中。**除非另有说明，否则无需 Beta 请求头。****优先使用模型支持的最新类型变体。**下方的 `_20260209` Web 搜索/Web 获取变体（动态过滤）要求使用 Opus 4.8/4.7/4.6、Sonnet 5 或 Sonnet 4.6；旧模型的基础变体列在表后。

| 工具 | `type` | `name` | 主要可选参数 | 结果块类型 |
|---|---|---|---|---|
| Web 搜索 | `web_search_20260209` | `web_search` | `max_uses`、`allowed_domains`/`blocked_domains`、`user_location` | `web_search_tool_result` → `.content` 是 `web_search_result` 列表 |
| Web 获取 | `web_fetch_20260209` | `web_fetch` | `max_uses`、`allowed_domains`/`blocked_domains`、`citations`、`max_content_tokens` | `web_fetch_tool_result` → `.content` 是带有 `document` 块的 `web_fetch_result` |
| 代码执行 | `code_execution_20260521` | `code_execution` | 无 | `bash_code_execution_tool_result` → `.content.stdout` / `.stderr` / `.return_code` |
| 工具搜索（正则表达式） | `tool_search_tool_regex_20251119` | `tool_search_tool_regex` | 将其他工具标记为 `defer_loading: true` | `tool_search_tool_result` |
| 工具搜索（BM25） | `tool_search_tool_bm25_20251119` | `tool_search_tool_bm25` | 将其他工具标记为 `defer_loading: true` | `tool_search_tool_result` |

`web_search_20260209` / `web_fetch_20260209` 内置动态过滤——底层会运行代码执行，因此不要在 `tools` 中单独声明 `code_execution`（第二个执行环境会使模型困惑）。对于早于 Opus 4.6 / Sonnet 4.6 的模型，请改用基础变体 `web_search_20250305` / `web_fetch_20250910`；Vertex AI 仅提供基础 `web_search_20250305`。`code_execution_20260120`（REPL 持久化 + 编程式工具调用）适用于 Opus 4.5+ / Sonnet 4.5+。**仅限 Go SDK**：`code_execution_20260521` 位于带有 `Betas: []anthropic.AnthropicBeta{"code-execution-2025-08-25"}` 的 `client.Beta.Messages.New` 下（其他语言使用普通 `client.messages.create`）；Go 中的 `code_execution_20260120` 与其他语言一样使用非 Beta 的 `client.Messages.New`。Web 获取只能获取对话中已经出现的 URL。工具在不同提供商上的可用性不同——参见 `shared/platform-availability.md`。`pause_turn` 处理方式见 `shared/tool-use-concepts.md`。

## 文档与文件输入（快速参考）

**PDF（base64，无需 Beta）：**在用户内容中使用 `{"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": <b64 string>}}`，并将其放在文本块之前。Base64 字符串不能包含换行符。限制：请求大小 32 MB，600 页（对于 200k 上下文模型为 100 页）。Java：`ContentBlockParam.ofDocument(DocumentBlockParam... Base64PdfSource.builder().data(...))`。

**Files API（Beta `files-api-2025-04-14`）：**通过 `client.beta.files.upload(...)` 上传 → 响应中的 `id` 即为 `file_id`。对于 PDF/文本，使用 `{"type": "document", "source": {"type": "file", "file_id": "..."}}` 引用；对于图像，则使用 `{"type": "image", ...}`——内容块类型必须与文件的 MIME 类型匹配。上传请求和引用该文件的 `messages.create` **都**必须携带 Beta 请求头。可用性见 `shared/platform-availability.md`。

**引用（无需 Beta）：**在每个 `document` 内容块上设置 `citations: {enabled: true}`（要么全部启用，要么全部不启用）。响应会拆分成多个 `text` 块；带引用的块包含 `citations` 数组。每条引用包含 `cited_text`、`document_index`、`document_title`，以及按 `type` 区分的位置：纯文本使用 `char_location`（`start_char_index`/`end_char_index`），PDF 使用 `page_location`（`start_page_number`/`end_page_number`，从 1 开始计数），自定义内容使用 `content_block_location`。与 `output_config.format` 不兼容。

## 工具使用模式（快速参考）

**严格工具使用（无需 Beta）：**在工具定义的顶层字段（与 `name`/`description`/`input_schema` 同级）设置 `strict: true`，**不要**放在 `tool_choice` 上。Schema 必须包含 `additionalProperties: false` + `required`。这可保证 `tool_use.input` 精确通过验证。Go：`Strict: anthropic.Bool(true)`，并通过 `InputSchema.ExtraFields` 设置 `additionalProperties`；Java：`.strict(true)` + `.putAdditionalProperty("additionalProperties", JsonValue.from(false))`。

**并行工具使用（默认开启）：**一条 assistant 消息可包含多个 `tool_use` 块。并发执行它们，然后在**一条** user 消息中返回**所有** `tool_result` 块（不要拆分到多条消息中）。对于失败的工具，返回带有 `is_error: true` 的 `tool_result`——不要将其丢弃。

**工具运行器（SDK Beta 辅助工具）：**通过 `client.beta.messages.*` 为你驱动工具调用循环。Python：`@beta_tool` 装饰器 + `client.beta.messages.tool_runner(...)` → `runner.until_done()`。TypeScript：来自 `@anthropic-ai/sdk/helpers/beta/zod` 的 `betaZodTool({...})` + `client.beta.messages.toolRunner(...)` → `await runner`。Go：`toolrunner.NewBetaToolFromJSONSchema(...)` + `client.Beta.Messages.NewToolRunner(...)` → `.RunToCompletion(ctx)`。Java 需要 `.addBeta("structured-outputs-2025-11-13")`。Ruby：`Anthropic::BaseTool` 子类 + `client.beta.messages.tool_runner(...)`。PHP：`BetaRunnableTool` + `->toolRunner(...)`。C#：原始 JSON-schema 工具 + 通过 `client.Beta.Messages.ToolRunner(...)` 使用 `BetaToolRunner`。

**编程式工具调用（无需 Beta 请求头）：**Claude 从代码执行内部调用你的自定义工具。添加 `{"type": "code_execution_20260120", "name": "code_execution"}`，**同时**在自定义工具上设置 `"allowed_callers": ["code_execution_20260120"]`。适用于 Opus 4.5+ / Sonnet 4.5+（可用性见 `shared/platform-availability.md`）。回复待处理的编程式调用时，user 消息必须**只包含** `tool_result` 块（不能包含文本）。不兼容 `strict: true`、`disable_parallel_tool_use`、强制 `tool_choice` 或 MCP 工具。

## 其他 API 使用界面（快速参考）

**消息批处理（无需 Beta；可用性见 `shared/platform-availability.md`）：**`client.messages.batches.create(requests=[{custom_id, params}, ...])` → 轮询 `client.messages.batches.retrieve(id).processing_status`，直到为 `"ended"` → 流式读取 `client.messages.batches.results(id)`。每个结果包含 `.custom_id` + `.result.type`（`succeeded`/`errored`/`canceled`/`expired`）；成功时读取 `.result.message.content`。Python 使用 `Request(custom_id=..., params=MessageCreateParamsNonStreaming(...))` 包装请求。结果可以按**任意顺序**返回——始终按 `custom_id` 建立索引，绝不要依赖位置。

**Models API（无需 Beta；可用性见 `shared/platform-availability.md`）：**`client.models.list()`（自动分页）和 `client.models.retrieve("claude-opus-4-8")`。每个模型对象包含 `id`、`display_name`、`created_at`，以及——自 2026 年 3 月起——`max_input_tokens`（上下文窗口）、`max_tokens`（输出上限）和 `capabilities`。不存在 `context_window` 字段。

**停止详情（GA，Opus 4.7+）：**仅当 `stop_reason == "refusal"` 时，`response.stop_details` 才会被填充（字段：`type: "refusal"`、`category: "cyber"|"bio"|null`、`explanation`）。对于其他所有 `stop_reason`（`end_turn`、`max_tokens`、`tool_use`、`pause_turn` 等），它都是 `null`——读取前始终进行条件检查。

**客户端配置（无需 Beta）：**`timeout` 默认 10 分钟；**各 SDK 的单位不同**——Python/Ruby：秒；TypeScript：**毫秒**；Go 使用 `option.WithRequestTimeout(time.Duration)`；Java 使用 `Duration`；C# 使用 `TimeSpan`。对于较大 `max_tokens` 的非流式请求，TS 会将默认值扩展至最多 60 分钟；Java 对流式请求进行类似扩展（Java 非流式请求会扩展到 30 秒–10 分钟）。`max_retries`/`maxRetries` 默认为 2（重试 408/409/429/5xx 和连接错误）。`base_url`（或环境变量 `ANTHROPIC_BASE_URL`）。单请求覆盖：Python `client.with_options(timeout=5.0).messages.create(...)`；TS `client.messages.create({...}, {timeout: 5_000})`；Ruby `request_options: {timeout: 5}`。超时会触发重试——总实际时间可能达到 `timeout × (max_retries+1)`。

## 工作负载身份联合（快速参考）

**GA，无需 Beta 请求头。**构造普通的零参数客户端（`Anthropic()` / `new Anthropic()` / `anthropic.NewClient()` / `AnthropicOkHttpClient.fromEnv()`）；当 `ANTHROPIC_FEDERATION_RULE_ID`、`ANTHROPIC_ORGANIZATION_ID`、`ANTHROPIC_SERVICE_ACCOUNT_ID` 和 `ANTHROPIC_IDENTITY_TOKEN_FILE`（或 `ANTHROPIC_IDENTITY_TOKEN`）**全部**设置时，SDK 会自动检测 WIF，在 `/v1/oauth/token` 交换 JWT，并自动刷新。`ANTHROPIC_WORKSPACE_ID` 不控制激活——仅当联合规则跨越多个工作区时才是必需的（否则返回 400 `workspace_id_required`）；对单工作区规则可选。`ANTHROPIC_API_KEY` 或 `ANTHROPIC_AUTH_TOKEN`（即使为空）优先于 WIF；已设置的 `ANTHROPIC_PROFILE` 也优先于联合环境变量（命名配置文件缺失会报错，而不会继续回退）——请取消设置这三个变量。

---

## 阅读指南

检测语言后，根据用户需求阅读相关文件。

**所有 SDK 语言使用相同的多文件布局**——目录 `{lang}/claude-api/` 包含 `README.md`（安装、客户端初始化、基本请求、思考、缓存、停止详情、其他内容）、`tool-use.md`（工具定义、智能体循环、Anthropic 定义的工具、结构化输出）、`streaming.md`、`batches.md`、`files-api.md`。并非每种语言都包含每个文件（例如 Ruby 没有 `batches.md`）；如果某个文件不存在，说明该语言的该功能示例尚未记录——请回退到 cURL 结构，或通过 WebFetch 获取 `shared/live-sources.md` 中的 SDK 仓库。**cURL** → `curl/examples.md`。

下方的快速任务参考对所有语言使用 `{lang}/claude-api/FILE.md` 路径表示法。

### 快速任务参考

**单次文本分类/总结/提取/问答：**
→ 只读取 `{lang}/claude-api/README.md`

**聊天 UI 或实时响应显示：**
→ 读取 `{lang}/claude-api/README.md` + `{lang}/claude-api/streaming.md`

**长时间运行的对话（可能超过上下文窗口）：**
→ 读取 `{lang}/claude-api/README.md`——参见 Compaction 章节

**迁移到更新模型（Fable 5 / Opus 4.8 / Opus 4.7 / Opus 4.6 / Sonnet 5 / Sonnet 4.6）或替换已退役模型：**
→ 读取 `shared/model-migration.md`

**为 Fable 5 编写或调优提示（长轮次、effort、详细程度、自主运行、子智能体）：**
→ 读取 `shared/model-migration.md` → Migrating to Fable 5 → Behavioral shifts (prompt-tunable) + Long-running agent recommendations

**提示缓存/优化缓存/“为什么我的缓存命中率很低”：**
→ 读取 `shared/prompt-caching.md` + `{lang}/claude-api/README.md`（Prompt Caching 章节）

**计算文件/提示/diff 中的 Token（“X 有多少 Token”）：**
→ 读取 `shared/token-counting.md`——使用 `messages.count_tokens`，绝不要使用 `tiktoken`

**函数调用/工具使用/智能体：**
→ 读取 `{lang}/claude-api/README.md` + `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`

**智能体设计（工具使用界面、上下文管理、缓存策略）：**
→ 读取 `shared/agent-design.md`

**批处理（非延迟敏感）：**
→ 读取 `{lang}/claude-api/README.md` + `{lang}/claude-api/batches.md`

**跨多个请求上传文件：**
→ 读取 `{lang}/claude-api/README.md` + `{lang}/claude-api/files-api.md`

**托管智能体（具有工作区、由服务器管理的有状态智能体）：**
→ 读取 `shared/managed-agents-overview.md` + 其余 `shared/managed-agents-*.md` 文件。对于 Python、TypeScript、Go、Ruby、PHP 和 Java，请阅读 `{lang}/managed-agents/README.md` 获取代码示例。对于 cURL，请阅读 `curl/managed-agents.md`。**智能体是持久化的——创建一次，之后通过 ID 引用。**保存 `agents.create` 返回的智能体 ID，并将其传给之后的每次 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是通过版本控制的 YAML 创建智能体和环境的一种便捷方式——参见 `shared/anthropic-cli.md`。如果对应语言的 README 中没有展示所需绑定，请通过 WebFetch 获取 `shared/live-sources.md` 中的相关条目，不要猜测。C# 提供 Beta 托管智能体支持——详情见 `csharp/claude-api/README.md`，原始 HTTP 参考见 `curl/managed-agents.md`。

### Claude API（完整文件参考）

读取**语言特定的 Claude API 源文档**——每种 SDK 语言使用 `{language}/claude-api/`，cURL 使用 `curl/examples.md`：

1. **`{language}/claude-api/README.md`**——**先阅读此文件。**安装、快速入门、常见模式、错误处理。
2. **`shared/tool-use-concepts.md`**——当用户需要函数调用、代码执行、记忆或结构化输出时阅读。涵盖概念基础。
3. **`shared/agent-design.md`**——设计智能体时阅读：bash 与专用工具、编程式工具调用、工具搜索/技能、上下文编辑与压缩与记忆的比较、缓存原则。
4. **`{language}/claude-api/tool-use.md`**——用于语言特定的工具使用代码示例（工具运行器、手动循环、代码执行、记忆、结构化输出）。
5. **`{language}/claude-api/streaming.md`**——构建聊天 UI 或增量显示响应的界面时阅读。
6. **`{language}/claude-api/batches.md`**——离线处理大量请求（非延迟敏感）时阅读。异步运行，成本为 50%。
7. **`{language}/claude-api/files-api.md`**——在多个请求间发送同一文件而不重复上传时阅读。
8. **`shared/prompt-caching.md`**——添加或优化提示缓存时阅读。涵盖前缀稳定性设计、断点放置以及会静默使缓存失效的反模式。
9. **`shared/error-codes.md`**——调试 HTTP 错误或实现错误处理时阅读。包含各 SDK 类型化异常类表和 Go 的 `errors.As` 模式。
10. **`shared/model-migration.md`**——升级到更新模型、替换已退役模型，或将 `budget_tokens` / 预填充模式转换为当前 API 时阅读。
11. **`shared/live-sources.md`**——用于获取最新官方文档的 WebFetch URL。

并非每种语言都包含每个文件（例如 Ruby 没有 `batches.md`）；如果某个文件不存在，说明该语言的该功能示例尚未记录。

> **注意：**有关托管智能体的文件参考，请参见上方的 `## Managed Agents (Beta)` 章节——其中列出了所有 `shared/managed-agents-*.md` 文件和语言特定 README。

---

## 何时使用 WebFetch

在以下情况使用 WebFetch 获取最新文档：

- 用户要求“最新”或“当前”信息
- 缓存数据似乎不正确
- 用户询问此处未涵盖的功能

实时文档 URL 位于 `shared/live-sources.md`。

## 常见陷阱

- **没有 `ANTHROPIC_API_KEY` ≠ 没有凭据。**不要仅仅因为环境变量未设置就退出或向用户索要密钥——先运行 `ant auth status`。执行 `ant auth login` 后，无需环境变量，裸 `Anthropic()` 客户端和 `ant …` 即可工作；对于原始 curl，请使用 `Authorization: Bearer $(ant auth print-credentials --access-token)`，并添加请求头 `anthropic-beta: oauth-2025-04-20`。参见上方的身份验证快速参考和 `shared/anthropic-cli.md`。
- 将文件或内容传给 API 时，不要截断输入。如果内容太长，无法放入上下文窗口，请通知用户并讨论可选方案（分块、总结等），不要静默截断。
- **Fable 5 / Sonnet 5 / Opus 4.8 / 4.7 思考：**仅支持自适应模式。`thinking: {type: "enabled", budget_tokens: N}` 返回 400——`budget_tokens` 已完全移除（`temperature`、`top_p`、`top_k` 也已移除）。使用 `thinking: {type: "adaptive"}`。Opus 4.8 继承 4.7 的使用界面，没有新的破坏性变更；Fable 5 新增一项变更——显式 `thinking: {type: "disabled"}` 返回 400（Sonnet 5 / 4.7 / 4.8 接受该设置）；应改为省略该参数。
- **Opus 4.6 / Sonnet 4.6 思考：**使用 `thinking: {type: "adaptive"}`——不要在新的 4.6 代码中使用 `budget_tokens`（在 Opus 4.6 和 Sonnet 4.6 上均已弃用；有关现有代码的渐进迁移，请参见 `shared/model-migration.md` 中的过渡性逃生口——注意，此例外不适用于 Fable 5、Opus 4.7 或 4.8）。对于旧模型，`budget_tokens` 必须小于 `max_tokens`（最小值 1024）。设置错误会引发异常。
- **已移除预填充（Fable 5 和 4.6/4.7/4.8 系列）：**在 Fable 5、Opus 4.6、Opus 4.7、Opus 4.8 和 Sonnet 4.6 上，assistant 消息预填充（最后一个 assistant 轮次的预填充）会返回 400 错误。请改用结构化输出（`output_config.format`）或 system prompt 指令控制响应格式。（有一个例外：回退额度预填充声明——使用 `fallback_has_prefill_claim: true` 兑换额度时，服务器接受原样回传的 assistant 消息；参见迁移指南的拒绝章节。）
- **Fable 5 的 `refusal` 停止原因：**安全分类器可能拒绝请求——HTTP 200 成功响应中带有 `stop_reason: "refusal"`（输出前：`content` 为空，不计费；流式传输中途：部分输出会计费——请丢弃）。读取 `response.content[0]` 前检查 `stop_reason`，否则被拒绝的请求会导致索引错误。若要使用另一个模型重试，请原样重放历史记录——其他模型会从提示中丢弃被拒模型的思考块且不计费；无需手动移除（回退额度兑换无论如何都必须原样回传被拒绝的响应体，包括思考块）。回退是**选择加入的**——新的 `claude-fable-5` 代码应默认包含服务器端 `fallbacks` 参数，以免拒绝直接导致请求失败；参见上方的 Claude Fable 5 章节。
- **Fable 5 分词器：**与 Opus 4.8 使用相同的分词器——从 Opus 4.7/4.8 迁移时，Token 数量大致不变。从 Opus 4.6、Sonnet、Haiku 或更早模型迁移时，Token 数量会有所不同（Opus 4.7 分词器使用的 Token 约为 1×–1.35×）——请分别使用每个模型调用一次 `count_tokens` 并比较 `input_tokens`，重新测量。
- **编辑前确认迁移范围：**当用户要求将代码迁移到更新的 Claude 模型，但没有指定具体文件、目录或文件列表时，**先询问要应用到什么范围**——整个工作目录、某个特定子目录，还是一组特定文件。用户确认前不要开始编辑。“迁移我的代码库”“将我的项目移至 X”“升级到 Sonnet 4.6”或裸命令“迁移到 Opus 4.8”等祈使表达**仍然有歧义**——它们说明了要做什么，却没有说明在哪里做，因此必须询问。只有当提示指定了精确文件、具体目录或明确文件列表（“迁移 `app.py`”“迁移 `services/` 下的所有内容”“更新 `a.py` 和 `b.py`”）时，才可不询问直接继续。参见 `shared/model-migration.md` 步骤 0。
- **`max_tokens` 默认值：**不要将 `max_tokens` 设得过低——达到上限会在思考中途截断输出，并需要重试。对于非流式请求，默认使用约 `~16000`（使响应保持在 SDK HTTP 超时范围内）。对于流式请求，默认使用约 `~64000`（无需担心超时，因此应为模型留出空间）。只有在有明确理由时才降低：分类（约 `~256`）、成本上限、刻意要求短输出，或者用于缓存预热的 **`max_tokens: 0`**（参见 `shared/prompt-caching.md` → Pre-warming）。
- **128K 输出 Token：**Fable 5、Opus 4.6、Opus 4.7、Opus 4.8、Sonnet 5 和 Sonnet 4.6 支持最高 128K `max_tokens`，但为了避免 HTTP 超时，SDK 要求对如此大的值使用流式传输。使用 `.stream()` 和 `.get_final_message()` / `.finalMessage()`。
- **工具调用 JSON 解析（Fable 5 和 4.6/4.7/4.8 系列）：**Fable 5、Opus 4.6、Opus 4.7、Opus 4.8 和 Sonnet 4.6 在工具调用 `input` 字段中可能产生不同的 JSON 字符串转义（例如 Unicode 或正斜杠转义）。始终使用 `json.loads()` / `JSON.parse()` 解析工具输入——绝不要对序列化输入进行原始字符串匹配。
- **结构化输出（所有模型）：**在 `messages.create()` 上使用 `output_config: {format: {...}}`，不要使用已弃用的 `output_format` 参数。这是一项通用 API 变更，并非 4.6 特有。
- **不要重新实现 SDK 功能：**SDK 提供高级辅助方法——请直接使用，不要从头构建。特别是：使用 `stream.finalMessage()`，不要将 `.on()` 事件包装在 `new Promise()` 中；使用类型化异常类（`Anthropic.RateLimitError` 等），不要通过字符串匹配错误消息；使用 SDK 类型（`Anthropic.MessageParam`、`Anthropic.Tool`、`Anthropic.Message` 等），不要重新定义等价接口。
- **错误处理——捕获具体异常链，而不是一个宽泛类。**单独使用 `except APIStatusError` / `catch (AnthropicServiceException)` / `rescue APIError` 会丢失可重试错误（429、≥500、网络）与不可重试错误（400/404）之间的区别。请按最具体到最宽泛的顺序编写异常链——例如 `NotFoundError` → `RateLimitError` → `APIStatusError` → `APIConnectionError`（或 Go 等价形式：使用 `errors.As` 转换为 `*anthropic.Error`，然后执行 `switch apierr.StatusCode { case 404: …; case 429: …; default: … }`）。各语言的类名和命名空间见 `shared/error-codes.md`。
- **不要调研 SDK 类型——先编写。**如果此技能附带的文档中没有展示某个类型名，请根据语言特定文档中的命名空间/包表编写代码文件，然后让编译器错误指出正确名称。不要在编写前花费多个轮次使用 WebFetch、克隆 SDK 仓库，或编译并运行单独的反射程序来发现类型名——先产出源文件，再修复编译器报告的问题。可以针对已安装的 SDK 快速运行 `strings` / `jar tf` / `javap` 来定位名称（会在几秒内返回），但不要进一步升级调研。文件中的错误类型名可以修复；整个会话都花在发现阶段却没有写出文件则无法挽回。
- **Bash 和文本编辑器工具由 Anthropic 定义且没有 schema。**声明 `{"type": "bash_20250124", "name": "bash"}` / `{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}`——不要添加 `input_schema`。使用你自己的 schema 且名为 `"bash"` 的自定义工具是另一个不同的工具。处理器路径和安全检查见 `shared/tool-use-concepts.md` § Client-Side Tools。
- **Advisor 工具模型配对。**Advisor 工具的 `model` 必须至少与请求顶层的 `model` 一样强大——例如执行器 `claude-sonnet-5` → advisor `claude-opus-4-8` 或 `claude-opus-4-7`。无效配对会返回 400。配对表见 `shared/tool-use-concepts.md` § Advisor。可用性见 `shared/platform-availability.md`。
- **Agent Skills ≠ 托管智能体。**若要让 Claude 通过 Agent Skills 生成 `.pptx`/`.xlsx` 等文件，请调用 `client.beta.messages.create`，并传入 `container={"skills": [...]}`、`code_execution_20260521` 工具，以及 `code-execution-2025-08-25` + `skills-2025-10-02` 两个 Beta。不要在这里使用 `client.beta.agents` / `sessions` / `environments`——它们属于托管智能体使用界面，不是 Agent Skills。
- **MCP 连接器需要两部分。**仅设置 `mcp_servers=[{type:"url", url, name}]` 会作为验证错误被拒绝——还需添加 `tools=[{type:"mcp_toolset", mcp_server_name:<same name>}]`，并使用 Beta `mcp-client-2025-11-20`。可用性见 `shared/platform-availability.md`。
- **上下文编辑 ≠ 压缩。**上下文编辑会*清除*工具结果和思考块；压缩会*总结*历史记录。对于上下文编辑，请在带有 Beta `context-management-2025-06-27` 的 `client.beta.messages.*` 上使用 `context_management.edits`，类型为 `clear_tool_uses_20250919`（或 `clear_thinking_20251015`）——不要使用属于压缩功能的 `compact_20260112` 类型或 `compact-2026-01-12` Beta。
- **`inference_geo` 是直接的顶层请求参数**——`client.messages.create(..., inference_geo="us")` / `.inferenceGeo("us")`。不要将其放入 `extra_body` / `putAdditionalBodyProperty`。适用于 Opus 4.6 / Sonnet 4.6 及更高版本；可用性见 `shared/platform-availability.md`。`response.usage.inference_geo` 会报告推理运行位置。
- **细粒度工具流式传输不是 Beta 功能。**在工具定义上设置 `eager_input_streaming: true`，并调用常规 `client.messages.stream(...)`。不需要 Beta 请求头，也没有 `client.beta.*` 路径。
- **缓存诊断是 Beta 功能。**使用带有 Beta `cache-diagnosis-2026-04-07` 的 `client.beta.messages.*`。第一轮传入 `diagnostics: {previous_message_id: null}`，后续轮次传入 `diagnostics: {previous_message_id: <previous response id>}`；结果位于 `response.diagnostics`。可用性见 `shared/platform-availability.md`。
- **记忆工具类型是 `memory_20250818`。**声明 `{"type": "memory_20250818", "name": "memory"}`。Go 在 `client.Beta.Messages.New` 上使用 Beta 命名空间类型 `{OfMemoryTool20250818: &anthropic.BetaMemoryTool20250818Param{}}`；Python/TypeScript/Ruby/PHP/C# 使用非 Beta 的 `client.messages.create`；Java 同时提供非 Beta 的 `MemoryTool20250818` 和 Beta 工具运行器路径。Python/TypeScript 提供 `BetaAbstractMemoryTool` / `betaMemoryTool` 辅助方法，用于实现后端。
- **使用功能真正支持的模型。**某些功能仅限特定模型层级——快速模式仅限 Opus 4.8 / 4.7，任务预算仅限 Fable 5 / Sonnet 5 / Opus 4.8 / 4.7，Advisor 工具要求有效的执行器↔Advisor 配对。如果用户提示指定的模型不支持该功能，请改用受支持的模型，并在输出中注明替换。
- **Bedrock / Foundry：使用平台客户端类。**对于 Bedrock，请使用 `…BedrockMantle…` 客户端（例如 Python 的 `AnthropicBedrockMantle`、Java 的 `BedrockMantleBackend`）和带 `anthropic.` 前缀的模型 ID；不带 `Mantle` 的 `AnthropicBedrock`/`BedrockBackend` 是旧版路径。对于 Foundry，在 SDK 支持的语言（C#、Java、PHP、Python、TypeScript）中使用 `AnthropicFoundry` / `FoundryBackend` / `AnthropicFoundryClient`；Go 和 Ruby 没有 Foundry 客户端——Ruby 的文档化回退方案是使用带自定义 `base_url` 的第一方客户端。各语言表见上文。
- **不要为 SDK 数据结构定义自定义类型：**SDK 为所有 API 对象导出了类型。消息使用 `Anthropic.MessageParam`，工具定义使用 `Anthropic.Tool`，工具结果使用 `Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam`，响应使用 `Anthropic.Message`。自行定义 `interface ChatMessage { role: string; content: unknown }` 会重复 SDK 已有内容并丢失类型安全。
- **报告和文档输出：**对于生成报告、文档或可视化的任务，代码执行沙箱已预装 `python-docx`、`python-pptx`、`matplotlib`、`pillow` 和 `pypdf`。Claude 可以生成格式化文件（DOCX、PDF、图表），并通过 Files API 返回——对于“报告”或“文档”类请求，请考虑使用这种方式，而不只是输出纯 stdout 文本。
- **服务器工具错误不会引发异常。**Web 搜索和 Web 获取错误会返回 HTTP 200，并包含 `web_search_tool_result` / `web_fetch_tool_result` 块，其 `content` 是单个错误对象（例如 `{error_code: "max_uses_exceeded"}`）——不会抛出异常。对于 Web 搜索，成功时 `content` 是一个*列表*；错误时 `content` 是一个*对象*——索引前请据此分支处理。
- **代码执行输出块类型：**`code_execution_20260521` 返回 `bash_code_execution_tool_result`（包含 `.content.stdout`），**不是**旧版裸 `code_execution_tool_result`。遍历 `response.content` 并匹配正确的类型。
- **工具搜索：绝不要延迟加载所有工具。**搜索工具本身不得设置 `defer_loading: true`，并且 `tools` 中至少有一个工具必须不是延迟加载的，否则 API 会返回 400 `All tools have defer_loading set`。
- **`strict: true` 放在工具上，而不是 `tool_choice` 上。**将 `strict` 放在 `tool_choice` 上不会生效；它应位于工具定义中，与 `name`/`description`/`input_schema` 同级。
- **并行工具结果放在一条 user 消息中。**将 `tool_result` 块拆分到多条 user 消息中，会静默地训练 Claude 停止进行并行调用。一条包含多个 `tool_use` 块的 assistant 消息 → 一条包含多个 `tool_result` 块的 user 消息。
- **引用与结构化输出不兼容。**在文档上启用 `citations: {enabled: true}` 的同时设置 `output_config.format` 会返回 400。
- **批处理结果无序。**通过 `custom_id` 匹配，绝不要依赖结果流中的位置。
- **Vertex 模型 ID 不带前缀。**不同于 Bedrock 带 `anthropic.` 前缀的 ID，Vertex 对当前代模型使用裸的第一方 ID（例如 `"claude-opus-4-8"`）；带日期的快照模型使用 `@` 分隔符（例如 `claude-haiku-4-5@20251001`）。
- **除非 `stop_reason == "refusal"`，否则 `stop_details` 为 `null`。**对于 `max_tokens`、`end_turn` 等，`stop_details` 为 `null`——读取 `.category` 前必须进行条件检查。
- **WIF 身份验证：取消设置 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_PROFILE`。**`ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN`（即使设置为 `""`）在 SDK 的优先级链中高于 Workload Identity Federation，并会静默胜出；已设置的 `ANTHROPIC_PROFILE` 也会胜出（命名配置文件缺失会报错，而不会继续回退）。请使用 `unset`，不要将它们设为空值。
