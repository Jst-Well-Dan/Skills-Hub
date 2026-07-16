<!-- source-sha256: e38e0eaa609316b10423a9a138ed95e35099accd3f735585295c8a8f165c28a3 -->
---
name: vercel-composition-patterns
description:
  可扩展的 React 组合模式。适用于重构存在大量布尔属性的组件、
  构建灵活的组件库或设计可复用 API。由涉及复合组件、
  渲染属性、上下文提供者或组件架构的任务触发。包含 React 19
  API 变更。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React 组合模式

用于构建灵活、可维护的 React 组件的组合模式。通过使用复合组件、提升状态和
组合内部实现，避免布尔属性泛滥。这些模式让代码库在扩展时更易于人类和 AI
智能体使用。

## 何时应用

在以下情况下参考这些指南：

- 重构具有大量布尔属性的组件
- 构建可复用的组件库
- 设计灵活的组件 API
- 审查组件架构
- 使用复合组件或上下文提供者

## 按优先级划分的规则类别

| 优先级 | 类别       | 影响 | 前缀            |
| ------ | ---------- | ---- | --------------- |
| 1      | 组件架构   | 高   | `architecture-` |
| 2      | 状态管理   | 中   | `state-`        |
| 3      | 实现模式   | 中   | `patterns-`     |
| 4      | React 19 API | 中 | `react19-`      |

## 快速参考

### 1. 组件架构（高）

- `architecture-avoid-boolean-props` - 不要添加布尔属性来自定义
  行为；请使用组合
- `architecture-compound-components` - 使用共享上下文组织复杂
  组件

### 2. 状态管理（中）

- `state-decouple-implementation` - 提供者是唯一知道状态如何
  管理的地方
- `state-context-interface` - 定义包含状态、操作和元数据的通用接口，
  以实现依赖注入
- `state-lift-state` - 将状态移入提供者组件，使兄弟组件能够访问

### 3. 实现模式（中）

- `patterns-explicit-variants` - 创建显式的变体组件，而不是使用
  布尔模式
- `patterns-children-over-render-props` - 使用 children 进行组合，而
  不是使用 renderX 属性

### 4. React 19 API（中）

> **⚠️ 仅适用于 React 19+。** 如果使用 React 18 或更早版本，请跳过此部分。

- `react19-no-forwardref` - 不要使用 `forwardRef`；使用 `use()` 代替 `useContext()`

## 如何使用

阅读各个规则文件，了解详细说明和代码示例：

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

每个规则文件包含：

- 关于其重要性的简要说明
- 带有说明的错误代码示例
- 带有说明的正确代码示例
- 其他上下文和参考资料

## 完整汇编文档

包含所有规则完整展开内容的完整指南：`AGENTS.md`
