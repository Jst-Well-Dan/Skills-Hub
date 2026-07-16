<!-- source-sha256: afc5eb6d748f8d4ff521a3bec024e51fc77d35344a502555486f029871d262d0 -->
---
name: baoyu-post-to-weibo
description: 将内容发布到微博。支持包含文本、图片和视频的普通微博，以及通过 Chrome CDP 使用 Markdown 输入发布头条文章。当用户要求“post to Weibo”、“发微博”、“发布微博”、“publish to Weibo”、“share on Weibo”、“写微博”或“微博头条文章”时使用。
version: 1.117.3
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-post-to-weibo
    requires:
      anyBins:
        - bun
        - npx
---

# 发布到微博

通过真实的 Chrome 浏览器将文本、图片、视频和长篇文章发布到微博（绕过反机器人检测）。

## 脚本目录

**重要**：所有脚本均位于此技能的 `scripts/` 子目录中。

**智能体执行说明**：
1. 确定此 SKILL.md 文件的目录路径，并将其记为 `{baseDir}`
2. 脚本路径 = `{baseDir}/scripts/<script-name>.ts`
3. 将本文档中的所有 `{baseDir}` 替换为实际路径
4. 确定 `${BUN_X}` 运行时：如果已安装 `bun` → `bun`；如果 `npx` 可用 → `npx -y bun`；否则建议安装 bun

**脚本参考**：
| 脚本 | 用途 |
|--------|---------|
| `scripts/weibo-post.ts` | 普通微博（文本 + 图片） |
| `scripts/weibo-article.ts` | 发布头条文章（Markdown） |
| `scripts/copy-to-clipboard.ts` | 将内容复制到剪贴板 |
| `scripts/paste-from-clipboard.ts` | 发送真实的粘贴按键操作 |

## 偏好设置（EXTEND.md）

按优先级顺序检查 EXTEND.md——找到的第一个生效：

| 优先级 | 路径 | 作用域 |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-post-to-weibo/EXTEND.md` | 项目 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-post-to-weibo/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-post-to-weibo/EXTEND.md` | 用户主目录 |

如果均未找到，则使用默认设置。

**EXTEND.md 支持**：默认 Chrome 配置文件

## 前置条件

- Google Chrome 或 Chromium
- `bun` 运行时
- 首次运行：手动登录微博（会话将被保存）

---

## 普通微博

文本 + 图片/视频（文件总数最多 18 个）。发布于微博首页。

```bash
${BUN_X} {baseDir}/scripts/weibo-post.ts "Hello Weibo!" --image ./photo.png
${BUN_X} {baseDir}/scripts/weibo-post.ts "Watch this" --video ./clip.mp4
```

**参数**：
| 参数 | 说明 |
|-----------|-------------|
| `<text>` | 微博内容（位置参数） |
| `--image <path>` | 图片文件（可重复使用） |
| `--video <path>` | 视频文件（可重复使用） |
| `--profile <dir>` | 自定义 Chrome 配置文件 |

**注意**：脚本会打开浏览器并填入内容。用户需要检查并手动发布。

---

## 头条文章

在 `https://card.weibo.com/article/v3/editor` 发布 Markdown 长文章。

```bash
${BUN_X} {baseDir}/scripts/weibo-article.ts article.md
${BUN_X} {baseDir}/scripts/weibo-article.ts article.md --cover ./cover.jpg
```

**参数**：
| 参数 | 说明 |
|-----------|-------------|
| `<markdown>` | Markdown 文件（位置参数） |
| `--cover <path>` | 封面图片 |
| `--title <text>` | 覆盖标题（最多 32 个字符，超出时截断） |
| `--summary <text>` | 覆盖摘要（最多 44 个字符，超出时自动重新生成） |
| `--profile <dir>` | 自定义 Chrome 配置文件 |

**Frontmatter**：YAML front matter 支持 `title`、`summary`、`cover_image`。

**字符限制**：
- 标题：最多 32 个字符（超出时截断并发出警告）
- 摘要/导语：最多 44 个字符（超出时根据正文内容自动重新生成）

**Markdown 转 HTML**：将 Markdown 转换为 HTML 时，绝对不要传递任何 `--theme` 参数。使用默认主题（不提供主题参数）。

**文章工作流程**：
1. 打开 `https://card.weibo.com/article/v3/editor`
2. 点击“写文章”按钮，等待编辑器变为可编辑状态
3. 填写标题（验证是否符合 32 个字符的限制）
4. 填写摘要/导语（验证是否符合 44 个字符的限制）
5. 通过粘贴将 HTML 内容插入 ProseMirror 编辑器
6. 逐一替换图片占位符（复制图片 → 选择占位符 → 粘贴）

**内容编排后检查**：插入所有图片后，脚本会自动验证：
- 编辑器内容中是否还存在 `WBIMGPH_` 占位符
- 预期图片数量与实际图片数量是否一致

如果检查失败（输出中出现警告），请在用户发布前告知具体问题。

---

## 发布类型选择

除非用户明确指定发布类型：
- **Markdown 文件**（`.md`）→ **头条文章**
- **纯文本** / 带图片的文本 → **普通微博**

## 故障排除

### Chrome 调试端口未就绪

如果脚本因 `Chrome debug port not ready` 或 `Unable to connect` 而失败，仅终止 CDP Chrome 实例（同时带有 `--remote-debugging-port` 和 baoyu-skills 配置文件的实例），然后重试：

```bash
pkill -f "remote-debugging-port.*baoyu-skills/chrome-profile" 2>/dev/null; sleep 2
```

**严重警告**：绝对不要终止所有 Chrome 进程（`pkill -f "Google Chrome"`）。只能终止由 CDP 使用 baoyu-skills 配置文件目录启动的 Chrome 实例。用户可能仍有普通 Chrome 窗口处于打开状态。

**重要**：此操作应自动执行——遇到该错误时，无须询问用户，直接终止 CDP Chrome 实例并重试命令。

## 注意事项

- 首次运行：需要手动登录（会话将保持）
- 所有脚本都只会将内容填入浏览器，用户必须检查并手动发布
- 跨平台：macOS、Linux、Windows

## 扩展支持

通过 EXTEND.md 进行自定义配置。有关路径和支持的选项，请参阅**偏好设置**部分。
