# Skills-Hub Review 编写指南

本指南说明如何创建、关联、生成和验证 Skills-Hub 的专题点评。点评源文件位于 `reviews/`，生成后的文档和网站数据不得手工维护。

## 1. 文件位置与命名

创建：

```text
reviews/<slug>.md
```

`slug` 使用简短的 kebab-case，例如 `ponytail-guide.md`。不要在 `reviews/` 放置 `README.md` 等辅助 Markdown；加载器会把该目录下的所有 `*.md` 当作点评解析。

## 2. Front matter

文件必须以 JSON front matter 开头。分隔符之间是合法 JSON，不是普通 YAML：

```markdown
---
{"title":"Ponytail Skills 使用指南","type":"review","related_projects":["ponytail"]}
---
# Ponytail Skills 使用指南
```

字段如下：

| 字段 | 必填 | 说明 |
|---|---|---|
| `title` | 是 | 网站和点评索引显示的标题，必须是字符串 |
| `type` | 是 | 仅允许 `comparison`、`review`、`test` |
| `related_projects` | 否 | 项目 ID 数组；关联项目下的全部 skill |
| `related_skills` | 否 | 精确 skill 键数组，格式为 `<project-id>/<skill-id>` |

至少设置一种关联字段，否则文章会进入点评索引，但不会出现在任何 skill 的“相关点评”中。

### 类型选择

| 类型 | 网站标签 | 适用内容 |
|---|---|---|
| `comparison` | 横向比较 | 比较多个项目或 skill 的定位、能力和选择方式 |
| `review` | 使用点评 | 系统介绍、学习笔记、使用指南或能力评价 |
| `test` | 测试记录 | 有明确步骤、环境、观察结果和结论的实际测试 |

### 关联整个项目

```json
{"title":"Ponytail Skills 使用指南","type":"review","related_projects":["ponytail"]}
```

这会把文章关联到 `ponytail` 项目下的全部 skill。

### 精确关联 skill

```json
{"title":"局部与全仓库审计对比","type":"comparison","related_skills":["ponytail/ponytail-review","ponytail/ponytail-audit"]}
```

项目 ID 和 skill ID 必须以 `registry/projects.yaml` 为准。

## 3. 编写流程

1. 运行 `git status --short`，记录并保留无关改动。
2. 从 `registry/projects.yaml` 确认项目 ID、skill ID 和路径。
3. 完整阅读点评涉及的源 `SKILL.md`，不要只根据名称或目录描述推断内容。
4. 参考已有 `reviews/*.md` 的结构，但不要复制与目标无关的章节。
5. 使用 `apply_patch` 创建或修改 `reviews/<slug>.md`。
6. 先验证加载器，再生成文档和网站。

点评应明确说明：

- 项目或 skill 的定位
- 各 skill 的实际内容
- 自然语言和显式命令触发条件
- 相似 skill 的范围区别
- 只读、修改、持续模式或一次性行为等边界
- 来源文件中存在的限制、例外或数据诚信要求

## 4. 生成

在仓库根目录依次运行：

```powershell
python scripts\content_sources.py
python scripts\generate_docs.py
python scripts\generate_site.py
```

生成器会更新：

- `docs/reviews/<slug>.md`：去除 front matter 的公开文档
- `docs/reviews/index.md`：点评索引
- `site/skill-content.json`：skill 内容和点评关联数据
- `site/index.html`：静态网站

`generate_docs.py` 还可能刷新其他生成文档。不要为了点评手工修改生成输出；如果生成器产生与任务无关的内容差异，应先核对原因，再只撤回无关差异。

## 5. 网站关联机制

`scripts/content_sources.py` 读取 `reviews/*.md`：

- `related_projects` 命中项目 ID 时，关联该项目的全部 skill。
- `related_skills` 命中 `<project-id>/<skill-id>` 时，只关联对应 skill。

`scripts/generate_site.py` 把关联结果写入 `site/skill-content.json`。网站打开 skill 详情时，在内容下方显示“相关点评”，链接到：

```text
docs/reviews/<slug>.md
```

## 6. 验证清单

- `python scripts\content_sources.py` 无错误。
- `python scripts\generate_docs.py` 报告的 review 数量符合预期。
- `python scripts\generate_site.py` 成功完成。
- `docs/reviews/<slug>.md` 已生成。
- `docs/reviews/index.md` 包含标题和正确的类型标签。
- `site/skill-content.json` 中预期的每个 skill 都包含该 review 的 `slug`。
- `git diff --check` 无空白错误。
- `git status --short` 中没有误改 `libraries/`、registry 或其他用户工作。

PowerShell 精确检查某个 slug 的关联：

```powershell
$data = Get-Content -Raw site\skill-content.json | ConvertFrom-Json -AsHashtable
$data.GetEnumerator() |
  Where-Object { $_.Value.reviews.slug -contains '<slug>' } |
  Select-Object -ExpandProperty Key
```

输出的路径数量和范围应与 `related_projects` 或 `related_skills` 的意图一致。

## 7. 常见错误

- 使用 YAML front matter：加载器要求 JSON。
- 把 `type` 写成未支持的值：只能使用三种已登记类型。
- 使用目录名猜测关联键：必须查 `registry/projects.yaml`。
- 只创建 `docs/reviews/` 文件：下次生成会覆盖，源文件应放在 `reviews/`。
- 创建 `reviews/README.md`：它也会被当作点评解析。
- 只生成文档、不生成网站：网站不会获得新的关联数据。
- 用原始中文搜索网站 JSON 验证：JSON 可能转义 Unicode，应结构化解析。
