<!-- source-sha256: e0357a8de226483dce83933ab1e543b563a3ef9c40e6cfaa2fefe31b58ac5c20 -->
---
name: public-qa-chatbot
description: >
  构建无需身份验证的公共问答聊天机器人小组件的最佳实践。
  涵盖速率限制、安全加固、成本优化、语义缓存、
  可观测性、用户体验模式、聊天滚动行为和架构。
  技术栈无关，并提供来自生产实现的具体示例。
license: MIT
metadata:
  author: aidotengineer
  version: "1.1"
  category: "chatbot"
  compatibility: 任何具有服务端 API 路由的 Web 框架
  tags: "rate-limiting, security, caching, observability, LLM, chat-ui, virtualization"
---
# 公共问答聊天机器人——最佳实践

这是一项用于构建无需身份验证、面向公众的问答聊天机器人小组件的综合技能，适用于营销网站、会议页面、文档门户以及其他需要在控制成本和滥用风险的同时为匿名访客提供服务的场景。

本技能提炼自为 [AI Engineer Europe 2026](https://ai.engineer/europe) 大会提供支持的生产实现，并补充了 [TanStack Virtual 的聊天指南](https://tanstack.com/blog/tanstack-virtual-chat)中的聊天滚动经验，以及 Mintlify 的[虚拟文件系统助手](https://www.mintlify.com/blog/how-we-built-a-virtual-filesystem-for-our-assistant)中的智能体检索经验。有关 Mintlify 模式的简洁 Markdown 参考版本，请参阅 [MINTLIFY_VIRTUAL_FILESYSTEM.md](MINTLIFY_VIRTUAL_FILESYSTEM.md)。

如需可运行的 React/TanStack Virtual 长聊天滚动演示以及展开式底部命令架，请使用 `assets/vite-react-tanstack-chat-demo`。该演示包括悬停/双击消息控件、低调的 token/延迟统计、工具调用和多模态示例、通过左右滑动切换助手回答变体，以及带实时转录和音频波形图的 Realtime 语音采集栏。

![带实时语音转录和底部命令架的公共问答聊天机器人演示](assets/chatbot-demo-voice-live.png)

在本地运行演示：

```bash
cd assets/vite-react-tanstack-chat-demo
npm install
npm run dev -- --port 5179
```

若要体验 Realtime 语音路径，请在设置 `OPENAI_API_KEY` 后启动开发服务器。标准 API 密钥只能保留在服务端；浏览器应接收临时 Realtime 客户端密钥。

## 何时使用此技能

- 在公共网站中嵌入聊天机器人小组件（无需用户登录）
- 根据已知 FAQ / 知识库回答问题
- 使用由 LLM 驱动的回答服务匿名访客
- 需要防范滥用、成本超支和 API 配额耗尽
- 构建受约束的问答机器人（而非通用助手）
- 审查公共聊天机器人的小组件用户体验、流式传输行为、滚动锚定或历史记录加载

## 技术栈选择

本技能以技术栈无关的方式编写。参考实现使用下列技术栈，但每个组件均可替换：

| 组件 | 参考选择 | 替代方案 |
|---|---|---|
| **LLM 提供商** | Gemini 3.1 Flash-Lite（通过 `@ai-sdk/google`） | OpenAI GPT-4o-mini、Anthropic Claude Haiku、Mistral、通过 Groq/Together 使用 Llama |
| **AI SDK** | Vercel AI SDK v6（`ai`） | LangChain、LlamaIndex、直接使用提供商 SDK |
| **托管平台** | Vercel（无服务器函数） | Cloudflare Workers、AWS Lambda、Railway、Fly.io、Render |
| **速率限制** | Upstash Redis（`@upstash/ratelimit`） | Cloudflare Rate Limiting、AWS WAF、Redis（自托管）、Arcjet |
| **语义缓存** | Upstash Vector + Gemini Embeddings | Pinecone、Weaviate、Qdrant、pgvector、Cloudflare Vectorize |
| **智能体文档检索** | 建立在已索引文档之上的只读虚拟文件系统 | 普通 RAG、托管搜索 API；仅为异步/开发者工具使用真实沙箱 |
| **嵌入模型** | Gemini `text-embedding-004`（128 维） | OpenAI `text-embedding-3-small`、Cohere Embed v3、Voyage AI |
| **可观测性** | Braintrust（`wrapAISDK`） | Langfuse、Helicone、LangSmith、OpenTelemetry、Datadog LLM Obs |
| **前端** | React（内联组件） | Vue、Svelte、原生 JS、Web Components |
| **长聊天虚拟化** | TanStack Virtual 聊天支持 | 短小组件使用原生滚动、react-virtuoso；仅在已有验证时使用自定义虚拟列表 |

不要要求每个公共 FAQ 小组件都使用虚拟化。简短且有长度上限的聊天可以继续使用简单的 DOM 列表。当对话可能变得很长、行具有动态高度、需要在顶部插入更早的历史记录，或流式输出使滚动锚定变得脆弱时，再使用虚拟化聊天列表。使用 React 且确有理由使用虚拟列表时，应优先使用 TanStack Virtual 的聊天支持，而不是自定义滚动计算。

同样，不要要求每个公共 FAQ 小组件都使用智能体式文档浏览。对于简短、稳定的 FAQ，普通 RAG 已经足够。当答案分布在多个页面、用户询问精确语法、文档具有重要的层级结构，或 top-k 检索经常遗漏专家会使用 `grep` 查找的章节时，再添加虚拟文档文件系统。

***
## 1. 速率限制

### 多层速率限制

在多个粒度上应用限制以防止滥用：

- **每轮对话**：限制每个会话的消息数（例如每个会话 9 轮）
- **每位访客每天**：限制每个 IP 每天的会话数（例如每天 15 个）
- **全局每天**：限制所有访客每天的会话总数（例如每天 3000 个）

```typescript
// Example constants
const LIMITS = {
  turnsPerSession: 9,
  sessionsPerVisitorPerDay: 15,
  globalSessionsPerDay: 3000,
};
```

### 在生产环境中使用分布式速率限制

内存速率限制会在每次无服务器冷启动时重置，并且无法跨实例共享。生产环境应使用分布式存储：

**Upstash Redis（参考）：**
```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const redis = new Redis({ url: REDIS_URL, token: REDIS_TOKEN });
const limiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(15, "1 d"), // 15 per day
  prefix: "chatbot:visitor",
});
const { success } = await limiter.limit(clientIp);
```

**替代方案：**
- **Cloudflare Rate Limiting**——内置于 Cloudflare Workers，无需外部数据库
- **Arcjet**——带机器人检测功能的即插即用速率限制 SDK
- **AWS WAF**——边缘侧基于速率的规则
- **自托管 Redis**——`ioredis` + 自定义滑动窗口逻辑

始终为本地开发保留内存回退方案：
```typescript
const useDistributed = !!redisUrl && !!redisToken;
if (!useDistributed) {
  // Fall back to in-memory Map for local dev
}
```

### 服务端权威计数

绝不要信任客户端上报的轮次计数或会话标志。服务端必须自行根据 `messages` 数组统计轮次：

```typescript
// Server counts turns - never trust client-reported values
const userTurnCount = messages.filter(m => m.role === "user").length;
const isNewSession = userTurnCount <= 1;
```

### 会话计数时机

仅在服务端确认成功响应**之后**递增会话计数器，而不是在用户提交时递增。这样可以避免请求失败、网络错误或流被中止造成虚假的会话计数：

```typescript
// Client-side: count after first assistant response arrives
useEffect(() => {
  const hasAssistantMessage = messages.some(m => m.role === "assistant");
  if (hasAssistantMessage && !sessionCounted.current) {
    sessionCounted.current = true;
    incrementSessionCount();
  }
}, [messages]);
```

### 非新会话处理

当请求并非新会话（即现有对话中的后续轮次）时，完全跳过每日会话计数器的递增。为进行速率限制，一段对话中只有第一轮应被计为一个“会话”：

```typescript
if (!isNewSession) {
  return { allowed: true }; // Skip session counting for follow-up turns
}
```

### BYOK（自带密钥）回退方案

受到速率限制时，允许用户输入自己的 API 密钥以继续聊天。这样既能保留良好的用户体验，又会将滥用产生的成本转移给用户自己：

```typescript
// Skip rate limiting when user provides their own key
if (!userApiKey) {
  const limit = await checkRateLimit(ip, turnCount, isNewSession);
  if (!limit.allowed) {
    return res.status(429).json({ error: limit.reason, rateLimited: true });
  }
}
const apiKey = userApiKey || serverKey;
```

提供获取密钥的直接链接（例如 Gemini 使用 https://aistudio.google.com/apikey，OpenAI 使用 https://platform.openai.com/api-keys）。

***
## 2. 安全性

### 来源验证

根据允许列表检查 `Origin` 或 `Referer` 请求头。这可以防止第三方嵌入脚本消耗你的 API 配额等跨站请求滥用：

```typescript
const origin = req.headers.origin ?? req.headers.referer ?? "";
const allowedHosts = ["localhost", "yourdomain.com", "vercel.app"];
if (origin && !allowedHosts.some(h => origin.includes(h))) {
  return res.status(403).json({ error: "Forbidden" });
}
```

> **注意：** 对 v1 而言，子字符串匹配（`origin.includes(h)`）可以接受，但理论上可能匹配到精心构造的域名。若要进行更严格的验证，请解析 URL 并比较主机名。

### 输入大小限制

同时限制消息数量和单条消息长度，以防止通过填充 token 抬高 LLM 账单的攻击：

```typescript
const MAX_MESSAGES = 10;
const MAX_MESSAGE_LENGTH = 2000;

const trimmedMessages = messages.slice(-MAX_MESSAGES).map(m => ({
  ...m,
  parts: m.parts.map(p =>
    p.type === "text" && typeof p.text === "string"
      ? { ...p, text: p.text.slice(0, MAX_MESSAGE_LENGTH) }
      : p
  ),
}));
```

还应限制模型输出：对于简短的问答回复，使用 `maxOutputTokens: 500`。

### 验证所有参数

绝不要信任针对用户提供值的 `as` 类型断言。应根据已知集合进行验证：

```typescript
const VALID_PAGES = new Set(["europe", "home", "worldsfair"]);
if (!VALID_PAGES.has(page)) {
  return res.status(400).json({ error: "Invalid page parameter." });
}
```

### 对检索界面预先执行访问权限裁剪

对于基于文档的聊天机器人，访问控制必须发生在检索之前，而不是答案生成之后。如果机器人公开语义搜索、精确搜索或虚拟文档文件系统，应对每个界面应用相同的可见性过滤器：

- 在构建模型可浏览的任何路径树之前，排除未发布、草稿、内部、仅限客户或受角色限制的页面。
- 对向量、关键词和分块查询应用相同的过滤器。不要只在 UI 中隐藏路径，却仍让相应分块可以被搜索。
- 应优先完全省略不可访问的路径。模型不应能够提到“有一个内部计费页面，但你无法访问它”。
- 在索引分块中包含 `isPublic`、`groups`、`tenantId`、`docsVersion` 或等效元数据，以便低成本且可测试地进行过滤。

### 安全的错误处理

- 绝不要向客户端泄露原始 SDK 错误字符串（其中可能包含来自 BYOK 的 API 密钥）
- 绝不要记录完整的错误对象（其中可能包含敏感数据）
- 返回通用错误消息：

```typescript
} catch {
  console.error("Chat API error");
  return res.status(500).json({
    error: "An error occurred processing your request. Please try again.",
  });
}
```

### 无服务器平台上的 IP 解析

使用平台信任的请求头。在 Vercel 上：`x-real-ip` > `x-vercel-forwarded-for` > `x-forwarded-for`。标准的 `x-forwarded-for` 可以被客户端伪造。

**替代方案：**
- **Cloudflare：** `CF-Connecting-IP`
- **AWS ALB/CloudFront：** `X-Forwarded-For`（由 AWS 设置时，第一个 IP 可信）
- **Fastly：** `Fastly-Client-IP`

### 禁用非文本模态

如果只需要文本回复，请显式限制模型：

```typescript
const model = provider("gemini-3.1-flash-lite", {
  responseModalities: ["TEXT"], // Gemini-specific
  // For OpenAI: modalities: ["text"]
});
```

还应在系统提示词中声明“纯文本助手”，作为纵深防御措施。

***
## 3. 成本优化

### 语义缓存

使用向量相似度搜索，为语义相似的问题缓存并复用回答。对于用户会以不同措辞重复询问相同问题的 FAQ 类聊天机器人，此方法最为有效。

**Upstash Vector（参考）：**
```typescript
import { Index } from "@upstash/vector";

const vectorIndex = new Index({ url: VECTOR_URL, token: VECTOR_TOKEN });

// Lookup: check cache before calling LLM
const results = await vectorIndex.query({
  vector: await getEmbedding(question),
  topK: 1,
  includeMetadata: true,
  filter: `page = '${page}'`,
});
if (results[0]?.score >= 0.92 && results[0]?.metadata?.answer) {
  return results[0].metadata.answer; // Cache hit - skip LLM call
}

// Store: cache after LLM responds (fire-and-forget)
void vectorIndex.upsert({
  id: `cache-${Date.now()}`,
  vector: embedding,
  metadata: { question, answer, page, cachedAt: Date.now() },
});
```

**关键决策：**
- **相似度阈值**：使用 0.92 以上，以避免返回错误的缓存回答。较低的值会提高命中率，但也会增加错误回复的风险。
- **嵌入维度**：128 维足以进行 FAQ 相似度判断，且计算和存储成本低于完整的 768/1536/3072 维。
- **缓存范围**：只缓存第一轮问题（命中率最高，实现最简单）。
- **TTL**：7 天较为合理；过期不久的回答仍优于完全没有缓存。

**替代方案：**
- **Pinecone**——支持元数据过滤的托管向量数据库
- **pgvector**——如果你已经使用 PostgreSQL
- **Cloudflare Vectorize**——边缘原生，可与 Workers 搭配
- **Qdrant/Weaviate**——可自托管或使用云服务，查询能力更丰富

### 强制执行缓存 TTL

始终在缓存条目的元数据中存储 `cachedAt` 时间戳。查询时拒绝超过 TTL（例如 7 天）的条目。这样可以防止陈旧回答无限期存在，尤其是在 FAQ 内容发生变化时：

```typescript
const CACHE_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 days
if (Date.now() - result.metadata.cachedAt > CACHE_TTL_MS) {
  // Stale - treat as cache miss
}
```

### 缓存命中的流协议一致性

返回缓存回答时，应使用与实时 LLM 回复**相同的流式协议**。不要切换到不同的响应格式（例如从 UI Message Stream 切换到手动 Data Stream Protocol）。格式不一致会导致客户端解析错误和用户体验损坏：

```typescript
// BAD: different format for cache hits
res.write(`0:${JSON.stringify(cachedText)}\n`); // Manual Data Stream Protocol
// GOOD: same format for both paths
const stream = createUIMessageStream({ /* ... */ });
pipeUIMessageStreamToResponse(stream, res);
```

### 优化精确搜索

对于公开 `grep` 风格工具的文档助手，应避免通过网络扫描每个页面或分块。使用两阶段精确搜索路径：

1. **粗筛选**：让文档数据库查找元数据或文本中可能包含固定字符串或正则表达式的页面。尽可能使用数据存储原生过滤器，例如 `$contains`、全文索引、三元组搜索，或按章节/路径进行元数据过滤。
2. **批量预取**：一次性获取匹配页面的所有候选分块，并按 `page` 和 `chunk_index` 排序。
3. **精细过滤**：在内存中执行精确字符串或正则表达式匹配，只返回最终命中的路径/片段。
4. **缓存**：按 `{ path, docsVersion }` 缓存预取的页面分块，使重复的 `grep`/`cat` 工作流不会重复访问数据库。

记录候选数量和最终命中数量。如果粗筛选返回过多页面，应让模型缩小查询范围，而不是悄悄执行昂贵的全语料库扫描。

### FAQ 列表视图

在聊天界面旁提供可浏览的 FAQ 列表。这样，提出常见问题的用户完全不需要触发任何 LLM 调用：

```typescript
// Structured FAQ data for UI rendering
export const FAQ_QUESTIONS: Array<{
  category: string;
  question: string;
  answer: string;
}> = [
  { category: "Ticketing", question: "Can I get a refund?", answer: "Yes, per our refund policy..." },
  // ...
];
```

按类别组织为可展开的章节。点击问题后，可以直接显示预先编写的回答，也可以将问题发送到聊天中，以获得更详细的 LLM 回复。

### 使用足以胜任任务的最便宜模型

对于受约束的问答聊天机器人，通常不需要最强大的模型：

| 模型 | 输入成本 | 输出成本 | 最适合 |
|---|---|---|---|
| Gemini 3.1 Flash-Lite | $0.25/1M | $1.50/1M | 最便宜，适合 FAQ |
| GPT-4o-mini | $0.15/1M | $0.60/1M | 成本与质量平衡良好 |
| Claude Haiku | $0.25/1M | $1.25/1M | 速度快，善于遵循指令 |
| Llama 3.3 70B（通过 Groq） | 提供免费套餐 | 提供免费套餐 | 成本敏感型原型 |

### 较短的输出限制

将 `maxOutputTokens` 设置为满足需求的最小值（例如，2–4 句话的回答使用 500 个 token）。这样可以限制每次请求的成本，并保持回复简洁。

### 上下文缓存

在模块级别预先构建并缓存系统提示词上下文。这样可避免每次请求时重新执行昂贵的字符串拼接：

```typescript
let cachedContext: Record<string, string> | null = null;

function buildContext(): Record<string, string> {
  if (cachedContext) return cachedContext;
  // ... expensive computation ...
  cachedContext = result;
  return cachedContext;
}
```

***
## 4. 可观测性

### 追踪每次 LLM 调用

检测所有 LLM 调用的输入/输出、延迟、token 用量和成本。这对于监控滥用、调试和成本跟踪至关重要。

**Braintrust（参考）：**
```typescript
import { initLogger, wrapAISDK } from "braintrust";
initLogger({ projectName: "my-chatbot", apiKey: BRAINTRUST_API_KEY });
const { streamText } = wrapAISDK(ai); // Auto-traces all calls
```

**替代方案：**
- **Langfuse**——开源、可自托管，支持 OpenAI/Anthropic/自定义模型
- **Helicone**——基于代理，无代码集成
- **LangSmith**——适用于使用 LangChain 的情况
- **OpenTelemetry**——厂商中立，可导出到 Datadog/Honeycomb/Grafana
- **Datadog LLM Observability**——适用于已经使用 Datadog 的情况

### 记录语义缓存命中

跟踪缓存命中率，以了解节省的成本并调节相似度阈值。缓存命中是一次“免费”回复，省去了一次 LLM 调用。

### 追踪检索工具调用

将检索工具与 LLM 调用分开追踪。对于语义搜索、精确搜索和虚拟文件系统工具，记录：

- 工具名称、查询/模式、请求路径和文档版本。
- 延迟、缓存命中/未命中、数据库往返次数、获取的分块数、候选数量和最终结果数量。
- 模型是否从宽泛的语义搜索升级为精确的 `grep`/`cat`/`ls` 探索。
- 用户可见的结果信号，例如答案引用率、“我不知道”比例、赞/踩以及转交/升级率。

这可以帮助你判断智能体检索是在提升答案质量，还是仅仅增加了成本和延迟。

### 不要记录敏感数据

避免记录完整的错误对象、API 密钥或用户个人身份信息。只记录足够用于调试的信息（错误类型、状态码、IP 哈希）。

***
## 5. 用户体验模式

### Markdown 渲染

在聊天回复中启用 Markdown，并通过系统提示词指示模型使用它：

```text
You may use markdown formatting in your responses when appropriate:
- Use **bold** for emphasis on key information like dates, prices, or venue names
- Use [links](url) when referencing websites
- Use bullet points for lists of speakers, sessions, or options
- Keep formatting light and readable
```

**React：** `react-markdown` + `remark-gfm`  
**Vue：** `vue-markdown-render`  
**原生 JS：** `marked` 或 `markdown-it`

### 可拖动和调整大小的窗口

允许用户重新定位聊天窗口并调整其大小。将几何信息持久化到 `localStorage`，使其在页面重新加载后仍然保留。将位置限制在视口边界内：

```typescript
const newX = Math.max(0, Math.min(
  e.clientX - dragOffset.x,
  window.innerWidth - geometry.width
));
```

### 流式回复

始终以流式方式返回回复，以提升感知速度。使用 SDK 的流式 API，而不是等待完整回复。首个 token 快速出现比总延迟更重要。

在 UI 中，随着 token 到达更新同一条进行中的助手消息。不要为每个 token 追加一行新消息。token 级别的消息行成本高昂，会破坏对话记录语义，并使滚动锚定更加困难。

### 聊天滚动与虚拟化

公共问答小组件通常一开始很短，因此在没有证据表明存在问题之前，使用普通滚动容器即可。当小组件可能包含很长的历史记录、富 Markdown、工具结果、图像、代码块、历史记录分页，或高度会随着 token 流式传输增长的消息时，再添加虚拟化。

确有必要使用虚拟化时，建议 React 实现使用 TanStack Virtual 的聊天支持，但应保持其可选且可替换。最重要的是以下滚动约定：

- 将聊天视为一个**末端锚定的反向信息流**，而不是普通的顶部锚定列表。
- 消息数据保持正常的时间顺序；避免使用 `flex-direction: column-reverse`、反向变换，以及手动维护的 `scrollTop += delta` 记账逻辑。
- 使用稳定的消息 ID 作为行键。以索引为键无法在顶部插入较早的历史记录后保持位置。
- 加载较早的历史记录时，应使用普通数组更新在前面插入消息，例如 `setMessages((current) => [...olderMessages, ...current])`。
- 仅当用户原本就在最新消息附近时才跟随新追加的消息。如果用户已向上滚动阅读历史记录，传入的输出不得将其强行拉回底部。
- 使用明确的“接近最新位置”阈值，例如约 `80px`，不要使用在不同浏览器和动态高度下很脆弱的精确底部检查。
- 当用户离开末端时，提供“最新消息”或“跳到底部”控件。
- 对于真实聊天，动态行高是默认情况。Markdown、链接、代码、工具输出和流式文本应被测量，或允许重新排版而不发生重叠。
- 对高频 token 流式传输，优先使用即时/自动跟随。平滑滚动在离散追加时可能效果不错，但应进行验证，因为动画目标可能会与动态测量相冲突。
- 将分页游标、`hasMoreHistory`、加载标志和请求去重保留在应用状态中。虚拟化器应接收当前有序消息数组，而不是负责数据获取。

TanStack Virtual 使用 `anchorTo: 'end'`、`followOnAppend`、`scrollEndThreshold`、稳定的 `getItemKey`、`measureElement`、`isAtEnd()`、`getDistanceFromEnd()` 和 `scrollToEnd()` 来映射这些经验。这些 API 是实用的默认选择，而非硬性依赖。

### 底部命令架

不要把编辑器仅仅当作文本框。对于 AI 应用，屏幕底部是便于拇指触及的宝贵空间，可以放置用户在组织提示词时所需的操作：附件、工具、模型、语音、发送、模式、推理深度、运行时上下文和工具启动器。

当应用拥有足够多的控件时，使用渐进式底部命令架：

- 默认编辑器保持紧凑：输入框、添加/附件、工具开关、模型标签、麦克风和发送。
- 将次要控件展开到底部面板，而不是把所有控件都塞进默认编辑器。
- 无论处于紧凑还是展开状态，都应让发送操作只需轻触一次。
- 保持主画布视觉平静；让底部命令架成为命令平面。
- 使用紧凑标签显示模式和执行状态，例如 `Plan` / `Build`、工作强度、设备/项目/分支，以及预算或用量。
- 将提示词编辑过程中可能使用的工具启动器放入展开的命令架，例如终端、文件搜索、Web 搜索、文档或附件。
- 在展开的命令架上方添加明确的关闭/折叠控件，使用户可以收回垂直空间。
- 对于没有工具或设置的简单公共 FAQ 小组件，应避免使用此模式。对于受约束的问答，紧凑编辑器加 FAQ 标签通常已经足够。
- 为紧凑编辑器预留布局空间，然后让展开的工具栏控件以覆盖层形式向上延伸。打开工具不应调整聊天记录的大小，也不应导致其跳动或重新锚定。
- 测试键盘打开/关闭、安全区域边距、命令架展开/折叠、消息流式传输，以及命令架处于两种状态时的历史记录阅读体验。

### 优雅降级

每项可选服务都应具有回退方案：

| 服务 | 不可用时…… |
|---|---|
| Redis（速率限制） | 回退到内存计数器 |
| 向量数据库（缓存） | 跳过语义缓存，始终调用 LLM |
| 可观测性（追踪） | 跳过追踪，在本地记录日志 |
| 服务端 API 密钥 | 提示用户使用 BYOK |
| 虚拟化聊天列表 | 回退到有对话记录长度限制的原生滚动列表 |

```typescript
// Pattern: optional service with graceful fallback
const vectorIndex = vectorUrl && vectorToken
  ? new Index({ url: vectorUrl, token: vectorToken })
  : null; // null = skip caching

if (vectorIndex) { /* try cache */ }
// Always falls through to LLM call
```

### 悬停预览

当用户将鼠标悬停在聊天气泡上时，显示最热门的 FAQ 问题。这能让用户立即了解聊天机器人可以提供哪些帮助，并减少“不知道该问什么”的阻力。

### 感知主题的自适应配色

在支持深色/浅色模式的页面中嵌入聊天机器人小组件时，应使聊天机器人的颜色与页面背景形成**对比**：

- 深色页面 -> 白色/浅色聊天机器人
- 浅色页面 -> 黑色/深色聊天机器人

接收页面的主题状态（例如 `isDark` 属性），并从单个主题调色板函数派生所有颜色。使用 `useMemo` 避免每次渲染时重新计算：

```tsx
const theme = useMemo(() => getTheme(isDark), [isDark]);
// getTheme returns 40+ color tokens: bg, text, borders, buttons, surfaces, shadows
```

定义全面的颜色 token，使每个 UI 元素都能自适应。这样可以避免在整个组件中散布硬编码颜色，并让整个小组件在一个位置响应主题变化。

***
## 6. 架构

### 可插拔组件

将聊天机器人设计为一个接收属性的独立组件，使其可以放入具有不同品牌和上下文的任何页面：

```tsx
<Chatbot
  page="europe"
  accentColor="#7C3AED"
  title="AI Engineer Europe Assistant"
/>
```

### 使用工具调用而非填塞上下文

不要将所有数据都塞入系统提示词，而应公开可供模型按需调用的工具。这样可以缩小上下文窗口，并提高回复准确性：

```typescript
tools: {
  search_speakers: tool({
    description: "Search for speakers by name, company, or role",
    inputSchema: jsonSchema<{ search?: string }>({ ... }),
    execute: async (args) => searchSpeakers(args),
  }),
  search_sessions: tool({
    description: "Search sessions by title, speaker, day, type, or track",
    inputSchema: jsonSchema<{ search?: string; day?: string }>({ ... }),
    execute: async (args) => searchSessions(args),
  }),
}
```

### 用于智能体检索的虚拟文档文件系统

Top-k RAG 适合简单的 FAQ 问题，但当答案横跨多个页面、用户需要精确语法，或正确页面未进入嵌入距离最近的结果时，它就会失效。对于基于文档的聊天机器人，可以考虑将知识库公开为只读虚拟文件系统，使模型能够使用 `ls`、`cat`、`find` 和 `grep` 等熟悉的工具进行探索。

关键思想是向模型提供**文件系统工作流**，不一定要提供真实文件系统。Mintlify 的 ChromaFs 模式将 shell 命令映射到现有文档索引，而不是为每位访客启动一个沙箱。这对于公共聊天机器人的延迟和成本至关重要：其文章报告称，会话创建的 p90 从使用沙箱/仓库设置时约 `46s`，下降到在 Chroma 上使用虚拟文件系统时约 `100ms`。

推荐形式：

- 将文档站点的路径树（例如页面 slug 和章节路径）作为紧凑的 JSON 构件，存储在与索引内容相同的数据存储中。
- 初始化会话时，将路径树作为 `Set<path>` 加 `Map<directory, children>` 加载到内存中，使 `ls`、`cd` 和基本 `find` 不需要网络调用。
- 在路径树到达模型之前应用访问控制。对于公共小组件，这通常意味着裁剪未发布、私有、草稿、仅限客户或仅限管理员的页面。模型不应看到它无法读取的路径。
- 通过获取页面的所有分块、按 `chunk_index` 排序并重新组装完整页面，实现 `cat /path/page.mdx`。在会话期间缓存页面读取结果，使重复查看成本较低。
- 对 OpenAPI 规范、生成的 API 参考 JSON、变更日志或带版本的文档等大型构件，支持惰性文件指针。在 `ls` 中显示文件，但仅在模型运行 `cat` 时获取内容。
- 将文件系统明确设为只读。任何类似写入的操作都应返回 `EROFS` 风格的错误，使助手可以自由探索，而无需进行状态清理或承担跨用户修改风险。
- 将递归 `grep` 优化为两阶段搜索：使用向量/文档数据库进行粗筛选以识别候选页面，然后在内存中对获取的候选内容执行精确字符串或正则表达式匹配。这样无需通过网络扫描每个文件，也能提供精确匹配行为。

尽可能将虚拟文件系统公开为范围狭窄的工具，而不是通用 shell：

```typescript
tools: {
  list_docs: tool({
    description: "List child paths under a documentation directory.",
    inputSchema: jsonSchema<{ path: string }>({ ... }),
    execute: async ({ path }) => docsFs.ls(path),
  }),
  read_doc: tool({
    description: "Read a full documentation page by path.",
    inputSchema: jsonSchema<{ path: string }>({ ... }),
    execute: async ({ path }) => docsFs.cat(path),
  }),
  search_docs_exact: tool({
    description: "Search docs by exact string or regex and return matching paths/snippets.",
    inputSchema: jsonSchema<{ pattern: string; regex?: boolean }>({ ... }),
    execute: async ({ pattern, regex }) => docsFs.grep(pattern, { regex }),
  }),
}
```

当聊天机器人需要像文档专家一样工作时，使用此模式。对于宽泛的问题，保留普通语义搜索作为第一遍工具；当模型需要精确措辞、语法、跨页面综合或基于来源的引用时，再让它升级到 `grep`/`cat`/`ls`。

### 系统提示词结构

按以下顺序组织系统提示词：

1. **角色和约束**——“你是会议助手……”
2. **格式说明**——“适当时使用 Markdown……”
3. **工具使用指南**——“使用工具搜索演讲者/会议环节……”
4. **硬性约束**——“仅文本，不使用图像/音频……”
5. **回退说明**——“如果不知道，建议发送邮件……”
6. **参考数据**——FAQ 文本、演讲者列表、会议环节列表

### 使用 API 路由，而非边缘函数

对于需要流式传输和外部服务调用（Redis、向量数据库、可观测性）的聊天机器人端点，应使用标准 API 路由/无服务器函数，而不是边缘函数。边缘函数具有更严格的大小和依赖限制，其冷启动特性也可能在导入多个 SDK 时造成问题。

***
## 7. 知识库管理

### 路径树索引

对于大型文档站点，应在分块索引旁生成文档清单：

```typescript
type DocsPath = {
  path: string;        // "/auth/oauth.mdx"
  title: string;       // "OAuth"
  isPublic: boolean;
  groups: string[];
  updatedAt: string;
  sourceId: string;
  docsVersion: string;
};
```

运行时，将经过访问权限裁剪的清单加载到内存：

- 使用 `Set<string>` 存储有效文件路径。
- 使用 `Map<string, string[]>` 进行目录到子项的查找。
- 可选的标题/路径别名，以实现更宽容的 `find_docs` 行为。

这样可以使 `list_docs`、`find_docs` 和路径验证完全在内存中完成。当 `docsVersion` 变化时，重新构建路径树或使其失效。

### 结构化 FAQ 数据

维护两种形式的 FAQ 数据：

1. **用于系统提示词的扁平文本**——模型作为上下文读取的单个字符串
2. **用于 UI 的结构化对象**——包含 `question`、`answer`、`category` 字段的类型化数组，用于渲染 FAQ 列表视图

```typescript
// System prompt context (flat text)
export const FAQ_KNOWLEDGE_BASE = `
## TICKETING & PRICING
Q: Can I get a refund?
A: Yes, per our refund policy...
`;

// UI list view (structured)
export const FAQ_QUESTIONS = [
  { category: "Ticketing", question: "Can I get a refund?", answer: "Yes..." },
];
```

### 从分块重新组装完整页面

分块向量结果适合发现内容，但对于最终回答而言通常损失过多信息。对于 `read_doc(path)` 或引用验证，应获取整个页面：

```typescript
const chunks = await vectorIndex.query({
  topK: 200,
  includeMetadata: true,
  filter: `path = '${path}' AND docsVersion = '${docsVersion}'`,
});

return chunks
  .sort((a, b) => a.metadata.chunk_index - b.metadata.chunk_index)
  .map(chunk => chunk.metadata.text)
  .join("\n\n");
```

按 `{ path, docsVersion }` 缓存完整页面读取结果。这样，模型就可以使用与人类文档读者相同的源材料，回答精确语法、多章节以及“比较这些页面”等问题。

### 包含场地/后勤详情

始终在上下文中直接包含实用信息（场地名称、地址、日期、购票 URL）。这些是最常见的问题，绝不应要求调用工具。

***
## 8. 常见陷阱

### 避免在 React 聊天小组件中使用操作 DOM 的库

像 `html2canvas` 这样会克隆并操作 DOM 的库，可能干扰 React 的虚拟 DOM 协调，导致页面重新加载、状态丢失或事件处理程序损坏。如果需要页面截图，请使用原生浏览器 API（`navigator.mediaDevices.getDisplayMedia`），或改在服务端进行捕获。

### 不要让聊天滚动变成一堆特殊情况

长聊天机器人小组件常见的失败模式是散落各处的滚动计算：`column-reverse`、反向变换、手动偏移增量、无条件的 `scrollToBottom` 和基于索引的键。这些技巧通常可以通过简短的手动测试，但在加载较早的历史记录、助手流式输出很长的 Markdown 回答，或用户阅读历史记录时有新输出到达的情况下就会失败。

应优先采用单一滚动约定：

- 数据中的消息按顺序排列。
- 行使用稳定 ID。
- 在顶部插入历史记录时，不改变用户的可见锚点。
- 仅当用户已经接近最新位置时才追加/跟随。
- 流式传输期间让当前助手消息行增长。
- 将“阅读历史记录”和“固定在最新位置”作为两种不同状态进行测试。

### 部署前验证准确的模型标识符

LLM 模型 ID 经常变化，并且可能要求使用 `-preview` 等后缀。错误的模型 ID 可能返回 200 OK 响应，但流正文为空或包含错误，从而让问题看起来像前端错误。部署前应始终根据提供商文档验证准确的模型 ID，并通过真实 API 调用进行测试。

### 推送前始终执行本地构建

推送到分支前，绝不要跳过 `pnpm build` / `npm run build`。在本地捕获 TypeScript 错误、导入问题和其他编译失败，比等待 CI 后再修复快得多。当多人编辑相同文件时，这一点尤其重要。

***
## 9. 检查清单

构建新的公共问答聊天机器人时，请使用此检查清单：

- [ ] 速率限制：每轮、每位访客和全局限制
- [ ] 生产环境使用分布式速率限制器（不能只有内存限制）
- [ ] 仅在服务端确认响应后递增会话计数器
- [ ] 非新会话跳过每日计数器递增
- [ ] API 端点进行 Origin/CSRF 验证
- [ ] 输入大小限制（消息数量 + 消息长度）
- [ ] 服务端权威轮次计数（不信任客户端）
- [ ] 安全错误处理（不泄露 SDK 错误，日志中不含个人身份信息）
- [ ] 根据托管平台正确解析 IP
- [ ] 为受到速率限制的用户提供 BYOK 回退方案
- [ ] 对第一轮问题使用强制执行 TTL 的语义缓存
- [ ] 缓存命中使用与实时回复相同的流协议
- [ ] 对于大型文档/聊天机器人，虚拟文件系统工具支持 `ls`/`cat`/`grep` 风格的探索，无需为每位用户创建沙箱
- [ ] 文档文件系统为只读、经过访问权限裁剪，并从有序分块重新组装完整页面
- [ ] 提供 FAQ 列表视图以减少 LLM 调用
- [ ] 对所有 LLM 调用进行可观测性检测/追踪
- [ ] 使用流式回复提升感知速度
- [ ] 流式 UI 让单条助手消息增长，而不是追加 token 行
- [ ] 在聊天回复中渲染 Markdown
- [ ] 限制为纯文本模态
- [ ] 使用与页面背景形成对比的主题感知颜色
- [ ] 可选服务不可用时能够优雅降级
- [ ] 短小组件使用简单的原生滚动，长/动态历史记录使用虚拟化
- [ ] 编辑器在紧凑和展开的底部命令架状态下都保持可用
- [ ] 展开的底部命令架不会遮挡最新消息或跳转控件
- [ ] 行键使用稳定的消息 ID；可在顶部插入内容的历史记录不得使用索引键
- [ ] 在顶部插入较早的历史记录时，保持用户可见消息的位置
- [ ] 仅当用户已接近最新位置时才跟随新消息
- [ ] 用户离开末端时显示“跳到最新消息”控件
- [ ] 动态消息高度重新测量时，不发生重叠、空白间隙或滚动漂移
- [ ] 移动设备键盘打开/关闭不会遮挡编辑器或破坏最新位置固定
- [ ] 系统提示词包含角色、约束、格式、工具和参考数据
- [ ] 不向前端暴露 API 密钥
- [ ] 已根据提供商文档验证准确的模型 ID
- [ ] 每次推送前本地构建均通过

## 链接

- 来源技能：[smol-ai/skills public-qa-chatbot](https://github.com/smol-ai/skills/blob/main/public-qa-chatbot/SKILL.md)
- TanStack Virtual 聊天博客：[Chat UIs Are Lists Until They Aren't](https://tanstack.com/blog/tanstack-virtual-chat)
- TanStack Virtual 聊天指南：[tanstack.com/virtual/latest/docs/chat](https://tanstack.com/virtual/latest/docs/chat)
- TanStack Virtual React 聊天示例：[tanstack.com/virtual/latest/docs/framework/react/examples/chat](https://tanstack.com/virtual/latest/docs/framework/react/examples/chat)
- Mintlify 虚拟文件系统助手：[How we built a virtual filesystem for our Assistant](https://www.mintlify.com/blog/how-we-built-a-virtual-filesystem-for-our-assistant)
- 参考实现：[github.com/aiDotEngineer/aiecode2025](https://github.com/aiDotEngineer/aiecode2025)（参见 `src/pages/api/chat.ts` 和 `src/components/Chatbot.tsx`）
- Agent Skills 规范：[agentskills.io/specification](https://agentskills.io/specification)
- Vercel AI SDK：[sdk.vercel.ai](https://sdk.vercel.ai)
- Upstash：[upstash.com](https://upstash.com)
- Braintrust：[braintrust.dev](https://braintrust.dev)
- Langfuse（替代方案）：[langfuse.com](https://langfuse.com)
- Arcjet（替代方案）：[arcjet.com](https://arcjet.com)
