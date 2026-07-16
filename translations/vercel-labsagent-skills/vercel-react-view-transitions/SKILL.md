<!-- source-sha256: 8c4c0f8b5581ef473fbf388b2df7d13e02d418ab2150a912b9b7eafdf4b76a01 -->
---
name: vercel-react-view-transitions
description: 使用 React 的视图过渡 API（`<ViewTransition>` 组件、`addTransitionType` 和 CSS 视图过渡伪元素）实现流畅、具有原生体验的动画指南。当用户希望添加页面过渡、为路由变化添加动画、创建共享元素动画、为组件的进入/退出添加动画、为列表重新排序添加动画、实现带方向的（前进/后退）导航动画，或在 Next.js 中集成视图过渡时，请使用此技能。当用户提到视图过渡、`startViewTransition`、`ViewTransition`、过渡类型，或询问如何在不使用第三方动画库的情况下为 React UI 状态之间的变化添加动画时，也应使用此技能。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# React 视图过渡

使用浏览器原生的 `document.startViewTransition` 为 UI 状态之间的变化添加动画。使用 `<ViewTransition>` 声明动画作用于“什么”，使用 `startTransition` / `useDeferredValue` / `Suspense` 触发动画发生的“时机”，使用 CSS 类控制动画“如何”呈现。不支持的浏览器会平稳跳过动画。

## 何时使用动画

每个 `<ViewTransition>` 都应该传达一种空间关系或连续性。如果你无法明确说明它传达了什么，就不要添加它。

按照以下顺序实现列表中所有适用的模式：

| 优先级 | 模式 | 它传达的含义 |
|----------|---------|---------------------|
| 1 | **共享元素**（`name`） | “同一个事物——正在深入查看” |
| 2 | **Suspense 显示** | “数据已加载” |
| 3 | **列表身份**（每个项目的 `key`） | “相同的项目，新的排列方式” |
| 4 | **状态变化**（`enter`/`exit`） | “某个内容出现了/消失了” |
| 5 | **路由变化**（布局层级） | “正在前往一个新位置” |

这是实现顺序，而不是一个“任选其一”的列表。实现所有适合该应用的模式。仅当应用中没有相应使用场景时，才跳过某种模式。

### 选择动画样式

| 上下文 | 动画 | 原因 |
|---------|-----------|-----|
| 层级导航（列表 → 详情） | 按类型指定的 `nav-forward` / `nav-back` | 传达空间深度 |
| 横向导航（标签页之间） | 不带属性的 `<ViewTransition>`（淡入淡出）或 `default="none"` | 没有需要传达的深度 |
| Suspense 显示 | `enter`/`exit` 字符串属性 | 内容正在到达 |
| 重新验证／后台刷新 | `default="none"` | 静默进行——无需动画 |

仅将方向滑动用于层级导航（列表 → 详情）和有序序列（上一张/下一张照片、轮播图、分页结果）。对于有序序列，方向用于传达位置：“下一个”从右侧滑入，“上一个”从左侧滑入。横向／无序导航（标签页之间）不应使用方向滑动——这会错误地暗示空间深度。

---

## 可用性

- **Next.js：**不要安装 `react@canary`——App Router 已在内部捆绑 React canary。`ViewTransition` 可以开箱即用。`npm ls react` 可能显示一个看似稳定版的版本；这是预期行为。
- **不使用 Next.js：**安装 `react@canary react-dom@canary`（稳定版 React 尚未包含 `ViewTransition`）。
- 浏览器支持：Chromium 111+、Firefox 144+、Safari 18.2+。在不支持的浏览器中会平稳降级。

---

## 实现工作流

向现有应用添加视图过渡时，**请逐步遵循 `references/implementation.md`。**从审查开始——不要跳过。将 `references/css-recipes.md` 中的 CSS 配方复制到全局样式表中——不要自行编写动画 CSS。

---

## 核心概念

### `<ViewTransition>` 组件

```jsx
import { ViewTransition } from 'react';

<ViewTransition>
  <Component />
</ViewTransition>
```

React 会自动分配唯一的 `view-transition-name`，并在幕后调用 `document.startViewTransition`。切勿自行调用 `startViewTransition`。

### 动画触发器

| 触发器 | 触发时机 |
|---------|--------------|
| **enter** | `<ViewTransition>` 首次在某个 Transition 期间插入时 |
| **exit** | `<ViewTransition>` 首次在某个 Transition 期间移除时 |
| **update** | `<ViewTransition>` 内部发生 DOM 变更时。存在嵌套 VT 时，变更应用于最内层的 VT |
| **share** | 具名 VT 卸载，同时另一个具有相同 `name` 的 VT 在同一个 Transition 中挂载时 |

只有 `startTransition`、`useDeferredValue` 或 `Suspense` 会激活 VT。常规 `setState` 不会产生动画。

### 关键放置规则

只有当 `<ViewTransition>` 出现在**任何 DOM 节点之前**时，才会激活进入/退出动画：

```jsx
// Works
<ViewTransition enter="auto" exit="auto">
  <div>Content</div>
</ViewTransition>

// Broken — div wraps the VT, suppressing enter/exit
<div>
  <ViewTransition enter="auto" exit="auto">
    <div>Content</div>
  </ViewTransition>
</div>
```

---

## 使用视图过渡类设置样式

### 属性

可用值：`"auto"`（浏览器交叉淡化）、`"none"`（禁用）、`"class-name"`（自定义 CSS），或用于特定类型动画的 `{ [type]: value }`。

```jsx
<ViewTransition default="none" enter="slide-in" exit="slide-out" share="morph" />
```

如果 `default` 为 `"none"`，除非显式列出，否则所有触发器都会关闭。

### CSS 伪元素

- `::view-transition-old(.class)`——离场快照
- `::view-transition-new(.class)`——入场快照
- `::view-transition-group(.class)`——容器
- `::view-transition-image-pair(.class)`——旧快照与新快照组成的配对

可直接使用的动画配方请参阅 `references/css-recipes.md`。

---

## 过渡类型

使用 `addTransitionType` 为过渡添加标签，使 VT 能根据上下文选择不同的动画。可以多次调用它以叠加类型——树中的不同 VT 会响应不同类型：

```jsx
startTransition(() => {
  addTransitionType('nav-forward');
  addTransitionType('select-item');
  router.push('/detail/1');
});
```

传入一个对象，将类型映射到 CSS 类。适用于 `enter`、`exit`，**以及** `share`：

```jsx
<ViewTransition
  enter={{ 'nav-forward': 'slide-from-right', 'nav-back': 'slide-from-left', default: 'none' }}
  exit={{ 'nav-forward': 'slide-to-left', 'nav-back': 'slide-to-right', default: 'none' }}
  share={{ 'nav-forward': 'morph-forward', 'nav-back': 'morph-back', default: 'morph' }}
  default="none"
>
  <Page />
</ViewTransition>
```

`enter` 和 `exit` 不必对称。例如，可以淡入，但根据方向滑出：

```jsx
<ViewTransition
  enter={{ 'nav-forward': 'fade-in', 'nav-back': 'fade-in', default: 'none' }}
  exit={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
  default="none"
>
```

**TypeScript：**`ViewTransitionClassPerType` 要求对象中必须包含 `default` 键。

对于具有多个页面的应用，将按类型指定的 VT 提取为可复用的包装器：

```jsx
export function DirectionalTransition({ children }: { children: React.ReactNode }) {
  return (
    <ViewTransition
      enter={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
      exit={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
      default="none"
    >
      {children}
    </ViewTransition>
  );
}
```

### `router.back()` 和浏览器后退按钮

`router.back()` 以及浏览器的后退/前进按钮**不会**触发视图过渡（`popstate` 是同步的，与 `startViewTransition` 不兼容）。请改用带有明确 URL 的 `router.push()`。

### 类型与 Suspense

类型在导航期间可用，但在后续的 Suspense 显示期间**不可用**（这是独立的过渡，没有类型）。页面级进入/退出应使用类型映射；Suspense 显示应使用简单的字符串属性。

---

## 共享元素过渡

两个 VT 使用相同的 `name`——一个正在卸载，另一个正在挂载——会创建共享元素变形动画：

```jsx
<ViewTransition name="hero-image">
  <img src="/thumb.jpg" onClick={() => startTransition(() => onSelect())} />
</ViewTransition>

// On the other view — same name
<ViewTransition name="hero-image">
  <img src="/full.jpg" />
</ViewTransition>
```

- 同一时间只能挂载一个具有特定 `name` 的 VT——请使用唯一名称（`photo-${id}`）。注意可复用组件：如果带有具名 VT 的组件同时渲染在模态框／弹出框和页面中，两者会同时挂载并破坏变形动画。可以通过属性使名称成为条件值，或将具名 VT 从共享组件移到具体使用方中。
- `share` 的优先级高于 `enter`/`exit`。仔细考虑每条导航路径：当无法形成匹配配对时（例如目标页面没有相同的名称），会改为触发 `enter`/`exit`。请考虑该元素在这些路径中是否需要后备动画。
- 在包含共享变形动画的页面上，切勿使用淡出退出动画——应改用方向滑动。

---

## 常见模式

### 进入/退出

```jsx
{show && (
  <ViewTransition enter="fade-in" exit="fade-out"><Panel /></ViewTransition>
)}
```

### 列表重新排序

```jsx
{items.map(item => (
  <ViewTransition key={item.id}><ItemCard item={item} /></ViewTransition>
))}
```

在 `startTransition` 内部触发。避免在列表与 VT 之间添加包装用的 `<div>`。

### 组合共享元素与列表身份

共享元素和列表身份是相互独立的关注点——不要将二者混为一谈。当列表项包含共享元素时（例如一张会变形为详情视图的图片），请使用两个嵌套的 `<ViewTransition>` 边界：

```jsx
{items.map(item => (
  <ViewTransition key={item.id}>                                      {/* list identity */}
    <Link href={`/items/${item.id}`}>
      <ViewTransition name={`item-image-${item.id}`} share="morph">   {/* shared element */}
        <Image src={item.image} />
      </ViewTransition>
      <p>{item.name}</p>
    </Link>
  </ViewTransition>
))}
```

外层 VT 处理列表重新排序／进入动画。内层 VT 处理跨路由的共享元素变形。缺少任意一层，都意味着对应动画会静默地不发生。

### 使用 `key` 强制重新进入

```jsx
<ViewTransition key={searchParams.toString()} enter="slide-up" default="none">
  <ResultsGrid />
</ViewTransition>
```

**注意：**如果包装的是 `<Suspense>`，更改 `key` 会重新挂载该边界并重新获取数据。

### 从 Suspense 后备内容过渡到实际内容

简单交叉淡化：
```jsx
<ViewTransition>
  <Suspense fallback={<Skeleton />}><Content /></Suspense>
</ViewTransition>
```

方向显示：
```jsx
<Suspense fallback={<ViewTransition exit="slide-down"><Skeleton /></ViewTransition>}>
  <ViewTransition enter="slide-up" default="none"><Content /></ViewTransition>
</Suspense>
```

更多模式请参阅 `references/patterns.md`。

---

## 多个 VT 如何交互

所有匹配触发器的 VT 都会在一次 `document.startViewTransition` 中同时触发。处于**不同**过渡中的 VT（导航与稍后完成的 Suspense）不会相互竞争。

### 积极使用 `default="none"`

如果不使用它，每个 VT 都会在**每次**过渡时触发浏览器交叉淡化——包括 Suspense 完成、`useDeferredValue` 更新和后台重新验证。始终使用 `default="none"`，并仅显式启用所需的触发器。

### 两种模式共存

**模式 A——方向滑动：**每个页面上的按类型指定 VT，在导航期间触发。
**模式 B——Suspense 显示：**使用简单字符串属性，在数据加载完成时触发（无类型）。

它们可以共存，因为它们在不同时间触发。两者都设置 `default="none"` 可防止相互干扰。始终将 `enter` 与 `exit` 配对使用。将方向 VT 放在页面组件中，而不是布局中。

### 嵌套 VT 的限制

当父级 VT 退出时，其中的嵌套 VT **不会**触发自身的进入/退出动画——只有最外层 VT 会执行动画。目前无法在页面导航期间实现逐项交错动画。实验性的选择性启用修复方案请参阅 [react#36135](https://github.com/facebook/react/pull/36135)。

---

## Next.js 集成

有关 Next.js 设置（`experimental.viewTransition` 标志、`next/link` 上的 `transitionTypes` 属性、App Router 模式、服务器组件），请参阅 `references/nextjs.md`。

---

## 无障碍

始终将 `references/css-recipes.md` 中的减少动态效果 CSS 添加到全局样式表。

---

## 参考文件

- **`references/implementation.md`**——逐步实现工作流。
- **`references/patterns.md`**——模式、动画时序、事件 API、故障排除。
- **`references/css-recipes.md`**——可直接使用的 CSS 动画配方。
- **`references/nextjs.md`**——Next.js App Router 模式和服务器组件详细信息。

## 完整汇编文档

包含所有已展开参考文件的完整指南：`AGENTS.md`
