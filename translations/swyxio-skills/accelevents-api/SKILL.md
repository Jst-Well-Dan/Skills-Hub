<!-- source-sha256: 161922b7c1b3bbb007cfaf7e03ddb0234bd27667f656ca6904e0fc5eecdecbf2 -->
---
name: accelevents-api
description: 用于通过 Accelevents REST API 读取或更新 AI Engineer Europe 演讲者记录，尤其适用于完整记录的 PUT 更新、认证请求头的特殊行为以及保留演讲者现有字段。
---

# Accelevents API — 演讲者管理

## API 端点

- **基础 URL：** `https://api.accelevents.com/rest/host/event/{eventUrl}/speaker`
- **欧洲活动 URL：** `ai-engineer-europe-2026`
- **API 密钥：** 以 `ACCELEVENTS_API_KEY` 密钥形式存储

### 身份认证

- **读取（GET）：** 使用 `Authorization: Bearer {key}` 请求头
- **写入（PUT）：** 使用 `Key: {key}` 请求头——在写入操作中使用 `Authorization: Bearer` 请求头会返回 401。这是一个未记录的特殊行为。

### GET 演讲者列表

```
GET /rest/host/event/{eventUrl}/speaker?page=0&size=500
Headers: Authorization: Bearer {api_key}
```

返回 `{"data": [...], "recordsTotal": N}`。每位演讲者包含以下字段：`speakerId`、`firstName`、`lastName`、`email`、`company`、`linkedIn`、`twitter`、`instagram`、`bio`、`title`、`imageUrl`、`allowEditSessions`、`allowOverrideDetails` 等。

### PUT（更新）演讲者

```
PUT /rest/host/event/{eventUrl}/speaker/{speakerId}
Headers: Key: {api_key}, Content-Type: application/json
Body: { full speaker DTO }
```

**关键：PUT 端点会替换整条演讲者记录。** 请求正文中省略的任何字段都会被重置为 `null`/`false`。你必须：

1. 首先获取当前演讲者数据（通过 GET）
2. 将更新内容合并到完整的现有数据中
3. 在 PUT 请求中发送合并后的完整载荷

必填字段：`speakerId`、`firstName`、`lastName`、`email`

以下字段如已存在，必须始终保留：`company`、`linkedIn`、`twitter`、`instagram`、`bio`、`title`、`pronouns`、`imageUrl`、`allowEditSessions`、`allowOverrideDetails`、`allowAttendeeAccess`、`moderator`、`showModerator`、`position`

成功响应：`{"type": "Success", "message": "Speaker updated"}`

## 双向同步工作流

同步脚本（`src/pages/europe/source/_scripts/sync_accelevents.py`）从 Accelevents 拉取数据。但是，schedule.json 可能包含 Accelevents 中缺失的更丰富数据（来自之前的抓取）。正确的工作流如下：

1. **拉取** Accelevents API 中的最新数据
2. **比较** schedule.json 与 API 数据，找出双方的数据缺口
3. **向上推送** schedule.json 中存在但 Accelevents 中缺失的所有数据（LinkedIn、Twitter、公司）
4. **向下拉取** Accelevents 中存在但 schedule.json 中缺失的所有数据
5. 在所有更新完成后**保存快照**

这可确保两个系统都拥有所有已知数据的并集。

## 已知问题

### 损坏的公司名称

Accelevents 门户存在一个 UI 缺陷，会导致公司字段被单个字符覆盖（例如 `"i"`、`"d"`、`"N"`）。这似乎是门户 UI 中的按键捕获问题。同步脚本包含一项保护措施，会拒绝单字符公司值并记录一条 `[WARN]`。

### 数据事实来源

- **schedule.json** 是网站的事实来源（位于 `src/pages/europe/source/schedule.json`）
- **accelevents_speakers_latest.json** 是仅供参考/调试使用的原始 API 快照——网站构建不会使用它
- schedule.json 更改后，运行：`python3 _scripts/export_csv.py`
- 照片更改后，运行：`pnpm europe:source:sync-public`
