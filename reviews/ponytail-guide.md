---
{"title":"Ponytail Skills 系统学习与使用指南","type":"review","related_projects":["ponytail"]}
---
# Ponytail Skills 系统学习与使用指南

Ponytail 是一组面向软件开发的“反过度工程化”技能。它不鼓励草率编码，而是要求先理解完整问题，再选择能够正确工作的最简单方案。

> 一句话定位：先判断是否需要实现，再依次考虑复用现有代码、标准库、平台原生能力、现有依赖和最小实现。

## 1. Skill 组成

Ponytail 包含 6 个 skill：一个持续生效的编码模式，以及五个一次性工具。

| Skill | 类型 | 主要作用 |
|---|---|---|
| `ponytail` | 持续模式 | 在编码任务中强制选择最简单、最少依赖、最短的可靠方案 |
| `ponytail-review` | 一次性报告 | 检查当前 diff 或局部改动中的过度设计 |
| `ponytail-audit` | 一次性报告 | 扫描整个仓库中的过度设计 |
| `ponytail-debt` | 一次性报告 | 收集代码中的 `ponytail:` 简化标记，形成技术债清单 |
| `ponytail-gain` | 一次性展示 | 展示 Ponytail 发布的基准测试收益 |
| `ponytail-help` | 一次性展示 | 显示模式、命令、配置和更新方法 |

“一次性”表示执行后只输出结果，不改变后续编码行为。只有主 `ponytail` 模式会持续影响当前会话。

## 2. `ponytail`：核心编码模式

### 2.1 触发场景

它适用于编写、添加、重构、修复、评审和设计代码，以及选择库或依赖等编码任务。以下表达也会显式触发它：

- `ponytail` 或 `/ponytail`
- `be lazy`、`lazy mode`
- `simplest solution`、`minimal solution`
- `YAGNI`、`do less`、`shortest path`
- 对过度工程、样板代码、代码膨胀或不必要依赖的抱怨

它不用于一般知识、普通写作、翻译、摘要和菜谱等非编码任务。

### 2.2 最简决策阶梯

面对一个开发需求时，按顺序检查，并在第一个能够正确解决问题的位置停止：

1. 这个功能真的需要存在吗？推测性需求先不实现。
2. 代码库里已经有可以复用的 helper、类型或模式吗？
3. 标准库能够解决吗？
4. 平台原生能力能够解决吗？
5. 已安装的依赖能够解决吗？
6. 能否用一行代码完成？
7. 都不满足时，才编写最少的新代码。

例如，浏览器原生的 `<input type="date">` 能满足需求时，不应先引入日期选择器依赖。

### 2.3 Bug 修复原则

Ponytail 要求修复根因，而不是只处理报告中的表面症状：

- 修改共享函数前先查找全部调用方。
- 找到所有失败路径共同经过的位置。
- 尽量在共享位置修复一次，避免给每个调用方分别增加补丁。

因此，“最小修改”指最小的根因修复，不是最小的表面改动。

### 2.4 编码规则

- 不创建只有一个实现的接口。
- 不为一个产品创建工厂。
- 不为永远不变的值增加配置项。
- 不为“以后可能需要”提前搭建脚手架。
- 优先删除，优先直接、容易维护的实现。
- 在理解完整调用链之后，尽量减少修改文件数和代码量。
- 不为几行代码可以解决的问题增加新依赖。
- 两个标准库方案同样简短时，选择边界情况更可靠的方案。

如果采用了有明确容量上限的简化方案，需要留下限制和升级触发条件：

```python
# ponytail: global lock, use per-account locks if throughput matters
```

### 2.5 三种强度

| 模式 | 触发方式 | 行为 |
|---|---|---|
| Lite | `/ponytail lite` | 完成用户要求，同时用一行指出更简单的替代方案，由用户决定 |
| Full | `/ponytail` 或 `/ponytail full` | 默认模式，执行完整的最简决策阶梯 |
| Ultra | `/ponytail ultra` | 极端 YAGNI，删除优先，并主动质疑没有证据支持的需求 |

模式会持续到用户切换、关闭或当前会话结束。可用 `stop ponytail`、`normal mode` 或 `/ponytail off` 关闭。

### 2.6 不得简化掉的内容

Ponytail 明确禁止为了少写代码而删除：

- 信任边界上的输入校验
- 防止数据丢失的错误处理
- 安全措施
- 无障碍基础能力
- 用户明确要求的完整功能
- 真实硬件需要的校准参数

非平凡逻辑还应留下一个最小可运行检查，例如一个 `assert`、`demo()` 或很小的 `test_*.py`。简单的一行代码则不必机械增加测试。

### 2.7 输出方式

默认先给代码，再用不超过三行说明跳过了什么，以及何时才需要增加它。用户明确要求报告、教程或逐阶段讲解时，可以完整说明，不受这个简短输出限制。

## 3. `ponytail-review`：局部过度工程评审

### 3.1 触发场景

- `/ponytail-review`
- `review for over-engineering`
- `what can we delete`
- `is this over-engineered`
- `simplify review`
- “检查这次改动有没有过度设计”

它面向当前 diff、PR 或一组局部改动。

### 3.2 检查标签

| 标签 | 含义 |
|---|---|
| `delete:` | 死代码、未使用的灵活性或推测性功能，可以直接删除 |
| `stdlib:` | 手写了标准库已经提供的能力 |
| `native:` | 依赖或代码重复了平台原生能力 |
| `yagni:` | 当前不需要的抽象、配置或中间层 |
| `shrink:` | 保持逻辑不变，但可以用更少代码表达 |

每个发现只占一行，并包含位置、应删除的内容和替代方案：

```text
repo.py:L88: yagni: AbstractRepository with one implementation. Inline it until a second one exists.
```

报告最后给出 `net: -<N> lines possible.`。没有可删内容时只输出 `Lean already. Ship.`。

### 3.3 边界

它只检查复杂度，不负责正确性 Bug、安全漏洞和性能问题，也不会直接修改代码。一个最小 smoke test 或 `assert` 不应被判定为冗余。

## 4. `ponytail-audit`：全仓库过度工程审计

### 4.1 触发场景

- `/ponytail-audit`
- `audit this codebase`
- `audit for over-engineering`
- `what can I delete from this repo`
- `find bloat`
- “扫描整个项目，看看哪些代码可以删”

### 4.2 与 review 的区别

| `ponytail-review` | `ponytail-audit` |
|---|---|
| 检查当前 diff 或局部改动 | 扫描整个仓库 |
| 面向一次提交或 PR | 面向存量代码治理 |
| 按代码位置列出问题 | 按预期削减收益排序 |

审计重点包括标准库的重复实现、可由平台原生能力替代的依赖、单实现接口、单产品工厂、只转发调用的包装层、无用配置和推测性功能。

输出沿用 `delete:`、`stdlib:`、`native:`、`yagni:` 和 `shrink:` 标签，并以 `net: -<N> lines, -<M> deps possible.` 结尾。它同样只报告，不直接修改，也不检查安全、正确性和性能。

## 5. `ponytail-debt`：简化技术债清单

### 5.1 触发场景

- `/ponytail-debt`
- `ponytail debt`
- `what did ponytail defer`
- `list the shortcuts`
- `ponytail ledger`
- `what did we mark to do later`
- “列出 Ponytail 留下的技术债”

### 5.2 扫描与输出

它扫描代码注释中的 `ponytail:` 标记，并跳过 `.git`、`node_modules` 和构建输出。例如：

```javascript
// ponytail: linear scan, add an index above 100k records
```

每条记录应提取：

- 做了什么简化
- 当前方案的容量或适用上限
- 重新考虑它的触发条件
- 对应的升级路径

没有写升级触发条件的标记会增加 `no-trigger`，因为这种技术债最容易永久遗留。报告以 `<N> markers, <M> with no trigger.` 结尾；没有标记时输出 `No ponytail: debt. Clean ledger.`。

它默认只读。用户明确要求持久化时，才写成例如 `PONYTAIL-DEBT.md`；需要负责人信息时可以结合 `git blame`。

## 6. `ponytail-gain`：官方基准收益展示

### 6.1 触发场景

- `/ponytail-gain`
- `ponytail gain`
- `what does ponytail save`
- `show ponytail impact`
- `ponytail scoreboard`
- “Ponytail 能节省多少代码或成本”

### 6.2 展示内容

它显示固定的 ASCII 记分牌。文件记录的发布基准中位数为：

- 代码量降低约 `80–94%`
- 成本降低约 `47–77%`
- 速度约快 `3–6×`

这些数据来自五个日常任务和三个模型的基准测试，不是当前仓库的实际收益。

### 6.3 诚信边界

它禁止为当前仓库虚构节省行数或成本，因为没有实际写出的复杂版本就不存在可靠基线。当前仓库可以真实统计的只有 `/ponytail-debt` 收集的标记，以及 `/ponytail-audit` 发现的潜在削减项。

该 skill 只展示信息，不改文件，也不改变当前模式。

## 7. `ponytail-help`：命令帮助卡

### 7.1 触发场景

- `/ponytail-help`
- `ponytail help`
- `what ponytail commands`
- `how do I use ponytail`
- “Ponytail 有哪些命令”

### 7.2 包含内容

帮助卡汇总：

1. Lite、Full 和 Ultra 三种模式
2. 六个 skill 的作用和命令
3. 如何关闭模式
4. 如何修改默认模式
5. 如何更新插件
6. 项目文档地址

默认模式是 `full`。配置解析优先级为：

```text
环境变量 > 配置文件 > full
```

环境变量示例：

```bash
export PONYTAIL_DEFAULT_MODE=ultra
```

配置文件示例：

```json
{ "defaultMode": "lite" }
```

配置位置是 Linux/macOS 的 `~/.config/ponytail/config.json`，或 Windows 的 `%APPDATA%\ponytail\config.json`。设置为 `off` 可以关闭会话开始时的自动启用。

帮助文件还说明，不同宿主可能使用不同命令形式：Codex 使用 `@` 形式，Claude Code 和 OpenCode 使用 `/` 形式。实际可用形式取决于宿主如何安装和暴露 skill；自然语言描述也可以触发相应能力。

## 8. 快速选择

| 用户需求 | 应选择的 skill |
|---|---|
| “帮我用最简单的方式实现这个功能” | `ponytail` |
| “看看我这次提交有没有过度设计” | `ponytail-review` |
| “扫描整个项目，看看哪些代码可以删” | `ponytail-audit` |
| “把以前主动留下的简化项列出来” | `ponytail-debt` |
| “Ponytail 到底能节省多少成本” | `ponytail-gain` |
| “告诉我 Ponytail 有哪些命令” | `ponytail-help` |

`ponytail-review` 和 `ponytail-audit` 最容易混淆：提到 diff、PR 或当前修改时使用 review；提到 repo、codebase 或整个项目时使用 audit。

## 9. 使用建议

日常编码可以让 `ponytail` 以 Full 模式持续工作；提交前按需使用 `ponytail-review`；代码库积累较久后使用 `ponytail-audit`；对主动留下的简化方案定期运行 `ponytail-debt`。

这组 skill 的共同目标不是追求最少字符，而是减少没有现实需求支撑的代码、抽象、依赖和维护成本，同时保留安全、正确性、错误处理和最小验证。
