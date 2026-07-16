<!-- source-sha256: fcbc9565d9ef2cca3adcc9163ceff28991e65928f710c509d8218e5094484671 -->
---
name: email-marketing
zh_name: "营销邮件"
en_name: "营销邮件"
emoji: "📧"
description: "产品发布邮件，包含页眉、主视觉、行动号召、规格表和表格回退布局"
category: email
scenario: marketing
aspect_hint: "600 像素邮件宽度"
featured: 7
tags: ["email", "newsletter", "mjml"]
---

【模板：品牌产品发布邮件】
【意图】纯 HTML 邮件，600px 单栏，兼容邮件客户端。
【布局】

- 页眉（文字标识居中）
- 主视觉图块（SVG 占位）
- 标题组合（包含倾斜斜体强调文字）
- 正文 + 主要行动号召按钮
- 规格网格（3 列）
- 页脚（社交链接 + 退订）

【设计细节】

- 使用 `<table role='presentation'>` 做布局兜底
- 颜色使用内联样式（不要依赖 class）
