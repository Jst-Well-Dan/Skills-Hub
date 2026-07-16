<!-- source-sha256: 8b78d002681e806d8ed730d0f214e5f2db6e61d0944d59b36a1432009f1f7bdd -->
---
name: conference-transcribe
description: |
  将包含多场演讲的会议直播或较长的 YouTube 视频转录为按演讲拆分的独立文本。解析视频描述中的时间戳以拆分演讲，下载音频/视频，转录每个片段，然后使用 LLM 清理并格式化转录文本，添加关键要点和密集时间戳。当用户说“转录这场会议”“将此直播拆分为多场演讲”“分别转录每场演讲”，或提供带章节时间戳的数小时活动直播 YouTube URL 时使用。
license: MIT
user_invocable: true
argument-hint: <youtube-url>
compatibility: |
  需要安装了 ffmpeg 和 yt-dlp 的 macOS。至少需要一个转录后端（推荐使用 Groq API 以获得更快速度）。清理阶段需要 LLM API 密钥（推荐 Anthropic）。
metadata:
  author: swyxio
  version: "1.0"
  last-updated: "2026-04-10"
  primary-tools: yt-dlp, ffmpeg, Groq Whisper API, Claude API
---

# 会议转录

将包含多场演讲的会议直播转录为独立、清理完善的单场演讲 Markdown 文件，并附上关键要点和密集时间戳。

## 经验总结（来自 2026 年 4 月 AIE Europe 第一天）

此技能诞生于一次真实的转录工作。以下是有效和无效的方法：

### 有效的方法

1. **将 YouTube 自动字幕作为主要来源**——YouTube 的英文自动字幕（VTT）效果出奇地好，而且是*即时*可用的。无需等待下载，无需下载模型，也无需 GPU。对于提供字幕的 YouTube 视频，应优先于 Whisper 使用此方法。
2. 使用 **`yt-dlp --write-sub --write-auto-sub --sub-lang en`** 直接获取字幕，然后解析 VTT 文件。
3. 使用 **`yt-dlp --download-sections`** 将各场演讲下载为 MP4 片段（用于存档/分享），并通过 `ThreadPoolExecutor(max_workers=2)` 并行处理。
4. **解析视频描述**以获取章节时间戳——视频描述是确定演讲边界的权威来源。
5. **两阶段转录流程**：原始 VTT 解析 -> LLM 清理。原始解析负责去重和时间戳分桶；LLM 负责提升可读性、修正专有名词、提取关键要点并进行格式化。
6. **使用 Opus 压缩**以便上传至云端 API：`ffmpeg -c:a libopus -b:a 32k` 可将 1 小时音频压缩至约 14MB（低于 Groq/OpenAI 的 25MB 限制）。
7. `yt-dlp --write-info-json` 生成的 **`metadata.json`** 提供结构化章节数据，比解析描述文本更容易。

### 无效的方法

1. 在新机器上使用**本地 Whisper（任何变体）**都很麻烦：
   - `pip install` 会与 macOS 的外部管理环境（PEP 668）冲突。需要使用 `uv venv` 或 `--break-system-packages`。
   - `mlx-whisper` 的模型下载量很大（large-v3-turbo 约 1.5GB），且在没有 `HF_TOKEN` 时会被限速。
   - 在 CPU 上运行 `faster-whisper`，转录 7 小时以上的音频会非常慢。
   - 总体而言，从头配置本地 Whisper 所花的时间，比直接使用 YouTube 字幕还长。
2. **没有密钥时使用 Groq API**——需要预先向用户索取。
3. **在 Apple Silicon 上并行运行 Whisper**——MLX 使用 GPU，因此并行工作线程会争用资源。本地模型更适合顺序运行。
4. **上传大型 WAV 文件至 API**——16kHz 单声道 WAV 约为 1.9MB/分钟。一场 30 分钟的演讲约为 57MB，超过 API 的 25MB 限制。必须先压缩为 opus/ogg。

### 决策树：选择哪个转录后端？

```
是否有 YouTube 字幕？（使用 yt-dlp --list-subs 检查）
  是 -> 使用 YouTube 字幕（最快、免费、无需配置）
  否 -> 是否有 Groq/OpenAI API 密钥？
    是 -> 使用 Groq API（whisper-large-v3-turbo，几乎免费且非常快）
    否 -> 是否已安装本地 Whisper？
      是 -> 使用 faster-whisper 或 mlx-whisper
      否 -> 通过 uv 安装：`uv venv .venv && source .venv/bin/activate && uv pip install faster-whisper`
```

## 分步工作流程

### 步骤 0：检查前置条件

```bash
which yt-dlp || echo "MISSING: brew install yt-dlp"
which ffmpeg || echo "MISSING: brew install ffmpeg"
which jq || echo "MISSING: brew install jq"

# Check for API keys (optional but recommended)
[ -n "$GROQ_API_KEY" ] && echo "Groq: ready" || echo "Groq: not set (needed for Whisper API)"
[ -n "$ANTHROPIC_API_KEY" ] && echo "Anthropic: ready" || echo "Anthropic: not set (needed for cleanup)"
```

### 步骤 1：获取视频元数据和字幕

```bash
VIDEO_URL="$1"  # YouTube URL from user

# Download metadata + captions (no video)
yt-dlp --write-info-json --skip-download \
  --write-sub --write-auto-sub --sub-lang en \
  -o "media/%(id)s" "$VIDEO_URL"
```

这会生成：

- `media/<id>.info.json`——包含章节在内的完整元数据
- `media/<id>.en-orig.vtt` 或 `media/<id>.en.vtt`——自动字幕

### 步骤 2：将章节时间戳解析为演讲清单

读取 `.info.json` 文件并提取章节。过滤休息时段、无标题片段等内容。

创建 `talks.json` 清单：

```json
[
  {
    "index": 1,
    "title": "Speaker Name: Talk Title",
    "speaker": "Speaker Name",
    "slug": "01-speaker-name",
    "source_chapter_start": "00:24:25",
    "source_chapter_end": "00:42:39",
    "start_seconds": 1465,
    "end_seconds": 2559,
    "duration_seconds": 1094
  }
]
```

如果元数据中没有章节，则改为解析视频描述，查找符合以下模式的时间戳行：

- `HH:MM:SS - Speaker Name: Talk Title`
- `HH:MM:SS Speaker Name (Company): Description`

### 步骤 3：构建原始转录文本（字幕路径）

如果有 YouTube 字幕，则解析 VTT 文件：

1. 解析所有 VTT 提示段（时间戳 + 文本）。
2. 对清单中的每场演讲，选择其时间范围内的提示段。
3. **对重叠文本去重**——YouTube VTT 提示段经常重复上一提示段中的单词。使用滑动窗口单词匹配方法（参见 `append_without_overlap` 模式）。
4. **将提示段按约 30 秒分桶组成段落**，以提升可读性。
5. 将每场演讲写入原始转录文件，并使用双时间戳：`[HH:MM:SS | +MM:SS]`（直播绝对时间 | 相对于演讲开始的时间）。

输出格式：

```markdown
# 演讲者姓名：演讲标题

- 来源：https://youtube.com/watch?v=ID&t=1465s
- 来源范围：00:24:25 - 00:42:39
- 时长：00:18:14
- 转录来源：YouTube 自动字幕

## 带时间戳的转录文本

[00:24:26 | +00:00:01] 大家早上好……

[00:24:54 | +00:00:29] 下一段文本……
```

### 步骤 3（备选）：构建原始转录文本（Whisper/API 路径）

如果没有 YouTube 字幕，则从音频进行转录：

1. 下载音频：`yt-dlp -f bestaudio -x --audio-format wav -o "full_audio.%(ext)s" "$VIDEO_URL"`
2. 使用 ffmpeg 拆分为单场演讲片段：
   ```bash
   ffmpeg -i full_audio.wav -ss "$START" -to "$END" -ac 1 -ar 16000 "segments/${SLUG}.wav"
   ```
3. 压缩以供 API 上传：
   ```bash
   ffmpeg -i "segments/${SLUG}.wav" -ac 1 -ar 16000 -c:a libopus -b:a 32k "segments/${SLUG}.ogg"
   ```
4. 如果 ogg > 25MB，则进一步拆分为 10 分钟的分块。
5. 通过 Groq API（首选）或其他后端进行转录：
   ```bash
   curl -s https://api.groq.com/openai/v1/audio/transcriptions \
     -H "Authorization: Bearer $GROQ_API_KEY" \
     -F file="@segments/${SLUG}.ogg" \
     -F model="whisper-large-v3-turbo" \
     -F language="en" \
     -F response_format="verbose_json" \
     -F 'timestamp_granularities[]=segment'
   ```
6. 重新组合各分块，并校正偏移量以生成绝对时间戳。
7. 并行处理：对于 Groq 的速率限制，同时发起 3 个 API 调用是安全的。

### 步骤 4：下载视频片段（可选、并行）

用于存档各场演讲视频：

```bash
yt-dlp -f 91 \
  --downloader ffmpeg \
  --downloader-args "ffmpeg_i:-allowed_extensions ALL" \
  --download-sections "*${START}-${END}" \
  -o "clips/${SLUG}.%(ext)s" \
  "$VIDEO_URL"
```

使用 `ThreadPoolExecutor(max_workers=2)` 运行——并发执行超过 2 个 yt-dlp 下载任务往往会被限速。

### 步骤 5：LLM 清理阶段

将每份原始转录文本发送给 Claude（或其他 LLM）进行清理。同时发起 3 个 API 调用。

**用于清理的系统提示词：**

```
你是一名专业的转录文本编辑。请将这份原始自动字幕转录文本整理为清晰、易读的文档。

规则：
1. 保留所有采用 [HH:MM:SS | +MM:SS] 格式的时间戳。每隔 30-60 秒包含一个时间戳。
2. 修正转录错误：专有名词、技术术语、公司名称和行业术语。
3. 在自然的话题转换处添加段落分隔。
4. 删除填充词（嗯、呃、就是、你知道），除非它们具有实际含义。
5. 保留演讲者的表达风格——只做清理，不要重写。
6. 对于多人发言片段，使用 [演讲者姓名]: 格式。

输出格式：
# 演讲标题
**演讲者**——职位/公司
**活动**：{活动名称和日期}

## 关键要点
- 4-8 条关键收获

## 带时间戳的易读转录文本
[包含时间戳和段落的内容，并进行适度换行以提升可读性]
```

### 步骤 6：写入最终输出

按以下结构组织：

```
transcripts/
  raw/       -- 未编辑的 VTT 解析或 Whisper 输出
  cleaned/   -- 经 LLM 清理的 Markdown
clips/       -- 各场演讲的 MP4 文件（可选）
talks.json   -- 包含元数据的清单
reports/
  talk-manifest.md  -- 汇总表
```

## 快速开始（复制粘贴）

适用于带章节和自动字幕的 YouTube 会议直播这一常见场景：

```bash
# 1. Grab metadata + captions
yt-dlp --write-info-json --skip-download --write-auto-sub --sub-lang en -o "media/%(id)s" "$URL"

# 2. Build talks.json from chapters in info.json
python3 scripts/build_transcripts.py

# 3. Download individual clips (parallel, optional)
python3 scripts/download_clips.py

# 4. Clean up transcripts with LLM
python3 scripts/cleanup_transcripts.py
```

`build_transcripts.py` 和 `cleanup_transcripts.py` 脚本负责处理 VTT 解析、去重、时间戳格式化和 LLM 清理。参考实现请参阅 AIE Europe 项目。
