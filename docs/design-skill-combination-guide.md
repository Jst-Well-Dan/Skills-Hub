# GSAP、Impeccable 与 Taste 使用指南

本文介绍 Skills-Hub 中三个设计类 skill 合集的定位、重合关系、子 skill 功能，以及在不同项目和开发阶段中的推荐搭配方式。

> 一句话定位：Taste 决定“长什么样”，Impeccable 决定“是否好用、完整、可交付”，GSAP 决定“复杂动效怎样正确实现”。

## 1. 总体定位

| 合集 | 核心角色 | 主要解决的问题 | 最适合的场景 |
|---|---|---|---|
| Taste | 视觉导演 | 审美方向、品牌感、视觉差异化、避免模板化 | 营销站、作品集、品牌官网、视觉改版 |
| Impeccable | 产品设计师与质量负责人 | UX、信息架构、设计系统、评审、打磨和上线质量 | 网站、Dashboard、工具、后台、表单和产品界面 |
| GSAP | 动效工程师 | 时间线、滚动、SVG、拖拽、复杂编排、框架集成和性能 | 复杂交互、滚动叙事、动画密集型页面 |

推荐的职责链为：

```text
Taste：确定视觉方向
   ↓
Impeccable：完成产品设计、交互和质量验收
   ↓
GSAP：实现已经确认有价值的复杂动效
```

这不是固定的执行顺序。产品工具通常由 Impeccable 主导；纯品牌和营销页面通常由 Taste 主导；没有复杂动效时可以完全不使用 GSAP。

## 2. 覆盖与重合

### 2.1 Taste 与 Impeccable

这是重合最多的一组。二者都会处理：

- 排版、色彩、间距、网格与视觉层级
- 响应式、深色模式、可访问性和性能
- 品牌一致性与已有设计系统
- 改版前审计和完成后的质量检查
- 常见 AI 设计痕迹，例如滥用渐变、玻璃拟态、重复卡片和装饰性编号

区别在于：

- Taste 更强调视觉风格、审美取向和反模板化。
- Impeccable 更强调 UX、任务效率、完整状态、验证流程和生产质量。

当二者意见冲突时，按界面类型决定主导权：

- 营销站、作品集、品牌页：Taste 的视觉方向优先。
- Dashboard、后台、工具和多步骤流程：Impeccable 的 Product Register 优先。
- 已有品牌 token 或设计系统：现有规范优先于两个 skill。

### 2.2 Taste、Impeccable 与 GSAP

三者都涉及动画，但负责不同层级：

| 层级 | 负责内容 | 推荐 skill |
|---|---|---|
| 动效方向 | 动效是克制、活泼、实验性还是滚动叙事 | Taste |
| 交互意图 | 动效是否传达状态、反馈和层级，是否值得存在 | Impeccable `animate` |
| 技术实现 | Tween、Timeline、ScrollTrigger、插件、清理和性能 | GSAP |

简单的 hover、颜色变化、按钮反馈和淡入淡出优先使用原生 CSS。需要编排、运行时控制、滚动绑定、SVG 或拖拽时再使用 GSAP。

### 2.3 性能与无障碍

- Taste 提供总体性能预算、`prefers-reduced-motion` 和 Core Web Vitals 约束。
- Impeccable 的 `audit`、`optimize` 和 `adapt` 检查整页质量。
- GSAP Performance 具体处理 transform、opacity、布局抖动、批处理和动画实例清理。

## 3. GSAP 合集

GSAP 合集包含 8 个可独立使用的 skill。它们是动画 API 和工程实践的技术资料，不负责决定品牌或页面信息架构。

来源目录：[libraries/gsap-skills](../libraries/gsap-skills)

| 子 skill | 功能 | 什么时候使用 | 常见搭配 |
|---|---|---|---|
| `gsap-core` | `to`、`from`、`fromTo`、ease、duration、stagger、defaults、`matchMedia` | 单个或一组元素的基础动画；需要响应式动画或 reduced motion | 所有其他 GSAP skill 的基础 |
| `gsap-timeline` | 多步骤动画编排、位置参数、标签、嵌套和播放控制 | 多个动作需要串行、并行、暂停、反转或跳转 | `gsap-core`，必要时加 `gsap-scrolltrigger` |
| `gsap-scrolltrigger` | 滚动触发、scrub、pin、批量触发、横向滚动和滚动时间线 | 视差、固定章节、滚动叙事、进入视口动画 | `gsap-core` + `gsap-timeline` |
| `gsap-react` | React/Next.js 中的 `useGSAP`、ref、scope、context 和卸载清理 | React 或 Next.js 项目使用 GSAP | 根据需求再加 timeline、ScrollTrigger 或 plugins |
| `gsap-frameworks` | Vue、Nuxt、Svelte、SvelteKit 等框架的生命周期、作用域和清理 | 非 React 的组件框架中使用 GSAP | `gsap-core`，按需加入其他 GSAP skill |
| `gsap-plugins` | Flip、Draggable、Observer、SplitText、ScrambleText、MorphSVG、DrawSVG、MotionPath、CustomEase 等 | 元素重排、拖拽、文本拆分、SVG 路径、特殊缓动或高级滚动 | `gsap-core`，并只加载实际使用的插件 |
| `gsap-performance` | transform/opacity、will-change、批处理、减少布局计算和控制并发动画 | 动画卡顿、FPS 下降、长列表或大量 ScrollTrigger | 在动画完成后做专项性能检查 |
| `gsap-utils` | clamp、mapRange、normalize、interpolate、random、snap、wrap、pipe、toArray | 输入映射、吸附、循环、随机化、数值归一化和元素集合处理 | core、ScrollTrigger 和交互式动画 |

### GSAP 选择路径

```text
一个简单动画
└─ gsap-core

多个动画需要编排
└─ gsap-core + gsap-timeline

动画由滚动控制
└─ gsap-core + gsap-timeline + gsap-scrolltrigger

React / Next.js
└─ 在上述组合中加入 gsap-react

Vue / Svelte / Nuxt
└─ 在上述组合中加入 gsap-frameworks

Flip、拖拽、SVG、文字拆分或特殊缓动
└─ 再加入 gsap-plugins

出现卡顿或动画规模较大
└─ 使用 gsap-performance 检查
```

不必每次加载全部 8 个 skill。常规项目通常只需要 core 加一个任务相关模块。

## 4. Taste 合集

Taste 合集包含 13 个可安装 skill。它既有通用视觉规范，也有互斥的风格路线、图像生成工作流和兼容性工具。

来源目录：[libraries/taste-skill](../libraries/taste-skill)

### 4.1 核心设计与改版

| 子 skill | 功能 | 什么时候使用 | 注意事项 |
|---|---|---|---|
| `design-taste-frontend` | 当前默认的 anti-slop 前端设计 skill；先判断页面、受众和视觉语言，再通过设计差异度、动效强度和视觉密度三个旋钮实施 | Landing Page、作品集、品牌页和网站改版 | 不以 Dashboard、数据表格和多步骤产品 UI 为主要范围 |
| `redesign-existing-projects` | 审计现有界面，在不破坏功能的前提下提高视觉品质 | 用户明确要求优化、现代化或重新设计已有项目 | 与 Impeccable `critique` 有重合；前者偏视觉，后者偏 UX 评审 |
| `high-end-visual-design` | 提供高端机构式排版、间距、阴影、卡片和动画规则 | 页面功能已明确，但整体看起来廉价、普通或缺乏精致度 | 它是强化视觉品质的规则集，不替代完整 UX 流程 |

### 4.2 风格路线

| 子 skill | 功能 | 什么时候使用 | 注意事项 |
|---|---|---|---|
| `minimalist-ui` | 暖色单色、编辑式排版、扁平 Bento、柔和色彩，无渐变和重阴影 | 内容、作品集、文档、工具需要克制和安静的高级感 | 不要同时启用工业粗野主义路线 |
| `industrial-brutalist-ui` | 瑞士印刷、军事终端、机械网格、强字号对比和模拟退化效果 | 数据密集型 Dashboard、实验作品集、文化或编辑网站需要强烈个性 | 风格很强，应先确认品牌和受众适合 |
| `gpt-taste` | AIDA 页面结构、宽幅编辑式排版、非重复布局、Bento 和强 GSAP ScrollTrigger 叙事 | 明确追求 Awwwards、实验性营销页或强滚动体验 | 与官方 GSAP skill 重合较大；动画 API、清理和性能以 GSAP 合集为准 |

这些风格 skill 是候选路线，不是叠加增益。一个页面应先选择一种主要视觉语言。

### 4.3 图像、品牌与视觉稿

| 子 skill | 功能 | 什么时候使用 | 产出 |
|---|---|---|---|
| `brandkit` | 创建品牌规范板、Logo 系统、视觉世界、身份提案和高级 Mockup | 新品牌、品牌重塑、需要先定义视觉资产时 | 品牌视觉图或展示板 |
| `imagegen-frontend-web` | 为网站每个 section 分别生成横向设计参考图，维持统一叙事和色板 | 编码前需要完整网站视觉稿，尤其是营销页 | 一节一张独立设计图，不直接写代码 |
| `imagegen-frontend-mobile` | 生成具有统一视觉语言的移动端界面和流程图 | iOS、Android 或跨平台 App 概念设计 | 手机界面图片，不直接写代码 |
| `image-to-code` | 先生成并分析设计图，再实现尽可能一致的网页 | 视觉还原度比快速编码更重要，或用户明确要求 image-first | 设计图加对应实现代码 |

推荐图像工作流：

```text
需要品牌基础
└─ brandkit
   ↓
需要网页视觉稿
└─ imagegen-frontend-web
   ↓
需要根据视觉稿实现
└─ image-to-code
```

如果已有可靠的 Figma、截图或设计系统，不必为了走流程重新生成图片。

### 4.4 工作流和兼容工具

| 子 skill | 功能 | 什么时候使用 | 注意事项 |
|---|---|---|---|
| `stitch-design-taste` | 为 Google Stitch 创建语义化 `DESIGN.md`，包含排版、色彩、布局和动效规范 | 项目明确使用 Google Stitch | 不使用 Stitch 时通常不需要 |
| `full-output-enforcement` | 禁止占位符和省略输出，要求完整代码，并规定超出长度时的分段方式 | 用户需要完整、不可截断的大规模输出 | 它不是设计能力，只控制交付完整性 |
| `design-taste-frontend-v1` | 保留 Taste v1 的原始行为 | 老项目依赖 v1 的具体规则或需要复现旧输出 | 新项目默认使用 `design-taste-frontend`，不要同时启用 v1 和当前版 |

### Taste 选择路径

```text
一般营销站、作品集或视觉改版
└─ design-taste-frontend

已有网站需要升级
└─ design-taste-frontend + redesign-existing-projects

明确的安静极简方向
└─ minimalist-ui

明确的工业粗野主义方向
└─ industrial-brutalist-ui

强实验性滚动营销页
└─ gpt-taste + 对应 GSAP skill

需要先做品牌或设计图
└─ brandkit / imagegen-frontend-web / imagegen-frontend-mobile

视觉稿驱动编码
└─ image-to-code
```

## 5. Impeccable 合集

Impeccable 在 Skills-Hub 中表现为一个主 skill，而不是几十个独立安装的 skill。主 skill 根据用户意图路由到 23 个命令 reference，并加载 Brand 或 Product 设计规范。

来源：[Impeccable 主 skill](../libraries/impeccable/plugin/skills/impeccable/SKILL.md)

### 5.1 Build：规划和建设

| 命令 | 功能 | 什么时候使用 |
|---|---|---|
| `shape [feature]` | 编码前规划需求、用户路径、状态和界面结构 | 新功能还没有明确 UX 方案，或需要先确定范围 |
| `craft [feature]` | 从 shape、视觉方向、生产代码到浏览器检查的完整实施流程 | 要求端到端构建一个可交付功能 |
| `init` | 建立项目上下文，生成或完善 PRODUCT.md、DESIGN.md 和后续建议 | 项目首次使用 Impeccable，缺少产品或设计说明 |
| `document` | 从现有代码提炼并生成 DESIGN.md | 项目已有界面和 token，但缺少设计文档 |
| `extract [target]` | 从现有实现提取可复用 token、模式和组件 | 多处出现重复样式，需要形成设计系统 |

### 5.2 Evaluate：评审和审计

| 命令 | 功能 | 什么时候使用 |
|---|---|---|
| `critique [target]` | 从 UX、层级、信息架构、认知负担等角度进行启发式评审和评分 | 想知道界面“哪里不好、为什么不好、先改什么” |
| `audit [target]` | 检查可访问性、响应式、性能和技术质量 | 上线前、改版后，或出现跨设备和无障碍问题 |

`critique` 主要判断设计和体验是否正确，`audit` 主要判断实现是否合格。二者通常可以连续使用。

### 5.3 Refine：收敛和生产化

| 命令 | 功能 | 什么时候使用 |
|---|---|---|
| `polish [target]` | 上线前处理细节、一致性和最后一轮质量问题 | 功能已完成，需要达到正式交付标准 |
| `bolder [target]` | 通过更明确的层级、比例和字体增强视觉力度 | 页面安全、平淡、没有记忆点 |
| `quieter [target]` | 减少噪声、装饰和过强视觉竞争 | 页面过于吵闹、信息难以聚焦 |
| `distill [target]` | 删除复杂性，让界面回到核心任务 | 页面元素、层级或操作过多 |
| `harden [target]` | 补齐错误、空状态、加载、边界数据、国际化等生产状态 | Happy path 已完成，但尚不适合真实用户使用 |
| `onboard [target]` | 设计首次使用、空状态、引导和激活流程 | 新用户不知道如何开始或无法快速到达 aha moment |

### 5.4 Enhance：专项视觉增强

| 命令 | 功能 | 什么时候使用 |
|---|---|---|
| `animate [target]` | 添加传达状态、反馈和层级的有目的动效 | 界面反馈生硬或状态变化难以理解；复杂实现可继续交给 GSAP |
| `colorize [target]` | 为单调界面建立有角色分工的色彩体系 | 页面过灰，重点、状态和品牌缺乏区分 |
| `typeset [target]` | 改善字体选择、字号层级、行宽和排版节奏 | 信息可读性弱、标题与正文层级不清 |
| `layout [target]` | 修复间距、对齐、密度、网格和视觉流 | 组件本身没问题，但页面整体松散或拥挤 |
| `delight [target]` | 增加符合品牌的个性、惊喜和微交互 | 产品可用但缺少情感和辨识度 |
| `overdrive [target]` | 在确认方案后实现高强度、非常规的视觉效果 | 旗舰页、活动页或实验性体验需要突破常规 |

### 5.5 Fix：解决具体问题

| 命令 | 功能 | 什么时候使用 |
|---|---|---|
| `clarify [target]` | 改善按钮、标签、提示、错误信息和 UX 文案 | 用户看不懂操作、状态或下一步 |
| `adapt [target]` | 针对设备、屏幕、平台和使用环境重新设计体验 | 桌面转移动端、Web 转触屏，或特定断点体验失效 |
| `optimize [target]` | 诊断并修复 UI 性能问题 | 首屏慢、交互卡顿、动画掉帧或资源过重 |

### 5.6 Iterate：浏览器内迭代

| 命令 | 功能 | 什么时候使用 |
|---|---|---|
| `live` | 在运行中的页面选择元素、生成视觉变体并比较 | 文字描述不足以决策，需要直接在浏览器中尝试多个方案 |

### 5.7 内部规范和管理能力

下面这些 reference 主要由 Impeccable 主 skill 自动加载，不必把它们当成独立设计命令：

| 模块 | 作用 |
|---|---|
| `brand` | 营销站、品牌页、作品集等“设计本身就是产品”的规范 |
| `product` | Dashboard、后台、工具等“设计服务于任务”的规范 |
| `interaction-design` | 覆盖默认、hover、focus、active、loading、error、disabled、empty 等交互状态 |
| `codex` | Codex 环境中的视觉方向、资产生产和实施停点 |
| `hooks` | 管理界面代码编辑后的设计质量检测 hook |
| `pin` / `unpin` | 将常用 Impeccable 命令固定或取消为独立快捷命令 |

### Impeccable 选择路径

```text
不知道先做什么或缺少项目设计上下文
└─ init

新功能尚未设计
└─ shape
   ↓
需要继续完成实现
└─ craft

已有界面，需要找问题
├─ 体验和设计问题：critique
└─ 技术质量问题：audit

问题已经明确
├─ 间距和结构：layout
├─ 排版：typeset
├─ 颜色：colorize
├─ 动效：animate
├─ 文案：clarify
├─ 响应式：adapt
└─ 性能：optimize

准备上线
└─ harden + audit + polish
```

## 6. 按项目类型搭配

### 6.1 营销网站、品牌官网和作品集

1. Taste `design-taste-frontend` 确定 Design Read 和视觉路线。
2. Impeccable `shape` 或 `craft` 梳理内容、转化路径和完整交互。
3. 复杂动效按需使用 GSAP core、timeline 或 ScrollTrigger。
4. 使用 Impeccable `critique`、`audit` 和 `polish` 收尾。

### 6.2 Dashboard、工具和 SaaS 产品

1. Impeccable `shape` 或 `craft` 作为主流程，并使用 Product Register。
2. Taste 只做视觉反模板检查，不主导复杂业务界面。
3. 状态切换、列表重排或数据可视化需要复杂动画时使用 GSAP。
4. 使用 Impeccable `harden`、`adapt` 和 `audit` 验证真实使用场景。

### 6.3 Awwwards 或实验性滚动网站

1. 使用 Taste `gpt-taste` 或主 Taste skill 确定创意方向。
2. 使用 Impeccable `overdrive` 明确方案、价值与技术风险。
3. 使用 GSAP timeline、ScrollTrigger、plugins 和 performance 实现。
4. 使用 Impeccable `adapt` 为移动端和 reduced motion 提供降级方案。

### 6.4 已有网站改版

1. Taste `redesign-existing-projects` 做视觉审计。
2. Impeccable `critique` 做 UX 和信息结构评审。
3. 使用 `layout`、`typeset`、`colorize` 等命令定点修复。
4. 仅在明确有价值时增加 GSAP 动效。
5. 使用 Impeccable `audit` 和 `polish` 完成验收。

### 6.5 Skills-Hub 网站

Skills-Hub 是开发者资源目录和检索工具，更接近产品界面。推荐：

- 主导：Impeccable Product Register。
- 视觉辅助：Taste `design-taste-frontend`。
- 常用流程：`critique` → `layout` / `typeset` → `audit` → `polish`。
- 动效策略：简单反馈使用 CSS；只有复杂的结果重排、抽屉编排或滚动叙事才引入 GSAP。

搜索速度、信息密度、卡片可读性和 GitHub 跳转效率，应优先于装饰性动画。

## 7. 使用原则与常见误区

### 应该这样做

- 每个阶段只指定一个主导 skill，其他 skill 提供专项支持。
- 先确定页面类型、用户任务、品牌约束和质量目标。
- 动效先判断价值，再选择 CSS 或 GSAP。
- 风格 skill 只选择一个主要方向。
- 已有代码、品牌 token 和设计系统拥有最高优先级。

### 避免这样做

- 同时启用 Taste v1 和当前版。
- 同时启用 `minimalist-ui` 与 `industrial-brutalist-ui`。
- 把 Taste 主 skill 用作复杂 Dashboard 的唯一设计规范。
- 同时让 `gpt-taste` 和 GSAP skill 各自生成一套动画实现。
- 为了使用 GSAP 而增加没有信息价值的动画。
- 一次性加载三个合集的所有子 skill，导致规则冲突和上下文膨胀。

## 8. 快速决策表

| 用户需求 | 首选 | 按需补充 |
|---|---|---|
| “做一个不模板化的 Landing Page” | Taste `design-taste-frontend` | Impeccable `craft`、GSAP |
| “改进这个 Dashboard” | Impeccable `critique` 或 `craft` | Taste 视觉检查、GSAP |
| “这个页面看起来很普通” | Taste 或 Impeccable `bolder` | `typeset`、`colorize`、`layout` |
| “页面太花、太吵” | Impeccable `quieter` / `distill` | Taste anti-slop 检查 |
| “做滚动叙事和固定章节” | GSAP ScrollTrigger + Timeline | Taste 定调、Impeccable `animate` |
| “React 动画卸载后出错” | `gsap-react` | `gsap-performance` |
| “需要 Logo 和品牌视觉板” | Taste `brandkit` | `imagegen-frontend-web` |
| “先出整站视觉稿再写代码” | Taste `imagegen-frontend-web` + `image-to-code` | Impeccable `critique` |
| “上线前全面检查” | Impeccable `harden` + `audit` + `polish` | GSAP Performance |
| “移动端体验不对” | Impeccable `adapt` | 对应 GSAP 框架 skill |

## 9. 最终建议

长期使用时，可以固定以下治理规则：

> Taste 拥有视觉方向建议权；Impeccable 拥有产品 UX 和最终验收权；GSAP 只在复杂动效被确认有价值后，拥有动画实现权。

这样可以利用三个合集的独特能力，同时减少重复判断、规则冲突和不必要的上下文占用。
