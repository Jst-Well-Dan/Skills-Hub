<!-- source-sha256: daad0a628cd1f5936050a8e65addf2e3512120de75c76a8358974a7f2e25991e -->
---
name: schedule-design
description: 使用 React 构建会议日程页面的设计模式与经验。涵盖主题系统、二维网格概览、筛选器 UX、粘性布局、模态框、收藏和数据规范化。适用于构建或修改日程视图、网格表格、筛选面板或会议 UI 组件。
---

# 日程设计模式

从构建 `/europe/schedule` 页面中总结的经验——这是一个单文件（约 2000 行）React 组件，包含二维房间×时间网格、一维场次列表、模态详情视图、多维筛选、收藏、主题和语义搜索。

## 架构

### 单文件组件非常适合日程页面

整个页面位于一个 `.tsx` 文件中。子组件（`TypeBadge`、`SpeakerPhoto`、`SessionModal`、`GridOverview`、`SessionCard`、`FilterPill`、`StarButton`）定义在同一文件中。这样可避免跨模块边界逐层传递 props，并保持日程组件自包含。仅当其他地方需要复用时，才将其拆分到单独文件中。

### 使用 `getStaticProps` 在构建时提取数据

原始 JSON（包含可为 null/可选的字段）在构建时被规范化为整洁的 `ScheduleSession` 对象，并确保字符串字段始终有值（使用空字符串，而不是 null）。这样便无需在整个渲染逻辑中执行 null 检查。

### 合成全体会议场次

全体会议/后勤安排场次（早餐、午餐、展览时间）以 `PLENARY_SESSIONS` 数组的形式硬编码，并在构建时与演讲者场次合并。它们使用 `id: 10000 + i` 以避免冲突。

## 主题系统

### 使用语义令牌对象，而不是 CSS 变量

定义一个包含约 40 个语义令牌（`bg`、`bgCard`、`text`、`textSecondary`、`border`、`accent`、`gridHeaderBg`、`starActive` 等）的 `Theme` 类型。创建 `DARK_THEME` 和 `LIGHT_THEME` 常量。向每个子组件传递 `t: Theme` 和 `isDark: boolean`。

### 跨页面持久化主题

使用共享键（`eu-theme`）将偏好存储在 `localStorage` 中。挂载时先检查 `localStorage`，然后回退到 `window.matchMedia('(prefers-color-scheme: light)')`。这样可在 `/europe` 和 `/europe/schedule` 之间同步主题。

### 全局样式也必须应用主题

Body 背景、滚动条颜色（`::webkit-scrollbar-*`）、文本选择样式（`::selection`）以及任何 `<style jsx global>` 块都必须引用主题令牌。不要忘记徽标图片——如果徽标是在透明背景上的白色图案，请在浅色模式下使用 `filter: invert(1)`。

## 二维网格概览（房间 × 时间）

### 网格使用 HTML `<table>`，而不是 CSS grid

真正的 `<table>` 配合 `<thead>`、`<tr>`、`<th>`、`<td>`，能够正确处理列对齐、粘性表头和水平滚动。CSS Grid 难以处理可滚动容器中的粘性列。

### 粘性表头和粘性首列

- 日期表头行：`position: sticky; top: 0; zIndex: 20`，并使用 `colSpan={rooms.length + 1}`，使其在水平滚动时横跨完整宽度。
- 房间表头行：`position: sticky; top: 30px`（按日期表头高度进行偏移）。
- 时间列：`position: sticky; left: 0; zIndex: 10`。
- 优先列（例如 Plenary）：`position: sticky; left: 48px`（按时间列宽度进行偏移），`zIndex: 10`。

### 全体会议列跨列显示

全体会议场次会横跨全天，因此 Plenary 列需要特殊逻辑：在每个时间段跟踪哪些全体会议场次处于“活动”状态（已开始且尚未结束），并以较低的不透明度和“继续”标签渲染仍在持续的场次。

### 房间排序顺序很重要

按以下顺序排列房间：Plenary 优先 → Keynote 房间 → 常规房间（按字母顺序）→ 特殊房间（例如 Leadership Lunch）→ Expo 房间。使用数字分组值进行排序。

### 网格单元格使用明亮的柔和色和深色文字

网格单元格使用独立的 `GRID_COLORS` 调色板，采用明亮的柔和背景色和深色文字——这与使用深色背景和浅色文字的徽章颜色不同。这样可以提高密集网格中的可读性。

### 单元格溢出

在网格单元格的内容 div 上设置 `maxHeight: 80` 和 `overflowY: 'auto'`，使内容密集的单元格可以滚动，而不是撑高整行。

### 点击网格单元格 → 模态框

点击网格单元格会打开 `SessionModal` 覆盖层（而不是行内展开）。模态框使用带背景模糊效果的 `position: fixed; inset: 0`，并可通过 ESC、点击背景或关闭按钮关闭。模态框打开时锁定 Body 滚动（`document.body.style.overflow = 'hidden'`）。

## 筛选系统

### 对类型分组，使筛选器更简洁

将细粒度类型映射为用户友好的分组。例如，通过 `TYPE_FILTER_GROUPS` 记录和 `typeFilterGroup()` 函数，将 `track_keynote`、`talk` 和 `lightning` 全部映射到单一的 `"talks"` 筛选分组。各个场次的徽章仍显示具体类型——只有筛选标签进行分组。

### 使用 `Set<string>` 实现包含式多选

每个筛选维度（日期、类型、主题）都使用一个 `Set<string>`。空集合 = 不筛选（显示全部）。使用 `toggleSet` 辅助函数以不可变方式添加/移除值。

### 筛选面板可折叠，但活动状态必须明显

当筛选面板折叠时：

1. “筛选器”按钮变为紫色/高亮，并显示计数徽章：`Filters (3) ▼`。
2. 表头下方的紧凑摘要栏显示活动筛选条件标签。
3. 表头中的场次数量（`92/214`）变为粗体并使用强调色。

如果缺少这些提示，用户不会意识到筛选器处于活动状态——这是一个实际出现过的可用性问题。

### 筛选器布局：带标签的分组行

每个筛选维度独占一行，并带有大写标签（`DAY`、`TYPE`、`TRACK`）。底部单独一行包含“已收藏”、“清除所有筛选器”和数量摘要。这比将不同类型的筛选标签混放在一个行内布局中清晰得多。

### 使用 localStorage 存储已收藏项目

使用 `localStorage` 键 `aie-schedule-favorites` 存储由场次 ID 组成的 JSON 数组。将其封装在返回 `{ favorites, toggleFavorite, isFavorited }` 的 `useFavorites` hook 中。已收藏项目在网格中使用金色边框/光晕：`boxShadow: '0 0 8px rgba(250,204,21,0.5)'`。

## 场次展示

### 先显示标题，再显示演讲者署名

网格单元格和卡片先显示场次标题，再在下方显示演讲者信息。演讲者署名格式为：`{name} - {company}, {role}`，并提供合理的回退处理——如果缺少 company 或 role，则省略相应的短横线/逗号部分。

### 检测待定演讲者

使用正则表达式 `/^tbd\b/i` 检测占位演讲者姓名，并以较低的不透明度渲染。

### 演讲者照片及首字母回退

`SpeakerPhoto` 组件尝试加载图片，加载失败时回退为带有姓名首字母（从姓名中提取）的圆形徽章。图片使用 `loading="lazy"`。

## URL 状态

### 模态框状态同步到 URL 查询参数

打开模态框时，通过浅层路由替换设置 `?session=<id>`。挂载时检查 `router.query.session` 以恢复模态框。这样可以分享场次链接。

## 语义搜索

### 带请求 ID 防护的防抖 API 调用

每次按键都会递增 `semanticRequestIdRef`。仅应用 ID 与最新 ref 匹配的响应——过时或乱序的响应会被静默丢弃。使用 `AbortController` 进行清理。防抖延迟：400ms。

## 常见陷阱

1. **`next lint` 在 Next.js 16 中不可用**——改用 `npx tsc --noEmit`。
2. **表格中的粘性 `position`**：在 `<td>` 上使用 `position: sticky` 时必须显式设置 `background`——否则滚动时透明单元格会显示其下方的内容。
3. **日期表头上的 `colSpan`**：如果没有正确设置 `colSpan` 以横跨所有列，水平滚动时日期表头将无法延伸至完整宽度。
4. **全体会议对比度**：深色配深色或浅色配浅色的全体会议徽章很容易被忽略。请在两套调色板中为全体会议场次提供独特的高对比度颜色。
5. **密集网格单元格中的行高**：对于网格单元格中的 9-10px 文字，默认行高过于宽松。使用 `lineHeight: 1.15`。
6. **房间名称拼写错误**：始终根据源数据验证房间名称（例如 `"Westley"` 与 `"Wesley"`）。在 JSON 源文件中批量重命名，比在渲染代码中修补更安全。
7. **用户看不到筛选状态**：最常见的 UX 抱怨是“我不知道为什么看到的场次变少了”。即使筛选面板已折叠，也始终要让活动筛选状态保持可见。
