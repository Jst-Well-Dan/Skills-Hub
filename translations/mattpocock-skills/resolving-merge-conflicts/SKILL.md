<!-- source-sha256: c7c9ba81362a786aac05d2223123bf1bd2f8a99c3243a72882ede9c68bedfb24 -->
---
name: resolving-merge-conflicts
description: "当你需要解决正在进行的 git merge/rebase 冲突时使用。"
---

1. **查看 merge/rebase 的当前状态。**检查 git 历史记录和发生冲突的文件。

2. **查找每个冲突的主要来源。**深入理解每项更改的原因及其原始意图。阅读 commit 消息，检查 PR，并查看原始 issue/ticket。

3. **解决每个冲突区块。**尽可能保留双方的意图。如果两者不兼容，请选择符合 merge 既定目标的一方，并注明取舍。**不要**创造新行为。始终解决冲突；绝不使用 `--abort`。

4. 找出项目的**自动化检查**并运行它们——通常依次运行 typecheck、tests 和 format。修复 merge 引入的所有问题。

5. **完成 merge/rebase。**暂存所有内容并 commit。如果正在执行 rebase，请继续 rebase 流程，直到所有 commit 都完成 rebase。
