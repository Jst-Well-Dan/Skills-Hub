<!-- source-sha256: f036ca8e0c908acdb530eda8cad1631328aabc73c55798b624aac06b8b824fbc -->
---
name: media-transform
description: 通用媒体转换编排器——从任何来源（X/Twitter、Zoom、YouTube、网页嵌入）下载视频，上传到 YouTube，生成带时间戳的转录、章节，使用 GPT-Image-2 创建缩略图，并对标题进行 A/B 测试。当用户希望将视频从一个平台迁移到另一个平台，或提出“下载此视频并上传到 YouTube”“发布此录像”“保存并转录此内容”或任何视频流水线任务时使用。包含每个阶段中总结出的最佳实践和偏好。
---

# 媒体转换

用于媒体转换流水线的通用编排器。根据来源和目标串联原子技能，并在每个阶段设置检查点。

## 架构

流水线的每个阶段都由一个专用原子技能处理。此编排器提供：

1. **阶段选择**——根据来源和目标决定运行哪些步骤
2. **偏好设置**——经过实战检验的默认值和已知注意事项
3. **经验总结**——哪些方法有效、哪些无效，以及应避免什么
4. **检查点**——展示计划、获得确认，然后执行

## 原子技能

| 阶段 | 技能 | 备注 |
|-------|-------|-------|
| 下载（X/Twitter） | `download-x-video` | yt-dlp、`--print after_move:filepath` |
| 下载（Zoom） | `zoom-download` | 基于浏览器，优先使用画廊视图 |
| 下载（网页嵌入） | `download-video` | 处理 Vimeo、YouTube 嵌入和 referer 请求头 |
| 下载（通用 URL） | 直接使用 `yt-dlp` | `brew install yt-dlp` |
| 上传到 YouTube | `youtube-api` | OAuth、可恢复上传、标签、元数据 |
| 更新元数据 | `youtube-api` | `update_metadata.py`——标题、描述、标签 |
| 设置缩略图 | `youtube-api` | `set_thumbnail.py`——上传自定义缩略图 |
| 转录 | `transcribe-anything` | 多后端，自动选择最佳后端 |
| 章节（LLM 标题） | `podcast-publishing-assistant` | 高质量章节摘要 |

## 流水线

### 流水线 A：X/Twitter → YouTube + 章节

```
download-x-video → youtube-api（上传）→ transcribe-anything → youtube-api（更新描述）
```

```bash
# 1. 下载
python3 download-x-video/scripts/download_x_video.py "https://x.com/user/status/123/video/1" /tmp

# 2. 上传（不公开）
python3 youtube-api/scripts/upload_video.py \
    --file /tmp/x_video_<id>.mp4 \
    --title "视频标题" \
    --privacy unlisted

# 3. 转录（在 Apple Silicon 上优先使用 mlx_whisper）
mlx_whisper /tmp/x_video_<id>.mp4 \
    --model mlx-community/whisper-turbo \
    --output-dir /tmp --output-format json \
    --word-timestamps True

# 4. 生成章节并更新描述
# 请参阅下方的“章节生成”部分
```

### 流水线 B：Zoom → YouTube + 缩略图

```
zoom-download → youtube-api（上传 + 元数据 + 缩略图）
```

Zoom 录像通常自带转录。重点处理合适的标题、播放列表分配和缩略图。

### 流水线 C：通用视频 → YouTube + 转录

```
yt-dlp 下载 → youtube-api（上传）→ transcribe-anything
```

对于 yt-dlp 支持的任何视频 URL（YouTube、Vimeo 等），下载后重新发布。

## 标题生成

使用 LLM 生成 3–5 个候选标题。根据以下启发式标准进行评估：

**优秀 YouTube 标题的特点：**
- **好奇心缺口**：暗示存在观众尚不了解的信息
- **具体性**：姓名、数字和具体论断胜过含糊表述
- **打破惯性**：采用意外的叙述角度或矛盾表达
- **少于 70 个字符**：避免在搜索结果中被截断
- **关键词前置**：将最重要的词放在最前面
- **拒绝标题党**：标题必须与内容相符（留存率比 CTR 更重要）

**标题生成提示词模板：**
```
为一个关于 [topic] 的视频生成 5 个 YouTube 候选标题。
视频时长为 [duration]，内容为 [brief content description]。

要求：
- 每个标题少于 70 个字符
- 使用不同角度：(1) 激发好奇，(2) 操作指南/价值导向，(3) 争议性/逆向观点，
  (4) 具体/数字驱动，(5) 问题形式
- 不要全部使用大写字母，不要滥用表情符号
- 标题必须准确反映内容
```

### 标题 A/B 测试

YouTube Studio 原生提供“测试与比较”（Test & Compare）功能（最多测试 3 个标题/缩略图，最长运行 2 周，根据观看时长占比确定胜者）。YouTube Data API 无法直接使用此功能。

**以编程方式自行进行 A/B 测试：**

使用 `youtube-api/scripts/update_metadata.py` 按计划轮换标题，然后通过 YouTube Analytics 分析表现：

```bash
# 开始测试：设置标题 A
python3 youtube-api/scripts/update_metadata.py --video-id <ID> --title "标题 A"

# 24–48 小时后：轮换为标题 B
python3 youtube-api/scripts/update_metadata.py --video-id <ID> --title "标题 B"

# 再过 24–48 小时：查看分析数据以确定胜者
# 胜者 = 更高的 CTR * 平均观看时长（早期测试也可只看 CTR）
```

**A/B 测试计划：**
- 每 24–48 小时轮换一次（YouTube 需要时间积累展示次数）
- 每个视频测试 2–3 个标题
- 总计运行 1–2 周
- 胜者依据：CTR（点击率）× 留存率，而不只是观看次数

## 缩略图生成

### GPT-Image-2（推荐）

通过 `image_generate` 工具使用 GPT-Image-2（`openai/gpt-image-2`）是首选的缩略图生成方式：

**与缩略图相关的关键能力：**
- **近乎完美的文本渲染**：可在缩略图中加入清晰可读的文本（此前 AI 无法做到）
- **思考模式**：渲染前规划构图，确保面孔、文本和布局协调一致
- **最高 2K 分辨率**：2048px，非常适合制作 1280×720 的缩略图，并留有裁剪空间
- **16:9 宽高比**：YouTube 缩略图原生比例
- **多语言文本**：支持多种文字系统（拉丁文字、CJK 等）
- **多变体生成**：通过一个提示词生成最多 4–8 个风格一致的变体

**缩略图提示词模板：**
```
为标题为“[TITLE]”的视频制作 YouTube 缩略图。风格：[clean/bold/minimalist/tech]。
[Specific visual elements: faces, diagrams, text overlays]。
宽高比：16:9。高对比度、引人注目。画面简洁。
图中要显示的文字（如有）：“[KEY PHRASE]”，位置为 [position]。
```

**生成后处理：**
- 使用 `youtube-api/scripts/set_thumbnail.py` 上传
- 如果大于 2MB，请压缩：`convert -resize 1280x720 -quality 85 input.png output.jpg`

### 缩略图 A/B 测试

YouTube 原生“测试与比较”（Test & Compare）功能最多支持 3 张缩略图。生成 3 种不同的创意方案：

1. **文字为主**：使用大号字体展示关键短语或数字
2. **面孔/情绪**：富有表现力的反应和眼神交流
3. **概念/抽象**：使用与主题相关的视觉隐喻

## 各阶段的偏好与经验总结

### 下载

**yt-dlp 路径检测：**
- 使用 `--print after_move:filepath` 可靠地获取最终路径（不要通过解析 stdout 中的 `[download] Destination` 获取）
- 来自 X/Twitter 的 HLS 流在下载过程中使用分片文件名；只有 `after_move` 路径才是最终合并文件

**X/Twitter 身份验证：**
- 某些视频需要身份验证：`yt-dlp --cookies-from-browser chrome`

### 上传

**OAuth 令牌缓存：**
- `youtube-api` 技能会处理此操作：`~/.config/youtube-api/token.pickle`（或 Cowork 路径）
- 首次运行会打开浏览器请求授权；后续运行将使用缓存
- 在 Mac 上 → 本地配置；在 Cowork VM 中 → 挂载的 Downloads 文件夹（重置后仍会保留）

**默认隐私设置：**
- 除非用户明确要求设为 `public`，否则始终默认为 `unlisted`

**可恢复上传：**
- Google API 客户端支持可恢复上传，因此大型文件（100MB 以上）也能顺利上传

### 转录

**在 Apple Silicon 上优先使用 mlx_whisper（速度快 10 倍）：**
- `mlx_whisper`（`pipx install mlx-whisper`）：约 1300 帧/秒 → 转录 27 分钟音频约需 2 分钟
- `openai-whisper` CLI：约 95 帧/秒 → 转录相同音频约需 28 分钟
- `openai-whisper` 搭配 `--device mps` 使用 turbo/large 模型时会产生 NaN 错误——**请避免使用**，改用 mlx_whisper

**Turbo 模型是最佳平衡点：**
- 速度足以满足实时使用
- 质量几乎与 large 模型一样好
- small 模型准确度太低，不适合生成章节

**说话人分离仍属于理想目标：**
- 需要 whisperX + pyannote + HuggingFace token
- 会增加 5–10 分钟处理时间
- 质量取决于音频清晰度
- 可用时，使用带 `--diarize` 标志的 `transcribe-anything`

### 章节生成

**垃圾内容过滤至关重要：**
- 过滤纯填充语片段：“Yeah.”、“Cool.”、“Mm-hmm.”、“Right.”
- 过滤重复填充语：“Yeah. Yeah. Yeah.”（连续出现 3 个以上无意义词）
- 末尾经常出现空片段（文本为空、时长为零）

**按词边界截断：**
- 不要在单词中间截断章节标题
- “What areas of data do you feel are underserved by now that l” → 在最后一个空格处截断

**质量要求较高时使用 LLM 标题：**
- 原始转录生成的章节虽可用，但不够美观
- 若需要精致的输出，请使用 `podcast-publishing-assistant`，或将片段提供给 LLM
- 提示词：“为这些带时间戳的转录片段生成简洁的章节标题（少于 60 个字符）”

**间隔调整：**
- 默认 30 秒间隔会为 27 分钟的视频生成约 46 个章节——便于导航
- 60 秒间隔会生成约 27 个章节——更简洁，但粒度较低
- 10 秒间隔对 YouTube 来说过于细碎（章节数量上限约为 100）

## 检查点模式

在每个操作阶段开始前展示摘要并获得确认。这样可以尽早发现不匹配：

1. **执行前检查**：扫描来源（推文、Zoom 录像等）→ 列出可用内容
2. **标题检查**：展示 3–5 个候选标题，由用户选择
3. **缩略图检查**：生成 3 个缩略图变体，由用户选择
4. **下载完成**：确认文件、标题和时长
5. **上传完成**：确认 URL、隐私设置和播放列表
6. **转录完成**：确认片段数量和质量
7. **最终确认**：展示所有结果，并询问是否设置标题 A/B 测试

## 故障排除

### 未启用 YouTube API
```bash
gcloud services enable youtube.googleapis.com --project=<PROJECT_ID>
```

### OAuth 重定向失败（ERR_CONNECTION_REFUSED）
- 确保端口未被占用：`lsof -i :8080`
- GCP OAuth 的重定向 URI 中必须包含 `http://localhost`

### mlx_whisper 报错“Failed to load audio”
- `brew install ffmpeg`

### 章节质量较差
- 原始转录章节可满足快速导航需求，但显得不够专业
- 若需达到发布质量，请使用 `podcast-publishing-assistant` 或 LLM 后处理
- 垃圾内容过滤能捕获大多数低质量章节，但可能遗漏边缘情况（“I mean”“you know”）

### 缩略图过大
- YouTube 的大小上限为 2MB。压缩命令：`convert -resize 1280x720 -quality 85 input.png output.jpg`
- GPT-Image-2 的输出在上传多个变体时可能需要压缩
