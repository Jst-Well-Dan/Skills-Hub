<!-- source-sha256: 71ed7794962fa6e803ee83030517b5b93a9f70fbfeb431ec4535c5480a8d8355 -->
---
name: vercel-react-best-practices
description: 来自 Vercel Engineering 的 React 和 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码时，应使用此技能以确保采用最佳性能模式。涉及 React 组件、Next.js 页面、数据获取、包体积优化或性能改进的任务会触发此技能。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React 最佳实践

由 Vercel 维护的 React 和 Next.js 应用程序综合性能优化指南。包含横跨 8 个类别的 70 条规则，并按影响程度确定优先级，以指导自动化重构和代码生成。

## 何时应用

在以下情况中参考这些指南：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 审查代码中的性能问题
- 重构现有 React/Next.js 代码
- 优化包体积或加载时间

## 按优先级排列的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 消除瀑布流 | 严重 | `async-` |
| 2 | 包体积优化 | 严重 | `bundle-` |
| 3 | 服务端性能 | 高 | `server-` |
| 4 | 客户端数据获取 | 中高 | `client-` |
| 5 | 重新渲染优化 | 中 | `rerender-` |
| 6 | 渲染性能 | 中 | `rendering-` |
| 7 | JavaScript 性能 | 中低 | `js-` |
| 8 | 高级模式 | 低 | `advanced-` |

## 快速参考

### 1. 消除瀑布流（严重）

- `async-cheap-condition-before-await` - 在等待标志或远程值之前，先检查低成本的同步条件
- `async-defer-await` - 将 await 移至实际使用它的分支中
- `async-parallel` - 对相互独立的操作使用 Promise.all()
- `async-dependencies` - 对部分依赖关系使用 better-all
- `async-api-routes` - 在 API 路由中尽早启动 Promise，尽晚 await
- `async-suspense-boundaries` - 使用 Suspense 流式传输内容

### 2. 包体积优化（严重）

- `bundle-barrel-imports` - 直接导入，避免使用桶文件
- `bundle-analyzable-paths` - 优先使用可静态分析的导入路径和文件系统路径，避免产生宽泛的包和追踪范围
- `bundle-dynamic-imports` - 对大型组件使用 next/dynamic
- `bundle-defer-third-party` - 在水合后加载分析和日志功能
- `bundle-conditional` - 仅在功能启用时加载模块
- `bundle-preload` - 在悬停或聚焦时预加载，以提升感知速度

### 3. 服务端性能（高）

- `server-auth-actions` - 像认证 API 路由一样认证服务器操作
- `server-cache-react` - 使用 React.cache() 进行单次请求内的去重
- `server-cache-lru` - 使用 LRU 缓存进行跨请求缓存
- `server-dedup-props` - 避免 RSC props 中的重复序列化
- `server-hoist-static-io` - 将静态 I/O（字体、徽标）提升至模块层级
- `server-no-shared-module-state` - 避免在 RSC/SSR 中使用模块级可变请求状态
- `server-serialization` - 尽量减少传递给客户端组件的数据
- `server-parallel-fetching` - 重构组件以并行执行数据获取
- `server-parallel-nested-fetching` - 在 Promise.all 中按项目串联嵌套数据获取
- `server-after-nonblocking` - 对非阻塞操作使用 after()

### 4. 客户端数据获取（中高）

- `client-swr-dedup` - 使用 SWR 自动进行请求去重
- `client-event-listeners` - 对全局事件监听器进行去重
- `client-passive-event-listeners` - 对滚动事件使用被动监听器
- `client-localstorage-schema` - 对 localStorage 数据进行版本管理并尽量精简

### 5. 重新渲染优化（中）

- `rerender-defer-reads` - 不要订阅仅在回调中使用的状态
- `rerender-memo` - 将高成本工作提取到记忆化组件中
- `rerender-memo-with-default-value` - 提升默认的非原始类型 props
- `rerender-dependencies` - 在 effect 中使用原始类型依赖项
- `rerender-derived-state` - 订阅派生布尔值，而不是原始值
- `rerender-derived-state-no-effect` - 在渲染期间派生状态，而不是在 effect 中派生
- `rerender-functional-setstate` - 使用函数式 setState 以获得稳定的回调
- `rerender-lazy-state-init` - 对高成本值向 useState 传入函数
- `rerender-simple-expression-in-memo` - 避免对简单原始值使用 memo
- `rerender-split-combined-hooks` - 拆分具有独立依赖项的 hooks
- `rerender-move-effect-to-event` - 将交互逻辑放入事件处理程序
- `rerender-transitions` - 对非紧急更新使用 startTransition
- `rerender-use-deferred-value` - 延迟高成本渲染以保持输入响应流畅
- `rerender-use-ref-transient-values` - 对频繁变化的瞬时值使用 refs
- `rerender-no-inline-components` - 不要在组件内部定义组件

### 6. 渲染性能（中）

- `rendering-animate-svg-wrapper` - 为 div 包装器添加动画，而不是 SVG 元素
- `rendering-content-visibility` - 对长列表使用 content-visibility
- `rendering-hoist-jsx` - 将静态 JSX 提取到组件外部
- `rendering-svg-precision` - 降低 SVG 坐标精度
- `rendering-hydration-no-flicker` - 对仅客户端数据使用内联脚本
- `rendering-hydration-suppress-warning` - 抑制预期的内容不匹配警告
- `rendering-activity` - 使用 Activity 组件进行显示和隐藏
- `rendering-conditional-render` - 条件渲染使用三元运算符，而不是 &&
- `rendering-usetransition-loading` - 加载状态优先使用 useTransition
- `rendering-resource-hints` - 使用 React DOM 资源提示进行预加载
- `rendering-script-defer-async` - 在 script 标签上使用 defer 或 async

### 7. JavaScript 性能（中低）

- `js-batch-dom-css` - 通过类或 cssText 批量处理 CSS 更改
- `js-index-maps` - 为重复查找构建 Map
- `js-cache-property-access` - 在循环中缓存对象属性
- `js-cache-function-results` - 在模块级 Map 中缓存函数结果
- `js-cache-storage` - 缓存 localStorage/sessionStorage 读取结果
- `js-combine-iterations` - 将多次 filter/map 合并为一个循环
- `js-length-check-first` - 在执行高成本比较前检查数组长度
- `js-early-exit` - 尽早从函数返回
- `js-hoist-regexp` - 将 RegExp 的创建提升到循环外部
- `js-min-max-loop` - 使用循环而不是排序来求最小值或最大值
- `js-set-map-lookups` - 使用 Set/Map 实现 O(1) 查找
- `js-tosorted-immutable` - 使用 toSorted() 保持不可变性
- `js-flatmap-filter` - 使用 flatMap 在一次遍历中完成映射和过滤
- `js-request-idle-callback` - 将非关键工作推迟到浏览器空闲时执行

### 8. 高级模式（低）

- `advanced-effect-event-deps` - 不要将 `useEffectEvent` 的结果放入 effect 依赖项
- `advanced-event-handler-refs` - 将事件处理程序存储在 refs 中
- `advanced-init-once` - 每次应用加载时仅初始化应用一次
- `advanced-use-latest` - 使用 useLatest 获取稳定的回调引用

## 使用方法

阅读各个规则文件以获取详细说明和代码示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每个规则文件包含：
- 关于该规则为何重要的简要说明
- 带有解释的错误代码示例
- 带有解释的正确代码示例
- 额外的上下文和参考资料

## 完整汇编文档

有关展开全部规则的完整指南，请参阅：`AGENTS.md`
