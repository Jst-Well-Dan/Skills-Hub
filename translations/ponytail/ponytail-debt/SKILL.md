<!-- source-sha256: c84fba75f0ca12bfe83f9a78ea02fd125c5dd3f1fbb18124105a489937f284e6 -->
---
name: ponytail-debt
description: >
  将代码库中的每一条 `ponytail:` 注释汇总到技术债台账中，从而跟踪
  ponytail 有意留下的捷径和延期事项，而不是让它们腐化成“以后就等于永远不做”。
  当用户说“ponytail 技术债”、“/ponytail-debt”、“ponytail 延期了什么”、
  “列出捷径”、“ponytail 台账”或“我们标记了哪些以后再做的事项”时使用。
  一次性报告，不做任何更改。
---

每个有意采用的 ponytail 捷径都会用 `ponytail:` 注释标记，并注明其上限和升级路径。
此操作会将它们汇总到一个台账中，防止延期事项悄无声息地变成永久搁置。

## 扫描

在仓库中 grep 注释标记，跳过 `node_modules`、`.git` 和构建输出：

`grep -rnE '(#|//) ?ponytail:' .`  （如果你的技术栈使用其他注释前缀，请添加它们）

每个匹配项对应台账中的一行。注释前缀可避免仅仅提到此约定的普通文本被收入台账。

## 输出

每个标记占一行，并按文件分组：

`<file>:<line>, <简化了什么>. 上限：<注明的限制>. 升级：<重新评估的触发条件>.`

约定格式为 `ponytail: <ceiling>, <upgrade path>`，因此直接从注释中提取上限和
触发条件。还想为每行添加负责人？请加上 `git blame -L<line>,<line>`。

标记腐化风险：任何未注明升级路径或触发条件的 `ponytail:` 注释都添加
`no-trigger` 标签，这些就是会悄无声息地腐化的项目。

最后以 `<N> 个标记，<M> 个没有触发条件。` 结尾。未找到任何内容时：
`没有 ponytail: 技术债。台账干净。`

## 边界

仅执行读取和报告，不做任何更改。如需持久保存，请提出要求，届时会将台账写入文件
（例如 `PONYTAIL-DEBT.md`）。一次性操作。使用“stop ponytail-debt”或
“normal mode”可恢复原模式。
