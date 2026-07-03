# Kakuna Codebase Hardening Suite

来源：`libraries/swyxio-skills`

这个目录是从 `swyxio/skills` 中单独提取出来的 **Kakuna Codebase Hardening Suite**。它不是一个单一 skill，而是一组面向代码库硬化、产品化和发布前质量控制的工作流集合。

这套 suite 的核心目标是：把一个能跑的项目，逐步变成更容易维护、更适合上线、更容易排查问题、更有安全边界、更有测试保障的产品级代码库。

## swyxio 推荐怎么使用

swyxio 在原 README 中把 Kakuna suite 组织成一个递进式 hardening progression，也就是按阶段逐步加固代码库：

1. **Foundation 基础层**
   - 先用 `codebase-maintainability-guardrails` 建立默认工程标准。
   - 如果代码库已经混乱、文件过大、边界不清，再用 `antislop-codebase` 做结构性清理和迁移。

2. **Productization 产品化层**
   - 当代码结构已经足够清晰，可以进入 `productionize-app-with-services`，补齐审计日志、权限、API、OpenAPI/agent docs、功能开关、管理后台、可观测性和部署 smoke。

3. **Safety 安全层**
   - 用 `security-hardening` 做务实的应用安全审查和修复，覆盖认证、权限、密钥、输入校验、上传、SSRF、CORS/CSRF、速率限制和安全响应头等。

4. **Operability 可运维层**
   - 用 `observability-hardening` 增加结构化日志、错误分类、request id、trace、metrics、dashboard、alert 和用户可见的操作状态。
   - 用 `release-readiness-hardening` 建立发布门禁、环境校验、smoke tests、回滚方案、迁移检查、上线后验证和监控。

5. **Quality 质量层**
   - 用 `test-strategy-hardening` 审计测试是否真的有价值，再加固 flaky tests、contract tests、关键 e2e、回归夹具、运行时间和覆盖质量。

简单说，swyxio 推荐的顺序是：

```text
维护性标准 -> 结构清理 -> 产品化服务 -> 安全加固 -> 可观测性 -> 发布就绪 -> 测试策略
```

实际项目里不一定每次都要完整跑完 7 个。更务实的方式是按当前问题选择入口：

- 项目刚开始或正在做较大功能：从 `codebase-maintainability-guardrails` 开始。
- 项目已经很乱：从 `antislop-codebase` 开始。
- Demo 要变成产品：从 `productionize-app-with-services` 开始。
- 准备上线或已有安全顾虑：单独使用 `security-hardening`。
- 线上问题难排查：单独使用 `observability-hardening`。
- 快要发布：单独使用 `release-readiness-hardening`。
- 测试很多但不可信，或重构前需要安全网：单独使用 `test-strategy-hardening`。

## 1. codebase-maintainability-guardrails

路径：`codebase-maintainability-guardrails/`

这是默认工程标准 skill。它适合在大多数实质性编码工作中作为基础约束使用，尤其是前端、全栈、从零开始的应用、生产级重构、UI 迁移、功能开发等场景。

它关注的问题包括：

- 避免入口文件、路由文件、`App`、layout 逐渐变成巨型文件。
- 避免把业务逻辑堆进 `utils`、`helpers`、`misc` 这类模糊目录。
- 把纯领域逻辑、schema、reducer、normalizer、prompt builder、provider parser 等抽成可测试模块。
- 保护已有持久化状态、数据库结构、localStorage、API 合约，不在重构时偷偷破坏兼容性。
- 让 CSS 或 Tailwind 样式尽量归属到 feature，而不是散落成全局样式污染。
- 对 UI 变更做真实 viewport 的视觉检查，而不是只看构建通过。

适合使用的情况：

- 你要让 Codex/Claude 参与较大代码修改，希望它不要把项目越改越乱。
- 你正在做 feature work，但希望顺手保持代码边界清晰。
- 你要做行为保持型重构，不希望重构混入产品行为变化。
- 你在维护一个前端或全栈应用，希望建立一套默认工程护栏。

不适合单独解决的问题：

- 它不是完整迁移计划工具。如果项目已经严重混乱，需要用 `antislop-codebase`。
- 它不是安全审计、发布检查或可观测性专项。

## 2. antislop-codebase

路径：`antislop-codebase/`

这是结构性清理和迁移 skill。它用于把“能跑但很痛苦”的代码库，迁移成更小、更 typed、更有测试、更接近产品形态的模块结构，同时保持现有产品行为基本不变。

它关注的问题包括：

- 识别大文件、热点文件、混乱依赖、薄弱测试、入口膨胀、API 重复、样式散乱。
- 制定可执行迁移计划，包括目标、非目标、风险、分阶段切片、测试计划和并发工作边界。
- 先建立安全网，再拆分文件、抽取纯逻辑、稳定公共接口、迁移样式。
- 保持每一阶段都可构建、可测试、可回滚。
- 最后输出迁移审计材料，说明前后变化、指标、风险和剩余问题。

适合使用的情况：

- 代码库已经原型化过度，文件很大，逻辑纠缠，维护成本高。
- 用户说“帮我清理这个 repo”、“做 maintainability migration”、“把结构现代化”。
- 需要在不改变产品行为的前提下，拆分模块、补类型、补测试、收敛 API。
- 准备后续产品化、上线或团队协作，先把代码结构打稳。

不适合扩大的范围：

- 不要把它变成完整生产就绪项目。
- 安全审计、合规、SRE、incident response、深度可观测性、runbook 等，应该交给后续专项 skill。

## 3. productionize-app-with-services

路径：`productionize-app-with-services/`

这是产品化 skill。它适合在一个 demo 或 prototype 已经可用之后，把它补齐成更像真实产品的系统。

它关注的问题包括：

- 产品级启动和环境校验。
- 共享 action layer，让 UI、API、job、webhook、command palette 能复用同一套业务动作。
- API key、权限、scope、rate limit、REST/API、OpenAPI、agent docs。
- 审计日志、admin UX、角色权限、功能开关。
- PostHog 或等价产品分析、LLM/media 操作可观测性、健康检查。
- 部署 smoke、迁移审计、最终 audit microsite。

适合使用的情况：

- 一个 demo 已经能跑，但要交给真实用户、客户、团队或自动化 agent 使用。
- 需要加 API、API key、权限、审计日志、管理后台。
- 需要把本地或 UI-only 功能变成可通过程序调用的产品能力。
- 需要为 AI agents 或 bots 提供稳定接口、文档和幂等操作。

和 `antislop-codebase` 的区别：

- `antislop-codebase` 主要处理结构可维护性。
- `productionize-app-with-services` 处理产品运营能力：权限、审计、API、可观测性、feature flags、部署验证等。
- 如果代码本身还非常混乱，建议先做 `antislop-codebase`，再做产品化。

## 4. security-hardening

路径：`security-hardening/`

这是应用安全加固 skill。它不是形式化合规文档，而是务实地找出可利用风险，优先修复上线前最该修的安全问题。

它关注的问题包括：

- 认证、session、角色权限、server mutation 授权边界。
- API route、webhook、文件上传下载、provider 调用、数据库访问、后台任务、admin 工具。
- secrets、环境变量、token 存储、日志泄漏、依赖入口、网络出站风险。
- SSRF、上传约束、CORS、CSRF、rate limit、输入校验、安全响应头。
- 权限绕过、危险 URL/文件、错误日志泄漏等高风险路径的 focused tests。

适合使用的情况：

- 用户明确要求 appsec review、security audit、auth/session risk review。
- 准备上线，需要知道是否有 must-fix 安全问题。
- 最近加了 API、webhook、上传、provider integration、admin mutation。
- 担心日志泄漏密钥、用户内容或 prompt。

输出应包含：

- 已修复问题和证据。
- 剩余风险、严重程度、利用路径概述和下一步建议。
- 明确说明审查范围，不笼统声称“系统已经安全”。

## 5. observability-hardening

路径：`observability-hardening/`

这是可观测性加固 skill。它适合产品已经能跑，但线上失败难以解释、难以复现、难以定位的情况。

它关注的问题包括：

- 关键用户路径、API route、后台 job、provider call、长耗时操作、高成本路径。
- 结构化日志、错误类别、request/correlation id、trace、metrics、dashboard。
- 产品分析和工程诊断的边界。
- 隐私安全的 redaction policy，避免把用户内容、prompt、私密数据打进日志。
- 长任务的用户可见状态，例如进度、耗时、重试、失败原因。
- 能回答真实调试问题的 dashboard、log query、admin/developer view。

适合使用的情况：

- 线上问题出现后只能猜，没有清晰日志链路。
- 用户说“加 structured logging”、“加 request id”、“加 dashboard/alert”。
- 有 LLM、媒体处理、异步 job、第三方 provider 等难排查链路。
- 需要让管理员或用户看到任务状态，而不是一直 loading。

质量标准：

- 一次失败能从用户动作追到 route/job/provider，再追回最终响应。
- 日志低基数、结构化、默认脱敏。
- alert 对应明确动作，而不是制造噪音。

## 6. release-readiness-hardening

路径：`release-readiness-hardening/`

这是发布就绪 skill。它回答的问题是：这个项目能不能安全发布，我们凭什么知道？

它关注的问题包括：

- 部署平台、构建命令、运行时配置、环境变量、迁移、存储、队列、provider、feature flags。
- CI/CD、手动部署步骤、分支/tag/version 策略、生产 smoke 路径。
- 本地 gate：typecheck、lint、unit、build。
- integration/e2e/visual gate：覆盖本次改动影响的用户旅程。
- migration/data check、production-shaped smoke test、上线后日志和监控检查。
- env validation、health/readiness endpoint、rollback instructions、kill switch。

适合使用的情况：

- 用户问“这个能上线了吗”、“帮我做 release checklist”、“发布前检查一下”。
- 项目即将部署到 preview/staging/production。
- 有数据库迁移、配置变更、provider 变更或高风险新功能。
- 需要明确哪些 gate 通过、哪些跳过、哪些是接受的风险。

它的最终报告应该区分：

- 已通过的检查。
- 未运行或被阻塞的检查。
- 已接受的风险。
- 回滚步骤和上线后需要监控的内容。

## 7. test-strategy-hardening

路径：`test-strategy-hardening/`

这是测试策略加固 skill。它不是追求覆盖率数字，而是判断测试是否真的能防回归，并提高“每分钟测试运行时间带来的信心”。

它关注的问题包括：

- 发现测试命令、测试框架、e2e harness、fixture、mock、snapshot、CI、coverage、运行时间。
- 按层分类测试：unit、contract/schema、integration、e2e/browser、visual、smoke、load/perf、migration/data。
- 找出 flaky、重复 happy path、过度 mock、无效 smoke、脆弱 snapshot、实现细节断言。
- 为关键产品行为、外部/provider parsing、权限、迁移、历史回归建立高信号测试。
- 在重构前增加 characterization tests。
- 把慢但有价值的测试移入明确套件，而不是阻塞日常开发。

适合使用的情况：

- 测试很多，但大家不信任。
- 测试经常 flaky、慢、重复，或者失败信息没有价值。
- 准备大重构、发布、安全加固或产品化，需要先建立安全网。
- 想知道现有测试到底能抓住哪些真实 bug。

最终报告应该回答：

- 增加、删除、合并、跳过或隔离了哪些测试。
- 运行时间前后变化。
- 信心提升在哪里。
- 还缺哪些关键测试。

## 快速选择指南

| 你的当前问题 | 优先使用 |
| --- | --- |
| 正在做较大功能或重构，希望保持代码质量 | `codebase-maintainability-guardrails` |
| 代码库混乱、文件巨大、边界不清 | `antislop-codebase` |
| Demo 要变成真实产品 | `productionize-app-with-services` |
| 担心权限、密钥、输入、上传、API 安全 | `security-hardening` |
| 线上失败难排查，日志和状态不清楚 | `observability-hardening` |
| 准备发布，需要门禁、smoke、回滚方案 | `release-readiness-hardening` |
| 测试不可信，或重构/发布前需要测试安全网 | `test-strategy-hardening` |

## 包含的目录

- `codebase-maintainability-guardrails/`
- `antislop-codebase/`
- `productionize-app-with-services/`
- `security-hardening/`
- `observability-hardening/`
- `release-readiness-hardening/`
- `test-strategy-hardening/`

每个子目录都是一个独立 skill，包含自己的 `SKILL.md`，部分 skill 还带有 `references/` 参考资料。
