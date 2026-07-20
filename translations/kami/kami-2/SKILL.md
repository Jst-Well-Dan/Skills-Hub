<!-- source-sha256: 37f27a1af7d5c2f8e6aaafcdff25d6cca69470728acd0dc72f290baf6c579b76 -->
---
name: kami
description: '排版专业文档与产品落地页：简历、单页文档、白皮书、信件、作品集、幻灯片、落地页。温暖的羊皮纸色调、墨蓝色强调色、以衬线字体为主的层级结构。中文使用 TsangerJinKai02，英文使用 Charter，日文使用 YuMincho（尽力支持）。当出现“做 PDF / 排版 / 一页纸 / 白皮书 / 作品集 / 简历 / PPT / slides / Marp / markdown slides / マークダウンのスライド / 落地页 / 官网 / landing page / product page”，或“build me a resume / make a one-pager / design a slide deck / turn this into a PDF / make this presentable / create a landing page”时触发。'
---

# kami · 紙

**紙 · かみ**——承载你的交付物的纸张。

好内容值得好纸张。文档与落地页共享一套设计语言：温暖的羊皮纸画布、墨蓝色强调色、以衬线字体为主的层级结构、紧凑的编辑节奏。

属于 `Kaku · Waza · Kami`——Kaku 编写代码，Waza 训练习惯，**Kami 交付文档**。

**更新检查（非阻塞）。** 开始任务时，运行 `bash scripts/check-update.sh`。它每天最多执行一次只读版本检查；若有新版 kami 可用，会输出一行提示。将该行转告用户，然后继续。它不会发送任何数据；在离线、沙箱环境或没有 `curl` 时会静默失败。绝不能让它阻塞工作。

## 步骤 0 · 加载品牌配置（如果存在）

检查 `~/.config/kami/brand.md`（首选）或 `~/.kami/brand.md`（旧版后备路径）。如果找到，请阅读 `references/brand-profile.md`，了解完整的四层应用规范（占位符替换、会话默认值、视觉定制、习惯备注）及其六条护栏。如果没有配置文件，则不中断并继续。

关键规则：明确提示 > 编辑判断 > 习惯备注 > frontmatter 默认值 > 内置默认值。配置文件只静默补全空缺，绝不覆盖当前对话。

## 步骤 0.5 · 用户项目样式扫描（选择启用）

仅当用户明确引用同级项目作为视觉参考时运行，例如：“like my <project> site”“match the style of <repo>”“use the look from <directory>”。没有此类引用时静默跳过。

触发后，在生成前：

1. 定位所引用项目的样式文件：
   ```bash
   find <referenced-path> -maxdepth 4 \( -name "*.css" -o -name "tailwind.config.*" -o -name "theme.*" -o -name "tokens.*" \) | head -20
   ```
2. 提取：主色值（hex / hsl）、字体栈、间距尺度、圆角尺度。优先使用 CSS 变量或设计令牌中声明的值，而非行内字面量。
3. 将其作为 C 层（视觉定制）合并到当前会话的品牌配置中，而不是 B 层（会话默认值）。不要覆盖明确的 `--brand` 标志或用户在本轮输入的值。
4. 继续前用一行报告：“已扫描 <project>，提取 N 种颜色 / M 种字体；将其用作视觉参考。”

如果引用路径不存在、未找到类似 CSS 的文件，或提取结果与用户当前消息中的明确值冲突，则跳过并回退到品牌配置默认值。

---

## 步骤 1 · 确定语言

**匹配用户的语言。** 中文 -> `*.html` / `slides-weasy.html`。英文 -> `*-en.html` / `slides-weasy-en.html`。日文 -> 尽力使用 CJK 路径（`.html` / `slides-weasy.html`），优先使用日文明朝体，交付前进行视觉质量检查。韩文 -> 尽力使用专用的 `*-ko.html` / `slides-weasy-ko.html` 系列，交付前进行视觉质量检查。参考文档共用英文规范。

如果存在歧义（例如只有“resume”这样的单词命令），用一句话询问，不要猜测。

| 用户语言 | HTML 模板 | 幻灯片（默认 PDF） | 幻灯片（后备 PPTX） |
|---|---|---|---|
| 中文（主要支持） | `*.html` | `slides-weasy.html` | `slides.py` |
| 英文 | `*-en.html` | `slides-weasy-en.html` | `slides-en.py` |
| 日文（尽力支持） | `*.html` | `slides-weasy.html` | `slides.py` |
| 韩文（尽力支持） | `*-ko.html` | `slides-weasy-ko.html` | 不适用（仅在必须使用 PPTX 时使用 `slides-en.py`） |
| 其他语言（尽力支持） | 根据文字覆盖范围选择 CJK 或 EN 路径，然后手动验证 | 选择 `slides-weasy.html` 或 `slides-weasy-en.html`，然后手动验证 | 仅在必须使用 PPTX 时使用 `slides.py` / `slides-en.py` |

> 默认使用 WeasyPrint HTML 路径；仅当用户明确需要可编辑幻灯片时，才回退到 PPTX（`slides*.py`）。

设计、写作、生产和图表指导始终使用 `CHEATSHEET.md` 与 `references/*.md`。

带有 `class="language-*"` 的代码块仅在构建环境安装了可选的 `Pygments` 时才会高亮。即使没有它，PDF 仍能正常渲染，代码块只会保持单色。

## 步骤 1.5 · 意图提取（静默检查清单）

选择模板之前，确认以下四个维度清晰。除非缺失 2 个以上且无法从上下文推断，否则不要询问。

| 维度 | 要提取的内容 | 示例 |
|---|---|---|
| **目的** | 此文档为何存在 | 说服投资者、协调内部团队，还是促成候选人签约 |
| **受众** | 谁会阅读，以及他们已经知道什么 | 技术型 CTO（跳过基础知识）与非技术董事会（解释术语） |
| **约束** | 对长度、格式、语气或交付方式的硬性限制 | “最多一页”“正式英文”“可直接印刷的 A4” |
| **成功标准** | 什么结果才算成功 | 他们安排会议 / 批准预算 / 理解架构 |

规则：
- 如果对话已经回答某个维度，静默跳过。
- 如果可以从文档类型推断某个维度（例如简历的目的始终是“获得面试机会”），则跳过。
- 如果确实有 2 个以上维度不清楚，用一个紧凑问题询问（最多包含 2 个子问题）。
- 绝不要把四个问题全部作为检查清单询问。这是后台验证，不是表单。

## 执行契约

创建或修改输出前，锁定契约：语言、模板、输出格式、页数或长度目标、视觉验收检查和验证命令。用户请求清晰时直接推断；仅当缺失字段会实质性改变交付物时才询问。

使用最接近的现有模板和验证路径。除非当前请求在没有它的情况下无法完成，否则不要添加新模板、共享 CSS 层、依赖、脚本标志或可选模式。

如果改动涉及 `SKILL.md`、模板、脚本、参考资料或软件包输入，请在交付前判断是否必须刷新 `dist/kami.zip`。在软件包包含变更文件之前，可交付行为尚未就绪。

---

## 步骤 2 · 选择文档类型

| 用户说 | 文档 | 中文模板 | 英文模板 | 韩文模板 |
|---|---|---|---|---|
| “one-pager / 方案 / 执行摘要 / exec summary” | 单页文档 | `one-pager.html` | `one-pager-en.html` | `one-pager-ko.html` |
| “white paper / 白皮书 / 长文 / 年度总结 / technical report” | 长文档 | `long-doc.html` | `long-doc-en.html` | `long-doc-ko.html` |
| “formal letter / 信件 / 辞职信 / 推荐信 / memo” | 信件 | `letter.html` | `letter-en.html` | `letter-ko.html` |
| “portfolio / 作品集 / case studies” | 作品集 | `portfolio.html` | `portfolio-en.html` | `portfolio-ko.html` |
| “resume / CV / 简历 / 履歴書” | 简历 | `resume.html` | `resume-en.html` | `resume-ko.html` |
| “slides / PPT / deck / 演示” | 幻灯片 | `slides-weasy.html` | `slides-weasy-en.html` | `slides-weasy-ko.html` |
| “个股研报 / equity report / 估值分析 / investment memo / 股票分析” | 个股研报 | `equity-report.html` | `equity-report-en.html` | `equity-report-ko.html` |
| “更新日志 / changelog / release notes / 版本记录” | 更新日志 | `changelog.html` | `changelog-en.html` | `changelog-ko.html` |
| “landing page / 落地页 / 官网 / product page / 产品页” | 落地页 | `landing-page.html` | `landing-page-en.html` | `landing-page-ko.html` |

> **更新日志与发行说明**：上面的更新日志模板用于生成带样式的文档。GitHub 发行说明是另一种交付物；请通过 `/write` 使用发行说明模板模式。

> **落地页**：屏幕优先的交互式模板。不输出 PDF。包含自动轮播的图库、首屏入场动画、响应式断点（880px / 480px）和减少动态效果偏好支持。可将静态 HTML 部署到 Vercel / Netlify / 任意主机。代理填充 {{PLACEHOLDER}} 值和 HTML 注释块，然后保存为可直接提供服务的 `.html` 文件。

> **落地页配套文件**：对于生产环境中的多语言部署，将五个 `landing-page-*.example` 文件复制到主 HTML 旁边，移除 `.example` 后缀并填充占位符。它们涵盖 Vercel 重写与响应头、站点地图 hreflang、robots AI 允许列表，以及供 AI 助手使用的 llms.txt + llms-full.txt。主 HTML 的 `<head>` 中已包含匹配的 hreflang 和 og:locale；`landing-page-en.html` 末尾的 Accept-Language 重定向默认被注释，需要选择启用。`{{SITE_ORIGIN}}` 是 `{{CANONICAL_URL}}` 的协议与主机部分（例如 `https://example.com`）。参见 `references/design.md` 第 11 节《配套资源》。

> **生产级产品站点模式**：如果用户需要文档、帮助、发行版、更新日志、路线图、法律页面或两种以上语言区域，请将其视为站点系统。填充模板前，锁定产品类别、真实截图位置、语言区域列表、配套文件、长内容页面和生成器/检查需求。不要把项目专用的发行产物、支付服务商、appcast 规则和私有本地路径放入 Kami。参见 `references/design.md` 第 11 节《产品站点系统》。

> **文档页面**：当落地页扩展为文档或帮助站点时，使用 `references/design.md` 第 11 节《文档站点》中的文档外壳：带有 2px 品牌色导轨的粘性侧栏导航（不是深色下划线）、在平板断点以下隐藏的本页目录、受约束的正文行宽，以及安静、无边框的上一篇/下一篇导航（文本链接，而非带边框的卡片）。构建时在深色代码表面上高亮代码，运行时无需 JS；纯文本代码始终是真实来源。

> 幻灯片：默认使用 `slides-weasy.html` / `slides-weasy-en.html` / `slides-weasy-ko.html`（WeasyPrint HTML → PDF）。仅当用户明确要求可编辑的 PPTX 文件时，才使用 `slides.py` / `slides-en.py`。仅当用户明确要求 Marp / markdown slides / 存放在 `.md` 文件中的幻灯片时，才使用 `assets/templates/marp/slides-marp(.md|.css)`。

> 幻灯片方案：起草幻灯片前，阅读 design.md 第 8 节。生成或裁剪视觉素材前，先勾勒标题序列、证据形态和图片位置。将面向受众的文案与视觉简报分开。Marp 专用约束位于 design.md §8《Marp 变体》。

### 决策树（询问前使用）

在提出一句话问题前先走完此决策树。仅当两个选项确实都适用时才询问。

| 信号 | 文档 |
|---|---|
| 长度目标未知 | 分类前询问“需要多少页” |
| ≤ 1 页 + 投资者 / 招聘人员 / 执行摘要受众 | 单页文档 |
| ≤ 1 页 + 正式通信（销售、招聘、辞职、备忘录） | 信件 |
| 1.5-2 页 + 职业叙事 + 项目要点 | 简历 |
| 3-6 页 + 项目展示 + 视觉内容较多 | 作品集 |
| 6-15 页 + 持续论证 + 视觉密度较低 | 长文档 |
| 演示流程 + 演讲支持 + 每页一个论点 | 幻灯片 |
| 财务 / 指标仪表板 + 投资论点 + 价格或风险观点 | 个股研报 |
| 按版本记录 + 发行事实 | 更新日志 |
| 面向浏览器的产品展示 + 定价 + 截图 + 常见问题 | 落地页 |

足以提出一句话问题的歧义示例：
- “1.5 page career story with heavy visuals” -> 询问“简历还是作品集？”
- “2 page exec summary with metric tiles” -> 询问“单页文档还是个股研报？”
- “5 page argument with several charts” -> 询问“长文档还是作品集？”

先根据决策树选择。仅当决策树确实无法判断时才询问。

### 图表（基本元素，不是独立模板类型）

当用户要求在长文档 / 作品集 / 幻灯片中加入**图表**（而不是独立文档）时，请使用 `assets/diagrams/`，而非模板：

| 用户说 | 图表 | 模板 |
|---|---|---|
| “架构图 / architecture / 系统图 / components diagram” | 架构图 | `assets/diagrams/architecture.html` |
| “架构全景 / architecture board / 平台全景 / 系统大图 / five-layer panorama” | 架构全景图 | `assets/diagrams/architecture-board.html` |
| “流程图 / flowchart / 决策流 / branching logic” | 流程图 | `assets/diagrams/flowchart.html` |
| “象限图 / quadrant / 优先级矩阵 / 2×2 matrix” | 象限图 | `assets/diagrams/quadrant.html` |
| “柱状图 / bar chart / 分类对比 / grouped bars” | 柱状图 | `assets/diagrams/bar-chart.html` |
| “折线图 / line chart / 趋势 / 股价 / time series” | 折线图 | `assets/diagrams/line-chart.html` |
| “环形图 / donut / pie / 占比 / 分布结构” | 环形图 | `assets/diagrams/donut-chart.html` |
| “状态机 / state machine / 状态图 / lifecycle” | 状态机 | `assets/diagrams/state-machine.html` |
| “时间线 / timeline / 里程碑 / milestones / roadmap” | 时间线 | `assets/diagrams/timeline.html` |
| “泳道图 / swimlane / 跨角色流程 / cross-team flow” | 泳道图 | `assets/diagrams/swimlane.html` |
| “树状图 / tree / hierarchy / 层级 / 组织架构” | 树状图 | `assets/diagrams/tree.html` |
| “分层图 / layer stack / 分层架构 / OSI / stack” | 分层图 | `assets/diagrams/layer-stack.html` |
| “维恩图 / venn / 交集 / overlap / 集合关系” | 维恩图 | `assets/diagrams/venn.html` |
| “K 线 / candlestick / OHLC / 股价走势 / price history” | K 线图 | `assets/diagrams/candlestick.html` |
| “瀑布图 / waterfall / 收入桥 / revenue bridge / decomposition” | 瀑布图 | `assets/diagrams/waterfall.html` |

绘制前阅读 `references/diagrams.md`——其中包含选择指南、kami 令牌映射和 AI 粗制滥造反模式表。从模板中提取 `<svg>` 块，并将其放入长文档 / 作品集内的 `<figure>` 中。

对于**完整系统架构全景图**（在一个产物中呈现平台全景、控制平面、路线图或负责人映射），不要让单个架构图超过节点预算。从 `assets/diagrams/architecture-board.html` 开始，并遵循 `references/diagrams.md` 中的《架构全景图》章节：五个固定信息层，使用带状区域而非卡片，连线绝不贴在模块边缘，并在任何渲染前先列出结构大纲。

对于**由仓库维护的图表**（README 或文档站点架构图、“给项目画张架构图”，或更新用户仓库中已有的图表），请遵循 `references/diagrams.md` 中的《维护型图表资源》：先执行证据检查（现有 `prompt.md`、`index.html`、当前 PNG，然后是定义对象与边界的事实），保持三件套（`index.html` + 同名 PNG + `prompt.md`）一致，编码已交付 / 构建中 / 未来的成熟度，并在每次修改 HTML 后重新导出 PNG。绝不要凭记忆重绘现有图表，也绝不要手动编辑 PNG。

绘制前始终询问：**相比一段写得好的文字，这张图是否能让读者学到更多？** 如果不能，就不要画。

**根据数据自动选择图表。** 当内容包含数值数据时，选择图表类型并嵌入，无需等待用户指定。决策树（首个匹配项优先）：

| 数据形态 | 图表 |
|---|---|
| 包含开盘/最高/最低/收盘字段，或每日价格 | K 线图 |
| 包含加减贡献项，且加总为一个总值（桥接、瀑布、损益） | 瀑布图 |
| 一个系列，数值合计约为 100%，项目 ≤ 6 | 环形图 |
| 一个系列，数值合计约为 100%，项目 ≥ 7 | 水平柱状图 |
| 两个或更多跨时间系列（月、季度、年） | 折线图 |
| 一个跨时间系列，主要体现较大的数量变化（不是比率） | 柱状图 |
| 多个类别、同一时间快照、2 个以上系列 | 分组柱状图 |
| 2×2 战略或优先级定位 | 象限图 |
| 深度 ≥ 2 的层级数据 | 树状图 |
| 包含决策分支的流程 | 流程图 |
| 涉及 ≥ 3 个参与者的跨团队或跨角色流程 | 泳道图 |
| 2-3 个群组之间的集合重叠或共享属性 | 维恩图 |
| 类别对比、单一系列、没有时间轴 | 柱状图 |

当数据适合多种类型时，优先选择最清晰展示差异的类型。始终将其嵌入带有说明文字的 `<figure>` 中，说明文字应陈述洞察，而不只是数据范围。

### 插图（使用宿主图片模型，而非内联 SVG）

上面的内联图表是由你手工组装的矢量 SVG。对于独立的光栅插图，或按 Kami 风格重绘图形、照片或截图，请将绘制工作交给宿主自身的图片生成功能。绝不要调用外部图片 API，也不要要求密钥；渲染是宿主的工作。

- 如果当前宿主可以生成图片（例如 ChatGPT），请应用下方简报并直接渲染图片。
- 如果不能（Claude、Codex、大多数编码代理），请将简报以文本形式输出，以便用户粘贴到任意图片模型中。

简报：温暖的羊皮纸色（`#f5f4ed`）背景，绝不使用纯白；只使用一种强调色，即墨蓝色（`#1B365D`）；其余全部使用带黄棕底色的暖灰色，不使用其他颜色；细而单一的几何线条与简单的扁平图标；不使用渐变、投影或 3D；标签使用衬线字体；留白充足，构图如同排版精良报告中的插图。

## 步骤 2.1 · 来源与素材检查

当文档依赖用户草稿以外的事实或素材时，在提炼或填充内容前执行此步骤。仅当用户已为个人草稿提供全部所需内容时才跳过。

### 来源检查

当文档提到特定公司、产品、人物、发布日期、版本、融资轮次、指标、市场事实、技术规格或任何可能变化的当前事实时触发。

- 写作前优先使用一手来源：用户提供的材料、官方网站、文档、申报文件、新闻稿、应用商店页面或仓库发行版
- 对决定文档内容的事实，保留简短的来源名称和日期记录
- 如果来源相互冲突，或某项事实无法快速核实，请询问用户，不要静默选择
- 除非已经核实，否则避免使用“最新”“近期”“新”、版本号、发布日期或财务数据等具有时效性的表述

### 素材检查

当文档涉及公司、产品、项目、场所或个人品牌时触发。

布局前，确认能使主体易于识别的素材：

| 需求 | 何时必需 | 可接受来源 |
|---|---|---|
| Logo | 任何品牌文档 | 用户文件或官方 SVG/PNG |
| 产品图片 | 实体产品 / 场所 / 物体 | 官方图片、用户图片或明确标记的空缺 |
| UI 截图 | 应用 / SaaS / 网站 / 工具 | 当前截图、官方产品图片或用户截取 |
| 品牌颜色 | 品牌单页文档 / 作品集 / 幻灯片 | 官方值、从资源提取的值，或保留 kami 墨蓝色 |
| 字体 | 仅当品牌字体很重要时 | 官方字体、接近的系统后备字体或 kami 默认字体 |

如果缺少必需项，请使用紧凑的空缺表并只询问一次。不要用通用图片、近似绘制的 Logo 或虚构值替代缺失素材。

Logo 后备规则：当请求没有指定 Logo，但品牌配置中有 `logo` 路径时，根据 `references/brand-profile.md` 的 C 层填充 `one-pager` / `portfolio` / `slides-weasy` 中已注释的 `.brand-logo` 位置。将 `~` 展开为绝对路径；如果文件不存在或模板没有相应位置，则保持注释并在没有 Logo 的情况下渲染（绝不要插入损坏的图片）。当前请求中明确指定的 Logo 始终优先。

### 素材状态块

完成素材检查后，在继续之前输出结构化状态块。这是一次性的透明度展示，不是问题：

```
素材状态：
- Logo：OK assets/client-logo.svg
- 品牌颜色：OK #1B365D 已映射到 --brand
- 产品截图：MISSING（使用 kami 默认占位符继续）
- UI 截图：此文档类型不需要
```

使用 `OK`、`MISSING` 或 `not required`。如果缺少必需项且尚未收到用户输入，请通过空缺表询问一次；否则静默继续。

## 步骤 2.5 · 提炼原始内容（如适用）

**自动判断是否需要提炼。** 不要询问用户；根据输入判断：

| 跳过提炼（直接填充） | 执行提炼 |
|---|---|
| 内容已有与模板结构匹配的明确章节标签 | 没有章节结构的原始散文 |
| 指标已量化且带有单位 | 数字散落或仅被暗示，尚未提取 |
| 用户写了“use this as-is” / “直接用这个” / “原封不动” | 用户粘贴了多来源材料堆（聊天 / 邮件线程 / 多份文档） |
| 内容数量与模板匹配（例如 4 个指标对应 4 张指标卡） | 内容数量与模板不匹配（项目过多或过少） |
| 单一且连贯的叙述口吻，主张一致 | 来源之间存在相互冲突的主张或重复事实 |

如果不确定，就执行提炼。提炼成本很低；重做一份结构错位的文档则不然。

当用户交付**原始材料**（会议记录、头脑倾倒、不同格式的现有文档、聊天记录、零散要点）时：

1. **提取**：提取每一项事实主张、数字、日期、名称、来源、素材引用和行动项
2. **分类**：将每个提取项映射到目标模板的章节（各文档类型的章节结构见 `references/writing.md`）
3. **空缺检查**：列出模板需要但原始内容没有的项目——包括缺失事实、缺失证据和缺失素材
4. **只询问一次**：与用户共享空缺表。不要猜测并填补空缺。

空缺检查示例：

| 模板需要 | 已找到 | 缺失 |
|---|---|---|
| 4 张指标卡 | “8 年”“50 人团队” | 还需 2 项可量化成果 |
| 3-5 个核心项目 | 提到 2 个 | 至少还需 1 个带成果的项目 |
| 素材 | 已提供 Logo 文件 | 产品截图来源 |

然后带着结构化、已提炼的内容进入步骤 2.6（幻灯片）或布局说明（其他所有文档类型）。

## 步骤 2.6 · 幻灯片预检（仅限幻灯片）

除幻灯片外，所有文档类型均跳过此步骤。

### 路径选择

默认使用 WeasyPrint HTML 路径。仅当用户明确要求可编辑的 PPTX 文件时切换到 pptx。仅当用户明确要求 Marp / markdown slides 时切换到 Marp。

| 路径 | 模板 | 何时使用 |
|---|---|---|
| WeasyPrint HTML → PDF（默认） | `slides-weasy.html` / `slides-weasy-en.html` / `slides-weasy-ko.html` | 除非需要 PPTX 或 Marp，否则适用于所有情况 |
| python-pptx → PPTX（后备） | `slides.py` / `slides-en.py` | 用户明确要求可编辑的 PPTX |
| Marp Markdown（变体） | `assets/templates/marp/slides-marp.md`（+ `slides-marp.css`）/ `slides-marp-en.md`（+ `slides-marp-en.css`） | 用户明确要求 Marp、“markdown slides”或 `.md` 幻灯片。发布的 `.md` 是 Kami Marp 本身可运行的演示；复制它，替换内容并保留结构。通过本地 `marp` CLI 渲染；未捆绑。 |

### 页面尺寸

默认是 `280mm 158mm`。仅当用户提到长度或密度约束时才询问。

| 尺寸 | 何时使用 |
|---|---|
| `280mm 158mm` | 默认；适合大多数幻灯片 |
| `297mm 167mm` | 用户希望空间稍大 |
| `338mm 190mm` | 内容密集的页面或每页包含大量数据点 |

### 内容预检

起草任何幻灯片之前，向用户确认以下要点。一次性询问全部，跳过已有答案的项目：

| # | 问题 |
|---|---|
| 1 | **受众 + 场合**——房间里有哪些人？是现场主题演讲、投资者一对一交流，还是异步分享链接？ |
| 2 | **长度目标**——演示时长或幻灯片数量？（15 分钟：约 10 页 / 30 分钟：约 20 页 / 45 分钟：约 25-30 页） |
| 3 | **来源材料**——已经准备好哪些内容：大纲、文档、笔记、数据？ |
| 4 | **图片**——是否有截图、图表、Logo 或产品图片；哪些页面需要真实证据位置；是否需要单独的视觉简报？ |
| 5 | **硬性约束**——品牌颜色、必需 Logo、是否必须使用 PPTX、是否有必需页面？ |
| 6 | **格式确认**——是幻灯片，还是看起来像幻灯片的单页文档？ |

起草任何落地页或产品站点之前，从来源材料中锁定以下要点。仅当缺失项会改变交付物时询问一次：

| # | 锁定项 |
|---|---|
| 1 | **产品类别**——首屏类别：应用、CLI、终端、实用工具、技能、模板系统，或用户提供的其他标签。 |
| 2 | **真实素材**——可用的产品截图、Logo、图标或 UI 截图，并将其映射到首屏/图库/功能/社交位置。缺失素材必须保持标记，不能用图库图片替代。 |
| 3 | **站点形态**——单页，还是主页加文档/帮助/发行版/更新日志/路线图/法律页面？ |
| 4 | **语言区域**——确切的语言区域列表、规范路径，以及是否需要生成器/检查模式。 |
| 5 | **事实载体**——必须保持同步的安装路径、价格、版本、支持渠道、常见问题、`llms.txt` 和 `llms-full.txt`。 |

### 幻灯片内容规则

- 幽灵幻灯片测试：按顺序只读每页标题。它们必须能讲清论证；否则先修正标题或结构，再设置样式
- 每页只使用一种证据形态：图表、表格、截图、代码、引语或结论。将混合证据拆开，不要挤在一页
- 面向受众的文案应保持干净：标题、正文和说明文字绝不能包含图片提示词、裁剪说明或生成备注
- 不使用章节分隔页：用 `.eyebrow` 表示章节编号，不要使用专门的蓝色背景页面
- 不使用 CJK 括号：将 `（...）` 替换为 `·` 或 `,`
- 每条要点占一行：删减到一行能够容纳
- 2×2 布局：使用 `table.t2x2`，不要使用 CSS Grid
- 固定结论：使用 `.co`，设置 `position: absolute; bottom: 12mm`

这些规则同样适用于 Marp 幻灯片。Marp 专用语法见 `references/design.md` §8《Marp 变体》。

## 步骤 2.7 · 布局说明（透明、非阻塞）

加载规范并填充模板前，撰写一段简短的编辑式说明，陈述布局意图：模板选择、长度目标、叙事弧线、嵌入图表、素材状态和输出格式。使用与文档相同的语言。控制在 80 个词以内，写成散文，不要写成状态面板。随后立即继续，不要等待。

示例（中文）：

> 排版意图：Equity Report 中文版，2 页 A4。先立论与目标价，进入估值 (DCF 与可比公司)，落于催化剂与风险。中段嵌一张营收趋势折线和 FY26 收入桥瀑布。Logo 已就位，产品图暂缺，header 改走纯文字。输出 HTML 与 PDF。

示例（英文）：

> 布局意图：个股研报（英文版），两页 A4。以投资论点和目标价开篇，继而分析估值（DCF 与可比公司），最后落于催化剂和风险。文档中段放置一张营收折线图和一张 FY26 瀑布图。Logo 已就位；产品图片缺失，因此页眉保持纯文本。输出：HTML 和 PDF。

此说明用于提高透明度，而非请求批准。如果用户提出异议，则进行调整；否则继续执行步骤 3。

---

## 步骤 3 · 加载适量规范

选择与任务匹配的层级。默认使用能够覆盖工作的最低层级。

| 层级 | 何时使用 | 阅读内容 |
|---|---|---|
| **仅内容** | 更新文本、替换要点、翻译现有文档。CSS 保持不变。 | 仅 `CHEATSHEET.md` |
| **布局微调** | 调整间距、移动章节、在规范内改变字号。会修改 CSS。 | `CHEATSHEET.md` + 模板（令牌已内联） |
| **新文档** | 从零或根据原始内容构建。 | 完整设计规范 + 写作规范 + 模板 |
| **简历内容** | 简历专用要点结构、项目表述、范围-结果-成果规则。 | `resume-writing.md` + 模板 |
| **来源 / 素材** | 公司、产品、市场、发布、融资、规格或品牌主题。 | `writing.md` 来源规则 + 用户/来源材料 |
| **幻灯片（>20 页）** | 需要部分分隔、代码卡片和章节标题的长篇演示。 | 完整设计规范 + 幻灯片方案（design.md 第 8 节） |
| **故障排查** | 渲染错误、字体问题、页面溢出。 | `production.md`（如果 CSS 是原因，再加设计规范） |
| **反模式** | 交付前审查 AI 生成的草稿。 | `anti-patterns.md`（六类检查清单） |
| **图表** | 在文档中嵌入 SVG，或维护仓库所属的图表（三件套：HTML + PNG + prompt.md）。 | 仅 `diagrams.md`（包含自己的令牌映射） |

如果工作后来需要更多规范，可以随时在任务中途升级。

完整规范文件：
- 设计：`references/design.md`
- 写作（通用）：`references/writing.md`
- 写作（简历专用）：`references/resume-writing.md`
- 生产：`references/production.md`
- 图表：`references/diagrams.md`
- 反模式：`references/anti-patterns.md`

## 步骤 4 · 将内容填入模板

- 将模板复制到工作目录；不要从零编写 HTML
- **CSS 保持不变**，只编辑正文
- 内容遵循 `writing.md`：以数据取代形容词，以有辨识度的措辞取代行业陈词滥调
- 避免 `references/anti-patterns.md` 中列出的模式：空洞、虚构、模仿、过度、来源空缺、语气污染
- **填充前，阅读 `writing.md` 中“各文档类型的质量标准”章节，了解对应文档类型的质量标准。** 结构只是必要条件，并不充分：简历要点需要行动 + 范围 + 结果 + 业务成果；个股研报需要差异化认知 + 量化催化剂；幻灯片需要“论点-证据”式标题。达到质量标准与填满每个占位符同样重要。

### 不要生成

以下是最常见的 AI 文档失败模式。完整列表参见 `references/anti-patterns.md`。

- 最终文档中不要遗留占位文本（“Lorem ipsum”“[Insert here]”“TBD”）
- 不要虚构指标、财务数据或统计数据；用 `[DATA NEEDED: description]` 标记空缺
- 不要把图库图片描述当作图片占位符（“一支多元化团队在现代办公室中协作”）
- 不要为了填满模板位置而填充内容（只有 3 个真实项目的简历不需要虚构到 5 个）
- 不要写只是把标题改写成句子的段落

### 填写 PDF 元数据（WeasyPrint 会将其写入 PDF）

每个模板的 `<head>` 中都有元数据占位符。构建前填满全部四项：

| 占位符（中文） | 占位符（英文） | 规则 |
|---|---|---|
| `{{作者}}` | `{{AUTHOR}}` | 简历/信件/作品集：使用文档中的人物姓名。其他文档：保持原样（构建脚本会从 git 配置或环境变量推断） |
| `{{摘要}}` | `{{DESCRIPTION}}` | 从前两个段落中提取一句话（≤150 个字符） |
| `{{关键词}}` | `{{KEYWORDS}}` | 从标题和章节标题中提取 3-5 个关键词，以逗号分隔 |
| `{{文档标题}}` / `{{信件主题}}` 等 | `{{DOC_TITLE}}` / `{{LETTER_SUBJECT}}` 等 | 从 H1 或 `.header .title` 文本推断 |

`<meta name="generator" content="Kami">` 已在模板中固定；不要修改。

**作者推断**：`build.py` 按以下顺序自动设置 PDF 的 `/Author` 元数据：
1. `git config user.name`（首选）
2. `KAMI_AUTHOR` 环境变量（后备）
3. `"Kami"`（最终后备）

对于个人文档（简历/信件/作品集），HTML `<meta name="author">` 应与内容中的人物姓名一致。对于非个人文档（单页文档/长文档），保持占位符原样，由构建脚本进行推断。

## 步骤 4.1 · 单页密度目标（仅限多页模板）

适用：slides-weasy / long-doc / portfolio / equity-report / changelog。不适用 resume / one-pager / letter（这些有独立的长度合约）。

正文页填充率目标 60-80%。封面 / 目录 / 末尾署名页豁免。这条规则解决的是 AI 生成多页文档时最常见的 draft 缺陷：把内容拆得太散，结果几页都填不满。

### 每页项目数量契约

| 模板 | 典型正文页 | 硬性下限（低于则合并） |
|---|---|---|
| slides-weasy | 1 个论点标题 + 3-5 个支持项，或 1 张图表 + 2-3 个标注 | <3 个项目且无图表 → 合并到相邻幻灯片 |
| long-doc | 1 个章节标题 + 2-4 个段落 + 最多 1 张插图 | 章节渲染后占页面 <40% → 合并到相邻章节 |
| portfolio | 1 个项目标题 + 1 张主图 + 3-5 条成果要点 | 无图片且成果 <3 项 → 与相邻项目合并 |
| equity-report | 1 个章节 + 1 个表格/图表 + 支持性正文 | 页面上只有一个两行表格 → 合并章节 |
| changelog | 1 个版本块 + 4-8 条记录 | 版本记录 <4 条 → 与上一版本放在同一页 |

### 稀疏页面合并规则

最终确定前扫描草稿。任何正文页预计渲染后填充率低于 50% → 按顺序应用以下方法之一：

1. 向上合并到上一章节。
2. 向下合并到下一章节。
3. 将列表提升为值得占用空间的小型图表或表格。
4. 将 `.co` 标注固定在底部（仅限 slides-weasy）。固定标注上方的留白是有意设计，不算稀疏。

禁止用以下方式“填满”稀疏页面：添加填充性文字、把标题重复成句子、虚构统计数据、换一种说法重复上一页。如果合并选项都不适用，则该页面本身就不应该存在。

### 最后一页豁免

最后一张正文页允许只有 40-60% 的填充率。强行平衡最后一页通常意味着填充内容。版权页 / 结束页可以是任意填充率。

### 构建后验证

```bash
python3 scripts/build.py --check-density   # 标记 >25%（WARN）/ >50%（SPARSE）的尾部留白
```

如果正文页（非封面、非最后一页）出现 SPARSE 警告，请将其视为草稿缺陷，并按照合并规则重新编写。

## 步骤 4.2 · 简历招聘人员检查（仅限简历）

机械检查（`--check-placeholders`、`--check-resume-balance`、`--check-density`）验证结构和布局，而不是文案。简历即使通过所有检查，读起来仍可能存在问题。填充后、构建前，按照 `references/resume-writing.md` 中的行定义（“每行应填写什么”），像招聘人员一样重读每张项目卡片：角色一行应说明你在项目中的职位，而不只是背景；行动一行应以动词开头，每句话只描述一种具体方法；影响一行应体现成果，而不是重复过程。还需进行一项跨行检查：任何一行都不能重复另一行的信息。

根据来源材料重写不合格的行。如果来源无法支持某一行（例如没有成果事实），请向用户询问缺失事实。不要填充，也不要回退到通用表述（“保障稳定运行”“improved efficiency”）。

此检查在内部静默执行；仅当某一行无法在没有用户新信息的情况下修复时才反馈。

## 步骤 4.5 · 自动选择输出格式

不要询问用户导出哪种格式。根据上下文决定：

| 信号 | 输出 | 原因 |
|---|---|---|
| 任何文档请求 | HTML + PDF | PDF 是默认交付物，HTML 是源文件 |
| Slides / PPT / deck | HTML + PDF + PPTX | 演示文稿需要可投影格式 |
| “分享” / “发朋友圈” / “share” / “post” / “preview” | + PNG | 社交平台和即时通信需要图片 |
| “嵌入” / “插图” / “embed in another doc” | 仅 PNG | 用作其他文档中的素材 |
| 用户明确指定格式 | 遵循用户要求 | 明确请求覆盖自动选择 |

文档模板始终交付 PDF。落地页交付可直接提供服务的静态 HTML 文件。PPTX 随幻灯片提供。分享场景提供 PNG。用户不应需要考虑格式。

## 步骤 5 · 构建与验证

```bash
python3 scripts/build.py --verify           # 构建所有模板 + 页数 + 字体检查 + 幻灯片
python3 scripts/build.py --verify resume-en # 单一目标完整验证
python3 scripts/build.py landing-page        # 屏幕优先静态 HTML 模板检查
python3 scripts/build.py --verify slides    # 单个幻灯片完整验证
python3 scripts/build.py --check-placeholders path/to/filled.html
python3 scripts/build.py --check-markdown path/to/filled.pdf
python3 scripts/build.py --check-resume-balance path/to/resume.pdf
python3 scripts/build.py --check-density              # 页面留白扫描器（跳过封面）
python3 scripts/build.py --check            # lint + 令牌/主题 + 公开站点事实检查
python3 scripts/build_metadata.py --check   # Claude/Codex 插件镜像 + 市场漂移检查
```

> **屏幕验证**：`--check-density` 是印刷检查关卡。对于屏幕输出（落地页或文档页面），应在每种语言区域下分别以 375px 和 1280px 截取渲染页面，并在交付前检查是否存在孤行。参见 `references/design.md` 第 11 节《响应式截图验证》。

源模板有意保留 `{{...}}` 字段。请对完成的文档运行占位符检查，而不是对模板库运行。

对于以 Markdown 为来源的长文档，还应对渲染后的 PDF 运行 `--check-markdown`。它会捕获交付前本应转换或删除、但仍可见的原始 `---`、`**bold**` 和行内代码反引号。

视觉异常（标签双重矩形、字体回退、分页问题）-> `production.md` 第 4 部分。

### 维护者模式检查

仅在维护此仓库或发行包时使用这些检查，不要用于普通文档生成。

- 如果市场元数据、生成的插件镜像、版本选择或安装路径发生变化，运行 `python3 scripts/build_metadata.py --check`；对于 Claude Code 安装行为，使用隔离的 `HOME=/tmp/...`，通过 `claude plugin marketplace add <path>`、`claude plugin install kami@kami` 和 `claude plugin details kami@kami` 进行冒烟测试；对于 Codex 安装行为，使用隔离的 `CODEX_HOME=/tmp/...`，通过 `codex plugin marketplace add <path>`、`codex plugin add kami@kami` 和 `codex plugin list` 进行冒烟测试。
- 如果 `SKILL.md`、模板、脚本、参考资料或其他软件包输入发生变化，且该行为通过技能包交付，请运行 `bash scripts/package-skill.sh`，并在交付前检查 `dist/kami.zip`。
- 如果刷新了 GitHub 发行版资源，请下载上传后的 `kami.zip`，并将其 ZIP 条目名称及每个条目的 SHA-256 摘要与本地 `dist/kami.zip` 进行比较；页面文本、文件大小和容器哈希不足以完成验证。

## 字体

**中文**
- 正文衬线字体：TsangerJinKai02-W04.ttf（400 字重）+ TsangerJinKai02-W05.ttf（500 字重，真实粗体）
- 模板使用双重 @font-face 声明：W04 用于正文，W05 用于标题
- 两个文件都是商业字体。将其保留在仓库中，用于本地预览和 CDN 后备，但不要将其捆绑到 Claude Desktop 技能 ZIP 中
- 模板内置的后备链：Source Han Serif SC -> Noto Serif CJK SC -> Songti SC -> STSong -> Georgia

**日文（尽力支持）**
- 使用 CJK 模板路径，目前没有专用的 `-ja` 模板
- 日文明朝体优先字体栈：YuMincho -> Hiragino Mincho ProN -> Noto Serif CJK JP -> Source Han Serif JP -> TsangerJinKai02 -> serif
- 交付前目视验证换行、标点节奏和强调字重

**韩文（尽力支持）**
- 专用 `-ko` 模板使用 Source Han Serif K Regular / Medium，每个后备字体栈中均保留真实的 OTF 字体族名称 `Source Han Serif KR`
- 后备字体：Noto Serif KR / Apple SD Gothic Neo / AppleMyungjo / Charter / Georgia
- 这些 OTF 使用 OFL 许可证，并为本地预览 / CDN 后备纳入版本控制，但会从 Claude Desktop 技能 ZIP 中排除，以缩小软件包体积

**英文**
- 单一衬线字体：Charter（系统捆绑于 macOS/iOS），同时用于标题和正文
- 不使用单独的无衬线字体：`--sans: var(--serif)`，每页一种字体
- 后备字体：Georgia（跨平台）/ Palatino / Times New Roman

将字体文件放在 HTML 旁边并使用相对 `@font-face` 路径，是最稳定的设置。`scripts/package-skill.sh` 会从 Claude Desktop ZIP 中排除大型 CJK 字体文件，使上传的软件包保持在 6MB 上限以下，并包含顶层 `kami/` 技能文件夹。始终上传 `package-skill.sh` 的输出，绝不要手工压缩检出目录（受版本控制的 CJK 字体会使其过大，Claude Desktop 将拒绝上传）。

**字体自动恢复（Claude Desktop）**

构建中文或韩文文档前，确保字体已存在。脚本会尝试多个 CDN 来源，并执行重试和大小验证：

```bash
bash scripts/ensure-fonts.sh
```

它会下载到 XDG 用户字体目录（`${XDG_DATA_HOME:-~/.local/share}/fonts/kami`，可用 `KAMI_FONT_DIR` 覆盖），**而不是**技能的 `assets/fonts`——这能保持已安装技能体积较小，确保 Claude Desktop 不会触及其大小限制。fontconfig 默认会扫描该目录，因此 WeasyPrint 能在其中找到 `TsangerJinKai02` 和 `Source Han Serif K`；在线渲染则回退到 jsDelivr `@font-face` URL。构建前运行一次。如果所有来源均失败，脚本会输出各语言的替代方案。

## 反馈协议

当用户给出**模糊的视觉反馈**（“looks off”“太挤了”“not elegant”）时，不要猜测。附带当前值反问：

| 用户说 | 询问内容 |
|---|---|
| “太挤了” / “too cramped” | 哪个元素？行高（当前：X）？内边距（当前：Y）？页面边距？ |
| “太松了” / “too loose” | 方向相同，反向调整 |
| “颜色不对” / “color feels wrong” | 哪个元素？品牌蓝是否使用过多？某种灰色是否显得太冷？ |
| “不够好看” / “not polished” | 字体渲染？对齐？留白分布？层级不清晰？ |
| “看着不专业” / “unprofessional” | 内容措辞？还是布局（对齐、一致性）？ |

回复模板：“X 当前设置为 Y。你希望选择 (a) [规范内的具体替代值]，还是 (b) [另一个选项]？”

绝不要在未说明具体属性及其新值的情况下只说“我会调整间距”。

---

## 不应使用此技能的情况

- 用户明确要求 Material / Fluent / Tailwind 默认风格——这是不同的设计语言
- 需要深色 / 赛博朋克 / 未来主义美学（本技能刻意反未来感）
- 需要饱和的多色设计（本技能只使用一种强调色）
- 需要卡通 / 动画 / 插画风格（本技能采用编辑设计风格）
- Web 动态应用 UI（本技能用于印刷 / 静态文档）

---

下一步：**应用步骤 3 的层级表决定需要阅读的内容**，然后复制匹配的模板并开始填充。
