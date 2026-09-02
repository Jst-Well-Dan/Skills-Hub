<!-- source-sha256: 69a9903796e65c66edbe9ec9621eca8953c7cc2a93a718687306891daf0463d4 -->
---
name: hyperframes-animation
description: "HyperFrames 的全部动画知识——原子运动规则、多阶段场景蓝图、场景转场、更广泛的动效设计技巧，以及七个运行时适配器（默认 GSAP，另加 Lottie、Three.js、Anime.js、CSS keyframes、Web Animations API、TypeGPU）。适用于任何运动或动画任务：选择 2-4 条规则并组合，或加载蓝图，或查询特定运行时 API（例如 GSAP eases / Lottie player / Three.js mixer）。还涵盖对现有合成编排（动画地图）的审查，以及 24 种具名文本动画效果。HyperFrames 原生：单一暂停时间线、可安全 seek、确定性。"
---

# HyperFrames 动画

一个 skill 中包含所有运动知识：**规则**（原子配方）、**蓝图**（多阶段场景模板）、**转场**（场景到场景）、**技巧**（更广泛的动效设计模式）和**适配器**（各运行时 API）。

有关合成契约（数据属性、子合成、确定性），请参阅 `hyperframes-core`。

## 默认：组合原子规则

从 `rules-index.md` 中选择 2-4 条规则，用单一暂停的 GSAP 时间线将它们串联起来，即可完成。这比从蓝图开始更快，产生的代码也更少。

## 在以下情况加载蓝图

- 场景符合现有的预设计多阶段模板（brand-reveal、social-proof 等），且复用其阶段流水线能节省实际创作时间
- 你希望获得复杂 4-5 阶段编排的可运行、可信的代码

蓝图位于 `blueprints-index.md`。每个条目指向 `blueprints/<id>.md`（配方）。不要推测性地阅读它；仅当你已决定需要场景级编排时再加载。

## 路由

| 想要…                                                                         | 阅读                                                |
| ------------------------------------------------------------------------------ | --------------------------------------------------- |
| 按触发条件 / 标签选择原子运动模式                                             | `rules-index.md`                                    |
| 阅读一条规则完整的 HTML / CSS / GSAP 配方                                     | `rules/<name>.md`                                   |
| 选择多阶段场景模板                                                            | `blueprints-index.md`                               |
| 阅读一个蓝图的完整配方                                                        | `blueprints/<id>.md`                                |
| 编写场景转场（由 CSS 驱动，位于两个片段之间）                                 | `transitions/overview.md`, `transitions/catalog.md` |
| 查询更广泛的动效设计技巧                                                      | `techniques.md`                                     |
| 分析现有合成的动画地图                                                        | `scripts/animation-map.mjs`                         |
| GSAP API——时间线 / tween / 位置参数                                          | `adapters/gsap.md`                                  |
| GSAP——可直接使用的效果配方                                                    | `rules/gsap-effects.md`                             |
| GSAP——变换 / 性能                                                            | `adapters/gsap-transforms-and-perf.md`              |
| GSAP——缓动 / stagger                                                         | `adapters/gsap-easing-and-stagger.md`               |
| GSAP——时间线 / 标签                                                          | `adapters/gsap-timeline-and-labels.md`              |
| Lottie / dotLottie（After Effects 导出，`window.__hfLottie`）                 | `adapters/lottie.md`                                |
| Three.js / WebGL（3D 场景、`AnimationMixer`、`hf-seek`）                      | `adapters/three.md`                                 |
| Anime.js（`window.__hfAnime`）                                                | `adapters/animejs.md`                               |
| CSS keyframes（`animation-delay` / `play-state` / `fill-mode`）               | `adapters/css-animations.md`                        |
| Web Animations API（`element.animate()`、`currentTime` seek）                 | `adapters/waapi.md`                                 |
| TypeGPU / WebGPU（`navigator.gpu`、WGSL、计算管线）                           | `adapters/typegpu.md`                               |
| HTML-as-texture + WebGL/GLSL 后期效果（通过 `drawElementImage` 捕获实时 DOM） | `adapters/html-in-canvas-patterns.md`               |
| 具名文本动画效果（通过外部 `animate-text` skill 提供的 24 个 ID）             | `adapters/animate-text.md`                          |

## 选择运行时

- **GSAP** 是 95% 动效工作的默认选择——涵盖时间线编排、变换、缓动、stagger。本 skill 中的所有原子规则均基于 GSAP。
- 当资源拥有自身预烘焙时间线时使用 **Lottie**（通常为 After Effects 导出）。
- **Three.js** 用于 3D 场景、相机运动、由 shader 驱动的视觉效果。
- 当 GSAP 大材小用时，使用 **Anime.js** 进行轻量 tween。
- **CSS** 用于简单的重复图案、装饰、shimmer——无需 JavaScript 动画成本。
- **WAAPI** 用于无需 GSAP 依赖的原生浏览器 keyframes。
- **TypeGPU / WebGPU** 用于 GPU 渲染的 canvas（粒子、液态玻璃、自定义 shader）。

多个运行时可以共存于同一个合成中。每个运行时都将其实例注册到特定运行时的全局对象上，以便 HyperFrames 能在一次传递中 seek 它们全部。

## 关键约束

**前提条件：`hyperframes-core` → 不可协商规则**（单一暂停时间线、`data-duration` 控制长度、禁止 `Math.random` / `Date.now` / `performance.now`、禁止 `repeat: -1`、禁止在后续场景片段上使用页面加载时的 `gsap.set`、禁止 `display` 或原始 `visibility` tween，以及禁止在 `async` / `setTimeout` / `Promise` 内构建时间线）。核心仍允许在明确的时间线边界使用 GSAP `autoAlpha` 和零时长可见性设置。仅在非片段元素或片段内的包装器上使用这些例外；框架拥有 `.clip` 生命周期。不要在此重述完整契约。

在核心契约之上的动画工艺补充：

- **预计算布局常量**——绝不要在 tween 时从 `getBoundingClientRect()` 推导位置。tween 时的 DOM 测量会失去同步，因为渲染器会并行采样；在合成设置时计算一次坐标并复用。
- **空间运动仅使用 GSAP 变换别名**（`x`、`y`、`scale`、`rotation`）。核心的允许列表也允许对非空间属性进行 tween：`opacity` / `color` / `backgroundColor` / `borderRadius`——但绝不要使用 `width` / `height` / `top` / `left` 进行布局变更。

## 脚本

```bash
node skills/hyperframes-animation/scripts/animation-map.mjs <composition-dir> \
  --out <composition-dir>/.hyperframes/anim-map
```

读取注册在 `window.__timelines` 上的每个 GSAP 时间线，枚举 tween，采样 bbox，计算标记，并输出 `animation-map.json`。创作完成后，使用它审查编排（空白区、stagger 一致性、生命周期警告）。

`animation-map.mjs` 会先从当前项目解析辅助包，然后可以引导使用捆绑的 HyperFrames 包版本。仅当在捆绑 CLI/skill 安装之外运行该 skill，且需要显式固定该引导版本时，才设置 `HYPERFRAMES_SKILL_PKG_VERSION=<version>`。

## 另请参阅

- `hyperframes-core` ——合成结构、数据属性、子合成、确定性渲染契约
- `hyperframes-creative` ——调色板、排版、叙事、节拍规划（非动画创意指导）
- `hyperframes-cli` ——`npx hyperframes lint / check / snapshot / preview / render`
