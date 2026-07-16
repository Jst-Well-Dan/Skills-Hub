<!-- source-sha256: 7cf6302902893e723c106a261191347b8c32a95891fc81b1f558f085287c0f38 -->
---
name: edgeone-pages-dev
description: >-
  此技能用于指导在 EdgeOne Pages 上开发全栈功能，包括边缘函数、
  云函数（Node.js / Go / Python 运行时）、中间件、KV 存储和本地开发工作流。
  当用户希望专门在 EdgeOne Pages 上创建 API、无服务器函数、中间件、
  WebSocket 端点或全栈功能时，应使用此技能，例如：
  “创建 API”“添加无服务器函数”“编写中间件”“构建全栈应用”、
  “添加 WebSocket 支持”“设置边缘函数”“使用 KV 存储”、
  “创建 Go API”“构建 Python 后端”“在 EdgeOne Pages 上使用 Flask/FastAPI/Gin”。
  不要针对框架原生功能（Next.js API 路由、Next.js 中间件、
  Nuxt 服务端路由）或 EdgeOne Pages 项目之外的通用 Express/Koa 开发触发此技能。
  不要针对部署触发此技能——请改用 edgeone-pages-deploy。
  不要针对其他平台（Cloudflare Workers、Vercel Functions、AWS Lambda）触发此技能。
metadata:
  author: edgeone
  version: "4.0.0"
---

# EdgeOne Pages 开发指南

在 **EdgeOne Pages** 上开发全栈应用——包括边缘函数、云函数（Node.js / Go / Python）和中间件。

## 何时使用此技能

- 在 EdgeOne Pages 上创建 API、无服务器函数或后端逻辑
- 添加用于请求拦截、重定向、身份验证守卫或 A/B 测试的中间件
- 构建由静态前端和服务端函数组成的全栈应用
- 使用 KV 存储持久化边缘侧数据
- 设置 WebSocket 端点（Node.js 运行时）
- 在 EdgeOne Pages 上集成 Express、Koa、Gin、Echo、Flask、FastAPI 或 Django
- 调试 EdgeOne Pages 运行时错误（函数故障、中间件问题、KV 问题）

**不要用于：**
- 部署 → 使用 `edgeone-pages-deploy` 技能
- Next.js / Nuxt 中间件或 API 路由 → 使用框架自身的 API，而不是平台的 `middleware.js`
- EdgeOne Pages 项目之外的通用 Express/Koa/Gin/Flask 开发
- Cloudflare Workers、Vercel Functions 或其他平台

## 如何使用此技能（适用于编码智能体）

1. 阅读下方的**决策树**，选择正确的运行时
2. 按照**路由**表加载相关参考文件
3. 使用该参考文件中的代码模式实现用户的需求

## ⛔ 关键规则（绝不可跳过）

1. **为任务选择正确的运行时。** 遵循决策树——绝不要猜测。
2. **边缘函数运行在 V8 上，而不是 Node.js。** 绝不要在边缘函数中使用 Node.js 内置模块（`fs`、`path`、Node 的 `crypto`）或 npm 包。
3. **云函数支持三种运行时：Node.js、Go 和 Python。** 将所有函数文件放在 `cloud-functions/` 目录下。平台会根据文件扩展名识别语言（`.js`/`.ts` → Node.js、`.go` → Go、`.py` → Python）。
4. **Node.js 函数返回标准 Web `Response` 对象**，而不是 `res.send()`——除非通过 `[[default]].js` 模式使用 Express/Koa。
5. **Go Handler 模式**要求使用 `http.HandlerFunc` 签名；**框架模式**使用标准框架代码，并自动适配端口和路径。
6. **Python 入口文件**通过类或应用模式识别（`class handler(BaseHTTPRequestHandler)`、`app = Flask(...)`、`app = FastAPI(...)`）。其他 `.py` 文件会被视为辅助模块。
7. **中间件仅用于轻量级请求拦截。** 绝不要在中间件中执行繁重计算或数据库调用。
8. **本地开发始终使用 `edgeone pages dev`。** 绝不要为函数单独运行开发服务器——CLI 会在 8088 端口处理所有内容。
9. **绝不要在 `edgeone.json` 中将 `edgeone pages dev` 配置为 `devCommand`，也不要在 `package.json` 中将其配置为 `dev` 脚本**——这会导致无限递归。
10. **对于框架项目（Next.js、Nuxt 等），使用框架自身的中间件**——而不是平台的 `middleware.js`。

---

## 技术决策树

```
请求拦截 / 重定向 / 重写 / 身份验证守卫 / A/B 测试？
  → 中间件                                            → 阅读 references/middleware.md

需要超低延迟的轻量级 API（简单逻辑，不使用 npm）？
  → 边缘函数                                          → 阅读 references/edge-functions.md

需要 KV 持久化存储？（⚠️ 请先在控制台启用 KV）
  → 边缘函数 + KV 存储                                → 阅读 references/kv-storage.md

需要使用 npm 包 / 数据库 / WebSocket 的复杂后端？
  → 云函数（Node.js）                                 → 阅读 references/node-functions.md

使用 Express 或 Koa 框架？
  → 使用 [[default]].js 的云函数（Node.js）           → 阅读 references/node-functions.md

需要使用 Go 构建高性能 API（Gin / Echo / Chi / Fiber）？
  → 云函数（Go）                                      → 阅读 references/go-functions.md

需要使用 Flask / FastAPI / Django / Sanic 构建 Python API？
  → 云函数（Python）                                  → 阅读 references/python-functions.md

不含服务端逻辑的纯静态网站？
  → 无需函数——直接部署静态文件

需要项目结构模板？
  → 阅读 references/recipes.md
```

### 运行时对比

| 功能 | 边缘函数 | 云函数（Node.js） | 云函数（Go） | 云函数（Python） | 中间件 |
|---------|--------------|--------------------------|---------------------|------------------------|------------|
| **运行时** | V8（类似 CF Workers） | Node.js v20.x | Go 1.26+ | Python 3.10 | V8（边缘） |
| **npm/软件包** | ❌ 不支持 | ✅ 完整的 npm 生态系统 | ✅ Go 模块 | ✅ pip（自动检测） | ❌ 不支持 |
| **最大代码大小** | 5 MB | 128 MB | 128 MB | 128 MB（含依赖项） | 边缘函数包的一部分 |
| **最大请求体** | 1 MB | 6 MB | 6 MB | 6 MB | N/A（透传） |
| **最大 CPU / 墙上时钟时间** | 200 ms CPU | 120 s 墙上时钟时间 | 120 s 墙上时钟时间 | 120 s 墙上时钟时间 | 仅限轻量级处理 |
| **KV 存储** | ✅ 支持（全局变量） | ❌ 不支持 | ❌ 不支持 | ❌ 不支持 | ❌ 不支持 |
| **WebSocket** | ❌ 不支持 | ✅ 支持 | ❌ 不支持 | ❌ 不支持 | ❌ 不支持 |
| **框架支持** | — | Express、Koa | Gin、Echo、Chi、Fiber | Flask、FastAPI、Django、Sanic | — |
| **使用场景** | 轻量级 API、边缘计算 | 复杂 API、全栈应用 | 高性能 API、编译型语言速度 | 数据科学、机器学习、快速原型开发 | 请求预处理 |

### 云函数——语言对比

| 功能 | Node.js | Go | Python |
|---------|---------|-----|--------|
| **文件扩展名** | `.js` / `.ts` | `.go` | `.py` |
| **处理器样式** | `export function onRequest(ctx)` → `Response` | `func Handler(w, r)`（Handler）或 `func main()`（框架） | `class handler(BaseHTTPRequestHandler)` 或框架应用实例 |
| **框架模式** | 通过 `[[default]].js` 使用 Express/Koa | 通过入口 `.go` 文件使用 Gin/Echo/Chi/Fiber | 通过入口 `.py` 文件使用 Flask/FastAPI/Django |
| **依赖项管理** | `package.json`（npm） | `go.mod`（自动） | `requirements.txt` + 自动检测 |
| **开发模式** | Handler / 框架 | Handler / 框架 | Handler / WSGI / ASGI |

---

## 路由

| 任务 | 阅读 |
|------|------|
| 边缘函数（轻量级 API、V8 运行时、KV 存储） | [references/edge-functions.md](references/edge-functions.md) |
| KV 存储（边缘侧持久化键值存储） | [references/kv-storage.md](references/kv-storage.md) |
| 云函数——Node.js（npm、数据库、Express/Koa、WebSocket） | [references/node-functions.md](references/node-functions.md) |
| 云函数——Go（Gin、Echo、Chi、Fiber、net/http） | [references/go-functions.md](references/go-functions.md) |
| 云函数——Python（Flask、FastAPI、Django、Sanic、Handler） | [references/python-functions.md](references/python-functions.md) |
| 中间件（重定向、重写、身份验证守卫、A/B 测试） | [references/middleware.md](references/middleware.md) |
| 项目结构模板和常用方案 | [references/recipes.md](references/recipes.md) |
| 调试和故障排除 | [references/troubleshooting.md](references/troubleshooting.md) |

---

## 项目设置（快速开始）

初始化项目：

```bash
edgeone pages init
```

启动本地开发：

```bash
edgeone pages dev            # 在 http://localhost:8088/ 上提供所有内容
```

关联项目（KV 和环境变量需要此操作）：

```bash
edgeone pages link
```

管理环境变量：

```bash
edgeone pages env pull       # 从控制台拉取到本地 .env
```

在函数中通过 `context.env.KEY`（Node.js）、`os.Getenv("KEY")`（Go）或 `os.environ.get("KEY")`（Python）访问环境变量。

有关详细的项目结构和方案，请参阅 [references/recipes.md](references/recipes.md)。
