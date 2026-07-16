<!-- source-sha256: 44ed8107977ad22e7eadbab3ba2b6df7c03cb8f448db6cc926dcc8227e45cb95 -->
---
name: autoreview
description: 在进行非平凡的代码编辑、分支或 PR 工作或提交后，使用 autoreview 辅助工具执行结构化收尾代码审查。当用户要求 autoreview、Codex 审查、Claude 审查、第二模型审查，或要求在提交、交付、合并或发布前进行最终审查时使用。
---

# 自动审查

运行捆绑的结构化审查辅助工具作为收尾检查。这是代码审查，而不是 Guardian `auto_review` 审批路由。

来源归属：

- 改编自 OpenClaw 的 `autoreview` skill：https://github.com/openclaw/agent-skills/blob/main/skills/autoreview/SKILL.md
- 要求注明的来源：https://x.com/steipete/status/2059453909819654554

未设置引擎时，默认使用 Codex 审查。它通常能提供最佳的审查结果，并应继续作为常规的最终收尾引擎。

适用场景：

- 用户要求 Codex 审查 / Claude 审查 / autoreview / 第二模型审查
- 完成非平凡的代码编辑后、最终回复/提交/交付前
- 修复后审查本地分支或 PR 分支

## 契约

- 将审查输出视为建议。绝不要盲目应用。
- 通过阅读真实代码路径和相邻文件来验证每一项发现。
- 当发现依赖外部行为时，阅读依赖项的文档/源码/类型。
- 拒绝不切实际的边缘情况、推测性风险、大范围重写，以及会使代码库过度复杂的修复。
- 优先在正确的归属边界进行小范围修复；除非重构能明确改善该类缺陷，否则不要重构。
- 持续进行，直到结构化审查不再返回已接受/可操作的发现。
- 如果审查触发的修复更改了代码，请重新运行针对性测试，并重新运行结构化审查辅助工具。
- 对于安全审计抑制变更，验证已接受的发现仍可审计：被抑制的发现保留在结构化输出中，活动输出保留不可抑制的抑制提示，汇总发现不能隐藏无关的活动风险。
- 绝不要切换或覆盖所请求的审查引擎/模型。如果审查遇到模型容量限制，请使用相同的引擎/模型将同一命令重试几次。
- 对大型包保持耐心。模型调用处于活动状态时，结构化审查最长可能需要 30 分钟，尤其是在使用 Codex 工具或 Web 搜索时。
- 将 `review still running: ... elapsed=... pid=...` 之类的心跳行视为正常进展，而不是卡死。只要心跳仍在推进，就让辅助工具继续运行。当实时引擎文本有用时传入 `--stream-engine-output`；Codex 和 Claude 会过滤工具/文件交互信息，其他引擎则原样传递输出。
- 不要仅仅因为审查已静默 2-5 分钟，或仍处于 30 分钟窗口内，就终止审查。只有在多次未收到预期心跳、超过 30 分钟或子进程明显失败后才检查进程；应优先让同一个辅助工具命令完成。
- 工具在审查模式中很有用。辅助工具默认允许只读检查工具和 Web 搜索，以便审查者核查依赖契约、上游文档和当前行为。
- 始终包含安全视角，但不应因此妨碍合理功能。只有当变更造成具体、可操作的风险，或移除了重要的安全检查时，才报告安全发现。
- 对于回归来源追溯，请区分各个角色：被追责代码的作者、被追责 PR 的作者、PR 合并者/提交者、当前 PR 作者，以及 PR/日期。如果无法追溯到被追责的 PR，请使用被追责的提交作为来源：提交 SHA、日期和作者用户名。不要猜测合并者，也不要将缺失的 PR 元数据表述为一项单独发现。
- 如果被追责的 PR 是由 `clawsweeper[bot]` 或其他自动化工具合并的，请尽可能识别人工触发者。先检查时间线/评论；如果受到速率限制，请使用 gitcrawl/缓存或公开 PR HTML。查找启用自动合并的维护者命令，例如 `@clawsweeper automerge`、`/landpr`，或标签/状态评论。报告 `automerge triggered by @login`；如果未找到，则说明触发者未知。
- 不要在审查内部调用内置的 `codex review`、嵌套审查者或审查者小组。辅助工具会构建一个包，调用一个选定的引擎，验证一个结构化结果，然后停止。
- 一旦辅助工具以 0 退出且没有已接受/可操作的发现，就立即停止。不要仅仅为了获得更好看的“干净”提示行、第二意见或更清晰的收尾措辞而额外运行一次审查。
- 即使底层 Codex CLI 输出很简短，也应将辅助工具成功退出且不存在可操作发现视为干净的审查结果。
- 多审查者小组仅可按需启用。仅在明确要求或风险足以证明额外开销合理时使用；主代理仍须在修复前验证每一项已接受的发现。
- 如果以符合预期/不值得修复为由拒绝某项发现，只有当简短的行内代码注释能够说明未来审查者应当了解的真实不变量或归属决策时，才添加该注释。
- 如果 `gh`/Gitcrawl 报告 `database disk image is malformed`，请运行一次 `gitcrawl doctor --json`，让便携式缓存在重试审查前完成修复；除非修复失败且时效性要求实时访问 GitHub，否则不要绕过该垫片。
- 如果 Gitcrawl 报告便携式清单不匹配、源/运行时数据库健康错误，或便携式存储检出过期，请运行 `gitcrawl doctor --json` 并检查 `source_db_health`、`runtime_db_health` 和 `portable_store_status`，然后再考虑回退到实时 GitHub。
- 不要仅为审查而推送。只有当用户要求推送/交付/更新 PR 时才推送。

## 选择目标

本地脏工作区：

```bash
<autoreview-helper> --mode local
```

仅当补丁确实以未暂存/已暂存/未跟踪状态存在于当前检出中时使用此模式。对于已提交、已推送或 PR 工作，应让辅助工具指向提交或分支差异；不要仅仅因为辅助工具文档首先提到脏工作区，就强制使用 `--mode local` / `--uncommitted`。干净的本地审查只能证明不存在本地补丁。

分支/PR 工作：

```bash
<autoreview-helper> --mode branch --base origin/main
```

可选审查上下文是一等输入：

```bash
<autoreview-helper> --mode branch --base origin/main --prompt-file /tmp/review-notes.md --dataset /tmp/evidence.json
```

如果存在打开的 PR，请使用它的实际基础分支：

```bash
base=$(gh pr view --json baseRefName --jq .baseRefName)
<autoreview-helper> --mode branch --base "origin/$base"
```

已提交的单项变更：

```bash
<autoreview-helper> --mode commit --commit HEAD
```

或者使用该辅助工具：

```bash
/Users/steipete/Projects/agent-scripts/skills/autoreview/scripts/autoreview --mode commit --commit HEAD
```

对于 `main` 上已经落地或已经推送的工作，请使用提交审查。推送后，使用干净的 `main` 与 `origin/main` 比较通常会得到空差异。对于较小的提交栈，请明确逐个审查提交，或在合并前使用 `--base` 审查分支。

## 并行收尾

如果格式化可能改变行位置，请先格式化。之后可以并行运行测试和审查：

```bash
scripts/autoreview --parallel-tests "<focused test command>"
```

权衡：测试可能迫使代码发生变更，使审查结果过时。如果测试或审查导致代码编辑，请重新运行受影响的测试，并重新运行审查，直到不再有已接受/可操作的发现。该次重运行干净退出后即停止；不要再花费一个漫长的审查周期进行重复确认。

## 审查者小组

针对一个冻结的包运行多个审查者：

```bash
<autoreview-helper> --reviewers codex,claude
```

除非 `--engine` 更改第一个审查者，否则 `--panel` 是 Codex 加 Claude 的简写：

```bash
<autoreview-helper> --panel
```

明确设置审查者模型和思考/投入程度：

```bash
<autoreview-helper> --reviewers codex,claude --model codex=gpt-5.1 --thinking codex=high --model claude=sonnet --thinking claude=max
```

也支持内联语法：

```bash
<autoreview-helper> --reviewers codex:gpt-5.1:high,claude:sonnet:max
```

Codex 将思考程度映射到 `model_reasoning_effort`，并接受 `low`、`medium`、`high` 或 `xhigh`。Claude 将思考程度映射到 `--effort`，并且还接受 `max`。没有真正思考调节参数的引擎会拒绝 `--thinking`。

## 上下文效率

直接运行辅助工具，使目标选择、引擎选择、结构化验证和退出状态都保持在同一条路径中。如果输出嘈杂，请在辅助工具返回后总结其已完成的输出；不要要求另一个代理或审查者重新运行审查。

## 辅助工具

OpenClaw 仓库本地辅助工具：

```bash
.agents/skills/autoreview/scripts/autoreview --help
```

`agent-scripts` 检出中的辅助工具：

```bash
skills/autoreview/scripts/autoreview --help
```

来自 `agent-scripts` 的全局辅助工具：

```bash
~/.codex/skills/agent-scripts/autoreview/scripts/autoreview --help
```

如果从 `agent-scripts` 安装，路径为：

```bash
/Users/steipete/Projects/agent-scripts/skills/autoreview/scripts/autoreview --help
```

该辅助工具：

- 优先选择本地脏变更
- 否则，如果 `gh pr view` 可用，则使用当前 PR 的基础分支
- 否则，对非 main 分支使用 `origin/main`
- 支持 `--engine codex`、`claude`、`droid` 和 `copilot`；默认值为 `AUTOREVIEW_ENGINE` 或 `codex`；未设置任何值时，Codex 应继续作为默认值
- 对已提交的工作使用 `--mode commit --commit <ref>`，尤其是在变更落地后的干净 `main` 上
- 对 PR/分支工作，应保留为 `--mode auto` 或强制使用 `--mode branch`；提交后不要强制使用 `--mode local`
- 除非设置了 `--output`、`--json-output` 或实时流式引擎 stderr，否则只写入 stdout
- 支持 `--dry-run`、`--parallel-tests`、`--prompt`、`--prompt-file`、`--dataset`、`--no-tools`、`--no-web-search` 和提交引用
- 支持通过 `--stream-engine-output` 或 `AUTOREVIEW_STREAM_ENGINE_OUTPUT=1` 获取实时引擎文本，同时保留结构化验证；Codex 和 Claude 会隐藏工具/文件事件详情，输出紧凑的活动摘要，并在轮次完成时报告用量
- 支持通过 `--panel` / `--reviewers` 按需启用审查者小组，以及按引擎设置 `--model` 和 `--thinking`
- 在选定的 CLI 支持时，默认允许只读工具和 Web 搜索；在提示词中禁止嵌套审查；Codex 通过 `codex exec` 在只读沙箱中运行，并输出结构化结果
- 等待选定的审查引擎时，会按长时间运行间隔将 `review still running: <engine> elapsed=<seconds>s pid=<pid>` 打印到 stderr，除非近期已经显示过流式输出或紧凑的 Codex 活动
- 当选定的审查命令以 0 退出时，打印 `autoreview clean: no accepted/actionable findings reported`
- 存在已接受/可操作的发现时以非零状态退出

## 最终报告

包括：

- 使用的审查命令
- 运行的测试/验证
- 接受/拒绝的发现，以及简短原因
- 最后一次辅助工具/审查运行得到的干净审查结果，或有意识地拒绝剩余发现的原因

不要仅为改进最终报告措辞而再次运行审查。如果最后一次辅助工具运行以 0 退出且未产生已接受/可操作的发现，请将该次运行如实报告为干净。
