<!-- source-sha256: 346dbcea5430b39e95845d28af0a086a6a4df5d34dece2d5b435cfe79abbeb4c -->
---
name: download-x-video
description: 使用 yt-dlp 下载 X/Twitter 帖子中的视频。当用户想要“下载这个 X 视频”“保存这个推文视频”“从 Twitter 获取视频”，或提供包含视频的 x.com/twitter.com 状态 URL 时使用。支持 HLS 流，并使用 --print after_move:filepath 可靠地检测路径。
---

# 下载 X/Twitter 视频

通过 yt-dlp 下载 X/Twitter 帖子中的视频。

## 前置条件

- `yt-dlp`：`brew install yt-dlp`

## 用法

```bash
python3 scripts/download_x_video.py "https://x.com/user/status/123/video/1" [/output/dir]
```

将下载文件的路径输出到 stdout。

## 工作原理

- 使用带有 `--print after_move:filepath` 参数的 yt-dlp，以可靠地检测路径
- 支持 Twitter 的 HLS 流媒体格式（分片 MP4）
- 输出模板：指定目录中的 `x_video_<tweet_id>.<ext>`

## 故障排除

### yt-dlp 身份验证错误

如果 Twitter 要求登录，yt-dlp 可能需要 Cookie：

```bash
yt-dlp --cookies-from-browser chrome "https://x.com/..."
```
