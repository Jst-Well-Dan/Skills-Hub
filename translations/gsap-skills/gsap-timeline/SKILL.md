<!-- source-sha256: 1a8b0f39cc4be3ed3d834b89672e4ae2f151b901dc3450bebf10bbc45379fe02 -->
---
name: gsap-timeline
description: 官方 GSAP 时间线技能——gsap.timeline()、位置参数、嵌套和播放控制。适用于编排动画顺序、协调关键帧，或用户询问动画编排、时间线或动画顺序时（无论是在 GSAP 中，还是在推荐支持时间线的库时）。
license: MIT
---

# GSAP 时间线

## 何时使用此技能

适用于构建多步骤动画、按顺序或并行协调多个补间动画，或用户询问 GSAP 中的时间线、动画排序或关键帧式动画时。

**相关技能：** 对于单个补间动画和缓动，请使用 **gsap-core**；对于滚动驱动的时间线，请使用 **gsap-scrolltrigger**；对于 React，请使用 **gsap-react**。

## 创建时间线

```javascript
const tl = gsap.timeline();
tl.to(".a", { x: 100, duration: 1 })
  .to(".b", { y: 50, duration: 0.5 })
  .to(".c", { opacity: 0, duration: 0.3 });
```

默认情况下，补间动画会依次**追加**。使用**位置参数**可将补间动画放置在特定时间，或相对于其他补间动画进行定位。

## 位置参数

第三个参数（或 vars 中的 position 属性）控制放置位置：

- **绝对位置**：`1`——在第 1 秒开始。
- **相对位置（默认）**：`"+=0.5"`——在结束后 0.5 秒；`"-=0.2"`——在结束前 0.2 秒。
- **标签**：`"labelName"`——位于该标签处；`"labelName+=0.3"`——在标签后 0.3 秒。
- **放置方式**：`"<"`——在最近添加的动画开始时启动；`">"`——在最近添加的动画结束时启动（默认）；`"<0.2"`——在最近添加的动画开始后 0.2 秒启动。

示例：

```javascript
tl.to(".a", { x: 100 }, 0);           // 在 0 秒
tl.to(".b", { y: 50 }, "+=0.5");      // 在上一个动画结束后 0.5 秒
tl.to(".c", { opacity: 0 }, "<");     // 与上一个动画同时开始
tl.to(".d", { scale: 2 }, "<0.2");    // 在上一个动画开始后 0.2 秒
```

## 时间线默认值

将默认值传入时间线，使所有子补间动画继承这些值：

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 }).to(".b", { y: 50 }); // 两者均使用 0.5 秒和 power2.out
```

## 时间线选项（构造函数）

- **paused: true**——创建时暂停；调用 `.play()` 开始播放。
- **repeat**、**yoyo**——与补间动画相同；应用于整个时间线。
- **onComplete**、**onStart**、**onUpdate**——时间线级别的回调。
- **defaults**——合并到每个子补间动画中的 vars。

## 标签

添加并使用标签，使动画编排清晰易读且便于维护：

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");
tl.addLabel("outro", "+=0.5");
tl.to(".b", { opacity: 0 }, "outro");
tl.play("outro");  // 从 "outro" 开始
tl.tweenFromTo("intro", "outro"); // 暂停时间线并返回一个新的 Tween，该 Tween 会让时间线的播放头从 intro 动画到 outro，且不使用缓动。
```

## 嵌套时间线

时间线可以包含其他时间线。

```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });
master.add(child, 0);
master.to(".c", { opacity: 0 }, "+=0.2");
```

## 控制播放

- **tl.play()** / **tl.pause()**
- **tl.reverse()** / 先执行 **tl.progress(1)**，然后执行 **tl.reverse()**
- **tl.restart()**——从头开始。
- **tl.time(2)**——跳转到第 2 秒。
- **tl.progress(0.5)**——跳转到 50%。
- **tl.kill()**——终止时间线以及（默认情况下）其子动画。

## GSAP 官方最佳实践

- ✅ 优先使用时间线进行动画编排
- ✅ 使用**位置参数**（第三个参数），将补间动画放置在特定时间或相对于标签的位置。
- ✅ 使用 `addLabel()` 添加**标签**，使动画编排清晰易读且便于维护。
- ✅ 将 **defaults** 传入时间线构造函数，使子补间动画继承 duration、ease 等属性。
- ✅ 将 ScrollTrigger 放在时间线（或顶层补间动画）上，而不是放在时间线内部的补间动画上。

## 请勿

- ❌ 当可以用**时间线**编排动画时，不要通过 **delay** 串联动画；对于多步骤动画，应优先使用 `gsap.timeline()` 和位置参数。
- ❌ 当许多子补间动画共用相同的 duration 或 ease 时，不要忘记传入 **defaults**（例如 `defaults: { duration: 0.5, ease: "power2.out" }`）。
- ❌ 不要忘记：时间线构造函数上的 **duration** 与补间动画的 duration 并不相同；时间线的“duration”由其子动画决定。
- ❌ 不要嵌套包含 ScrollTrigger 的动画；ScrollTrigger 只能放在顶层 Tween/Timeline 上。
