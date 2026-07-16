<!-- source-sha256: 95ae2683b30d892d165af92a350c5628b68106f395a59b448857b654e306ed91 -->
---
name: vercel-optimize
description: "用于优化已部署项目的 Vercel 成本和性能，尤其适用于 Next.js、SvelteKit、Nuxt，以及支持有限的 Astro 应用。首先收集 Vercel 指标、用量、项目配置和代码扫描结果；仅调查有指标依据的候选项；基于已验证文件以及与版本匹配的 Vercel/框架文档，生成按优先级排序的建议。当用户请求降低 Vercel 账单、分析缓慢或昂贵的路由、寻找缓存机会，或分析 Function Invocations、Build Minutes、Fast Data Transfer、Core Web Vitals、Bot Management、Fluid compute 或成本明细时触发。"
metadata:
  version: "1.2.0"
---

# Vercel 优化

执行一次可观测性优先的 Vercel 优化审计。在 `signals.json` 存在且确定性筛选指向某个路由、文件或项目设置之前，不要检查源文件。

核心原则：如果任何规则不清楚，请阅读 [references/doctrine.md](references/doctrine.md)。

- 指标优先。建议从 Vercel 生产环境信号出发，而不是对整个仓库执行 grep。
- 确定性筛选。由 `scripts/gate-investigations.mjs` 决定哪些内容值得调查。
- 范围限定于候选项。只读取候选项指定的文件或路由局部导入链。
- 与版本匹配的引用。只能使用 `references/docs-library.json`；无效或版本不匹配的引用会被移除。
- 面向客户的文案。在撰写报告文本或聊天输出前，阅读 [references/voice.md](references/voice.md)。

## 前置条件

- Vercel CLI v53+，并支持 `vercel metrics`、`vercel usage`、`vercel contract` 和 `vercel api`。
- 已认证的 CLI 会话：`vercel login`。
- 已关联的应用目录：`vercel link`。`VERCEL_PROJECT_ID` 可以帮助解析项目配置，但 `vercel metrics` 仍然要求目录已关联。关联信息或环境必须包含目标项目所属的组织/团队/用户范围，以便收集器解析出 CLI 可安全使用的 `--scope`，并确保 `vercel metrics`、`vercel usage` 和 `vercel contract` 使用同一账户。
- Node.js 20+。
- 若要生成有路由级指标依据的建议，需要 Observability Plus。

绝不要把认证令牌放进 shell 命令中。不要在可能回显到聊天中的命令里输入 `VERCEL_TOKEN=...`、`--token ...` 或 `Authorization: Bearer ...`。

## 框架支持

预检会读取 `package.json`，并在指标并行收集前设定预期。

| 框架 | 状态 | 说明 |
|---|---|---|
| Next.js App Router | 支持 | 路由映射、扫描器、操作手册和引用最完善 |
| Next.js Pages Router | 支持 | 检测到后，范围限定为 Pages Router 的惯用模式 |
| SvelteKit | 支持 | 支持 `src/routes` 文件的路由映射和 SvelteKit 扫描器 |
| Nuxt | 支持 | 支持路由映射以及通用/平台检查；框架专属建议较少 |
| Astro | 有限支持 | 支持路由映射和通用检查；框架专属建议较少 |
| Hono / Remix / 未知 | 默认阻止 | 仅当用户接受有限的平台/纯代码审计时继续 |

如果框架不受支持，请在扫描或筛选前停止并询问：

```text
此项目使用 <framework>。Vercel Optimize 支持为 Next.js、SvelteKit 和 Nuxt 提供有指标依据的代码建议。对 Astro 的支持有限。对于 <framework>，我仍可执行有限的平台/扫描器审计，但 Vercel 路由级指标可能无法映射回源文件。

你希望我继续进行有限审计，还是在这里停止？
```

如果用户选择继续，请使用 `--continue-unsupported-framework` 重新运行收集。

## 运行目录

每次审计都使用一个新的运行目录。不要跨运行复用简报、子代理输出或报告。

```bash
RUN_DIR="$(mktemp -d -t vercel-optimize-XXXXXX)"
```

## 流程

### 1. 收集、扫描并合并信号

从已关联的应用目录运行；如果脚本支持，也可以传入 `--cwd`。将 stdout 的 JSON 与 stderr 日志分开。不要合并输出流。

```bash
node scripts/collect-signals.mjs [projectId] > "$RUN_DIR/vercel-signals.json" 2> "$RUN_DIR/collect.stderr"
node -e 'JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"))' "$RUN_DIR/vercel-signals.json"

node scripts/scan-codebase.mjs <repo-root> > "$RUN_DIR/codebase.json"
node scripts/merge-signals.mjs "$RUN_DIR/vercel-signals.json" "$RUN_DIR/codebase.json" --out "$RUN_DIR/signals.json"
```

收集细节、架构、指标 ID 和降级行为记录在 [references/data-collection.md](references/data-collection.md) 中。指标注册表位于 [lib/queries.mjs](lib/queries.mjs)；所有查询都应使用统一的 14 天时间窗口。

`collect-signals.mjs` 会将已关联项目的所有者解析为 `commandScope.cliScope`，并在检查 Observability Plus 前，验证解析出的账户能否读取解析出的项目。下游脚本会为每个接受 `--scope` 的 Vercel CLI 命令复用该范围。不要在缺少同一范围的情况下手动运行 `vercel usage`、`vercel metrics` 或 `vercel contract`；未指定范围的用量数据可能来自用户的个人组织，而路由指标则来自团队项目。

如果项目或范围解析存在歧义，请停止并询问用户要审计哪个 Vercel 项目以及哪个团队/个人范围。不要根据当前 `vercel whoami` 显示的团队推断目标范围；在关联信息、`.vercel/repo.json` 中的精确项目匹配，或 `VERCEL_PROJECT_ID` + `VERCEL_ORG_ID` 明确标识目标账户前，不要继续收集指标、用量或合约信息。

对于 `PROJECT_SCOPE_UNRESOLVED`、`SCOPE_UNRESOLVED` 或 `PROJECT_SCOPE_MISMATCH`，使用以下提示：

```text
我目前还无法安全地确定本次审计对应的 Vercel 项目和账户。

请确认 Vercel 项目名称或 ID 以及团队 slug/名称，或者告诉我它位于你的个人账户下。确认后，我会重新关联或针对该确切范围重新运行收集，然后再检查指标。
```

### 1.1 遇到阻塞项时停止

在筛选前检查阻塞项：

```bash
jq '{frameworkSupportBlocker, observabilityPlus, observabilityPlusUsable, observabilityPlusBlocker, observabilityPlusBlockerDetail}' "$RUN_DIR/signals.json"
```

必须采取的操作：

- `frameworkSupportBlocker === "unsupported_framework"`：使用上面的不受支持框架提示。
- `PROJECT_SCOPE_UNRESOLVED`、`SCOPE_UNRESOLVED` 或 `PROJECT_SCOPE_MISMATCH`：停止并询问用户要审计哪个 Vercel 项目及哪个团队/个人范围。对于团队项目，在执行 `vercel link --yes --project <project-name-or-id> --team <team-slug>` 后重新运行；对于个人项目，在目标用户账户下完成关联，或同时设置 `VERCEL_PROJECT_ID` 和 `VERCEL_ORG_ID` 后重新运行。
- `observabilityPlusBlocker === null`：继续。
- `no_traffic`：告知用户路由指标稀疏；仅在用户接受有限输出时继续。
- `payment_required` 或 `no_oplus_probe`：逐字呈现 [references/observability-plus.md](references/observability-plus.md) 并询问。
- `project_disabled`：告知用户为项目启用 Observability Plus，或接受有限审计。
- `daily_quota_exceeded`：停止并告知用户 Observability 查询配额已用尽；在下一个 UTC 午夜重置后重试，或询问是否继续进行有限的纯代码审计。
- `not_linked`：关联应用目录，然后重新运行第 1 步。如果应用路径和项目已知：

```bash
vercel link --yes --project <project-name-or-id> --cwd <app-dir>
# 已知时添加 --team <team-id-or-slug>
```

- `forbidden` 或 `project_not_found`：修复认证/团队范围。不要推销 Observability Plus。
- `all_failed_other`：显示原始错误代码，并询问是否以有限的纯代码模式继续。

不要静默回退到纯代码模式。如果用户接受有限审计，请使用以下命令重新运行收集：

```bash
node scripts/collect-signals.mjs [projectId] --continue-without-observability > "$RUN_DIR/vercel-signals.json" 2> "$RUN_DIR/collect.stderr"
```

然后再次扫描并合并。

### 2. 筛选候选项

```bash
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" > "$RUN_DIR/gate.json"
```

输出结构：

- `toLaunch`：需要调查的代码范围候选项。
- `platform`：项目/账户范围建议。
- `gated`：被跳过、已覆盖或不合格的候选项，但仍必须出现在报告中。
- `budget`：候选项预算和选择模式。

默认预算为 6 个代码范围候选项，并带有多样性保护规则。若要扩大范围：

```bash
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" --max-candidates 12 > "$RUN_DIR/gate.json"
node scripts/gate-investigations.mjs "$RUN_DIR/signals.json" --max-candidates all > "$RUN_DIR/gate.json"
```

生成的候选项文档：[references/candidates.md](references/candidates.md)。

### 2.1 必要时询问审计范围

深入调查前，运行：

```bash
node scripts/budget-summary.mjs "$RUN_DIR/gate.json" --format json > "$RUN_DIR/budget-summary.json"
```

如果 `shouldAsk` 为 false，则继续。

如果 `shouldAsk` 为 true：

1. 严格按照返回内容输出 `exactChatMessage.body`。不要概括、截断、重新排序或改写。
2. 然后使用 `questionText` 提问；如果宿主支持结构化问题，则使用 `questionPayload`。
3. 如果用户选择了不同数量，请使用 `--max-candidates <choice>` 重新运行筛选。

绝不要把长预览放进问题字段。预览和问题是两个独立的界面区域。

### 2.2 深入调查并协调候选项

```bash
node scripts/deep-dive.mjs "$RUN_DIR/signals.json" "$RUN_DIR/gate.json" --cwd <project-dir> > "$RUN_DIR/investigation-evidence.json"

node scripts/reconcile-candidates.mjs "$RUN_DIR/investigation-evidence.json" \
  --gate "$RUN_DIR/gate.json" \
  --out "$RUN_DIR/reconciled-investigation.json"
```

`--cwd` 必须是已关联的项目目录，以便 `deep-dive.mjs` 验证同一项目关联，并为所有后续 `vercel metrics` 调用复用 `signals.json.commandScope.cliScope`。

在任何源代码调查前，协调过程会确定性地将被证伪的候选项转换为观察结果：

- `metric_mismatch`
- `error_storm`
- `deployment_regression`
- `scanner_only_no_metric`

### 2.3 生成简报并调查

列出工作项：

```bash
node scripts/prepare-investigation-brief.mjs "$RUN_DIR/signals.json" "$RUN_DIR/reconciled-investigation.json" --list > "$RUN_DIR/briefs-manifest.json"
```

为 `briefs-manifest.json.briefs` 中的每个条目生成一份简报。`group` 可以是 `toLaunch` 或 `platform`；不要只生成 `toLaunch` 简报。

```bash
mkdir -p "$RUN_DIR/briefs" "$RUN_DIR/sub-agent-outputs"
node scripts/prepare-investigation-brief.mjs "$RUN_DIR/signals.json" "$RUN_DIR/reconciled-investigation.json" \
  --group <brief.group> --index <brief.index> --out "$RUN_DIR/briefs/<brief.group>-<brief.index>.md"
```

使用 `briefs-manifest.json.briefs[].label` 作为可见的工作者名称，例如 `Low cache-hit route on /docs/llm-digest/[...slug]`，而不是 `toLaunch-7`。

并行分发规则：

- 1-2 份简报：内联调查。
- 3 份及以上简报：如果宿主支持，则为每份简报生成一个子代理。
- 不支持子代理的宿主：内联串行运行。

子代理约定：

- 整份简报就是完整提示。
- 只读取简报中列出的文件，以及需要时的路由局部导入。
- 使用 [references/recommendations.md](references/recommendations.md) 输出一条 JSON 建议或一条 JSON 无需更改的发现。
- 不要引用所提供引用子集之外的 URL。
- 不要建议检测到的版本不支持的框架功能。

如果子代理试图对整个仓库执行 grep，则该候选项格式不正确；应丢弃或不作判断，而不是扩大范围。

### 2.4 收集输出

将每个原始调查结果保存到 `$RUN_DIR/sub-agent-outputs/`，然后收集：

```bash
node scripts/collect-sub-agent-outputs.mjs \
  --manifest "$RUN_DIR/briefs-manifest.json" \
  --out "$RUN_DIR/recommendations.json" \
  "$RUN_DIR/sub-agent-outputs/"
```

收集器会提取 JSON、在前面添加预先解析的记录、强制执行清单顺序，并在 `candidateRef` 值缺失、重复、未知或不匹配时失败。

### 3. 验证建议

```bash
node scripts/verify-and-regen.mjs "$RUN_DIR/recommendations.json" \
  --signals "$RUN_DIR/signals.json" \
  --repo-root <project-dir> \
  --out "$RUN_DIR/verify.json"
```

此脚本会提取声明、验证文件/引用/版本适配性、评定质量、应用净化器、输出 `verifiedRecommendations`、`withheldRecommendations`、`renderableRecommendations`，并为失败或不安全的建议创建 `regenPlan`。

建议架构、写作规则、净化器顺序和评分规则：[references/recommendations.md](references/recommendations.md)。验证规则：[references/verification.md](references/verification.md)。

对于每个 `regenPlan` 条目，使用同一份简报重新运行，并添加一个 `Previous attempt failed these checks` 部分，列出 `topFailures`。仅当验证结果有所改善且引用没有被严重削减时，才保留重新生成的输出。

### 4. 渲染报告和最终消息

```bash
node scripts/render-report.mjs "$RUN_DIR/verify.json" "$RUN_DIR/gate.json" "$RUN_DIR/signals.json" \
  --project <name> \
  --out "$RUN_DIR/report.md" \
  --message-out "$RUN_DIR/final-message.json"
```

仅在开发该技能时使用 `--debug-out "$RUN_DIR/debug.json"`。面向客户的 Markdown 和聊天输出不得暴露 `passRate`、`quality`、净化器轨迹、原始子代理名称或其他实现字段。

渲染后，逐字输出 `final-message.json.body` 并停止。不要添加亮点、调试说明、原始计数、子代理摘要或额外解释。渲染阶段的去重、平台上限和严格安全丢弃可能改变客户可见的数量，因此绝不要根据原始 `verify.json` 进行概括。

报告结构和影响描述：[references/scoring.md](references/scoring.md)。

## 建议规则

每条建议都必须：

- 可追溯到已启动的候选项、平台候选项、预先解析的观察结果，或经验证且与流量无关的扫描器发现。
- 包含来自 `signals.json` 或 `evidence.deepDive` 的已观察指标证据。
- 涉及代码时，引用经过验证的文件及行号。
- 至少包含一个适用于检测到的框架/版本的允许引用。
- 使用精确的已观察性能数值。
- 只使用成本量级描述；绝不要面向客户给出 `$N` 节省金额。
- 不要建议缩短 Vercel Workflow 运行时端点（`/.well-known/workflow/v1/*`）的持续时间。这些是用于持久步骤/流程执行的生成式编排路由，应在调查前严格排除。
- Workflow 建议必须说明要改变的边界。有效示例：将持久任务加入队列并返回运行 ID，而不是等待完成；修复流重放/关闭/锁；或减少已验证的过量 Workflow Steps/Storage。不要根据 Workflow 端点的挂钟持续时间推断成本节省。
- 对于流式传输、SSE、可恢复聊天或其他有意长期保持的路由，不要仅凭挂钟函数持续时间将其描述为问题。必须有证据表明存在可避免的首字节前工作、高活跃 CPU、重复调用，或可以移出用户可见路径的响应后工作。
- 建议缓存时，指定具体的缓存策略。
- 除非证据证明可以安全缓存，否则以下响应应保持动态：认证敏感路径、错误、回退响应、缺失内容、无效请求、因地理位置/设备而变化的输出，以及未版本化的动态 URL。

对于 `signals.project` 中已经存在的事实，绝不要建议“验证 X 是否开启”，包括 Fluid compute 状态、内存层级、区域、函数内并发和超时。

## 扫描器规则

扫描器发现仅作补充。除非扫描器声明 `metadata.trafficIndependent === true`，否则丢弃标注为 `COLD-PATH` 或 `NO-ROUTE-MAPPING` 的发现。

与流量无关的示例：中间件匹配器、源映射、React Compiler 配置、构建设置。路由局部缓存或数据获取模式需要路由级流量证据。

扫描器文档：[references/scanner-patterns.md](references/scanner-patterns.md)。

## 最终客户术语

使用：

- `建议已就绪`
- `调查所得观察结果`
- `已调查，不建议更改`
- `本次运行未调查`

避免：

- `子代理`
- `不作判断`
- `通过率`
- `质量评分`
- `筛选`
- `大语言模型`

## 失败文案

使用以下消息，不要添加销售文案或流程细节。

**过去 14 天没有流量：**

> 此项目在过去 14 天内没有有意义的流量，因此路由级指标较为稀疏。我仍可检查与流量无关的扫描器发现和项目设置，但在流量积累起来之前，无法对路由修复进行排序。

**路由级指标不可用：**

> 使用 [references/observability-plus.md](references/observability-plus.md) 中的逐字选择模板。不要静默回退到纯代码模式；应提供两条路径供选择：启用 Observability Plus 并重新运行有指标依据的审计，或接受一次有限的纯代码运行。

**项目未关联：**

> 此工作树未关联到 Vercel 项目。运行 `vercel link --yes --project <project-name-or-id> --cwd <app-dir>`，然后重新运行审计。如果团队已知，请添加 `--team <team-id-or-slug>`。

**大多数路由到文件的映射失败：**

> 路由清单匹配到的路由不足可观测性数据中所见路由的一半。这在使用自定义路由的 monorepo 中很常见。我已经呈现了能够匹配的内容；其余内容会出现在“本次运行未调查”部分。
