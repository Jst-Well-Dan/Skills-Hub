<!-- source-sha256: c19e7c4778b55914609826061cd986647327ab68a7b720ecd273b8eb9571e255 -->
---
name: edgeone-pages-deploy
description: >-
  此技能用于将前端和全栈项目部署到 EdgeOne Pages（腾讯 EdgeOne）。
  当用户的主要意图是部署、发布、上线、托管、启动或发布新版本时，应使用此技能——例如
  “部署我的应用”“发布此网站”“将其上线”“创建预览部署”“部署到 EdgeOne”
  “发布到生产环境”“上线”“发布”“发一版”“重新部署”。
  当部署仅作为次要步骤被提及时，请勿触发
  （例如“编写一个 API 并部署它”——主要意图是编写代码，应使用 edgeone-pages-dev）。
  对于部署后的运行时错误，请勿触发（例如 CORS 问题、部署后出现 500 错误——
  应使用 edgeone-pages-dev 进行故障排查）。
metadata:
  author: edgeone
  version: "2.0.0"
---

# EdgeOne Pages 部署技能

将任何项目部署到 **EdgeOne Pages**。

## ⛔ 关键规则（绝不可跳过）

1. **CLI 版本 ≥ `1.2.30`**——如果版本较低，请重新安装。绝不可使用过时版本继续操作。
2. **绝不可截断部署 URL**——`EDGEONE_DEPLOY_URL` 包含访问所需的查询参数。始终输出**完整的** URL。
3. **登录前询问用户选择中国站还是全球站**。绝不可擅自假定。
4. **自动检测登录方式**——桌面环境使用浏览器登录，无头/远程/CI 环境使用令牌登录。遵循下方决策表。
5. **通过令牌登录后，询问用户是否希望将令牌保存在本地**，以供后续使用。

---

## 部署流程

首先运行以下检查，然后遵循决策表：

```bash
# 检查 1：CLI 是否已安装且版本正确？
edgeone -v

# 检查 2：是否已经登录？
edgeone whoami

# 检查 3：项目是否已经关联？
cat edgeone.json 2>/dev/null

# 检查 4：是否存在已保存的令牌？
cat .edgeone/.token 2>/dev/null
```

### 决策表

| CLI 版本 | 登录状态 | 操作 |
|-------------|-------------|--------|
| 未安装或 < 1.2.30 | — | → 前往**安装 CLI** |
| `≥ 1.2.30` ✓ | 已登录 | → 前往**部署** |
| `≥ 1.2.30` ✓ | 未登录，但有已保存的令牌 | → 前往**使用令牌部署**（使用已保存的令牌） |
| `≥ 1.2.30` ✓ | 未登录，且无已保存的令牌 | → 前往**登录** |

---

## 安装 CLI

```bash
npm install -g edgeone@latest
```

验证：`edgeone -v`——确认输出为 `1.2.30` 或更高版本。如果不是，请重试安装。

---

## 登录

### 1. 询问用户选择站点

在运行任何登录命令之前，使用 IDE 的选择控件（`ask_followup_question`）：

> 请选择你的 EdgeOne Pages 站点：
> - **中国站**——适用于中国大陆用户（console.cloud.tencent.com）
> - **全球站**——适用于中国大陆以外的用户（console.intl.cloud.tencent.com）

### 2. 检测环境并选择登录方式

| 条件 | 方式 |
|-----------|--------|
| 本地桌面 IDE（VS Code、Cursor 等） | **浏览器登录** |
| 远程 / SSH / 容器 / CI / 云端 IDE / 无头环境 | **令牌登录** |
| 用户明确要求使用令牌 | **令牌登录** |

#### 浏览器登录

```bash
# 中国站
edgeone login --site china

# 全球站
edgeone login --site global
```

等待用户完成浏览器身份验证。完成后，CLI 会输出成功消息。

#### 令牌登录

令牌登录**不**使用 `edgeone login`。请通过 `-t` 在部署命令中直接传入令牌。

指导用户获取令牌：
1. 前往控制台：
   - **中国站**：https://console.cloud.tencent.com/edgeone/pages?tab=settings
   - **全球站**：https://console.intl.cloud.tencent.com/edgeone/pages?tab=settings
2. 找到 **API Token** → **Create Token** → 复制令牌

⚠️ 提醒用户：该令牌拥有账户级权限。绝不可将其提交到代码仓库。

### 3. 询问是否将令牌保存在本地

用户提供令牌后，询问：

> 是否将此令牌保存在本地，以供后续部署使用？
> - **是**——保存到 `.edgeone/.token`（下次自动使用）
> - **否**——仅用于本次部署

**如果选择“是”：**

```bash
mkdir -p .edgeone
echo "<token>" > .edgeone/.token
grep -q '.edgeone/.token' .gitignore 2>/dev/null || echo '.edgeone/.token' >> .gitignore
```

向用户确认：“✅ 令牌已保存到 `.edgeone/.token`，并已添加到 `.gitignore`。”

---

## 部署

### 使用浏览器身份验证进行部署

```bash
# 项目已经关联（edgeone.json 存在）
edgeone pages deploy

# 新项目（无 edgeone.json）
edgeone pages deploy -n <project-name>
```

`<project-name>`：根据项目目录名称自动生成。首次部署会自动创建 `edgeone.json`。

### 使用令牌部署

首先检查是否存在已保存的令牌：

```bash
cat .edgeone/.token 2>/dev/null
```

- 找到已保存的令牌 → 使用该令牌，并告知用户：“正在使用 `.edgeone/.token` 中保存的令牌”
- 未找到已保存的令牌 → 请求用户提供令牌（参见上方的“令牌登录”）

```bash
# 项目已经关联
edgeone pages deploy -t <token>

# 新项目
edgeone pages deploy -n <project-name> -t <token>
```

令牌已包含站点信息——无需使用 `--site` 标志。

使用手动输入的令牌成功部署后，询问用户是否希望保存该令牌（参见上方的“询问是否将令牌保存在本地”）。

### 部署到预览环境

```bash
edgeone pages deploy -e preview
```

### 构建行为

CLI 会自动检测框架、运行构建并上传输出目录。无需手动配置。

---

## ⚠️ 解析部署输出（关键）

`edgeone pages deploy` 成功后，CLI 会输出：

```
[cli][✔] Deploy Success
EDGEONE_DEPLOY_URL=https://my-project-abc123.edgeone.cool?<auth_query_params>
EDGEONE_DEPLOY_TYPE=preset
EDGEONE_PROJECT_ID=pages-xxxxxxxx
[cli][✔] You can view your deployment in the EdgeOne Pages Console at:
https://console.cloud.tencent.com/edgeone/pages/project/pages-xxxxxxxx/deployment/xxxxxxx
```

**提取规则：**

| 字段 | 提取方式 | ⛔ 警告 |
|-------|---------------|-----------|
| **访问 URL** | `EDGEONE_DEPLOY_URL=` 后的完整值 | **包含完整的查询字符串**（`?` 及其后的所有内容）——缺少这些参数，页面将无法加载 |
| **项目 ID** | `EDGEONE_PROJECT_ID=` 后的值 | — |
| **控制台 URL** | “You can view your deployment...” 后的一行 | — |

**向用户显示：**

> ✅ 部署完成！
> - **访问 URL**：`https://my-project-abc123.edgeone.cool?<auth_query_params>`
> - **控制台 URL**：`https://console.cloud.tencent.com/edgeone/pages/project/...`

---

## 错误处理

| 错误 | 解决方案 |
|-------|----------|
| `command not found: edgeone` | 运行 `npm install -g edgeone@latest` |
| 登录时浏览器未打开 | 切换到令牌登录 |
| “not logged in”错误 | 运行 `edgeone whoami` 进行检查，然后重新登录或使用令牌 |
| 使用令牌时出现身份验证错误 | 令牌可能已过期——请在控制台重新生成 |
| 项目名称冲突 | 使用 `-n` 指定其他名称 |
| 构建失败 | 检查日志——通常是缺少依赖项或构建脚本有误 |

---

有关 CLI 命令参考、环境变量、本地开发设置和令牌管理的详细信息，请参阅 [references/command-reference.md](references/command-reference.md)。
