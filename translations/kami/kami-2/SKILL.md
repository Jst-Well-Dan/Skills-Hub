<!-- source-sha256: 5b659e98b628dfb9951dff9d96ebac051866480202250c017e038f2732c1d6ea -->
---
name: kami
description: '排版专业文档与产品落地页：简历、单页文档、白皮书、信件、作品集、幻灯片、落地页。暖色羊皮纸质感、墨蓝色强调、以衬线字体为主的层级。中文使用 TsangerJinKai02，英文使用 Charter，日文使用 YuMincho（尽力支持）。由 "做 PDF / 排版 / 一页纸 / 白皮书 / 作品集 / 简历 / PPT / slides / Marp / markdown slides / マークダウンのスライド / 落地页 / 官网 / landing page / product page"，或 "build me a resume / make a one-pager / design a slide deck / turn this into a PDF / make this presentable / create a landing page" 触发。'
---

# kami · 紙

**紙 · かみ**——承载你的交付成果的纸张。

好内容值得配上好纸张。文档与落地页共享同一种设计语言：暖色羊皮纸画布、墨蓝色强调、以衬线字体为主的层级，以及紧凑的编辑节奏。

`Kaku · Waza · Kami` 的一部分——Kaku 编写代码，Waza 训练习惯，**Kami 交付文档**。

**更新检查（非阻塞）。** 开始任务时，运行 `bash scripts/check-update.sh`。它每天最多执行一次只读版本检查；当有新版 kami 可用时，会打印一行提示。将该行转告用户，然后继续。它不会发送任何数据，并会在离线、沙盒环境或缺少 `curl` 时静默失败。绝不能让它阻塞工作。

## 步骤 0 · 加载品牌配置（如存在）

检查 `~/.config/kami/brand.md`（首选）或 `~/.kami/brand.md`（旧版回退路径）。如果找到，请阅读 `references/brand-profile.md`，了解完整的四层应用规范（占位符替换、会话默认值、视觉定制、习惯备注）及其六项护栏。如果不存在配置，则不中断地继续。

关键规则：明确提示 > 编辑判断 > 习惯备注 > frontmatter 默认值 > 内置默认值。配置只会静默补全缺失信息，绝不会覆盖当前对话。

## 步骤 0.5 · 用户项目风格扫描（选择加入）

仅当用户明确引用同级项目作为视觉参考时运行，例如："like my <project> site"、"match the style of <repo>"、"use the look from <directory>"。没有此类引用时静默跳过。

触发后，在生成之前：

1. 定位所引用项目的样式文件：
   ```bash
   find <referenced-path> -maxdepth 4 \( -name "*.css" -o -name "tailwind.config.*" -o -name "theme.*" -o -name "tokens.*" \) | head -20
   ```
2. 提取：主色值（hex / hsl）、字体栈、间距尺度、圆角尺度。优先采用 CSS 变量或设计令牌中声明的值，而非内联字面量。
3. 将结果作为 C 层（视觉定制）合并进当前会话的品牌配置，而不是 B 层（会话默认值）。不得覆盖明确的 `--brand` 标志或用户在本轮中输入的值。
4. 继续前用一行报告："已扫描 <project>，提取 N 种颜色 / M 种字体；将其用作视觉参考。"

如果引用路径不存在、未找到类似 CSS 的文件，或提取结果会与用户当前消息中的明确值冲突，则跳过并回退到品牌配置默认值。

---

## 步骤 1 · 确定语言

**匹配用户的语言。** 中文 -> `*.html` / `slides-weasy.html`。英文 -> `*-en.html` / `slides-weasy-en.html`。日文 -> 尽力使用 CJK 路径（`.html` / `slides-weasy.html`），优先使用日文明朝体，并在交付前进行视觉 QA。韩文 -> 尽力使用专用的 `*-ko.html` / `slides-weasy-ko.html` 系列，并在交付前进行视觉 QA。参考文档共用英文规范。

语义不明确时（例如只有 "resume" 这样的单词命令），用一句话询问，不要猜测。

| 用户语言 | HTML 模板 | 幻灯片（默认 PDF） | 幻灯片（PPTX 回退） |
|---|---|---|---|
| 中文（主要支持） | `*.html` | `slides-weasy.html` | `slides.py` |
| 英文 | `*-en.html` | `slides-weasy-en.html` | `slides-en.py` |
| 日文（尽力支持） | `*.html` | `slides-weasy.html` | `slides.py` |
| 韩文（尽力支持） | `*-ko.html` | `slides-weasy-ko.html` | 不适用（仅在必须提供 PPTX 时使用 `slides-en.py`） |
| 其他语言（尽力支持） | 根据文字覆盖范围选择 CJK 或 EN 路径，然后手动验证 | 选择 `slides-weasy.html` 或 `slides-weasy-en.html`，然后手动验证 | 仅在必须提供 PPTX 时使用 `slides.py` / `slides-en.py` |

> 默认使用 WeasyPrint HTML 路径；仅当用户明确需要可编辑的演示文稿时，才回退到 PPTX（`slides*.py`）。

始终使用 `CHEATSHEET.md` 和 `references/*.md` 获取设计、写作、制作及图表指导。

仅当构建环境安装了可选的 `Pygments` 时，带有 `class="language-*"` 的代码块才会高亮。未安装时，PDF 仍可正常渲染，代码块保持单色。

## 步骤 1.5 · 意图提取（静默检查清单）

选择模板之前，确认以下四个维度已经明确。除非至少有 2 项缺失且无法从上下文推断，否则不要提问。

| 维度 | 要提取的内容 | 示例 |
|---|---|---|
| **目的** | 这份文档为何存在 | 说服投资者、统一内部团队认知，还是打动候选人 |
| **受众** | 谁会阅读，他们已经了解什么 | 技术型 CTO（跳过基础知识）与非技术董事会（解释术语） |
| **约束** | 对篇幅、格式、语气或交付方式的硬性限制 | "最多一页"、"正式英文"、"可直接印刷的 A4" |
| **成功标准** | 什么结果算成功 | 对方安排会议 / 批准预算 / 理解架构 |

规则：

- 如果对话已经回答某个维度，静默跳过。
- 如果某个维度可从文档类型推断（例如简历的目的始终是"获得面试"），则跳过。
- 如果至少 2 个维度确实不明确，用一个紧凑问题询问（最多包含 2 个子问题）。
- 绝不要把四项全部作为清单询问。这是后台核验，不是表单。

## 执行契约

创建或修改输出之前，锁定契约：语言、模板、输出格式、页数或篇幅目标、视觉验收检查及验证命令。用户请求足够明确时直接推断；仅当缺失字段会实质改变交付成果时才询问。

使用最接近的现有模板和验证路径。除非当前请求不新增便无法完成，否则不要添加新模板、共享 CSS 层、依赖项、脚本标志或可选模式。

如果改动涉及 `SKILL.md`、模板、脚本、参考资料或打包输入，请在交付前判断是否必须刷新 `dist/kami.zip`。在软件包包含已更改文件之前，交付行为尚未就绪。

---

## 步骤 2 · 选择文档类型

| 用户说 | 文档 | 中文模板 | 英文模板 | 韩文模板 |
|---|---|---|---|---|
| "one-pager / 方案 / 执行摘要 / exec summary" | 单页文档 | `one-pager.html` | `one-pager-en.html` | `one-pager-ko.html` |
| "white paper / 白皮书 / 长文 / 年度总结 / technical report" | 长文档 | `long-doc.html` | `long-doc-en.html` | `long-doc-ko.html` |
| "formal letter / 信件 / 辞职信 / 推荐信 / memo" | 信件 | `letter.html` | `letter-en.html` | `letter-ko.html` |
| "portfolio / 作品集 / case studies" | 作品集 | `portfolio.html` | `portfolio-en.html` | `portfolio-ko.html` |
| "resume / CV / 简历 / 履歴書" | 简历 | `resume.html` | `resume-en.html` | `resume-ko.html` |
| "slides / PPT / deck / 演示" | 幻灯片 | `slides-weasy.html` | `slides-weasy-en.html` | `slides-weasy-ko.html` |
| "个股研报 / equity report / 估值分析 / investment memo / 股票分析" | 个股研报 | `equity-report.html` | `equity-report-en.html` | `equity-report-ko.html` |
| "更新日志 / changelog / release notes / 版本记录" | 更新日志 | `changelog.html` | `changelog-en.html` | `changelog-ko.html` |
| "landing page / 落地页 / 官网 / product page / 产品页" | 落地页 | `landing-page.html` | `landing-page-en.html` | `landing-page-ko.html` |

> **更新日志与发行说明**：上面的更新日志模板用于生成带样式的文档。GitHub 发行说明是另一种交付成果；请使用带有发行说明模板模式的 `/write`。

> **落地页**：屏幕优先的交互式模板。不输出 PDF。包含自动轮播的图库、首屏入场动画、响应式断点（880px / 480px），并支持 `prefers-reduced-motion`。可将静态 HTML 部署到 Vercel / Netlify / 任意主机。智能体填写 {{PLACEHOLDER}} 值和 HTML 注释块，然后保存为可直接提供服务的 `.html` 文件。

> **落地页配套文件**：生产环境的多语言部署需要将五个 `landing-page-*.example` 文件复制到主 HTML 旁边，移除 `.example` 后缀并填写占位符。这些文件涵盖 Vercel 重写与响应头、站点地图 hreflang、robots AI 允许列表，以及供 AI 助手使用的 llms.txt + llms-full.txt。主 HTML 的 `<head>` 中已经包含匹配的 hreflang 和 og:locale；`landing-page-en.html` 末尾的 Accept-Language 重定向默认被注释，可选择启用。`{{SITE_ORIGIN}}` 是 `{{CANONICAL_URL}}` 的协议与主机部分（例如 `https://example.com`）。参见 `references/design.md` 第 11 节《配套资源》。

> **生产级产品网站模式**：如果用户需要文档、帮助、发行版本、更新日志、路线图、法律页面或两个以上的语言区域，请将其视为网站系统。填充模板之前，锁定产品类别、真实截图槽位、语言区域列表、配套文件、长内容页面，以及生成器/检查需求。不要把项目特定的发行构件、支付服务商、appcast 规则和私有本地路径放入 Kami。参见 `references/design.md` 第 11 节《产品网站系统》。

> **文档页面**：当落地页扩展成文档或帮助网站时，使用 `references/design.md` 第 11 节《文档网站》中的文档外壳：带有 2px 品牌色导轨的吸顶侧边导航（不要使用深色下划线）、在平板断点以下隐藏的本页目录、受约束的正文行宽，以及安静且无边框的上一篇/下一篇导航（使用文本链接，而不是带边框的卡片）。构建时在深色代码表面上高亮代码，不使用运行时 JS；纯文本代码始终是真实来源。

> 幻灯片：默认使用 `slides-weasy.html` / `slides-weasy-en.html` / `slides-weasy-ko.html`（WeasyPrint HTML → PDF）。仅当用户明确要求可编辑的 PPTX 文件时，才使用 `slides.py` / `slides-en.py`。仅当用户明确要求 Marp / markdown slides / 存放在 `.md` 文件中的演示文稿时，才使用 `assets/templates/marp/slides-marp(.md|.css)`。

> 演示文稿配方：起草幻灯片前，阅读 design.md 第 8 节。生成或裁切视觉素材前，先勾勒标题序列、证据形态和图片槽位。受众文案与视觉简报分开。Marp 特有的约束位于 design.md §8《Marp 变体》。

### 决策树（提问前使用）

在提出一句话问题之前，先沿此树判断。仅当两个单元格确实都适用时才询问。

| 信号 | 文档 |
|---|---|
| 篇幅目标未知 | 分类前询问"需要多少页" |
| ≤ 1 页 + 投资者 / 招聘人员 / 执行摘要受众 | 单页文档 |
| ≤ 1 页 + 正式通信（销售、招聘、辞职、备忘录） | 信件 |
| 1.5-2 页 + 职业叙事 + 项目要点 | 简历 |
| 3-6 页 + 项目展示 + 重视觉 | 作品集 |
| 6-15 页 + 持续论证 + 低视觉密度 | 长文档 |
| 演示流程 + 演讲辅助 + 每页一个论断 | 幻灯片 |
| 财务 / 指标仪表盘 + 投资论点 + 价格或风险观点 | 个股研报 |
| 按版本记录 + 发行事实 | 更新日志 |
| 面向浏览器的产品展示 + 定价 + 截图 + FAQ | 落地页 |

值得用一句话澄清的歧义示例：

- "1.5 page career story with heavy visuals" -> 询问"简历还是作品集？"
- "2 page exec summary with metric tiles" -> 询问"单页文档还是个股研报？"
- "5 page argument with several charts" -> 询问"长文档还是作品集？"

先按决策树选择。只有决策树确实无法判断时才询问。

### 图表（基础构件，不是独立模板类型）

当用户要求在长文档 / 作品集 / 幻灯片**内部加入图表**（而非独立文档）时，使用 `assets/diagrams/`，而不是文档模板：

| 用户说 | 图表 | 模板 |
|---|---|---|
| "架构图 / architecture / 系统图 / components diagram" | 架构图 | `assets/diagrams/architecture.html` |
| "流程图 / flowchart / 决策流 / branching logic" | 流程图 | `assets/diagrams/flowchart.html` |
| "象限图 / quadrant / 优先级矩阵 / 2×2 matrix" | 象限图 | `assets/diagrams/quadrant.html` |
| "柱状图 / bar chart / 分类对比 / grouped bars" | 柱状图 | `assets/diagrams/bar-chart.html` |
| "折线图 / line chart / 趋势 / 股价 / time series" | 折线图 | `assets/diagrams/line-chart.html` |
| "环形图 / donut / pie / 占比 / 分布结构" | 环形图 | `assets/diagrams/donut-chart.html` |
| "状态机 / state machine / 状态图 / lifecycle" | 状态机 | `assets/diagrams/state-machine.html` |
| "时间线 / timeline / 里程碑 / milestones / roadmap" | 时间线 | `assets/diagrams/timeline.html` |
| "泳道图 / swimlane / 跨角色流程 / cross-team flow" | 泳道图 | `assets/diagrams/swimlane.html` |
| "树状图 / tree / hierarchy / 层级 / 组织架构" | 树状图 | `assets/diagrams/tree.html` |
| "分层图 / layer stack / 分层架构 / OSI / stack" | 分层图 | `assets/diagrams/layer-stack.html` |
| "维恩图 / venn / 交集 / overlap / 集合关系" | 维恩图 | `assets/diagrams/venn.html` |
| "K 线 / candlestick / OHLC / 股价走势 / price history" | K 线图 | `assets/diagrams/candlestick.html` |
| "瀑布图 / waterfall / 收入桥 / revenue bridge / decomposition" | 瀑布图 | `assets/diagrams/waterfall.html` |

绘图前阅读 `references/diagrams.md`——其中包含选择指南、kami 令牌映射和 AI 粗制滥造反模式表。从模板中提取 `<svg>` 块，并将其放入长文档 / 作品集中的 `<figure>` 内。

绘制前始终问：**与这张图相比，一段写得好的文字是否会让读者学到更少？** 如果不会，就不要画图。

**根据数据自动选择图表。** 当内容包含数值数据时，选择合适的图表类型并嵌入，无需等待用户指定。决策树（首个匹配项胜出）：

| 数据形态 | 图表 |
|---|---|
| 包含 open/high/low/close 字段，或每日价格 | K 线图 |
| 包含合计成总数的正负贡献（桥接、瀑布、损益） | 瀑布图 |
| 单个序列，数值总和约为 100%，项目 ≤ 6 | 环形图 |
| 单个序列，数值总和约为 100%，项目 ≥ 7 | 水平柱状图 |
| 两个或更多随时间变化的序列（月、季度、年） | 折线图 |
| 单个随时间变化的序列，主要体现数量的大幅变化（而非比率） | 柱状图 |
| 多个类别、同一时间快照、2 个以上序列 | 分组柱状图 |
| 2×2 战略或优先级定位 | 象限图 |
| 深度 ≥ 2 的层级数据 | 树状图 |
| 带有决策分支的流程 | 流程图 |
| 包含 ≥ 3 个参与者的跨团队或跨角色流程 | 泳道图 |
| 2-3 个组之间的集合重叠或共有属性 | 维恩图 |
| 类别比较、单一序列、无时间轴 | 柱状图 |

当数据适合多种类型时，优先选择最清晰体现差异的类型。始终嵌入 `<figure>` 中，并添加说明洞察而不只是数据范围的图注。

### 插图（使用宿主图像模型，而非内联 SVG）

上面的内联图表是手工组装的矢量 SVG。对于独立的栅格插图，或以 Kami 风格重绘图形、照片或截图，请将绘制工作交给宿主自身的图像生成功能。绝不要调用外部图像 API 或要求提供密钥；渲染是宿主的工作。

- 如果当前宿主可以生成图像（例如 ChatGPT），请应用下面的简报并直接渲染图像。
- 如果不能（Claude、Codex、大多数编码智能体），则以文本形式输出简报，供用户粘贴到任意图像模型中。

简报：暖色羊皮纸（`#f5f4ed`）背景，绝不使用纯白；只使用一种强调色，即墨蓝色（`#1B365D`）；其余全部使用带黄褐底色的暖灰色，不使用其他颜色；纤细的单线几何笔触和简单扁平图标；无渐变、投影或 3D；使用衬线字体标签；留白充足，构图如同排版精良报告中的插图。

## 步骤 2.1 · 来源与素材检查

当文档依赖用户草稿之外的事实或素材时，在提炼或填充内容前执行此步骤。仅当用户已为个人草稿提供全部所需信息时才跳过。

### 来源检查

当文档提及特定公司、产品、人物、发布日期、版本、融资轮次、指标、市场事实、技术规格，或任何可能变化的当前事实时触发。

- 写作前优先使用第一手来源：用户提供的材料、官方网站、文档、申报文件、新闻稿、应用商店页面或仓库发行版
- 对影响文档的事实，简要记录来源名称与日期
- 如果来源冲突或事实无法快速核实，请询问用户，而不是静默选择
- 除非已核实，否则避免使用"最新"、"近期"、"全新"、版本号、发布日期或财务数据等听起来具有时效性的说法

### 素材检查

当文档涉及公司、产品、项目、场所或个人品牌时触发。

排版前确认能使主体易于识别的素材：

| 需求 | 何时需要 | 可接受来源 |
|---|---|---|
| Logo | 任何品牌文档 | 用户文件或官方 SVG/PNG |
| 产品图片 | 实体产品 / 场所 / 物体 | 官方图片、用户图片或明确标记的缺口 |
| UI 截图 | 应用 / SaaS / 网站 / 工具 | 当前截图、官方产品图片或用户截屏 |
| 品牌颜色 | 品牌单页文档 / 作品集 / 演示文稿 | 官方值、从资源提取的值，或保留 kami 墨蓝色 |
| 字体 | 仅当品牌字体很重要时 | 官方字体、相近的系统回退字体，或 kami 默认字体 |

如果缺少必需项，请用紧凑的缺口表一次性询问。不要用通用图片、近似绘制的 Logo 或虚构值替代缺失素材。

Logo 回退：当请求未指定 Logo，但品牌配置包含 `logo` 路径时，按照 `references/brand-profile.md` C 层填充 `one-pager` / `portfolio` / `slides-weasy` 中被注释的 `.brand-logo` 槽位。将 `~` 展开为绝对路径；如果文件不存在或模板没有对应槽位，则保持注释状态并在没有 Logo 的情况下渲染（绝不要插入损坏的图片）。当前请求中明确提供的 Logo 始终优先。

### 素材状态块

完成素材检查后，在继续之前输出结构化状态块。这是一次性的透明度展示，不是问题：

```
素材状态：
- Logo：OK assets/client-logo.svg
- 品牌颜色：OK #1B365D 已映射到 --brand
- 产品截图：MISSING（继续使用 kami 默认占位符）
- UI 截图：此文档类型不需要
```

使用 `OK`、`MISSING` 或 `not required`。如果缺少必需项且尚未收到用户输入，请使用缺口表询问一次；否则静默继续。

## 步骤 2.5 · 提炼原始内容（如适用）

**自动判断是否需要提炼。** 不要询问用户；根据输入判断：

| 跳过提炼（直接填充） | 执行提炼 |
|---|---|
| 内容具有与模板结构匹配的明确章节标签 | 没有章节结构的原始文字 |
| 指标已经量化且带有单位 | 数字散落或仅被暗示，尚未提取 |
| 用户写了 "use this as-is" / "直接用这个" / "原封不动" | 用户粘贴了多来源材料堆（聊天 / 邮件线程 / 多份文档） |
| 内容数量与模板匹配（例如 4 个指标对应 4 张指标卡片） | 内容数量与模板不匹配（过多或过少） |
| 单一且连贯的表达口吻，主张一致 | 多个来源之间存在冲突主张或重复事实 |

有疑问时就执行提炼。提炼成本很低；重做一份结构错位的文档成本很高。

当用户交付**原始素材**（会议记录、思维倾倒、不同格式的现有文档、聊天记录、零散要点）时：

1. **提取**：找出每项事实陈述、数字、日期、名称、来源、素材引用和行动项
2. **分类**：将每项提取内容映射到目标模板的章节（各文档类型的章节结构参见 `references/writing.md`）
3. **缺口检查**：列出模板需要但原始内容中缺少的内容——包括缺失事实、缺失证据和缺失素材
4. **询问一次**：向用户展示缺口表。不要猜测补全缺口。

缺口检查示例：

| 模板需要 | 已找到 | 缺失 |
|---|---|---|
| 4 张指标卡片 | "8 年"、"50 人团队" | 还需 2 项可量化成果 |
| 3-5 个核心项目 | 提及 2 个 | 至少还需 1 个带成果的项目 |
| 素材 | 已提供 Logo 文件 | 产品截图来源 |

然后使用结构化、已提炼的内容进入步骤 2.6（幻灯片）或排版意图说明（其他所有文档类型）。

## 步骤 2.6 · 演示文稿预检（仅限幻灯片）

除幻灯片外，所有文档类型都跳过此步骤。

### 路径选择

默认使用 WeasyPrint HTML 路径。仅当用户明确需要可编辑的 PPTX 文件时切换到 pptx。仅当用户明确要求 Marp / markdown slides 时切换到 Marp。

| 路径 | 模板 | 使用时机 |
|---|---|---|
| WeasyPrint HTML → PDF（默认） | `slides-weasy.html` / `slides-weasy-en.html` / `slides-weasy-ko.html` | 除非要求 PPTX 或 Marp，否则适用于所有情况 |
| python-pptx → PPTX（回退） | `slides.py` / `slides-en.py` | 用户明确要求可编辑的 PPTX |
| Marp Markdown（变体） | `assets/templates/marp/slides-marp.md`（+ `slides-marp.css`）/ `slides-marp-en.md`（+ `slides-marp-en.css`） | 用户明确要求 Marp、"markdown slides" 或 `.md` 演示文稿。交付的 `.md` 是 Kami Marp 本身可运行的演示；复制它、替换内容并保留结构。通过本地 `marp` CLI 渲染；不随包提供。 |

### 页面尺寸

默认值为 `280mm 158mm`。仅当用户提到篇幅或密度约束时才询问。

| 尺寸 | 使用时机 |
|---|---|
| `280mm 158mm` | 默认；适合大多数演示文稿 |
| `297mm 167mm` | 用户希望空间稍大 |
| `338mm 190mm` | 内容密集的幻灯片，或每页有大量数据点 |

### 内容预检

起草任何幻灯片之前，与用户确认以下各项。一次性询问全部问题，并跳过已经回答的项目：

| # | 问题 |
|---|---|
| 1 | **受众 + 场合**——现场有哪些人？是现场主题演讲、投资者一对一交流，还是异步分享链接？ |
| 2 | **篇幅目标**——演示时长或幻灯片数量？（15 分钟：约 10 页 / 30 分钟：约 20 页 / 45 分钟：约 25-30 页） |
| 3 | **源材料**——已有何种内容：大纲、文档、笔记、数据？ |
| 4 | **图片**——是否有截图、图表、Logo 或产品图片；哪些页面需要真实证据槽位；是否需要单独的视觉简报？ |
| 5 | **硬性约束**——品牌颜色、必需 Logo、是否必须 PPTX、是否有必须存在的页面？ |
| 6 | **格式确认**——需要幻灯片演示文稿，还是看起来像演示文稿的单页文档？ |

起草任何落地页或产品网站前，根据源材料锁定以下各项。仅当缺失项会改变交付成果时，一次性询问：

| # | 锁定项 |
|---|---|
| 1 | **产品类别**——首屏类别：应用、CLI、终端、实用工具、技能、模板系统，或用户提供的其他标签。 |
| 2 | **真实资源**——可用的产品截图、Logo、图标或 UI 捕获，并映射至首屏/图库/功能/社交槽位。缺失资源必须保持明确标记，不得用素材库图片替代。 |
| 3 | **网站形态**——单页，还是主页加文档/帮助/发行版/更新日志/路线图/法律页面？ |
| 4 | **语言区域**——确切的语言区域列表、规范路径，以及是否需要生成器/检查模式。 |
| 5 | **事实界面**——必须保持同步的安装路径、价格、版本、支持渠道、FAQ、`llms.txt` 和 `llms-full.txt`。 |

### 幻灯片内容规则

- 幽灵演示文稿测试：按顺序只读幻灯片标题。标题必须讲清论证；否则在设计样式前修正标题或结构
- 每页只使用一种证据形态：图表、表格、截图、代码、引语或结论。将混合证据拆开，不要塞进一页
- 面向受众的文案保持干净：标题、正文和图注绝不能包含图片提示词、裁切说明或生成备注
- 不使用章节分隔页：使用 `.eyebrow` 标示章节编号，不要使用专门的蓝色背景页面
- 不使用 CJK 括号：将 `（...）` 替换为 `·` 或 `,`
- 每个要点只占一行：精简到能放下为止
- 2×2 布局：使用 `table.t2x2`，不要使用 CSS Grid
- 固定结论：使用 `.co` 和 `position: absolute; bottom: 12mm`

这些规则同样适用于 Marp 演示文稿。Marp 特有语法参见 `references/design.md` §8《Marp 变体》。

## 步骤 2.7 · 排版意图说明（透明、非阻塞）

加载规范并填充模板之前，写一段简短的编辑式说明，阐明排版意图：模板选择、篇幅目标、叙事弧线、嵌入图表、素材状态和输出格式。匹配文档语言。控制在 80 个词以内，使用散文式表达，不要写成状态面板。随后立即继续，不要等待。

示例（中文）：

> 排版意图：Equity Report 中文版，2 页 A4。先立论与目标价，进入估值 (DCF 与可比公司)，落于催化剂与风险。中段嵌一张营收趋势折线和 FY26 收入桥瀑布。Logo 已就位，产品图暂缺，header 改走纯文字。输出 HTML 与 PDF。

示例（英文）：

> Layout intent: Equity Report (EN), two pages A4. Open with thesis and price target, run through valuation (DCF and comparables), close on catalysts and risks. A revenue line chart and an FY26 waterfall sit mid-doc. Logo is in hand; product image is absent, so the header stays text-only. Output: HTML and PDF.

此说明用于提高透明度，而非等待批准。如果用户反对，则进行调整；否则继续步骤 3。

---

## 步骤 3 · 加载恰当数量的规范

选择与任务匹配的层级。默认使用能覆盖工作的最低层级。

| 层级 | 使用时机 | 阅读内容 |
|---|---|---|
| **仅内容** | 更新文字、替换要点、翻译现有文档。CSS 保持不变。 | 仅 `CHEATSHEET.md` |
| **布局微调** | 调整间距、移动章节、在规范内更改字号。涉及 CSS。 | `CHEATSHEET.md` + 模板（令牌已内联） |
| **新文档** | 从零开始或根据原始内容构建。 | 完整设计规范 + 写作规范 + 模板 |
| **简历内容** | 简历特有的要点结构、项目框架、范围—结果—成果规则。 | `resume-writing.md` + 模板 |
| **来源 / 素材** | 公司、产品、市场、发布、融资、规格或品牌主体。 | `writing.md` 来源规则 + 用户/来源材料 |
| **演示文稿（>20 页）** | 需要章节分隔、代码卡片和章节标题的长演示。 | 完整设计规范 + 演示文稿配方（design.md 第 8 节） |
| **故障排查** | 渲染错误、字体问题、页面溢出。 | `production.md`（如果原因是 CSS，则加设计规范） |
| **反模式** | 交付前审查 AI 生成的草稿。 | `anti-patterns.md`（六类检查清单） |
| **图表** | 在文档中嵌入 SVG。 | 仅 `diagrams.md`（包含自己的令牌映射） |

如果工作实际需要的内容超出初始层级，可随时在任务中途升级。

完整规范文件：

- 设计：`references/design.md`
- 写作（通用）：`references/writing.md`
- 写作（简历专用）：`references/resume-writing.md`
- 制作：`references/production.md`
- 图表：`references/diagrams.md`
- 反模式：`references/anti-patterns.md`

## 步骤 4 · 将内容填入模板

- 将模板复制到工作目录；不要从零编写 HTML
- **CSS 保持不变**，只编辑 body
- 内容遵循 `writing.md`：数据优先于形容词，独特表达优先于行业陈词滥调
- 避免 `references/anti-patterns.md` 中列出的模式：空洞、捏造、模仿、过度、来源缺口、语气污染
- **填充前，阅读 `writing.md` 中“各文档类型的质量标准”**。结构是必要条件，但并不充分：简历要点需要行动 + 范围 + 结果 + 业务成果；个股研报需要差异化观点 + 量化催化剂；幻灯片需要论断—证据式标题。达到质量标准与填满每个占位符同样重要。

### 禁止生成

以下是最常见的 AI 文档失败模式。完整列表参见 `references/anti-patterns.md`。

- 最终文档中不得保留占位文字（"Lorem ipsum"、"[Insert here]"、"TBD"）
- 不得虚构指标、财务数据或统计数字；使用 `[DATA NEEDED: description]` 标记缺口
- 不得将素材库图片描述用作图片占位符（"A diverse team collaborating in a modern office"）
- 不得为了填满模板槽位而填充内容（只有 3 个真实项目的简历不需要虚构到 5 个）
- 不得写出只把自身标题改写成句子的段落

### 填写 PDF 元数据（WeasyPrint 会将其写入 PDF）

每个模板的 `<head>` 中都有元数据占位符。构建前填写全部四项：

| 占位符（中文） | 占位符（英文） | 规则 |
|---|---|---|
| `{{作者}}` | `{{AUTHOR}}` | 简历/信件/作品集：使用文档中的人名。其他所有类型：保持原样（构建脚本会从 git 配置或环境推断） |
| `{{摘要}}` | `{{DESCRIPTION}}` | 从前 2 段中提取一句话（≤150 个字符） |
| `{{关键词}}` | `{{KEYWORDS}}` | 从标题 + 章节标题中提取 3-5 个关键词，用逗号分隔 |
| `{{文档标题}}` / `{{信件主题}}` 等 | `{{DOC_TITLE}}` / `{{LETTER_SUBJECT}}` 等 | 根据 H1 或 `.header .title` 文本推断 |

模板中的 `<meta name="generator" content="Kami">` 已固定；不要更改。

**作者推断**：`build.py` 会按以下顺序自动设置 PDF 的 `/Author` 元数据：

1. `git config user.name`（首选）
2. `KAMI_AUTHOR` 环境变量（回退）
3. `"Kami"`（最终回退）

对于个人文档（简历/信件/作品集），HTML `<meta name="author">` 应与内容中的人名一致。对于非个人文档（单页文档/长文档），保持占位符原样，让构建脚本自行推断。

## 步骤 4.1 · 每页密度目标（仅限多页模板）

适用：slides-weasy / long-doc / portfolio / equity-report / changelog。不适用 resume / one-pager / letter（这些有独立的长度合约）。

正文页填充率目标 60-80%。封面 / 目录 / 末尾署名页豁免。这条规则解决的是 AI 生成多页文档时最常见的 draft 缺陷：把内容拆得太散，结果几页都填不满。

### 每页项目数契约

| 模板 | 典型正文页 | 硬性下限（低于时合并） |
|---|---|---|
| slides-weasy | 1 个论断式标题 + 3-5 个支持项，或 1 张图表 + 2-3 个标注 | <3 个项目且无图表 → 合并到相邻幻灯片 |
| long-doc | 1 个章节标题 + 2-4 段 + 最多 1 张图 | 章节渲染后不足页面 40% → 合并到相邻章节 |
| portfolio | 1 个项目标题 + 1 张主图 + 3-5 个成果要点 | 无图片且成果不足 3 项 → 与相邻项目合并 |
| equity-report | 1 个章节 + 1 张表格/图表 + 支持性正文 | 页面上只有 2 行表格 → 合并章节 |
| changelog | 1 个版本块 + 4-8 条记录 | 版本不足 4 条记录 → 与上一版本放在同一页 |

### 稀疏页面合并规则

最终确定前扫描草稿。任何预计渲染后填充不足 50% 的正文页，都按顺序应用以下方法之一：

1. 向上合并到上一章节。
2. 向下合并到下一章节。
3. 将列表提升为值得占用空间的小型图表或表格。
4. 将 `.co` 标注固定在底部（仅 slides-weasy）。固定标注上方的留白是有意设计，不属于稀疏。

禁止用以下方式“填满”稀疏页面：加入填充性文字、把标题重复成句子、虚构统计数据、换种说法重述上一页。如果无法应用合并选项，该页面本身就不应存在。

### 末页豁免

最后一页正文允许只有 40-60% 的填充率。强行平衡末页通常意味着填充。版权页 / 结束幻灯片可具有任意填充率。

### 构建后验证

```bash
python3 scripts/build.py --check-density   # 标记 >25%（WARN）/ >50%（SPARSE）的尾部空白
```

如果正文页（不是封面，也不是末页）出现 SPARSE 警告，应将其视为草稿缺陷，并按合并规则重新编写。

## 步骤 4.5 · 自动选择输出格式

不要询问用户要导出哪种格式。根据上下文决定：

| 信号 | 输出 | 原因 |
|---|---|---|
| 任何文档请求 | HTML + PDF | PDF 是默认交付成果，HTML 是源文件 |
| 幻灯片 / PPT / 演示文稿 | HTML + PDF + PPTX | 演示文稿需要可投影格式 |
| "分享" / "发朋友圈" / "share" / "post" / "preview" | + PNG | 社交平台和即时通信需要图片 |
| "嵌入" / "插图" / "embed in another doc" | 仅 PNG | 用作其他文档内的素材 |
| 用户明确指定格式 | 遵从用户 | 明确请求覆盖自动选择 |

文档模板始终交付 PDF。落地页交付可直接提供服务的静态 HTML 文件。幻灯片同时交付 PPTX。分享场景同时交付 PNG。用户不应需要考虑格式问题。

## 步骤 5 · 构建与验证

```bash
python3 scripts/build.py --verify           # 构建所有模板 + 页数 + 字体检查 + 幻灯片
python3 scripts/build.py --verify resume-en # 对单个目标执行完整验证
python3 scripts/build.py landing-page        # 检查屏幕优先的静态 HTML 模板
python3 scripts/build.py --verify slides    # 验证单个幻灯片演示文稿
python3 scripts/build.py --check-placeholders path/to/filled.html
python3 scripts/build.py --check-resume-balance path/to/resume.pdf
python3 scripts/build.py --check-density              # 页面空白扫描器（跳过封面）
python3 scripts/build.py --check            # 仅检查 CSS 规则违规（快速，不构建）
python3 scripts/build_metadata.py --check   # Codex 插件镜像 + 市场元数据漂移检查
```

> **屏幕验证**：`--check-density` 是印刷输出的门禁。对于屏幕输出（落地页或文档页面），应在每个语言区域下分别以 375px 和 1280px 截取渲染页面，并在交付前检查行尾孤字。参见 `references/design.md` 第 11 节《响应式截图验证》。

源模板有意保留 `{{...}}` 字段。占位符检查应针对完成后的文档，而不是模板库。

视觉异常（标签双重矩形、字体回退、分页问题）-> `production.md` 第 4 部分。

### 维护者模式检查

仅在维护此仓库或发行包时使用这些检查，不用于普通文档生成。

- 如果市场元数据、生成的插件镜像、版本选择或安装路径发生变化，运行 `python3 scripts/build_metadata.py --check`；对于 Codex 安装行为，还应使用隔离的 `CODEX_HOME=/tmp/...`，通过 `codex plugin marketplace add <path>`、`codex plugin add kami@kami` 和 `codex plugin list` 进行冒烟测试。
- 如果 `SKILL.md`、模板、脚本、参考资料或其他打包输入发生变化，并且相关行为通过技能包交付，请运行 `bash scripts/package-skill.sh`，并在交付前检查 `dist/kami.zip`。
- 如果刷新 GitHub 发行版资源，请下载上传后的 `kami.zip`，将其中的 ZIP 条目名称和每个条目的 SHA-256 摘要与本地 `dist/kami.zip` 比较；页面文字、文件大小及容器哈希并不足够。

## 字体

**中文**

- 主要衬线字体：TsangerJinKai02-W04.ttf（400 字重）+ TsangerJinKai02-W05.ttf（500 字重，真实粗体）
- 模板使用双重 @font-face 声明：W04 用于正文，W05 用于标题
- 两个文件均为商业字体。应将它们保留在仓库中，用于本地预览和 CDN 回退，但不要将其打包进 Claude Desktop 技能 ZIP
- 模板内置回退链：Source Han Serif SC -> Noto Serif CJK SC -> Songti SC -> STSong -> Georgia

**日文（尽力支持）**

- 使用 CJK 模板路径，目前没有专用 `-ja` 模板
- 日文明朝体优先的字体栈：YuMincho -> Hiragino Mincho ProN -> Noto Serif CJK JP -> Source Han Serif JP -> TsangerJinKai02 -> serif
- 交付前目视检查换行、标点节奏和强调字重

**韩文（尽力支持）**

- 专用 `-ko` 模板使用 Source Han Serif K Regular / Medium，并在每个回退字体栈中保留真实的 OTF 字体族名称 `Source Han Serif KR`
- 回退：Noto Serif KR / Apple SD Gothic Neo / AppleMyungjo / Charter / Georgia
- OTF 文件采用 OFL 许可证，并被纳入版本控制以供本地预览 / CDN 回退，但为保持软件包体积较小，会从 Claude Desktop 技能 ZIP 中排除

**英文**

- 单一衬线字体：Charter（系统自带于 macOS/iOS），同时用于标题和正文
- 不使用独立无衬线字体：`--sans: var(--serif)`，每页只使用一种字体
- 回退：Georgia（跨平台）/ Palatino / Times New Roman

将字体文件与 HTML 放在一起并使用相对 `@font-face` 路径，是最稳定的设置。`scripts/package-skill.sh` 会从 Claude Desktop ZIP 中排除大型 CJK 字体文件，使上传包保持在 6MB 的大小上限以内。始终上传该 `package-skill.sh` 的输出，绝不要手动压缩检出的仓库（版本控制中的 CJK 字体会使其过大，Claude Desktop 将拒绝上传）。

**字体自动恢复（Claude Desktop）**

构建中文或韩文文档前，确保字体存在。该脚本会尝试多个 CDN 来源，并进行重试和大小验证：

```bash
bash scripts/ensure-fonts.sh
```

它会下载到 XDG 用户字体目录（`${XDG_DATA_HOME:-~/.local/share}/fonts/kami`，可通过 `KAMI_FONT_DIR` 覆盖），**而不是**技能的 `assets/fonts`——这样可保持已安装技能体积较小，避免 Claude Desktop 触发大小限制。fontconfig 默认扫描该目录，因此 WeasyPrint 能在那里找到 `TsangerJinKai02` 和 `Source Han Serif K`；在线渲染则回退到 jsDelivr `@font-face` URL。构建前运行一次。如果所有来源均失败，脚本会输出各语言的替代方案。

## 反馈协议

当用户给出**模糊的视觉反馈**（"looks off"、"太挤了"、"not elegant"）时，不要猜测。结合当前值追问：

| 用户说 | 询问内容 |
|---|---|
| "太挤了" / "too cramped" | 哪个元素？行高（当前：X）？内边距（当前：Y）？页边距？ |
| "太松了" / "too loose" | 相同方向，但反向调整 |
| "颜色不对" / "color feels wrong" | 哪个元素？品牌蓝使用过多？某种灰色显得太冷？ |
| "不够好看" / "not polished" | 字体渲染？对齐？留白分布？层级不清晰？ |
| "看着不专业" / "unprofessional" | 内容措辞？还是布局（对齐、一致性）？ |

响应模板："X 当前设置为 Y。你希望使用 (a) [规范内的具体替代值]，还是 (b) [另一个选项]？"

绝不要只说"我会调整间距"，却不指出具体属性及其新值。

---

## 不应使用此技能的情况

- 用户明确要求 Material / Fluent / Tailwind 默认样式——属于不同的设计语言
- 需要深色 / 赛博朋克 / 未来主义美学（本技能刻意反未来）
- 需要饱和的多色设计（本技能只有一种强调色）
- 需要卡通 / 动画 / 插画风格（本技能采用编辑设计风格）
- Web 动态应用 UI（本技能用于印刷 / 静态文档）

---

下一步：**应用步骤 3 的层级表决定要阅读的内容**，然后复制匹配的模板并开始填充。
