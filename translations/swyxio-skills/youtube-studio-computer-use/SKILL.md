<!-- source-sha256: cd94f0d9c09391dab25cf98689cbef8b0945d9aa1402eb412ff7014fdb3ba585 -->
---
name: youtube-studio-computer-use
description: 当 API 访问不可用、功能不足，或对于仅限 Studio 的编辑操作速度较慢时，通过 Chrome 和 Computer Use 自动操作 YouTube Studio。适用于浏览器驱动的 YouTube Studio 工作，例如编辑现有视频、添加自定义缩略图、更改可见性、安排发布时间、选择播放列表、保存和验证 Studio 状态、从按钮禁用状态中恢复，以及协调 DOM 注入与 Computer Use 点击。当稳定的 API 凭据或批量上传工作流可用时，对于纯上传、下载或元数据准备任务，优先使用 API 或 youtube-studio-batch-upload skill。
---

# YouTube Studio Computer Use

## 使用此 Skill

当任务必须在 Chrome 中操作实时 YouTube Studio UI 时，请使用此 skill：

- 为现有视频添加或替换缩略图。
- 通过 Studio 可见性控件安排或重新安排视频发布时间。
- 在缺少 API 配置时，修复元数据、播放列表、观众、可见性或保存状态。
- 使用台账和恢复列表批量执行一系列 Studio 编辑页面操作。
- 针对脆弱的 UI 状态，将 DOM 注入与 Computer Use 结合使用。

当主要工作是下载源视频、整理文件名、构建元数据、上传新视频或维护上传台账时，请改用 `youtube-studio-batch-upload`。如果 OAuth/API 凭据已经存在且相关操作能够由 API 完整支持，则使用官方 YouTube API 流程，尤其是批量读取或写入元数据时。此 skill 用于处理混乱的浏览器操作路径。

## 基本规则

- 每轮执行直接 UI 操作前，调用 `mcp__computer_use.get_app_state`。
- 将 Chrome 标签页视为与用户共享。注入 JS 前，明确定位或激活目标 YouTube Studio 标签页；用户浏览过其他页面后，不要依赖“前台窗口的活动标签页”。
- 维护本地 JSON/CSV 状态台账，其中包含 `video_id`、标题、操作、目标时间、缩略图路径、`ok`、错误和验证文本。
- 转到下一个视频前先保存当前视频。验证 `All changes saved` 以及预期的侧边栏状态，例如 `Visibility Scheduled`。
- 如果用户也在使用 Chrome，应假定焦点可能发生移动。中断后重新查询应用状态，并重新定位 Studio 标签页。
- 更改元数据时，不要发布私有或内部的源 URL 或备注。

## 浏览器自动化模式

使用 Computer Use 锚定会话，并使用 DOM JS 执行重复的页面操作：

1. 打开或选择 YouTube Studio 编辑页面：`https://studio.youtube.com/video/<video_id>/edit`。
2. 等待编辑页面完全渲染。必须检测到正文文本、需要时出现缩略图或输入区域，以及 `Edit video visibility status` 控件。
3. 通过 Chrome AppleScript 或浏览器工具运行小型 JS 代码片段。对于异步浏览器操作，在页面内启动异步任务，将结果存储到 `window.__codex...`，然后轮询该结果。AppleScript 无法可靠地等待 Promise。
4. 对于 DOM JS 无法访问的原生弹窗、文件选择器和 UI 状态，使用 Computer Use 点击。
5. 保存、等待、验证并追加到台账，然后再继续。

有关详细代码片段和已知故障模式，请阅读 `references/studio-dom-patterns.md`。

## 缩略图

可靠地替换缩略图需要使用 Studio 隐藏的文件输入框：

- 将缩略图区域滚动到视野中，并等待 `input[type=file]#file-loader`。
- 除非准备处理原生文件选择器，否则不要点击上传按钮。
- 一种稳健的 DOM 路径是通过小型 localhost 服务器提供本地缩略图文件，在页面中使用 `fetch` 获取它、创建 `File`、通过 `DataTransfer` 设置 `input.files`，然后依次触发 `input` 和 `change`。
- 注入后，等待缩略图控件不再显示 `Uploading...`。较大或加载较慢的图片可能需要轮询 60 秒。

如果 Studio 显示了新缩略图，但状态对象仍显示 pending，请在重试前检查页面；重试可能只会无害地再次替换同一张缩略图，但在 Studio 完成上传前不要保存。

## 发布时间安排

安排发布时间很脆弱，因为 YouTube Studio 验证的是隐藏组件状态，而不只是输入文本。

- 使用 `Edit video visibility status` 控件打开可见性弹窗。
- 选择 `Schedule`，然后设置日期和时间。
- 对于日期，打开日期选择器并点击可见日期，比直接赋值文本更可靠。
- 对于时间，点击时间字段并选择可见的列表框选项，例如 `8:30 AM`。仅设置 `input.value = "8:30 AM"` 可能会显示正确的值，但仍使 `Done` 保持禁用。
- 点击 `Done` 前，确认它已启用。
- 点击页面级的 `Save`，然后等待出现 `All changes saved`，并确认侧边栏显示 `Visibility Scheduled`。

对于间隔发布，请按照 YouTube 本地时区生成时间段，例如从 `9:30 AM` 开始，每个视频增加 30 分钟。在台账中记录每个已分配的时间。

## 恢复

常见恢复方式：

- `missing file input`：缩略图区域尚未渲染。滚动到 Thumbnail，然后再次等待。
- 缩略图结果为 `pending`：页面内异步任务未能在轮询窗口内完成。延长轮询时间，使用多线程本地服务器，并检查 Studio 是否已经在上传缩略图。
- 设置时间后 `Done` 仍处于禁用状态：从下拉列表框中选择时间；不要仅输入或赋值。
- `missing schedule`：可见性弹窗未打开或仍处于折叠状态。重新打开可见性控件，并检查可见的弹窗文本。
- JS 在错误页面上运行：明确重新定位 Studio 标签页，并再次运行 `get_app_state`。

批量操作中绝不要强行跳过失败。停止操作、修补驱动程序，然后根据台账从下一个可用发布时间段继续。
