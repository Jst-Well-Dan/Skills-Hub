<!-- source-sha256: 38ab2f375241beb559272ab40b9e0f32535042600baba175b3f41f29156e7488 -->
---
name: youtube-api
description: |
  通过 YouTube Data API v3 以编程方式管理 YouTube 视频——上传视频文件、上传自定义缩略图、更新视频元数据（标题、描述、标签），以及查询视频/频道信息，而无需使用 YouTube Studio 的浏览器界面。每当用户希望执行以下操作时，请使用此技能：将本地视频文件上传到 YouTube；使用本地图像文件设置、更新或更改 YouTube 视频的缩略图；批量设置多个视频的缩略图；以编程方式更新视频标题、描述或标签；查询其频道的视频列表；或进行任何涉及 YouTube Data API 的操作。触发词："upload to youtube"、"upload video"、"set thumbnail"、"upload thumbnail"、"change thumbnail"、"YouTube API"、"batch thumbnails"、"update video title"、"update video description"、"youtube metadata"，或任何对以编程方式管理 YouTube 视频的提及。当基于浏览器的 YouTube Studio 上传不可靠或速度缓慢时，也应使用此技能。
license: MIT
compatibility: |
  需要 Python 3.8+，并安装 google-api-python-client、google-auth-oauthlib 和 google-auth。
  可在 macOS、Linux 和 Windows 上运行。需要一个已启用 YouTube Data API v3
  且配置了 OAuth 2.0 桌面应用凭据的 Google Cloud 项目。在无头环境/Cowork 中使用前，
  需要在用户的本地计算机上通过浏览器完成一次性 OAuth 授权。
metadata:
  author: swyxio
  version: "1.0"
  last-updated: "2026-03-28"
  primary-tools: YouTube Data API v3, Python, Google OAuth 2.0
---

# YouTube API

通过 YouTube Data API v3 以编程方式管理 YouTube 视频——包括上传、缩略图、元数据和查询——完全绕过 YouTube Studio 的浏览器界面。

## 此技能存在的原因

YouTube Studio 的浏览器界面在批量操作时并不可靠，也不便于自动化。缩略图文件选择器时常失灵，编辑多个视频的元数据十分繁琐，浏览器上传也可能停滞或重置。此技能使用 OAuth2 身份验证和持久化令牌缓存封装了 YouTube Data API v3，因此完成设置后，上传及后续编辑都可以完全通过脚本执行——即使 Cowork 虚拟机发生重置也不受影响。

## 前置条件

### Python 依赖项

```bash
pip install google-api-python-client google-auth-oauthlib google-auth --break-system-packages
```

### Google Cloud 项目设置（一次性）

如果用户尚未设置 YouTube API 凭据，请引导他们完成以下步骤。整个过程大约需要 5 分钟：

1. **创建/选择 Google Cloud 项目**
   - 前往 [console.cloud.google.com](https://console.cloud.google.com)
   - 创建新项目或选择现有项目

2. **启用 YouTube Data API v3**
   - 导航至 APIs & Services → Library
   - 搜索 "YouTube Data API v3" → 点击 Enable

3. **配置 OAuth 权限请求页面**
   - 前往 Google Auth Platform → Overview → "Get started"
   - 应用名称：任意名称（例如 "YouTube API Tool"）
   - 用户支持电子邮件：选择用户的 Google 电子邮件地址
   - 受众：**External**
   - 联系电子邮件：用户的电子邮件地址
   - 同意 Google API Services User Data Policy → 点击 Create

4. **将用户添加为测试用户**（关键步骤——应用将保持 Testing 模式）
   - 前往 Google Auth Platform → Audience
   - 在 "Test users" 下点击 "+ Add users"
   - 添加与其 YouTube 频道关联的 Google 电子邮件地址
   - 保存

5. **创建 OAuth 2.0 凭据**
   - 前往 Google Auth Platform → Clients → "+ Create client"
   - 应用类型：**Desktop app**
   - 名称：任意名称（例如 "YouTube API Tool"）
   - 点击 Create
   - **下载 JSON 文件**——这就是 `client_secret.json` 文件

6. **存储凭据**

   在 macOS/Linux 上（标准方式）：
   ```bash
   mkdir -p ~/.config/youtube-api
   mv ~/Downloads/client_secret_*.json ~/.config/youtube-api/client_secret.json
   ```

   用于 Cowork 持久化（虚拟机重置后仍然保留）：
   ```bash
   mkdir -p ~/Downloads/.youtube-api
   mv ~/Downloads/client_secret_*.json ~/Downloads/.youtube-api/client_secret.json
   ```

7. **运行首次 OAuth 流程**（必须在用户的本地计算机上进行——将打开浏览器）
   ```bash
   python <skill-path>/scripts/setup_auth.py
   ```
   这会打开浏览器以进行 Google OAuth 授权。用户登录、授权应用后，`token.pickle` 将缓存在 `client_secret.json` 所在目录。此后，所有后续运行（包括在 Cowork 中运行）都将完全自动化。

   出现权限请求页面时，系统会警告该应用 "unverified"——这对于测试模式来说是正常现象。点击 "Advanced" → "Go to [app name] (unsafe)" → 允许访问。

### 凭据存储位置

脚本会自动检测最佳凭据位置：

| 环境 | 配置目录 | 是否跨会话保留？ |
|---|---|---|
| Cowork | `/sessions/*/mnt/Downloads/.youtube-api/` | 是（位于用户的真实计算机上） |
| 标准环境 | `~/.config/youtube-api/` | 是 |

`client_secret.json` 和 `token.pickle` 必须位于同一目录中。脚本会先检查 Cowork 路径，然后回退到标准路径。

## 操作

### 设置缩略图

将自定义缩略图上传到一个或多个 YouTube 视频。

**单个视频：**
```bash
python <skill-path>/scripts/set_thumbnail.py --video-id VIDEO_ID --thumbnail /path/to/image.jpg
```

**批量模式：**
```bash
python <skill-path>/scripts/set_thumbnail.py \
  --batch VIDEO_ID_1:/path/to/thumb1.jpg VIDEO_ID_2:/path/to/thumb2.jpg
```

**缩略图要求：**
- 最大大小：2 MB（使用 `convert input.jpg -resize 1280x720 -quality 85 output.jpg` 进行压缩）
- 格式：JPEG（推荐）、PNG
- 尺寸：推荐 1280x720（16:9 宽高比）

### 上传视频

将制作完成的本地视频文件直接上传到 YouTube。

```bash
python <skill-path>/scripts/upload_video.py --file /path/to/video.mp4 --privacy unlisted
```

上传时可选择提供元数据：

```bash
python <skill-path>/scripts/upload_video.py \
  --file /path/to/video.mp4 \
  --privacy unlisted \
  --title "Video Title" \
  --description "Optional description" \
  --tags "tag1,tag2"
```

### 更新视频元数据

更新一个或多个视频的标题、描述和/或标签。

**单个视频：**
```bash
python <skill-path>/scripts/update_metadata.py --video-id VIDEO_ID \
  --title "New Title" \
  --description "New description" \
  --tags "tag1,tag2,tag3"
```

**批量模式（使用 JSON）：**
```bash
python <skill-path>/scripts/update_metadata.py --batch updates.json
```

其中 `updates.json` 的内容如下：
```json
[
  {"video_id": "abc123", "title": "New Title", "description": "New desc"},
  {"video_id": "def456", "tags": ["tag1", "tag2"]}
]
```

只会更新你指定的字段——其他所有内容都会保留。

### 列出频道视频

查询已通过身份验证的用户频道中由其上传的视频。

```bash
python <skill-path>/scripts/list_videos.py [--max-results 50]
```

返回视频 ID、标题、发布日期和缩略图 URL。适合用于构建批量操作。

## API 配额

- `thumbnails.set`：每次调用 50 个单位
- `videos.update`：每次调用 50 个单位
- `videos.list`：每次调用 1 个单位
- `search.list`：每次调用 100 个单位
- 默认每日配额：10,000 个单位 → 每天约可上传 200 个缩略图或执行 200 次元数据更新
- 如果达到配额限制，请等待次日，或在 Google Cloud Console → APIs & Services → Quotas 中申请提高配额

## 故障排除

| 错误 | 原因 | 解决方法 |
|---|---|---|
| "token has been expired or revoked" | OAuth 令牌已过期且无法刷新 | 从配置目录（启动时会显示）中删除 `token.pickle`，然后重新运行 `setup_auth.py` |
| "quotaExceeded" | 已达到每日 API 配额 | 等待次日或申请提高配额 |
| "forbidden" 或 "thumbnailsNotAccessible" | 账户没有使用自定义缩略图的权限 | 确认 YouTube 账户状态良好且已启用自定义缩略图 |
| "The caller does not have permission" | 未在 OAuth 权限请求页面中列为测试用户 | 在 Google Auth Platform → Audience 中将该 Google 电子邮件地址添加为测试用户 |
| 图像出现 "fileNotFound" | 文件路径错误 | 检查文件路径；脚本会在上传前进行验证 |
| 图像过大 | 超过 2 MB | 压缩：`convert input.jpg -resize 1280x720 -quality 85 output.jpg` |
| OAuth 浏览器未打开 | 正在无头环境/Cowork 环境中运行 | 先在本地计算机上运行 `setup_auth.py`，然后将 `token.pickle` 复制到 Cowork 配置目录 |

## 与其他流水线集成

此技能非常适合作为内容流水线的最后一步。例如，使用图像生成工具创建缩略图后：

```bash
# Generate thumbnails, then upload them
python <skill-path>/scripts/set_thumbnail.py \
  --batch \
  xUy0vno25k0:~/Downloads/thumb_feb4.jpg \
  LJFL6bYyGHg:~/Downloads/thumb_feb13.jpg \
  s5bTZfYUcac:~/Downloads/thumb_feb18.jpg
```
