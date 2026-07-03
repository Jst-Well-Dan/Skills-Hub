# Project Testing Skill Pack

这是一个面向“项目测试”的组合 skill 包，收录了 3 个互补的测试相关 skill：

- `test-strategy-hardening`
- `webapp-testing`
- `dogfood`

它们不是同一种能力的重复版本，而是覆盖测试工作的三个层次：

| Skill | 角色 | 主要用途 |
|---|---|---|
| `test-strategy-hardening` | 测试策略与测试体系审查 | 判断应该测什么、现有测试是否有价值、缺哪些关键覆盖、测试如何分层 |
| `webapp-testing` | Playwright 自动化浏览器验证 | 启动本地 Web 应用，执行页面交互、截图、读取 console、验证具体流程 |
| `dogfood` | 探索式 QA / 用户视角测试 | 像真实用户一样使用产品，发现 bug、UX 问题、交互断点，并产出复现证据 |

## 什么时候使用这个包

适合使用这个组合包的情况：

- 想测试一个 Web App、SaaS、后台系统、工具型产品或全栈项目。
- 准备上线前，希望确认关键流程是否真的可用。
- 项目测试很少，想先建立测试策略。
- 已经有测试，但不确定这些测试是否有价值。
- 想让 agent 像用户一样探索应用，找出隐藏问题。
- 想用 Playwright 对本地项目做自动化验证。

不太适合的情况：

- 只是测试一个很小的脚本函数。
- 只需要跑一次现有单元测试，不需要额外分析。
- 项目没有可交互界面，而且目标也不是测试体系建设。

## 三者之间的关系

可以把它们理解成三个问题：

1. `test-strategy-hardening`：我们应该怎么测？
2. `webapp-testing`：这个功能按预期跑通了吗？
3. `dogfood`：真实用户使用时会遇到什么问题？

推荐顺序通常是：

```text
test-strategy-hardening -> webapp-testing -> dogfood
```

但这不是强制顺序。很多时候只需要其中一个或两个。

## 只用一个的情况

### 只用 `test-strategy-hardening`

当你关心的是测试体系，而不是马上点开页面测试。

适合请求：

```text
请审查这个项目的测试体系，告诉我缺哪些关键测试。
```

```text
这个项目准备大重构，先帮我设计测试策略。
```

```text
现有测试是不是有价值？哪些该保留、重写、删除？
```

它会关注：

- 测试命令、框架、CI 配置。
- 单元测试、集成测试、E2E、视觉测试、smoke test 的分层。
- 哪些测试覆盖关键业务，哪些只是装饰性测试。
- 哪些关键路径缺少回归保护。
- 测试运行时间、脆弱性、重复性、fixture 质量。

### 只用 `webapp-testing`

当你已经知道要验证哪些页面或流程，需要实际跑浏览器测试。

适合请求：

```text
用 Playwright 测试这个本地 Web App 的登录和创建流程。
```

```text
启动项目并截图检查首页、设置页、移动端布局。
```

```text
帮我验证这个按钮点击后是否真的提交成功，并检查 console 错误。
```

它会关注：

- 启动本地 dev server。
- 等待页面渲染完成。
- 使用 Playwright 点击、输入、跳转。
- 截图保存证据。
- 查看浏览器 console 和页面错误。
- 验证具体用户路径是否可运行。

### 只用 `dogfood`

当你想让 agent 像真实用户一样探索产品，而不是只按预设脚本执行。

适合请求：

```text
请 dogfood 这个网站，找出 5-10 个真实用户会遇到的问题。
```

```text
对这个后台系统做探索式 QA，并给出复现步骤和截图。
```

```text
帮我测试这个 app 的核心体验，重点找 UX 问题和功能断点。
```

它会关注：

- 从用户视角浏览主要页面。
- 点击导航、按钮、表单、弹窗、下拉菜单。
- 尝试真实端到端流程。
- 查找 console 错误和网络失败。
- 对每个问题记录截图、视频、复现步骤。
- 输出结构化 QA 报告。

## 组合使用方式

### 快速功能验收

只需要确认关键功能是否能跑通：

```text
webapp-testing
```

典型流程：

1. 启动项目。
2. 打开核心页面。
3. 执行 1-3 条关键路径。
4. 截图并检查 console。
5. 报告通过、失败和复现步骤。

### Web App QA

既要验证核心路径，也要找真实体验问题：

```text
webapp-testing -> dogfood
```

典型流程：

1. 先用 `webapp-testing` 跑通明确的核心流程。
2. 再用 `dogfood` 探索非预期路径和边界状态。
3. 把结果分成“功能阻断”“体验问题”“视觉/响应式问题”“console/网络错误”。

### 上线前测试

项目准备发布，需要更系统的测试判断：

```text
test-strategy-hardening -> webapp-testing -> dogfood
```

典型流程：

1. 用 `test-strategy-hardening` 盘点测试体系和关键风险。
2. 用 `webapp-testing` 验证核心用户流程。
3. 用 `dogfood` 做探索式 QA，找遗漏问题。
4. 最后根据风险决定是否补测、修 bug 或推迟发布。

### 重构前测试

项目准备重构，先建立安全网：

```text
test-strategy-hardening -> webapp-testing
```

典型流程：

1. 识别关键业务行为。
2. 判断现有测试是否能保护这些行为。
3. 补最小高价值 characterization tests。
4. 用浏览器验证核心行为当前状态。
5. 再开始重构。

## 推荐提示词

### 让 agent 先判断使用哪些 skill

```text
请使用 project-testing-skill-pack 帮我测试这个项目。先判断应该使用 test-strategy-hardening、webapp-testing、dogfood 中的哪些，再执行。
```

### 做完整 Web App 测试

```text
请对这个 Web App 做一次完整测试：
1. 先用 test-strategy-hardening 评估测试体系和关键风险；
2. 再用 webapp-testing 跑核心用户流程；
3. 最后用 dogfood 做探索式 QA；
请输出问题列表、复现步骤、截图/日志证据，以及建议优先级。
```

### 只做快速验收

```text
请用 webapp-testing 快速验收这个项目的核心流程，启动本地服务，检查页面交互、截图和 console 错误。
```

### 只做探索式 QA

```text
请用 dogfood 对这个应用做探索式 QA，目标是找出 5-10 个真实用户可能遇到的问题，每个问题都要有复现步骤和截图证据。
```

### 只做测试体系审查

```text
请用 test-strategy-hardening 审查这个项目的测试体系，告诉我现有测试是否有价值、缺哪些关键测试、下一步应该补哪些测试。
```

## 输出建议

使用这个包时，建议要求 agent 输出以下内容：

- 测试范围：测试了哪些页面、接口、流程。
- 测试方式：策略审查、Playwright 自动化、探索式 QA。
- 通过项：哪些关键流程已验证。
- 问题列表：按严重程度排序。
- 复现步骤：每个问题如何重现。
- 证据：截图、视频、console 错误、日志片段。
- 未覆盖范围：哪些内容还没有测。
- 下一步建议：先修什么、补什么测试、是否可以发布。

## 注意事项

- 不要默认三个都用。小任务优先选择一个最匹配的 skill。
- `test-strategy-hardening` 偏分析和规划，不会自动替你完成所有测试。
- `webapp-testing` 偏确定性验证，适合已有明确测试目标。
- `dogfood` 偏探索式发现问题，不应该代替单元测试或集成测试。
- 如果项目需要登录、测试账号、OTP 或外部服务凭据，需要提前提供或允许 agent 暂停等待输入。
- 如果是生产环境测试，必须避免破坏真实数据。优先使用测试账号、临时记录和可清理数据。

## 目录结构

```text
project-testing-skill-pack/
  README.md
  test-strategy-hardening/
    SKILL.md
    references/
    agents/
  webapp-testing/
    SKILL.md
    examples/
    scripts/
  dogfood/
    SKILL.md
    references/
    templates/
```

## 来源

- `test-strategy-hardening`：来自 `swyxio-skills` / Kakuna Codebase Hardening Suite。
- `webapp-testing`：来自 `anthropic` skill 集合。
- `dogfood`：来自 `agent-browser` skill 集合。

