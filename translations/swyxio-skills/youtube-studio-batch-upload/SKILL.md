<!-- source-sha256: 4f1da7f8adbdfbed7b55a853916cc35ed6bc0e008c11e4203b77074b6f5a3721 -->
---
name: youtube-studio-batch-upload
description: 用于批量上传来自 Airtable、Google Drive、Loom、YouTube 或本地文件的视频至 YouTube Studio 的工作流。当 Codex 需要下载大量已提交的视频、整理文件名、根据表格字段生成 YouTube 标题和描述、通过 Chrome/Computer Use 上传、将视频设为“不公开”、添加播放列表、在继续处理下一个视频前保存每次上传、跟踪链接，以及报告不完整或受阻的来源行时使用。
---

# YouTube Studio 批量上传

## 操作规则

- 使用 browser/computer-use skill 处理实时 YouTube Studio 或 Airtable UI 操作。每轮在执行直接 UI 操作前调用 `get_app_state`。
- 将上传视为批量瀑布式流程：下载/恢复来源、整理文件名、准备元数据、上传、逐个设置视频标题/播放列表/可见性并保存、验证、登记台账。
- 不要在 YouTube 描述中包含源视频 URL。除非用户明确要求发布这些链接，否则从最终描述中移除 Drive、Loom、WeTransfer 和源 YouTube 链接。
- 默认在描述中使用提交的完整演讲摘要；除非用户要求简短文案，否则不要将其压缩成预告。
- 不要发布 Airtable 内部字段，例如 `Additional Notes`、审核者备注、来源状态或操作评论，除非用户明确将其标记为公开文案。
- 在进入可见性设置前，始终选择目标播放列表。
- 在打开或编辑下一个上传项前，始终选择 `Unlisted` 并点击 `Save`。
- 如果 YouTube 因 SD 处理尚未完成而阻止保存，请停留在模态框中等待，并在处理完成后保存。不要假定草稿已经发布。
- 在 UI 允许的情况下，优先批量选择文件。如果选择器控件失效，则改为上传较小批次或逐个上传文件，但下载和元数据准备仍应保持批量处理。
- 为 `waitlisted`、`WIP`、`To provide`、私有/已删除链接或拒绝访问的 Drive 文件等行保留清晰的受阻列表。

## 工作流

1. 将源表格导出或抓取为 CSV/TSV，至少包含：演讲者姓名、演讲标题、演讲描述、视频源 URL、个人简介、公司、账号、LinkedIn/GitHub 以及所有公开链接。除非另有说明，否则将备注/状态字段视为私有信息。
2. 构建清单和元数据 JSON：
   - 运行 `scripts/youtube_batch_helper.py build-metadata presenters.csv --out work/youtube_metadata.json`。
   - 除非用户另有要求，否则使用 `--playlist "Playlist Name"` 和 `--skip-source-url`。
   - 下载前检查受阻行以及来源值为占位符的行。
3. 将源视频下载到 `downloads/.../raw`：
   - Drive：优先使用 `yt-dlp`；如果权限要求 Chrome cookie/会话，则使用经过浏览器身份验证的直接下载。
   - Loom：尝试使用 `yt-dlp`；如果失败，则检查页面中的签名 HLS 清单，并使用 `ffmpeg` 合并。
   - YouTube 源视频：尝试将 `yt-dlp` 与浏览器 cookie 或其他播放器客户端配合使用。遵守访问权限和版权限制。
4. 在批次目录下整理待上传文件，并使用最终的人类可读名称：
   - `Talk Title - Speaker Name.mp4`
   - 保留 YouTube 接受的标点符号；避免使用与文件系统不兼容的字符。
5. 在 Chrome 中打开 YouTube Studio 上传页面，选择尽可能多的已整理文件，然后完成每个上传对话框：
   - 根据元数据设置标题和描述。
   - 选择播放列表。
   - 依次完成视频元素和检查步骤。
   - 选择 `Unlisted`。
   - 保存并等待，直到该行显示为 `Unlisted / None` 或已知限制。
6. 在台账中记录每个 YouTube 链接并报告：
   - 已上传数量和新链接。
   - 所有限制，尤其是版权限制。
   - 受阻/不可用的来源行及确切原因。

## 元数据格式

除非用户提供频道专用模板，否则使用以下描述布局：

```text
<Talk Description>

Speakers:
- <Name> (<Company>): <Bio>
  X/Twitter: <url-or-handle>
  LinkedIn: <url>
  GitHub: <url-or-handle>
```

如果提交的完整演讲描述/摘要适合公开展示，请将其完整包含在内。包含演讲者填写的社交媒体和公司/项目 URL，但对于缺失字段，不要保留空行。不要包含源视频 URL 或内部 `Additional Notes`/审核者字段。

描述应保持客观，不要杜撰缺失的所属机构。对于不完整的演讲者姓名，使用现有字段；如果用户要求补全缺失的公开信息，则使用网络搜索。

## UI 自动化

使用 Chrome DOM 自动化操作 YouTube Studio 时，请阅读 `references/ui-js-snippets.md`。这些代码片段涵盖设置 contenteditable 标题/描述框、选择播放列表、逐步点击、保存为不公开状态，以及验证行状态。

对于仅限 Studio 的现有视频清理工作，例如更换缩略图、设置发布时间、恢复保存状态或修复上传后的播放列表，请切换到 `youtube-studio-computer-use` skill。此 skill 应专注于获取来源、准备元数据、整理文件名、批量上传和上传台账。

当 DOM 自动化无法访问原生 UI 时，使用直接的 Computer Use 点击操作处理文件选择器和模态框按钮。仅在确认截图状态后使用坐标。

## 验证

- 验证每个已上传行在保存后均显示 `Unlisted`。
- 使用辅助审计工具或 DOM 回读，验证描述中不存在源 URL 模式。
- 在上传模态框中验证播放列表选择；YouTube Studio 的频道列表并不总是显示播放列表成员关系。
- 检查上传处理对话框：如果对话框仍提示必须先完成 SD 处理才能以不公开方式发布，仅显示 `Video upload complete` 并不足够。

## 辅助脚本

`scripts/youtube_batch_helper.py` 提供：

- `build-metadata`：将 Airtable/CSV 行转换为 YouTube 元数据 JSON 和受阻行报告。
- `audit-descriptions`：扫描元数据 JSON，检查是否意外包含源 URL。
- `ledger`：创建或更新包含已上传链接和状态的 CSV 台账。

运行 `python3 scripts/youtube_batch_helper.py --help` 查看命令详情。
