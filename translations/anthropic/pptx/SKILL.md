<!-- source-sha256: a7ff03e2c85b636f55232a6b1555f5dd90216b7a1a359ab289d8364e6acbc6a0 -->
---
name: pptx
description: "只要以任何方式涉及 `.pptx` 或 `.potx` 文件——无论作为输入、输出还是两者兼有——都使用此技能。这包括：创建幻灯片、路演材料或演示文稿；读取、解析或提取任何 `.pptx` 或 `.potx` 文件中的文本（即使提取的内容随后会用于其他地方，例如电子邮件或摘要）；编辑、修改或更新现有演示文稿；合并或拆分幻灯片文件；处理模板（`.potx`）、版式、演讲者备注或评论。只要用户提到“deck”“slides”“presentation”，或引用 `.pptx` 或 `.potx` 文件名，无论之后计划如何处理其内容，都应触发此技能。如果需要打开、创建或改动 `.pptx` 或 `.potx` 文件，请使用此技能。"
license: 专有。完整条款见 LICENSE.txt
---

# PPTX 创建、编辑与分析

`.pptx` 是由 XML 文件组成的 ZIP 归档。请根据任务选择处理方式：

| 任务 | 方式 |
|---|---|
| **创建**新幻灯片 | 编写 `pptxgenjs` 脚本——参见下方注意事项 |
| **编辑**现有幻灯片，或基于模板构建 | 解压 → 编辑 `ppt/slides/slideN.xml` → 压缩 |
| **读取**内容 | `markitdown deck.pptx`（每张幻灯片对应一个区块，位于 `<!-- Slide number: N -->` 标记下）；可视化网格：`python scripts/thumbnail.py deck.pptx` |

## 脚本

路径均相对于此技能的目录。其他内容均使用普通 Python、`node` 或 shell。

| 脚本 | 功能 |
|---|---|
| `scripts/thumbnail.py deck.pptx [prefix]` | 生成包含每张幻灯片并带标签的网格，用于选择模板版式。仅支持 `.pptx`。请传入 `prefix`——其默认值为 `thumbnails`，会覆盖在同一目录中处理的其他幻灯片所生成的网格 |
| `scripts/add_slide.py unpacked/ slide2.xml [--after slideN.xml]` | 复制一张幻灯片（或 `slideLayoutN.xml`），并完成所有包级登记工作。也可以通过 `-o out.pptx` 直接处理 `.pptx` |
| `scripts/clean.py unpacked/` | 删除不再被引用的幻灯片、媒体和 rels。请在 `<p:sldIdLst>` 最终确定后运行 |
| `scripts/office/validate.py deck.pptx [--original src.pptx]` | 执行架构、关系、内容类型、图表和幻灯片检查；每项失败都会指出修复方法。任何基于模板生成的幻灯片都应传入 `--original`——它会以模板作为架构检查的基线，避免将模板自身的 XSD 错误误认为是你的错误 |
| `scripts/office/soffice.py --headless --convert-to pdf deck.pptx` | LibreOffice 包装器——直接运行 `soffice` 会在此沙箱中挂起 |

## 使用 pptxgenjs 创建——注意事项

`pptxgenjs` 已预安装——不要先运行 `npm install`；直接编写脚本并调用 `require('pptxgenjs')`。仅当该 require 失败时，才运行 `npm install pptxgenjs`。模型了解其 API；以下是容易踩坑的地方：

- **添加幻灯片前先设置 `pres.layout`。** 默认画布为 `LAYOUT_16x9` = **10" × 5.625"**，而不是 13.3" 宽。超出边界的坐标会被写入而不会被限制——形状只是不出现在幻灯片上。（`LAYOUT_WIDE` 为 13.3" × 7.5"。）
- **十六进制颜色：绝不能包含 `#`，绝不能使用 8 位。** 使用 `color: "FF0000"`。`"#FF0000"` 和在十六进制颜色中内嵌 alpha（`"00000020"`）都会**损坏文件**。若需半透明：填充和图像使用 `transparency: 0-100`，阴影使用 `opacity: 0.0-1.0`——将它们用在对方的场景中都会被静默忽略。
- **pptxgenjs 会就地修改选项对象**（首次使用时将值转换为 EMU）。绝不能在两次 `add*` 调用间共享同一个 `shadow`/选项对象——每次都创建新对象。
- **阴影的 `offset` 必须 ≥ 0**——负偏移会损坏文件。若要让阴影向上投射，请使用 `angle: 270` 并配合正偏移。
- **`letterSpacing` 会被静默忽略**——真正的选项是 `charSpacing`。
- **列表：**每一项都使用 `bullet: true`，绝不能使用字面量 `•`（会渲染成双重项目符号）。除最后一项外，数组中的每一项都应设置 `breakLine: true`。项目符号段落之间使用 `paraSpaceAfter` 设置间距，不要使用 `lineSpacing`（会产生巨大间隔）。
- **每个输出文件使用一个新的 `new pptxgen()`**——绝不能复用实例。
- **`rectRadius` 仅适用于 `ROUNDED_RECTANGLE`**，不适用于 `RECTANGLE`。
- **不支持渐变填充**——请改用渐变图像作为背景。
- **文本框自带内部边距**——当文本必须与同一 x 坐标上的形状、线条或图标对齐时，请设置 `margin: 0`。
- **演讲者备注应放在 `slide.addNotes("...")` 中**（纯文本，每张幻灯片调用一次），绝不能放在幻灯片上的文本框中。
- **保持图表为原生格式。** PowerPoint 能绘制的所有图表都使用 `addChart()`（组合图可传入由 `{type, data, options}` 组成的数组）。对于库未公开的 PowerPoint 原生功能（趋势线、误差线），请自行计算额外系列，或对生成的 OOXML 进行后处理——不要退回为渲染图像。只有 PowerPoint 没有原生形式的图表类型（Sankey、network、chord）才应以图像形式插入。
- **默认图表渲染效果非常简陋**——没有标题、没有数据标签，配色也过时。请设置 `showTitle` + `title`、`showValue: true` + `dataLabelPosition`、来自配色方案的 `chartColors: [...]`，并弱化边框（`catAxisLabelColor`/`valAxisLabelColor`、`valGridLine: { color, size }`、`catGridLine: { style: "none" }`；单系列图表设置 `showLegend: false`）。
- **对于堆积条形图或堆积柱形图，`dataLabelPosition` 必须是 `ctr`、`inEnd` 或 `inBase`。** `outEnd` 会**损坏文件**。
- **使用 `secondaryValAxis`/`secondaryCatAxis` 的组合系列，需要在图表选项中同时提供 `valAxes` 和 `catAxes`，且每项各包含两个条目。** 否则 pptxgenjs 会写入从未声明的轴 *ids*，PowerPoint 会**丢弃该图表**并报告文件损坏。仅提供 `valAxes` 并不够。
- **执行 `writeFile()` 后，运行 `python scripts/office/validate.py deck.pptx`。** 它会报告上述两个图表问题，以及 PowerPoint 会拒绝的幻灯片 XML 缺陷，并指出每项问题的修复方法。请在生成器中修复，而不是手动编辑打包后的 XML。
- **绝不能重新排列 `<p:presentation>` 的子元素。** pptxgenjs 会将 `<p:notesMasterIdLst>` 写在 `<p:sldIdLst>` 之后，并让两个母版指向同一个主题部件。PowerPoint 可以正常读取——但移动该元素后，同一份幻灯片将无法打开。
- **图标：**将 `react-icons` 渲染为 SVG（`ReactDOMServer.renderToStaticMarkup`），使用 `sharp` 以 ≥256px 栅格化，然后通过 `addImage({ data: "image/png;base64," + buf.toString("base64") })` 插入——必须包含 `image/png;base64,` 前缀（`react-icons`、`react`、`react-dom` 和 `sharp` 已预安装——仅当 require 失败时才运行 `npm install react-icons react react-dom sharp`）。

## 编辑现有幻灯片和模板

先选择版式：`python scripts/thumbnail.py template.pptx template-thumbs` 会生成带标签的全幻灯片网格，并打印所创建的文件——`template-thumbs.jpg`；超过 12 张幻灯片后会拆分为 `template-thumbs-N.jpg`。**务必传入以该幻灯片文件命名的第二个参数。** 默认值为 `thumbnails`，因此在同一目录中为两份幻灯片生成缩略图时，后者会静默覆盖前者的网格——第一份幻灯片的网格会直接消失（这仅用于模板分析——可视化 QA 需要使用[转换为图像](#转换为图像)中的全分辨率渲染；该脚本只接受 `.pptx`，因此需先将 `.potx` 复制为以 `.pptx` 结尾的名称）。将它与 `markitdown` 配合使用，把每个内容章节映射到模板幻灯片，并变换版式——不要让每个章节都使用相同的标题加项目符号版式。

```bash
python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" deck.pptx
python scripts/add_slide.py unpacked/ slide2.xml --after slide2.xml   # 复制一张幻灯片（或 slideLayoutN.xml）；打印新幻灯片的路径
# 重新排序/删除幻灯片 = 编辑 ppt/presentation.xml 中的 <p:sldIdLst>
python scripts/clean.py unpacked/                                     # 删除后：移除孤立的幻灯片、媒体、rels
# 编辑 ppt/slides/slideN.xml 中的幻灯片内容
(cd unpacked && rm -f ../out.pptx && zip -Xr ../out.pptx .)           # 从目录内部压缩；先 rm，否则被删除的部件仍会保留
python scripts/office/validate.py out.pptx --original deck.pptx
```

- **在编辑任何幻灯片内容之前，完成所有结构性工作——添加、删除和重新排序。** `add_slide.py` 会逐字复制幻灯片文件，因此在编辑后再复制会克隆已编辑的内容；而 `clean.py` 会删除 `<p:sldIdLst>` 中缺失的任何幻灯片，包括你刚刚写入的幻灯片。
- **绝不能手动复制幻灯片文件**——`add_slide.py` 会完成新幻灯片所需的全部登记工作，并报告其创建内容（`Created ppt/slides/slide17.xml from slide2.xml`）。它也可以直接操作文件：`add_slide.py deck.pptx slide2.xml -o out.pptx`——**请传入 `-o`，否则它会就地重写输入幻灯片。** 复制的幻灯片仍然会*引用*源幻灯片的图表/SmartArt/嵌入对象部件，而不是克隆它们，因此编辑其中一张幻灯片的图表也会改变另一张。
- **如果使用 `python-pptx`**，它无法完成三件事：复制幻灯片（其唯一入口是 `add_slide(layout)`）；通过 `text_frame.text = "..."` 保留格式（这会把段落折叠成单个无样式文本运行——应改为赋值给 `run.text`）；读取大多数模板插图使用的 SVG/EMF（`add_picture` 会引发 `UnidentifiedImageError`）。
- 旧版 `.ppt` 必须先转换：`python scripts/office/soffice.py --headless --convert-to pptx file.ppt`。`.potx` 模板的解包与打包方式完全相同——输出时保留 `.potx` 扩展名。
- 若要复用模板中的图标或图像，请复制已经包含它的幻灯片或版式。

填充模板时：

- 如果编写 XML 转换脚本，请使用 `defusedxml.minidom` 解析——通过 `xml.etree.ElementTree` 往返处理 OOXML 会重写命名空间前缀并损坏幻灯片。
- **模板槽位 ≠ 源数据项。** 如果模板展示 4 名团队成员，而你只有 3 名，请删除第 4 名成员的整个组（图像 + 文本框），而不只是删除其文本——然后在 QA 中检查是否存在孤立的视觉元素。
- 每个列表项使用一个 `<a:p>`——绝不能把多个项目拼接到同一段落中。复制同级 `<a:pPr>` 以保留间距，并在标题、章节标题和行内标签（`Status:`、`Owner:`）的 `<a:rPr>` 上设置 `b="1"`。
- 让项目符号继承自版式；只有需要覆盖时才添加 `<a:buChar>`、`<a:buAutoNum>`（编号）或 `<a:buNone>`——绝不能在文本中使用字面量 `•`。
- 带前导或尾随空格的文本，需要在其 `<a:t>` 上设置 `xml:space="preserve"`。

## 设计构思

**不要制作乏味的幻灯片。** 白色背景上的普通项目符号不会给任何人留下深刻印象。请为每张幻灯片考虑以下列表中的构思。

### 开始之前

- **选择大胆且由内容驱动的配色方案**：配色应让人感觉是专门为当前主题设计的。如果把你的颜色换到完全不同的演示文稿中仍然“适用”，说明你的选择还不够具体。
- **强调主次，而非均等**：一种颜色应占主导地位（60-70% 的视觉权重），搭配 1-2 种辅助色和一种鲜明的强调色。绝不要让所有颜色具有相同权重。
- **深色/浅色对比**：标题页和结论页使用深色背景，内容页使用浅色背景（“三明治”结构）。也可以全程使用深色，营造高级感。
- **坚持一种视觉母题**：选择一种独特元素并重复使用——例如圆角图像框、彩色圆圈中的图标。让它贯穿每张幻灯片。**不要使用色条或强调色条纹作为母题**（参见“避免”列表）。

### 配色方案

选择与主题相符的颜色——不要默认使用通用蓝色。可参考以下配色：

| 主题 | 主色 | 辅色 | 强调色 |
|-------|---------|-----------|--------|
| **午夜行政风** | `1E2761`（海军蓝） | `CADCFC`（冰蓝） | `FFFFFF`（白色） |
| **森林与苔藓** | `2C5F2D`（森林绿） | `97BC62`（苔藓绿） | `F5F5F5`（奶油色） |
| **珊瑚活力** | `F96167`（珊瑚色） | `F9E795`（金色） | `2F3C7E`（海军蓝） |
| **暖陶土色** | `B85042`（陶土色） | `E7E8D1`（沙色） | `A7BEAE`（鼠尾草绿） |
| **海洋渐变** | `065A82`（深蓝） | `1C7293`（蓝绿色） | `21295C`（午夜蓝） |
| **炭灰极简** | `36454F`（炭灰色） | `F2F2F2`（灰白色） | `212121`（黑色） |
| **蓝绿信赖感** | `028090`（蓝绿色） | `00A896`（海沫绿） | `02C39A`（薄荷绿） |
| **浆果与奶油** | `6D2E46`（浆果色） | `A26769`（灰玫瑰色） | `ECE2D0`（奶油色） |
| **鼠尾草宁静感** | `84B59F`（鼠尾草绿） | `69A297`（桉树绿） | `50808E`（石板色） |
| **醒目樱桃红** | `990011`（樱桃红） | `FCF6F5`（灰白色） | `2F3C7E`（海军蓝） |

### 每张幻灯片

**每张幻灯片都需要视觉元素**——图像、图表、图标或形状。纯文字幻灯片令人难以记住。

**版式选项：**
- 双栏（左侧文字，右侧插图）
- 图标 + 文字行（彩色圆圈中的图标、粗体标题、下方说明）
- 2x2 或 2x3 网格（一侧放图像，另一侧放内容块网格）
- 半出血图像（完整占据左侧或右侧），并叠加内容

**数据展示：**
- 大型数据强调（60-72pt 的大号数字，下方配小标签）
- 对比栏（之前/之后、优点/缺点、并排选项）
- 时间线或流程图（编号步骤、箭头）

**视觉润色：**
- 在章节标题旁放置彩色小圆圈中的图标
- 对关键数据或标语使用斜体强调文字

### 字体排印

**写入 `.pptx` 的字体名称由用户的 PowerPoint 渲染，而不是由当前环境渲染。** 可视化 QA 使用 LibreOffice 渲染，它会替换系统中不存在的字体——对于某些字体，替代字体的宽度不同，因此 QA 预览可能显示文字溢出（或能够容纳），而实际幻灯片中的结果却不同。为确保 QA 可信：

- **安全字体**（在 QA 中按真实宽度渲染，且随 Office 提供）：**Arial、Calibri、Cambria、Times New Roman、Courier New、Bookman Old Style、Century Schoolbook**。正文以及任何需要精确适配的位置都使用这些字体。
- **在零 QA 风险下呈现个性的标题**：将安全列表中的衬线标题字体（Cambria、Bookman Old Style、Century Schoolbook）与安全列表中的无衬线正文字体（Calibri 或 Arial）搭配。这样既能形成视觉对比，又不会牺牲可靠的溢出检查。
- **如果用户要求使用安全列表以外的字体**（例如 Georgia 或 Trebuchet MS）：在用户要求的位置使用该字体，但应为这些容器额外预留约 10% 的空间，并且不要相信这些元素的 QA 文本适配结果——该字体的预览只是近似值。如果用户没有指定字体，正文优先使用安全列表中的字体。
- **QA 不可靠字体**（替代字体宽度不同——溢出检查可能出错）：Georgia、Trebuchet MS、Impact、Arial Black、Garamond、Consolas、Palatino Linotype。Calibri Light 的替代效果因环境而异，应视为 QA 不可靠字体。可以在留有余量的标题/强调文字中使用；不要相信这些字体的 QA 文本适配结果。
- **绝不要默认使用 Aptos**——Office 在 2023 年后采用的默认字体在此环境中没有度量兼容的替代字体，并且旧版 Office 也未安装它，因此两端都不可靠。

| 元素 | 大小 |
|---------|------|
| 幻灯片标题 | 36-44pt 粗体 |
| 章节标题 | 20-24pt 粗体 |
| 正文 | 14-16pt |
| 说明文字 | 10-12pt，弱化显示 |

### 间距

- 最小页边距为 0.5"
- 内容块之间留出 0.3-0.5"
- 留出呼吸空间——不要填满每一寸区域

### 避免事项（常见错误）

- **不要重复使用相同版式**——在不同幻灯片间变化使用分栏、卡片和数据强调
- **不要将正文居中**——段落和列表应左对齐；仅标题可居中
- **不要吝啬字号对比**——标题需要达到 36pt 以上，才能从 14-16pt 的正文中脱颖而出
- **不要默认使用蓝色**——选择能反映具体主题的颜色
- **不要随意混用间距**——选择 0.3" 或 0.5" 的间隔，并保持一致
- **不要只设计一张幻灯片而让其余页面保持朴素**——要么贯彻完整设计，要么全程保持简洁
- **不要创建纯文字幻灯片**——添加图像、图标、图表或视觉元素；避免普通的标题 + 项目符号
- **不要忘记文本框内边距**——当线条或形状需要与文字边缘对齐时，请在文本框上设置 `margin: 0`，或偏移形状以补偿内边距
- **不要使用低对比度元素**——图标和文字都需要与背景形成强烈对比；避免在浅色背景上使用浅色文字，或在深色背景上使用深色文字
- **绝不要在标题下使用强调线**——这是 AI 生成幻灯片的典型特征；请改用留白或背景色
- **绝不要添加装饰性色条或强调色条纹**——包括：横跨幻灯片宽度的页眉/页脚色条、沿幻灯片一侧延伸的垂直边栏条纹、卡片或内容块一侧的细强调条纹，以及矩形上的“单侧边框”。这些看起来像 AI 生成的填充物。如果想突出卡片，请使用细微的背景色调、投影或图标——不要使用边缘条纹。
- **不要默认使用奶油色/米色背景**——未指定背景时，请使用白色（`FFFFFF`）或用户的品牌配色；避免默认使用 `F5F5DC`、`FAF0E6`、`FAEBD7`、`FFF8E1` 等暖中性色
- **不要交付溢出形状范围的文字**——如果文字无法容纳，请减小字号、拆分到多张幻灯片或扩大容器；绝不要让内容被截断或溢出边界

## QA（必需）

第一次渲染通常会存在一些实际问题——重叠、溢出、错位。找出并修复这些问题，只重新渲染改动过的幻灯片，然后停止。

### 内容 QA

```bash
markitdown output.pptx
```

检查是否存在内容缺失、拼写错误和顺序错误。

**使用模板时，检查是否残留占位文本：**

```bash
markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|this.*(page|slide).*layout"
```

如果 grep 返回结果，请在宣布完成前修复。

### 文件 QA（必需）

```bash
python scripts/office/validate.py output.pptx                      # 从头构建
python scripts/office/validate.py output.pptx --original src.pptx  # 基于模板构建
```

**如果幻灯片来自模板，务必传入 `--original`。** 模板本身可能包含 XSD 拒绝的部件，因此直接运行可能会报告并非由你造成的失败——真正的回归问题也可能被淹没其中。`--original` 会以模板作为架构和幻灯片检查的基线，抑制模板中原本就存在的错误。结构检查——关系、内容类型、图表——会忽略 `--original`，无论如何都会报告从模板继承的问题，因此请根据问题本身判断这些报告。

pptxgenjs 可能生成 PowerPoint 拒绝打开、但其他所有工具都能接受的图表 XML：python-pptx 可以打开这些幻灯片，LibreOffice 可以渲染它们，XSD 检查也能通过。每项失败都会指出修复方法。请在生成器中修复并重新构建。

### 可视化 QA

将幻灯片转换为图像（参见[转换为图像](#转换为图像)），并逐一检查。长时间查看生成代码后，你往往会看到自己预期的效果，而不是实际渲染结果，因此请以全新的视角查看图像（如果有子代理，这项工作很适合交给它）。需要检查的用户可见缺陷包括：

- **文字溢出，或文字在文本框或幻灯片边界处被截断——首先检查此项。** 这是最常见且始终对用户可见的缺陷。（如果预览器对某种字体的渲染按“字体排印”章节所述并不可靠，则该预览只是近似结果：应相信预留的约 10% 余量，而不是表面上的适配情况。）
- 元素重叠（文字穿过形状、线条穿过文字、元素堆叠）
- 来源引用或页脚与上方内容发生碰撞
- 元素间距过小（< 0.3"），或卡片/章节几乎相互接触
- 间距不均匀（一处大片空白，另一处过于拥挤）
- 与幻灯片边缘的距离不足（< 0.5"）
- 分栏或相似元素未保持一致对齐
- 低对比度文字（例如奶油色背景上的浅灰色文字）
- 替换文字后模板装饰错位——例如标题下划线原本按单行标题定位，但替换后的标题换成了两行
- 低对比度图标（例如深色背景上的深色图标，且没有高对比度圆形底）
- 文本框过窄，导致过度换行
- 残留的占位内容

## 转换为图像

将演示文稿转换为单独的幻灯片图像，以便进行视觉检查：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

**将上方打印出的绝对路径直接传给查看工具。** `rm` 会清除之前运行所留下的旧图像。`pdftoppm` 会根据页数补零：少于 10 页的幻灯片使用 `slide-1.jpg`，10-99 页使用 `slide-01.jpg`，100 页以上使用 `slide-001.jpg`。

**修复后，重新运行上方全部四条命令**——必须先从编辑后的 `.pptx` 重新生成 PDF，`pdftoppm` 才能反映改动。

## 依赖项

`pptxgenjs`（npm，已预安装——仅当 `require('pptxgenjs')` 失败时安装）· `markitdown[pptx]`、`Pillow`、`defusedxml`、`lxml`（pip——用于文本导出、缩略图、清理、验证）· LibreOffice（`soffice`，通过 `scripts/office/soffice.py` 针对沙箱环境自动配置）· `pdftoppm`（Poppler）
