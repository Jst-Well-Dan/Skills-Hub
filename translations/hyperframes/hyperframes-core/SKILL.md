<!-- source-sha256: 4b710ea43ded213525c1101bb39116898085ec8031f1d28a2a1e0ea39aa54d68 -->
---
name: hyperframes-core
description: HyperFrames 合成契约——构建一个可渲染项目。用于合成结构、`data-*` 时间属性、`class="clip"`、轨道、子合成、变量、由框架控制的媒体播放、确定性渲染规则与验证。还涵盖 Tailwind 项目以及 STORYBOARD.md / SCRIPT.md 计划格式。编写合成 HTML 前请先阅读。
---

# HyperFrames 核心

HyperFrames 从 HTML 渲染视频。合成是一个 HTML 文件：其 DOM 使用 `data-*` 属性声明时间，其动画运行时可寻址，且其媒体播放由框架控制。

本技能是**技术契约**——如何构建一个 hyperframes 项目。以下正文是构建指南；各主题的详细内容位于 `references/`（索引见下），按需阅读。其他关注点位于同级领域技能中——`hyperframes-animation`、`hyperframes-creative`、`media-use`、`hyperframes-cli`、`hyperframes-registry`。`/hyperframes` 中的能力地图说明了各自涵盖的内容。

## 参考资料

| 文件                                 | 阅读它以便…                                                                                                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/minimal-composition.md`  | 从最小的可渲染合成骨架开始                                                                                                                                                          |
| `references/composition-patterns.md` | 选择单体或模块化；构建模块化 `index.html`；选择子合成原型                                                                                                                          |
| `references/data-attributes.md`      | 查询任意 `data-*`（根 / clip / 子合成宿主 / 旧版别名）；使用 `class="clip"`                                                                                                       |
| `references/tracks-and-clips.md`     | 选择 `data-track-index`，处理同轨重叠 / z-index，使一个 clip 相对于另一个进行计时                                                                                                 |
| `references/sub-compositions.md`     | 接入子合成（宿主属性、`<template>`、每实例变量）并在其中制作动画                                                                                                                   |
| `references/variables-and-media.md`  | 声明变量；放置 `<video>`/`<audio>`，设置音量，裁剪                                                                                                                                |
| `references/determinism-rules.md`    | 构建可寻址时间线；确定性禁令；可动画属性白名单；布局 / 文本适配                                                                                                                    |
| `references/full-screen-motion.md`   | 使用共享背景创作全帧动态                                                                                                                                                             |
| `references/storyboard-format.md`    | 编写 `STORYBOARD.md` 计划（+ 已解析的清单）                                                                                                                                         |
| `references/review-loop.md`          | 在实时画板上运行计划 → 草图 → 构建审查流程——由每个故事板规划工作流共享                                                                                                            |
| `references/production-loop.md`      | 将获批计划交付为视频——自由构建直接遵循的阶段依赖关系（音频、帧、组装、转场、字幕、验证、交付）                                                                                    |
| `references/brief-contract.md`       | brief 的基本规则——模式推导（协作 / 自主）、共享字段注册表、提问不变量（提问本身位于 `/hyperframes` → 意图层）                                                                     |
| `references/brief-format.md`         | 编写 `BRIEF.md`——工作流的 Setup 写入、后续每一步读取的已确认意图文档                                                                                                              |
| `references/script-format.md`        | 编写可选的 `SCRIPT.md` 锁定旁白                                                                                                                                                     |
| `references/subagent-dispatch.md`    | 将子代理调度动词（并行扇出 / 后台 / 等待）映射到你的运行环境                                                                                                                       |
| `references/frame-worker-core.md`    | 共享帧工作者角色契约——每个叙事工作流的数据包构建器都会将其前置到该工作流的 `sub-agents/frame-worker.md` 增量中                                                                     |
| `references/tailwind.md`             | 在 Tailwind v4 项目中工作（`init --tailwind`；运行时契约不同于 Studio 的 v3）                                                                                                     |

有关动画运行时的具体内容（GSAP API、Lottie、Three.js 等），请前往 `hyperframes-animation` → `adapters/<runtime>.md`。

## 构建合成

### 两种根形式（不可互换）

- **独立式**（顶层 `index.html`）——根 `<div data-composition-id="…">` 直接位于 `<body>` 中，**不使用 `<template>` 包装**（包装会隐藏所有内容并破坏渲染）。
- **子合成**（通过 `data-composition-src` 加载）——根元素**必须**包裹在 `<template>` 中。

> ⚠ 传输规则：运行时**只克隆 `<template>` 内容**；其外部的所有内容（包括 `<head>` 样式/脚本）都会被丢弃——请将 `<style>`/`<script>` 放在模板**内部**。
> ⚠ 宿主 ID 规则：宿主槽位的 `data-composition-id` 必须与内部模板的 `data-composition-id` **完全相等**，并且与 `window.__timelines["<id>"]` 键**完全相等**——不得使用 `-mount`/`-slot`/`-host` 后缀。

文件形状、宿主接入和预渲染检查清单 → `references/sub-compositions.md`。

### 根元素必须有尺寸（静默布局错误）

独立根元素需要一个明确的**有尺寸盒子**（以 px 指定的 `width`/`height`），并且到 `height:100%` 元素为止的每个祖先元素都必须具有已解析的高度——否则 flex/`100%` 子元素会收缩至约 0，内容将堆叠在左上角。不要仅依赖自动化门禁来捕获此问题；请检查快照。骨架 → `references/minimal-composition.md`。

### 一条暂停的时间线

每个合成都会在 `window.__timelines["<id>"]` 注册**恰好一条** `gsap.timeline({ paused: true })`（键 = 根 `data-composition-id`），并在页面加载时**同步**构建。渲染时长 = 根 `data-duration`，而非时间线长度。不要手动将子时间线嵌套进宿主。完整契约（包括非 GSAP 运行时）→ `references/determinism-rules.md` + `hyperframes-animation/adapters/`。

### 首次 lint 常见陷阱（保证首次构建失败）

以下两条规则 `lint` **确实**会捕获，但只会在事后捕获——第一次就正确编写：

- **根**合成元素必须带有 `data-start="0"`（与 `data-composition-id`/`data-width`/`data-height` 一同存在）；省略它会使 `lint` 以 `root_composition_missing_data_start` 失败。
- 绝不要将 CSS 初始 `transform` 与针对**同一**属性的 GSAP tween 配对——CSS 值与 tween 的起始值会冲突，`lint` 会以 `gsap_css_transform_conflict` 拒绝。请在 tween 内使用 `gsap.fromTo(el, { x: -40 }, { x: 0 })` 设置初始状态，而不是使用 CSS `transform: translateX(-40px)`。

### 不可协商规则（自动化门禁可能遗漏的静默错误）

此处列出；完整原理见所链接的参考资料。请勿违反：

- 禁止渲染时钟 / 未设种子的 `Math.random` / 网络 / 输入状态；禁止 `repeat: -1`（请使用有限次数）。→ `determinism-rules.md`
- 仅对视觉属性白名单中的属性制作动画；绝不要 tween `display` 或原始 `visibility`。GSAP `autoAlpha` 和零时长时间线边界设置是唯一的可见性例外，且仅适用于非 clip 元素或 clip 内的包装器。框架单独控制 `.clip` 可见性。不要在页面加载时对后续场景 clip 使用 `gsap.set`。→ `determinism-rules.md`
- 正文文本中禁止使用 `<br>`；经过 transform 的元素必须是块级且有尺寸；脉冲的绝对定位装饰元素需要预留峰值空间。→ `determinism-rules.md`
- `<video>`/`<audio>` 可在**任意嵌套深度**下工作（包括子合成 `<template>` 或包装器内）；框架控制播放，并会在其所在位置执行媒体寻址/解码。唯一的注意事项是时间线，而非放置位置：子合成时间线不能为宿主根元素制作动画。→ `variables-and-media.md`
- 每个 `id` 在**组装后**的页面中必须唯一；在子合成内，请以合成 ID 为 `id` 加前缀（`#<id>-hero`）。重复的 `<video>`/`<img>` ID 会渲染为**空白**——制作器通过 `getElementById` 注入帧，跨文件重复项会绕过 `lint`。→ `composition-patterns.md`
- 全屏场景填充应放在全出血的**子元素**上（`position:absolute; inset:0`），绝不能放在合成根元素本身——制作器的帧合成可能会丢弃根元素自身的 `background`（帧会渲染为**黑色**），即使预览/`snapshot` 显示正常。→ `composition-patterns.md`

## 编辑现有合成

- 先阅读文件。保留无关的时间、轨道、ID、变量、媒体路径。
- 匹配现有的合成 ID 和时间线键。
- 添加 clip：选择不重叠的 `data-track-index`，或有意调整周围时间。
- 任意合成元素上的 `data-hidden` 会在预览和渲染中同时隐藏它，覆盖其时间窗口；它是非破坏性/可逆的，并由 Studio 时间线的眼睛图标切换。
- 添加子合成：在接入宿主前验证其内部 `data-composition-id`。

## 验证

使用 `hyperframes-cli` 获取命令详情

- [ ] `npx hyperframes check` 通过（lint、运行时、布局、运动和对比度均为 0 项发现）
- [ ] 包含子合成的项目：`npx hyperframes snapshot --at <midpoints>`，并目视检查每一帧
- [ ] 使用 `npx hyperframes preview` 进行审查（用户可在 Studio 时间线中编辑任何内容）
- [ ] 仅在用户批准后执行 `npx hyperframes render`
