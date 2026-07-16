<!-- source-sha256: 06f7a583bb6fb0738d0b8ab97cd356a09851ed0d9b6462c1b3ab355b83f7ee29 -->
---
name: testing-schedule-preview
description: 用于测试 AI Engineer Europe 内部 Bun 日程预览或公开日程页面，包括工具提示、模态框、CFP 元数据和本地预览工作流。
---

# 测试 Europe 日程

## 概述
需要测试两种日程视图：
1. **Bun 预览**，地址为 `http://127.0.0.1:1234/_deploy/` — 包含 CFP 数据、会话 ID 和联系信息的内部工具
2. **公开日程页面**，地址为 `/europe/schedule` — 面向公众，包含网格概览和会话列表

## Bun 预览（内部）

### 启动服务器
```bash
cd /path/to/aiecode2025
pnpm europe:source:preview
```
此命令会在 `src/pages/europe/source/` 中运行 `bun run bun-preview.mjs`。

如果端口 1234 已被占用，请先终止现有进程：
```bash
fuser -k 1234/tcp
```
注意：`lsof` 可能不可用，请改用 `fuser`。

### 关键文件
- `src/pages/europe/source/_deploy/index.html` — 预览 HTML
- `src/pages/europe/source/schedule.json` — 数据源
- `src/pages/europe/source/photos/` — 演讲者照片

### 测试内容
- 悬停工具提示会在光标附近显示演讲者摘要
- 点击展开的模态框会显示完整详情（CFP 数据、会话 ID、联系方式）
- 关闭模态框：按 ESC 键、点击背景遮罩、点击关闭按钮
- 模态框打开时工具提示会隐藏（遮罩层后方不会残留幽灵工具提示）
- CFP 标签颜色在工具提示和模态框中均能正确渲染

## 公开日程页面

### 访问方式
- 本地：`http://localhost:3000/europe/schedule`（需要 Next.js 开发服务器）
- Vercel 预览：PR 会在 `https://aiecode2025-git-{branch}-aieng.vercel.app/europe/schedule` 获得部署

### 关键文件
- `src/pages/europe/schedule.tsx` — 包含网格概览、会话卡片、模态框和筛选器的 React 组件

### 页面结构
1. **页眉**，包含搜索、语义搜索开关、筛选器、全部展开/全部折叠按钮
2. **会议室 x 时间概览网格** — 日期标签页（4 月 8/9/10 日），会议室作为列，时间段作为行
3. **会话列表** — 按日期分组的可展开卡片

### 测试内容
- 网格单元格可点击 — 点击后会打开居中的模态遮罩层
- 模态框显示：类型徽章、标题、时间/会议室/专题、演讲者照片 + 姓名 + 职位 + 公司 + 社交链接、完整摘要
- 关闭模态框：按 ESC 键、点击背景遮罩、点击 ESC 按钮
- 模态框中的社交链接会在新标签页中打开，且不会关闭模态框
- 交叉核对：模态框内容应与下方列表视图中展开的 SessionCard 一致
- 网格中的日期标签页切换正常
- 搜索功能会筛选会话列表
- Expand All / Collapse All 按钮正常工作

### 测试方法
1. 打开日程页面
2. 切换到 4 月 9 日或 10 日，查看网格中的分会场演讲
3. 点击一个演讲单元格 — 验证模态框内容
4. 测试全部 3 种关闭方式
5. 搜索同一演讲标题 — 在列表视图中找到它
6. 展开该项，并将其内容与模态框中显示的内容进行比较

## 环节类型
- **主题演讲**：大多为受邀演讲者，CFP 数据较少，带有 INVITED 徽章
- **分会场演讲**：受邀演讲者与 CFP 演讲者混合，可能包含描述
- **展区环节**：由公司赞助，通常位于三个会议室之一
- **研讨会**：全部安排在 4 月 8 日，部分有多位演讲者，时间段较长
- **专题主题演讲**：各专题的开场演讲

## 所需的 Devin 密钥
无需密钥 — Bun 预览和公开日程均不需要身份验证。
