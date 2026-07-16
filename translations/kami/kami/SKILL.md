<!-- source-sha256: 5b659e98b628dfb9951dff9d96ebac051866480202250c017e038f2732c1d6ea -->
---
name: kami
description: '排版专业文档和产品落地页：简历、单页文档、白皮书、信件、作品集、幻灯片、落地页。暖色羊皮纸、墨蓝色强调色、以衬线字体为主的层级。中文使用 TsangerJinKai02，英文使用 Charter，日文使用 YuMincho（尽力支持）。当出现 "做 PDF / 排版 / 一页纸 / 白皮书 / 作品集 / 简历 / PPT / slides / Marp / markdown slides / マークダウンのスライド / 落地页 / 官网 / landing page / product page"，或 "build me a resume / make a one-pager / design a slide deck / turn this into a PDF / make this presentable / create a landing page" 时触发。'
---

# kami · 紙

**紙 · かみ**——承载你的交付成果的纸张。

好内容值得用好纸承载。文档与落地页采用统一的设计语言：暖色羊皮纸画布、墨蓝色强调色、以衬线字体为主的层级，以及紧凑的编辑节奏。

属于 `Kaku · Waza · Kami`——Kaku 编写代码，Waza 训练习惯，**Kami 交付文档**。

**更新检查（非阻塞）。** 开始任务时，运行 `bash scripts/check-update.sh`。它每天最多执行一次只读版本检查；当有新版 kami 可用时，会输出一行信息。将该行转告用户，然后继续。它不会发送任何数据，在离线、沙箱环境或缺少 `curl` 时会静默失败。绝不能让它阻塞工作。

## 步骤 0 · 加载品牌配置（如果存在）

检查 `~/.config/kami/brand.md`（首选）或 `~/.kami/brand.md`（旧版后备）。如果找到，请阅读 `references/brand-profile.md`，了解完整的四层应用规范（占位符替换、会话默认值、视觉定制、习惯备注）及其六项护栏。如果不存在配置，则不中断并继续。

关键规则：明确提示 > 编辑判断 > 习惯备注 > frontmatter 默认值 > 内置默认值。配置只会静默补全缺失信息；绝不会覆盖当前对话。

## 步骤 0.5 · 用户项目风格扫描（选择启用）

仅当用户明确引用同级项目作为视觉参考时运行此步骤，例如："like my <project> site"、"match the style of <repo>"、"use the look from <directory>"。如果没有此类引用，则静默跳过。

触发后，在生成之前：

1. 定位所引用项目的样式文件：
   ```bash
   find <referenced-path> -maxdepth 4 \( -name "*.css" -o -name "tailwind.config.*" -o -name "theme.*" -o -name "tokens.*" \) | head -20
   ```
2. 提取：主要颜色值（hex / hsl）、字体栈、间距尺度、圆角尺度。优先采用 CSS 变量或设计令牌中声明的值，而不是内联字面量。
3. 将其作为 Layer C（视觉定制）合并进当前会话的品牌配置，而不是 Layer B（会话默认值）。不要覆盖明确的 `--brand` 标志，也不要覆盖用户在当前轮次中输入的值。
4. 继续之前，用一行报告："已扫描 <project>，提取 N 种颜色 / M 种字体；将其用作视觉参考。"

如果引用路径不存在、未找到类似 CSS 的文件，或提取结果会与用户当前消息中的明确值冲突，则跳过并回退到品牌配置默认值。

---

## 步骤 1 · 确定语言

**匹配用户的语言。** 中文 -> `*.html` / `slides-weasy.html`。英文 -> `*-en.html` / `slides-weasy-en.html`。日文 -> 尽力使用 CJK 路径（`.html` / `slides-weasy.html`），优先 JP Mincho，交付前进行视觉 QA。韩文 -> 尽力使用专用的 `*-ko.html` / `slides-weasy-ko.html` 系列，交付前进行视觉 QA。参考文档共用英文规范。

当语言不明确时（例如只有 "resume" 这样的单词命令），用一句话询问，不要猜测。

| 用户语言 | HTML 模板 | 幻灯片（默认 PDF） | 幻灯片（后备 PPTX） |
|---|---|---|---|
| 中文（主要支持） | `*.html` | `slides-weasy.html` | `slides.py` |
| 英文 | `*-en.html` | `slides-weasy-en.html` | `slides-en.py` |
| 日文（尽力支持） | `*.html` | `slides-weasy.html` | `slides.py` |
| 韩文（尽力支持） | `*-ko.html` | `slides-weasy-ko.html` | 不适用（仅在必须使用 PPTX 时使用 `slides-en.py`） |
| 其他语言（尽力支持） | 根据文字覆盖范围选择 CJK 或 EN 路径，然后手动验证 | 选择 `slides-weasy.html` 或 `slides-weasy-en.html`，然后手动验证 | 仅在必须使用 PPTX 时使用 `slides.py` / `slides-en.py` |

> 默认使用 WeasyPrint HTML 路径；仅当用户明确需要可编辑的演示文稿时，才回退到 PPTX（`slides*.py`）。

始终使用 `CHEATSHEET.md` 和 `references/*.md` 获取设计、写作、制作及图表指导。

仅当构建环境安装了可选的 `Pygments` 时，带有 `class="language-*"` 的代码块才会进行语法高亮。没有它，PDF 仍能正常渲染，代码块则保持单色。

## 步骤 1.5 · 意图提取（静默检查清单）

选择模板之前，确认以下四个维度均已明确。除非缺失 2 项以上且无法从上下文推断，否则不要询问。

| 维度 | 要提取的内容 | 示例 |
|---|---|---|
| **目的** | 为什么需要这份文档 | 说服投资者、协调内部团队，或促成候选人签约 |
| **受众** | 谁会阅读，以及他们已经知道什么 | 技术型 CTO（跳过基础知识）与非技术董事会（解释术语） |
| **约束** | 对长度、格式、语气或交付方式的硬性限制 | "最多一页"、"正式英文"、"可直接打印的 A4" |
| **成功标准** | 什么结果算成功 | 对方安排会议 / 批准预算 / 理解架构 |

规则：

- 如果对话已经回答某个维度，则静默跳过。
- 如果某个维度可以从文档类型推断（例如简历的目的始终是“获得面试机会”），则跳过。
- 如果确实有 2 项以上不明确，则用一个紧凑的问题一次询问（最多包含 2 个子问题）。
- 绝不要把四项全部作为清单询问。这是后台验证，而不是表单。

## 执行契约

创建或修改输出之前，锁定契约：语言、模板、输出格式、页数或长度目标、视觉验收检查及验证命令。用户请求足够明确时直接推断；仅当缺失字段会实质改变交付成果时才询问。

使用最接近的现有模板和验证路径。除非当前请求无法在没有它的情况下完成，否则不要新增模板、共享 CSS 层、依赖项、脚本标志或可选模式。

如果改动涉及 `SKILL.md`、模板、脚本、参考资料或包输入，请在交付前判断是否必须刷新 `dist/kami.zip`。只有包中包含变更后的文件，待发布行为才算就绪。

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

> **更新日志与发布说明**：上面的更新日志模板用于生成带样式的文档。GitHub 发布说明属于另一种交付成果；请通过 `/write` 使用发布说明模板模式。

> **落地页**：以屏幕为先的交互式模板。不输出 PDF。包含自动轮播的画廊、首屏入场动画、响应式断点（880px / 480px）及 prefers-reduced-motion 支持。可作为静态 HTML 部署到 Vercel / Netlify / 任意主机。代理填写 {{PLACEHOLDER}} 值和 HTML 注释块，然后保存为可直接提供服务的 `.html` 文件。

> **落地页配套文件**：进行生产级多语言部署时，将五个 `landing-page-*.example` 文件复制到主 HTML 旁边，移除 `.example` 后缀并填写占位符。它们涵盖 Vercel 重写与响应头、sitemap hreflang、robots AI 允许列表，以及供 AI 助手使用的 llms.txt + llms-full.txt。主 HTML 的 `<head>` 中已经包含匹配的 hreflang 和 og:locale；`landing-page-en.html` 末尾的 Accept-Language 重定向默认被注释，可选择启用。`{{SITE_ORIGIN}}` 是 `{{CANONICAL_URL}}` 的协议与主机部分（例如 `https://example.com`）。参见 `references/design.md` 第 11 节 «Companion assets»。

> **生产级产品站模式**：如果用户需要文档、帮助、发布、更新日志、路线图、法律页面或两种以上语言区域设置，请将其视为站点系统。填充模板之前，锁定产品类别、真实截图槽位、语言区域列表、配套文件、长内容页面以及生成器/检查需求。不要将项目专属发布产物、支付提供商、appcast 规则和私有本地路径放入 Kami。参见 `references/design.md` 第 11 节 «Product site system»。

> **文档页面**：当落地页扩展成文档或帮助站点时，使用 `references/design.md` 第 11 节 «Documentation site» 中的文档外壳：带 2px 品牌色竖线（而不是深色下划线）的粘性侧边栏导航、在平板断点以下隐藏的本页目录、宽度受限的正文区域，以及安静的无边框上一篇/下一篇导航（使用文本链接，而不是带边框的卡片）。构建时在深色代码表面完成高亮，不使用运行时 JS；纯代码始终是事实来源。

> 幻灯片：默认使用 `slides-weasy.html` / `slides-weasy-en.html` / `slides-weasy-ko.html`（WeasyPrint HTML → PDF）。仅当用户明确要求可编辑的 PPTX 文件时，才使用 `slides.py` / `slides-en.py`。仅当用户明确要求 Marp / markdown slides / 存放在 `.md` 文件中的演示文稿时，才使用 `assets/templates/marp/slides-marp(.md|.css)`。

> 演示文稿方法：起草幻灯片前阅读 design.md 第 8 节。生成或裁剪视觉素材之前，先勾勒标题顺序、证据形态和图片槽位。将面向受众的文案与视觉简报分开。Marp 专属约束位于 design.md §8 «Marp variant»。

### 决策树（询问前使用）

在提出一句话问题之前先遍历此树。仅当两个选项确实都适用时才询问。

| 信号 | 文档 |
|---|---|
| 长度目标未知 | 分类前询问“多少页” |
| ≤ 1 页 + 投资者 / 招聘人员 / 执行摘要受众 | 单页文档 |
| ≤ 1 页 + 正式通信（销售、招聘、辞职、备忘录） | 信件 |
| 1.5-2 页 + 职业叙事 + 项目要点 | 简历 |
| 3-6 页 + 项目展示 + 视觉内容较多 | 作品集 |
| 6-15 页 + 持续论证 + 视觉密度较低 | 长文档 |
| 演示流程 + 演讲支持 + 每页一个论断 | 幻灯片 |
| 财务 / 指标仪表板 + 投资论点 + 价格或风险观点 | 个股研报 |
| 按版本记录 + 发布事实 | 更新日志 |
| 在浏览器中展示产品 + 定价 + 截图 + FAQ | 落地页 |

适合用一句话澄清的歧义示例：

- "1.5 page career story with heavy visuals" -> 询问“简历还是作品集？”
- "2 page exec summary with metric tiles" -> 询问“单页文档还是个股研报？”
- "5 page argument with several charts" -> 询问“长文档还是作品集？”

先按决策树选择。只有决策树确实无法判断时才询问。

### 图表（基础组件，而非独立模板类型）

当用户要求在长文档 / 作品集 / 幻灯片中**嵌入图表**（而不是独立文档）时，使用 `assets/diagrams/`，而不是模板：

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

绘图前阅读 `references/diagrams.md`——其中包含选择指南、kami 令牌映射和 AI 粗制滥造反模式表。从模板中提取 `<svg>` 块，并将其放入长文档 / 作品集内的 `<figure>` 中。

绘图之前始终先问：**与这张图相比，一段写得好的文字是否会让读者学到更少？** 如果不会，就不要画图。

**根据数据自动选择图表。** 当内容包含数值数据时，选择图表类型并嵌入，无需等待用户指定。决策树如下（首个匹配项优先）：

| 数据形态 | 图表 |
|---|---|
| 包含 open/high/low/close 字段，或每日价格 | K 线图 |
| 包含加减贡献项，且这些项汇总成总数（bridge、waterfall、P&L） | 瀑布图 |
| 单个系列，数值合计约为 100%，项目 ≤ 6 | 环形图 |
| 单个系列，数值合计约为 100%，项目 ≥ 7 | 水平柱状图 |
| 两个或更多跨时间序列（月份、季度、年份） | 折线图 |
| 单个跨时间序列，数量变化幅度占主导（而非比率） | 柱状图 |
| 多个类别、相同时间快照、2 个以上系列 | 分组柱状图 |
| 2×2 战略或优先级定位 | 象限图 |
| 深度 ≥ 2 的层级数据 | 树状图 |
| 带决策分支的流程 | 流程图 |
| 涉及 ≥ 3 个参与者的跨团队或跨角色流程 | 泳道图 |
| 2-3 个群组之间的集合重叠或共享属性 | 维恩图 |
| 类别比较、单个系列、无时间轴 | 柱状图 |

当数据适合多种图表时，优先选择最清晰地展示差异的图表。始终嵌入 `<figure>`，并添加说明洞察而不只是数据范围的标题。

### 插图（使用宿主图片模型，而非内联 SVG）

上面的内联图表是手工组装的矢量 SVG。对于独立的光栅插图，或按 Kami 风格重绘图形、照片或截图，请将绘制工作交给宿主自身的图片生成功能。绝不要调用外部图片 API，也不要要求 API 密钥；渲染是宿主的工作。

- 如果当前宿主能够生成图片（例如 ChatGPT），请应用下面的简报并直接渲染图片。
- 如果无法生成（Claude、Codex、大多数编程代理），请将简报以文本形式输出，供用户粘贴到任意图片模型中。

简报：暖色羊皮纸（`#f5f4ed`）背景，绝不使用纯白；只使用一种强调色，即墨蓝色（`#1B365D`）；其他所有颜色均为带黄棕底色的暖灰色，不使用其他颜色；使用纤细的单线几何笔触和简单的扁平图标；不使用渐变、投影或 3D；标签采用衬线字体；留有充足空白，构图如同排版精良报告中的插图。

## 步骤 2.1 · 来源与素材检查

当文档依赖用户草稿之外的事实或素材时，请在提炼或填充内容之前执行此步骤。仅对于用户已经提供全部所需内容的个人草稿才跳过。

### 来源检查

当文档提及特定公司、产品、人物、发布日期、版本、融资轮次、指标、市场事实、技术规格或任何可能发生变化的当前事实时触发。

- 写作前优先使用一手来源：用户提供的材料、官方网站、文档、监管文件、新闻稿、应用商店页面或仓库发布记录
- 对驱动文档内容的事实，简短记录来源名称和日期
- 如果来源冲突，或无法快速核实某项事实，请询问用户，不要静默选择
- 除非经过核实，否则避免使用“最新”“近期”“全新”、版本号、发布日期或财务数字等带有时效性的说法

### 素材检查

当文档涉及公司、产品、项目、场所或个人品牌时触发。

排版前，确认能使主题具备辨识度的素材：

| 需求 | 何时必需 | 可接受内容 |
|---|---|---|
| Logo | 任何品牌文档 | 用户文件或官方 SVG/PNG |
| 产品图片 | 实物产品 / 场所 / 物件 | 官方图片、用户图片或明确标记的空缺 |
| UI 截图 | App / SaaS / 网站 / 工具 | 当前截图、官方产品图片或用户截取内容 |
| 品牌颜色 | 品牌单页文档 / 作品集 / 演示文稿 | 官方值、从素材提取的值，或保留 kami 墨蓝色 |
| 字体 | 仅当品牌排版很重要时 | 官方字体、接近的系统后备字体或 kami 默认字体 |

如果缺少必需项，请使用紧凑的空缺表并只询问一次。不要用通用图片、近似绘制的 Logo 或虚构值替代缺失素材。

Logo 后备规则：当请求中未指定 Logo，但品牌配置中存在 `logo` 路径时，按照 `references/brand-profile.md` Layer C 填充 `one-pager` / `portfolio` / `slides-weasy` 中已注释的 `.brand-logo` 槽位。将 `~` 展开为绝对路径；如果文件缺失或模板没有槽位，则保持注释状态并在没有 Logo 的情况下渲染（绝不插入损坏的图片）。当前请求中明确提供的 Logo 始终优先。

### 素材状态块

完成素材检查后，在继续之前输出结构化状态块。这是一次性的透明度展示，不是问题：

```
素材状态：
- Logo：OK assets/client-logo.svg
- 品牌颜色：OK #1B365D 已映射到 --brand
- 产品截图：MISSING（继续使用 kami 默认占位符）
- UI 截图：此文档类型不需要
```

使用 `OK`、`MISSING` 或 `not required`。如果缺少必需项且尚未收到用户输入，请使用空缺表询问一次；否则静默继续。

## 步骤 2.5 · 提炼原始内容（如适用）

**自动判断是否需要提炼。** 不要询问用户；根据输入自行判断：

| 跳过提炼（直接填充） | 执行提炼 |
|---|---|
| 内容具有与模板结构匹配的明确章节标签 | 没有章节结构的原始文本 |
| 指标已量化且带有单位 | 数字分散或仅为暗示，尚未提取 |
| 用户写了 "use this as-is" / "直接用这个" / "原封不动" | 用户粘贴了多来源材料集合（聊天 / 邮件线程 / 多份文档） |
| 内容数量与模板匹配（例如 4 项指标对应 4 张指标卡） | 内容数量与模板不匹配（过多或过少） |
| 语气统一，论断一致 | 来源之间存在冲突论断或重复事实 |

拿不准时就执行提炼。提炼成本很低；因文档结构不匹配而返工则不然。

当用户提供**原始材料**（会议记录、思维倾倒、不同格式的现有文档、聊天记录、零散要点）时：

1. **提取**：找出每项事实论断、数字、日期、名称、来源、素材引用和行动项
2. **分类**：将每项提取内容映射到目标模板的章节（各文档类型的章节结构参见 `references/writing.md`）
3. **检查空缺**：列出模板所需但原始内容缺少的项目——包括缺失事实、缺失证据和缺失素材
4. **询问一次**：与用户分享空缺表。不要猜测并填补空缺。

空缺检查示例：

| 模板需要 | 已找到 | 缺失 |
|---|---|---|
| 4 张指标卡 | "8 years"、"50-person team" | 另外 2 项可量化成果 |
| 3-5 个核心项目 | 提及 2 个 | 至少再提供 1 个带结果的项目 |
| 素材 | 已提供 Logo 文件 | 产品截图来源 |

然后，携带结构化、提炼后的内容，继续执行步骤 2.6（幻灯片）或排版说明（其他所有文档类型）。

## 步骤 2.6 · 演示文稿预检（仅限幻灯片）

除幻灯片外，所有其他文档类型均跳过此步骤。

### 路径选择

默认使用 WeasyPrint HTML 路径。仅当用户明确要求可编辑的 PPTX 文件时切换到 pptx。仅当用户明确要求 Marp / markdown slides 时切换到 Marp。

| 路径 | 模板 | 何时使用 |
|---|---|---|
| WeasyPrint HTML → PDF（默认） | `slides-weasy.html` / `slides-weasy-en.html` / `slides-weasy-ko.html` | 除非要求 PPTX 或 Marp，否则适用于所有情况 |
| python-pptx → PPTX（后备） | `slides.py` / `slides-en.py` | 用户明确要求可编辑的 PPTX |
| Marp Markdown（变体） | `assets/templates/marp/slides-marp.md`（+ `slides-marp.css`）/ `slides-marp-en.md`（+ `slides-marp-en.css`） | 用户明确要求 Marp、"markdown slides" 或 `.md` 演示文稿。随附的 `.md` 是 Kami Marp 本身可工作的演示；复制它、替换内容并保留结构。通过本地 `marp` CLI 渲染；未捆绑。 |

### 页面尺寸

默认为 `280mm 158mm`。仅当用户提到长度或密度约束时才询问。

| 尺寸 | 何时使用 |
|---|---|
| `280mm 158mm` | 默认；适合大多数演示文稿 |
| `297mm 167mm` | 用户希望空间稍大 |
| `338mm 190mm` | 内容密集的幻灯片，或每页包含大量数据点 |

### 内容预检

起草任何幻灯片前，与用户确认以下事项。一次性询问所有事项，已经回答的则跳过：

| # | 问题 |
|---|---|
| 1 | **受众 + 场合**——现场有哪些人，是现场主题演讲、投资者一对一沟通，还是异步分享链接？ |
| 2 | **长度目标**——演示时长或幻灯片数量？（15 分钟：约 10 页 / 30 分钟：约 20 页 / 45 分钟：约 25-30 页） |
| 3 | **来源材料**——哪些内容已经准备好：大纲、文档、笔记、数据？ |
| 4 | **图片**——是否有截图、图表、Logo 或产品图片；哪些幻灯片需要真实证据槽位；是否需要单独的视觉简报？ |
| 5 | **硬性约束**——品牌颜色、必需的 Logo、是否必须使用 PPTX、是否有必须存在的幻灯片？ |
| 6 | **格式确认**——是幻灯片演示文稿，还是看起来像演示文稿的单页文档？ |

起草任何落地页或产品站之前，从来源材料中锁定以下事项。仅当缺失项会改变交付成果时询问一次：

| # | 锁定项 |
|---|---|
| 1 | **产品类别**——首屏类别：app、CLI、terminal、utility、skill、template system，或用户提供的其他标签。 |
| 2 | **真实素材**——可用的产品截图、Logo、图标或 UI 截图，并映射到 hero/gallery/feature/social 槽位。缺失素材必须保持标记，不得用图库图片替代。 |
| 3 | **站点形态**——单页，还是首页加 docs/help/releases/changelog/roadmap/legal 页面？ |
| 4 | **语言区域**——准确的语言区域列表、规范路径，以及是否需要生成器/检查模式。 |
| 5 | **事实界面**——必须保持同步的安装路径、价格、版本、支持渠道、FAQ、`llms.txt` 和 `llms-full.txt`。 |

### 幻灯片内容规则

- 幽灵演示文稿测试：只按顺序阅读幻灯片标题。它们必须能讲清论证；否则先修正标题或结构，再处理样式
- 每页只使用一种证据形态：图表、表格、截图、代码、引语或结论。将混合证据拆分，不要挤在同一页
- 面向受众的文案保持干净：标题、正文和说明中绝不能包含图片提示词、裁剪说明或生成备注
- 不使用章节分隔页：使用 `.eyebrow` 标记章节编号，而不是专门的蓝色背景页面
- 不使用 CJK 括号：将 `（...）` 替换为 `·` 或 `,`
- 每个要点只占一行：精简到能够放下一行
- 2×2 布局：使用 `table.t2x2`，而不是 CSS Grid
- 固定结论：使用位于 `position: absolute; bottom: 12mm` 的 `.co`

这些规则同样适用于 Marp 演示文稿。Marp 专属语法参见 `references/design.md` §8 «Marp variant»。

## 步骤 2.7 · 排版说明（透明、非阻塞）

加载规范并填充模板之前，写一段简短的编辑式说明，陈述排版意图：模板选择、长度目标、叙事弧线、嵌入图表、素材状态和输出格式。使用与文档相同的语言。控制在 80 字以内，采用段落形式，而不是状态面板。随后立即继续，不要等待。

示例（中文）：

> 排版意图：Equity Report 中文版，2 页 A4。先立论与目标价，进入估值 (DCF 与可比公司)，落于催化剂与风险。中段嵌一张营收趋势折线和 FY26 收入桥瀑布。Logo 已就位，产品图暂缺，header 改走纯文字。输出 HTML 与 PDF。

示例（英文）：

> 排版意图：Equity Report（英文版），两页 A4。先提出投资论点与目标价，再介绍估值（DCF 与可比公司），最后总结催化剂和风险。文档中段放置一张营收折线图和一张 FY26 瀑布图。Logo 已就绪；缺少产品图片，因此页眉仅使用文字。输出：HTML 和 PDF。

该说明用于保持透明，而不是请求批准。如果用户提出异议，则进行调整；否则继续执行步骤 3。

---

## 步骤 3 · 加载适量规范

选择与任务匹配的层级。默认使用能够覆盖工作的最低层级。

| 层级 | 何时使用 | 阅读内容 |
|---|---|---|
| **仅内容** | 更新文本、替换要点、翻译现有文档。CSS 保持不变。 | 仅 `CHEATSHEET.md` |
| **排版微调** | 调整间距、移动章节、在规范内修改字号。涉及 CSS。 | `CHEATSHEET.md` + 模板（令牌已内联） |
| **新文档** | 从零开始或根据原始内容构建。 | 完整设计规范 + 写作规范 + 模板 |
| **简历内容** | 简历专属要点结构、项目描述方式、范围-结果-影响规则。 | `resume-writing.md` + 模板 |
| **来源 / 素材** | 公司、产品、市场、发布、融资、规格或品牌主题。 | `writing.md` 来源规则 + 用户/来源材料 |
| **演示文稿（>20 页）** | 需要 Part Divider、Code Cards、章节标题的长演示文稿。 | 完整设计规范 + Deck Recipe（design.md 第 8 节） |
| **故障排除** | 渲染错误、字体问题、页面溢出。 | `production.md`（如果原因是 CSS，还需设计规范） |
| **反模式** | 交付前审查 AI 生成的草稿。 | `anti-patterns.md`（六类检查清单） |
| **图表** | 在文档中嵌入 SVG。 | 仅 `diagrams.md`（具有自己的令牌映射） |

如果工作实际需要比初始层级更多的内容，可以随时在任务中途升级。

完整规范文件如下：

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
- 避免 `references/anti-patterns.md` 中列出的模式：空洞、虚构、模仿、过度、来源缺口、语气污染
- **填充前，阅读 `writing.md` 中 "Quality bars by document type" 一节里对应文档类型的质量标准。** 结构必不可少，但仅有结构还不够：简历要点需要 Action + Scope + Result + Business Outcome；个股研报需要差异化预期 + 量化催化剂；幻灯片需要论断-证据式标题。达到质量标准与填满所有占位符同样重要。

### 不要生成

以下是最常见的 AI 文档失败模式。完整列表参见 `references/anti-patterns.md`。

- 不要在最终文档中留下占位文本（"Lorem ipsum"、"[Insert here]"、"TBD"）
- 不要虚构指标、财务数据或统计数据；使用 `[DATA NEEDED: description]` 标记空缺
- 不要用图库图片描述作为图片占位符（"A diverse team collaborating in a modern office"）
- 不要为了填满模板槽位而填充内容（只有 3 个真实项目的简历不需要虚构到 5 个）
- 不要写仅仅以句子形式复述自身标题的段落

### 填写 PDF 元数据（WeasyPrint 会将其写入 PDF）

每个模板的 `<head>` 中都有元数据占位符。构建前填写全部四项：

| 占位符（中文） | 占位符（英文） | 规则 |
|---|---|---|
| `{{作者}}` | `{{AUTHOR}}` | 简历/信件/作品集：使用文档中的人名。其他类型：保持原样（构建脚本会从 git config 或 env 推断） |
| `{{摘要}}` | `{{DESCRIPTION}}` | 从前 2 个段落中提取一句话（≤150 个字符） |
| `{{关键词}}` | `{{KEYWORDS}}` | 从标题 + 章节标题中提取 3-5 个关键词，以逗号分隔 |
| `{{文档标题}}` / `{{信件主题}}` 等 | `{{DOC_TITLE}}` / `{{LETTER_SUBJECT}}` 等 | 从 H1 或 `.header .title` 文本推断 |

`<meta name="generator" content="Kami">` 已在模板中固定；不要修改。

**作者推断**：`build.py` 会自动按以下顺序设置 PDF `/Author` 元数据：

1. `git config user.name`（主要）
2. `KAMI_AUTHOR` 环境变量（后备）
3. `"Kami"`（最终后备）

对于个人文档（简历/信件/作品集），HTML `<meta name="author">` 应与内容中的人名一致。对于非个人文档（单页文档/长文档），保持占位符不变，让构建脚本进行推断。

## 步骤 4.1 · 每页密度目标（仅限多页模板）

适用：slides-weasy / long-doc / portfolio / equity-report / changelog。不适用 resume / one-pager / letter（这些有独立的长度合约）。

正文页填充率目标 60-80%。封面 / 目录 / 末尾署名页豁免。这条规则解决的是 AI 生成多页文档时最常见的 draft 缺陷：把内容拆得太散，结果几页都填不满。

### 每页项目数量契约

| 模板 | 典型正文页 | 硬性下限（低于此值则合并） |
|---|---|---|
| slides-weasy | 1 个论断标题 + 3-5 个支撑项，或 1 张图表 + 2-3 个标注 | <3 个项目且没有图表 → 合并到相邻幻灯片 |
| long-doc | 1 个章节标题 + 2-4 个段落 + 最多 1 张插图 | 章节渲染后不足页面的 <40% → 合并到相邻章节 |
| portfolio | 1 个项目标题 + 1 张主图 + 3-5 个成果要点 | 没有图片且成果少于 3 项 → 与相邻项目合并 |
| equity-report | 1 个章节 + 1 个表格/图表 + 支撑文本 | 页面上只有一个 2 行表格 → 合并章节 |
| changelog | 1 个版本块 + 4-8 条记录 | 版本少于 4 条记录 → 与上一版本放在同一页 |

### 稀疏页面合并规则

最终确定之前扫描草稿。任何正文页若预计渲染后的填充率低于 50%，请依次采取以下措施之一：

1. 向上合并到前一个章节。
2. 向下合并到后一个章节。
3. 将列表升级为值得占用该空间的小型图表或表格。
4. 将 `.co` 标注固定到底部（仅限 slides-weasy）。固定标注上方的空白是有意设计，而不是稀疏。

禁止用以下方式“填满”稀疏页面：添加填充性文字、将标题重复为句子、虚构统计数据、换一种说法复述前一页。如果合并方案都不适用，这一页本身就不应存在。

### 末页豁免

最后一张正文页允许保持 40-60% 的填充率。强行平衡末页通常意味着填充内容。版权说明 / 结束页可以采用任意填充率。

### 构建后验证

```bash
python3 scripts/build.py --check-density   # flags >25% (WARN) / >50% (SPARSE) trailing whitespace
```

如果正文页（非封面、非末页）出现 SPARSE 警告，请将其视为草稿缺陷，并按合并规则重新编写。

## 步骤 4.5 · 自动选择输出格式

不要询问用户要导出哪种格式。根据上下文决定：

| 信号 | 输出 | 原因 |
|---|---|---|
| 任何文档请求 | HTML + PDF | PDF 是默认交付成果，HTML 是源文件 |
| Slides / PPT / deck | HTML + PDF + PPTX | 演示文稿需要可投影格式 |
| "分享" / "发朋友圈" / "share" / "post" / "preview" | + PNG | 社交平台和消息应用需要图片 |
| "嵌入" / "插图" / "embed in another doc" | 仅 PNG | 用作其他文档中的素材 |
| 用户明确指定格式 | 遵循用户要求 | 明确请求优先于自动选择 |

文档模板始终交付 PDF。落地页交付可直接提供服务的静态 HTML 文件。幻灯片附带 PPTX。分享场景附带 PNG。用户不应需要考虑格式问题。

## 步骤 5 · 构建与验证

```bash
python3 scripts/build.py --verify           # build all templates + page count + font check + slides
python3 scripts/build.py --verify resume-en # single target full verification
python3 scripts/build.py landing-page        # screen-first static HTML template check
python3 scripts/build.py --verify slides    # single slide deck verification
python3 scripts/build.py --check-placeholders path/to/filled.html
python3 scripts/build.py --check-resume-balance path/to/resume.pdf
python3 scripts/build.py --check-density              # page whitespace scanner (skips cover)
python3 scripts/build.py --check            # CSS rule violations only (fast, no build)
python3 scripts/build_metadata.py --check   # Codex plugin mirror + marketplace drift check
```

> **屏幕验证**：`--check-density` 是打印输出门禁。对于屏幕输出（落地页或文档页面），请改为在每种语言区域下以 375px 和 1280px 截取渲染页面，并在交付前检查孤行。参见 `references/design.md` 第 11 节 «Responsive screenshot verification»。

源模板有意保留 `{{...}}` 字段。对完成后的文档运行占位符检查，而不是对模板库运行。

视觉异常（标签双重矩形、字体后备、分页问题）-> `production.md` 第 4 部分。

### 维护者模式检查

仅在维护此仓库或发布包时使用这些检查，不要用于普通文档生成。

- 如果商城元数据、生成的插件镜像、版本选择或安装路径发生变化，请运行 `python3 scripts/build_metadata.py --check`；对于 Codex 安装行为，还应使用隔离的 `CODEX_HOME=/tmp/...`，通过 `codex plugin marketplace add <path>`、`codex plugin add kami@kami` 和 `codex plugin list` 进行冒烟测试。
- 如果 `SKILL.md`、模板、脚本、参考资料或其他包输入发生变化，且相关行为通过 skill 包发布，请运行 `bash scripts/package-skill.sh`，并在交付前检查 `dist/kami.zip`。
- 如果刷新了 GitHub release 资源，请下载已上传的 `kami.zip`，并将其 ZIP 条目名称和每个条目的 SHA-256 摘要与本地 `dist/kami.zip` 比较；页面文字、文件大小和容器哈希均不足以完成验证。

## 字体

**中文**

- 主要衬线字体：TsangerJinKai02-W04.ttf（400 字重）+ TsangerJinKai02-W05.ttf（500 字重，真正的粗体）
- 模板使用两条 @font-face 声明：W04 用于正文，W05 用于标题
- 两个文件均为商业字体。将它们保留在仓库中用于本地预览和 CDN 后备，但不要将其捆绑进 Claude Desktop skill ZIP
- 模板内置后备链：Source Han Serif SC -> Noto Serif CJK SC -> Songti SC -> STSong -> Georgia

**日文（尽力支持）**

- 使用 CJK 模板路径，目前还没有专用的 `-ja` 模板
- 优先使用 JP Mincho 的字体栈：YuMincho -> Hiragino Mincho ProN -> Noto Serif CJK JP -> Source Han Serif JP -> TsangerJinKai02 -> serif
- 交付前对换行、标点节奏和强调字重进行视觉验证

**韩文（尽力支持）**

- 专用 `-ko` 模板使用 Source Han Serif K Regular / Medium，并在每个后备字体栈中保留真实的 OTF 字体族名称 `Source Han Serif KR`
- 后备字体：Noto Serif KR / Apple SD Gothic Neo / AppleMyungjo / Charter / Georgia
- OTF 文件采用 OFL 许可证，并纳入版本控制以供本地预览 / CDN 后备，但会从 Claude Desktop skill ZIP 中排除，以保持较小的包体积

**英文**

- 单一衬线字体：Charter（系统捆绑于 macOS/iOS），同时用于标题和正文
- 不单独使用无衬线字体：`--sans: var(--serif)`，每页一种字体
- 后备字体：Georgia（跨平台）/ Palatino / Times New Roman

将字体文件放在 HTML 旁边并使用相对 `@font-face` 路径，是最稳定的设置。`scripts/package-skill.sh` 会从 Claude Desktop ZIP 中排除大型 CJK 字体文件，因此上传包会保持在 6MB 包大小上限以内。始终上传该 `package-skill.sh` 的输出，绝不要手工压缩整个检出目录（纳入版本控制的 CJK 字体会使其过大，Claude Desktop 将拒绝上传）。

**字体自动恢复（Claude Desktop）**

构建中文或韩文文档之前，确保字体存在。该脚本会尝试多个 CDN 来源，并进行重试和大小验证：

```bash
bash scripts/ensure-fonts.sh
```

它会下载到 XDG 用户字体目录（`${XDG_DATA_HOME:-~/.local/share}/fonts/kami`，可通过 `KAMI_FONT_DIR` 覆盖），而**不会**下载到 skill 的 `assets/fonts`——这样可使已安装的 skill 保持较小，确保 Claude Desktop 永远不会触发其大小限制。fontconfig 默认会扫描该目录，因此 WeasyPrint 能在那里找到 `TsangerJinKai02` 和 `Source Han Serif K`；在线渲染则回退到 jsDelivr `@font-face` URL。构建前运行一次。如果所有来源都失败，脚本会输出各语言的替代方案。

## 反馈协议

当用户提供**模糊的视觉反馈**（"looks off"、"太挤了"、"not elegant"）时，不要猜测。结合当前值反问：

| 用户说 | 询问内容 |
|---|---|
| "太挤了" / "too cramped" | 哪个元素？行高（当前：X）？内边距（当前：Y）？页边距？ |
| "太松了" / "too loose" | 相同方向，反向调整 |
| "颜色不对" / "color feels wrong" | 哪个元素？品牌蓝使用过度？某种灰色显得太冷？ |
| "不够好看" / "not polished" | 字体渲染？对齐？空白分布？层级不清晰？ |
| "看着不专业" / "unprofessional" | 内容措辞？还是排版（对齐、一致性）？ |

模板回复："X 当前设置为 Y。你希望选择 (a) [规范内的具体替代方案]，还是 (b) [另一种方案]？"

绝不要只说“我会调整间距”，却不指出具体属性及其新值。

---

## 不应使用此 skill 的情况

- 用户明确要求 Material / Fluent / Tailwind 默认风格——设计语言不同
- 需要深色 / 赛博朋克 / 未来主义美学（此设计刻意反未来）
- 需要饱和的多色设计（此设计只有一种强调色）
- 需要卡通 / 动画 / 插画风格（此设计属于编辑风格）
- Web 动态应用 UI（此设计面向印刷 / 静态文档）

---

下一步：**应用步骤 3 的层级表决定要阅读哪些内容**，然后复制匹配的模板并开始填充。
