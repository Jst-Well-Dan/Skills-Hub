<!-- source-sha256: e9c0d762c8e87beda71d313c555a86871dc947ebc39d0b5cf86acfafb35c38e4 -->
---
name: multimodal-extraction
description: "给定本地视频或视频 URL，在需要时下载媒体，提取幻灯片帧和关键时刻，转录音频，并编写一个 Markdown 时间线，将截图与对应时间戳处的转录文本交错排列。适用于将视频转换为多模态笔记文件、与幻灯片同步的转录稿、带截图的转录稿，或包含图片的演讲回顾。"
version: 0.1.0
---

# 多模态提取

## 概述

此技能将现有的视频工作流组合成一个产物：

- `download-video` 用于 URL 输入
- `thumbnail-extraction` 用于幻灯片帧和关键截图
- `transcribe-anything` 用于转录策略

此实现有意优先追求速度：

1. 仅当输入为 URL 时才下载
2. 复用 `thumbnail-extraction` 中快速的幻灯片/关键帧启发式方法
3. 使用本地 `whisper` JSON 输出生成带时间戳的转录片段
4. 将所有内容合并为一个使用相对图片链接的 Markdown 时间线

## 何时使用

- “将这场演讲转换为多模态笔记”
- “为我制作一份带截图的 Markdown 转录稿”
- “同时提取幻灯片和转录文本”
- “根据这个视频制作一份回顾文档”
- “给定这个 YouTube URL，生成一份与幻灯片同步的转录稿”

## 要求

```bash
brew install ffmpeg yt-dlp
pip3 install --break-system-packages openai-whisper
```

将复用以下现有本地脚本：

- `../thumbnail-extraction/thumbnail_extractor.py`

## 命令

```bash
python3 multimodal_extract.py <video_or_url> [output_dir] [--language en] [--whisper-model turbo] [--top-n 4]
```

## 功能说明

### 第 1 步：解析来源

- 如果输入是本地文件，则直接使用
- 如果输入以 `http://` 或 `https://` 开头，则先使用 `yt-dlp` 下载
- 对于 YouTube URL，直接使用 `yt-dlp` 通常就足够了
- 对于处理起来更棘手的托管页面，此技能遵循与 `download-video` 相同的实用目标：先获得一个可用的本地文件

### 第 2 步：提取视觉锚点

运行：

```bash
python3 ../thumbnail-extraction/thumbnail_extractor.py "$VIDEO" "$OUTPUT/visuals" 4 --extract-slides
```

这会生成：

- `visuals/` 根目录中的最佳缩略图候选项
- `visuals/slides/` 中的幻灯片图片
- 带时间戳的清单文件

### 第 3 步：转录

提取经过标准化处理的单声道 16k 音频：

```bash
ffmpeg -y -i "$VIDEO" -vn -ac 1 -ar 16000 -acodec pcm_s16le \
  -af "highpass=f=80,lowpass=f=8000,loudnorm=I=-16:TP=-1.5:LRA=11" \
  "$OUTPUT/audio/source_preprocessed.wav"
```

然后使用 Whisper 进行转录：

```bash
whisper "$OUTPUT/audio/source_preprocessed.wav" \
  --model turbo \
  --language en \
  --word_timestamps True \
  --condition_on_previous_text False \
  --output_format json \
  --output_dir "$OUTPUT/transcript"
```

### 第 4 步：合并到 Markdown

该脚本会：

- 读取幻灯片和缩略图清单
- 读取 Whisper 转录片段
- 按时间戳对所有视觉锚点排序
- 对相邻视觉锚点之间的转录文本进行分组
- 写入 `multimodal_timeline.md`，其中包含：
  - 章节时间戳
  - 关联图片
  - 对应时间区间内的转录文本

## 输出

```
output_dir/
  source/
  visuals/
  audio/
  transcript/
  multimodal_timeline.md
```

## 设计原则

目标是实现端到端提取的整体速度最大化。

这意味着：

- 优先使用启发式方法
- 默认使用本地转录
- 常规流程中不使用 VLM
- 只提供足以让 Markdown 产物立即可用的结构

## 未来扩展

- 为 `transcribe-anything` 添加后端切换功能
- 当存在源幻灯片文稿时，添加可感知文稿结构的幻灯片标注
- 添加说话人分离章节
- 在 Markdown 时间线之上添加章节划分或摘要生成功能
