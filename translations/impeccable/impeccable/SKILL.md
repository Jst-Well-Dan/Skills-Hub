<!-- source-sha256: 44dec2359cff5c3ede5abbc72a8525c46de38bdaa6a3fcb454c1f581dbc65db3 -->
---
name: impeccable
description: 当用户希望设计、重新设计、塑造、评析、审计、润色、澄清、提炼、强化、优化、适配、添加动画、着色、提取或以其他方式改进前端界面时使用。涵盖网站、落地页、仪表盘、产品 UI、应用外壳、组件、表单、设置、引导流程和空状态。处理 UX 审查、视觉层级、信息架构、认知负荷、无障碍、性能、响应式行为、主题、反模式、排版、字体、间距、布局、对齐、颜色、动效、微交互、UX 文案、错误状态、边界情况、i18n，以及可复用的设计系统或令牌。也适用于需要变得更大胆或更令人愉悦的平淡设计、应该变得更克制的喧闹设计、在实时浏览器中迭代 UI 元素，或需要在技术上呈现非凡质感的宏大视觉效果。不适用于纯后端或非 UI 任务。
version: 3.8.0
user-invocable: true
argument-hint: "[craft|shape · audit|critique · animate|bolder|colorize|delight|layout|overdrive|quieter|typeset · adapt|clarify|distill · harden|onboard|optimize|polish · init|document|extract|live] [target]"
license: Apache 2.0
allowed-tools:
  - Bash(npx impeccable *)
---

设计并迭代生产级前端界面。真正可运行的代码、明确坚定的设计选择、卓越的工艺水准。

## 设置

继续之前，你必须完成以下步骤：

1. 每个会话运行一次 `node .claude/skills/impeccable/scripts/context.mjs`。如果请求点名或暗示了 monorepo 中的某个文件、路由或应用，请推断具体路径，改为运行 `node .claude/skills/impeccable/scripts/context.mjs --target <path>`。如果你已经在本次对话中看到过它的输出，请勿重新运行。该脚本要么以 Markdown 块形式打印项目的 PRODUCT.md（存在 DESIGN.md 时也会打印），要么告知你该文件缺失。遵循它打印的所有指示。**如果它报告 `NO_PRODUCT_MD`，请停止，并在做任何其他事情之前遵循 `reference/init.md`。**如果输出以 `UPDATE_AVAILABLE` 指令结尾，请遵循该指令（询问用户一次是否更新，然后继续）。它绝不会阻塞当前任务。
2. 如果用户调用了子命令（`craft`、`shape`、`audit`、`polish`……），接下来你必须读取 `reference/<command>.md`。此项不可选。该参考文件定义了命令流程；不读取它，你就会漏掉用户预期的步骤。
3. 熟悉代码中任何现有的设计系统、约定和组件。至少读取一个项目文件（CSS / tokens / theme / 一个有代表性的组件或页面）。**即使你已在第 2 步加载子命令参考文件，此项仍为必需。**不要重复造轮子；现有方案有效时就使用它，只有 UX 能因此获益时才另辟蹊径。
4. 阅读匹配的语域参考文件。**此项不可选；跳过它会产生千篇一律的输出。**如果项目是营销网站、落地页、活动页面、长篇内容或作品集（设计就是产品），请阅读 `reference/brand.md`。如果是应用 UI、管理后台、仪表盘或工具（设计服务于产品），请阅读 `reference/product.md`。按首次匹配选择：(1) 任务线索（“landing page”还是“dashboard”）；(2) 当前聚焦的界面（正在处理的页面、文件或路由）；(3) PRODUCT.md 中的 `register` 字段。
5. **如果项目是全新的（第 3 步未发现现有 CSS tokens / theme / 已确定的品牌颜色）**，请运行 `node .claude/skills/impeccable/scripts/palette.mjs`，获取品牌种子色和配色指导。这是主品牌色的锚点。按照脚本说明，围绕它构建其余调色板（bg、surface、ink、accent、muted）。全程使用 OKLCH。**仅当第 3 步在现有 tokens 中发现已确定的品牌颜色时才跳过此步骤；在这种情况下，应优先保持品牌识别度。**

## 设计指导

产出可直接发布的生产级代码，而不是原型或起点。除非用户要求，否则不要走捷径（有疑问时就询问）。在得到完整实现之前不要停止（美观、响应式、快速、精确、无缺陷、符合品牌）。你应认真对待细节：制作的每个页面、区块或组件，都要使用可用工具（浏览器截图、计算机操作等）进行实战检验。Claude 有能力完成非凡的作品。不要有所保留。

### 通用规则

#### 颜色

- **验证对比度。** 正文文本与背景的对比度必须达到 ≥4.5:1；大号文本（≥18px 或粗体 ≥14px）需要达到 ≥3:1。占位符文本同样需要达到 4.5:1，不能采用默认的柔和灰色。最常见的问题是：带色调的近白色背景上使用柔和灰色正文。如果对比度哪怕只是接近临界值，也应把正文颜色沿色阶向 ink 端加深；为了“优雅”而使用浅灰色，是 AI 设计显得难以阅读的首要原因。
- 彩色背景上的灰色文本看起来会褪色。请使用该背景自身色相的更深色阶，或使用文本颜色的透明版本。

#### 排版

- 将正文行长限制在 65–75ch。
- 不要搭配相似但不完全相同的字体（两个几何无衬线字体、两个人文无衬线字体）。应沿对比轴搭配（衬线 + 无衬线、几何 + 人文），或使用同一字体家族的不同字重。
- Hero / 展示标题上限：clamp() 的最大值 ≤ 6rem（约 96px）。再大，页面就是在吼叫，而不是在设计。
- 展示标题字间距下限：≥ -0.04em。再紧，字母就会相互接触；那是拥挤，不是“设计感”。
- 在 h1–h3 上使用 `text-wrap: balance`，使每行长度更均衡；在长篇正文上使用 `text-wrap: pretty`，减少孤行和孤字。

#### 布局

- 通过变化间距创造节奏。
- 卡片是偷懒的答案。只有当它们确实是最佳的交互表意形式时才使用。嵌套卡片永远是错的。
- 一维布局使用 Flexbox，二维布局使用 Grid。当 `flex-wrap` 更简单时，不要默认使用 Grid。
- 对于无需断点的响应式网格，使用：`repeat(auto-fit, minmax(280px, 1fr))`。
- 建立语义化的 z-index 层级（dropdown → sticky → modal-backdrop → modal → toast → tooltip）。绝不要使用 999 或 9999 之类的任意值。

#### 动效

- 动效应有明确意图，不能事后补上。应将其视为构建过程的一部分。
- 除非确有必要，否则不要为 CSS 布局属性添加动画。
- 使用指数型曲线缓出（ease-out-quart / quint / expo）。不要使用弹跳或弹性效果。
- 对更高级的动效需求使用库（例如 motion、gsap、anime.js、lenis 等）。
- 减少动态效果不是可选项。每个动画都需要一个 `@media (prefers-reduced-motion: reduce)` 替代方案：通常是交叉淡入淡出或即时切换。
- 对同一列表中的项目使用错峰动画是合理的。真正暴露问题的是机械统一的反射式做法（每个区块都套用同一种入场动画），而不是动效本身；每次揭示都应契合它所揭示的内容。抑制这种机械反射，绝不意味着应交付一个完全没有动效的页面。
- 揭示动画必须增强默认已经可见的内容。不要让内容可见性依赖由类触发的过渡；过渡在隐藏标签页和无头渲染器中会暂停，导致揭示永不触发，最终交付空白区块。
- 高级动效材质不只是 transform/opacity。当 blur、backdrop-filter、clip-path、mask 和 shadow/glow 能显著改善效果并保持流畅时，它们也属于可用的表达手段。

#### 交互

- 在 `overflow: hidden` 或 `overflow: auto` 容器内用 `position: absolute` 渲染的下拉菜单会被裁切。使用原生 `<dialog>` / popover API、`position: fixed` 或 portal 来摆脱该层叠上下文。

### 仅限新项目（不存在既有工作时）

#### 颜色与主题

- 使用 OKLCH。
- **奶油色 / 沙色 / 米色的 body 背景，是 2026 年已经泛滥的 AI 默认选择。**整个暖中性色带（OKLCH L 0.84-0.97、C < 0.06、色相 40-100），无论你如何命名，看起来都会像奶油、沙子、纸张或羊皮纸。诸如 `--paper`、`--cream`、`--sand`、`--bone`、`--flour`、`--linen`、`--parchment`、`--wheat`、`--biscuit`、`--ivory` 这样的 token 名称本身就是明显信号。如果需求是“温暖、传统、家庭式海岸意大利风”、“杂志式温暖”或“编辑式克制”，不要把它转化成带暖色调的近白色背景；那正是 AI 的套路。请选择：(a) 使用饱和品牌色作为 body 背景（陶土色、牛血红、深赭色、近黑色）；(b) 使用 chroma 为 0 的真正灰白色（或让 chroma 倾向品牌自身色相，而不是默认偏暖）；或 (c) 使用明显属于品牌自身色彩的较深中间调染色中性色。品牌的“温暖感”应由强调色 + 排版 + 图像承载，而不是由 body 背景承载。
- 染色中性色：朝品牌色相加入 0.005–0.015 的 chroma。不要因为“品牌给人这种感觉”就默认向暖色或冷色偏移；那会造成跨项目的单一化。
- 选择主题时：深色与浅色都绝不是默认答案。不能因为“工具用深色看起来很酷”就选深色，也不能为了“稳妥”就选浅色。在选择之前，先写一句具体的物理场景：谁在使用它、在哪里、环境光线如何、处于什么情绪。如果这句话无法迫使你得出答案，说明它还不够具体。继续补充细节，直到答案明确。
- 在挑选具体颜色之前，先选择一种**颜色策略**。承诺程度由低到高分四级：
  - **克制（Restrained）**：染色中性色 + 一个占比 ≤10% 的强调色。产品默认；品牌极简主义。
  - **鲜明（Committed）**：一种饱和色覆盖 30–60% 的界面。以身份识别为核心的品牌页面默认选择。
  - **完整调色板（Full palette）**：3–4 个命名角色，每一种都有意识地使用。适合品牌活动；产品数据可视化。
  - **浸染（Drenched）**：界面本身就是颜色。适合品牌 Hero 区和活动页面。

### 绝对禁用

匹配即拒绝。如果你正准备编写以下任何一种内容，请改用不同结构重写该元素。

- **侧边条边框。** 在卡片、列表项、提示块或警告中，将大于 1px 的 `border-left` 或 `border-right` 用作彩色强调。绝不要有意这样做。改用完整边框、染色背景、前置数字/图标，或什么都不用。
- **渐变文本。** 将 `background-clip: text` 与渐变背景结合。它只具装饰性，从不传递意义。使用单一纯色。通过字重或字号强调。
- **默认使用玻璃拟态。** 将模糊和玻璃卡片用于装饰。只能少量且有明确目的地使用，否则完全不用。
- **Hero 指标模板。** 大数字、小标签、辅助统计数据、渐变强调。典型的 SaaS 陈词滥调。
- **完全相同的卡片网格。** 尺寸相同、由图标 + 标题 + 文本组成的卡片，无休止地重复。
- **每个区块上方都放置小号、全大写、宽字距的眉题。** 这种 2023 年风格的引题（每个标题上方都有小号全大写宽字距文本，如“ABOUT”“PROCESS”“PRICING”）如今已成为泛滥的 AI 脚手架；无论需求如何，它都会出现在 55–95% 的生成结果中，而这正是明显模式的定义。把一个命名明确的引题作为有意设计的品牌系统，是品牌声音；每个区块都有眉题，则是 AI 语法。请选择不同的节奏。
- **默认使用编号区块标记作为脚手架（01 / 02 / 03）。** 在每个区块上方放置 `01 · About / 02 · Process / 03 · Pricing`，是比眉题套路更深一层的问题：因为“落地页都这么做”就顺手采用它，意味着你在条件反射式地搭脚手架。只有当区块确实构成序列（真正的三步流程、有序流程、类型明确的时间线），且顺序承载读者需要的信息时，数字才有存在价值。一个页面中有意设计的一组编号序列是品牌声音；整个网站每个区块都使用编号眉题，则是 AI 语法。
- **文本溢出容器。** 长标题单词、大幅 clamp 缩放和狭窄网格组合在一起，会导致标题在平板或移动端溢出。请在每个断点测试标题文案；如果发生溢出，请降低 clamp 最大值或重写文案。视口是设计的一部分。

### AI 粗制滥造测试

如果有人看着这个界面，可以毫不怀疑地说“这是 AI 做的”，那它就失败了。跨语域的失败模式，就是上面的绝对禁用项。各语域特有的失败模式记录在相应参考文件中。

**类别反射检查。** 从两个层次执行；第二层能捕捉第一层遗漏的问题。

- **一阶：**如果有人仅凭类别就能猜出主题 + 调色板，那就是第一层训练数据反射。重新设计场景描述和颜色策略，直到答案无法仅凭领域被明显猜中。
- **二阶：**如果有人能根据“类别 + 反例”猜出审美家族（“不是 SaaS 奶油色的 AI 工作流工具 → 编辑式排版”、“不是海军蓝配金色的金融科技 → 终端原生深色模式”），那就是更深一层的陷阱。第一层反射避开了，第二层却没有。继续修改，直到两个答案都不明显。品牌语域中的[反射拒绝审美路线](reference/brand.md)列表可以捕捉当前已经泛滥的风格家族。

## 命令

| 命令 | 类别 | 描述 | 参考文件 |
|---|---|---|---|
| `craft [feature]` | 构建 | 先塑造，再端到端构建功能 | [reference/craft.md](reference/craft.md) |
| `shape [feature]` | 构建 | 编写代码前规划 UX/UI | [reference/shape.md](reference/shape.md) |
| `init` | 构建 | 设置项目上下文：PRODUCT.md、DESIGN.md、实时配置、后续步骤 | [reference/init.md](reference/init.md) |
| `document` | 构建 | 根据现有项目代码生成 DESIGN.md | [reference/document.md](reference/document.md) |
| `extract [target]` | 构建 | 将可复用的 tokens 和组件提取到设计系统中 | [reference/extract.md](reference/extract.md) |
| `critique [target]` | 评估 | 带启发式评分的 UX 设计审查 | [reference/critique.md](reference/critique.md) |
| `audit [target]` | 评估 | 技术质量检查（a11y、性能、响应式） | [reference/audit.md](reference/audit.md) |
| `polish [target]` | 优化 | 发布前的最终质量检查 | [reference/polish.md](reference/polish.md) |
| `bolder [target]` | 优化 | 强化过于保守或平淡的设计 | [reference/bolder.md](reference/bolder.md) |
| `quieter [target]` | 优化 | 弱化过于激进或刺激过度的设计 | [reference/quieter.md](reference/quieter.md) |
| `distill [target]` | 优化 | 提炼本质，移除复杂性 | [reference/distill.md](reference/distill.md) |
| `harden [target]` | 优化 | 达到生产就绪：错误、i18n、边界情况 | [reference/harden.md](reference/harden.md) |
| `onboard [target]` | 优化 | 设计首次使用流程、空状态和激活体验 | [reference/onboard.md](reference/onboard.md) |
| `animate [target]` | 增强 | 添加目的明确的动画和动效 | [reference/animate.md](reference/animate.md) |
| `colorize [target]` | 增强 | 为单色 UI 策略性地添加颜色 | [reference/colorize.md](reference/colorize.md) |
| `typeset [target]` | 增强 | 改进排版层级和字体 | [reference/typeset.md](reference/typeset.md) |
| `layout [target]` | 增强 | 修复间距、节奏和视觉层级 | [reference/layout.md](reference/layout.md) |
| `delight [target]` | 增强 | 增加个性和令人难忘的细节 | [reference/delight.md](reference/delight.md) |
| `overdrive [target]` | 增强 | 突破常规限制 | [reference/overdrive.md](reference/overdrive.md) |
| `clarify [target]` | 修复 | 改进 UX 文案、标签和错误消息 | [reference/clarify.md](reference/clarify.md) |
| `adapt [target]` | 修复 | 针对不同设备和屏幕尺寸进行适配 | [reference/adapt.md](reference/adapt.md) |
| `optimize [target]` | 修复 | 诊断并修复 UI 性能问题 | [reference/optimize.md](reference/optimize.md) |
| `live` | 迭代 | 视觉变体模式：在浏览器中选择元素并生成替代方案 | [reference/live.md](reference/live.md) |

另有三个管理命令：`pin <command>`、`unpin <command>` 和 `hooks <on|off|status|...>`，详见下文。

### 路由规则

1. **无参数**：用户是在询问“我应该做什么？”菜单应根据上下文调整，而不是静态不变。设置流程已经运行过 `context.mjs`；如果它报告了 `NO_PRODUCT_MD`，说明你已经进入 init（设置）流程，请完成该流程并跳过本规则。否则，运行一次 `node .claude/skills/impeccable/scripts/context-signals.mjs` 并读取其 JSON，然后先给出**价值最高的 2–3 个后续命令**，每个命令附上一条从信号中提取的单行理由，随后提供完整菜单（上表，按类别分组）。**绝不要自动运行命令；推荐只是建议，需要用户确认。**

   根据这些信号进行判断；没有必须服从的分数：
   - `setup.hasDesign` 为 false，而 `setup.hasCode` 为 true → `document`（记录视觉系统）。
   - `critique.latest` 为 `null` → 项目从未接受过评析；对于已经完成设置且拥有真实界面的项目，推荐 `/impeccable critique <surface>` 是很可靠的默认选择。
   - `critique.latest` 的 `score` 较低，或 `p0` / `p1` 非零 → `polish`（它会读取该快照作为待办列表）；如果快照看起来已过时，则重新运行 `critique`。
   - `git.changedFiles` 指向某一个界面 → 将 `audit` 或 `polish` 明确限定到这些文件，并点名列出。
   - `devServer.running` 为 true → 可以使用 `live` 在浏览器中进行迭代；如果为 false，不要优先推荐 `live`。
   - 否则，完全按照 init 中“Recommend starting points”步骤的意图分组（构建新内容 / 改进现有内容 / 进行视觉迭代），并根据 `setup.register` 定制。

   **如果 `scan.targets` 非空，运行一次 `node .claude/skills/impeccable/scripts/detect.mjs --json <scan.targets joined by spaces>`**（针对本地文件的内置检测器：无网络、无 npx）。`scan.via` 会说明这些目标来自哪里：`git-changes`（脏工作树中的标记/样式文件，也是最相关的一组）、`source-dir`（例如 `src`、`app`）、`html` 或 `root`。将检测结果纳入推荐：存在大量质量 / 对比度问题 → `audit` 或 `polish`；出现特定粗制滥造模式 → 使用匹配命令（渐变文本或眉题 → `quieter` / `typeset`，扁平或灰暗调色板 → `colorize`，依此类推）。这是比猜测更可靠的真实当前信号。如果 detect 出错，或文件树过大导致速度缓慢，请跳过它，并建议用户自行运行 `audit`；绝不要让推荐因它而阻塞。

   推荐内容保持为 2–3 个明确选项，并给出要输入的确切命令。菜单继续作为后备；推荐应放在最前面。
2. **第一个词匹配某个命令**（上表或 `pin` / `unpin` / `hooks`）：加载其参考文件并遵循其中的说明。命令名称之后的所有内容都是目标。
3. **第一个词不匹配，但意图明显映射到某个命令**（例如“修复间距”→ `layout`，“重写这条错误消息”→ `clarify`，“颜色感觉太平淡”→ `colorize`）：加载该命令的参考文件，并像用户直接调用它一样执行。如果有两个命令都可能适用，只询问一次用户选择哪个。
4. **没有明确匹配的命令**：视为通用设计调用。应用设置步骤、通用规则和已加载的语域参考文件，并将完整参数用作上下文。

此时设置内容（上下文收集、语域）已经加载；子命令不会重新调用 `/impeccable`。

如果第一个词是 `craft`，仍需先运行设置流程，但后续流程由 [reference/craft.md](reference/craft.md) 负责。如果设置流程调用 `init` 作为阻塞项，请完成 init、刷新上下文，然后恢复原始命令和目标。

`teach` 是 `init` 的弃用别名：如果用户输入它，请加载 [reference/init.md](reference/init.md)，并像用户运行了 `init` 一样继续。

## Pin / Unpin

**Pin** 会创建一个独立快捷方式，使 `/<command>` 可以直接调用 `/impeccable <command>`。**Unpin** 会移除该快捷方式。脚本会写入项目中存在的每个工具目录。

```bash
node .claude/skills/impeccable/scripts/pin.mjs <pin|unpin> <command>
```

有效的 `<command>` 是上表中的任意命令。简洁报告脚本结果。成功时确认新的快捷方式；出错时逐字转达 stderr。

## Hooks

`/impeccable hooks <on|off|status|ignore-rule|ignore-file|ignore-value|reset>` 用于管理此项目的设计检测器 hook。该 hook 会在直接编辑 UI 文件后自动运行检测器，并以系统提醒形式呈现发现的问题。完整流程位于 [reference/hooks.md](reference/hooks.md)；当用户调用带任意参数的 `/impeccable hooks` 时，请加载该文件。
