<!-- source-sha256: a85441f31decd5705ade6b526206d60be129dbe926251c67213fe1649da5f197 -->
---
name: setup-matt-pocock-skills
description: 为此仓库配置工程技能——设置问题跟踪器、分类标签词汇和领域文档布局。在首次使用其他工程技能之前运行一次。
disable-model-invocation: true
---

# 设置 Matt Pocock 的技能

搭建工程技能所依赖的每仓库配置：

- **问题跟踪器**——问题存放的位置（默认使用 GitHub；同时开箱即用地支持本地 Markdown）
- **分类标签**——用于五种规范分类角色的字符串
- **领域文档**——`CONTEXT.md` 和 ADR 的存放位置，以及读取它们的消费方规则

这是一个由提示驱动的技能，而不是确定性脚本。先探索，展示发现的内容，向用户确认，然后再写入。

## 流程

### 1. 探索

查看当前仓库，了解其初始状态。读取实际存在的内容；不要作任何假设：

- `git remote -v` 和 `.git/config`——这是 GitHub 仓库吗？具体是哪一个？
- 仓库根目录中的 `AGENTS.md` 和 `CLAUDE.md`——其中任意一个是否存在？其中是否已经有 `## Agent skills` 章节？
- 仓库根目录中的 `CONTEXT.md` 和 `CONTEXT-MAP.md`
- `docs/adr/` 以及所有 `src/*/docs/adr/` 目录
- `docs/agents/`——此技能之前生成的输出是否已经存在？
- `.scratch/`——表明已经在使用本地 Markdown 问题跟踪器约定

### 2. 展示发现并询问

总结哪些内容存在、哪些内容缺失。然后引导用户**逐一**完成三个决定——展示一个部分，取得用户的回答，再进入下一部分。不要一次性抛出全部三个部分。

假设用户不了解这些术语的含义。每个部分都以简短说明开头（它是什么、这些技能为什么需要它，以及选择不同选项会带来什么变化）。然后展示可选项和默认选项。

**A 部分——问题跟踪器。**

> 说明：“问题跟踪器”是此仓库中存放问题的位置。`to-issues`、`triage`、`to-prd` 和 `qa` 等技能会对其进行读写——它们需要知道应该调用 `gh issue create`、在 `.scratch/` 下写入 Markdown 文件，还是遵循你描述的其他工作流。请选择你实际用于跟踪此仓库工作的地方。

默认倾向：这些技能是为 GitHub 设计的。如果 `git remote` 指向 GitHub，则建议使用 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自托管主机），则建议使用 GitLab。否则（或如果用户有其他偏好），提供以下选项：

- **GitHub**——问题存放在仓库的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab**——问题存放在仓库的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 Markdown**——问题以文件形式存放在此仓库的 `.scratch/<feature>/` 下（适合个人项目或没有远程仓库的项目）
- **其他**（Jira、Linear 等）——请用户用一段话描述工作流；该技能会将其记录为自由格式文本

当且仅当用户选择了 **GitHub** 或 **GitLab** 时，提出一个后续问题：

> 说明：开源仓库经常以拉取请求而不仅仅是问题的形式接收功能请求——PR 是附带代码的问题。如果启用此选项，`/triage` 会将*外部* PR 纳入同一队列，并使用与问题相同的标签和状态对其进行处理（协作者正在进行的 PR 不受影响）。如果 PR 不是你接收请求的渠道，请保持关闭。

- **将 PR 作为请求渠道**——是 / 否（默认：否）。将答案记录在 `docs/agents/issue-tracker.md` 中。对于本地 Markdown 和其他跟踪器，跳过此问题——它们没有 PR。

**B 部分——分类标签词汇。**

> 说明：当 `triage` 技能处理新收到的问题时，会让它在一个状态机中流转——需要评估、等待报告者回复、可由 AFK 智能体接手、可由人工接手或不予修复。为此，它需要应用与你*实际配置*的字符串相匹配的标签（或问题跟踪器中的等效项）。如果仓库已经使用不同的标签名称（例如使用 `bug:triage` 而不是 `needs-triage`），请在此处进行映射，以便该技能应用正确的标签，而不是创建重复标签。

五种规范角色：

- `needs-triage`——需要维护者评估
- `needs-info`——等待报告者回复
- `ready-for-agent`——信息完整，已准备好由 AFK 智能体处理（智能体无需任何人工上下文即可接手）
- `ready-for-human`——需要人工实现
- `wontfix`——不会采取行动

默认值：每种角色的字符串与其名称相同。询问用户是否要覆盖其中任何一项。如果其问题跟踪器中没有现有标签，使用默认值即可。

**C 部分——领域文档。**

> 说明：某些技能（`improve-codebase-architecture`、`diagnosing-bugs`、`tdd`）会读取 `CONTEXT.md` 文件来了解项目的领域语言，并从 `docs/adr/` 读取过去的架构决策。它们需要知道仓库是只有一个全局上下文，还是有多个上下文（例如，前端和后端上下文相互独立的单体仓库），以便在正确的位置查找。

确认布局：

- **单上下文**——仓库根目录中有一个 `CONTEXT.md` 和一个 `docs/adr/`。大多数仓库使用这种布局。
- **多上下文**——根目录中的 `CONTEXT-MAP.md` 指向各上下文的 `CONTEXT.md` 文件（通常用于单体仓库）。

### 3. 确认并编辑

向用户展示以下内容的草稿：

- 要添加到所编辑的 `CLAUDE.md` / `AGENTS.md` 中的 `## Agent skills` 块（选择规则见步骤 4）
- `docs/agents/issue-tracker.md`、`docs/agents/triage-labels.md`、`docs/agents/domain.md` 的内容

允许用户在写入前进行编辑。

### 4. 写入

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，则编辑它。
- 否则，如果 `AGENTS.md` 存在，则编辑它。
- 如果两者都不存在，请询问用户要创建哪一个——不要替用户选择。

当 `CLAUDE.md` 已经存在时，绝不要创建 `AGENTS.md`（反之亦然）——始终编辑已经存在的那个文件。

如果所选文件中已经存在 `## Agent skills` 块，请就地更新其内容，而不是追加重复内容。不要覆盖用户对周围章节所做的编辑。

该块：

```markdown
## Agent skills

### Issue tracker

[用一行总结问题的跟踪位置，以及外部 PR 是否作为分类处理渠道]。参见 `docs/agents/issue-tracker.md`。

### Triage labels

[用一行总结标签词汇]。参见 `docs/agents/triage-labels.md`。

### Domain docs

[用一行总结布局——“单上下文”或“多上下文”]。参见 `docs/agents/domain.md`。
```

然后，以此技能文件夹中的种子模板为起点，写入三个文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md)——GitHub 问题跟踪器
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)——GitLab 问题跟踪器
- [issue-tracker-local.md](./issue-tracker-local.md)——本地 Markdown 问题跟踪器
- [triage-labels.md](./triage-labels.md)——标签映射
- [domain.md](./domain.md)——领域文档消费方规则和布局

对于“其他”问题跟踪器，使用用户的描述从头编写 `docs/agents/issue-tracker.md`。

### 5. 完成

告知用户设置已完成，并说明哪些工程技能现在会读取这些文件。提醒用户以后可以直接编辑 `docs/agents/*.md`——只有当他们想要切换问题跟踪器或从头重新开始时，才需要重新运行此技能。
