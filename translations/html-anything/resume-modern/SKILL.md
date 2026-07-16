<!-- source-sha256: 821a0d09f2db73f2fad4bd0bd67f276ebb6d0c5494897830fcd69c2dbcdc7e7c -->
---
name: resume-modern
zh_name: "极简简历"
en_name: "现代简历"
emoji: "📄"
description: "现代极简简历，A4 单页，适合打印或导出 PDF"
category: resume
scenario: personal
aspect_hint: "A4 (210×297mm)"
recommended: 12
tags: ["resume", "cv", "简历"]
example_id: sample-resume-frontend
example_name: "极简简历 · 前端工程师"
example_format: markdown
example_tagline: "A4 单页，可打印 / 导出 PDF"
example_desc: "高级前端工程师简历，两栏布局，数字成就高亮"
---

【模板：现代极简简历】
- 容器宽度模拟 A4：`w-[210mm] min-h-[297mm] mx-auto`，内边距 16-20mm。
- 顶部姓名使用超大字号 (text-4xl)，下方一行放置联系方式（邮箱 / 电话 / 城市 / GitHub / LinkedIn），中间用细竖线分隔。
- 主体可选两栏布局：左侧 60% 为主线（经历/项目/教育），右侧 40% 为副线（技能/语言/获奖）。
- 章节标题：小型大写字母风格，上方一条短强调线 (w-8 h-0.5)。
- 每条经历：公司 + 职位 + 时间区间（右对齐），下方 1-3 条项目符号内容以动词开头。
- 不使用花哨颜色，采用黑白灰 + 1 种强调色（深蓝 / 墨绿）。
- 添加 @media print 样式，隐藏不必要的元素，保留颜色。
