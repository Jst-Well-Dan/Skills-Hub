<!-- source-sha256: 6a49f45b40a80d8288eb28855ef3254bb2788a6a4c883a9bff6893ea20acc559 -->
---
name: skillhub-ingest
description: 在 Skills-Hub 仓库中添加、分类、提取、记录并验证托管在 GitHub 上的技能。当用户要求添加一个或多个技能仓库、从 GitHub URL 导入技能、处理 todo.md 中的技能收录项、从不完整的 GitHub 下载中恢复、为传入的技能创建新类别或标签、在收录后刷新 Skills-Hub 注册表/文档，或重复执行仓库的技能入库工作流时使用。
---

# SkillHub 收录

## 目的

使用此工作流将外部 GitHub 技能仓库添加到此 Skills-Hub 项目中，同时确保不遗漏注册、提取、文档生成或验证步骤。

该项目将源代码快照存储在 `libraries/` 中，将提取出的可安装副本存储在 `extracted-skills/` 中，将注册表数据存储在 `registry/projects.yaml` 中，将标签存储在 `registry/tags.yaml` 中，并将生成的文档存储在 `README.md` 和 `docs/` 中。

## 收录来源

如果用户提到 `todo.md`，请先读取该文件并提取 GitHub URL。将空行视为分隔符，而不是错误。按顺序处理各仓库，因为注册表写入不支持并发安全。

如果用户直接提供 URL，请将每个 GitHub URL 规范化为 `owner/repo`，然后继续执行相同的工作流。

在更改文件之前，检查本地状态：

```powershell
Get-ChildItem -Force
rg --files
git status --short
```

如果该目录不是 Git 仓库，请继续操作，但不要基于 git 差异作出假设。

## 仓库发现

对于每个待收录的仓库，请在下载前选择一个稳定的本地目标名称：

- 当上游仓库名称足够明确时，优先使用该名称，例如 `kami`。
- 当仓库名称较为通用时，添加所有者或用途信息，例如使用 `mattpocock-skills` 而不是 `skills`。
- 仅当现有目标明确来自同一来源时才复用它。

检查它是否已存在：

```powershell
Test-Path libraries\<target-name>
rg '"id": "<target-name>"' registry\projects.yaml
python scripts\list_skills.py --name <target-name> --skills
```

发现上游技能路径：

```powershell
gh api repos/<owner>/<repo>/git/trees/<ref>?recursive=1 --jq '.tree[].path' | rg '(^|/)SKILL\.md$'
```

选择能够保留有用技能上下文的最小源路径：

- 当仓库根目录包含安装文档、脚本、插件元数据或应当一起保留的多个技能区域时，使用 `.`。
- 当所有预期技能都位于 `skills` 中且不需要根目录上下文时，使用 `skills`。
- 当只应跟踪一个技能时，使用具体的技能目录。

如果不确定，应优先保留仓库上下文，避免提取范围过窄。

## 添加仓库

对于普通的 GitHub 目录收录，请先尝试使用 `scripts/add_skill.py`：

```powershell
python scripts\add_skill.py https://github.com/<owner>/<repo> --path <source-path> --target <target-name> --tag <tag1> --tag <tag2>
```

如果 GitHub API 下载超时或留下不完整的临时目录，请在确认失败的临时目录位于 `libraries/` 下之后，仅删除该目录：

```powershell
$tmp = Resolve-Path libraries\.<target-name>.tmp -ErrorAction SilentlyContinue
if ($tmp -and $tmp.Path.StartsWith((Resolve-Path libraries).Path)) {
  Remove-Item -LiteralPath $tmp.Path -Recurse -Force
}
```

然后，当需要跟踪整个仓库时，回退到浅克隆：

```powershell
git clone --depth 1 https://github.com/<owner>/<repo>.git libraries\<target-name>
python scripts\scan_skills.py
```

对于大型仓库或在多个技能目录下包含大量文件的仓库，尤其应使用浅克隆。克隆后，`scan_skills.py` 会读取 `.git/config` 并记录 GitHub 来源。

## 类别和标签

除非用户明确要求或清楚地暗示需要一个新的持久类别，否则请使用现有类别。

添加类别时：

1. 将其添加到 `scripts/skillhub_common.py` 中的 `CATEGORY_LABELS`。
2. 向 `CATEGORY_KEYWORDS` 添加有用的关键词。
3. 将所有新标签添加到 `DEFAULT_TAGS`、`TAG_KEYWORDS` 和 `registry/tags.yaml`。
4. 锁定必须保留在新类别中的项目：

```json
"category": "<category-id>",
"category_locked": true
```

锁定非常重要，因为后续刷新注册表时会再次推断类别，除非设置了 `category_locked`。

避免创建不存在于 `registry/tags.yaml` 中的项目标签。优先使用 `docs`、`frontend`、`pdf`、`workflow`、`coding`、`data`、`image` 和 `automation` 等现有标签；仅当仓库专用的新标签具有可复用性时才创建它们。

## 提取和文档

添加所有项目并确认分类正确后，提取可安装的技能。

对于通过 `add_skill.py` 导入的项目，通常只需提取新项目：

```powershell
python scripts\extract_skills.py --project <project-id>
```

对于浅克隆回退方案或批量处理 `todo.md` 的收录任务，当项目数量适中时，可以重新构建所有提取出的技能：

```powershell
python scripts\extract_skills.py
```

然后重新生成自动生成的文档：

```powershell
python scripts\generate_docs.py
```

## 验证

在报告完成之前，运行以下检查：

```powershell
python -m json.tool registry\projects.yaml > $null
python -m json.tool registry\tags.yaml > $null
python scripts\list_skills.py --name <target-name> --skills
python scripts\list_skills.py --category <category-id> --skills
```

还需验证：

- `libraries/` 下没有残留失败的临时目录。
- 每个新项目在 `libraries/<project-id>/` 下都有预期的源代码快照。
- 每个提取出的技能都存在于 `extracted-skills/<project-id>/` 下。
- `README.md`、`docs/index.md` 和 `docs/by-category.md` 中提到了新项目。
- `registry/projects.yaml` 未指向缺失的 `libraries/<project-id>` 目录。

使用 `rg` 进行针对性检查：

```powershell
rg '<project-id>|<category-label>' README.md docs\by-category.md docs\index.md
```

如果收录来源是 `todo.md`，除非用户已要求清理，否则请在删除条目前先征得同意。如果用户要求清理，则只删除已成功导入的 URL。

## 报告

在最终回复中包括：

- 已添加的项目 ID 和技能数量。
- 创建的任何新类别或标签。
- 更新的主要文件。
- 已通过的验证命令。
- 任何值得说明的重试或限制，例如暂时性的 GitHub API 故障或浅克隆回退。
