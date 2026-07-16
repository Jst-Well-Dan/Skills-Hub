<!-- source-sha256: 0fd23b8a02cb2ec6385a35af22964b48dd5119b47fe48c77f4e64e3baa06b606 -->
---
name: docs-page
zh_name: "技术文档页"
en_name: "Docs Page"
emoji: "📘"
description: "三栏文档页: 侧导航 + 正文 + 右 TOC"
category: doc
scenario: engineering
aspect_hint: "桌面 1440"
tags: ["docs", "api", "tutorial", "guide"]
---

【模板: 技术文档页】
【意图】API / 教程文档单页, 长读体验优先。
【布局】
- 行首导航 (章节 + sticky)
- 文章正文 (含代码块, 提示框, 表格)
- 行尾 TOC (sticky, scroll-spy)
- 顶栏搜索 + 版本 + 主题切换
【设计细节】
- 代码块: 圆角 + 深色 + 语言标签 + 复制按钮
- 提示框: 信息 / 警告 / 危险三色
