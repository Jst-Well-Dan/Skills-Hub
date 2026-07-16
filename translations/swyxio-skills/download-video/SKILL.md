<!-- source-sha256: 63629c0e560d324047f8862a475b6bc64b22d3713b9e2cf3545df2323b6d6fb2 -->
---
name: download-video
description: |
  从网页下载嵌入式视频。获取页面，识别视频托管服务（Vimeo、YouTube 等），解析正确的嵌入/播放器 URL，然后使用 yt-dlp 下载。支持需要 referer 请求头或嵌入 URL 的私有/不公开列出视频。当有人说“下载这个视频”“保存这个视频”“从这个页面获取视频”“抓取这个视频”，或者提供一个 URL 并要求从中下载媒体时，请使用此技能。当有人粘贴包含嵌入式视频的页面 URL，并希望将视频文件保存到本地时，也应触发此技能。
license: MIT
compatibility: |
  需要安装了 yt-dlp 的 macOS 或 Linux（brew install yt-dlp）。建议安装 curl_cffi Python 包以支持模拟客户端（pip3 install curl_cffi）。需要互联网连接。
metadata:
  author: swyxio
  version: "1.1"
  last-updated: "2026-03-28"
  primary-tools: yt-dlp, WebFetch
---

# 下载视频

此技能通过检查页面源代码、识别视频托管服务和嵌入 URL，然后使用 yt-dlp 下载视频文件，从网页下载嵌入式视频。

## 为什么需要此技能

许多活动回放、网络研讨会和演讲通过私有/不公开列出的视频托管服务（尤其是 Vimeo）嵌入页面。直接视频 URL 通常会返回 404，因为只有通过带有正确 referer 的嵌入式播放器才能访问视频。此技能会自动处理这种情况。

## 前置条件

确保 yt-dlp 已安装并更新到最新版本（旧版本会遇到不同的错误）：

```bash
which yt-dlp || brew install yt-dlp
brew upgrade yt-dlp
```

安装客户端模拟库。在现代 macOS 上（Python 通过 Homebrew 安装），必须使用 `--break-system-packages` 标志：

```bash
pip3 install --break-system-packages curl_cffi
```

注意：仅安装 `curl_cffi` 并不能解决 Vimeo 私有视频的下载问题。真正有效的是嵌入 URL 方法（步骤 2）。但 `curl_cffi` 可以避免出现具有误导性的 OAuth 400 错误，以免它掩盖真正的问题。

## 如何使用此技能

### 步骤 1：获取页面并识别视频

使用 WebFetch 检查目标 URL。查找：

1. 指向视频播放器的 **iframe src** 属性
2. 包含直接媒体 URL 的 **video/source 标签**
3. **Schema.org VideoObject** 元数据（`contentUrl`、`embedUrl`）
4. 包含视频 URL 或配置对象的 **JavaScript 变量**
5. 播放器容器元素上的 **Data 属性**

提取视频托管服务以及所有识别信息：

| 托管服务 | URL 模式 | 嵌入模式 |
|---|---|---|
| Vimeo | `vimeo.com/{id}` | `player.vimeo.com/video/{id}` |
| YouTube | `youtube.com/watch?v={id}` | `youtube.com/embed/{id}` |
| Wistia | `fast.wistia.com/medias/{id}` | `fast.wistia.com/embed/medias/{id}` |
| Brightcove | 各不相同 | `players.brightcove.net/{account}/{player}/index.html?videoId={id}` |
| Loom | `loom.com/share/{id}` | `loom.com/embed/{id}` |

### 步骤 2：解析下载 URL

对于私有/不公开列出的视频，直接 URL（例如 `vimeo.com/123456`）通常会失败。请改用**嵌入/播放器 URL**：

- **Vimeo**：使用 `https://player.vimeo.com/video/{id}`，而不是 `https://vimeo.com/{id}`
- **YouTube**：直接 URL 通常有效，但嵌入 URL 也可以使用
- **Wistia**：使用带有媒体哈希值的嵌入 URL

如果视频包含隐私哈希值（Vimeo 的 `h=` 参数），请将其包括在内：
```
https://player.vimeo.com/video/{id}?h={hash}
```

### 步骤 3：使用 yt-dlp 下载

对于 Vimeo，**跳过直接 URL，直接使用嵌入 URL**。对于私有/不公开列出的视频，直接 URL 几乎总会失败。对于其他托管服务，请按顺序尝试，并在首次成功时停止。

**尝试 1——嵌入/播放器 URL（Vimeo 从这里开始）：**
```bash
yt-dlp "https://player.vimeo.com/video/{id}"
```

**尝试 2——添加 referer 请求头**（如果尝试 1 返回 403）：
```bash
yt-dlp --referer "{source_page_url}" "https://player.vimeo.com/video/{id}"
```

**尝试 3——添加 referer + origin 请求头：**
```bash
yt-dlp --referer "{source_page_url}" --add-header "Origin: {source_origin}" "https://player.vimeo.com/video/{id}"
```

**尝试 4——直接 URL（仅适用于公开视频或非 Vimeo 托管服务）：**
```bash
yt-dlp "{video_url}"
```

### 步骤 4：选择画质（可选）

如果用户需要特定画质：

```bash
# List available formats
yt-dlp -F "{url}"

# Download best quality (default)
yt-dlp -f "bestvideo+bestaudio" "{url}"

# Download specific resolution
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "{url}"

# Download audio only
yt-dlp -f "bestaudio" -x --audio-format mp3 "{url}"
```

### 步骤 5：输出位置

默认情况下，yt-dlp 会保存到当前目录。要指定输出路径：

```bash
yt-dlp -o "~/Downloads/%(title)s.%(ext)s" "{url}"
```

## 故障排除

### OAuth 令牌错误（Vimeo）
```
ERROR: Failed to fetch OAuth token: HTTP Error 400: Bad Request
```
当 yt-dlp 在不支持客户端模拟的情况下尝试直接访问 `vimeo.com/{id}` URL 时，会发生此错误。需要做两件事：
1. 安装 `curl_cffi`：`pip3 install --break-system-packages curl_cffi`
2. 更重要的是，**切换到嵌入 URL**——这才是真正的修复方法。即使安装了 `curl_cffi`，直接 URL 也很可能因视频是私有的而返回 404（见下文）。

### 404 未找到（Vimeo）
```
ERROR: Unable to download macos API JSON: HTTP Error 404: Not Found
```
这是安装 `curl_cffi` 并更新 yt-dlp 后会遇到的情况——OAuth 错误消失了，但由于视频在直接 URL 上是私有/不公开列出的，仍然无法找到。**切换到嵌入 URL**：
- `vimeo.com/{id}` -> `player.vimeo.com/video/{id}`

Vimeo 的典型错误演变过程是：OAuth 400 ->（安装 curl_cffi + 更新 yt-dlp）-> 404 ->（使用嵌入 URL）-> 成功。

### 403 禁止访问
```
ERROR: HTTP Error 403: Forbidden
```
**修复方法**：添加来源页面的 referer 请求头：
```bash
yt-dlp --referer "{source_page_url}" "{embed_url}"
```

### 客户端模拟警告
```
WARNING: The extractor is attempting impersonation, but no impersonate target is available
```
**修复方法**：安装 curl_cffi。这是一个非致命警告，但可能导致后续失败。

### 地区限制内容
```
ERROR: This video is not available in your country
```
**修复方法**：考虑使用 VPN。yt-dlp 支持 `--proxy` 标志：
```bash
yt-dlp --proxy socks5://127.0.0.1:1080 "{url}"
```

## 实际示例：OpenAI Forum Vimeo 嵌入视频

以下是经过测试、可以在 `forum.openai.com` 活动回放页面上正常工作的确切操作顺序（2026-03-28）：

```bash
# 1. Page has schema.org VideoObject with contentUrl: https://vimeo.com/1174947711
#    Direct URL fails (private video).

# 2. This works — use the player embed URL:
yt-dlp --referer "https://forum.openai.com/" "https://player.vimeo.com/video/1174947711"

# 3. yt-dlp downloads HLS fragments (484 in this case), merges video+audio.
#    Result: ~683MB MP4 file.
```

对于这个特定视频，referer 并非严格必需（尝试 1 即可成功），但对于 Vimeo 嵌入视频，包含它是一种良好实践。

## 常见视频页面模式

### OpenAI Forum 活动
- 视频以 Vimeo 形式嵌入，视频 ID 位于 schema.org `contentUrl` 中
- 直接 Vimeo URL 返回 404（私有）
- 使用 `player.vimeo.com/video/{id}`——referer 可选，但建议添加
- 以 HLS 流形式下载（包含许多分片），yt-dlp 会自动合并

### 会议演讲页面
- 通常使用 Vimeo 或 YouTube 嵌入视频
- 检查页面源代码中的 `iframe` 元素
- 有些页面使用封装 YouTube/Vimeo 的自定义播放器——请查找底层嵌入 URL

### 课程/LMS 平台
- 通常使用带有域名限制的 Wistia 或 Vimeo
- 通常必须添加 referer 请求头
- 可能需要 Cookie——必要时使用 `--cookies-from-browser chrome`

### Gradual/活动平台
- 许多活动回放平台（例如 OpenAI Forum 使用的平台）基于 Gradual 构建
- 它们将视频元数据存储在页面 head 中的 schema.org VideoObject 里
- `contentUrl` 字段包含 Vimeo URL，但它是面向公众的 URL，无法用于下载
- 始终将其转换为 `player.vimeo.com` 嵌入形式
