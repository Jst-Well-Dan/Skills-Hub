<!-- source-sha256: 178bdbf0fbb683d4ea3c843143008c9d0c44a8d53a829d1512e9c95d5ce35e2b -->
---
name: deck-presenter-mode
zh_name: "演讲者模式 Deck"
en_name: "Presenter Mode Deck"
emoji: "🎤"
description: "东京之夜默认主题，按 T 切换 5 种主题，按 S 打开提词器弹窗"
category: slides
scenario: engineering
aspect_hint: "16:9"
featured: 26
tags: ["presenter", "notes", "提词", "teleprompter"]
---

【模板：演讲者模式 Deck】
【意图】专为怕忘词的演讲者设计的 deck，包含逐字稿 notes 与 popup teleprompter。
【布局】

- 每页 + `<aside class="notes">` 150-300 字稿
- 右下角小 toolbar：按 T 切换主题 / 按 S 打开 popup
- Popup：CURRENT / NEXT / SCRIPT / TIMER 四张磁吸卡

【设计细节】

- 默认 tokyo-night；共 5 套主题（含 light）
