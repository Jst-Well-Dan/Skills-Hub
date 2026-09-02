<!-- source-sha256: 4577193cca207a6812904953d278af739255a7a88d44c214ffe5aa6f0d896bff -->
---
name: hyperframes-keyframes
description: >
  当 HyperFrames 合成需要可安全跳转的 2D/3D 关键帧、GSAP
  时间线、CSS 关键帧、Anime.js、WAAPI、FLIP、路径、遮罩、SVG 变形/绘制、
  文字拖尾、3D 深度，或 `hyperframes keyframes` 诊断时使用。
  不适用于宽泛的场景策略、品牌设计、媒体素材搜集、字幕或
  通用视频规划。
---

# HyperFrames 关键帧

关键帧是一份姿态契约：可见状态、连续的主体身份、可安全跳转的运行时、经验证的像素。

广泛的场景方案请使用 `hyperframes-animation`。完整命令文档请使用 `hyperframes-cli`。仅在选择实现机制时使用 `references/keyframe-patterns.md`，而非用于视觉风格。

## 流程

1. 确定动画主体、可见状态、最终状态和运行时。
2. 选择能证明提示要求的最小机制。仅当机制不明确时阅读 `references/keyframe-patterns.md`。
3. 在声明的运行时中编写可安全跳转的关键帧。同步构建并注册运行时实例。
4. 使用 `hyperframes lint`、`hyperframes check`、`hyperframes keyframes`、一次聚焦的 `--shot`，以及证明时刻的快照进行验证。
5. 若证明失败，修复源关键帧，并在渲染前重新运行最小的失败诊断。

## 契约

- 命名移动的主体。
- 命名证明预期运动所需的姿态，包括最终状态。
- 对可见通道设置关键帧，而非隐藏的辅助状态。
- 当连续性重要时，保持对象身份。
- 仅当预期运动是替换或溶解时才使用交叉淡化。
- 将可读或具有语义的状态保持足够长以便看清。
- 最后一帧是动画的一部分，不是收尾清理。
- 除非被要求，否则不要重置为静止状态。
- 除非被要求，否则不要以黑场结束。
- 若编辑起始场景，除非被要求重新设计，否则保留布局、文案、素材、颜色和最终状态。

## 运行时规则

GSAP：

- 在页面加载时同步构建
- 使用 `gsap.timeline({ paused: true })`
- 注册为 `window.__timelines[compositionId]`
- 注册表键必须与 `data-composition-id` 匹配
- 不要为渲染关键运动调用 `tl.play()`
- 保持重复次数有限

CSS 关键帧：

- 有限的持续时间和迭代次数
- 确定性的延迟
- `animation-fill-mode: both`
- 当时序属于剪辑时使用 `data-start`

Anime.js：

- 同步创建
- `autoplay: false`
- 有限的持续时间和循环次数
- 将每个实例推送到 `window.__hfAnime`

WAAPI：

- 有限的 `duration`
- `fill: "both"`
- 确定性构建
- 文本界面不列出 WAAPI；使用 `--shot`（它会跳转 WAAPI）和快照验证

绝不要用于渲染关键运动：

- `Date.now()`
- `performance.now()`
- 未设种子的 `Math.random()`
- 悬停/滚动触发器
- 定时器
- 异步创建的时间线
- 未注册的 `requestAnimationFrame`
- 无限循环

## GSAP 骨架

```js
const root = document.querySelector("[data-composition-id]");
const compositionId = root.dataset.compositionId;
const tl = gsap.timeline({ paused: true });

tl.addLabel("state-a", 0);
tl.to(".subject", {
  keyframes: [
    { x: 0, opacity: 1, duration: 0.2 },
    { x: 120, opacity: 1, duration: 0.4, ease: "power2.out" },
    { x: 100, opacity: 1, duration: 0.2, ease: "power2.inOut" },
  ],
  ease: "none",
});

window.__timelines = window.__timelines || {};
window.__timelines[compositionId] = tl;
```

为语义状态使用标签。使用位置参数而非链式延迟。对于触及相同属性的后续 `from()`/`fromTo()` 补间，使用 `immediateRender: false`。

## 关键帧形式

- 数组关键帧：带有每步持续时间/缓动的姿态阶梯。
- 百分比关键帧：在单个补间内精确计时。
- 属性数组：紧凑的多停点变化。
- 当每个停点都带有自己的缓动时，在父级上使用 `ease: "none"`。
- 当每个片段应共享相同感觉时使用 `easeEach`。

不要从示例复制数值距离或时序。应从实际合成的几何形状和持续时间中推导它们。

对于一个主体在两个方框之间移动，优先使用一个连续的 transform 补间或 FLIP。仅当观众应感受到明显节拍时，才将 `x/y/scale` 拆分为多个带缓动的关键帧；每个片段都会改变速度，并可能显得卡顿。

## 通道

优先使用合成器/视觉通道：`x/y/z`、`xPercent/yPercent`、`scale`、`rotationX/Y/Z`、`skew`、`transformOrigin`、`svgOrigin`、`opacity`、`autoAlpha`、`clip-path`、遮罩、CSS 变量、SVG 路径/虚线值、相机变换、着色器 uniforms。

避免布局/生命周期通道：`top/left/right/bottom`、`width/height`、`margin/padding`、`display`、`visibility`、延迟 DOM 创建、通过辅助叠层实现主体运动。

对于可见性变化，在已注册、可跳转的 GSAP 时间线上使用 `autoAlpha`，或在显式边界处使用零持续时间的 `tl.set()`。仅定位非剪辑元素或剪辑内的包装器；绝不要定位 `.clip` 本身。绝不要对原始 `visibility` 进行持续时间补间，也绝不要对 `display` 进行补间。

## 机制选择

选择能证明提示要求的最小机制：

| 需求                                  | 机制                                               |
| ------------------------------------- | -------------------------------------------------- |
| 同一主体改变方框或层级                | 共享元素 / FLIP                                    |
| 主体沿可见路线移动                    | 路径移动                                           |
| 描边增长或描绘                        | 描边绘制                                           |
| 形状变成另一种形状                    | 形状插值                                           |
| 揭示边界可见                          | 剪辑、遮罩或着色器 uniform                         |
| 多个项目按顺序移动                    | stagger / 索引延迟                                 |
| 文字本身移动                          | 行、词、字符或带状细分                             |
| 表面弯曲、拉伸或裁剪                  | 父/子级反向变换                                    |
| UI 有状态                             | 显式状态机                                         |
| 场景有深度                            | DOM 3D、Three.js 或 WebGL 相机/对象关键帧          |

机制可以组合，但每一种都必须阐明创意。装饰不是证明。

## 时序

- 仅当预备动作能阐明原因或方向时才使用。
- 加速从静止开始。
- 峰值证明应毫不含糊地展示机制。
- 后续动作体现能量和方向。
- 仅当主体应具有弹性或触感时才使用超调。
- 恒速路径移动通常需要 `ease: "none"`。
- 离散 UI 状态通常需要锐利的缓出。
- 重复元素需要有序偏移，而非完全相同的时序。
- 最终定格需要比过渡姿态更长的保持时间。
- 平滑意味着同一主体具有连续速度。
- 不要重叠写入相同 transform 属性的补间，除非该重叠是有意的且已验证。
- 避免在同一主视觉表面也在缩放或移动时，对大型 `clip-path`/遮罩变化做动画；在主运动稳定后使用嵌套揭示。

## 文本

保留行框、词间距、可读性和最终适配度。若文字在内部移动，应移动字形或遮罩带，而不只是文字周围的装饰。对可读帧做快照。

## SVG

对于描边增长，优先使用 `DrawSVGPlugin`，其次使用 `stroke-dasharray`/`stroke-dashoffset`。对于形状插值，优先使用 `MorphSVGPlugin`；必要时将基本图元转换为路径，并将复杂轮廓拆分为更简单的部分。

## 3D

仅缩放是伪深度。对稳定的父级使用透视、`transform-style: preserve-3d`、z 轴移动、旋转、相机/世界运动、遮挡，以及对象交叉时的图层顺序。

使用一到两个能暴露深度关系的诊断角度。若倾斜证明未显示深度交叉，请改善 z/相机/遮挡。

## Canvas / WebGL

通过确定性状态对相机位置、相机目标、对象变换、材质不透明度、着色器 uniforms 和后处理强度设置关键帧。从 HyperFrames 时间进行渲染。使用 `--ghost`，因为标记框无法看到内部 canvas 运动。

## CLI 证明

```bash
npx hyperframes lint
npx hyperframes check
npx hyperframes keyframes .
npx hyperframes keyframes . --json
npx hyperframes keyframes . --runtime all
npx hyperframes keyframes . --selector "<selector>" --shot "<file>" --samples <n>
npx hyperframes keyframes . --selector "<selector>" --shot "<file>" --layout strip --from <t0> --to <t1>
npx hyperframes keyframes . --shot "<file>" --ghost --angle <angle>
npx hyperframes snapshot . --at <times>
```

为 `<selector>` 选择真实的动画主体。为 `<times>` 选择首帧、证明姿态、最终保持前和精确最终帧。仅在必须证明深度时选择 `<angle>`。

| 工具             | 证明                                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| `keyframes`      | 目标、显式停点、路径、描绘、组合父/子级运动、CSS 停点、Anime 注册                                  |
| `--shot`         | 幽灵图、路线形状、时间间距、DOM 3D 投影、聚焦选择器证明                                            |
| `--layout strip` | 原地运动、重叠、接触、细微缩放/不透明度、文字波浪                                                  |
| `--ghost`        | canvas、WebGL、着色器运动、渲染的 3D                                                               |
| `snapshot --at`  | 遮罩、文本可读性、完整状态、最终定格、黑场/重置尾部                                                |

若选择器证明看起来不对：

1. 重新运行 `--json`
2. 找到实际动画目标
3. 拍摄该目标
4. 对完整帧做快照
5. 相信绘制的像素而非日志

## 诊断解读

`flat` 表示没有显式的中间姿态。`keyframes` 表示存在显式停点。`motionPath` 表示存在路线。`trace` 表示多描边绘制。`composed with` 表示子级运动继承父级运动。

均匀的幽灵间距表示恒速。聚集的幽灵表示缓入或稳定。大间隔表示快速移动。

辅助选择器拍摄不是证明。破损完整帧上的洋葱皮拍摄不是证明。

## 错误处理

| 失败               | 修复                                                                               |
| ------------------ | ---------------------------------------------------------------------------------- |
| endpoint-only      | 添加中间姿态，保持峰值证明，重新运行 `--shot`                                        |
| identity break     | 保持一个元素存活，使用共享源/最终方框，移除替代性交叉淡化                           |
| fake 3D            | 添加 z/相机移动、遮挡、倾斜证明                                                    |
| wrong final        | 添加最终保持，对最终保持前和精确最终帧做快照                                       |
| unseekable runtime | 暂停自动播放，注册实例，移除定时器，同步构建                                       |
| unreadable text    | 保留行框，减少位移，添加最终保持，对文字帧做快照                                   |

## 完成

运行 `hyperframes lint`、`hyperframes check`、`hyperframes keyframes`、一次聚焦的 `--shot` 和快照。确认首帧、证明姿态、最终保持前、精确最终帧、主体拥有的运动，以及没有调试叠层。
