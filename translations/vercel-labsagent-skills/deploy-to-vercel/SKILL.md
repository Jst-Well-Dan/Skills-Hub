<!-- source-sha256: cfcc3dd479ab2e0ae721ddf39b8af84d977321487672f1487c8d6855f576927b -->
---
name: deploy-to-vercel
description: 将应用程序和网站部署到 Vercel。当用户请求“部署我的应用”、“部署并把链接给我”、“将其上线”或“创建预览部署”等部署操作时使用。
metadata:
  author: vercel
  version: "3.0.0"
---

# 部署到 Vercel

将任何项目部署到 Vercel。除非用户明确要求部署到生产环境，否则**始终部署为预览环境**（而非生产环境）。

目标是帮助用户建立最佳的长期配置：将其项目关联到 Vercel，并通过 git push 进行部署。以下每种方法都会尽量让用户更接近这一状态。

## 第 1 步：收集项目状态

在决定使用哪种方法之前，运行以下全部四项检查：

```bash
# 1. Check for a git remote
git remote get-url origin 2>/dev/null

# 2. Check if locally linked to a Vercel project (either file means linked)
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null

# 3. Check if the Vercel CLI is installed and authenticated
vercel whoami 2>/dev/null

# 4. List available teams (if authenticated)
vercel teams list --format json 2>/dev/null
```

### 团队选择

如果用户属于多个团队，以项目符号列表展示所有可用的团队 slug，并询问要部署到哪一个团队。用户选择团队后，立即进入下一步——不要再要求额外确认。

在所有后续 CLI 命令（`vercel deploy`、`vercel link`、`vercel inspect` 等）中，通过 `--scope` 传入团队 slug：

```bash
vercel deploy [path] -y --no-wait --scope <team-slug>
```

如果项目已关联（存在 `.vercel/project.json` 或 `.vercel/repo.json`），这些文件中的 `orgId` 将决定所属团队——无需再次询问。如果只有一个团队（或只有个人账户），跳过询问并直接使用。

**关于 `.vercel/` 目录：**已关联的项目会包含以下文件之一：

- `.vercel/project.json`——由 `vercel link` 创建（单项目关联）。包含 `projectId` 和 `orgId`。
- `.vercel/repo.json`——由 `vercel link --repo` 创建（基于仓库的关联）。包含 `orgId`、`remoteName`，以及将目录映射到 Vercel 项目 ID 的 `projects` 数组。

存在任一文件都表示项目已关联。务必检查这两个文件。

**不要**在未关联的目录中使用 `vercel project inspect`、`vercel ls` 或 `vercel link` 来检测状态——如果没有 `.vercel/` 配置，它们会发起交互式询问（或在使用 `--yes` 时产生静默关联的副作用）。只有 `vercel whoami` 可以安全地在任何位置运行。

## 第 2 步：选择部署方法

### 已关联（存在 `.vercel/`）且有 git 远程仓库 → Git Push

这是理想状态。项目已关联并集成了 git。

1. **推送前询问用户。**绝不能在未经明确批准的情况下推送：
   ```
   此项目已通过 git 连接到 Vercel。我可以提交并推送更改，
   从而触发部署。要我继续吗？
   ```

2. **提交并推送：**
   ```bash
   git add .
   git commit -m "deploy: <description of changes>"
   git push
   ```
   Vercel 会自动根据推送内容执行构建。非生产分支会获得预览部署；生产分支（通常为 `main`）会获得生产部署。

3. **获取预览 URL。**如果 CLI 已通过身份验证：
   ```bash
   sleep 5
   vercel ls --format json
   ```
   JSON 输出中包含一个 `deployments` 数组。找到最新条目——其 `url` 字段就是预览 URL。

   如果 CLI 未通过身份验证，请告知用户前往 Vercel 控制面板，或查看其 git 提供商上的提交状态检查，以获取预览 URL。

---

### 已关联（存在 `.vercel/`）且没有 git 远程仓库 → `vercel deploy`

项目已关联，但没有 git 仓库。使用 CLI 直接部署。

```bash
vercel deploy [path] -y --no-wait
```

使用 `--no-wait`，让 CLI 立即返回部署 URL，而不是阻塞并等待构建完成（构建可能需要一段时间）。然后使用以下命令检查部署状态：

```bash
vercel inspect <deployment-url>
```

对于生产部署（仅当用户明确要求时）：

```bash
vercel deploy [path] --prod -y --no-wait
```

---

### 未关联且 CLI 已通过身份验证 → 先关联，再部署

CLI 可以正常工作，但项目尚未关联。这是帮助用户进入最佳状态的机会。

1. **询问用户要部署到哪个团队。**以项目符号列表展示第 1 步获取的团队 slug。如果只有一个团队（或只有个人账户），跳过此步骤。

2. **选择团队后，直接进行关联。**告知用户接下来会发生什么，但不要单独请求确认：
   ```
   正在将此项目关联到 Vercel 上的 <team name>。这将创建一个用于部署的
   Vercel 项目，并启用未来 git push 时的自动部署。
   ```

3. **如果存在 git 远程仓库**，使用所选团队作用域执行基于仓库的关联：
   ```bash
   vercel link --repo --scope <team-slug>
   ```
   此命令会读取 git 远程仓库 URL，并将其与从该仓库部署的现有 Vercel 项目进行匹配。它会创建 `.vercel/repo.json`。这比不带 `--repo` 的 `vercel link` 可靠得多；后者会尝试按目录名称匹配，当本地文件夹与 Vercel 项目名称不同时经常失败。

   **如果没有 git 远程仓库**，则退回到标准关联方式：
   ```bash
   vercel link --scope <team-slug>
   ```
   此命令会提示用户选择或创建项目。它会创建 `.vercel/project.json`。

4. **然后使用当前最佳方法进行部署：**

   - 如果存在 git 远程仓库 → 提交并推送（参见上面的 git push 方法）
   - 如果没有 git 远程仓库 → 执行 `vercel deploy [path] -y --no-wait --scope <team-slug>`，然后执行 `vercel inspect <url>` 检查状态

---

### 未关联且 CLI 未通过身份验证 → 安装、验证身份、关联、部署

Vercel CLI 尚未完成任何设置。

1. **安装 CLI（如果尚未安装）：**
   ```bash
   npm install -g vercel
   ```

2. **进行身份验证：**
   ```bash
   vercel login
   ```
   用户在浏览器中完成身份验证。如果运行环境不可交互、无法登录，请跳到下方的**无身份验证回退方案**。

3. **询问要部署到哪个团队**——以项目符号列表展示 `vercel teams list --format json` 返回的团队 slug。如果只有一个团队或个人账户，则跳过。选择后立即继续。

4. **使用所选团队作用域关联项目**（如果存在 git 远程仓库则使用 `--repo`，否则使用普通的 `vercel link`）：
   ```bash
   vercel link --repo --scope <team-slug>   # if git remote exists
   vercel link --scope <team-slug>          # if no git remote
   ```

5. **使用当前最佳方法部署**（如果存在远程仓库则使用 git push，否则执行 `vercel deploy -y --no-wait --scope <team-slug>`，然后执行 `vercel inspect <url>` 检查状态）。

---

### 无身份验证回退方案——claude.ai 沙箱

**使用时机：**在 claude.ai 沙箱中无法安装 CLI 或进行身份验证时，作为最后的手段。此方法不需要身份验证——它会返回一个**预览 URL**（在线站点）和一个**认领 URL**（用于转移到你的 Vercel 账户）。

```bash
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh [path]
```

**参数：**

- `path` - 要部署的目录或 `.tgz` 文件（默认为当前目录）

**示例：**

```bash
# Deploy current directory
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh

# Deploy specific project
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh /path/to/project

# Deploy existing tarball
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh /path/to/project.tgz
```

该脚本会从 `package.json` 自动检测框架，打包项目（排除 `node_modules`、`.git`、`.env`），上传项目，并等待构建完成。

**告知用户：**“你的部署已准备就绪：[previewUrl]。请前往 [claimUrl] 认领，以管理你的部署。”

---

### 无身份验证回退方案——Codex 沙箱

**使用时机：**在 CLI 可能未通过身份验证的 Codex 沙箱中。Codex 默认运行在沙箱环境中——先尝试使用 CLI，如果身份验证失败，再退回到部署脚本。

1. **检查是否已安装 Vercel CLI**（此检查无需提升权限）：
   ```bash
   command -v vercel
   ```

2. **如果已安装 `vercel`**，尝试使用 CLI 部署：
   ```bash
   vercel deploy [path] -y --no-wait
   ```

3. **如果未安装 `vercel`，或者 CLI 返回 `"No existing credentials found"` 错误**，使用回退脚本：
   ```bash
   skill_dir="<path-to-skill>"

   # Deploy current directory
   bash "$skill_dir/resources/deploy-codex.sh"

   # Deploy specific project
   bash "$skill_dir/resources/deploy-codex.sh" /path/to/project

   # Deploy existing tarball
   bash "$skill_dir/resources/deploy-codex.sh" /path/to/project.tgz
   ```

该脚本负责框架检测、打包和部署。它会等待构建完成，并返回包含 `previewUrl` 和 `claimUrl` 的 JSON。

**告知用户：**“你的部署已准备就绪：[previewUrl]。请前往 [claimUrl] 认领，以管理你的部署。”

**提升后的网络访问：**只有在沙箱阻止网络调用时，才提升实际部署命令的权限（`sandbox_permissions=require_escalated`）。**不要**提升 `command -v vercel` 检查的权限。

---

## 特定代理说明

### Claude Code／基于终端的代理

你拥有完整的 shell 访问权限。不要使用 `/mnt/skills/` 路径。按照上面的决策流程，直接使用 CLI。

对于无身份验证回退方案，请从该技能的安装位置运行部署脚本：

```bash
bash ~/.claude/skills/deploy-to-vercel/resources/deploy.sh [path]
```

具体路径可能因用户安装技能的位置而异。

### 沙箱环境（claude.ai）

你很可能无法运行 `vercel login` 或 `git push`。请直接使用**无身份验证回退方案——claude.ai 沙箱**。

### Codex

Codex 运行在沙箱中。先检查 CLI 是否可用，然后退回到部署脚本。请使用**无身份验证回退方案——Codex 沙箱**。

---

## 输出

始终向用户显示部署 URL。

- **Git push：**使用 `vercel ls --format json` 查找预览 URL。如果 CLI 未通过身份验证，请告知用户前往 Vercel 控制面板或查看提交状态检查。
- **CLI 部署：**显示 `vercel deploy --no-wait` 返回的 URL。使用 `vercel inspect <url>` 检查构建状态并向用户报告。
- **无身份验证回退方案：**同时显示预览 URL 和认领 URL：
  ```
  部署成功！

  预览 URL：https://my-app-abc123.vercel.app
  认领 URL：https://vercel.com/claim-deployment?code=...

  请通过预览 URL 查看你的网站。
  要将此部署转移到你的 Vercel 账户，请访问认领 URL。
  ```

**不要**使用 curl 或获取已部署的 URL 来验证其是否正常工作。只需返回链接。

---

## 故障排除

### 网络出口错误（claude.ai）

如果由于 claude.ai 的网络限制导致部署失败，请告知用户：

```
由于网络限制，部署失败。修复方法如下：

1. 前往 https://claude.ai/settings/capabilities
2. 将 *.vercel.com 添加到允许的域名
3. 再次尝试部署
```

### 提升后的网络访问（Codex／沙箱环境）

如果在沙箱环境中由于网络问题（超时、DNS 错误、连接重置）导致部署失败，请使用提升后的权限（`sandbox_permissions=require_escalated`）重新运行。不要提升初始 CLI 可用性检查的权限——只提升实际部署命令的权限。

给用户的示例说明：

```
部署到 Vercel 需要提升后的网络访问权限。我可以使用提升后的权限
重新运行该命令——要我继续吗？
```

### CLI 身份验证失败

如果 `vercel login` 或 `vercel deploy` 因身份验证错误而失败，请根据当前环境退回到无身份验证部署脚本（claude.ai 或 Codex 版本）。
