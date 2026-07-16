<!-- source-sha256: b7085574c6bf72e07c578db14316682b9ebf1e841d9db62916d284efd84c96cc -->
---
name: baoyu-youtube-transcript
description: 通过 URL 或视频 ID 下载 YouTube 视频的转录文本/字幕和封面图片。支持多种语言、翻译、章节和说话人识别。缓存原始数据，以便快速重新格式化。当用户要求“获取 YouTube 转录文本”“下载字幕”“获取字幕”“YouTube字幕”“YouTube封面”“视频封面”“视频缩略图”“视频封面图片”，或提供 YouTube URL 并希望提取转录文本、字幕文本或封面图片时使用。
version: 1.1.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-youtube-transcript
    requires:
      anyBins:
        - bun
        - npx
---

# YouTube 转录文本

从 YouTube 视频下载转录文本（字幕）。支持人工创建和自动生成的转录文本。无需 API 密钥或浏览器——直接使用 YouTube 的 InnerTube API，并在 YouTube 阻止直接 API 路径时自动回退到 `yt-dlp`。

首次运行时获取视频元数据和封面图片，并缓存原始数据，以便快速重新格式化。

## 脚本目录

脚本位于 `scripts/` 子目录中。`{baseDir}` = 此 SKILL.md 所在目录的路径。解析 `${BUN_X}` 运行时：如果已安装 `bun` → `bun`；如果 `npx` 可用 → `npx -y bun`；否则建议安装 bun。将 `{baseDir}` 和 `${BUN_X}` 替换为实际值。

| 脚本 | 用途 |
|--------|---------|
| `scripts/main.ts` | 转录文本下载 CLI |

## 用法

```bash
# 默认：带时间戳的 Markdown（英语）
${BUN_X} {baseDir}/scripts/main.ts <youtube-url-or-id>

# 指定语言（按优先级排序）
${BUN_X} {baseDir}/scripts/main.ts <url> --languages zh,en,ja

# 不带时间戳
${BUN_X} {baseDir}/scripts/main.ts <url> --no-timestamps

# 按章节分段
${BUN_X} {baseDir}/scripts/main.ts <url> --chapters

# 识别说话人（需要 AI 后处理）
${BUN_X} {baseDir}/scripts/main.ts <url> --speakers

# SRT 字幕文件
${BUN_X} {baseDir}/scripts/main.ts <url> --format srt

# 翻译转录文本
${BUN_X} {baseDir}/scripts/main.ts <url> --translate zh-Hans

# 列出可用的转录文本
${BUN_X} {baseDir}/scripts/main.ts <url> --list

# 强制重新获取（忽略缓存）
${BUN_X} {baseDir}/scripts/main.ts <url> --refresh
```

## 选项

| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `<url-or-id>` | YouTube URL 或视频 ID（允许多个） | 必填 |
| `--languages <codes>` | 以逗号分隔、按优先级排列的语言代码 | `en` |
| `--format <fmt>` | 输出格式：`text`、`srt` | `text` |
| `--translate <code>` | 翻译为指定的语言代码 | |
| `--list` | 列出可用的转录文本，而不获取内容 | |
| `--timestamps` | 每段包含 `[HH:MM:SS → HH:MM:SS]` 时间戳 | 开启 |
| `--no-timestamps` | 禁用时间戳 | |
| `--chapters` | 根据视频描述进行章节分段 | |
| `--speakers` | 输出带有说话人识别元数据的原始转录文本 | |
| `--exclude-generated` | 跳过自动生成的转录文本 | |
| `--exclude-manually-created` | 跳过人工创建的转录文本 | |
| `--refresh` | 强制重新获取，忽略缓存数据 | |
| `-o, --output <path>` | 保存到指定文件路径 | 自动生成 |
| `--output-dir <dir>` | 输出的基础目录 | `youtube-transcript` |

## 可选环境变量

| 变量 | 说明 |
|----------|-------------|
| `YOUTUBE_TRANSCRIPT_COOKIES_FROM_BROWSER` | 回退期间传递给 `yt-dlp --cookies-from-browser`，例如 `chrome`、`safari`、`firefox` 或 `chrome:Profile 1` |

## 输入格式

接受以下任意一种视频输入格式：

- 完整 URL：`https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- 短 URL：`https://youtu.be/dQw4w9WgXcQ`
- 嵌入 URL：`https://www.youtube.com/embed/dQw4w9WgXcQ`
- Shorts URL：`https://www.youtube.com/shorts/dQw4w9WgXcQ`
- 视频 ID：`dQw4w9WgXcQ`

## 输出格式

| 格式 | 扩展名 | 说明 |
|--------|-----------|-------------|
| `text` | `.md` | 包含 frontmatter（包括 `description`）、标题、摘要以及可选目录/封面/时间戳/章节/说话人的 Markdown |
| `srt` | `.srt` | 供视频播放器使用的 SubRip 字幕格式 |

## 输出目录

```
youtube-transcript/
├── .index.json                          # 视频 ID → 目录路径映射（用于缓存查找）
└── {channel-slug}/{title-full-slug}/
    ├── meta.json                        # 视频元数据（标题、频道、描述、时长、章节等）
    ├── transcript-raw.json              # 来自 YouTube API 的原始转录文本片段（已缓存）
    ├── transcript-sentences.json        # 按句子分段的转录文本（按标点拆分，并跨片段合并）
    ├── imgs/
    │   └── cover.jpg                    # 视频缩略图
    ├── transcript.md                    # Markdown 转录文本（根据句子生成）
    └── transcript.srt                   # SRT 字幕（根据原始片段生成，如果使用 --format srt）
```

- `{channel-slug}`：采用 kebab-case 格式的频道名称
- `{title-full-slug}`：采用 kebab-case 格式的完整视频标题

`--list` 模式仅输出到 stdout（不保存文件）。

## 缓存

首次获取时，脚本会保存：

- `meta.json` — 视频元数据、章节、封面图片路径、语言信息
- `transcript-raw.json` — 来自 YouTube API 的原始转录文本片段（`{ text, start, duration }[]`）
- `transcript-sentences.json` — 按句子分段的转录文本（`{ text, start: "HH:mm:ss", end: "HH:mm:ss" }[]`），按句末标点（`.?!…。？！` 等）拆分，时间戳根据字符长度按比例分配，并以识别 CJK 文本的方式合并
- `imgs/cover.jpg` — 视频缩略图

后续对同一视频的运行将使用缓存数据（不发起网络调用）。使用 `--refresh` 强制重新获取。如果请求了不同的语言，缓存将自动刷新。

当 YouTube 在直接 InnerTube 路径上返回反机器人/阻止响应时，脚本会使用备用客户端身份重试，然后在 `yt-dlp` 可用时回退到该工具。如果需要回退但 `yt-dlp` 不可用，代理应自行决定如何使 `yt-dlp` 可用并继续执行，而不是将安装决定推给用户。

SRT 输出（`--format srt`）根据 `transcript-raw.json` 生成。文本/Markdown 输出使用 `transcript-sentences.json`，以获得自然的句子边界。

## 工作流程

当用户提供 YouTube URL 并希望获取转录文本时：

1. 如果用户尚未指定语言，先使用 `--list` 运行，以显示可用选项
2. 运行脚本时，**始终使用单引号包裹 URL**——zsh 会将 `?` 视为 glob 通配符，因此未加引号的 YouTube URL 会导致“no matches found”：请使用 `'https://www.youtube.com/watch?v=ID'`
3. 默认使用 `--chapters --speakers` 运行，以获得最丰富的输出（章节 + 说话人识别）
3. 脚本会自动保存缓存数据和输出文件，并打印文件路径
4. 对于 `--speakers` 模式：脚本保存原始文件后，按照下方的说话人识别工作流程进行后处理并添加说话人标签

当用户只需要封面图片或元数据时，使用任意选项运行脚本也会缓存 `meta.json` 和 `imgs/cover.jpg`。

重新格式化同一视频时（例如先输出文本，再输出 SRT），会复用缓存数据——无需重新获取。

## 章节与说话人工作流程

### 章节（`--chapters`）

脚本从视频描述中解析章节时间戳（例如 `0:00 Introduction`），根据章节边界对转录文本进行分段，将片段分组为易于阅读的段落，并以带目录的 `.md` 格式保存。无需进一步处理。

如果描述中没有章节时间戳，转录文本将以分组段落的形式输出，不包含章节标题。

### 说话人识别（`--speakers`）

说话人识别需要 AI 处理。脚本会输出一个原始 `.md` 文件，其中包含：

- 带有视频元数据（标题、频道、日期、封面、描述、语言）的 YAML frontmatter
- 视频描述（用于提取说话人姓名）
- 描述中的章节列表（如果可用）
- SRT 格式的原始转录文本（预先计算开始/结束时间戳，节省 token）

脚本保存原始文件后，生成一个子代理（使用 Sonnet 等较便宜的模型以提高成本效益）来处理说话人识别：

1. 读取已保存的 `.md` 文件
2. 读取 `{baseDir}/prompts/speaker-transcript.md` 中的提示词模板
3. 按照提示词处理原始转录文本：
   - 使用视频元数据识别说话人（标题 → 嘉宾、频道 → 主持人、描述 → 姓名）
   - 根据对话流程、问答模式和上下文线索检测说话人切换
   - 划分章节（如果描述中有章节则使用，否则根据主题变化创建）
   - 使用 `**说话人姓名：**` 标签、段落分组（2-4 句）和 `[HH:MM:SS → HH:MM:SS]` 时间戳进行格式化
4. 使用处理后的转录文本覆盖 `.md` 文件（保留 YAML frontmatter）

使用 `--speakers` 时隐含启用 `--chapters`——处理后的输出始终包含章节分段。

## 错误情况

| 错误 | 含义 |
|-------|---------|
| Transcripts disabled | 视频完全没有字幕 |
| No transcript found | 请求的语言不可用 |
| Video unavailable | 视频已删除、设为私有或受地区限制 |
| IP blocked | 请求次数过多，请稍后重试 |
| Age restricted | 视频需要登录以进行年龄验证 |
| bot detected | 脚本会尝试备用客户端，然后尝试 `yt-dlp`；如果缺少回退工具，代理应自行解决，否则如果仍然失败，请尝试 `YOUTUBE_TRANSCRIPT_COOKIES_FROM_BROWSER=safari`（或你的浏览器） |
