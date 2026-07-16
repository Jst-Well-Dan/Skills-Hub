<!-- source-sha256: e15f1b5a51b8443ef1c8191c036301fd9b3e028069b82b625f327b0344cbc9d8 -->
---
name: baoyu-post-to-wechat
description: 通过 API 或 Chrome CDP 将内容发布到微信公众号。支持以 HTML、markdown 或纯文本作为输入发布文章，以及包含多张图片的贴图（原称图文）发布。Markdown 文章工作流默认将普通外部链接转换为底部引用，以生成更适合微信的内容。用户提到“发布公众号”、“post to wechat”、“微信公众号”或“贴图/图文/文章”时使用。
version: 1.118.2
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat
    requires:
      anyBins:
        - bun
        - npx
---

# 发布到微信公众号

## 用户输入工具

当此技能需要向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具**，即当前智能体运行环境提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **后备方案**：如果没有此类工具，则发送带编号的纯文本消息，并要求用户针对每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持每次调用提出多个问题，请将所有适用问题合并到一次调用中；如果只支持单个问题，则按优先级逐一提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行环境中请替换为当地等效工具。

## 语言

使用用户的语言回复。如果用户使用中文，则用中文回复；如果使用英文，则用英文回复。技术标记（路径、标志、字段名）保留英文。

## 脚本目录

`{baseDir}` = 此 SKILL.md 所在的目录。解析 `${BUN_X}`：优先使用 `bun`；否则使用 `npx -y bun`；再否则建议执行 `brew install oven-sh/bun/bun`。

| 脚本 | 用途 |
|--------|---------|
| `scripts/wechat-browser.ts` | 贴图发布（图文） |
| `scripts/wechat-article.ts` | 通过浏览器发布文章（文章） |
| `scripts/wechat-api.ts` | 通过 API 发布文章（文章） |
| `scripts/md-to-wechat.ts` | Markdown → 带图片占位符的微信就绪 HTML |
| `scripts/check-permissions.ts` | 验证环境和权限 |

## 偏好设置（EXTEND.md）

按顺序检查以下路径；第一个匹配项生效：

| 路径 | 作用域 |
|------|-------|
| `.baoyu-skills/baoyu-post-to-wechat/EXTEND.md` | 项目 |
| `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-post-to-wechat/EXTEND.md` | XDG |
| `$HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md` | 用户主目录 |

找到 → 读取、解析并应用。未找到 → 在执行任何其他操作前运行首次设置（`references/config/first-time-setup.md`）。

**最少必需键**（不区分大小写，接受 `1/0` 或 `true/false`）：

| 键 | 默认值 | 映射 |
|-----|---------|---------|
| `default_author` | 空 | CLI/前置元数据未提供 `author` 时的后备值 |
| `need_open_comment` | `1` | `draft/add` 中的 `articles[].need_open_comment` |
| `only_fans_can_comment` | `0` | `draft/add` 中的 `articles[].only_fans_can_comment` |

**推荐的 EXTEND.md**：

```md
default_theme: default
default_color: blue
default_publish_method: browser
default_author: 宝玉
need_open_comment: 1
only_fans_can_comment: 0
chrome_profile_path: /path/to/chrome/profile

# 远程 API 发布（可选）——仅当微信的 IP 白名单
# 排除了你的本地计算机时设置。请参阅下文“远程 API 方式”。
# remote_publish_host: server.example.com
# remote_publish_user: deploy
# remote_publish_port: 22
# remote_publish_identity_file: ~/.ssh/id_ed25519
# remote_publish_known_hosts_file: ~/.ssh/known_hosts
# remote_publish_strict_host_key_checking: accept-new
# remote_publish_connect_timeout: 10
# remote_publish_proxy_jump: bastion.example.com
```

有意不支持原始 `ssh` / `scp` 选项；仅接受上述类型化键。身份验证仅支持 SSH 密钥（不支持密码）。

**主题选项**：default、grace、simple、modern。**颜色预设**：blue、green、vermilion、yellow、purple、sky、rose、olive、black、gray、pink、red、orange（或十六进制颜色值）。

**值优先级**：CLI 参数 → 前置元数据 → EXTEND.md（账户级 → 全局）→ 技能默认值。

## 多账户支持

EXTEND.md 支持使用 `accounts:` 块管理多个公众号。当存在 2 个或更多条目时，工作流会插入步骤 0.5，提示选择账户（或者根据 `default: true` 或 `--account <alias>` 自动选择）。

完整详情——兼容性规则、每账户键、凭据解析、每账户 Chrome 配置文件、CLI 用法——请参阅 `references/multi-account.md`。

## 发布前检查（可选）

首次使用前，建议执行环境检查（用户可以跳过）：

```bash
${BUN_X} {baseDir}/scripts/check-permissions.ts
```

检查项：Chrome、配置文件隔离、Bun、辅助功能、剪贴板、粘贴按键、API 凭据、Chrome 冲突。

| 检查失败 | 修复方式 |
|-------------|-----|
| Chrome | 安装 Chrome 或设置 `WECHAT_BROWSER_CHROME_PATH` |
| 配置文件目录 | 位于 `baoyu-skills/chrome-profile` 的共享配置文件 |
| Bun 运行时 | `brew install oven-sh/bun/bun` 或 `npm install -g bun` |
| 辅助功能（macOS） | 系统设置 → 隐私与安全性 → 辅助功能 → 启用终端应用 |
| 剪贴板复制 | 确保 Swift/AppKit 可用（macOS：`xcode-select --install`） |
| 粘贴按键（Linux） | 安装 `xdotool`（X11）或 `ydotool`（Wayland） |
| API 凭据 | 按照步骤 2 中的引导设置操作，或在 `.baoyu-skills/.env` 中设置 |

## 贴图发布（图文）

包含多张图片的短内容（最多 9 张）：

```bash
${BUN_X} {baseDir}/scripts/wechat-browser.ts --markdown article.md --images ./images/
${BUN_X} {baseDir}/scripts/wechat-browser.ts --title "标题" --content "内容" --image img.png --submit
```

详情：`references/image-text-posting.md`。

## 文章发布工作流（文章）

```
- [ ] 步骤 0：加载偏好设置（EXTEND.md）
- [ ] 步骤 0.5：解析账户（仅多账户——参阅 references/multi-account.md）
- [ ] 步骤 1：确定输入类型
- [ ] 步骤 2：选择方式并配置凭据
- [ ] 步骤 3：解析主题/颜色并验证元数据
- [ ] 步骤 4：发布到微信
- [ ] 步骤 5：报告完成情况
```

### 步骤 0：加载偏好设置

检查并加载 EXTEND.md（参阅上文“偏好设置”）。如果未找到，请先完成首次设置，再提出任何其他问题。解析并缓存以下值供后续步骤使用：`default_theme`、`default_color`、`default_author`、`need_open_comment`、`only_fans_can_comment`。

### 步骤 1：确定输入类型

| 输入 | 检测方式 | 下一步 |
|-------|-----------|------|
| HTML 文件 | 路径以 `.html` 结尾且文件存在 | 跳至步骤 3 |
| Markdown 文件 | 路径以 `.md` 结尾且文件存在 | 步骤 2 |
| 纯文本 | 不是文件路径，或文件不存在 | 保存为 markdown，然后进入步骤 2 |

**纯文本处理**：

1. 生成 slug（取前 2–4 个有意义的单词，使用 kebab-case；为生成 slug，将中文翻译为英文）。
2. 保存到 `post-to-wechat/YYYY-MM-DD/<slug>.md`（如有需要则创建目录）。
3. 继续将其作为 markdown 文件处理。

### 步骤 2：选择发布方式并进行配置

除非已在 EXTEND.md 或 CLI 中指定，否则询问发布方式：

| 方式 | 速度 | 要求 |
|--------|-------|----------|
| `api`（推荐） | 快 | API 凭据（本地 IP 已加入白名单） |
| `browser` | 慢 | Chrome + 已登录的会话 |
| `remote-api` | 快 | API 凭据 + 一台可通过 SSH 访问且 IP 位于微信白名单中的服务器 |

**已选择 API 但缺少凭据** → 按照 `references/api-setup.md` 运行引导设置（写入 `.baoyu-skills/.env`）。

**`remote-api` 方式**：微信的“公众号设置 → IP 白名单”通常会将 API 访问限制为一两个固定 IP。如果本地计算机的 IP 不在白名单中，但某台云服务器的 IP 在其中，请使用 `remote-api`：所有 markdown 渲染、图片处理、草稿组装和 HTML 重写仍在本地进行，只有发送到 `api.weixin.qq.com` 的出站 HTTPS 调用（token、uploadimg、add_material、draft/add）会通过 SSH SOCKS5 动态端口转发（`ssh -N -D`），从而让微信将远程服务器视为源 IP。不会向远程主机写入任何文件；`AppSecret` 绝不会离开本地进程。远程主机只需具备 `sshd` 和出站网络连接——无需 Python，也无需智能体进程。请参阅下文“远程 API 方式”。

### 步骤 3：解析主题/颜色并验证元数据

1. **主题**：CLI `--theme` → EXTEND.md `default_theme` → `default`（第一个匹配项生效；如果已解析，切勿询问）。
2. **颜色**：CLI `--color` → EXTEND.md `default_color` → 省略（应用主题默认值）。
3. **验证元数据**（markdown 使用前置元数据，HTML 使用 meta 标签）：

| 字段 | 缺失时 → |
|-------|-----------|
| 标题 | 询问，或按 Enter 从内容中自动生成 |
| 摘要 | 前置元数据 `description` → `summary` → 询问或自动生成 |
| 作者 | CLI `--author` → 前置元数据 `author` → EXTEND.md `default_author` |
| 来源 URL | CLI `--source-url` → 前置元数据 `sourceUrl`/`contentSourceUrl`/`content_source_url` |

自动生成：标题 = 第一个 H1/H2 或第一句话；摘要 = 第一段，截断至 120 个字符。

4. **封面图片**（API `article_type=news` 必需）：CLI `--cover` → 前置元数据（`coverImage` / `featureImage` / `cover` / `image`）→ `imgs/cover.png` → 第一张内嵌图片 → 如果仍缺失，则停止并要求用户提供。

### 步骤 4：发布

**重要——绝不要预先将 markdown 转换为 HTML。** 发布脚本会在内部处理转换，而且两种方式对图片的渲染不同：API 方式渲染 `<img>` 标签以上传，浏览器方式使用占位符进行粘贴和替换。传入预先转换的 HTML 会导致其中一种方式失效。

**Markdown 引用默认行为**：对于 markdown 输入，普通外部链接默认转换为底部引用。仅当用户明确希望保留行内链接时，才使用 `--no-cite`。现有 HTML 输入保持原样。

**API 方式**（接受 `.md` 或 `.html`）：

```bash
${BUN_X} {baseDir}/scripts/wechat-api.ts <file> --theme <theme> [--color <color>] [--title <title>] [--summary <summary>] [--author <author>] [--cover <cover_path>] [--source-url <url>] [--no-cite]
```

即使主题为 `default`，也始终传递 `--theme`。仅当用户或 EXTEND.md 明确设置了颜色时才传递 `--color`。

**远程 API 方式**（使用相同脚本，添加 `--remote`）：

```bash
${BUN_X} {baseDir}/scripts/wechat-api.ts <file> --theme <theme> --remote [--remote-host <host>] [--remote-user <user>] [--remote-port <port>] [--remote-identity-file <path>] [--remote-known-hosts-file <path>] [--remote-strict-host-key-checking yes|no|accept-new] [--remote-connect-timeout <s>] [--remote-proxy-jump <spec>]
```

任何 `--remote-*` 标志都隐含启用 `--remote`。CLI 值优先于 EXTEND.md 中账户级、再到全局的 `remote_publish_*` 键。设置 `default_publish_method: remote-api` 也会在不使用 `--remote` 的情况下启用远程模式。

**`draft/add` 载荷规则**：

- 端点：`POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN`
- `article_type`：`news`（默认）或 `newspic`
- 对于 `news`，包含 `thumb_media_id`（封面必需）
- 请求正文中始终包含 `need_open_comment`（默认 `1`）和 `only_fans_can_comment`（默认 `0`），即使 CLI 未公开这些选项
- 对于 `news`，可以选择包含 `content_source_url`（原创文章 URL，显示为“阅读原文”链接，最大 1KB）。通过 CLI 标志 `--source-url` 或前置元数据 `sourceUrl`/`contentSourceUrl`/`content_source_url` 提供

**浏览器方式**（接受 `--markdown` 或 `--html`）：

```bash
${BUN_X} {baseDir}/scripts/wechat-article.ts --markdown <markdown_file> --theme <theme> [--color <color>] [--no-cite]
${BUN_X} {baseDir}/scripts/wechat-article.ts --html <html_file>
```

### 步骤 5：完成报告

```
微信发布完成！

输入：[类型] - [路径]
方式：[API | 浏览器]
主题：[主题] [颜色（如已设置）]

文章：
• 标题：[标题]
• 摘要：[摘要]
• 图片：[N] 张内嵌图片
• 评论：[开启/关闭]，[仅粉丝/所有人]    ← 仅 API 方式

结果：
✓ 草稿已保存到微信公众号
• media_id: [media_id]                         ← 仅 API 方式

后续步骤（API）：
→ 管理草稿：https://mp.weixin.qq.com（登录后进入「内容管理」→「草稿箱」）

已创建文件：
[• post-to-wechat/YYYY-MM-DD/slug.md（如果输入为纯文本）]
[• slug.html（已转换）]
```

## 功能对比

| 功能 | 贴图 | 文章（API） | 文章（远程 API） | 文章（浏览器） |
|---------|:---:|:---:|:---:|:---:|
| 纯文本输入 | ✗ | ✓ | ✓ | ✓ |
| HTML 输入 | ✗ | ✓ | ✓ | ✓ |
| Markdown 输入 | 标题/内容 | ✓ | ✓ | ✓ |
| 多张图片 | ✓（最多 9 张） | ✓（内嵌） | ✓（内嵌） | ✓（内嵌） |
| 主题 | ✗ | ✓ | ✓ | ✓ |
| 自动生成元数据 | ✗ | ✓ | ✓ | ✓ |
| 默认封面后备项（`imgs/cover.png`） | ✗ | ✓ | ✓ | ✗ |
| 评论控制 | ✗ | ✓ | ✓ | ✗ |
| 需要 Chrome | ✓ | ✗ | ✗ | ✓ |
| 需要 API 凭据 | ✗ | ✓ | ✓ | ✗ |
| 需要具有白名单 IP 且可通过 SSH 访问的服务器 | ✗ | ✗ | ✓ | ✗ |
| 速度 | 中等 | 快 | 快 | 慢 |

## 故障排除

| 问题 | 修复方式 |
|-------|-----|
| 缺少 API 凭据 | 按照步骤 2 中的引导设置操作 |
| 访问令牌错误 | 验证凭据有效且未过期 |
| 未登录（浏览器） | 首次运行会打开浏览器——扫描二维码登录。设置 `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` 可通过 Telegram 接收二维码图片 |
| 找不到 Chrome | 设置 `WECHAT_BROWSER_CHROME_PATH` |
| 缺少标题/摘要 | 使用自动生成或手动提供 |
| 没有封面图片 | 添加前置元数据封面，或将 `imgs/cover.png` 放入文章目录 |
| 评论默认值错误 | 检查 EXTEND.md 中的 `need_open_comment` / `only_fans_can_comment` |
| 粘贴失败 | 检查系统剪贴板权限 |
| `Remote publish host is required` | 设置 `--remote-host` 或 EXTEND.md 中的 `remote_publish_host` |
| `SOCKS proxy on 127.0.0.1:… not ready` | SSH 无法启动隧道——检查密钥、主机、`StrictHostKeyChecking`，或使用 `--remote-connect-timeout` |
| 远程发布期间出现 `ssh exited early` | 验证用户能以非交互方式通过 `ssh` 连接到服务器；如果连接较慢，请增大 `--remote-connect-timeout` |
| 远程 API 调用返回 `errcode 40164`（无效 IP） | 远程服务器的出口 IP 不在微信白名单中；请在公众号设置 → IP 白名单中添加该 IP |

## 参考资料

| 文件 | 内容 |
|------|---------|
| `references/image-text-posting.md` | 贴图参数、自动压缩 |
| `references/article-posting.md` | 文章主题、图片处理 |
| `references/multi-account.md` | 多账户兼容性、凭据、Chrome 配置文件、CLI |
| `references/api-setup.md` | 引导式凭据设置 |
| `references/config/first-time-setup.md` | 首次 EXTEND.md 设置 |

## 扩展支持

通过 EXTEND.md 提供自定义配置。有关路径和支持的选项，请参阅“偏好设置”。
