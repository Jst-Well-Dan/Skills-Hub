<!-- source-sha256: e26ac0962e4a016a561e4317232bd23d5266b74f38e8bfc785d81f41f93e25b9 -->
---
name: impeccable
description: 当用户希望设计、重新设计、塑造、评议、审查、润色、澄清、提炼、强化、优化、适配、动画化、着色、提取或以其他方式改进前端界面时使用。涵盖网站、落地页、仪表板、产品 UI、应用外壳、组件、表单、设置、引导流程和空状态。处理 UX 评审、视觉层级、信息架构、认知负荷、无障碍、性能、响应式行为、主题、反模式、排版、字体、间距、布局、对齐、颜色、动效、微交互、UX 文案、错误状态、边缘情况、i18n，以及可复用的设计系统或令牌。也适用于需要变得更大胆或更令人愉悦的平淡设计、应当变得更克制的喧闹设计、在实时浏览器中迭代 UI 元素，或应呈现出卓越技术感的宏大视觉效果。不适用于纯后端或非 UI 任务。
version: 3.9.1
user-invocable: true
argument-hint: "[craft|shape · audit|critique · animate|bolder|colorize|delight|layout|overdrive|quieter|typeset · adapt|clarify|distill · harden|onboard|optimize|polish · init|document|extract|live] [target]"
license: Apache 2.0
allowed-tools:
  - Bash(npx impeccable *)
  - Bash(node .claude/skills/impeccable/scripts/*)
---

设计并迭代生产级前端界面。提供真正可运行的代码、明确坚定的设计选择和卓越的工艺水准。

## 设置

继续之前，你必须完成以下步骤：

1. 每个会话运行一次 `node .claude/skills/impeccable/scripts/context.mjs`；如果运行时显示了此技能已加载的基础目录，则改为运行 `node <skill-base-dir>/scripts/context.mjs`。将 cwd/workdir 保持在用户项目中，而不是技能目录中。如果请求明确提到或隐含了 monorepo 内的文件、路由或应用，请推断具体路径，并在同一命令后追加 `--target <path>`。如果你已经在本次对话中看过其输出，请不要重复运行。该脚本要么以 Markdown 块形式输出项目的 PRODUCT.md（以及存在时的 DESIGN.md），要么告诉你它不存在。遵循它输出的所有指示。**如果它报告 `NO_PRODUCT_MD`：**当用户调用了 `init`、`teach`、`craft` 或 `shape`，或其措辞明显对应其中一种从零构建流程时（例如：“构建/创建/制作一个落地页”“设计一个新应用”或“塑造一项功能”），应先转入 `reference/init.md`。捕获产品上下文正是这些流程的重点。对于任何其他针对现有代码、范围明确的评估 / 改进 / 增强 / 修复 / 迭代请求，**不要**转入 init。现有代码就是上下文：继续执行请求的命令，根据当前关注的界面推断设计语域（步骤 4），并将 `/impeccable init` 作为用户之后可以选择的一次性建议。缺少 PRODUCT.md 绝不能阻塞范围明确的请求。如果输出末尾包含 `UPDATE_AVAILABLE` 指令，请遵循它（询问用户一次是否更新，然后继续）。它绝不会阻塞当前任务。
2. 如果用户调用了子命令（`craft`、`shape`、`audit`、`polish` 等），接下来你必须读取该命令的参考文件：**`reference/<command>.md`；当项目平台为原生平台时（根据 `context.mjs` 指令，为 `ios` / `android` / `adaptive`），则读取 Commands 表中的原生变体**（例如 `reference/audit.native.md`）。只读取其中一个，而不是两个。这是强制要求。参考文件定义了命令流程；不读取它，你就会漏掉用户期望的步骤。
3. 熟悉代码中已有的设计系统、约定和组件。至少读取一个项目文件（CSS / 令牌 / 主题 / 具有代表性的组件或页面）。**即使已在步骤 2 中加载子命令参考文件，这一步仍是必需的。**不要重复造轮子；现有方案可用时就使用它，只有当 UX 确实能获益时才另辟路径。
4. 读取匹配的设计语域参考文件。**这是强制要求；跳过它会产生千篇一律的输出。**如果项目是营销网站、落地页、宣传活动、长篇内容或作品集（设计本身就是产品），请读取 `reference/brand.md`。如果它是应用 UI、管理后台、仪表板或工具（设计服务于产品），请读取 `reference/product.md`。按首次匹配选择：(1) 任务线索（“落地页”与“仪表板”）；(2) 当前关注的界面（正在处理的页面、文件或路由）；(3) PRODUCT.md 中的 `register` 字段。
5. **如果 PRODUCT.md 的 `## Platform` 是 `ios` 或 `android`**，还要读取 `reference/<platform>.md`（HIG / Material 3 规范）。`adaptive`（跨平台，同时发布两端）需要读取两个文件。`web`、缺失或无法识别：无需额外读取。适用时，`context.mjs` 会输出该指令。
6. **如果项目是全新的（步骤 3 中未发现现有 CSS 令牌 / 主题 / 已确定的品牌颜色）**，请运行 `node .claude/skills/impeccable/scripts/palette.mjs`，以获得品牌种子色和构图指导。该颜色将作为主品牌色的锚点。按照脚本说明，围绕它构建其余调色板（bg、surface、ink、accent、muted）。全程使用 OKLCH。**只有当步骤 3 在现有令牌中发现了已确定的品牌颜色时，才跳过此步骤；在这种情况下，应优先保持品牌识别度。**

## 设计指导

产出可直接发布的生产级代码，而不是原型或起点。除非用户要求，否则不要走捷径（不确定时就询问）。在实现完整成果之前不要停下（美观、响应迅速、快速、精确、无错误且符合品牌）。你应认真对待细节：制作的每个页面、区块或组件都要使用可用工具（浏览器截图、计算机操作等）进行实战检验。Claude 能够完成非凡的工作。不要有所保留。

### 通用规则

#### 颜色

- **验证对比度。**正文文本与背景的对比度必须达到 ≥4.5:1；大号文本（≥18px 或粗体 ≥14px）需要达到 ≥3:1。占位符文本同样需要达到 4.5:1，不能使用默认的柔和灰色。最常见的问题是：带色调的近白色背景上使用柔和灰色正文。如果对比度哪怕只是接近临界值，也要将正文颜色向色阶中的 ink 端推进；为了“优雅”而使用浅灰色，是 AI 设计难以阅读的首要原因。
- 彩色背景上的灰色文本看起来会褪色。请使用背景自身色相的更深色阶，或使用文本颜色的透明版本。

#### 排版

- 将正文行长限制在 65–75ch。
- 不要搭配相似但并不相同的字体（两种几何无衬线字体、两种人文无衬线字体）。应沿对比轴搭配（衬线体 + 无衬线体、几何体 + 人文体），或使用同一字体家族的多种字重。
- Hero / 展示型标题的上限：clamp() 的最大值 ≤ 6rem（约 96px）。超过这一尺寸，页面是在叫喊，而不是在设计。
- 展示型标题的字距下限：≥ -0.04em。再紧会导致字母相碰；那是拥挤，不是“设计感”。
- 对 h1–h3 使用 `text-wrap: balance` 以获得均衡的行长；对长篇正文使用 `text-wrap: pretty` 以减少孤行。

#### 布局

- 通过变化间距来营造节奏。
- 卡片是偷懒的答案。只有当它确实是最佳可供性时才使用。嵌套卡片永远是错误的。
- 一维布局使用 Flexbox，二维布局使用 Grid。当 `flex-wrap` 更简单时，不要默认使用 Grid。
- 对于无需断点的响应式网格，使用：`repeat(auto-fit, minmax(280px, 1fr))`。
- 建立语义化的 z-index 层级（dropdown → sticky → modal-backdrop → modal → toast → tooltip）。绝不要使用 999 或 9999 之类的任意值。

#### 动效

- 动效应有明确意图，不能事后补上。应将其视为构建过程的一部分。
- 除非确有必要，否则不要为 CSS 布局属性添加动画。
- 使用指数曲线缓出（ease-out-quart / quint / expo）。不要使用 bounce，也不要使用 elastic。
- 对更高级的动效需求使用库（例如 motion、gsap、anime.js、lenis 等）。
- 减少动效不是可选项。每个动画都需要一个 `@media (prefers-reduced-motion: reduce)` 替代方案：通常是交叉淡化或即时切换。
- 对同一列表内的项目进行错峰动画是合理的。问题在于机械一致的惯性做法（每个区块都使用相同的入场动画），而不在于动效本身；每次呈现都应适合它所呈现的内容。抑制这种惯性绝不是让页面完全没有动效的理由。
- 呈现动画必须增强默认情况下已经可见的内容。不要依赖由类触发的过渡来控制内容可见性；过渡会在隐藏标签页和无头渲染器中暂停，导致呈现永不触发，最终发布的区块一片空白。
- 高级动效材质不只有 transform/opacity。当模糊、backdrop-filter、clip-path、mask 和阴影/辉光能够实质性改善效果且保持流畅时，它们也属于可用的表现手段。

#### 交互

- 在带有 `overflow: hidden` 或 `overflow: auto` 的容器中使用 `position: absolute` 渲染的下拉菜单会被裁剪。请使用原生 `<dialog>` / popover API、`position: fixed` 或 portal 来脱离该堆叠上下文。

### 仅限新项目（不存在既有成果时）

#### 颜色与主题

- 使用 OKLCH。
- **奶油色 / 沙色 / 米色的页面主体背景，是 2026 年已经泛滥的 AI 默认选择。**整个暖中性色区间（OKLCH L 0.84-0.97、C < 0.06、色相 40-100），无论你如何命名，看起来都像奶油、沙子、纸张或羊皮纸。`--paper`、`--cream`、`--sand`、`--bone`、`--flour`、`--linen`、`--parchment`、`--wheat`、`--biscuit`、`--ivory` 这样的令牌名本身就是明显特征。如果需求是“温暖、传统、家庭式海滨意大利风”“杂志般温暖”或“编辑式克制”，不要将其转化为带暖色调的近白色背景；那是典型的 AI 做法。请选择：(a) 使用饱和品牌色作为页面主体颜色（陶土色、牛血红、深赭色、近黑色），(b) 使用色度为 0 的真正灰白色（或让色度偏向品牌自身的色相，而不是默认偏暖），或 (c) 使用更深的中间调带色中性色，且明显属于品牌自身。“温暖感”应通过强调色 + 排版 + 图像来承载，而不是通过页面主体背景。
- 带色中性色：添加 0.005–0.015 的色度，并使其偏向品牌色相。不要因为“品牌给人这种感觉”就默认偏暖或偏冷；那会造成跨项目的审美单一化。
- 选择主题时：深色与浅色都绝不是默认答案。不能因为“工具用深色看起来很酷”就选择深色，也不能为了“保险”就选择浅色。选择前，先写一句描述实际场景的话：谁在使用、在哪里使用、环境光如何、处于什么情绪。如果这句话不能迫使你得出答案，就说明它还不够具体。继续添加细节，直到答案变得明确。
- 在选择颜色前，先确定一种**色彩策略**。按投入程度分为四级：
  - **克制**：带色中性色 + 一个占比 ≤10% 的强调色。产品默认；品牌极简主义。
  - **坚定**：一种饱和色覆盖 30–60% 的界面。身份驱动型页面的品牌默认策略。
  - **完整调色板**：3–4 个有明确名称的角色，每个角色都经过有意使用。适用于品牌活动和产品数据可视化。
  - **浸染**：界面本身就是颜色。适用于品牌 Hero 和宣传活动页面。

### 绝对禁用项

发现即拒绝。如果你正准备编写以下任何一种元素，请使用不同结构重写它。

- **侧边条边框。**在卡片、列表项、提示框或警报上使用大于 1px 的 `border-left` 或 `border-right` 作为彩色强调。绝不能将其作为刻意设计。请改用完整边框、带色背景、前置数字/图标，或什么都不用。
- **渐变文本。**将 `background-clip: text` 与渐变背景组合使用。它只是装饰，从不承载意义。使用单一纯色。通过字重或字号进行强调。
- **默认使用玻璃拟态。**将模糊和玻璃卡片用于装饰。只能少量且有明确目的地使用，否则完全不用。
- **Hero 指标模板。**大数字、小标签、辅助统计数据、渐变强调。典型的 SaaS 陈词滥调。
- **千篇一律的卡片网格。**相同尺寸的卡片以图标 + 标题 + 文本的形式无休止重复。
- **每个区块上方都放置微小的大写宽字距眉题。**这种 2023 年风格的引导标题（每个标题上方带有宽字距的小号全大写文本，如“ABOUT”“PROCESS”“PRICING”）如今已成为泛滥的 AI 脚手架；无论需求是什么，它都会出现在 55–95% 的生成结果中，这正是明显特征的定义。一个经过明确命名、作为品牌系统刻意使用的引导标题是品牌声音；每个区块都使用眉题则是 AI 语法。请选择不同的节奏。
- **默认使用编号区块标记作为脚手架（01 / 02 / 03）。**在每个区块上方放置 `01 · About / 02 · Process / 03 · Pricing`，是比眉题套路更深一层的问题：因为“落地页都这样做”而下意识采用，就是在机械地搭脚手架。只有当区块确实构成顺序（真实的三步流程、有序流、带类型的时间线），且顺序承载了读者需要的信息时，编号才有存在的价值。一个页面上经过刻意设计的编号序列是品牌声音；整个网站每个区块都使用编号眉题则是 AI 语法。
- **溢出容器的文本。**长标题单词 + 较大的 clamp 尺度 + 狭窄网格会导致标题在平板或移动端溢出。在每个断点测试标题文案；如果发生溢出，请降低 clamp 最大值或重写文案。视口是设计的一部分。

### AI 粗制滥造测试

如果有人一眼就能断言“这是 AI 做的”，那么它就失败了。跨设计语域的失败项就是上述绝对禁用项。各设计语域特有的失败项记录在对应参考文件中。

**类别惯性检查。**从两个层级执行；第二层级能捕获第一层级遗漏的问题。

- **第一层：**如果有人仅凭类别就能猜出主题 + 调色板，那就是最表层的训练数据惯性。重新设计场景描述和色彩策略，直到答案无法再从领域中直接推断出来。
- **第二层：**如果有人能通过类别加反面参考猜出审美流派（“不是奶油色 SaaS 风的 AI 工作流工具 → 编辑式排版”“不是海军蓝加金色的金融科技 → 终端原生深色模式”），那就是更深一层的陷阱。你避开了第一层惯性，却没有避开第二层。继续调整，直到两种答案都不再显而易见。品牌设计语域中的[拒绝惯性审美路线](reference/brand.md)列表涵盖了当前已经泛滥的风格流派。

## 命令

| 命令 | 类别 | 描述 | 参考 |
|---|---|---|---|
| `craft [feature]` | 构建 | 先塑造，再端到端构建一项功能 | [reference/craft.md](reference/craft.md) |
| `shape [feature]` | 构建 | 编写代码前规划 UX/UI | [reference/shape.md](reference/shape.md) |
| `init` | 构建 | 设置项目上下文：PRODUCT.md、DESIGN.md、实时配置和后续步骤 | [reference/init.md](reference/init.md) |
| `document` | 构建 | 根据现有项目代码生成 DESIGN.md | [reference/document.md](reference/document.md) |
| `extract [target]` | 构建 | 将可复用令牌和组件提取到设计系统中 | [reference/extract.md](reference/extract.md) |
| `critique [target]` | 评估 | 带启发式评分的 UX 设计评审 | [reference/critique.md](reference/critique.md) |
| `audit [target]` | 评估 | 技术质量检查（a11y、性能、响应式） | [reference/audit.md](reference/audit.md) · 原生：[reference/audit.native.md](reference/audit.native.md) |
| `polish [target]` | 改进 | 发布前的最终质量检查 | [reference/polish.md](reference/polish.md) |
| `bolder [target]` | 改进 | 增强保守或平淡的设计 | [reference/bolder.md](reference/bolder.md) |
| `quieter [target]` | 改进 | 弱化咄咄逼人或刺激过度的设计 | [reference/quieter.md](reference/quieter.md) |
| `distill [target]` | 改进 | 提炼至本质，移除复杂性 | [reference/distill.md](reference/distill.md) |
| `harden [target]` | 改进 | 达到生产就绪：错误、i18n、边缘情况 | [reference/harden.md](reference/harden.md) |
| `onboard [target]` | 改进 | 设计首次使用流程、空状态和激活体验 | [reference/onboard.md](reference/onboard.md) |
| `animate [target]` | 增强 | 添加有明确目的的动画和动效 | [reference/animate.md](reference/animate.md) |
| `colorize [target]` | 增强 | 为单色 UI 策略性地添加颜色 | [reference/colorize.md](reference/colorize.md) |
| `typeset [target]` | 增强 | 改进排版层级和字体 | [reference/typeset.md](reference/typeset.md) |
| `layout [target]` | 增强 | 修复间距、节奏和视觉层级 | [reference/layout.md](reference/layout.md) |
| `delight [target]` | 增强 | 添加个性和令人难忘的细节 | [reference/delight.md](reference/delight.md) |
| `overdrive [target]` | 增强 | 突破常规限制 | [reference/overdrive.md](reference/overdrive.md) |
| `clarify [target]` | 修复 | 改进 UX 文案、标签和错误消息 | [reference/clarify.md](reference/clarify.md) |
| `adapt [target]` | 修复 | 适配不同设备和屏幕尺寸 | [reference/adapt.md](reference/adapt.md) · 原生：[reference/adapt.native.md](reference/adapt.native.md) |
| `optimize [target]` | 修复 | 诊断并修复 UI 性能问题 | [reference/optimize.md](reference/optimize.md) |
| `live` | 迭代 | 视觉变体模式：在浏览器中选择元素并生成替代方案 | [reference/live.md](reference/live.md) |

此外还有三个管理命令：`pin <command>`、`unpin <command>` 和 `hooks <on|off|status|...>`，详见下文。

### 路由规则

1. **无参数**：用户是在询问“我该做什么？”菜单应根据上下文动态生成，而不是保持静态。设置流程已经运行了 `context.mjs`；如果它报告 `NO_PRODUCT_MD`，说明项目尚未捕获上下文，因此应将 `/impeccable init` 作为首要建议放在菜单开头（用一行说明原因），同时仍在下方显示其余内容；不要悄悄直接进入 init。否则，运行一次 `node .claude/skills/impeccable/scripts/context-signals.mjs` 并读取其 JSON，然后首先给出**最有价值的 2–3 个后续命令**，每个命令都附上一行根据这些信号得出的原因，随后给出完整菜单（即上表，按类别分组）。**绝不要自动运行命令；推荐只是建议，需要用户确认。**

   应对这些信号进行推理；不存在必须服从的分数：
   - `setup.hasDesign` 为 false，而 `setup.hasCode` 为 true → `document`（记录视觉系统）。
   - `critique.latest` 为 `null` → 项目从未接受过评议；对于已经设置完毕且拥有真实界面的项目，建议 `/impeccable critique <surface>` 是一个有力的默认选择。
   - `critique.latest` 的 `score` 较低，或 `p0` / `p1` 非零 → `polish`（它会将该快照作为待办列表读取）；如果快照看起来已经过时，则重新运行 `critique`。
   - `git.changedFiles` 指向单个界面 → 将 `audit` 或 `polish` 的范围明确限定到这些文件，并点名它们。
   - `devServer.running` 为 true → 可以使用 `live` 在浏览器中迭代；如果为 false，不要优先推荐 `live`。**`live` 和内置的 `detect.mjs` 仅适用于 Web。**如果 `setup.platform` 是 `ios`、`android` 或 `adaptive`，不要优先推荐二者；浏览器覆盖层和 HTML 规则引擎不适用于原生应用代码。
   - 否则，严格按照 init 的“Recommend starting points”步骤按意图分组（构建新内容 / 改进现有内容 / 进行视觉迭代），并根据 `setup.register` 进行调整。

   **如果 `scan.targets` 非空，且 `setup.platform` 不是 `ios`/`android`/`adaptive`，则运行一次 `node .claude/skills/impeccable/scripts/detect.mjs --json <scan.targets joined by spaces>`**（对本地文件运行的内置检测器：无需网络，不使用 npx；它读取 HTML/CSS，因此原生项目应跳过）。`scan.via` 会说明目标来源：`git-changes`（脏工作树中的标记/样式文件，是最相关的集合）、`source-dir`（例如 `src`、`app`）、`html` 或 `root`。将命中结果纳入你的推荐：存在大量质量 / 对比度问题 → `audit` 或 `polish`；存在具体的粗制滥造风格 → 使用对应命令（渐变文本或眉题 → `quieter` / `typeset`，平淡或灰暗的调色板 → `colorize`，依此类推）。这是一个真实且当前的信号，优于猜测。如果 detect 出错，或目录树庞大且运行缓慢，请跳过它，并建议用户自行运行 `audit`；绝不要让建议流程因此受阻。

   只给出 2–3 个明确建议，并附上需要输入的确切命令。菜单仍作为备用选项；推荐内容应作为开篇重点。
2. **第一个词匹配某个命令**（上表中的命令，或 `pin` / `unpin` / `hooks`）：加载其参考文件（在原生平台上，加载表中的原生变体；遵循设置步骤 2 的单文件规则），并按其说明执行。命令名之后的所有内容都是目标。
3. **第一个词不匹配命令，但意图明显对应某个命令**（例如“修复间距”→ `layout`，“重写这条错误消息”→ `clarify`，“颜色感觉很平淡”→ `colorize`）：加载该命令的参考文件（遵循相同的原生变体规则），并像用户已调用该命令一样继续。如果可能符合两个命令，只询问一次用户要选择哪一个。
4. **没有明确的命令匹配**：视为通用设计调用。执行设置步骤、通用规则和已加载的设计语域参考文件，并将完整参数作为上下文。

到此时，设置内容（上下文收集、设计语域）已加载；子命令不会重新调用 `/impeccable`。

如果第一个词是 `craft` 或 `shape`，或路由规则 3 明确将用户意图映射到其中任一命令，仍然应先运行设置流程，但后续流程由匹配的参考文件（[reference/craft.md](reference/craft.md) 或 [reference/shape.md](reference/shape.md)）负责。两者都是从零构建流程：如果设置流程将 `init` 作为阻塞步骤调用，请先完成 init，刷新上下文，然后恢复原始命令及其目标。

`teach` 是 `init` 的弃用别名：如果用户输入它，请加载 [reference/init.md](reference/init.md)，并像用户运行了 `init` 一样继续。

## Pin / Unpin

**Pin** 会创建独立快捷方式，使 `/<command>` 可以直接调用 `/impeccable <command>`。**Unpin** 会将其移除。该脚本会写入项目中所有存在的运行环境目录。

```bash
node .claude/skills/impeccable/scripts/pin.mjs <pin|unpin> <command>
```

有效的 `<command>` 是上表中的任意命令。简明报告脚本结果。成功时确认新的快捷方式；出错时逐字转述 stderr。

## Hooks

`/impeccable hooks <on|off|status|ignore-rule|ignore-file|ignore-value|reset>` 用于管理此项目的设计检测器钩子。直接编辑 UI 文件后，该钩子会自动运行检测器，并以系统提醒的形式显示发现的问题。完整流程位于 [reference/hooks.md](reference/hooks.md)；当用户调用带有任意参数的 `/impeccable hooks` 时，请加载该文件。
