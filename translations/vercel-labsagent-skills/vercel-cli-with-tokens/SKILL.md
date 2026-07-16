<!-- source-sha256: c06bea99e75eab07fde4fae26069baa002f82f39b53f07981704c2901551dd4c -->
---
name: vercel-cli-with-tokens
description: 使用基于令牌的身份验证在 Vercel 上部署和管理项目。当使用访问令牌而非交互式登录来操作 Vercel CLI 时使用——例如“部署到 vercel”“设置 vercel”“向 vercel 添加环境变量”。
metadata:
  author: vercel
  version: "1.0.0"
---

# 使用令牌的 Vercel CLI

使用 CLI 和基于令牌的身份验证在 Vercel 上部署和管理项目，无需依赖 `vercel login`。

## 步骤 1：查找 Vercel 令牌

在运行任何 Vercel CLI 命令之前，先确定令牌的来源。按顺序检查以下情况：

### A) 环境中已设置 `VERCEL_TOKEN`

```bash
printenv VERCEL_TOKEN
```

如果此命令返回了值，则已准备就绪。跳至步骤 2。

### B) 令牌位于 `.env` 文件的 `VERCEL_TOKEN` 中

```bash
grep '^VERCEL_TOKEN=' .env 2>/dev/null
```

如果找到，请将其导出：

```bash
export VERCEL_TOKEN=$(grep '^VERCEL_TOKEN=' .env | cut -d= -f2-)
```

### C) 令牌位于 `.env` 文件中，但变量名不同

查找任何看起来像 Vercel 令牌的变量（Vercel 令牌通常以 `vca_` 开头）：

```bash
grep -i 'vercel' .env 2>/dev/null
```

检查输出，确定哪个变量保存了令牌，然后将其导出为 `VERCEL_TOKEN`：

```bash
export VERCEL_TOKEN=$(grep '^<VARIABLE_NAME>=' .env | cut -d= -f2-)
```

### D) 未找到令牌——询问用户

如果以上方法均未找到令牌，请让用户提供一个。他们可以在 vercel.com/account/tokens 创建 Vercel 访问令牌。

---

**重要：** 将 `VERCEL_TOKEN` 导出为环境变量后，Vercel CLI 会原生读取它——**不要通过 `--token` 标志传递它**。将密钥放在命令行参数中会使其暴露在 shell 历史记录和进程列表中。

```bash
# 错误——令牌会显示在 shell 历史记录和进程列表中
vercel deploy --token "vca_abc123"

# 正确——CLI 从环境中读取 VERCEL_TOKEN
export VERCEL_TOKEN="vca_abc123"
vercel deploy
```

## 步骤 2：查找项目和团队

同样，检查项目 ID 和团队作用域。有了这些信息，CLI 无需执行 `vercel link` 即可定位正确的项目。

```bash
# 检查环境
printenv VERCEL_PROJECT_ID
printenv VERCEL_ORG_ID

# 或检查 .env
grep -i 'vercel' .env 2>/dev/null
```

**如果你有项目 URL**（例如 `https://vercel.com/my-team/my-project`），请提取团队 slug：

```bash
# 例如，从 "https://vercel.com/my-team/my-project" 中提取 "my-team"
echo "$PROJECT_URL" | sed 's|https://vercel.com/||' | cut -d/ -f1
```

**如果环境中同时存在 `VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID`**，请将它们导出——CLI 会自动使用这些变量，并跳过任何 `.vercel/` 目录：

```bash
export VERCEL_ORG_ID="<org-id>"
export VERCEL_PROJECT_ID="<project-id>"
```

注意：必须同时设置 `VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID`——只设置其中一个会导致错误。

## CLI 设置

确保已安装 Vercel CLI，并且它是最新版本：

```bash
npm install -g vercel
vercel --version
```

## 部署项目

除非用户明确要求部署到生产环境，否则始终部署为**预览环境**。根据现有条件选择一种方法。

### 快速部署（已有项目 ID——无需链接）

当环境中已设置 `VERCEL_TOKEN` 和 `VERCEL_PROJECT_ID` 时，直接部署：

```bash
vercel deploy -y --no-wait
```

指定团队作用域（通过 `VERCEL_ORG_ID` 或 `--scope`）：

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

生产环境部署（仅在明确要求时）：

```bash
vercel deploy --prod --scope <team-slug> -y --no-wait
```

检查状态：

```bash
vercel inspect <deployment-url>
```

### 完整部署流程（没有项目 ID——需要链接）

当你有令牌和团队信息，但没有预先存在的项目 ID 时，使用此流程。

#### 先检查项目状态

```bash
# 项目是否有 git 远程仓库？
git remote get-url origin 2>/dev/null

# 是否已经链接到 Vercel 项目？
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
```

#### 链接项目

**有 git 远程仓库（首选）：**

```bash
vercel link --repo --scope <team-slug> -y
```

读取 git 远程仓库并连接到匹配的 Vercel 项目。创建 `.vercel/repo.json`。这比普通的 `vercel link` 更可靠，后者会按目录名称进行匹配。

**没有 git 远程仓库：**

```bash
vercel link --scope <team-slug> -y
```

创建 `.vercel/project.json`。

**按名称链接到特定项目：**

```bash
vercel link --project <project-name> --scope <team-slug> -y
```

如果项目已链接，请检查 `.vercel/project.json` 或 `.vercel/repo.json` 中的 `orgId`，确认它与目标团队匹配。

#### 链接后部署

**A) Git 推送部署——有 git 远程仓库（首选）**

Git 推送会触发 Vercel 自动部署。

1. **推送前询问用户。** 未经明确批准，绝不推送。
2. 提交并推送：
   ```bash
   git add .
   git commit -m "deploy: <description of changes>"
   git push
   ```
3. Vercel 会自动构建。非生产分支会获得预览部署。
4. 获取部署 URL：
   ```bash
   sleep 5
   vercel ls --format json --scope <team-slug>
   ```
   在 `deployments` 数组中找到最新条目。

**B) CLI 部署——没有 git 远程仓库**

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

检查状态：

```bash
vercel inspect <deployment-url>
```

### 从远程仓库部署（代码未克隆到本地）

1. 克隆仓库：
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```
2. 链接到 Vercel：
   ```bash
   vercel link --repo --scope <team-slug> -y
   ```
3. 通过 git 推送（如果你有推送权限）或 CLI 进行部署。

### 关于 `.vercel/` 目录

已链接的项目具有以下文件之一：

- `.vercel/project.json`——由 `vercel link` 创建。包含 `projectId` 和 `orgId`。
- `.vercel/repo.json`——由 `vercel link --repo` 创建。包含 `orgId`、`remoteName` 和一个 `projects` 映射。

当环境中同时设置了 `VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID` 时，不需要这些文件。

**不要**在未链接的目录中运行 `vercel project inspect` 或 `vercel link` 来检测状态——它们会进行交互式提示，或以副作用的方式静默链接项目。`vercel ls` 是安全的（在未链接的目录中，它默认显示该作用域下的所有部署）。`vercel whoami` 在任何位置都可以安全运行。

## 管理环境变量

```bash
# 为所有环境设置
echo "value" | vercel env add VAR_NAME --scope <team-slug>

# 为特定环境设置（production、preview、development）
echo "value" | vercel env add VAR_NAME production --scope <team-slug>

# 列出环境变量
vercel env ls --scope <team-slug>

# 将环境变量拉取到本地 .env.local 文件
vercel env pull --scope <team-slug>

# 删除变量
vercel env rm VAR_NAME --scope <team-slug> -y
```

## 检查部署

```bash
# 列出最近的部署
vercel ls --format json --scope <team-slug>

# 检查特定部署
vercel inspect <deployment-url>

# 查看构建日志（需要 Vercel CLI v35+）
vercel inspect <deployment-url> --logs

# 查看运行时请求日志（默认实时跟踪；添加 --no-follow 可获取一次性快照）
vercel logs <deployment-url>
```

## 管理域名

```bash
# 列出域名
vercel domains ls --scope <team-slug>

# 将域名添加到项目——已链接目录或通过环境变量链接的目录（1 个参数）
vercel domains add <domain> --scope <team-slug>

# 添加域名——未链接目录（需要 <project> 位置参数）
vercel domains add <domain> <project> --scope <team-slug>
```

## Stripe Projects 套餐变更

如果此项目由 Stripe Projects 管理，**在执行任何收费或破坏性的套餐变更之前，请先询问用户**——升级会从真实银行卡扣费，降级会移除席位。

首先运行 `stripe projects status --json`，确认 Vercel 资源的本地名称。以下示例假定使用默认名称（`vercel-plan`）；如果该名称在执行 `stripe projects add` 时被重命名，请替换为实际名称。

- **升级到 Pro：** `stripe projects add vercel/pro`（或 `stripe projects upgrade vercel-plan pro`）
- **降级到 Hobby：** `stripe projects downgrade vercel-plan hobby`

### Pro 为你提供的功能

- 每月 20 美元的平台费用，其中包含每月 20 美元的使用额度。
- 新项目默认使用 Turbo 构建机器（30 个 vCPU、60 GB 内存）——构建速度明显快于 Hobby。
- 1 个部署席位，以及不限数量的免费 Viewer 席位（只读协作者、预览评论）。
- 更高的内含配额（每月 1 TB Fast Data Transfer、1000 万次 Edge Requests）。
- 可购买的付费附加功能：SAML SSO、HIPAA BAA、Flags Explorer、Observability Plus、Speed Insights、Web Analytics Plus。

完整详情：https://vercel.com/docs/plans/pro-plan

## 工作约定

- **绝不要通过 `--token` 标志传递 `VERCEL_TOKEN`。** 将其导出为环境变量，让 CLI 原生读取。
- **在询问用户之前，先检查环境中是否存在令牌。** 先检查当前环境和 `.env` 文件。
- **默认使用预览部署。** 仅在明确要求时部署到生产环境。
- **推送到 git 前先询问。** 未经用户批准，绝不推送提交。
- **不要直接修改 `.vercel/` 文件。** 此目录由 CLI 管理。可以读取这些文件（例如验证 `orgId`）。
- **不要通过 curl/fetch 已部署的 URL 进行验证。** 只需将链接返回给用户。
- 当结构化输出有助于后续步骤时，**使用 `--format json`**。
- 对会提示确认的命令**使用 `-y`**，以避免交互式阻塞。

## 故障排除

### 未找到令牌

检查环境以及任何现有的 `.env` 文件：

```bash
printenv | grep -i vercel
grep -i vercel .env 2>/dev/null
```

### 身份验证错误

如果 CLI 失败并显示 `Authentication required`：

- 令牌可能已过期或无效。
- 验证：`vercel whoami`（使用环境中的 `VERCEL_TOKEN`）。
- 请用户提供一个新令牌。

### 团队错误

验证作用域是否正确：

```bash
vercel whoami --scope <team-slug>
```

### 构建失败

检查构建日志：

```bash
vercel inspect <deployment-url> --logs
```

常见原因：

- 缺少依赖项——确保 `package.json` 完整并已提交。
- 缺少环境变量——使用 `vercel env add` 添加。
- 框架配置错误——检查 `vercel.json`。Vercel 会根据 `package.json` 自动检测框架（Next.js、Remix、Vite 等）；如果检测错误，请使用 `vercel.json` 覆盖。

### 未安装 CLI

```bash
npm install -g vercel
```
