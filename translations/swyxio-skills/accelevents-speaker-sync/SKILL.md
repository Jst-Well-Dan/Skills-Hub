<!-- source-sha256: 35ee3a0b8e14c232998d32e2c8a6d8f9d8479bd886c042b17a3b5e574b49e28f -->
---
name: accelevents-speaker-sync
description: 当网站上的演讲者、会议、日程、房间、主题轨道或头像变更必须同步回 AI Engineer Europe 2026 的 Accelevents 时使用。
---

# Accelevents 演讲者与会议同步

每当你更新网站上的演讲者数据或会议/日程详情时，都必须将这些更改推送到 Accelevents 中对应的个人资料和会议。

## 适用情况

### 演讲者变更
- 添加或替换演讲者照片
- 更新演讲者姓名、职位、公司、简介或社交链接
- 对 `src/pages/europe/source/schedule.json` 所做的任何影响演讲者元数据的更改

### 会议/日程变更
- 更改会议开始时间、结束时间或日期
- 更改会议房间、主题轨道或形式
- 更新会议/演讲标题
- 将演讲者移至不同的会议时段

## Accelevents API 详情

- **API 基础地址**：`https://api.accelevents.com`
- **活动 URL**：`ai-engineer-europe-2026`
- **读取操作的身份验证**：`Authorization: Bearer $ACCELEVENTS_API_KEY`
- **写入操作（PUT/POST）的身份验证**：`Key: $ACCELEVENTS_API_KEY` 请求头

## 演讲者更新工作流

### 1. 查找演讲者的 Accelevents ID

在 `src/pages/europe/source/schedule.json` 中查找你要更新的演讲者对应的 `acceleventsSpeakerId`。

或者按姓名搜索：
```bash
curl -s -H "Authorization: Bearer $ACCELEVENTS_API_KEY" \
  "https://api.accelevents.com/rest/host/event/ai-engineer-europe-2026/speaker?searchString=SPEAKER_NAME&page=0&size=10&expand=TAG"
```

### 2. 上传新照片（如果照片已更改）

上传图片文件（必须小于 2MB）：
```bash
curl -s -X POST \
  -H "Authorization: Bearer $ACCELEVENTS_API_KEY" \
  -F "file=@/path/to/photo.jpg" \
  "https://api.accelevents.com/rest/event/upload/image"
```

此操作会返回 `{"type": "Success", "message": "<image-uuid>"}`。将 `message` 的值保存为图片 UUID。

### 3. 更新演讲者资料

写入操作使用 PUT 和 `Key` 请求头（不要使用 `Authorization: Bearer`）：
```bash
curl -s -X PUT \
  -H "Key: $ACCELEVENTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"speakerId": SPEAKER_ID, "firstName": "First", "lastName": "Last", "email": "email@example.com", "imageUrl": "<image-uuid>"}' \
  "https://api.accelevents.com/rest/host/event/ai-engineer-europe-2026/speaker/SPEAKER_ID"
```

重要说明：
- PUT/写入操作使用 `Key` 请求头（不要使用 `Authorization: Bearer`）
- 使用扁平的 JSON 请求体（不要包装在 `speakerDTO` 对象中）
- 请求体中必须包含 `email`，这是必填字段
- 包含 `speakerId`、`firstName`、`lastName`，以避免清除现有数据

### 4. 验证更新

再次获取演讲者信息，确认更改已生效：
```bash
curl -s -H "Authorization: Bearer $ACCELEVENTS_API_KEY" \
  "https://api.accelevents.com/rest/host/event/ai-engineer-europe-2026/speaker?searchString=SPEAKER_NAME&page=0&size=10&expand=TAG"
```

## 会议/日程更新工作流

### 1. 在 Accelevents 中查找会议

列出所有会议，以找到需要更新的会议：
```bash
curl -s -H "Authorization: Bearer $ACCELEVENTS_API_KEY" \
  "https://api.accelevents.com/rest/events/ai-engineer-europe-2026/session?page=0&size=100&expand=SPEAKER,TRACK,TAG"
```

按标题或分配到会议的演讲者匹配会议。记下 `sessionId`。

`schedule.json` 中的演讲者可能包含映射到 Accelevents 会议 ID 的 `sessionId` 字段，请先在那里检查。

### 2. 更新会议

使用 PUT 和 `Key` 请求头：
```bash
curl -s -X PUT \
  -H "Key: $ACCELEVENTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Talk Title", "startTime": "2026/04/08 13:00", "endTime": "2026/04/08 15:00", "format": "WORKSHOP"}' \
  "https://api.accelevents.com/rest/host/event/ai-engineer-europe-2026/session/SESSION_ID"
```

关键字段：
- `title`：会议/演讲标题
- `startTime` / `endTime`：格式为 `yyyy/MM/dd HH:mm`
- `format`：`MAIN_STAGE`、`BREAKOUT_SESSION`、`MEET_UP`、`WORKSHOP`、`EXPO`、`BREAK`、`OTHER` 之一
- `locationId`：房间/地点 ID（从当前会议数据中获取）
- `status`：`VISIBLE` 或 `HIDDEN`

### 3. 验证会议更新

```bash
curl -s -H "Authorization: Bearer $ACCELEVENTS_API_KEY" \
  "https://api.accelevents.com/rest/events/ai-engineer-europe-2026/session?page=0&size=100&expand=SPEAKER,TRACK"
```

## 现有同步脚本

仓库中有一个位于 `src/pages/europe/source/_scripts/sync_accelevents.py` 的脚本，用于从 Accelevents 同步到网站（拉取数据）。上述工作流执行的是相反方向的操作（将数据推送到 Accelevents）。
