<!-- source-sha256: 45f2baeacf53f3e315310ebe1b1e2cdceb6379868b6cfce2374069252423a080 -->
---
name: invoice
zh_name: "可打印发票"
en_name: "可打印发票"
emoji: "🧾"
description: "标准发票：寄件方/收件方 + 明细 + 税费 + 总额 + 付款指引"
category: finance
scenario: finance
aspect_hint: "A4"
recommended: 13
tags: ["invoice", "bill", "发票"]
---

【模板：可打印发票】
【意图】A4 可打印的发票单页。
【布局】
- 页眉：发票号 / 日期 / 截止日
- 寄件方 / 收件方两块
- 明细表（描述 / 数量 / 单价 / 金额）
- 税费明细 + 合计（右对齐）
- 付款说明区
【设计细节】
- `@media print` 样式；保留颜色对比度
