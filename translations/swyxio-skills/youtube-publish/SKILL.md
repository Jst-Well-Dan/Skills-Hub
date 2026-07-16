<!-- source-sha256: e23b6b1ccd41a046a25e9e7f4f3843ef869759822736aeea0f67e6c4abd492fb -->
---
name: youtube-publish
description: >
  当用户要求“将视频上传到 YouTube”、
  “在 YouTube 上发布视频”、“设置 YouTube 标题和描述”、
  “为 YouTube 视频添加时间戳”，或需要编辑视频元数据、
  分配播放列表并在 YouTube Studio 中发布时，应使用此技能。
version: 0.1.0
---

# YouTube 视频发布与元数据

## 概述
将视频文件上传到 YouTube Studio，设置标题、描述、时间戳和播放列表，然后发布。

## 分步工作流程

### 1. 上传视频
- 前往 YouTube Studio → 内容 → 点击**创建** → **上传视频**
- **浏览器限制**：无法通过程序设置文件输入。用户必须在文件选择器对话框中手动选择文件。
- 上传所有文件，并等待处理完成（YouTube 会显示进度指示器）

### 2. 设置标题
根据内容类型（通过帧提取结果或会议名称确定）使用以下格式：

| 内容类型 | 标题格式 | 示例 |
|---|---|---|
| Weekly Jam（演示） | `[Topic/Demo]: AI in Action [D Mon YYYY]` | SpaceMolt - AI Agents in Multiplayer Space Games: AI in Action 7 Feb 2026 |
| Weekly Jam（演讲） | `[Topic]: AI in Action [D Mon YYYY]` | Recursive Language Models & Reasoning Trees: AI in Action 31 Jan 2026 |
| Paper Club | `[Paper Short Name] Paper Reading: AI in Action [D Mon YYYY]` | RL via Self-Distillation (SDPO) Paper Reading: AI in Action 12 Feb 2026 |
| 嘉宾场次 | `[Topic]: [Guest] and swyx [D Mon YYYY]` | — |

标题须保持在 **100 个字符以内**。将主题放在开头以便用户发现；系列名称和日期放在末尾。

### 3. 设置描述
模板：
```
Latent Space [Series Name] - [D Mon YYYY]

[Presenter name] [presents/demos/discusses] [对内容的 1-2 句简要描述]。

[可选：论文链接，例如“论文：https://arxiv.org/abs/XXXX.XXXXX”]

时间戳：
[HH:MM:SS] - [章节描述]
[HH:MM:SS] - [章节描述]
...

参与者：[画廊视图中可见的姓名]

加入 Latent Space 社区：https://latent.space
```

#### 生成时间戳
使用帧提取数据（来自 `zoom-download` 技能）识别自然的章节分界：
- **幻灯片切换** = 新主题或章节
- **演示开始/结束** = 过渡点
- **问答环节** = 通常位于末尾
- **论文章节**（适用于 Paper Club）= 引言、方法、结果、讨论

时长不足 1 小时的视频使用 `MM:SS` 格式，更长的视频使用 `H:MM:SS` 格式。YouTube 会自动将描述中的时间戳转换为链接。

每个视频应包含 **5-10 个时间戳**。每一项都应代表一次有意义的内容转变。

### 4. 设置播放列表
在“详细信息”页面的**播放列表**下 → 点击**选择**：

| 内容类型 | 播放列表 |
|---|---|
| AI in Action Weekly Jam（演示、展示、演讲） | **AI in Action** |
| 论文阅读 / Paper Club 场次 | **Paper Club** |

区分方式：
- Zoom 会议名称为“AI in Action Weekly Jam!” → **AI in Action** 播放列表
- 会议名称类似“[Person] and swyx”，且屏幕上显示 arxiv 论文 → **Paper Club** 播放列表
- 无法确定时，检查帧提取结果中是否有 arxiv 链接或论文标题 → Paper Club

### 5. 其他设置
- **观众**：“否，不是面向儿童的内容”（通常已是默认设置）
- **可见性**：**不公开**
- **立即发布**——不要保留为草稿

### 6. YouTube Studio 导航流程
针对每个视频：
```
详细信息 →（标题、描述、播放列表）→ 下一步 →
视频元素 → 下一步 →
检查 →（等待检查通过）→ 下一步 →
可见性 →（选择“不公开”）→ 保存/发布
```

对每个视频重复以上步骤。务必立即发布。

### 7. 验证
发布后，确认：
- 视频 URL 可访问（显示在“详细信息”页面的“视频链接”下）
- 标题、描述和播放列表正确
- 状态显示为“不公开”（而非“草稿”或“私享”）

## 故障排除
- **“处理中……”卡住**：对于较长的视频，YouTube 处理可能需要 5-30 分钟。请等待并刷新。
- **检查显示警告**：可能会出现版权或其他警告。对于原创 Zoom 录制内容，这些通常是误报——除非遇到硬性阻止，否则继续操作。
- **频道错误**：如果在“内容”中看到不熟悉的视频，则说明当前频道不正确。通过头像菜单切换账号。
- **重复上传**：上传前检查“内容”列表中是否已有时长和日期相同的视频。文件名后缀 `_gvo_` 表示仅包含画廊视图的重复文件，不应上传。
