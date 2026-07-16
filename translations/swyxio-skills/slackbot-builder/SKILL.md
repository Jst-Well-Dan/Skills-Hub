<!-- source-sha256: 1877c07d05b51014c0cc430df33fe3ea3bad4e39f4090b061a2f239f40727a36 -->
---
name: slackbot-builder
description: >
 将生产级 Slack 机器人构建为一套成熟度阶梯（L0–L6）：签名验证、
 快速确认 + 事件幂等、以线程作为会话、响应式反馈（表情回应、
 状态、实时流式传输）、Block Kit 交互 + 人工参与审批、
 原生 Agents & AI Apps 界面、文件/媒体输出 + 设置模态框、持久化
 长时间运行任务、速率限制 + 安全加固、模型调用追踪，以及
 多界面/多租户扩展。适用于构建或加固任何 Slack 应用、机器人、
 Slack 内智能体工作流，或 Slack Events API / Block Kit / 斜杠命令集成。
license: MIT
metadata:
 author: swyx
 version: "2.2"
 category: "slack"
 compatibility: Slack Events API、Slack Web API、无服务器或长时间运行的工作进程
 tags: "slack, bot, events-api, block-kit, modals, file-uploads, image-generation, durable-execution, workflows, cloudflare-workers, hono, kv, observability, tracing, agents"
---
# Slackbot 构建器

在创建或加固 Slack 应用、Slack 机器人、Slack 内智能体工作流或生产级
Slack 集成时使用此技能。

此技能按**成熟度阶梯（L0 → L6）**组织。找到你的目标级别，构建该级别及其
以下级别的全部内容，然后再晋级。每个级别都有一个完整的参考文件，其中包含
说明、代码和反模式——请阅读你当前所处级别的文件；不要一次性加载所有文件。

这些模式提炼自 AppSumo OpenInspect Slack 机器人
[packages/slack-bot/src](https://github.com/appsumo/openinspect/tree/main/packages/slack-bot/src)
中的源码级经验（检查于提交 `bd76f8d`），以及一个生产环境中的 aiebot 调度助手
（Web 和 Slack 共用同一个核心）。将两者视为务实的参考，而非依赖项。

## 贯穿每个级别的唯一规则

**Slack 是一个轻量适配器；所有智能都存在于与渠道无关的核心中。**
Slack 层只负责验证签名、调用 Slack Web API、渲染 Block
Kit，并委托给单一的核心入口点（例如 `runBotQuery(input, {emit})`）。
同一个核心服务于 Web、cron 和未来的机器人。如果你的 Slack 处理程序包含
业务逻辑，那就是缺陷。

## 阶梯

| 级别 | 主题 | 你要添加的内容 | 参考 |
|---|---|---|---|
| **L0** | 骨架——*它会响应* | `/health`、`/events`、签名验证、`url_verification`、快速返回 `200` | [level-0-skeleton.md](level-0-skeleton.md) |
| **L1** | 响应式问答（MVP）——*一个可用的机器人* | 3 秒内确认 + 异步工作、`event_id` 去重、忽略机器人、移除提及标记、在线程中调用 `chat.postMessage`、轻量 `fetch` 封装、JSON 日志 + 追踪 id | [level-1-mvp.md](level-1-mvp.md) |
| **L2** | 上下文感知——*感觉像在对话* | 以线程作为会话 + TTL 存储、有界的线程/频道上下文、私信、空提及时的提示、👀 表情回应 + `assistant.threads.setStatus` | [level-2-context.md](level-2-context.md) |
| **L3** | 交互式 / 智能体式——*执行操作，人工参与其中* | `/interactions`（已签名）、原地完成并更新的 Block Kit 审批、试运行验证、斜杠命令、路由/澄清阶梯、丰富且可操作的草稿（证据 + 产物、批量操作 + 应用前编辑、深层链接）、带消息内控制按钮的文件/媒体上传 + `views.open` 设置模态框（每线程）、实时状态流、受监控线程中的“我应该回复吗？” | [level-3-interactive.md](level-3-interactive.md) |
| **L4** | 原生智能体界面——*一流的智能体用户体验* | Agents & AI Apps 容器、`assistant_thread_started` 问候 + 建议提示词、线程标题、原生文本流式传输（`chat.startStream`/`appendStream`/`stopStream`），将你的 `emit` 流映射为带类型的回答 + 工具调用时间线，并优雅回退到消息流程 | [level-4-native-agent.md](level-4-native-agent.md) |
| **L5** | 已加固——*不会在凌晨 2 点把你叫醒* | 长时间运行的签名回调 + 持久 URL、App Home 偏好设置/仪表板（允许列表控制）、速率限制退避 + `ok:false` 处理、净化后的用户可见错误、存储 TTL 表、服务用户归属 + 审计、完整可观测性、安全/测试检查清单、权限范围降级、清单配置 | [level-5-hardened.md](level-5-hardened.md) |
| **L6** | 多界面 / 规模化——*完善的平台* | Web/Slack/cron 共用一个核心、多工作区/多租户、用于繁重任务的队列 + 背压、目标缓存、使用情况分析 + 回答质量反馈、紧急接管/降级配置 | [level-6-scale.md](level-6-scale.md) |

**可选能力参考**（仅在你要交付相应功能时加载——它们不是始终启用的阶梯级别）：
**图像生成** → [image-generation.md](image-generation.md)
（持久化渲染、模型参数门控、迭代按钮）。

## 明确主张

**通用不变量——在每个级别都成立**（特定级别的主张位于相应级别文件中，
因此只会在你到达该级别时加载）：

- 对于生产环境的 Web 服务，除非无法接收入站 HTTP，否则优先使用 **Events API，而不是 Socket Mode**。
- **解析前，必须根据原始请求正文验证每一个请求。** 没有例外，包括 `url_verification` 握手。
- **快速返回。** 在 Slack 的 3 秒窗口内完成身份验证、去重、将工作转入后台、记录日志并返回 `200`。
- **绝不要内联运行智能体工作。** 每个无服务器处理程序都有一个不易察觉的超时上限（Cloudflare `waitUntil` 约为 30 秒），它会在没有错误的情况下*取消*缓慢任务——机器人只会突然沉默。立即确认，在**持久化执行**中运行智能体循环 / 渲染 / 审计轮次，并保证最终返回结果或错误。在一个界面上修正执行模型后，再**审计每一个入口点**（提及、私信、斜杠命令、按钮、cron），这些入口都会调用同一个核心。→ [L5](level-5-hardened.md)
- **线程是会话边界。** 使用 `channel` + `thread_ts` 作为状态键。
- **绝不要回复自己。** 在执行昂贵任务前丢弃 `bot_id` / `bot_message` 和消息子类型。
- **使用真正的共享存储保存状态**（幂等性、会话、待处理的澄清、偏好设置）。内存映射仅用于开发环境。
- **Slack 是状态展示界面，而不是产品本身。** 对于长篇输出、日志、PR 和产物，应链接到持久化的 Web/会话 URL。
- **保持 Block Kit 简洁**；规范状态存在于你的后端中。
- **每个增强调用都应尽力而为**——表情回应、状态更新或上下文获取失败时，绝不能中止真正的回答。
- **不要静默降级。** 记录每条非默认路径（预设/确定性回答、跳过模型、提供商回退）——一个对所有提示词都静默返回相同答案的机器人，是最难调试的一类缺陷。
- **处处使用带追踪 id 的扁平 JSON 日志。** 否则 Slack 机器人会非常难以调试。

**特定级别的主张**（完整理由 + 实战教训见链接文件）：变更操作
需要人工确认，内联标志用于配置核心，根据原始请求而非上下文进行路由，
交互式操作必须*立即*确认点击 + 批量操作显示*增量*
进度，产物应提供迭代按钮 + 设置模态框交互 → [L3](level-3-interactive.md)；
检测*每一次*模型调用（而不仅是文本调用），缓慢任务在持久化执行中运行，而不是放在
后台 promise 中，每个入口界面都受到同等保护，每个任务都以保证送达的
结果或错误结束，并通过正确的界面机制交付 → [L5](level-5-hardened.md)；
图像生成的具体细节 → [image-generation.md](image-generation.md)。

## 如何使用此技能

1. 从表格中确定你的目标级别。
2. 打开该级别的参考文件（并快速浏览其下一级文件）。
3. 自底向上完成每个级别的检查清单；不要为了追逐 L3 功能而跳过 L0/L1 加固。
4. 在升级前，通过每个文件末尾的“达到以下条件即可晋级……”关卡。

## 实现倾向：从朴素方案开始

使用 TypeScript；一个小型 HTTP 框架（Hono、Fastify、Express 或原生路由
处理程序）；使用共享 KV/Redis/Postgres 存储状态；使用原始 Slack Web API `fetch` 封装，
除非项目中已经确立了某个 SDK；对于超过 1–2 秒的工作，使用队列或平台原生后台
执行机制；使用网页承载长篇输出。只有在产品需求明确时，才添加斜杠命令、
模态框、Socket Mode 或工作流步骤。
