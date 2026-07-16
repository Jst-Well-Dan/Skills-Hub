<!-- source-sha256: 96208a59d75adbac34fd2a8086cfb1c2f65ce4aae91972e386db5a936370737b -->
---
name: transcribe-anything
description: |
  使用可插拔的 ASR 后端将音频和视频文件转录为文本。默认后端是本地 whisper CLI（openai-whisper）。支持 whisperX（含说话人分离）、insanely-fast-whisper、faster-whisper、whisper.cpp、OpenAI Whisper API、Groq Whisper API、Deepgram、AssemblyAI、Gemini 和 Hugging Face 模型。通过使用 ffmpeg 进行预处理来处理超长文件（1–8 小时以上）：从视频中提取音频、转换为适合 ASR 的最佳格式、检测并跳过静音，以及针对 API 大小限制进行分块。支持说话人分离、词级时间戳、自定义词汇和多种输出格式。当有人说“转录这个”“转换成文本”“语音转文字”“获取文字稿”“转录这个视频/音频/播客/录音”，或提供媒体文件并希望获得文本输出时，请使用此技能。
license: MIT
compatibility: |
  需要 macOS（推荐 Apple Silicon）并已安装 ffmpeg。至少必须有一个可用的 ASR 后端——默认使用 openai-whisper（pip install openai-whisper）。如需说话人分离，推荐使用 whisperX（pip install whisperx）。如使用云端后端，必须将相应的 API 密钥设置为环境变量。
metadata:
  author: swyxio
  version: "1.0"
  last-updated: "2026-03-28"
  hardware: Apple Silicon（M 系列），也可在 CUDA GPU 和 CPU 上运行
  primary-tools: ffmpeg, whisper, whisperx, yt-dlp
---

# 转录任何内容

将音频和视频文件转录为文本。支持可插拔后端、针对长文件跳过静音、可选的说话人分离，以及多种输出格式。

## 设置

### 必需项（请先安装这些）

```bash
# ffmpeg — audio extraction, preprocessing, silence detection
brew install ffmpeg

# yt-dlp — downloading video/audio from URLs (optional but recommended)
brew install yt-dlp

# Default ASR backend — OpenAI's whisper CLI
pip3 install --break-system-packages openai-whisper
```

### 推荐的额外组件

```bash
# curl_cffi — prevents OAuth errors when downloading private videos
pip3 install --break-system-packages curl_cffi

# faster-whisper — 4x faster than whisper, built-in VAD silence skipping, lower memory
# Best local backend for long files (1hr+)
pip3 install --break-system-packages faster-whisper

# whisperX — adds speaker diarization + precise word-level timestamps
# Bundles faster-whisper + pyannote alignment
pip3 install --break-system-packages whisperx
```

**whisperX 说话人分离设置**（仅需一次）：

1. 在 https://huggingface.co 创建 Hugging Face 账户
2. 接受以下受限模型的条款：
   - https://huggingface.co/pyannote/speaker-diarization-3.1
   - https://huggingface.co/pyannote/segmentation-3.0
3. 在 https://huggingface.co/settings/tokens 创建访问令牌
4. 在 shell 配置文件中设置 `export HF_TOKEN=hf_...`

即使没有 HF 令牌访问权限，whisperX 仍可用于转录和词语对齐——只是不会提供说话人标签。

### 其他本地后端（可选，按需选择）

```bash
# insanely-fast-whisper — batched GPU inference, 10-20x faster on NVIDIA GPUs
pip3 install --break-system-packages insanely-fast-whisper

# whisper.cpp — C++ native with Metal acceleration on Apple Silicon
# Best option if you want to avoid Python entirely
brew install whisper-cpp
```

### 云端 API 密钥（可选）

如果要使用云端后端，请设置以下环境变量。这些变量都不是必需的——本地 whisper 开箱即用。

```bash
# OpenAI — best accuracy with gpt-4o-transcribe ($0.006/min)
export OPENAI_API_KEY=sk-...

# Groq — cheapest and fastest cloud option ($0.00004/min with turbo)
export GROQ_API_KEY=gsk_...

# Deepgram — best cloud diarization ($0.0043/min)
export DEEPGRAM_API_KEY=...

# AssemblyAI — cloud diarization + auto-chapters ($0.0062/min)
export ASSEMBLYAI_API_KEY=...

# Gemini — handles 9.5hr files natively, flexible prompting
export GEMINI_API_KEY=...
```

### 验证设置

运行以下命令检查有哪些组件可用：

```bash
echo "=== Required ==="
which ffmpeg && echo "ffmpeg: OK" || echo "ffmpeg: MISSING (brew install ffmpeg)"
which whisper && echo "whisper: OK" || echo "whisper: MISSING (pip3 install --break-system-packages openai-whisper)"

echo ""
echo "=== Local Backends ==="
which whisperx && echo "whisperx: OK" || echo "whisperx: not installed"
python3 -c "import faster_whisper" 2>/dev/null && echo "faster-whisper: OK" || echo "faster-whisper: not installed"
which insanely-fast-whisper 2>/dev/null && echo "insanely-fast-whisper: OK" || echo "insanely-fast-whisper: not installed"
which whisper-cpp 2>/dev/null && echo "whisper.cpp: OK" || echo "whisper.cpp: not installed"

echo ""
echo "=== Cloud APIs ==="
[ -n "$OPENAI_API_KEY" ] && echo "OpenAI: configured" || echo "OpenAI: not set"
[ -n "$GROQ_API_KEY" ] && echo "Groq: configured" || echo "Groq: not set"
[ -n "$DEEPGRAM_API_KEY" ] && echo "Deepgram: configured" || echo "Deepgram: not set"
[ -n "$ASSEMBLYAI_API_KEY" ] && echo "AssemblyAI: configured" || echo "AssemblyAI: not set"
[ -n "$GEMINI_API_KEY" ] && echo "Gemini: configured" || echo "Gemini: not set"

echo ""
echo "=== Optional ==="
which yt-dlp && echo "yt-dlp: OK" || echo "yt-dlp: not installed (brew install yt-dlp)"
python3 -c "import curl_cffi" 2>/dev/null && echo "curl_cffi: OK" || echo "curl_cffi: not installed"
[ -n "$HF_TOKEN" ] && echo "HF token: configured (diarization ready)" || echo "HF token: not set (no diarization)"
```

## 后端选择指南

根据用户需求选择后端：

| 场景 | 后端 | 原因 |
|----------|---------|-----|
| 默认 / 开箱即用 | `whisper` | 已安装，质量良好 |
| 需要说话人标签 | `whisperx` | 集成说话人分离和词语对齐 |
| 超长文件，本地处理 | `faster-whisper` | VAD 跳过静音，内存占用低 |
| 追求最高速度，本地 GPU | `insanely-fast-whisper` | 批量推理，速度快 10–20 倍 |
| Apple Silicon，不使用 Python | `whisper.cpp` | Metal 加速，纯 C++ |
| 最便宜且快速的云端方案 | `groq` | turbo 模型每分钟 $0.00004 |
| 最佳云端准确率 | `openai` | gpt-4o-transcribe 模型 |
| 支持说话人分离的云端方案 | `deepgram` 或 `assemblyai` | 原生说话人标签 |
| 对音频进行灵活问答 | `gemini` | 不仅可以转录，还可以提问 |

如果用户没有指定，请按以下优先级选择：

1. `whisper`（本地已安装）
2. `whisperx`（请求说话人分离且已安装时）
3. `openai` API（已设置 OPENAI_API_KEY 且文件大小适合时）

## 分步工作流程

### 第 1 步：识别输入

接受以下任意输入类型：

- 音频文件：mp3、wav、flac、ogg、m4a、opus、wma、aac
- 视频文件：mp4、mkv、webm、mov、avi、wmv
- URL：先使用 download-video 技能，或直接使用 yt-dlp

如果输入是 URL：

```bash
yt-dlp -x --audio-format wav -o "%(title)s.%(ext)s" "{url}"
```

### 第 2 步：使用 ffmpeg 预处理音频

**始终进行预处理。** 此步骤对质量和速度至关重要。

```bash
# Extract audio from video (or re-encode audio) to ASR-optimal format
ffmpeg -i "{input}" \
  -vn \
  -ac 1 \
  -ar 16000 \
  -acodec pcm_s16le \
  -af "highpass=f=80,lowpass=f=8000,loudnorm=I=-16:TP=-1.5:LRA=11" \
  "{output_stem}_preprocessed.wav"
```

参数说明：

- `-vn` — 移除视频
- `-ac 1` — 单声道（立体声会浪费处理时间，对 ASR 没有好处）
- `-ar 16000` — 16kHz（whisper 内部期望的采样率）
- `-acodec pcm_s16le` — 16 位 WAV
- `highpass=f=80` — 去除语音频率范围以下的低频轰鸣
- `lowpass=f=8000` — 去除语音频率范围以上的嘶声
- `loudnorm` — 标准化音量（对于音量变化较大的录音至关重要）

**预处理后检查时长：**

```bash
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "{preprocessed_file}" | cut -d. -f1)
echo "Duration: ${DURATION}s ($((DURATION / 3600))h $(((DURATION % 3600) / 60))m)"
```

### 第 3 步：处理长文件（>30 分钟）

对于超过 30 分钟的文件，请执行静音检测和分块。这对于 1–8 小时的录音尤其重要。

#### 3a：静音分析

```bash
# Detect silent regions (informational — see what we're working with)
ffmpeg -i "{preprocessed_file}" \
  -af silencedetect=noise=-30dB:d=2.0 \
  -f null - 2>&1 | grep -c "silence_end"
# Shows number of silence gaps >= 2 seconds
```

静音阈值指南：

- `-30dB` — 干净的录音（录音棚、播客）
- `-35dB` — 中等背景噪声
- `-40dB` — 嘈杂环境

#### 3b：对于本地后端（whisper、whisperx、faster-whisper）

本地后端可以原生处理长文件——无需分块。但应使用 VAD 跳过静音：

**使用 faster-whisper（内置 VAD）：**

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "preprocessed.wav",
    language="en",
    word_timestamps=True,
    vad_filter=True,
    vad_parameters=dict(
        min_silence_duration_ms=1000,
        speech_pad_ms=400,
        threshold=0.5,
    ),
    condition_on_previous_text=False,  # prevents hallucination cascades on long files
)
```

**使用 whisper CLI（没有内置 VAD——在预处理中移除静音）：**

```bash
# Remove silences longer than 2s, keeping 0.3s padding
ffmpeg -i "{preprocessed_file}" \
  -af "silenceremove=start_periods=1:start_threshold=-30dB:stop_periods=-1:stop_duration=2.0:stop_threshold=-30dB" \
  "{output_stem}_trimmed.wav"

# Then transcribe the trimmed file
whisper "{output_stem}_trimmed.wav" --model turbo --language en \
  --condition_on_previous_text False \
  --word_timestamps True \
  --output_format json \
  --output_dir ./
```

**长文件的重要注意事项：** 对超过 30 分钟的文件使用 whisper 时，始终添加 `--condition_on_previous_text False`。如果不添加，一次幻觉就可能形成连锁反应，破坏数小时的转录内容（whisper 会无休止地重复同一句话）。

#### 3c：对于云端 API（25MB 文件大小限制）

云端 API（OpenAI、Groq）的限制为 25MB。请先压缩，必要时再分块。

```bash
# Compress to opus (smallest format for speech) — 1 hour ≈ 14MB
ffmpeg -i "{preprocessed_file}" -ac 1 -ar 16000 -c:a libopus -b:a 32k "{output_stem}.ogg"

# Check file size
SIZE_MB=$(du -m "{output_stem}.ogg" | cut -f1)
echo "File size: ${SIZE_MB}MB"
```

如果压缩后的文件小于 25MB，请直接发送。否则，在静音边界处分块：

```bash
# Split into ~20-minute chunks on silence boundaries
# (under 25MB each at opus 32kbps)
ffmpeg -i "{output_stem}.ogg" \
  -f segment \
  -segment_time 1200 \
  -c copy \
  "{output_stem}_chunk_%03d.ogg"
```

对于每个分块，请记录起始偏移量，以便校正时间戳：

```bash
# Get duration of each chunk for timestamp reassembly
for f in {output_stem}_chunk_*.ogg; do
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "$f: ${dur}s"
done
```

### 第 4 步：转录

#### 后端：whisper（默认）

```bash
whisper "{input_file}" \
  --model turbo \
  --language en \
  --output_format json \
  --output_dir "{output_dir}" \
  --word_timestamps True \
  --condition_on_previous_text False \
  --fp16 False
```

Apple Silicon 的模型选择（CPU——无 CUDA）：

- `turbo` — 速度与质量的最佳平衡（推荐默认值）
- `large-v3` — 质量最高，比 turbo 慢 2–3 倍
- `medium.en` — 更快，仅支持英语，适合清晰语音
- `small.en` — 速度快，处理干净录音时质量可接受
- `base.en` — 最快，仅用于快速预览

注意：在 CPU（没有 MLX 的 Apple Silicon）上必须使用 `--fp16 False`。Whisper 默认使用 fp16，而它仅适用于 CUDA。

#### 后端：whisperx（含说话人分离）

```bash
whisperx "{input_file}" \
  --model large-v3 \
  --language en \
  --diarize \
  --min_speakers 2 \
  --max_speakers 6 \
  --hf_token "{HF_TOKEN}" \
  --compute_type int8 \
  --output_dir "{output_dir}" \
  --output_format json
```

如果没有可用的 HF 令牌，whisperX 仍可用于转录和词语对齐，只是不会进行说话人分离：

```bash
whisperx "{input_file}" \
  --model large-v3 \
  --language en \
  --compute_type int8 \
  --output_dir "{output_dir}" \
  --output_format json
```

#### 后端：faster-whisper（Python，最适合长文件）

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "{input_file}",
    language="en",
    beam_size=5,
    word_timestamps=True,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=1000),
    condition_on_previous_text=False,
)

for segment in segments:
    print(f"[{segment.start:.2f} -> {segment.end:.2f}] {segment.text}")
```

#### 后端：insanely-fast-whisper（GPU 批处理）

```bash
insanely-fast-whisper \
  --file-name "{input_file}" \
  --model-name openai/whisper-large-v3-turbo \
  --task transcribe \
  --language en \
  --batch-size 24 \
  --timestamp word \
  --transcript-path "{output_stem}.json"
```

#### 后端：whisper.cpp（在 Apple Silicon 上使用 Metal 加速）

```bash
# Download model if needed
whisper-cpp-download-model large-v3

# Transcribe with Metal GPU acceleration
whisper-cpp \
  -m ~/.local/share/whisper-cpp/ggml-large-v3.bin \
  -f "{preprocessed_wav}" \
  -l en \
  -t 8 \
  --output-json \
  --print-progress
```

注意：whisper.cpp 要求输入为 WAV（不能是 mp3/ogg）。始终先预处理为 WAV。

#### 后端：OpenAI API

```bash
curl -s https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F file="@{input_file}" \
  -F model="gpt-4o-transcribe" \
  -F language="en" \
  -F response_format="verbose_json" \
  -F 'timestamp_granularities[]=word' \
  -F 'timestamp_granularities[]=segment' \
  > "{output_stem}_openai.json"
```

对于多个分块，请循环处理并偏移时间戳：

```bash
OFFSET=0
for chunk in {output_stem}_chunk_*.ogg; do
  curl -s https://api.openai.com/v1/audio/transcriptions \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -F file="@$chunk" \
    -F model="gpt-4o-transcribe" \
    -F language="en" \
    -F response_format="verbose_json" \
    -F 'timestamp_granularities[]=segment' \
    > "${chunk%.ogg}_transcript.json"

  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$chunk")
  OFFSET=$(echo "$OFFSET + $DUR" | bc)
done
```

#### 后端：Groq API（最便宜的云端方案）

格式与 OpenAI 兼容，但基础 URL 不同：

```bash
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F file="@{input_file}" \
  -F model="whisper-large-v3-turbo" \
  -F language="en" \
  -F response_format="verbose_json" \
  -F 'timestamp_granularities[]=word' \
  -F 'timestamp_granularities[]=segment' \
  > "{output_stem}_groq.json"
```

#### 后端：Deepgram（云端，原生说话人分离）

```bash
curl -s -X POST "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&diarize=true&language=en&utterances=true" \
  -H "Authorization: Token $DEEPGRAM_API_KEY" \
  -H "Content-Type: audio/wav" \
  --data-binary "@{input_file}" \
  > "{output_stem}_deepgram.json"
```

#### 后端：AssemblyAI（云端，原生说话人分离和章节）

```python
import assemblyai as aai
aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]

config = aai.TranscriptionConfig(
    speaker_labels=True,
    language_code="en",
    auto_chapters=True,
    word_boost=["custom", "vocabulary", "terms"],
)

transcript = aai.Transcriber().transcribe("{input_file}", config=config)

for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")
```

#### 后端：Gemini（灵活，基于提示词）

```python
import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")
audio = genai.upload_file("{input_file}")

response = model.generate_content([
    audio,
    """Transcribe this audio verbatim. Format as markdown with:
    - Timestamps every ~30 seconds as ### headers (e.g., ### [00:01:30])
    - Speaker labels if you can distinguish voices (Speaker 1, Speaker 2, etc.)
    - Paragraph breaks at natural topic shifts
    Do not summarize or omit anything. Transcribe every word spoken."""
])

print(response.text)
```

注意：Gemini 原生支持最长约 9.5 小时的文件（无需分块），但时间戳为近似值，输出是由提示词塑造的非结构化文本。

### 第 5 步：格式化输出

用户的默认偏好是**采用 Markdown 格式的纯文本**。请将后端的原始输出转换为此格式。

#### 默认：Markdown 文字稿

```markdown
# Transcript: {filename}

**Date transcribed:** {date}
**Duration:** {duration}
**Backend:** {backend}
**Model:** {model}

***

## [00:00:00]

{text of first segment or group of segments...}

## [00:05:23]

{text continues with periodic timestamp headers...}

***

*Transcribed with {backend} ({model})*
```

**格式规则：**

- 每隔 2–5 分钟插入一次 `## [HH:MM:SS]` 时间戳标题（不要每个片段都插入——那样太嘈杂）
- 将同一说话人的连续片段合并为段落
- 如果可以进行说话人分离，请添加粗体说话人标签前缀：`**Speaker 1:** text...`
- 在主题发生重大转变或出现长时间停顿（>10 秒）时使用 `***` 水平分隔线
- 在自然的句子边界处保留段落分隔

#### 含说话人分离：

```markdown
# Transcript: {filename}

**Speakers:** 3 detected
**Duration:** 1h 23m

***

## [00:00:00]

**Speaker 1:** Welcome everyone to today's session. We're going to be talking about...

**Speaker 2:** Thanks for having me. I'm excited to share...

## [00:05:12]

**Speaker 1:** Let's dive into the first topic...
```

#### 其他输出格式

如果用户请求其他格式：

**SRT 字幕：**

```bash
whisper "{input}" --model turbo --output_format srt --output_dir ./
```

**VTT 字幕：**

```bash
whisper "{input}" --model turbo --output_format vtt --output_dir ./
```

**含词级时间戳的 JSON：**

```bash
whisper "{input}" --model turbo --output_format json --word_timestamps True --output_dir ./
```

**纯文本（无时间戳）：**

```bash
whisper "{input}" --model turbo --output_format txt --output_dir ./
```

**TSV（制表符分隔，用于电子表格）：**

```bash
whisper "{input}" --model turbo --output_format tsv --output_dir ./
```

## 自定义词汇 / 提示词提示

Whisper 支持使用 `initial_prompt` 引导模型偏向特定术语：

```bash
whisper "{input}" --model turbo --language en \
  --initial_prompt "This conversation discusses Kubernetes, GitLab CI/CD, Terraform, and Infrastructure as Code. Names mentioned: Sid Sijbrandij, David Thompson."
```

对于云端 API：

```bash
# OpenAI - use the prompt parameter
curl ... -F prompt="Technical terms: LLM, RAG, vector database, embeddings. Names: Sid Sijbrandij."

# AssemblyAI - use word_boost
config = aai.TranscriptionConfig(
    word_boost=["Kubernetes", "GitLab", "Sijbrandij", "Terraform"],
    boost_param="high",
)

# Deepgram - use keywords
curl ... "https://api.deepgram.com/v1/listen?keywords=Kubernetes:2&keywords=GitLab:2"
```

**何时使用自定义词汇：**

- 专有名词（人物、公司、产品）
- 领域特定术语
- 可能被听错的缩写（例如，“RAG”和“rag”）
- 英语语音中的非英语词语

## 处理特定输入类型

### 含片头/片尾音乐的播客

音乐片段会导致幻觉。请将其裁剪掉：

```bash
# Skip first 30s (intro music) and last 30s (outro)
TOTAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp3 | cut -d. -f1)
END=$((TOTAL - 30))
ffmpeg -i input.mp3 -ss 30 -to $END -ac 1 -ar 16000 -acodec pcm_s16le trimmed.wav
```

### 多轨录音（各说话人使用独立麦克风）

如果每个说话人都有自己的音轨：

```bash
# Extract each track
ffmpeg -i recording.mkv -map 0:a:0 -ac 1 -ar 16000 speaker1.wav
ffmpeg -i recording.mkv -map 0:a:1 -ac 1 -ar 16000 speaker2.wav

# Transcribe each separately (no diarization needed)
whisper speaker1.wav --model turbo --output_format json
whisper speaker2.wav --model turbo --output_format json

# Then interleave by timestamps in the markdown output
```

### 立体声录音（左/右声道分别对应不同说话人）

```bash
# Split channels
ffmpeg -i stereo.wav -af "pan=mono|c0=FL" -ar 16000 left.wav
ffmpeg -i stereo.wav -af "pan=mono|c0=FR" -ar 16000 right.wav

# Transcribe each channel as a separate speaker
```

### 来自 URL 的视频（下载并转录）

```bash
# Download audio only
yt-dlp -x --audio-format wav -o "%(title)s.%(ext)s" "{url}"

# Then run the standard preprocessing + transcription pipeline
```

## 故障排除

### Whisper 无休止地重复同一句话

这是幻觉连锁问题。解决方法：使用 `--condition_on_previous_text False`。如果已经设置，输入中可能存在长时间静音或音乐——请进行静音移除预处理。

### 在 Apple Silicon 上速度非常慢

Whisper 的 Python 实现无法很好地利用 Metal/MPS。可选方案：

- 使用 `whisper.cpp` 获得 Metal GPU 加速
- 使用 `--model turbo` 替代 `large-v3`（速度快 2–3 倍，质量损失很小）
- 对仅含英语的内容使用 `--model medium.en`（速度快 4–5 倍）
- 使用 Groq API（数秒即可转录数小时内容，几乎免费）

### 内存不足

- 使用 `compute_type="int8"` 的 `faster-whisper`（内存占用减半）
- 使用更小的模型（`medium` 或 `small`）
- 对文件进行分块（参见第 3c 步）

### pip install 失败并显示“externally-managed-environment”

现代 macOS Python（Homebrew）要求使用：

```bash
pip3 install --break-system-packages {package}
```

### 词级时间戳不准确

Whisper 原生的词级时间戳是近似值。如需精确的词级时间定位，请使用 whisperX，它会添加强制音素对齐。

### 外语或口音问题

- 省略 `--language`，让 whisper 自动检测
- 使用 `large-v3`（最佳多语言模型）
- 使用包含目标语言示例文本的 `--initial_prompt`
- 对于语码转换（一段录音中包含多种语言），Gemini 的处理效果优于 Whisper

## 后端比较速查表

| 后端 | 安装 | 说话人分离 | VAD | 速度（1 小时文件，Apple Silicon） | 成本 |
|---------|---------|-------------|-----|-------------------------------|------|
| whisper | `pip install openai-whisper` | 否 | 否 | 约 20–40 分钟（turbo） | 免费 |
| whisperx | `pip install whisperx` | 是（pyannote） | 是 | 约 15–30 分钟 | 免费 |
| faster-whisper | `pip install faster-whisper` | 否 | 是（Silero） | 约 10–20 分钟 | 免费 |
| insanely-fast-whisper | `pip install insanely-fast-whisper` | 实验性 | 否 | 约 5–10 分钟（GPU） | 免费 |
| whisper.cpp | `brew install whisper-cpp` | 基础 | 否 | 约 10–15 分钟（Metal） | 免费 |
| OpenAI API | API 密钥 | 否 | 不适用 | 约 1–2 分钟 | $0.006/分钟 |
| Groq API | API 密钥 | 否 | 不适用 | 约数秒 | $0.00004/分钟 |
| Deepgram | API 密钥 | 是（原生） | 不适用 | 约 1–2 分钟 | $0.0043/分钟 |
| AssemblyAI | API 密钥 | 是（原生） | 不适用 | 约 2–5 分钟 | $0.0062/分钟 |
| Gemini | API 密钥 | 通过提示词 | 不适用 | 约 1–3 分钟 | 按令牌计费 |
