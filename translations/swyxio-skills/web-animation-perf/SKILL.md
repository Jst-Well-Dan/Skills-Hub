<!-- source-sha256: 9d4a5cefda3041fbd334d2ad9dbdd6419c5e245d2c72fa3e10733889db6e1f40 -->
---
name: web-animation-perf
description: 防止由 JS 驱动的 CSS 动画发生布局/过渡/重排抖动。适用于构建或调试连续运动（旋转、环绕、视差、滚动关联效果、跑马灯、轮播图），以及出现卡顿、抖动、延迟、动画漂移、重影、“元素向中心坍缩”、“变慢”、“是否应该使用 canvas？”等症状，或将 `setInterval`/React 状态与 CSS `transition` 混合使用时。
---

# Web 动画性能

编写流畅、由 GPU 加速的 Web 动画的指南。大多数卡顿源于三个可以避免的错误；其余则取决于诊断技巧。

## 三条基本准则

### 1. 切勿将 `transition: all <duration>` 与每帧更新同一属性的 JS 结合使用

这是最常见的动画错误。如果 JS 在每个时钟周期更新 `left`/`top`/`transform`，同时元素还具有 `transition-all duration-700`（或类似设置），CSS 就会在过渡持续时间内，对 JS 连续设置的每一对值进行线性插值。对于非线性运动（环绕、弧线、缓动曲线），线性弦线会穿过预期路径——例如，旋转节点看起来会向中心向内漂移，视差元素会产生拖影，滚动关联效果会明显落后于滚动位置。

只选择一种驱动方式：

- **纯 CSS**：使用 `@keyframes` + `animation: spin 8s linear infinite`，交由浏览器处理。
- **纯 JS**：每帧设置*最终*位置；不要在该属性上设置 `transition`。仅针对状态变化使用单独且范围更窄的 `transition`（例如激活/未激活状态的缩放和颜色）。

如果你希望悬停/激活状态具有过渡效果，同时位置由 JS 驱动进行连续运动，请将过渡限定到具体属性（`transition: transform 300ms, background-color 300ms`），并排除由 JS 驱动的属性。

### 2. 连续运动应使用 `requestAnimationFrame`，切勿使用 `setInterval`

| 关注点 | `setInterval(fn, 16)` | `requestAnimationFrame(fn)` |
|---|---|---|
| 帧同步 | 会漂移；可能一帧触发 2 次或丢帧 | 与垂直同步锁定 |
| 标签页进入后台 | 继续运行，浪费 CPU/电量 | 浏览器会暂停 |
| 计时精度 | 墙上时钟，±浏览器计时器分辨率 | 向回调传入高分辨率 `performance.now()` 参数 |
| 负载下的抖动 | 不断累积 | 干净地跳过帧 |

始终根据经过的时间进行积分，而不是每个时钟周期使用固定步长。这样即使丢帧，运动仍然保持正确：

```js
useEffect(() => {
  let lastFrame = performance.now();
  let id = 0;
  const tick = (now) => {
    const dt = Math.min(now - lastFrame, 100); // clamp to handle tab-switch gaps
    lastFrame = now;
    const degrees = SPEED_DEG_PER_SEC * (dt / 1000);
    setRotation((prev) => (prev + degrees) % 360);
    id = requestAnimationFrame(tick);
  };
  id = requestAnimationFrame(tick);
  return () => cancelAnimationFrame(id);
}, []);
```

### 3. 为 `transform` 和 `opacity` 添加动画。避免使用 `left`/`top`/`width`/`height`/`margin`/`padding`

只有 `transform` 和 `opacity` 能跳过布局与绘制，完全在 GPU 合成器上运行。其他任何属性的变化都会触发重排——悬停时发生一次尚可接受，以 60Hz 发生则是灾难性的。

| 想要改变…… | 应这样做 | 不要这样做 |
|---|---|---|
| 位置 | `transform: translate3d(x, y, 0)` | `left`、`top`、`margin` |
| 大小 | `transform: scale(s)` | `width`、`height` |
| 旋转 | `transform: rotate(a)` | （没有对应的 `left/top` 方案——但应使用 `transform` 以提升到合成器层） |
| 淡入淡出 | `opacity` | `visibility`、`display`、颜色 alpha |

对于静态定位（只渲染一次且没有动画），使用 `left`/`top` 没有问题。该规则适用于*连续添加动画*的属性。

## 辅助实践

### 使用 `will-change` 提升到合成器层

```jsx
style={{ willChange: 'transform, opacity' }}
```

仅用于确实持续进行动画的元素。过度使用 `will-change` 会消耗 GPU 内存。

### 当状态驱动的重新渲染成为主要开销时，通过 refs 直接驱动 DOM

如果性能分析表明 React 协调过程是瓶颈（对于少于 50 个元素的情况很少见），则绕过 React 执行每帧更新：

```jsx
const nodeRefs = useRef([]);
// in rAF tick:
nodeRefs.current[idx].style.transform = `translate3d(${x}px, ${y}px, 0)`;
```

仅在发生有意义的语义变化时（例如高亮节点发生变化）才通过 React 状态重新渲染，而不是每帧都重新渲染。

### 当不确定动画状态是否正确时，对 DOM 位置进行采样

使用 Playwright 或 DevTools 实际测量渲染后的几何信息。对于圆周运动，可以验证位置是否落在轨道环上：

```js
// In Playwright page.evaluate, sample every 200ms for ~1s
const nodes = Array.from(document.querySelectorAll('.orbital-node'));
const ratios = nodes.map((n) => {
  const r = n.getBoundingClientRect();
  const dx = r.left + r.width / 2 - centerX;
  const dy = r.top + r.height / 2 - centerY;
  return Math.hypot(dx, dy) / expectedOrbitRadius; // should be 1.00
});
```

如果比率漂移到 1.00 以下（朝向中心），说明违反了规则 1：CSS 过渡正在与 JS 更新相互对抗。如果比率正确，但动画*看起来*卡顿，则应怀疑规则 2（计时器/rAF）或规则 3（`left/top` 重排）。

### Canvas？对于 UI 几乎从来都不是正确答案

对于 ≤ ~100 个 DOM 元素，由 GPU 合成的 `transform` 动画比 canvas 重绘更快，并且无需额外工作即可保留无障碍能力、点击目标、悬停状态和可检查性。仅在以下情况下使用 canvas：(a) 元素数量达到数千个；(b) 需要像素级渲染控制（粒子、流体模拟）；或 (c) 布局无法映射为 DOM 树。

## 诊断工作流

当用户报告“动画很慢/卡顿/坏了”时：

先考虑 5–7 个典型原因，然后在修改代码之前将范围缩小到最可能的 1–2 个。常见原因按大致顺序排列如下：

1. **`transition-all` 与 JS 更新相互竞争**（规则 1）——典型症状：运动*看起来像是*对预期路径进行了插值式抄近路（圆周运动向内漂移、视差效果延迟、出现拖影）。
2. **使用 `left/top/width/height` 而不是 `transform`**（规则 3）——典型症状：卡顿程度随元素数量或视口大小增加，DevTools Performance 中显示布局/绘制列。
3. **使用 `setInterval` 而不是 rAF**（规则 2）——典型症状：当标签页繁忙或进入后台时，抖动变得更严重。
4. **每帧更新 React 状态**——典型症状：性能分析器显示协调过程占据主要开销；对于少量元素尚可接受。
5. **在 `display`/`visibility`/`height: auto` 上添加动画**——典型症状：动画完全不运行，或直接跳变而不是进行补间。
6. **过度使用 `will-change`**——典型症状：页面其他位置滚动卡顿、GPU 内存压力增大。
7. **紧密循环中的布局抖动**：在同一帧内交错执行布局读取（`offsetWidth`、`getBoundingClientRect`）和写入。

先通过日志/测量进行验证，再逐项修改，每次不要更改多个因素。

## 快速参考：反模式 → 修复

```jsx
// ❌ ANTI-PATTERN
<div
  className="absolute transition-all duration-700"
  style={{ left: `${x}%`, top: `${y}%` }}
/>
useEffect(() => {
  const id = setInterval(() => setAngle((a) => a + 0.6), 50);
  return () => clearInterval(id);
}, []);

// ✅ FIX
<div
  className="absolute"
  style={{
    left: `${x}%`, top: `${y}%`,
    willChange: 'left, top',
  }}
/>
useEffect(() => {
  let last = performance.now(); let id = 0;
  const tick = (now) => {
    const dt = Math.min(now - last, 100); last = now;
    setAngle((a) => (a + DEG_PER_SEC * dt / 1000) % 360);
    id = requestAnimationFrame(tick);
  };
  id = requestAnimationFrame(tick);
  return () => cancelAnimationFrame(id);
}, []);
```

（为获得最佳性能，还应将 `left/top` 替换为 `transform: translate3d(...)`。）

## 仓库内案例研究：`OrbitalDiagram`（AIE 会议网站）

`apps/main/src/pages/worldsfair/index.jsx`——一个包含 11 个角色节点的旋转轨道图。原始实现同时触犯了三条基本反模式：

1. 每个节点都有 `transition-all duration-700`，同时由 `setInterval(50ms)` 在每个时钟周期更新 `left/top`。CSS 过渡会在 JS 连续设置的位置之间进行线性插值，以直线弦切过轨道。可见症状：在发布后的加速阶段，节点看起来会向中心徽标向内坍缩，而不是沿圆环运行。（规则 1）
2. 使用 `setInterval` 而不是 `requestAnimationFrame` → 造成抖动和计时不同步。（规则 2）
3. 为 `left`/`top` 添加动画而不是使用 `transform` → 每个时钟周期都会发生重排。（规则 3）

修复方式：

- 从旋转包装器中移除了 `transition-all duration-700`（仅在内部圆形元素上保留 `transition-all duration-300`，用于激活状态的缩放/颜色变化；它由事件驱动，而不是每帧驱动）。
- 改用带增量时间积分（`degPerSec × dt`）的 `requestAnimationFrame`，因此速度以度/秒表示，即使丢帧，运动也能保持正确。
- 添加了 `willChange: 'left, top, opacity'`。
- 使用 Playwright 对节点位置进行采样（`getBoundingClientRect`）来验证，并检查多个帧中每个节点的“距中心距离 ÷ 预期轨道半径”是否均为 1.00。

在验证此仓库中涉及动画代码的 PR 时，请使用 Playwright 随时间采样几何信息并断言预期的不变量——不要仅依赖截图，因为问题可能很细微（弦线与弧线的差异），或仅在加速/峰值运动期间出现。
