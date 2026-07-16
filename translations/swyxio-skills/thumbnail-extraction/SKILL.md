<!-- source-sha256: 4d026b621e955d0969791f9479760362a8188d650477f27c5b59d42b9a0293c1 -->
---
name: thumbnail-extraction
description: "从视频文件中提取最有趣的帧，用于合成缩略图。检测人脸、表情、微笑和演示文稿幻灯片。输出完整帧、人脸裁剪图和透明抠图。当用户要求提取缩略图、查找有趣的帧、从视频中截取画面或从录像中创建缩略图候选素材时使用。"
version: 0.1.0
---

# 视频缩略图提取

## 概述
自动扫描本地 MP4 视频（或通过 yt-dlp 获取的 YouTube URL），提取视觉上最有趣的 4 帧——优先选择表情丰富的人脸（笑出声、震惊、微笑）和引人注目的演示文稿幻灯片。输出完整帧、人脸裁剪图和已移除背景、可直接用于合成的透明 PNG。

## 使用场景
- 创建 YouTube 缩略图之前（作为 `youtube-thumbnails` skill 的输入）
- 需要从较长的视频录像中获取最佳截图时
- 合成缩略图且需要嘉宾的透明抠图时
- 处理 Zoom 画廊视图录像、访谈或演示文稿时

## 依赖项

### Python 包（仅需安装一次）
```bash
# In sandbox (Cowork VM):
pip install opencv-python scenedetect deepface pillow numpy --break-system-packages

# On host Mac (for background removal — sandbox can't download the model):
pip3 install 'rembg[cpu]' pillow --break-system-packages
```

### 系统工具
- `ffmpeg`（通常已预装）
- `python3`（3.10+）
- `yt-dlp`（可选，用于 YouTube URL）：`pip install yt-dlp --break-system-packages`

### 模型下载（首次运行）
- **DeepFace 表情模型**（约 1MB）：首次使用时自动下载。如果受到代理限制，表情检测会回退到 OpenCV 微笑级联分类器（仍然有效）。
- **rembg u2net 模型**（约 176MB）：首次使用时下载。如果沙盒阻止访问 GitHub Releases，则必须在宿主 Mac 上运行。

## 流水线架构

### 两阶段设计（节省内存）

**阶段 1 — 快速扫描**（仅使用 OpenCV，不使用深度学习）
- 每隔 10 秒从视频中采样一帧
- 跳过开头和结尾各 60 秒（片头/片尾）
- 对每一帧：
  - 通过 Haar 级联分类器检测人脸（速度快，无需 GPU）
  - 在人脸区域内检测微笑
  - 计算视觉方差（作为“有趣”内容的近似指标）
  - 检测演示文稿幻灯片（高边缘密度 + 低色彩饱和度）
- 根据以下指标为每一帧评分：人脸数量、微笑数量、微笑大小、视觉方差
- 使用**象限系统**选择得分最高且具有多样性的 12 个候选帧：将视频划分为 N 个时间段，从每个时间段中选择最佳帧 → 确保时间分布均匀

**阶段 2 — 深度分析**（使用 DeepFace，仅分析排名前 12 的候选帧）
- 仅从视频中重新读取选中的帧
- 运行 DeepFace 情绪检测（happy、surprise、fear、sad、angry、disgust、neutral）
- 根据缩略图价值为情绪加权：happy > surprise > fear > angry > sad > neutral
- 将阶段 1 的分数与表情分数相结合
- 最终选择：将候选帧划分到 N 个时间段中，从每个时间段中选择最佳帧 → 保证覆盖整个视频

**阶段 3 — 输出**（使用 rembg，仅处理最终的 4 帧）
- 将完整帧保存为 JPG（95% 质量）
- 以充足的边距（0.5x）裁剪检测到的最大人脸
- 对人脸裁剪图运行背景移除 → 透明 PNG
- 生成包含元数据的清单 JSON

### 评分启发式规则

| 信号 | 权重 | 说明 |
|--------|--------|-------|
| 检测到人脸 | 每张人脸 +2.0（上限 3 张） | 画廊视图得分较高 |
| 检测到微笑 | 每个微笑 +3.0 | 基于级联分类器，无需模型 |
| 微笑尺寸比例 | +5.0 × 比例 | 微笑越明显 = 表情越丰富 |
| 多人画面 | 额外 +1.0 | 2 张以上人脸 = 更具吸引力 |
| 开心表情 | 额外 +2.0（阶段 2） | 最适合缩略图 |
| 惊讶表情 | 额外 +2.0（阶段 2） | 引人注目 |
| 恐惧/愤怒表情 | 额外 +1.0（阶段 2） | “震惊”反应 |
| 视觉方差 | +0.0–1.5 | 根据画面复杂度归一化 |
| 演示文稿幻灯片 | 基准分 1.5 | 适用于幻灯片截图 |

### 时间多样性算法

流水线强制候选帧在时间上分散，以避免所选画面集中在同一片段：

1. **象限选择**（阶段 1 → 阶段 2）：将视频时长划分为 N 个时间段，从每个时间段中选择得分最高的帧
2. **强制分段选择**（阶段 2 → 最终结果）：将排名靠前的候选帧划分到 `top_n` 个等长时间段中，从每个时间段中选择最佳帧
3. 回退方案：如果某个时间段为空，则按全局最高分补充

这可以确保一段 76 分钟的视频从不同部分选取画面（例如 1:00、2:10、21:50、48:50），而不是集中在人物画面最多的片段中。

## 用法

### 命令行
```bash
python3 thumbnail_extractor.py <video_path> [output_dir] [top_n]
```

**参数：**
- `video_path` — MP4 文件路径（必需）
- `output_dir` — 输出保存位置（默认：`~/Downloads/thumb_candidates`）
- `top_n` — 要提取的候选素材数量（默认：4）

**示例：**
```bash
# Basic — extract 4 best frames
python3 thumbnail_extractor.py "GMT20260130-210038_Recording_gallery_2380x1544.mp4"

# Custom output dir and count
python3 thumbnail_extractor.py recording.mp4 ./thumbs 6

# YouTube video (download first)
yt-dlp -o "video.mp4" "https://youtube.com/watch?v=..."
python3 thumbnail_extractor.py video.mp4
```

### 输出文件

流水线会为每个候选素材生成：

| 文件 | 格式 | 说明 |
|------|--------|-------------|
| `{name}_{n}_{emotion}_{timestamp}_full.jpg` | JPG 95% | 完整视频帧 |
| `{name}_{n}_{emotion}_{timestamp}_face.jpg` | JPG 95% | 带边距的人脸裁剪图 |
| `{name}_{n}_{emotion}_{timestamp}_transparent.png` | 带 alpha 通道的 PNG | 已移除背景的人脸抠图 |
| `{name}_manifest.json` | JSON | 所有候选素材的元数据 |

**命名示例：** `GMT20260130-210038_3_happy_2-10_full.jpg`
- `GMT20260130-210038` — 视频名称（Zoom 录像会截短）
- `3` — 候选素材编号（按分数排序）
- `happy` — 检测到的主要情绪
- `2-10` — 时间戳（2 分 10 秒）
- `full` / `face` / `transparent` — 文件类型

### 清单 JSON 结构
```json
{
  "video": "GMT20260130-210038",
  "candidates": [
    {
      "index": 1,
      "timestamp": "2:10",
      "timestamp_sec": 130.0,
      "emotion": "happy",
      "emotion_score": 0.85,
      "combined_score": 12.4,
      "num_faces": 3,
      "is_presentation": false,
      "files": {
        "full": "..._full.jpg",
        "face_crop": "..._face.jpg",
        "transparent": "..._transparent.png"
      }
    }
  ]
}
```

## 背景移除（独立步骤）

由于 Cowork 沙盒可能阻止模型下载，请在宿主 Mac 上运行 rembg：

```bash
# On host Mac (via osascript or Terminal)
cd ~/Downloads/thumb_candidates
python3 -c "
from rembg import remove
from PIL import Image
import glob, os

for f in sorted(glob.glob('*_face.jpg')):
    out = f.replace('_face.jpg', '_transparent.png')
    print(f'Processing {f}...')
    img = Image.open(f)
    result = remove(img)
    result.save(out)
    print(f'  -> {out} ({os.path.getsize(out)//1024}KB)')
"
```

在 Apple Silicon 上，每张图像大约需要 10–15 秒。u2net 模型会在首次运行时自动下载（约 176MB）。

## 与其他 Skill 集成

### 输入到 `youtube-thumbnails`
提取完成后，将透明 PNG 用作合成元素：
1. 从候选素材中选择最佳人脸抠图
2. 在 Gemini 缩略图提示词中将其用作参考，或者
3. 使用 ImageMagick 将其手动合成到 Gemini 生成的背景上：

```bash
# Composite transparent face onto Gemini-generated background
convert gemini_background.jpg transparent_face.png \
  -gravity southeast -geometry +50+50 \
  -composite final_thumbnail.jpg
```

### 流水线流程
```
[Video MP4] → thumbnail-extraction → [face crops + transparent PNGs]
                                          ↓
                                   youtube-thumbnails → [Gemini background]
                                          ↓
                                   [Composite final thumbnail]
```

## 调优参数

在 `thumbnail_extractor.py` 顶部编辑以下参数：

| 参数 | 默认值 | 效果 |
|-----------|---------|--------|
| `SAMPLE_INTERVAL_SEC` | 10 | 越小 = 扫描的帧越多，速度越慢 |
| `ANALYSIS_SCALE` | 0.5 | 越小 = 人脸检测越快，准确度越低 |
| `SCENE_THRESHOLD` | 27.0 | 越小 = 检测到的场景边界越多 |
| `MIN_FACE_CONFIDENCE` | 0.80 | 越高 = 误检的人脸越少 |
| `top_n` | 4 | 最终候选素材数量 |

对于较短的视频（<10 分钟），可考虑使用 `SAMPLE_INTERVAL_SEC=5`，以实现更精细的覆盖。

## 故障排除

- **OOM / 进程被终止**：v2 流水线在阶段 1 期间，内存中同时保存的帧永远不会超过 1 帧。如果仍然发生 OOM，请将 `SAMPLE_INTERVAL_SEC` 增加到 15–20。
- **所有情绪均为 "neutral"**：DeepFace 模型无法下载（受到代理限制）。阶段 1 的微笑检测仍然有效——请查看清单中的 `num_smiles` 字段。
- **人脸裁剪到了错误的人**：流水线会选择检测到的最大人脸。在屏幕共享模式下，这可能是头像，而不是摄像头中的人脸。请检查完整帧进行确认。
- **未检测到人脸**：使用“共享屏幕与画廊视图”的 Zoom 录像效果最佳。在单人演讲者视图中，人脸可能离镜头过近或过大，导致级联检测器无法识别——尝试将 `ANALYSIS_SCALE` 降低到 0.3。
- **背景移除瑕疵**：rembg 的 u2net 可能会在头发周围产生光晕。要获得更干净的效果，请尝试 `u2net_human_seg` 模型：`remove(img, model_name='u2net_human_seg')`。
- **处理速度慢**：一段 76 分钟的视频，阶段 1 大约需要 2 分钟，阶段 2（12 个候选帧）大约需要 15 秒，背景移除（4 张人脸）大约需要 60 秒。大部分时间都用于阶段 1 的扫描。
