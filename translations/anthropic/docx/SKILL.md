<!-- source-sha256: cfbabd72b1aec7dfaad988fb6e5e16b27dc744b9a00cae15db9045e95f53903e -->
---
name: docx
description: "当用户想要创建、读取、编辑或处理 Word 文档（.docx 文件）时，请使用此技能。触发条件包括：任何提及“Word 文档”“word document”或“.docx”的情况，或者要求制作带有目录、标题、页码或信头等格式的专业文档。还应在以下情况使用：从 .docx 文件中提取或重新组织内容、在文档中插入或替换图像、在 Word 文件中执行查找和替换、处理修订或批注，或者将内容转换为精美的 Word 文档。如果用户要求以 Word 或 .docx 文件形式交付“报告”“备忘录”“信函”“模板”或类似成果，请使用此技能。请勿将其用于 PDF、电子表格、Google Docs 或与文档生成无关的常规编码任务。"
license: 专有许可。完整条款见 LICENSE.txt
---

# DOCX 创建、编辑与分析

## 概述

.docx 文件是包含 XML 文件的 ZIP 归档。

## 快速参考

| 任务 | 方法 |
|------|----------|
| 读取/分析内容 | 使用 `pandoc`，或解包以访问原始 XML |
| 创建新文档 | 使用 `docx-js`——参见下方“创建新文档” |
| 编辑现有文档 | 解包 → 编辑 XML → 重新打包——参见下方“编辑现有文档” |

### 将 .doc 转换为 .docx

旧版 `.doc` 文件必须先转换才能编辑：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 读取内容

```bash
# 提取包含修订的文本
pandoc --track-changes=all document.docx -o output.md

# 访问原始 XML
python scripts/office/unpack.py document.docx unpacked/
```

### 转换为图像

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 接受修订

要生成接受了所有修订的干净文档（需要 LibreOffice）：

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 创建新文档

使用 JavaScript 生成 .docx 文件，然后进行验证。安装：`npm install -g docx`

### 设置

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* 内容 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 验证

创建文件后，请对其进行验证。如果验证失败，请解包、修复 XML，然后重新打包。

```bash
python scripts/office/validate.py doc.docx
```

### 页面尺寸

```javascript
// 关键：docx-js 默认为 A4，而非美国信纸
// 始终显式设置页面尺寸，以确保结果一致
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5 英寸，以 DXA 表示
        height: 15840   // 11 英寸，以 DXA 表示
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 英寸页边距
    }
  },
  children: [/* 内容 */]
}]
```

**常见页面尺寸（DXA 单位，1440 DXA = 1 英寸）：**

| 纸张 | 宽度 | 高度 | 内容宽度（1 英寸页边距） |
|-------|-------|--------|---------------------------|
| 美国信纸 | 12,240 | 15,840 | 9,360 |
| A4（默认） | 11,906 | 16,838 | 9,026 |

**横向方向：** docx-js 会在内部交换宽度和高度，因此请传入纵向尺寸，并让它自行处理交换：

```javascript
size: {
  width: 12240,   // 将短边作为宽度传入
  height: 15840,  // 将长边作为高度传入
  orientation: PageOrientation.LANDSCAPE  // docx-js 会在 XML 中交换它们
},
// 内容宽度 = 15840 - 左页边距 - 右页边距（使用长边）
```

### 样式（覆盖内置标题）

使用 Arial 作为默认字体（普遍受支持）。为保证可读性，标题保持黑色。

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 默认 12pt
    paragraphStyles: [
      // 重要：使用准确的 ID 覆盖内置样式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // 目录需要 outlineLevel
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("标题")] }),
    ]
  }]
});
```

### 列表（绝不要使用 Unicode 项目符号）

```javascript
// ❌ 错误——绝不要手动插入项目符号字符
new Paragraph({ children: [new TextRun("• 项目")] })  // 错误
new Paragraph({ children: [new TextRun("\u2022 项目")] })  // 错误

// ✅ 正确——使用带有 LevelFormat.BULLET 的编号配置
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("项目符号项")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("编号项")] }),
    ]
  }]
});

// ⚠️ 每个 reference 都会创建独立的编号序列
// 相同 reference = 继续编号（1,2,3，然后 4,5,6）
// 不同 reference = 重新开始（1,2,3，然后 1,2,3）
```

### 表格

**关键：表格需要双重宽度设置**——既要设置表格的 `columnWidths`，也要设置每个单元格的 `width`。缺少其中任何一个，表格在某些平台上都会错误渲染。

```javascript
// 关键：始终设置表格宽度，以确保渲染一致
// 关键：使用 ShadingType.CLEAR（而不是 SOLID），以防止出现黑色背景
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // 始终使用 DXA（百分比在 Google Docs 中会失效）
  columnWidths: [4680, 4680], // 总和必须等于表格宽度（DXA：1440 = 1 英寸）
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // 每个单元格也要设置
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // 使用 CLEAR，而不是 SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // 单元格内边距（位于内部，不计入宽度）
          children: [new Paragraph({ children: [new TextRun("单元格")] })]
        })
      ]
    })
  ]
})
```

**表格宽度计算：**

始终使用 `WidthType.DXA`——`WidthType.PERCENTAGE` 在 Google Docs 中会失效。

```javascript
// 表格宽度 = columnWidths 之和 = 内容宽度
// 采用 1 英寸页边距的美国信纸：12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // 总和必须等于表格宽度
```

**宽度规则：**

- **始终使用 `WidthType.DXA`**——绝不要使用 `WidthType.PERCENTAGE`（与 Google Docs 不兼容）
- 表格宽度必须等于 `columnWidths` 之和
- 单元格的 `width` 必须与对应的 `columnWidth` 匹配
- 单元格的 `margins` 是内部填充——它们会缩小内容区域，而不会增加单元格宽度
- 对于全宽表格：使用内容宽度（页面宽度减去左右页边距）

### 图像

```javascript
// 关键：type 参数是必需的
new Paragraph({
  children: [new ImageRun({
    type: "png", // 必需：png、jpg、jpeg、gif、bmp、svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "标题", description: "描述", name: "名称" } // 三项均为必需
  })]
})
```

### 分页符

```javascript
// 关键：PageBreak 必须位于 Paragraph 内
new Paragraph({ children: [new PageBreak()] })

// 或使用 pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("新页面")] })
```

### 超链接

```javascript
// 外部链接
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "点击此处", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// 内部链接（书签 + 引用）
// 1. 在目标位置创建书签
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("第 1 章")] }),
]})
// 2. 链接到该书签
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "参见第 1 章", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

### 脚注

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("来源：2024 年年度报告")] },
    2: { children: [new Paragraph("方法论参见附录")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("收入增长了 15%"),
        new FootnoteReferenceRun(1),
        new TextRun("，采用调整后的指标"),
        new FootnoteReferenceRun(2),
      ],
    })]
  }]
});
```

### 制表位

```javascript
// 在同一行右对齐文本（例如，与标题分列两端的日期）
new Paragraph({
  children: [
    new TextRun("公司名称"),
    new TextRun("\t2025 年 1 月"),
  ],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
})

// 点引导符（例如目录样式）
new Paragraph({
  children: [
    new TextRun("引言"),
    new TextRun({ children: [
      new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.DOT,
      }),
      "3",
    ]}),
  ],
})
```

### 多栏布局

```javascript
// 等宽栏
sections: [{
  properties: {
    column: {
      count: 2,          // 栏数
      space: 720,        // 栏间距，以 DXA 表示（720 = 0.5 英寸）
      equalWidth: true,
      separate: true,    // 栏之间的竖线
    },
  },
  children: [/* 内容自然流入各栏 */]
}]

// 自定义栏宽（equalWidth 必须为 false）
sections: [{
  properties: {
    column: {
      equalWidth: false,
      children: [
        new Column({ width: 5400, space: 720 }),
        new Column({ width: 3240 }),
      ],
    },
  },
  children: [/* 内容 */]
}]
```

使用 `type: SectionType.NEXT_COLUMN` 创建新节，以强制分栏。

### 目录

```javascript
// 关键：标题必须仅使用 HeadingLevel——不能使用自定义样式
new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" })
```

### 页眉/页脚

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1 英寸
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("页眉")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("第 "), new TextRun({ children: [PageNumber.CURRENT] }), new TextRun(" 页")]
    })] })
  },
  children: [/* 内容 */]
}]
```

### docx-js 的关键规则

- **显式设置页面尺寸**——docx-js 默认为 A4；美国文档请使用美国信纸（12240 x 15840 DXA）
- **横向：传入纵向尺寸**——docx-js 会在内部交换宽度和高度；将短边作为 `width`、长边作为 `height` 传入，并设置 `orientation: PageOrientation.LANDSCAPE`
- **绝不要使用 `\n`**——请使用独立的 Paragraph 元素
- **绝不要使用 Unicode 项目符号**——请使用带编号配置的 `LevelFormat.BULLET`
- **PageBreak 必须位于 Paragraph 中**——单独使用会生成无效 XML
- **ImageRun 需要 `type`**——始终指定 png/jpg 等
- **始终使用 DXA 设置表格 `width`**——绝不要使用 `WidthType.PERCENTAGE`（在 Google Docs 中会失效）
- **表格需要双重宽度设置**——同时设置 `columnWidths` 数组和单元格 `width`，且二者必须匹配
- **表格宽度 = columnWidths 之和**——使用 DXA 时，确保它们的总和完全一致
- **始终添加单元格边距**——使用 `margins: { top: 80, bottom: 80, left: 120, right: 120 }` 提供易读的内边距
- **使用 `ShadingType.CLEAR`**——表格底纹绝不要使用 SOLID
- **绝不要使用表格充当分隔线/横线**——单元格具有最小高度，会渲染为空框（页眉/页脚中也一样）；请改为在 Paragraph 上使用 `border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } }`。对于双栏页脚，请使用制表位（参见“制表位”部分），不要使用表格
- **目录仅需要 HeadingLevel**——标题段落上不要使用自定义样式
- **覆盖内置样式**——使用准确的 ID："Heading1"、"Heading2" 等
- **包含 `outlineLevel`**——目录需要此项（H1 为 0，H2 为 1，依此类推）

---

## 编辑现有文档

**按顺序执行全部 3 个步骤。**

### 第 1 步：解包

```bash
python scripts/office/unpack.py document.docx unpacked/
```

提取 XML、进行美化格式化、合并相邻文本运行，并将智能引号转换为 XML 实体（`&#x201C;` 等），以确保它们在编辑后仍能保留。使用 `--merge-runs false` 可跳过文本运行合并。

### 第 2 步：编辑 XML

编辑 `unpacked/word/` 中的文件。相关模式请参见下方“XML 参考”。

除非用户明确要求使用其他名称，否则对修订和批注使用 **"Claude" 作为作者**。

**直接使用 Edit 工具进行字符串替换。不要编写 Python 脚本。** 脚本会引入不必要的复杂性。Edit 工具会准确显示将要替换的内容。

**关键：新内容请使用智能引号。** 添加包含撇号或引号的文本时，请使用 XML 实体生成智能引号：

```xml
<!-- 使用这些实体实现专业排版 -->
<w:t>这里&#x2019;有一句引语：&#x201C;你好&#x201D;</w:t>
```

| 实体 | 字符 |
|--------|-----------|
| `&#x2018;` | ‘（左单引号） |
| `&#x2019;` | ’（右单引号/撇号） |
| `&#x201C;` | “（左双引号） |
| `&#x201D;` | ”（右双引号） |

**添加批注：** 使用 `comment.py` 处理跨多个 XML 文件的样板内容（文本必须预先进行 XML 转义）：

```bash
python scripts/comment.py unpacked/ 0 "包含 &amp; 和 &#x2019; 的批注文本"
python scripts/comment.py unpacked/ 1 "回复文本" --parent 0  # 回复批注 0
python scripts/comment.py unpacked/ 0 "文本" --author "Custom Author"  # 自定义作者名称
```

然后向 document.xml 添加标记（参见“XML 参考”中的“批注”）。

### 第 3 步：打包

```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

通过自动修复进行验证、压缩 XML，并创建 DOCX。使用 `--validate false` 可跳过验证。

**自动修复将处理：**

- `durableId` >= 0x7FFFFFFF（重新生成有效 ID）
- 带空白字符的 `<w:t>` 缺少 `xml:space="preserve"`

**自动修复无法处理：**

- XML 格式错误、无效的元素嵌套、缺失关系、架构违规

### 常见陷阱

- **替换整个 `<w:r>` 元素**：添加修订时，请将整个 `<w:r>...</w:r>` 块替换为互为同级元素的 `<w:del>...<w:ins>...`。不要在文本运行内部插入修订标签。
- **保留 `<w:rPr>` 格式**：将原始文本运行的 `<w:rPr>` 块复制到修订文本运行中，以保留粗体、字号等格式。

---

## XML 参考

### 架构合规性

- **`<w:pPr>` 中的元素顺序**：`<w:pStyle>`、`<w:numPr>`、`<w:spacing>`、`<w:ind>`、`<w:jc>`，最后是 `<w:rPr>`
- **空白字符**：对于带有前导/尾随空格的 `<w:t>`，添加 `xml:space="preserve"`
- **RSID**：必须为 8 位十六进制数（例如 `00AB1234`）

### 修订

**插入：**

```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>插入的文本</w:t></w:r>
</w:ins>
```

**删除：**

```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>删除的文本</w:delText></w:r>
</w:del>
```

**在 `<w:del>` 内部**：使用 `<w:delText>` 而不是 `<w:t>`，使用 `<w:delInstrText>` 而不是 `<w:instrText>`。

**最小化编辑**——只标记发生变化的内容：

```xml
<!-- 将“30 天”改为“60 天” -->
<w:r><w:t>期限为 </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> 天。</w:t></w:r>
```

**删除整个段落/列表项**——移除段落的全部内容时，还要将段落标记标记为已删除，使其与下一段合并。在 `<w:pPr><w:rPr>` 内添加 `<w:del/>`：

```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- 列表编号（如果存在） -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>正在删除的整个段落内容……</w:delText></w:r>
  </w:del>
</w:p>
```

如果 `<w:pPr><w:rPr>` 中没有 `<w:del/>`，接受修订后会留下一个空段落/列表项。

**拒绝其他作者的插入**——将删除嵌套在对方的插入中：

```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>对方插入的文本</w:delText></w:r>
  </w:del>
</w:ins>
```

**恢复其他作者的删除**——在其后添加插入（不要修改对方的删除）：

```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>删除的文本</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>删除的文本</w:t></w:r>
</w:ins>
```

### 批注

运行 `comment.py`（参见第 2 步）后，向 document.xml 添加标记。对于回复，请使用 `--parent` 标志，并将标记嵌套在父批注的标记内部。

**关键：`<w:commentRangeStart>` 和 `<w:commentRangeEnd>` 是 `<w:r>` 的同级元素，绝不能位于 `<w:r>` 内部。**

```xml
<!-- 批注标记是 w:p 的直接子元素，绝不位于 w:r 内部 -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>已删除</w:delText></w:r>
</w:del>
<w:r><w:t> 更多文本</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

<!-- 批注 0 内嵌套回复 1 -->
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>文本</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### 图像

1. 将图像文件添加到 `word/media/`
2. 将关系添加到 `word/_rels/document.xml.rels`：

```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```

3. 将内容类型添加到 `[Content_Types].xml`：

```xml
<Default Extension="png" ContentType="image/png"/>
```

4. 在 document.xml 中引用：

```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- EMU：914400 = 1 英寸 -->
    <a:graphic>
      <a:graphicData uri=".../picture">
        <pic:pic>
          <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>
```

---

## 依赖项

- **pandoc**：文本提取
- **docx**：`npm install -g docx`（新文档）
- **LibreOffice**：PDF 转换（通过 `scripts/office/soffice.py` 为沙盒环境自动配置）
- **Poppler**：使用 `pdftoppm` 生成图像
