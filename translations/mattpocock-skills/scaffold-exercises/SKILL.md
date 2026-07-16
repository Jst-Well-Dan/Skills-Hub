<!-- source-sha256: 75f5c9d771606fb9762f16522efc954df11c324f87148d8ff069bce166257de9 -->
---
name: scaffold-exercises
description: 创建包含章节、习题、解答和讲解材料且能通过代码检查的习题目录结构。当用户想要搭建习题、创建习题存根或设置新的课程章节时使用。
---

# 搭建习题

创建能够通过 `pnpm ai-hero-cli internal lint` 的习题目录结构，然后使用 `git commit` 提交。

## 目录命名

- **章节**：位于 `exercises/` 内的 `XX-section-name/`（例如 `01-retrieval-skill-building`）
- **习题**：位于章节内的 `XX.YY-exercise-name/`（例如 `01.03-retrieval-with-bm25`）
- 章节编号 = `XX`，习题编号 = `XX.YY`
- 名称使用短横线命名法（小写字母、短横线）

## 习题变体

每道习题至少需要包含以下子文件夹之一：

- `problem/` - 包含 TODO 的学员工作区
- `solution/` - 参考实现
- `explainer/` - 概念性材料，不包含 TODO

创建存根时，除非计划另有指定，否则默认使用 `explainer/`。

## 必需文件

每个子文件夹（`problem/`、`solution/`、`explainer/`）都需要一个 `readme.md`，且该文件：

- **不能为空**（必须包含实际内容，即使只有一行标题也可以）
- 不能包含失效链接

创建存根时，创建一个包含标题和描述的最简 readme：

```md
# 习题标题

在此填写描述
```

如果子文件夹包含代码，还需要一个 `main.ts`（超过 1 行）。但对于存根，仅包含 readme 的习题即可。

## 工作流程

1. **解析计划** - 提取章节名称、习题名称和变体类型
2. **创建目录** - 对每个路径执行 `mkdir -p`
3. **创建 readme 存根** - 在每个变体文件夹中创建一个带标题的 `readme.md`
4. **运行代码检查** - 使用 `pnpm ai-hero-cli internal lint` 进行验证
5. **修复所有错误** - 反复处理，直到代码检查通过

## 代码检查规则摘要

代码检查器（`pnpm ai-hero-cli internal lint`）会检查：

- 每道习题都包含子文件夹（`problem/`、`solution/`、`explainer/`）
- 至少存在 `problem/`、`explainer/` 或 `explainer.1/` 之一
- 主子文件夹中存在非空的 `readme.md`
- 不存在 `.gitkeep` 文件
- 不存在 `speaker-notes.md` 文件
- readme 中不存在失效链接
- readme 中不存在 `pnpm run exercise` 命令
- 除非子文件夹仅包含 readme，否则每个子文件夹都需要 `main.ts`

## 移动/重命名习题

重新编号或移动习题时：

1. 使用 `git mv`（而不是 `mv`）重命名目录，以保留 Git 历史记录
2. 更新数字前缀以维持顺序
3. 移动后重新运行代码检查

示例：

```bash
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

## 示例：根据计划创建存根

给定如下计划：

```
章节 05：记忆技能培养
- 05.01 记忆简介
- 05.02 短期记忆（讲解材料 + 问题 + 解答）
- 05.03 长期记忆
```

创建：

```bash
mkdir -p exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer
mkdir -p exercises/05-memory-skill-building/05.02-short-term-memory/{explainer,problem,solution}
mkdir -p exercises/05-memory-skill-building/05.03-long-term-memory/explainer
```

然后创建 readme 存根：

```
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# 记忆简介"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# 长期记忆"
```
