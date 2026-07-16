<!-- source-sha256: 81c5002c6643b0de7b8710b00e7a9038daa6fb9b68d59870ee6adb12da8d10f8 -->
---
name: web-artifacts-builder
description: 使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建精美、多组件 claude.ai HTML 工件的工具套件。适用于需要状态管理、路由或 shadcn/ui 组件的复杂工件，不适用于简单的单文件 HTML/JSX 工件。
license: 完整条款见 LICENSE.txt
---

# Web 工件构建器

要构建功能强大的前端 claude.ai 工件，请遵循以下步骤：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码来开发工件
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包到单个 HTML 文件中
4. 向用户展示工件
5. （可选）测试工件

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包）+ Tailwind CSS + shadcn/ui

## 设计与样式指南

非常重要：为避免通常所说的“AI 粗制滥造感”，请避免过度使用居中布局、紫色渐变、千篇一律的圆角和 Inter 字体。

## 快速开始

### 第 1 步：初始化项目

运行初始化脚本以创建新的 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这将创建一个配置齐全的项目，其中包括：
- ✅ React + TypeScript（通过 Vite）
- ✅ Tailwind CSS 3.4.1，以及 shadcn/ui 主题系统
- ✅ 已配置路径别名（`@/`）
- ✅ 预安装 40 多个 shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖项
- ✅ 已配置 Parcel 以进行打包（通过 .parcelrc）
- ✅ 兼容 Node 18+（自动检测并固定 Vite 版本）

### 第 2 步：开发工件

要构建工件，请编辑生成的文件。有关指导，请参阅下方的**常见开发任务**。

### 第 3 步：打包为单个 HTML 文件

要将 React 应用打包为单个 HTML 工件：
```bash
bash scripts/bundle-artifact.sh
```

这将创建 `bundle.html`——一个自包含的工件，其中内联了所有 JavaScript、CSS 和依赖项。此文件可以直接在 Claude 对话中作为工件分享。

**要求**：项目的根目录中必须包含 `index.html`。

**脚本执行的操作**：
- 安装打包依赖项（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建支持路径别名的 `.parcelrc` 配置
- 使用 Parcel 构建（不生成源映射）
- 使用 html-inline 将所有资源内联到单个 HTML 中

### 第 4 步：与用户分享工件

最后，在与用户的对话中分享打包后的 HTML 文件，以便他们将其作为工件查看。

### 第 5 步：测试/可视化工件（可选）

注意：这是一个完全可选的步骤。仅在必要或用户要求时执行。

要测试或可视化工件，请使用可用工具（包括其他技能或 Playwright、Puppeteer 等内置工具）。通常应避免预先测试工件，因为这会延长从提出请求到看到成品工件之间的等待时间。如有需要，可在展示工件后再进行测试，或者在出现问题时进行测试。

## 参考资料

- **shadcn/ui 组件**：https://ui.shadcn.com/docs/components
