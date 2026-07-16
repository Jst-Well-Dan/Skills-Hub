<!-- source-sha256: 1927bcc4ea95b38203404ad5ea1d060b15c4a886c65ae53e885ff1793aabe0ba -->
---
name: gsap-utils
description: GSAP 官方 gsap.utils 技能——clamp、mapRange、normalize、interpolate、random、snap、toArray、wrap、pipe。当用户询问 gsap.utils、clamp、mapRange、random、snap、toArray、wrap 或 GSAP 中的辅助工具时使用。
license: MIT
---

# gsap.utils

## 何时使用此技能

在编写或审查使用 **gsap.utils** 进行数学计算、数组/集合处理、单位解析或动画数值映射的代码时应用（例如，将滚动位置映射为某个值、随机化、吸附到网格或归一化输入）。

**相关技能：**构建动画时与 **gsap-core**、**gsap-timeline** 和 **gsap-scrolltrigger** 配合使用；CustomEase 和其他缓动工具位于 **gsap-plugins** 中。

## 概述

**gsap.utils** 提供纯辅助工具，无需注册。可在补间变量（例如基于函数的值）、ScrollTrigger 或 Observer 回调中使用，也可在任何驱动 GSAP 的 JS 中使用。所有工具都位于 **gsap.utils** 下（例如 `gsap.utils.clamp()`）。

**省略值：函数形式。**许多工具将待转换的值作为**最后一个**参数。如果省略该参数，工具将返回一个稍后接收该值的**函数**。当需要使用相同配置对多个值执行限制、映射、归一化或吸附时，请使用函数形式（例如在 mousemove 处理程序或补间回调中）。**例外：random()**——将 **true** 作为最后一个参数传入，即可获得可复用函数（不要省略值）；参见 [random()](https://gsap.com/docs/v3/GSAP/UtilityMethods/random/)。

```javascript
// With value: returns the result
gsap.utils.clamp(0, 100, 150); // 100

// Without value: returns a function you call with the value later
let c = gsap.utils.clamp(0, 100);
c(150);  // 100
c(-10);  // 0
```

## 限制与范围

### clamp(min, max, value?)

将值限制在 min 和 max 之间。省略 **value** 可获得函数：`clamp(min, max)(value)`。

```javascript
gsap.utils.clamp(0, 100, 150); // 100
gsap.utils.clamp(0, 100, -10); // 0

let clampFn = gsap.utils.clamp(0, 100);
clampFn(150); // 100
```

### mapRange(inMin, inMax, outMin, outMax, value?)

将值从一个范围映射到另一个范围。适用于将滚动位置、进度（0–1）或输入范围转换为动画范围。省略 **value** 可获得函数：`mapRange(inMin, inMax, outMin, outMax)(value)`。

```javascript
gsap.utils.mapRange(0, 100, 0, 500, 50);  // 250
gsap.utils.mapRange(0, 1, 0, 360, 0.5);   // 180 (progress to degrees)

let mapFn = gsap.utils.mapRange(0, 100, 0, 500);
mapFn(50);  // 250
```

### normalize(min, max, value?)

返回给定范围内归一化为 0–1 的值。当目标范围为 0–1 时，它是映射的逆操作。省略 **value** 可获得函数：`normalize(min, max)(value)`。

```javascript
gsap.utils.normalize(0, 100, 50);   // 0.5
gsap.utils.normalize(100, 300, 200); // 0.5

let normFn = gsap.utils.normalize(0, 100);
normFn(50); // 0.5
```

### interpolate(start, end, progress?)

根据给定进度（0–1）在两个值之间进行插值。支持数字、颜色以及键相匹配的对象。省略 **progress** 可获得函数：`interpolate(start, end)(progress)`。

```javascript
gsap.utils.interpolate(0, 100, 0.5);       // 50
gsap.utils.interpolate("#ff0000", "#0000ff", 0.5); // mid color
gsap.utils.interpolate({ x: 0, y: 0 }, { x: 100, y: 50 }, 0.5); // { x: 50, y: 25 }

let lerp = gsap.utils.interpolate(0, 100);
lerp(0.5); // 50
```

## 随机与吸附

### random(minimum, maximum[, snapIncrement, returnFunction]) / random(array[, returnFunction])

返回 **minimum**–**maximum** 范围内的随机数，或从 **array** 中返回一个随机元素。可选的 **snapIncrement** 会将结果吸附到最近的倍数（例如 `5` → 5 的倍数）。**要获得可复用函数**，请将 **true** 作为最后一个参数（**returnFunction**）传入；返回的函数不接收参数，每次调用都会返回一个新的随机值。这是唯一使用 `true` 获取函数形式，而不是通过省略值来实现的工具。

```javascript
// immediate value: number in range
gsap.utils.random(-100, 100);        // e.g. 42.7
gsap.utils.random(0, 500, 5);        // 0–500, snapped to nearest 5

// reusable function: pass true as last argument
let randomFn = gsap.utils.random(-200, 500, 10, true);
randomFn();  // random value in range, snapped to 10
randomFn();  // another random value

// array: pick one value at random
gsap.utils.random(["red", "blue", "green"]);  // "red", "blue", or "green"
let randomFromArray = gsap.utils.random([0, 100, 200], true);
randomFromArray();  // 0, 100, or 200
```

**补间变量中的字符串形式：**使用 `"random(-100, 100)"`、`"random(-100, 100, 5)"` 或 `"random([0, 100, 200])"`；GSAP 会针对每个目标对其求值。

```javascript
gsap.to(".box", { x: "random(-100, 100, 5)", duration: 1 });
gsap.to(".item", { backgroundColor: "random([red, blue, green])" });
```

### snap(snapTo, value?)

将值吸附到 **snapTo** 的最近倍数，或吸附到允许值数组中最接近的值。省略 **value** 可获得函数：`snap(snapTo)(value)`（或 `snap(snapArray)(value)`）。

```javascript
gsap.utils.snap(10, 23);     // 20
gsap.utils.snap(0.25, 0.7);  // 0.75
gsap.utils.snap([0, 100, 200], 150); // 100 or 200 (nearest in array)

let snapFn = gsap.utils.snap(10);
snapFn(23); // 20
```

在补间中用于基于网格或步进的动画：

```javascript
gsap.to(".x", { x: 200, snap: { x: 20 } });
```

### shuffle(array)

返回一个包含相同元素但顺序随机的新数组。用于随机排列顺序（例如使用副本实现从 `"random"` 开始的交错效果）。

```javascript
gsap.utils.shuffle([1, 2, 3, 4]); // e.g. [3, 1, 4, 2]
```

### distribute(config)

**返回一个函数**，该函数根据每个目标在数组中（或网格中）的位置为其分配值。它在内部用于高级交错效果；当需要将值分布到多个元素上时均可使用（例如 scale、opacity、x、delay）。返回的函数接收 `(index, target, targets)`——既可以手动调用，也可以将结果直接传入补间；GSAP 会针对每个目标，以索引、元素和数组作为参数调用它。

**配置（全部可选）：**

| 属性 | 类型 | 说明 |
|----------|------|-------------|
| `base` | Number | 起始值。默认为 `0`。 |
| `amount` | Number | 在所有目标间分配的总量（加到 base 上）。例如，100 个目标配合 `amount: 1` → 每个目标之间相差 0.01。若要为每个目标设置固定步长，请改用 **each**。 |
| `each` | Number | 每个目标之间增加的量（加到 base 上）。例如，4 个目标配合 `each: 1` → 0、1、2、3。若要拆分一个总量，请改用 **amount**。 |
| `from` | Number \| String \| Array | 分布的起始位置：索引，或 `"start"`、`"center"`、`"edges"`、`"random"`、`"end"`，也可以是 `[0.25, 0.75]` 这样的比例。默认为 `0`。 |
| `grid` | String \| Array | 使用网格位置而不是平面索引：`[rows, columns]`（例如 `[5, 10]`），或使用 `"auto"` 自动检测。平面数组请省略。 |
| `axis` | String | 用于网格：限制为单个轴（`"x"` 或 `"y"`）。 |
| `ease` | Ease | 沿缓动曲线分布值（例如 `"power1.inOut"`）。默认为 `"none"`。 |

**在补间中：**将 `distribute(config)` 的结果作为属性值传入；GSAP 会针对每个目标，以 `(index, target, targets)` 调用该函数。

```javascript
// Scale: middle elements 0.5, outer edges 3 (amount 2.5 distributed from center)
gsap.to(".class", {
  scale: gsap.utils.distribute({
    base: 0.5,
    amount: 2.5,
    from: "center"
  })
});
```

**手动使用：**使用 `(index, target, targets)` 调用返回的函数，以获取该索引对应的值。

```javascript
const distributor = gsap.utils.distribute({
  base: 50,
  amount: 100,
  from: "center",
  ease: "power1.inOut"
});
const targets = gsap.utils.toArray(".box");
const valueForIndex2 = distributor(2, targets[2], targets);
```

更多信息请参阅 [distribute()](https://gsap.com/docs/v3/GSAP/UtilityMethods/distribute/)。

## 单位与解析

### getUnit(value)

返回值的单位字符串（例如 `"px"`、`"%"`、`"deg"`）。适用于值的归一化或转换。

```javascript
gsap.utils.getUnit("100px");   // "px"
gsap.utils.getUnit("50%");     // "%"
gsap.utils.getUnit(42);        // "" (unitless)
```

### unitize(value, unit)

为数字附加单位；如果值已有单位，则原样返回。适用于构建 CSS 值或补间结束值。

```javascript
gsap.utils.unitize(100, "px");  // "100px"
gsap.utils.unitize("2rem", "px"); // "2rem" (unchanged)
```

### splitColor(color, returnHSL?)

将颜色字符串转换为数组：**[red, green, blue]**（0–255），或 **[red, green, blue, alpha]**（当存在或需要 alpha 时为 4 个元素）。将 **true** 作为第二个参数（**returnHSL**）传入，则改为获得 **[hue, saturation, lightness]** 或 **[hue, saturation, lightness, alpha]**（HSL/HSLA）。支持 `"rgb()"`、`"rgba()"`、`"hsl()"`、`"hsla()"`、十六进制以及命名颜色（例如 `"red"`）。适用于动画化颜色分量或构建渐变。参见 [splitColor()](https://gsap.com/docs/v3/GSAP/UtilityMethods/splitColor/)。

```javascript
gsap.utils.splitColor("red");                    // [255, 0, 0]
gsap.utils.splitColor("#6fb936");                // [111, 185, 54]
gsap.utils.splitColor("rgba(204, 153, 51, 0.5)"); // [204, 153, 51, 0.5] (4 elements)
gsap.utils.splitColor("#6fb936", true);          // [94, 55, 47] (HSL: hue, saturation, lightness)
```

## 数组与集合

### selector(scope)

返回一个限定作用域的选择器函数，该函数只在给定元素（或 ref）内查找元素。在组件中使用它，可使 `".box"` 等选择器仅匹配该组件的后代元素，而不是整个文档。接受 DOM 元素或 ref（例如 React ref；支持 `.current`）。

```javascript
const q = gsap.utils.selector(containerRef);
q(".box");        // array of .box elements inside container
gsap.to(q(".circle"), { x: 100 });
```

### toArray(value, scope?)

将值转换为数组：选择器字符串（作用域限定到元素）、NodeList、HTMLCollection、单个元素或数组。当向 GSAP 传入混合输入（例如目标），并且需要真正的数组时使用。

```javascript
gsap.utils.toArray(".item");           // array of elements
gsap.utils.toArray(".item", container); // scoped to container
gsap.utils.toArray(nodeList);          // [ ... ] from NodeList
```

### pipe(...functions)

组合函数：**pipe(f1, f2, f3)(value)** 返回 f3(f2(f1(value)))。适用于在补间或回调中应用一连串转换（例如 normalize → mapRange → snap）。

```javascript
const fn = gsap.utils.pipe(
  (v) => gsap.utils.normalize(0, 100, v),
  (v) => gsap.utils.snap(0.1, v)
);
fn(50); // normalized then snapped
```

### wrap(min, max, value?)

将值循环映射到 min–max 范围内（包含 min，不包含 max）。适用于无限滚动或循环值。省略 **value** 可获得函数：`wrap(min, max)(value)`。

```javascript
gsap.utils.wrap(0, 360, 370);  // 10
gsap.utils.wrap(0, 360, -10);   // 350

let wrapFn = gsap.utils.wrap(0, 360);
wrapFn(370); // 10
```

### wrapYoyo(min, max, value?)

以悠悠球方式将值循环映射到范围内（在两端反弹）。适用于在范围内往返变化。省略 **value** 可获得函数：`wrapYoyo(min, max)(value)`。

```javascript
gsap.utils.wrapYoyo(0, 100, 150); // 50 (bounces back)

let wrapY = gsap.utils.wrapYoyo(0, 100);
wrapY(150); // 50
```

## 最佳实践

- ✅ 当多次使用相同范围/配置时（例如滚动处理程序、补间回调），省略值参数以获得可复用函数：`let mapFn = gsap.utils.mapRange(0, 1, 0, 360); mapFn(progress)`。
- ✅ 对齐网格或基于步进的值使用 **snap**；当 GSAP 或你的代码需要从选择器或 NodeList 获得真正的数组时，使用 **toArray**。
- ✅ 在组件中使用 **gsap.utils.selector(scope)**，使选择器的作用域限定于容器或 ref。

## 请勿

- ❌ 假设 **mapRange** / **normalize** 会处理单位；它们仅处理数字。当单位很重要时，请使用 **getUnit** / **unitize**。
- ❌ 覆盖或依赖未记录的行为；请遵循文档中规定的 API。

### 了解更多

https://gsap.com/docs/v3/HelperFunctions
