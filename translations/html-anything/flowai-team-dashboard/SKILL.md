<!-- source-sha256: e517e95bda0aa1d50a93b7ec6a446fb6e49fed67497049d84177e46710235974 -->
---
name: flowai-team-dashboard
zh_name: "FlowAI 团队管理"
en_name: "FlowAI Team Dashboard"
emoji: "🌊"
description: "三个标签页的团队管理后台：成员、详情、活动日志，包含图表和 CSV 导出"
category: dashboard
scenario: operations
aspect_hint: "桌面 1440"
tags: ["flowai", "team", "members"]
---

【模板：FlowAI 团队管理仪表板】
【意图】采用 FlowAI 美学风格的团队管理后台单页。
【布局】
- 标签页：团队成员 / 团队详情 / 活动日志
- KPI 统计行
- 成员表格（头像 + 角色 + 状态）
- 角色分布条形图
- 在线状态 + 活动迷你折线图
- 主要贡献者面板
【设计细节】
- 浅色/深色切换、悬停工具提示、点击缩放面板
- CSV 导出按钮（前端实现）
