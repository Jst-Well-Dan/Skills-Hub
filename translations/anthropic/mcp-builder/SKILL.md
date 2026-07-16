<!-- source-sha256: 0f4592dcb53cf2b5d6b7febee6b4152018b565551a1c29e3c612f57b218ab295 -->
---
name: mcp-builder
description: 创建高质量 MCP（模型上下文协议）服务器的指南，使 LLM 能够通过精心设计的工具与外部服务交互。适用于构建 MCP 服务器以集成外部 API 或服务，无论使用 Python（FastMCP）还是 Node/TypeScript（MCP SDK）。
license: 完整条款见 LICENSE.txt
---

# MCP 服务器开发指南

## 概述

创建 MCP（模型上下文协议）服务器，使 LLM 能够通过精心设计的工具与外部服务交互。MCP 服务器的质量取决于它帮助 LLM 完成现实世界任务的能力。

---

# 流程

## 🚀 高层工作流

创建高质量的 MCP 服务器包括四个主要阶段：

### 阶段 1：深入研究与规划

#### 1.1 理解现代 MCP 设计

**API 覆盖范围与工作流工具：**
在全面覆盖 API 端点和专用工作流工具之间取得平衡。工作流工具对于特定任务可能更加方便，而全面覆盖则赋予智能体组合操作的灵活性。性能因客户端而异——一些客户端受益于能够组合基础工具的代码执行能力，而另一些客户端更适合使用更高层级的工作流。如果不确定，应优先考虑全面覆盖 API。

**工具命名与可发现性：**
清晰且具有描述性的工具名称有助于智能体快速找到正确的工具。使用一致的前缀（例如 `github_create_issue`、`github_list_repos`）和面向操作的命名方式。

**上下文管理：**
简洁的工具描述以及筛选结果和对结果进行分页的能力有助于智能体工作。设计能够返回聚焦且相关数据的工具。一些客户端支持代码执行，可帮助智能体高效地筛选和处理数据。

**可操作的错误消息：**
错误消息应通过具体建议和后续步骤，引导智能体找到解决方案。

#### 1.2 研读 MCP 协议文档

**浏览 MCP 规范：**

从站点地图开始查找相关页面：`https://modelcontextprotocol.io/sitemap.xml`

然后获取带有 `.md` 后缀的特定页面以使用 Markdown 格式（例如 `https://modelcontextprotocol.io/specification/draft.md`）。

需要查阅的关键页面：
- 规范概述与架构
- 传输机制（可流式传输的 HTTP、stdio）
- 工具、资源和提示定义

#### 1.3 研读框架文档

**推荐技术栈：**
- **语言**：TypeScript（SDK 支持质量高，并且在许多执行环境中具有良好的兼容性，例如 MCPB。此外，AI 模型擅长生成 TypeScript 代码，这得益于其广泛应用、静态类型和优秀的代码检查工具）
- **传输方式**：远程服务器使用可流式传输的 HTTP，并采用无状态 JSON（与有状态会话和流式响应相比，更易于扩展和维护）。本地服务器使用 stdio。

**加载框架文档：**

- **MCP 最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) - 核心指南

**对于 TypeScript（推荐）：**
- **TypeScript SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 指南](./reference/node_mcp_server.md) - TypeScript 模式与示例

**对于 Python：**
- **Python SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 指南](./reference/python_mcp_server.md) - Python 模式与示例

#### 1.4 规划实现方案

**理解 API：**
查阅服务的 API 文档，识别关键端点、身份验证要求和数据模型。根据需要使用网页搜索和 WebFetch。

**工具选择：**
优先考虑全面覆盖 API。列出要实现的端点，从最常用的操作开始。

---

### 阶段 2：实现

#### 2.1 设置项目结构

有关项目设置，请参阅特定语言的指南：
- [⚡ TypeScript 指南](./reference/node_mcp_server.md) - 项目结构、package.json、tsconfig.json
- [🐍 Python 指南](./reference/python_mcp_server.md) - 模块组织、依赖项

#### 2.2 实现核心基础设施

创建共享实用工具：
- 具有身份验证功能的 API 客户端
- 错误处理辅助函数
- 响应格式化（JSON/Markdown）
- 分页支持

#### 2.3 实现工具

对于每个工具：

**输入模式：**
- 使用 Zod（TypeScript）或 Pydantic（Python）
- 包含约束和清晰的描述
- 在字段描述中添加示例

**输出模式：**
- 尽可能定义 `outputSchema` 以提供结构化数据
- 在工具响应中使用 `structuredContent`（TypeScript SDK 功能）
- 帮助客户端理解和处理工具输出

**工具描述：**
- 简明概述功能
- 参数描述
- 返回类型模式

**实现：**
- 对 I/O 操作使用 Async/await
- 通过可操作的消息进行恰当的错误处理
- 在适用时支持分页
- 使用现代 SDK 时，同时返回文本内容和结构化数据

**注解：**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### 阶段 3：审查与测试

#### 3.1 代码质量

审查以下内容：
- 无重复代码（DRY 原则）
- 一致的错误处理
- 完整的类型覆盖
- 清晰的工具描述

#### 3.2 构建与测试

**TypeScript：**
- 运行 `npm run build` 验证编译
- 使用 MCP Inspector 测试：`npx @modelcontextprotocol/inspector`

**Python：**
- 验证语法：`python -m py_compile your_server.py`
- 使用 MCP Inspector 测试

有关详细的测试方法和质量检查清单，请参阅特定语言的指南。

---

### 阶段 4：创建评估

实现 MCP 服务器后，创建全面的评估来测试其有效性。

**加载[✅ 评估指南](./reference/evaluation.md)以获取完整的评估说明。**

#### 4.1 理解评估目的

使用评估来测试 LLM 能否有效地使用你的 MCP 服务器回答现实且复杂的问题。

#### 4.2 创建 10 个评估问题

要创建有效的评估，请遵循评估指南中概述的流程：

1. **工具检查**：列出可用工具并理解其功能
2. **内容探索**：使用只读操作探索可用数据
3. **问题生成**：创建 10 个复杂且现实的问题
4. **答案验证**：亲自解答每个问题以验证答案

#### 4.3 评估要求

确保每个问题都满足：
- **独立性**：不依赖其他问题
- **只读**：只需执行非破坏性操作
- **复杂性**：需要多次调用工具并进行深入探索
- **现实性**：基于真实且人们关心的使用场景
- **可验证性**：具有唯一且明确的答案，可通过字符串比较进行验证
- **稳定性**：答案不会随时间变化

#### 4.4 输出格式

创建一个具有以下结构的 XML 文件：

```xml
<evaluation>
  <qa_pair>
    <question>查找有关以动物为代号的 AI 模型发布的讨论。其中一个模型需要确定一种使用 ASL-X 格式的特定安全等级。对于以一种带斑点的野生猫科动物命名的模型，当时正在确定的数字 X 是多少？</question>
    <answer>3</answer>
  </qa_pair>
<!-- 更多 qa_pair... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

在开发过程中根据需要加载以下资源：

### MCP 核心文档（首先加载）
- **MCP 协议**：从 `https://modelcontextprotocol.io/sitemap.xml` 的站点地图开始，然后获取带有 `.md` 后缀的特定页面
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) - 通用 MCP 指南，包括：
  - 服务器和工具命名约定
  - 响应格式指南（JSON 与 Markdown）
  - 分页最佳实践
  - 传输方式选择（可流式传输的 HTTP 与 stdio）
  - 安全和错误处理标准

### SDK 文档（在阶段 1/2 加载）
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取
- **TypeScript SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取

### 特定语言的实现指南（在阶段 2 加载）
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南，包括：
  - 服务器初始化模式
  - Pydantic 模型示例
  - 使用 `@mcp.tool` 注册工具
  - 完整的可运行示例
  - 质量检查清单

- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) - 完整的 TypeScript 指南，包括：
  - 项目结构
  - Zod 模式范例
  - 使用 `server.registerTool` 注册工具
  - 完整的可运行示例
  - 质量检查清单

### 评估指南（在阶段 4 加载）
- [✅ 评估指南](./reference/evaluation.md) - 完整的评估创建指南，包括：
  - 问题创建指南
  - 答案验证策略
  - XML 格式规范
  - 问题和答案示例
  - 使用所提供的脚本运行评估
