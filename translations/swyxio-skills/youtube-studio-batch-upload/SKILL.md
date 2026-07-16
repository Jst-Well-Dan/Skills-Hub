<!-- source-sha256: fffd0a483d24b0980b413b100b1e9682a0185195ad2edae55c63870a391e4caf -->
---
name: youtube-studio-batch-upload
description: 对来自 Airtable、Google Drive、Loom、YouTube 或本地文件的视频执行 YouTube Studio 批量上传工作流。当 Codex 需要下载大量已提交的视频、整理文件名、根据表格字段生成 YouTube 标题和描述、通过 Chrome/Computer Use 上传、将视频设为不公开、添加播放列表、在继续处理下一个视频前保存每次上传、跟踪链接，以及报告不完整或受阻的源数据行时使用。
---

# YouTube Studio 批量上传

## 操作规则

- 对 YouTube Studio 或 Airtable 实时界面执行操作时，使用 browser/computer-use skill。在一个回合中直接操作界面之前，先调用 `get_app_state`。
- 将上传视为批量瀑布式流程：下载/恢复来源、整理文件名、准备元数据、上传、逐个设置视频标题/播放列表/可见性并保存、验证、登记。
- 不要在 YouTube 描述中包含源视频 URL。除非用户明确要求发布这些链接，否则从最终描述中移除 Drive、Loom、WeTransfer 和源 YouTube 链接。
- 在进入可见性设置之前，始终选择目标播放列表。
- 在打开或编辑下一个上传项之前，始终选择 `Unlisted` 并点击 `Save`。
- 如果 YouTube 因 SD 处理尚未完成而阻止保存，请在模态框中等待，并在处理完成后保存。不要假定草稿已经发布。
- 在界面允许时，优先批量选择文件。如果选择器控件失效，则分成更小的批次上传或逐个上传文件，但下载和元数据准备仍应批量进行。
- 对 `waitlisted`、`WIP`、`To provide`、私有/已删除链接或拒绝访问的 Drive 文件等数据行，保留清晰的受阻列表。

## 工作流

1. 将源表格导出或抓取为 CSV/TSV，至少包含：演讲者姓名、演讲标题、演讲描述、视频源 URL、个人简介、公司、社交账号、LinkedIn/GitHub 和备注。
2. 构建清单和元数据 JSON：
   - 运行 `scripts/youtube_batch_helper.py build-metadata presenters.csv --out work/youtube_metadata.json`。
   - 除非用户另有说明，否则使用 `--playlist "Playlist Name"` 和 `--skip-source-url`。
   - 下载前检查受阻数据行，以及源字段值为占位符的数据行。
3. 将源视频下载到 `downloads/.../raw`：
   - Drive：优先使用 `yt-dlp`；如果权限要求使用 Chrome Cookie/会话，则通过已在浏览器中验证身份的方式直接下载。
   - Loom：尝试使用 `yt-dlp`；如果失败，检查页面中的签名 HLS 清单，并使用 `ffmpeg` 合并。
   - YouTube 源视频：尝试使用带浏览器 Cookie 或备用播放器客户端的 `yt-dlp`。遵守访问权限和版权限制。
4. 在批次目录下整理待上传文件，并使用最终的人类可读文件名：
   - `Talk Title - Speaker Name.mp4`
   - 保留 YouTube 接受的标点符号；避免使用对文件系统不友好的字符。
5. 在 Chrome 中打开 YouTube Studio 上传页面，选择尽可能多的已整理文件，然后完成每个上传对话框：
   - 根据元数据设置标题和描述。
   - 选择播放列表。
   - 依次完成 Video elements 和 Checks。
   - 选择 `Unlisted`。
   - 保存并等待，直到该行显示为 `Unlisted / None` 或显示已知限制。
6. 将每个 YouTube 链接记录到账本中，并报告：
   - 已上传数量和新链接。
   - 所有受限情况，尤其是版权限制。
   - 无法处理/不可用的源数据行及其确切原因。

## 元数据结构

除非用户提供特定于频道的模板，否则使用以下描述布局：

```text
<Talk Description>

Speakers:
- <Name> (<Company>): <Bio>
  X/Twitter: <url-or-handle>
  LinkedIn: <url>
  GitHub: <url-or-handle>

Additional notes/links:
- <notes that are not source video URLs>
```

描述应保持事实准确，不要虚构缺失的所属机构。对于不完整的演讲者姓名，使用现有字段；如果用户要求补充缺失的公开信息，则进行网络搜索。

## 界面自动化

使用 Chrome DOM 自动化操作 YouTube Studio 时，请阅读 `references/ui-js-snippets.md`。这些代码片段涵盖设置 contenteditable 标题/描述框、选择播放列表、点击完成各步骤、将视频保存为不公开，以及验证数据行状态。

当 DOM 自动化无法访问原生界面时，对文件选择器和模态框按钮使用直接的 Computer Use 点击操作。仅在确认截图状态后使用坐标。

## 验证

- 验证每个已上传的数据行在保存后均显示 `Unlisted`。
- 使用辅助程序审计或 DOM 回读，验证描述中不存在源 URL 模式。
- 在上传模态框中验证播放列表选择；YouTube Studio 的频道列表并不总是显示播放列表成员关系。
- 检查上传处理对话框：如果对话框仍提示必须完成 SD 处理才能以不公开方式发布，仅显示 `Video upload complete` 并不足够。

## 辅助脚本

`scripts/youtube_batch_helper.py` 提供：

- `build-metadata`：将 Airtable/CSV 数据行转换为 YouTube 元数据 JSON 和受阻数据行报告。
- `audit-descriptions`：扫描元数据 JSON，检查是否意外包含源 URL。
- `ledger`：创建或更新包含已上传链接和状态的 CSV 账本。

运行 `python3 scripts/youtube_batch_helper.py --help` 查看命令详情。
