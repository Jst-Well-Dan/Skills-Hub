<!-- source-sha256: e2643fd4cf2342fce1e93ae61bae2072825dd9acecd25d73a156aae497833943 -->
---
name: kanban-board
zh_name: "看板 / Kanban"
en_name: "看板"
emoji: "📌"
description: "待办 / 进行中 / 审核中 / 已完成四列，卡片 + 头像 + 泳道"
category: dashboard
scenario: operations
aspect_hint: "桌面 1440"
tags: ["kanban", "trello", "sprint", "看板"]
---

【模板：Kanban 看板】
【意图】类似 Trello 的 Kanban 单页。
【布局】

- 顶部筛选栏（负责人 / 标签 / 搜索）
- 4 列：待办 / 进行中 / 审核中 / 已完成
- 卡片包含：标题 / 标签 / 截止日期 / 头像 / 评论数
- 可选泳道（按史诗 / 负责人分组）

【设计细节】

- 不需要真正拖拽，但视觉上要像可拖拽
