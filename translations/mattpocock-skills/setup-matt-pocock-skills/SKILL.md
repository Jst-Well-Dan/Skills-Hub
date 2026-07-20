<!-- source-sha256: def265a8b15ffb8afc3f335d69e175ba9a7fe3991218984b0e49e8345cde3b20 -->
---
name: setup-matt-pocock-skills
description: 为此仓库配置工程技能——设置其议题跟踪器、分流标签词汇和领域文档布局。在首次使用其他工程技能之前运行一次。
disable-model-invocation: true
---

# 设置 Matt Pocock 的技能

搭建工程技能所依赖的每仓库配置：

- **议题跟踪器**——议题存放的位置（默认为 GitHub；同时原生支持本地 Markdown）
- **分流标签**——五种标准分流角色所使用的字符串
- **领域文档**——`CONTEXT.md` 和 ADR 的存放位置，以及读取它们的使用方规则

这是一个由提示驱动的技能，而非确定性脚本。先探索，展示你发现的内容，与用户确认，然后写入。

## 流程

### 1. 探索

查看当前仓库，了解其初始状态。读取所有已有内容；不要想当然：

- `git remote -v` 和 `.git/config`——这是 GitHub 仓库吗？是哪个仓库？
- 仓库根目录下的 `AGENTS.md` 和 `CLAUDE.md`——二者是否存在？其中是否已有 `## Agent skills` 章节？
- 仓库根目录下的 `CONTEXT.md` 和 `CONTEXT-MAP.md`
- `docs/adr/` 以及所有 `src/*/docs/adr/` 目录
- `docs/agents/`——此技能之前生成的输出是否已经存在？
- `.scratch/`——表明已经在使用本地 Markdown 议题跟踪器约定
- 是否安装了 `triage` 技能？（与此技能同级的 `triage` 技能文件夹，或你的可用技能中包含 `triage`。）这决定是否运行 B 节。
- Monorepo 信号——`pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 字段，或包含自身 `src/` 的非空 `packages/*`。仅真正的大型多包仓库才会存在这些信号；缺少这些信号意味着单上下文，而几乎所有仓库都是如此。

### 2. 展示发现并提问

总结已有内容和缺失内容。然后依次进行各节——每次一个章节、一个回答，之后再进入下一节。

每一节都先给出推荐答案，让用户可以只用一个词接受。只有当选择确实会产生分支时，才给出一行说明；如果探索结果已经确定答案，则完全跳过该节（未安装 `triage` 时跳过 B 节；不存在 monorepo 时跳过 C 节）。

**A 节——议题跟踪器。**

> 说明：“议题跟踪器”是此仓库中存放议题的位置。`to-tickets`、`triage`、`to-spec` 和 `qa` 等技能会读取和写入其中——它们需要知道应该调用 `gh issue create`、在 `.scratch/` 下写入 Markdown 文件，还是遵循你描述的其他工作流。请选择你实际用于跟踪此仓库工作的地方。

默认倾向：这些技能是为 GitHub 设计的。如果 `git remote` 指向 GitHub，请推荐 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自托管主机），请推荐 GitLab。否则（或用户另有偏好），提供以下选项：

- **GitHub**——议题存放在仓库的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab**——议题存放在仓库的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 Markdown**——议题以文件形式存放在此仓库的 `.scratch/<feature>/` 下（适合个人项目或没有远程仓库的仓库）
- **其他**（Jira、Linear 等）——请用户用一段话描述工作流；技能会将其记录为自由格式文本

将选择记录在 `docs/agents/issue-tracker.md` 中。GitHub 和 GitLab 模板带有一个“将 PR 作为请求入口”标志，默认为**关闭**——保持关闭且不要提及它；希望将外部 PR 纳入分流队列的用户之后可以自行在文件中开启该标志。

**B 节——分流标签词汇。** 如果未安装 `triage` 技能（探索阶段已经得知），则完全跳过本节——未安装的技能不需要标签。

如果已安装，只询问一个问题：

> 是否要保留默认分流标签？（推荐：**是**）

默认值是五种标准角色，每个标签字符串均与其名称相同：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。如果回答**是**，按原样写入。仅当用户回答否时——通常是因为其跟踪器已使用其他名称（例如用 `bug:triage` 表示 `needs-triage`）——才收集覆盖值，使 `triage` 使用已有标签，而非创建重复标签。

**C 节——领域文档。** 默认为**单上下文**——仓库根目录下使用一个 `CONTEXT.md` 和 `docs/adr/`。这适用于几乎所有仓库；无需询问，直接写入。

仅当探索发现 monorepo 信号时，才提供**多上下文**选项——使用根目录下的 `CONTEXT-MAP.md` 指向各上下文的 `CONTEXT.md` 文件。然后确认用户想要哪种布局。

### 3. 确认并编辑

向用户展示以下内容的草稿：

- 要添加到所编辑的 `CLAUDE.md` / `AGENTS.md` 中的 `## Agent skills` 区块（选择规则见第 4 步）
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 和 `docs/agents/triage-labels.md` 的内容（最后一个仅在安装了 `triage` 时提供）

允许用户在写入前进行编辑。

### 4. 写入

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则，如果 `AGENTS.md` 存在，编辑它。
- 如果二者均不存在，询问用户要创建哪一个——不要替用户选择。

当 `CLAUDE.md` 已存在时，绝不要创建 `AGENTS.md`（反之亦然）——始终编辑已经存在的那个文件。

如果所选文件中已存在 `## Agent skills` 区块，则原地更新其内容，而非追加重复区块。不要覆盖用户对周边章节的编辑。

区块内容：

```markdown
## Agent skills

### Issue tracker

[一行概述议题的跟踪位置]。参见 `docs/agents/issue-tracker.md`。

### Triage labels

[一行概述标签词汇]。参见 `docs/agents/triage-labels.md`。

### Domain docs

[一行概述布局——“单上下文”或“多上下文”]。参见 `docs/agents/domain.md`。
```

仅当安装了 `triage` 且运行了 B 节时，才包含 `### Triage labels` 子区块并写入 `docs/agents/triage-labels.md`。否则两者均省略。

然后以此技能文件夹中的种子模板为起点写入文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md)——GitHub 议题跟踪器
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)——GitLab 议题跟踪器
- [issue-tracker-local.md](./issue-tracker-local.md)——本地 Markdown 议题跟踪器
- [triage-labels.md](./triage-labels.md)——标签映射（仅当安装了 `triage` 时）
- [domain.md](./domain.md)——领域文档使用方规则和布局

对于“其他”议题跟踪器，请根据用户的描述从头编写 `docs/agents/issue-tracker.md`。

### 5. 完成

告知用户设置已完成，并说明哪些工程技能现在会读取这些文件。提及他们之后可以直接编辑 `docs/agents/*.md`——只有在想要切换议题跟踪器或从头重新开始时，才需要再次运行此技能。
