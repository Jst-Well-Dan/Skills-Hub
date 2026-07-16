<!-- source-sha256: 1bb15470c8bcedfc8aefeb2c7e852175fe0d28beccd8ae1c5ac707425255cdc3 -->
---
name: conference-developer-endpoints
description: 用于在 AI Engineer 大会页面中添加或审查面向开发者和 AI 的大会数据端点，例如 llms.txt、sessions.json、speakers.json 和 MCP 路由。
---

# 大会开发者与 AI 端点——通用模式

本技能记录了为任意 AI Engineer 大会公开面向开发者和 AI 的数据端点的标准模式。本仓库中的每场大会（例如 `/europe`、`/worldsfair`、`/miami`）都应遵循此模式，以提供一致且机器可读的大会数据访问方式。

## 每场大会需要构建的内容

对于路由为 `/{conf}` 的大会，创建以下内容：

### 1. 公共数据工具

创建 `src/data/{conf}-public-data.ts`，它应：
- 导入大会的源数据（通常是 `src/pages/{conf}/source/schedule.json`，以及 `src/data/{conf}-speakers.ts` 中的演讲者提取逻辑）
- 导出以下函数：`getPublicTalks()`、`getPublicSpeakers()`、`getScheduleByDay()`，以及一个 `CONFERENCE_META` 对象
- 在返回数据前，**移除所有敏感字段**：
  - `email` / `contact.email` — 演讲者电子邮箱地址
  - `notes` — 组织者内部备注
  - `acceleventsSpeakerId` — 内部平台 ID
  - `sessionId`、`invited` — 内部议程元数据
  - `cfpData` — 论文征集提交详情和评审状态
- 返回仅包含可安全公开字段的整洁类型（`PublicSpeaker`、`PublicTalk`）

### 2. API 路由

在 `src/pages/api/{conf}/` 中创建以下 API 路由：

| 文件 | 端点 | 格式 | 描述 |
|---|---|---|---|
| `llms-txt.ts` | `/{conf}/llms.txt` | 纯文本 | 大会基本信息和日程概览。包含指向其他端点的链接。 |
| `llms-full-txt.ts` | `/{conf}/llms-full.txt` | 纯文本 | 完整详情：每场演讲的描述、演讲者简介和社交链接。 |
| `sessions.ts` | `/{conf}/sessions.json` | JSON | 包含元数据的所有议程（演讲和研讨会）。启用 CORS。 |
| `speakers.ts` | `/{conf}/speakers.json` | JSON | 包含职位、公司和社交账号的所有演讲者。启用 CORS。 |
| `mcp.ts` | `/{conf}/mcp` | JSON-RPC 2.0 | 提供大会数据查询工具的 MCP 服务器。 |

所有端点都应：
- 设置适当的 `Cache-Control` 响应头（`s-maxage=3600, stale-while-revalidate=86400`）
- JSON 端点必须包含 CORS 响应头（`Access-Control-Allow-Origin: *`），并处理 `OPTIONS` 预检请求
- 绝不公开敏感或内部字段

### 3. URL 重写

在 `next.config.ts` 现有的 rewrites 部分下添加重写规则：

```ts
// {Conf} developer/AI endpoints
{
  source: '/{conf}/llms.txt',
  destination: '/api/{conf}/llms-txt',
},
{
  source: '/{conf}/llms-full.txt',
  destination: '/api/{conf}/llms-full-txt',
},
{
  source: '/{conf}/sessions.json',
  destination: '/api/{conf}/sessions',
},
{
  source: '/{conf}/speakers.json',
  destination: '/api/{conf}/speakers',
},
{
  source: '/{conf}/mcp',
  destination: '/api/{conf}/mcp',
},
```

### 4. MCP 服务器实现

MCP 端点应使用以下工具实现 JSON-RPC 2.0：

- `get_conference_info` — 返回大会元数据（日期、地点、会场、链接）
- `list_speakers` — 返回演讲者，并支持可选的 `search` 筛选条件
- `list_talks` — 返回演讲，并支持可选的 `day`、`type`、`track`、`search` 筛选条件
- `get_schedule` — 返回按日期组织的日程，并支持可选的 `day` 筛选条件

该端点应：
- 同时处理 GET（返回服务器信息）和 POST（JSON-RPC 请求）
- 支持批量请求
- 返回正确的 JSON-RPC 2.0 错误响应
- 遵循 Streamable HTTP 传输规范（2025-03-26）

### 5. 开发者文档页面

创建 `src/pages/{conf}/developers.tsx`，包含：
- 与大会网站设计相匹配的深色终端主题
- 以下章节：端点、快速开始（curl/JS/Python）、CLI 工具、MCP 服务器、Agent Skills、数据隐私
- 链接到各个端点的交互式端点卡片
- 带复制功能的代码块
- 适用于 Claude Desktop / Cursor / Windsurf 的 MCP 配置片段
- 标题和强调高亮使用 AIE 品牌金色（#FFE9A7）

### 6. Agent Skill

创建 `.agents/skills/{conf}-developer-api/SKILL.md`，包含：
- 带有 URL 和描述的端点清单
- 快速开始 curl 示例
- MCP 集成说明和配置
- 数据模型模式（演讲和演讲者的 JSON 结构）
- 被移除的敏感字段列表
- 仓库中的关键文件路径

### 7. CLI 工具

`cli/aie/` 中的通用 CLI（以 `aieng` 名称发布到 npm）支持所有大会。添加新大会时，在 `cli/aie/cli.mjs` 的 `CONFERENCES` 注册表数组中添加一个条目，包含：
- `slug` — 大会的路由短名（例如 `europe`）
- `aliases` — 简短别名（例如 `['eu', 'eur', 'london']`）
- `name`、`route`、`dates`、`location`、`status`
- `hasEndpoints` — 端点上线后设为 `true`

用法：`npx aieng {conf} [command]`（例如 `npx aieng eu speakers`）

## 参考实现

欧洲大会（`/europe`）是参考实现。使用以下文件作为模板：

- 数据工具：`src/data/europe-public-data.ts`
- API 路由：`src/pages/api/europe/`（llms-txt.ts、llms-full-txt.ts、sessions.ts、speakers.ts、mcp.ts）
- URL 重写：`next.config.ts`（搜索 "Europe developer/AI endpoints"）
- 内联章节：`src/components/europe-2026/DeveloperEndpointsSection.jsx`
- Agent Skill：`.agents/skills/europe-developer-api/SKILL.md`
- CLI 工具：`cli/aie/`（通用多大会工具，以 `aieng` 名称发布）

## 针对不同大会的适配

每场大会都有自己的数据源格式。需要考虑的主要差异：

- **欧洲**：源数据位于 `src/pages/europe/source/schedule.json`，演讲者通过 `src/data/europe-speakers.ts` 派生
- **World's Fair**：历史数据位于 `src/utils/speakers-sessions-details.json`（包含数百名 2025 年演讲者），新的 2026 年数据待定
- **迈阿密**：演讲者数据硬编码在 `src/components/aie-miami-2026/SpeakersSection.tsx` 和 `speakers.js` 中
- **新加坡**：数据位于 `src/components/aie-singapore-2026/`

进行适配时，在构建公共数据工具之前，务必检查该大会现有的数据源和提取模式。

## 验证检查清单

为新大会实现端点后：

1. 运行 `SKIP_ENV_VALIDATION=1 npx tsc --noEmit` — 必须以零错误通过
2. 启动开发服务器：`SKIP_ENV_VALIDATION=1 pnpm dev`
3. 验证每个端点都能返回数据：`curl http://localhost:3000/{conf}/llms.txt`
4. 验证 JSON 端点不包含电子邮箱、备注或内部 ID
5. 使用 `tools/list` JSON-RPC 调用测试 MCP 端点
6. 使用 `tools/call` JSON-RPC 调用测试 MCP 端点（例如使用搜索条件调用 `list_speakers`）
7. 验证开发者页面在浏览器中正确渲染
8. 运行构建：`SKIP_ENV_VALIDATION=1 pnpm build`

## 注意事项

- `pnpm lint` 无法在 Next.js 16 上运行；请使用 `npx tsc --noEmit` 进行类型检查
- 所有端点都使用 `s-maxage=3600, stale-while-revalidate=86400` 缓存
- MCP 实现是手写的 JSON-RPC 2.0（未使用官方 MCP SDK）
- 生产环境 URL 的基础域名是 `https://ai.engineer`
