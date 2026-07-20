---
{"title":"Impeccable Library 学习指南","type":"review","related_projects":["impeccable"]}
---

# Impeccable Library 学习指南

> 研究对象：`libraries/impeccable`  
> 结论先行：这个仓库不是“很多互相独立的 skill”，而是 **1 个 `impeccable` 主 skill、23 个面向用户的设计命令、3 个管理命令、28 份 reference、47 个运行脚本和 2 个专用子代理**。大量文件来自多 provider 构建与网站展示，因此目录数量远大于真实能力数量。

## 1. Impeccable 是什么

Impeccable 是给 AI 编程代理使用的前端设计工作流。它不只提供“美化页面”的审美提示，还把前端设计拆成几类可执行能力：

- 建立项目设计上下文：`PRODUCT.md`、`DESIGN.md`、live mode 配置。
- 在编码前完成 UX/UI discovery 和 design brief。
- 构建、评审、审计、打磨已有界面。
- 分别处理排版、色彩、布局、动效、响应式、UX 文案、性能和边界状态。
- 用确定性 detector 检测常见 AI 设计痕迹与质量问题。
- 在浏览器里选中真实元素，生成三个变体并把接受的结果写回源码。

主入口是：

```text
/impeccable <command> <target>
```

例如：

```text
/impeccable init
/impeccable critique landing
/impeccable harden checkout
/impeccable live
```

主 skill 的适用边界也很明确：网站、落地页、Dashboard、产品 UI、表单、设置页、onboarding 等前端界面；不用于纯后端或非 UI 任务。

## 2. 先看懂目录：哪些是源码，哪些是重复产物

```text
libraries/impeccable/
├─ skill/                         # skill 源码，学习时以这里为准
│  ├─ SKILL.src.md                # 主入口模板
│  ├─ reference/                  # 28 个按需加载的工作流/知识模块
│  ├─ scripts/                    # 47 个上下文、检测、live、hook 辅助脚本
│  └─ agents/                     # 2 个专用子代理
├─ plugin/skills/impeccable/      # 构建后的发布副本，不是第二套 skill
│  ├─ SKILL.md
│  ├─ reference/
│  ├─ scripts/
│  └─ agents/
├─ .agents/、.claude/、.cursor/…  # 各 AI 工具的生成产物
├─ cli/                           # 安装器与确定性 anti-pattern detector
├─ extension/                     # Chrome DevTools 扩展
├─ site/                          # Astro 官网与面向人的说明页面
├─ tests/                         # 构建、detector、live、skill behavior 测试
└─ scripts/                       # 仓库构建与 provider 转换脚本
```

学习时应遵循这条路径：

1. 读 `skill/SKILL.src.md`，理解总入口和路由。
2. 读 `skill/reference/*.md`，理解各命令的专门流程。
3. 需要理解自动化实现时，再读 `skill/scripts/`、`cli/` 和测试。
4. 不要同时读 `plugin/skills/impeccable/`；它和源码拥有相同的 28 个 reference，只是把模板变量展开为发布环境的命令文本。

`site/content/skills/` 是官网给人看的命令介绍；`site/content/reference/{config,context,detector,hooks}.md` 是产品文档，也不是运行时注入给代理的 28 个 reference。

## 3. 主 skill 如何工作

### 3.1 每次设计任务的强制 Setup

`SKILL.src.md` 规定了五步前置流程：

1. 运行 `context.mjs`，读取项目的 `PRODUCT.md` 和 `DESIGN.md`；如果没有 `PRODUCT.md`，必须先转入 `init.md`。
2. 用户调用了子命令时，必须加载对应的 `reference/<command>.md`。
3. 至少读取一个真实的项目样式、token、组件或页面文件，避免脱离现有系统设计。
4. 根据当前页面选择 `brand.md` 或 `product.md`，这是必读的“设计语域”。
5. 仅在全新项目且没有既有品牌色时，运行 `palette.mjs` 生成 OKLCH 品牌种子；已有设计身份优先。

这意味着 reference 不是百科附件，而是主 skill 的“延迟加载执行模块”：主入口负责识别意图，reference 负责规定该意图的具体步骤、输出、检查项和禁止事项。

### 3.2 两套设计语域

```text
                         ┌─ brand.md
用户请求 → 主 skill 路由 ┤  设计本身就是产品：营销、品牌、作品集、长页
                         │
                         └─ product.md
                            设计服务于任务：App、Dashboard、设置、工具
```

两者不是简单的“漂亮 vs 实用”：

| 维度 | Brand register | Product register |
|---|---|---|
| 成功标准 | 有明确观点、可辨识、避免模板化 | 熟悉、可信、任务流顺畅 |
| 字体 | 必须经过品牌声音与实物隐喻筛选，可用强烈配对 | 通常一个调校好的 sans 即可 |
| 色彩 | 可使用 Committed、Full palette、Drenched | 默认 Restrained，强调色主要表达行动与状态 |
| 布局 | 可非对称、破网格、长节奏、分段艺术指导 | 结构性响应式、稳定组件、允许信息密度 |
| 动效 | 可有一个编排良好的品牌时刻 | 150–250ms，主要表达状态，不做页面入场表演 |
| 核心风险 | 安全、平均、像 AI 落地页 | 组件微妙不一致、为个性重造标准控件 |

### 3.3 主 skill 的共用设计法律

无论调用哪个命令，主 skill 都持续约束：

- 文本对比度：正文至少 4.5:1，大字至少 3:1。
- 正文行长约 65–75ch；display 字号上限约 96px；字距不得小于 `-0.04em`。
- 一维用 Flex，二维用 Grid；建立语义化 z-index 层级。
- 动效必须支持 `prefers-reduced-motion`，避免随意动画布局属性和 bounce/elastic easing。
- 禁止渐变文字、默认玻璃拟态、hero metric 模板、重复同构卡片网格、每节 eyebrow、无意义的 `01/02/03` 段落编号、文字溢出等 AI 模板痕迹。
- 先判断“某个领域通常长什么样”，再检查“为了避开第一种套路而落入的第二种套路”。这是它的 first-order / second-order slop test。

## 4. 23 个用户命令分别做什么

下面的“产出”很重要：有些命令只做报告，有些会直接改代码，不能混用。

### 4.1 Build：建立上下文、规划并构建

| 命令 | 核心作用 | 主要流程与产出 |
|---|---|---|
| `craft [feature]` | 完整的端到端设计与实现 | 识别现有框架 → 强制执行 `shape` → 加载排版/布局等 reference → 有图像生成能力时完成 palette、mock、审批和资产切片 → 写生产代码 → 浏览器检查与迭代。它是最完整、门禁最多的命令。 |
| `shape [feature]` | 编码前完成 UX/UI 设计 | 以每轮 2–3 个问题做 discovery，明确用户、内容、真实数据范围、视觉方向、scope、约束、anti-goals；必要时生成 2–4 个视觉探针；最后输出 compact 或十段式 design brief，并停下等待确认。它不写代码。 |
| `init` | 初始化项目设计上下文 | 扫描一次代码库，访谈并写 `PRODUCT.md`；决定是否生成 `DESIGN.md`；有代码时写 live config；最后根据扫描结果推荐 2–4 个下一命令。不会静默覆盖已有文件。 |
| `document` | 把现有视觉系统写成规范 | Scan mode 从 CSS variables、Tailwind、theme、token、组件和渲染结果提取设计系统；写符合 Google Stitch 结构的 `DESIGN.md` 和扩展 sidecar。空项目可走 seed mode，但只写诚实的方向性骨架。 |
| `extract [target]` | 抽取可复用组件与 token | 只抽取出现至少 3 次且意图一致的模式；规划组件、token、variants 和迁移；替换旧用法并删除死代码；更新 Storybook/设计系统文档。没有设计系统时先询问，不擅自建一套。 |

`craft` 与 `shape` 的关系最容易误解：`shape` 的输出是经用户确认的设计 brief；`craft` 消费这个 brief 并继续实施。有原生图像生成时，brief 确认后仍要经过 palette 和 mock 的额外审批，不能直接编码。

### 4.2 Evaluate：只评估，不直接修

| 命令 | 核心作用 | 主要流程与产出 |
|---|---|---|
| `critique [target]` | 设计层面的综合批评 | 对同一稳定目标做两个互相独立的评估：A 是设计总监式 LLM review，B 是 detector + browser evidence；再合并 Nielsen 十项启发式、认知负荷、情绪旅程、persona 风险、P0–P3 问题，写快照供后续 `polish` 使用。 |
| `audit [target]` | 实现层面的技术审计 | 从 accessibility、performance、theming、responsive、anti-patterns 五维各打 0–4 分，总分 20；报告具体文件/行、用户影响、标准、严重度与建议命令。明确规定“只报告，不修复”。 |

两者的区别：

- `critique` 问“这个体验和视觉是否成立、用户是否理解和信任”。
- `audit` 问“实现是否可测地满足 a11y、性能、响应式、token 和规则”。

detector 是证据，不是质量证明；detector 全绿也不能替代真实浏览器观察和设计判断。

### 4.3 Refine：调整已有设计的力度与成熟度

| 命令 | 核心作用 | 主要流程与边界 |
|---|---|---|
| `polish [target]` | 上线前最终质量通检 | 先对齐设计系统并识别 drift 根因，再检查 IA、间距、排版、颜色、八种交互状态、文案、图标、表单、边界、响应式、性能和代码质量；可读取之前的 critique 快照。功能未完成时不应先 polish。 |
| `bolder [target]` | 让安全、平淡的设计更鲜明 | 找一个焦点，通过更强的层级、尺度、字重、色彩承诺、空间张力和有目的的动效放大；brand 追求辨识度，product 主要强化清晰度。不是堆霓虹、紫蓝渐变和玻璃效果。 |
| `quieter [target]` | 降低过强的视觉噪声 | 减少饱和度、颜色数量、字重、装饰、层级和不必要动效，同时保留少数视觉锚点和品牌性；“安静”不是全灰、全小、无层级。 |
| `distill [target]` | 删除不为主任务服务的复杂度 | 明确唯一核心目标；通过 progressive disclosure、合并行动、减少容器/卡片/颜色/字体/步骤/文案和代码 variants 来降负荷；最后记录被移除的能力及替代入口。 |
| `harden [target]` | 让界面承受真实世界数据和失败 | 覆盖长短文本、emoji、RTL、CJK、日期货币、无数据、网络错误、各类 HTTP 错误、大数据、并发、权限、服务端校验、键盘/读屏、慢网与内存泄漏。目标是生产韧性。 |
| `onboard [target]` | 缩短新用户到首次价值的时间 | 先定义 aha moment；用真实任务、渐进披露、可跳过 onboarding、上下文提示、empty state、短 guided tour 和 completion tracking 引导，而不是把整套功能讲一遍。 |

### 4.4 Enhance：专项增强视觉与体验

| 命令 | 核心作用 | 主要流程与技术重点 |
|---|---|---|
| `animate [target]` | 添加传达状态与层级的动效 | 先制定 hero、feedback、transition、delight 四层预算；使用 100/300/500ms 量级、quart/quint/expo ease-out、IntersectionObserver、WAAPI/现有动画库；限制重绘区域并提供 reduced-motion 版本。 |
| `colorize [target]` | 为灰、平、单一强调色的 UI 建立策略色彩 | 先选 Restrained/Committed/Full palette/Drenched，再定义主色与语义色；以 OKLCH 建色阶、验证对比度和色盲可读性；product 强调色不作装饰。live mode 必须给 `color-amount` 参数。 |
| `typeset [target]` | 修正字体、层级和可读性 | 审查字体选择、比例、字重、行长、行高、字距、加载与 OpenType；建立语义化 type scale，防止 generic font 和彼此过于相似的字体配对。live mode 提供可调 type scale 等参数。 |
| `layout [target]` | 修正空间组织、节奏和层级 | 建立 spacing scale，选择 Flex/Grid/Container Queries，打破单调卡片网格，控制 depth 与 optical alignment；响应式不是缩小，而是重排。live mode 通常提供 density 和 structure 参数。 |
| `delight [target]` | 在值得的时刻加入个性与记忆点 | 选择成功、等待、空状态、恢复、里程碑等自然时机，用微交互、品牌文案、插画、声音或隐藏发现增强体验；不得阻塞任务，重复 100 次仍不能烦人。 |
| `overdrive [target]` | 做技术上超出普通网页预期的效果 | 必须先提出 2–3 个方向并让用户选；可使用 View Transitions、scroll timeline、WebGL/WebGPU、Canvas、Workers、WASM、虚拟列表等；必须渐进增强、实机验证、保持 50–60fps 并提供 fallback。 |

### 4.5 Fix：针对明确缺陷修复

| 命令 | 核心作用 | 主要流程与技术重点 |
|---|---|---|
| `clarify [target]` | 改善 UX 文案 | 针对错误、标签、按钮、帮助、空状态、成功、加载、确认和导航统一术语；文案要回答“发生什么、为什么、怎么修”；按钮用明确的 verb + object；错误时不甩锅、不玩幽默。 |
| `adapt [target]` | 将设计适配新设备或媒介 | 分析原/目标上下文、输入方式、屏幕、网络和使用姿态；分别处理 mobile、tablet、desktop、print、email；使用 feature queries、safe area、responsive image、container query，并在真机而非只在 DevTools 验证。 |
| `optimize [target]` | 测量并修复 UI 性能瓶颈 | 先测 LCP/INP/CLS、bundle、网络、帧率和内存；只修真实瓶颈；覆盖图片、字体、code splitting、layout thrashing、paint、长列表、网络和 framework render；必须给出前后数据。 |

### 4.6 Iterate：浏览器内实时生成变体

| 命令 | 核心作用 | 主要流程 |
|---|---|---|
| `live` | 选中浏览器元素，热替换三个 AI 变体 | 启动 helper 并注入 live 脚本 → 打开真实 app URL → 长轮询事件 → 收到 `generate` 后读取标注、定位源码、加载对应 action reference、先提取现有设计身份，再一次性写三个变体 → 接受、丢弃或 steer → 将接受结果 carbonize 成干净的真实源码 → 停服和清理标记。 |

`live` 是整个项目最复杂的工作流。它处理：

- replace 与 insert 两种模式；
- HTML/JSX 与 Svelte 临时组件两种预览路径；
- `generate`、`steer`、`accept`、`discard`、`prefetch`、`manual_edit_apply`、`exit` 事件；
- durable journal、status/resume/complete 恢复；
- generated file 无法直接持久化时的 source fallback；
- 接受后清除临时 wrapper、参数、死 CSS 和 carbonize 标记；
- 首次 config、CSP 检测与经用户同意的 dev-only patch。

live 变体的原则不是“生成三个完全不同的品牌”，而是：先从 `DESIGN.md`、CSS token、computed style 和 sibling component 提取现有 identity，再在该 identity 内改变主要轴。只有用户明确要求 departure 时才偏离。

## 5. 3 个管理命令

它们写在主 skill 中，不计入 23 个设计命令：

| 命令 | 作用 |
|---|---|
| `pin <command>` | 用 `pin.mjs` 为某个子命令创建独立快捷入口，例如 `/audit`。 |
| `unpin <command>` | 删除对应快捷入口。 |
| `hooks <action>` | 加载 `hooks.md`，管理项目级 detector hook 的开关、状态和 ignore。 |

## 6. 28 个 reference 到底是什么

可把它们分成两类：

- **23 个命令 reference**：与用户命令一一对应，定义工作流。
- **5 个内部 reference**：不直接作为主命令出现，提供语域、交互知识、Codex 图像流程和 hook 管理。

### 6.1 命令 reference 的共同结构

多数命令文件采用相似骨架：

```text
作用与额外上下文
→ Register 差异（需要时）
→ Assess：先诊断真实问题
→ Plan：决定策略和边界
→ Implement / Improve：分维度实施
→ Verify：定义完成条件
→ NEVER：列出常见误用
→ Reference Material：较深的领域知识（部分文件内嵌）
```

这种结构让代理先理解再修改，并让不同模型产出相对稳定。较长的 reference 往往把过去的独立知识文档内嵌进来，例如：

- `clarify.md` 内嵌 UX writing 教材。
- `adapt.md` 内嵌 responsive design 教材。
- `colorize.md` 内嵌 OKLCH、functional palette、contrast 和 theming。
- `typeset.md` 内嵌 typography 深层参考。
- `critique.md` 内嵌认知负荷、Nielsen 评分、严重度和 persona 测试。

### 6.2 5 个内部 reference

| 文件 | 何时加载 | 作用 |
|---|---|---|
| `brand.md` | 当前目标是品牌、营销、落地页、作品集、长内容时必读 | 定义 brand register：字体选择流程与 reflex-reject 清单、避免饱和审美路线、色彩承诺、图像要求、布局/动效权限和额外 bans。其重点是“有具体品牌观点”，而不是统一生成一种花哨风格。 |
| `product.md` | 当前目标是 app、admin、dashboard、settings、工具时必读 | 定义 product register：单字体、固定 rem scale、Restrained 色彩、完备组件状态、短动效、标准 affordance 和一致性；目标是让工具消失进任务。 |
| `interaction-design.md` | `craft` 遇到复杂交互或表单时；也可被其他流程按需引用 | 提供八种交互状态、focus-visible、label/validation、loading、native dialog、Popover API、Anchor Positioning、portal、undo 优于 confirmation、roving tabindex、skip link 和手势可发现性。它是跨命令的底层交互教材。 |
| `codex.md` | `craft` 运行在有原生 `image_gen` 的 Codex 环境时 | 规定四个编码前停点：视觉问题回答、palette 确认、1–3 个结构不同的 mock、方向审批；然后盘点 mock 的真实视觉要素并由 asset producer 切出生产资产。防止模型确认 brief 后跳过视觉探索直接编码。 |
| `hooks.md` | 用户调用 `impeccable hooks ...` 时 | 通过 `hook-admin.mjs` 管理项目 detector hook；定义 `status/on/off/ignore-rule/ignore-file/ignore-value/reset`，区分 shared/local 配置，并要求用户明确确认后才能持久化 intentional finding 的 exception。 |

### 6.3 为什么 reference 要拆开，而不是全塞进 SKILL.md

主要有四个原因：

1. **节省上下文**：一次 `clarify` 不必加载 700 多行的 `live.md`。
2. **保持流程专一**：`audit` 明确只报告，`polish` 明确会修改；拆开可避免职责混淆。
3. **按需叠加知识**：`craft` 固定加载 `layout` 和 `typeset`，再按 brief 叠加 `animate`、`adapt`、`interaction-design` 等。
4. **适配 provider**：源码保留 `{{ask_instruction}}`、`{{command_prefix}}` 等模板变量，构建时生成适合 Claude、Codex、Cursor 等环境的文本。

## 7. reference 之间如何组合

### 7.1 一个完整的新功能

```text
craft
  ├─ init（缺 PRODUCT.md 时阻塞并先执行）
  ├─ shape（产生并确认任务级 brief）
  ├─ brand 或 product（确定设计语域）
  ├─ layout + typeset（craft 最低必读）
  ├─ animate / colorize / adapt / clarify / interaction-design（按 brief 叠加）
  ├─ codex（有原生图像生成时）
  └─ build → browser inspect → polish-level verification
```

### 7.2 一个已有页面的质量闭环

```text
critique ──→ 设计问题与 critique snapshot ─┐
audit ─────→ 技术问题与严重度 ─────────────┼→ 专项命令修复
detector ──→ 确定性证据 ───────────────────┘
                                               ↓
                                            polish
                                               ↓
                                      重新 critique / audit
```

### 7.3 浏览器内局部变体

```text
live generate
  → 判断 event.action
  → 加载 brand/product
  → 若 action=layout/colorize/... 再加载对应 reference
  → 保持 identity，生成三个主要轴不同的变体
  → 用户 accept
  → 写回真实源文件并清掉 live plumbing
```

## 8. reference、script、agent、detector 的职责边界

| 层 | 回答的问题 | 例子 |
|---|---|---|
| `SKILL.src.md` | 何时触发、先加载什么、如何路由 | Setup、通用设计法律、命令表、无参数推荐逻辑 |
| `reference/*.md` | 某类任务应该怎样思考、执行和验收 | `harden` 的 i18n/错误/边界流程，`audit` 的评分模板 |
| `skill/scripts/` | 怎样可靠地完成机器操作 | context 扫描、palette、detector wrapper、live server/poll/wrap/accept、hook admin |
| `agents/` | 哪些高度聚焦的工作应隔离执行 | raster asset 生产、live 手工编辑应用 |
| `cli/engine/` | 哪些规则可以不依赖 LLM 确定性检测 | 颜色、字体、卡片、布局、视觉对比度等 detector rules |
| `site/` / `extension/` | 怎样把能力呈现给人和浏览器 | 官网说明、demo、DevTools overlay |

两个专用 agent 的职责：

- `impeccable-asset-producer.md`：根据已批准 mock 和 crop contract 生成、清理并交付栅格资产；避免父代理把大段图像生产上下文混进实现任务。
- `impeccable-manual-edit-applier.md`：在 live mode 中把用户对多个元素的手工修改原子化写回源码，按固定 JSON contract 报告成功、部分成功或失败；它不负责 poll/reply。

## 9. `PRODUCT.md`、`DESIGN.md` 与 reference 的关系

这三个层次分别回答不同问题：

| 层次 | 回答 | 典型内容 |
|---|---|---|
| `PRODUCT.md` | 谁、为什么、品牌战略是什么 | register、用户、产品目的、品牌人格、anti-references、设计原则、无障碍需求 |
| `DESIGN.md` | 视觉系统实际长什么样 | colors、typography、elevation、components、do/don't；frontmatter 是规范 token，正文解释应用 |
| command reference | 当前这项工作如何完成 | 评估步骤、决策、修改维度、验证和禁止事项 |

优先级可以概括为：

- 战略/语气冲突时，`PRODUCT.md` 决定。
- 视觉 token/组件冲突时，`DESIGN.md` 决定。
- 操作顺序与验收冲突时，对应 command reference 决定。
- 已经上线的身份优先于 greenfield 的“反套路”建议；不能为了避开默认字体而擅自改掉品牌现有字体。

`document.md` 对 `DESIGN.md` 的格式要求很严格：YAML frontmatter 是机器可读 token；正文固定为 Overview、Colors、Typography、Elevation、Components、Do's and Don'ts 六部分。额外的 tonal ramp、shadow、motion、breakpoint 和完整组件 HTML/CSS 放进 `.impeccable/design.json`，不污染 Stitch frontmatter schema。

## 10. 推荐学习顺序

### 第一阶段：理解框架

1. `skill/SKILL.src.md`：只先看 frontmatter、Setup、General rules、Commands、Routing rules。
2. `reference/brand.md` 和 `reference/product.md`：理解同一条建议为何不能机械套在品牌页和产品 UI 上。
3. `reference/init.md`、`shape.md`、`craft.md`：理解“项目上下文 → 任务 brief → 生产实现”的主链。

### 第二阶段：理解质量闭环

4. `reference/critique.md`：重点看双评估、启发式评分、persona 和 snapshot。
5. `reference/audit.md`：重点看五维 20 分技术审计。
6. `reference/polish.md`：重点看设计系统 drift 分类和最终质量清单。

### 第三阶段：学习专项设计知识

7. `typeset.md`、`colorize.md`、`layout.md`：视觉基础。
8. `interaction-design.md`、`adapt.md`、`clarify.md`：交互、响应式和文案。
9. `animate.md`、`delight.md`、`overdrive.md`：从必要反馈到品牌时刻，再到技术性突破。
10. `harden.md`、`onboard.md`、`optimize.md`：生产韧性、激活与性能。

### 第四阶段：理解工程实现

11. `reference/live.md`：先读 contract、event loop、generate、accept/carbonize、cleanup；不要第一次就逐行钻 CSP 和 framework fallback。
12. `skill/scripts/live-*.mjs` 与 `tests/live-*.test.mjs`：沿事件状态机理解实现。
13. `cli/engine/detect-antipatterns.mjs` 和 fixtures：理解 prompt guidance 如何落成确定性规则。
14. `scripts/lib/transformers/`：理解 `SKILL.src.md` 和 references 如何变成各 provider 的发布副本。

## 11. 阅读时最值得借鉴的设计

1. **Progressive disclosure 用在 prompt 自身**：主入口只做路由，深知识放 reference，复杂操作交给 script。
2. **评估与修改分离**：`audit`、`critique` 先建立证据；专项命令和 `polish` 再修改。
3. **设计不是一套固定审美**：brand/product register 把“鲜明”与“可信”的目标分开。
4. **LLM 判断与确定性检测并用**：detector 擅长可计算规则，critique 擅长整体层级、情绪与认知负荷。
5. **中间产物可持续复用**：`PRODUCT.md`、`DESIGN.md`、critique snapshot、live journal 都减少下一轮重新猜测。
6. **复杂工作流设置明确停点**：尤其 `shape` 和 `codex`，用户确认是工作流的一部分，而不是礼貌性询问。
7. **把临时预览与永久源码严格分开**：live 的 wrap、accept、carbonize 和 cleanup 机制防止把调试标记留在生产源码。

## 12. 容易误读的地方

- `plugin/skills/impeccable` 不是另一个 skill；它是 `skill/` 的 provider-resolved 构建产物。
- 23 个 command 不是 23 个独立安装单元；用户安装的是一个 `impeccable` skill。
- reference 不是“建议读一下”；被路由到的 command reference 和 register reference 都是强制加载项。
- `critique` 与 `audit` 都不等于 `polish`：前两者的主要产出是报告，后者才是最终修改流程。
- `bolder` 不等于更多效果，`quieter` 不等于去掉个性，`distill` 不等于删除必要能力。
- `live` 的 helper port 不是应用 dev-server URL；浏览器必须打开真实应用地址。
- 官网的 skill 页面是便于人类阅读的介绍，不是代理执行时的权威源码。
- `libraries/` 在 Skills-Hub 中是上游快照，应当只读；如果未来要修改 Impeccable，应在上游源码或明确授权的同步流程中做，不应直接补丁这个快照。

## 13. 一句话总览

Impeccable 的真正价值不在“23 条美化提示”，而在一套分层的设计操作系统：**主 skill 负责上下文与路由，register 定义设计目标，command reference 定义专业流程，脚本提供确定性执行，detector 提供机器证据，browser live mode 完成可视化迭代，`PRODUCT.md` 与 `DESIGN.md` 让设计决策跨任务持续存在。**

## 14. 关键源码入口

- [主 skill 源模板](../libraries/impeccable/skill/SKILL.src.md)
- [28 个 reference 的源码目录](../libraries/impeccable/skill/reference/)
- [skill 辅助脚本目录](../libraries/impeccable/skill/scripts/)
- [专用 agent 目录](../libraries/impeccable/skill/agents/)
- [构建后的 plugin 发布副本](../libraries/impeccable/plugin/skills/impeccable/)
- [detector 核心](../libraries/impeccable/cli/engine/detect-antipatterns.mjs)
- [上游 README](../libraries/impeccable/README.md)
- [上游仓库维护说明](../libraries/impeccable/AGENTS.md)
