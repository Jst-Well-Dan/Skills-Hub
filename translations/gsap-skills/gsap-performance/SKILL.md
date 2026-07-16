<!-- source-sha256: cb5408d6fba707aabcbfe3320317a14c1f8fca6070074e5261047930f50d441e -->
---
name: gsap-performance
description: 官方 GSAP 性能优化技能——优先使用变换，避免布局抖动，合理使用 will-change 和批处理。用于优化 GSAP 动画、减少卡顿，或当用户询问动画性能、FPS 或流畅 60fps 时。
license: MIT
---

# GSAP 性能优化

## 何时使用此技能

在优化 GSAP 动画以实现流畅 60fps、降低布局与绘制开销，或用户询问性能、卡顿或高性能动画最佳实践时使用。

**相关技能：**使用 **gsap-core**（变换、autoAlpha）和 **gsap-timeline** 构建动画；有关 ScrollTrigger 的性能优化，请参阅 **gsap-scrolltrigger**。

## 优先使用变换和不透明度

为 **transform**（`x`、`y`、`scaleX`、`scaleY`、`rotation`、`rotationX`、`rotationY`、`skewX`、`skewY`）和 **opacity** 创建动画，可让相关工作在合成器中完成，并避免布局计算和大多数绘制操作。当变换可以实现相同效果时，应避免为布局开销较大的属性创建动画。

- ✅ 优先使用：**x**、**y**、**scale**、**rotation**、**opacity**。
- ❌ 尽可能避免：**width**、**height**、**top**、**left**、**margin**、**padding**（它们会触发布局计算并可能导致卡顿）。

GSAP 的 **x** 和 **y** 默认使用变换（translate）；移动元素时请使用它们，而非 **left**/**top**。

## will-change

在 CSS 中为将要执行动画的元素使用 **will-change**。它会提示浏览器将该元素提升至独立图层。

```css
will-change: transform;
```

## 批量执行读取和写入

GSAP 会在内部批量处理更新。当 GSAP 与直接的 DOM 读取/写入或依赖布局的代码混合使用时，请避免以交错方式执行读取和写入，以免反复造成布局抖动。应优先先完成所有读取，再完成所有写入（或者让 GSAP 一次性处理写入）。

## 大量元素（交错动画、列表）

- 当动画相同时，使用 **stagger**，而不是创建许多带有手动延迟的独立补间动画；这样效率更高。
- 对于长列表，请考虑使用**虚拟化**或仅为可见项目创建动画；如果同时创建数百个补间动画会导致卡顿，请避免这样做。
- 尽可能复用时间线；避免每一帧都创建新的时间线。

## 频繁更新的属性（例如鼠标跟随效果）

对于频繁更新的属性（例如鼠标跟随元素的 x/y），优先使用 **gsap.quickTo()**。它会复用单个补间动画，而不是在每次更新时创建新的补间动画。

```javascript
let xTo = gsap.quickTo("#id", "x", { duration: 0.4, ease: "power3" }),
    yTo = gsap.quickTo("#id", "y", { duration: 0.4, ease: "power3" });

document.querySelector("#container").addEventListener("mousemove", (e) => {
  xTo(e.pageX);
  yTo(e.pageY);
});
```

## ScrollTrigger 与性能

- **pin: true** 会提升被固定元素的图层；只固定必要的元素。
- 为 **scrub** 设置较小的值（例如 `scrub: 1`）可以减少滚动期间的工作量；请在低端设备上进行测试。
- 仅在布局实际发生变化时（例如内容加载后）调用 **ScrollTrigger.refresh()**，不要在每次调整窗口大小时调用；尽可能使用防抖。

## 减少同时执行的工作

- 当屏幕外或非活动状态的动画不可见时（例如用户离开当前页面），暂停或终止这些动画。
- 避免同时为大量元素的众多属性创建动画；必要时应简化动画或按顺序执行。

## 最佳实践

- ✅ 为 **transform** 和 **opacity** 创建动画；仅对会执行动画的元素在 CSS 中使用 **will-change**。
- ✅ 当动画相同时，使用 **stagger**，而不是创建许多带有手动延迟的独立补间动画。
- ✅ 对频繁更新的属性（例如鼠标跟随效果）使用 **gsap.quickTo()**。
- ✅ 清理或终止屏幕外动画；在布局变化时调用 **ScrollTrigger.refresh()**，并尽可能使用防抖。

## 不要这样做

- ❌ 当 **x**/**y**/**scale** 可以实现相同视觉效果时，不要通过为 **width**/**height**/**top**/**left** 创建动画来移动元素。
- ❌ 不要“以防万一”就为每个元素设置 **will-change** 或 **force3D**；仅对实际执行动画的元素使用它们。
- ❌ 未经低端设备测试，不要创建数百个相互重叠的补间动画或 ScrollTrigger。
- ❌ 不要忽略清理；遗留的补间动画和 ScrollTrigger 会持续运行，并可能影响性能和正确性。
