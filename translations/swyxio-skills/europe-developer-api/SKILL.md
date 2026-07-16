<!-- source-sha256: 096b45d6bddbc104acf63acd6904a78bbe86a9da8f8514a15fb4e7cf925d2d13 -->
---
name: europe-developer-api
description: 在使用 AI Engineer Europe 2026 面向开发者的端点、公开日程 JSON、演讲者 JSON、llms.txt 文件、MCP 访问以及本地 aieng CLI 时使用。
---

# Europe 开发者与 AI 端点

AI Engineer Europe 2026 提供多个对开发者友好的端点，用于基于会议数据构建应用、AI 集成和工具。

## 可用端点

所有端点均相对于 `https://ai.engineer`：

| 端点 | 说明 |
|---|---|
| `/europe/llms.txt` | 基本会议信息 + 日程概览（纯文本） |
| `/europe/llms-full.txt` | 完整详情：所有演讲、说明和演讲者（纯文本） |
| `/europe/sessions.json` | JSON 格式的所有场次（演讲 + 工作坊，不含敏感数据） |
| `/europe/speakers.json` | JSON 格式的所有演讲者（不含敏感数据） |
| `/europe/mcp` | MCP（模型上下文协议）服务器端点 |

## 快速开始

### 使用 curl 获取数据

```bash
# 基本信息
curl https://ai.engineer/europe/llms.txt

# 完整详情
curl https://ai.engineer/europe/llms-full.txt

# JSON 端点
curl https://ai.engineer/europe/sessions.json | jq .
curl https://ai.engineer/europe/speakers.json | jq .
```

### 使用 npx CLI

```bash
# 显示会议信息
npx aieng europe

# 列出所有演讲者
npx aieng eu speakers

# 列出所有演讲
npx aieng eu talks

# 搜索演讲者
npx aieng eu speakers --search "Matt"

# 按日期筛选演讲
npx aieng eu talks --day "April 9"

# 列出所有会议
npx aieng --list
```

### MCP 集成

位于 `/europe/mcp` 的 MCP 服务器实现了模型上下文协议（JSON-RPC 2.0）。你可以将其与任何兼容 MCP 的客户端配合使用。

**可用工具：**
- `get_conference_info` — 基本会议元数据
- `list_speakers` — 所有演讲者（可选搜索筛选条件）
- `list_talks` — 所有演讲（可选日期、类型、专题和搜索筛选条件）
- `get_schedule` — 按日期组织的完整日程

**MCP 请求示例：**
```bash
curl -X POST https://ai.engineer/europe/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_speakers","arguments":{"search":"Anthropic"}}}'
```

**MCP 客户端配置（例如用于 Claude Desktop）：**
```json
{
  "mcpServers": {
    "aie-europe": {
      "url": "https://ai.engineer/europe/mcp"
    }
  }
}
```

## 数据模型

### Sessions JSON 结构
```json
{
  "conference": "AI Engineer Europe 2026",
  "dates": "April 8-10, 2026",
  "location": "London, UK",
  "totalSessions": 100,
  "sessions": [
    {
      "title": "Session Title",
      "description": "Session description...",
      "day": "April 9",
      "time": "9:00-9:30am",
      "room": "Keynote",
      "type": "keynote",
      "track": "AI Agents",
      "speakers": ["Speaker Name"]
    }
  ]
}
```

### Speakers JSON 结构
```json
{
  "conference": "AI Engineer Europe 2026",
  "totalSpeakers": 100,
  "speakers": [
    {
      "name": "Speaker Name",
      "role": "Role",
      "company": "Company",
      "twitter": "https://x.com/handle",
      "linkedin": "https://linkedin.com/in/...",
      "github": "https://github.com/...",
      "photoUrl": "https://ai.engineer/europe-speakers/photo.jpg",
      "sessions": [...]
    }
  ]
}
```

## 关键路径（在此仓库中）

- 数据实用工具：`src/data/europe-public-data.ts`
- API 路由：`src/pages/api/europe/`
- 日程源数据：`src/pages/europe/source/schedule.json`
- URL 重写：`next.config.ts`（搜索 "Europe developer/AI endpoints"）
- 内联章节：`src/components/europe-2026/DeveloperEndpointsSection.jsx`
- npx CLI：`cli/aie/`（通用多会议 CLI，以 `aieng` 名称发布）

## 敏感字段（已从公开端点中移除）

以下来自 `schedule.json` 的字段不会公开：
- `contact.email` — 演讲者电子邮件地址
- `notes` — 组织者内部备注
- `acceleventsSpeakerId` — Accelevents 内部 ID
- `sessionId` — 内部场次 ID
- `invited` — 演讲者是受邀参加还是通过 CFP 入选
- `cfpData.status`、`cfpData.dateSubmitted`、`cfpData.combinedAcceptances` — 内部评审数据

## 注意事项

- 所有端点均返回 CORS 标头（`Access-Control-Allow-Origin: *`）
- JSON 端点支持 `OPTIONS` 预检请求
- 数据会被缓存（`s-maxage=3600, stale-while-revalidate=86400`）
- `pnpm lint` 无法在 Next.js 16 上运行；请使用 `npx tsc --noEmit` 进行类型检查
