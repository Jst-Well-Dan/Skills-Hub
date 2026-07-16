<!-- source-sha256: 5838b856c74c07fbc9fa99b6dfd1eee34ea554c3e530c30e0d58014b707d70a4 -->
---
name: gsap-plugins
description: 官方 GSAP 插件技能——涵盖注册、ScrollToPlugin、ScrollSmoother、Flip、Draggable、Inertia、Observer、SplitText、ScrambleText、SVG 和物理插件、CustomEase、EasePack、CustomWiggle、CustomBounce、GSDevTools。当用户询问 GSAP 插件、滚动到指定位置、FLIP 动画、拖拽、SVG 绘制或插件注册时使用。
license: MIT
---

# GSAP 插件

## 何时使用此技能

在使用或审查采用 GSAP 插件的代码时应用：注册插件、滚动到指定位置、FLIP 动画、可拖拽元素、SVG（DrawSVG、MorphSVG、MotionPath）、文本（SplitText、ScrambleText）、物理效果、缓动插件（CustomEase、EasePack、CustomWiggle、CustomBounce）或 GSDevTools。ScrollTrigger 有其独立技能（gsap-scrolltrigger）。

**相关技能：** 核心补间动画使用 **gsap-core**；ScrollTrigger 使用 **gsap-scrolltrigger**；React 使用 **gsap-react**。

## 许可与安装（重要）

所有 GSAP 插件都**免费**，包括商业用途。自 [Webflow 收购 GSAP](https://gsap.com/blog/webflow-GSAP/) 后，Club GSAP 不再是付费层级，并且**任何插件都不再需要会员资格、许可证密钥或身份验证令牌**——这也包括以前仅限 Club 使用的插件（**SplitText**、**MorphSVG** 等）。

- ✅ 从公开的 `gsap` npm 包安装所有内容：`npm install gsap`。所有插件均已包含——通过 `gsap/SplitText`、`gsap/MorphSVGPlugin` 等路径导入。
- ❌ **不要**生成带有 GreenSock 身份验证令牌的 `.npmrc`，不要建议使用私有的 `npm.greensock.com` 注册表，也不要告诉用户注册 Club GSAP 才能访问插件。这些说明已经过时。

## 注册插件

每个插件只需注册一次，以便 GSAP（以及打包工具）知道需要将其包含进来。对项目中使用的每个插件调用 **gsap.registerPlugin()**：

```javascript
import gsap from "gsap";
import { ScrollToPlugin } from "gsap/ScrollToPlugin";
import { Flip } from "gsap/Flip";
import { Draggable } from "gsap/Draggable";

gsap.registerPlugin(ScrollToPlugin, Flip, Draggable);
```

- ✅ 在任何补间动画或 API 调用中使用插件之前完成注册。
- ✅ 在 React 中，应在顶层或应用中注册一次（例如首次使用 useGSAP 之前）；不要在会重新渲染的组件内部注册。useGSAP 本身是一个插件，需要在使用前注册。

## 滚动

### ScrollToPlugin

为滚动位置（窗口或可滚动元素）添加动画。适用于不使用 ScrollTrigger 的“滚动到元素”或“滚动到位置”场景。

```javascript
gsap.registerPlugin(ScrollToPlugin);

gsap.to(window, { duration: 1, scrollTo: { y: 500 } });
gsap.to(window, { duration: 1, scrollTo: { y: "#section", offsetY: 50 } });
gsap.to(scrollContainer, { duration: 1, scrollTo: { x: "max" } });
```

**ScrollToPlugin——关键配置（scrollTo 对象）：**

| 选项 | 说明 |
|--------|-------------|
| `x`, `y` | 目标滚动位置（数字），或使用 `"max"` 表示最大值 |
| `element` | 要滚动到的选择器或元素（用于滚动到可视区域） |
| `offsetX`, `offsetY` | 相对于目标位置的像素偏移量 |

### ScrollSmoother

平滑滚动包装器（使原生滚动更平滑）。需要 ScrollTrigger 和特定的 DOM 结构（内容包装器 + 平滑滚动包装器）。需要平滑、带动量感的滚动时使用。设置方法请参阅 GSAP 文档；应在 ScrollTrigger 之后注册。DOM 结构如下：

```html
<body>
	<div id="smooth-wrapper">
		<div id="smooth-content">
			<!--- ALL YOUR CONTENT HERE --->
		</div>
	</div>
	<!-- position: fixed elements can go outside --->
</body>
```

## DOM / UI

### Flip

先使用 `Flip.getState()` 捕获状态，然后应用更改（例如布局或类更改），再使用 `Flip.from()` 从先前状态动画过渡到新状态（FLIP：First、Last、Invert、Play）。适用于在两种布局状态之间制作动画（列表、网格、展开/折叠）。

```javascript
gsap.registerPlugin(Flip);

const state = Flip.getState(".item");
// change DOM (reorder, add/remove, change classes)
Flip.from(state, { duration: 0.5, ease: "power2.inOut" });
```

**Flip——关键配置（Flip.from vars）：**

| 选项 | 说明 |
|--------|-------------|
| `absolute` | 在翻转期间使用 `position: absolute`（默认值：`false`） |
| `nested` | 为 true 时，只测量第一层子元素（更适合嵌套变换） |
| `scale` | 为 true 时，缩放元素以适应尺寸（避免拉伸）；默认值为 `true` |
| `simple` | 为 true 时，只对位置/缩放制作动画（速度更快、精度较低） |
| `duration`, `ease` | 标准补间动画选项 |

#### 更多信息

https://gsap.com/docs/v3/Plugins/Flip

### Draggable

使元素能够通过鼠标/触摸进行拖拽、旋转或投掷。适用于滑块、卡片、可重新排序列表或任何拖拽交互。

```javascript
gsap.registerPlugin(Draggable, InertiaPlugin);

Draggable.create(".box", { type: "x,y", bounds: "#container", inertia: true });
Draggable.create(".knob", { type: "rotation" });
```

**Draggable——关键配置选项：**

| 选项 | 说明 |
|--------|-------------|
| `type` | `"x"`、`"y"`、`"x,y"`、`"rotation"`、`"scroll"` |
| `bounds` | 用于限制拖拽范围的元素、选择器或 `{ minX, maxX, minY, maxY }` |
| `inertia` | 设置为 `true` 以启用投掷/动量效果（需要 InertiaPlugin） |
| `edgeResistance` | 0–1；拖拽越过边界时的阻力 |
| `cursor` | 拖拽期间使用的 CSS 光标 |
| `onDragStart`, `onDrag`, `onDragEnd` | 回调；接收事件和目标 |
| `onThrowUpdate`, `onThrowComplete` | 惯性处于活动状态时的回调 |

### Inertia（InertiaPlugin）

可与 Draggable 配合，在释放后产生动量；也可以跟踪任意对象任意属性的惯性/速度，从而通过简单的补间动画无缝滑行至停止。使用 `inertia: true` 时与 Draggable 一起注册：

```javascript
gsap.registerPlugin(Draggable, InertiaPlugin);
Draggable.create(".box", { type: "x,y", inertia: true });
```

或者跟踪某个属性的速度：

```javascript
InertiaPlugin.track(".box", "x");
```

然后使用 `"auto"` 延续当前速度并滑行至停止：

```javascript
gsap.to(obj, { inertia: { x: "auto" } });
```

### Observer

统一不同设备上的指针和滚动输入。适用于滑动、滚动方向或自定义手势逻辑，而不像 ScrollTrigger 那样直接绑定到滚动位置。

```javascript
gsap.registerPlugin(Observer);

Observer.create({
  target: "#area",
  onUp: () => {},
  onDown: () => {},
  onLeft: () => {},
  onRight: () => {},
  tolerance: 10
});
```

**Observer——关键配置选项：**

| 选项 | 说明 |
|--------|-------------|
| `target` | 要观察的元素或选择器 |
| `onUp`, `onDown`, `onLeft`, `onRight` | 滑动/滚动在对应方向上超过容差时执行的回调 |
| `tolerance` | 检测到方向前需要移动的像素数；默认值为 10 |
| `type` | `"touch"`、`"pointer"` 或 `"wheel"`（默认值：`"touch,pointer"`） |

## 文本

### SplitText

将元素文本拆分为字符、单词和/或行（每一项各自位于独立元素中），以实现交错动画或逐项动画。适用于逐字符、逐单词或逐行动画。返回的实例包含 **chars**、**words**、**lines**（设置 `mask` 时还包含 **masks**）。使用 **revert()** 恢复原始标记，或让 **gsap.context()** 执行恢复。可与 **gsap.context()**、**matchMedia()** 和 **useGSAP()** 集成。API：**SplitText.create(target, vars)**（target = 选择器、元素或数组）。

```javascript
gsap.registerPlugin(SplitText);

const split = SplitText.create(".heading", { type: "words, chars" });
gsap.from(split.chars, { opacity: 0, y: 20, stagger: 0.03, duration: 0.4 });
// later: split.revert() or let gsap.context() cleanup revert
```

使用 **onSplit()**（v3.13.0+）时，动画会在每次拆分时运行；使用 **autoSplit** 时，也会在重新拆分时运行。从 **onSplit()** 返回补间动画/时间线，可让 SplitText 在重新拆分时进行清理并同步进度：

```javascript
SplitText.create(".split", {
  type: "lines",
  autoSplit: true,
  onSplit(self) {
    return gsap.from(self.lines, { y: 100, opacity: 0, stagger: 0.05, duration: 0.5 });
  }
});
```

**SplitText——关键配置（SplitText.create vars）：**

| 选项 | 说明 |
|--------|-------------|
| **type** | 逗号分隔：`"chars"`、`"words"`、`"lines"`。默认值为 `"chars,words,lines"`。为了性能，只拆分需要的内容（例如不使用行时采用 `"words, chars"`）。避免仅拆分字符而不拆分单词/行，或者使用 **smartWrap: true** 防止异常换行。 |
| **charsClass**, **wordsClass**, **linesClass** | 每个拆分元素上的 CSS 类。追加 `"++"` 可添加递增类名（例如 `linesClass: "line++"` → `line1`、`line2`、…）。 |
| **aria** | `"auto"`（默认值）、`"hidden"` 或 `"none"`。无障碍功能：`"auto"` 会在拆分元素上添加 `aria-label`，并在线/单词/字符元素上添加 `aria-hidden`，使屏幕阅读器读取标签；`"hidden"` 对阅读器隐藏全部内容；`"none"` 保持 aria 不变。如果必须公开嵌套链接/语义，请使用 `"none"` 并添加仅供屏幕阅读器使用的副本。 |
| **autoSplit** | 为 `true` 时，会在字体加载完成后，或元素宽度发生变化（并且拆分了行）时恢复并重新拆分，从而避免错误换行。**动画必须在 onSplit() 内创建**，使其指向新拆分的元素；从 **onSplit()** **返回**动画，可在重新拆分时自动清理并同步时间。 |
| **onSplit(self)** | 拆分完成时的回调（如果 **autoSplit** 为 `true`，则每次重新拆分时也会调用）。接收 SplitText 实例。返回 GSAP 补间动画或时间线，可在重新拆分时自动恢复/同步该动画。 |
| **mask** | `"lines"`、`"words"` 或 `"chars"`。使用一个带有 `overflow: clip` 的额外元素包装每个单元，以实现遮罩/揭示效果。只能选择一种类型；通过实例的 **masks** 数组访问包装器（如果设置了类，也可使用类 `-mask`）。 |
| **tag** | 包装元素标签；默认值为 `"div"`。内联内容使用 `"span"`（注意：在某些浏览器中，旋转/缩放等变换可能无法在内联元素上呈现）。 |
| **deepSlice** | 为 `true`（默认值）时，会细分跨越多行的嵌套元素（例如 `<strong>`），防止行在垂直方向上拉伸。仅在拆分行时适用。 |
| **ignore** | 保持不拆分的选择器或元素（例如 `ignore: "sup"`）。 |
| **smartWrap** | 仅拆分**字符**时，使用 `white-space: nowrap` 的 span 包装单词，避免在单词中间换行。如果同时拆分单词或行，则忽略此选项。默认值为 `false`。 |
| **wordDelimiter** | 单词边界：字符串（默认值为 `" "`）、RegExp，或用于自定义拆分的 `{ delimiter: RegExp, replaceWith: string }`（例如用于话题标签或非拉丁文字的零宽连接符）。 |
| **prepareText(text, parent)** | 接收原始文本和父元素的函数；返回拆分前修改后的文本（例如为不使用空格的语言插入换行标记）。 |
| **propIndex** | 为 `true` 时，会在每个拆分元素上添加包含索引的 CSS 变量（例如 `--word: 1`、`--char: 2`）。 |
| **reduceWhiteSpace** | 折叠连续空格；默认值为 `true`。从 v3.13.0 开始，还会遵循换行，并可为 `<pre>` 插入 `<br>`。 |
| **onRevert** | 实例恢复时执行的回调。 |

**提示：** 只拆分需要制作动画的内容（例如只对单词制作动画时跳过字符拆分）。使用自定义字体时，请在字体加载后进行拆分（例如 `document.fonts.ready.then(...)`），或者使用 **autoSplit: true** 搭配 **onSplit()**。为了避免拆分字符时字距发生偏移，请使用 CSS `font-kerning: none; text-rendering: optimizeSpeed;`。避免使用 `text-wrap: balance`，因为它可能干扰拆分。SplitText 不支持 SVG `<text>`。

**了解更多：** [SplitText](https://gsap.com/docs/v3/Plugins/SplitText/)

### ScrambleText

使用字符扰乱/故障效果为文本制作动画。适用于以扰乱效果揭示或过渡文本。

```javascript
gsap.registerPlugin(ScrambleTextPlugin);

gsap.to(".text", {
  duration: 1,
  scrambleText: { text: "New message", chars: "01", revealDelay: 0.5 }
});
```

## SVG

### DrawSVG（DrawSVGPlugin）

通过为 `stroke-dashoffset` / `stroke-dasharray` 制作动画，揭示或隐藏 SVG 元素的描边。适用于 `<path>`、`<line>`、`<polyline>`、`<polygon>`、`<rect>`、`<ellipse>`。用于“绘制”或“擦除”描边。

**drawSVG 值：** 描述路径上描边的**可见区段**（起点和终点位置），并非“随时间从 A 动画到 B”。格式：以百分比或长度表示的 `"start end"`。示例：`"0% 100%"` = 完整描边；`"20% 80%"` = 仅显示 20% 到 80% 之间的描边（两端存在空隙）。补间动画会从元素的**当前**区段动画到**目标**区段——例如 `gsap.to("#path", { drawSVG: "0% 100%" })` 会从当前状态动画到完整描边。单个值（例如 `0`、`"100%"`）表示起点为 0：`"100%"` 等同于 `"0% 100%"`。

**必要条件：** 元素必须具有可见描边——请通过 CSS 或 SVG 属性设置 `stroke` 和 `stroke-width`，否则不会绘制任何内容。

```javascript
gsap.registerPlugin(DrawSVGPlugin);

// draw from nothing to full stroke
gsap.from("#path", { duration: 1, drawSVG: 0 });
// or explicit segment: from 0–0 to 0–100%
gsap.fromTo("#path", { drawSVG: "0% 0%" }, { drawSVG: "0% 100%", duration: 1 });
// stroke only in the middle (gaps at ends)
gsap.to("#path", { duration: 1, drawSVG: "20% 80%" });
```

**注意事项：** 仅影响描边（不影响填充）。优先使用单区段 `<path>` 元素；多区段路径在某些浏览器中可能呈现异常。无法通过视觉方式更改 `<use>` 的内容。**DrawSVGPlugin.getLength(element)** 和 **DrawSVGPlugin.getPosition(element)** 分别返回描边长度和当前位置。

**了解更多：** [DrawSVG](https://gsap.com/docs/v3/Plugins/DrawSVGPlugin)

### MorphSVG（MorphSVGPlugin）

通过为 `d` 属性（路径数据）制作动画，将一个 SVG 形状变形为另一个形状。起始形状和结束形状不需要具有相同数量的点——MorphSVG 会将其转换为三次贝塞尔曲线，并根据需要添加点。适用于图标之间的变形、形状过渡或基于路径的动画。支持 `<path>`、`<polyline>` 和 `<polygon>`；`<circle>`、`<rect>`、`<ellipse>` 和 `<line>` 会在内部转换，也可通过 **MorphSVGPlugin.convertToPath(selector | element)** 转换（将 DOM 中的元素替换为 `<path>`）。

**morphSVG 值：** 可以是**选择器**（例如 `"#lightning"`）、**元素**、**原始路径数据**（例如 `"M47.1,0.8 73.3,0.8..."`），或者对于 polygon/polyline，可以是**点字符串**（例如 `"240,220 240,70 70,70 70,220"`）。如需完整配置，请使用**对象形式**，其中 **shape** 是唯一必需的属性。

```javascript
gsap.registerPlugin(MorphSVGPlugin);

// convert primitives to path first if needed:
MorphSVGPlugin.convertToPath("circle, rect, ellipse, line");

gsap.to("#diamond", { duration: 1, morphSVG: "#lightning", ease: "power2.inOut" });
// object form:
gsap.to("#diamond", {
  duration: 1,
  morphSVG: { shape: "#lightning", type: "rotational", shapeIndex: 2 }
});

```

**MorphSVG——关键配置（morphSVG 对象）：**

| 选项 | 说明 |
|--------|-------------|
| **shape** | _（必需。）_ 目标形状：选择器、元素或原始路径字符串。 |
| **type** | `"linear"`（默认值）或 `"rotational"`。Rotational 使用角度/长度插值，可避免变形过程中出现折结；当 linear 效果不正确时可以尝试。 |
| **map** | 区段的匹配方式：`"size"`（默认值）、`"position"` 或 `"complexity"`。当起始/结束区段无法对齐时使用；如果都不起作用，请拆分成多个路径，并分别进行变形。 |
| **shapeIndex** | 偏移起始路径中映射到结束路径第一个点的点（避免形状“交叉”或翻转）。单区段路径使用数字；多区段路径使用**数组**（例如 `[5, 1, -8]`）。负数会反转对应区段。先使用一次 **shapeIndex: "log"** 将自动计算值记录到日志，然后把数字/数组粘贴到补间动画中。**findShapeIndex(start, end)**（独立工具）提供交互式 UI，用于寻找合适的值。仅适用于闭合路径。 |
| **smooth** | （v3.14+）。添加平滑点。可以是数字（例如 `80`）、`"auto"` 或对象：`{ points: 40 \| "auto", redraw: true \| false, persist: true \| false }`。`redraw: false` 保留原始锚点（完全忠实、间距不太均匀）。`persist: false` 在补间动画结束时移除添加的点。当默认变形显得锯齿明显或不自然时使用。 |
| **curveMode** | 布尔值（v3.14+）。对控制手柄的角度/长度进行插值，而不是对原始 x/y 进行插值，以避免曲线产生折结。如果变形过程中间出现折结，可以尝试使用。 |
| **origin** | **type: "rotational"** 的旋转原点。字符串：`"50% 50%"`（默认值），或使用 `"20% 60%, 35% 90%"` 为起始/结束状态指定不同的原点。 |
| **precision** | 输出路径数据的小数位数；默认值为 `2`。 |
| **precompile** | 预计算路径字符串的数组（也可以先使用一次 **precompile: "log"**，再从控制台复制）。跳过开销较大的启动计算；适用于非常复杂的变形。仅适用于 `<path>`（请先转换 polygon/polyline）。 |
| **render** | 每次更新时调用的函数 rawPath, target——例如绘制到 canvas。RawPath 是一个区段数组（每个区段都是由交替排列的 x、y 三次贝塞尔坐标组成的数组）。 |
| **updateTarget** | 使用 **render**（例如仅使用 canvas）时，设置 **updateTarget: false**，使原始 `<path>` 不被更新。**MorphSVGPlugin.defaultUpdateTarget** 用于设置默认值。 |

**工具：** **MorphSVGPlugin.convertToPath(selector | element)** 将 DOM 中的 circle/rect/ellipse/line/polygon/polyline 转换为 `<path>`。**MorphSVGPlugin.rawPathToString(rawPath)** 和 **stringToRawPath(d)** 用于在路径字符串与原始数组之间转换。插件会在目标上存储原始 `d`（例如，要补间返回原始形状，可使用 `morphSVG: "#originalId"` 或同一元素）。

**提示：** 对于扭曲或翻转的变形，请设置 **shapeIndex**（使用 `"log"` 或 findShapeIndex()）。对于多区段路径，**shapeIndex** 是一个数组（每个区段对应一个值）。只有在首帧较慢时才进行预编译；它无法解决补间动画过程中的卡顿（必要时请简化 SVG 或减小尺寸）。

**了解更多：** [MorphSVG](https://gsap.com/docs/v3/Plugins/MorphSVGPlugin)

### MotionPath（MotionPathPlugin）

使元素沿 SVG 路径运动。适用于让对象沿路径（例如曲线或自定义路线）移动。

```javascript
gsap.registerPlugin(MotionPathPlugin);

gsap.to(".dot", {
  duration: 2,
  motionPath: { path: "#path", align: "#path", alignOrigin: [0.5, 0.5] }
});
```

**MotionPath——关键配置（motionPath 对象）：**

| 选项 | 说明 |
|--------|-------------|
| `path` | SVG 路径元素、选择器或路径数据字符串 |
| `align` | 用于对齐目标的路径元素或选择器 |
| `alignOrigin` | `[x, y]` 原点（0–1）；默认值为 `[0.5, 0.5]` |
| `autoRotate` | 旋转元素以跟随路径切线 |
| `curviness` | 0–2；路径平滑度 |

### MotionPathHelper

MotionPath 的可视化编辑器（对齐、偏移）。在开发过程中用于调整路径对齐方式。

```javascript
gsap.registerPlugin(MotionPathPlugin, MotionPathHelperPlugin);

const helper = MotionPathHelper.create(".dot", "#path", { end: 0.5 });
// adjust in UI, then use helper.path or helper.getProgress() in your animation
```

## 缓动

### CustomEase

自定义缓动曲线（三次贝塞尔曲线或 SVG 路径）。内置缓动不够用时使用。基本用法已在 gsap-core 中介绍；使用时进行注册：

```javascript
gsap.registerPlugin(CustomEase);
const ease = CustomEase.create("name", ".17,.67,.83,.67");
gsap.to(".el", { x: 100, ease: ease, duration: 1 });
```

### EasePack

添加更多具名缓动（例如 SlowMo、RoughEase、ExpoScaleEase）。注册后，在补间动画中使用相应的缓动名称。

### CustomWiggle

摆动/抖动缓动。当数值需要“摆动”（多次振荡）时使用。

### CustomBounce

可配置强度的弹跳式缓动。

## 物理效果

### Physics2D（Physics2DPlugin）

二维物理效果（速度、角度、重力）。适用于使用简单物理效果制作动画（例如抛射物、弹跳）。

```javascript
gsap.registerPlugin(Physics2DPlugin);

gsap.to(".ball", {
  duration: 2,
  physics2D: {
    velocity: 250,
    angle: 80,
    gravity: 500
  }
});
```

### PhysicsProps（PhysicsPropsPlugin）

将物理效果应用于属性值。适用于由物理效果驱动的属性动画。

```javascript
gsap.registerPlugin(PhysicsPropsPlugin);

gsap.to(".obj", {
  duration: 2,
  physicsProps: {
    x: { velocity: 100, end: 300 },
    y: { velocity: -50, acceleration: 200 }
  }
});
```

## 开发

### GSDevTools

用于拖动时间线、切换动画和调试的 UI。仅在开发期间使用；不要发布到生产环境。注册后，使用时间线引用创建实例。

```javascript
gsap.registerPlugin(GSDevTools);
GSDevTools.create({ animation: tl });
```

## 其他

### Pixi（PixiPlugin）

将 GSAP 与 PixiJS 集成，用于为 Pixi 显示对象制作动画。使用 GSAP 为 Pixi 对象制作动画时进行注册。

```javascript
gsap.registerPlugin(PixiPlugin);

const sprite = new PIXI.Sprite(texture);
gsap.to(sprite, { pixi: { x: 200, y: 100, scale: 1.5 }, duration: 1 });
```

## 最佳实践

- ✅ 在首次使用前，通过 **gsap.registerPlugin()** 注册使用的每个插件。
- ✅ 对布局过渡使用 **Flip.getState()** → DOM 更改 → **Flip.from()**；对带动量的拖拽使用 **Draggable** + **InertiaPlugin**。
- ✅ 在组件卸载或元素被移除时恢复插件实例（例如 `SplitTextInstance.revert()`）。

## 不要这样做

- ❌ 未先注册插件（**gsap.registerPlugin()**）便在补间动画或 API 中使用它。
- ❌ 将 GSDevTools 或仅供开发使用的插件发布到生产环境。

### 了解更多

https://gsap.com/docs/v3/Plugins/
