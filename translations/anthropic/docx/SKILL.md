<!-- source-sha256: 8017469ea95fb7d28225c62daf8e2f3492a7b516fc64c18c28977cbf8980b7fe -->
---
name: docx
description: "当用户想要创建、读取、编辑或处理 Word 文档（.docx 文件）或 Word 模板（.dotx 文件）时，请使用此技能。触发条件包括：任何对 'Word doc'、'word document'、'.docx'、'.dotx' 的提及，或要求制作带有目录、标题、页码、信头等格式的专业文档。还应在以下情况使用：从 .docx 或 .dotx 文件中提取或重新组织内容、在文档中插入或替换图片、在 Word 文件中执行查找和替换、处理修订或批注，或将内容转换为精美的 Word 文档。如果用户要求以 Word 或 .docx 文件形式交付 'report'、'memo'、'letter'、'template' 或类似成果，请使用此技能。不要将其用于 PDF、电子表格、Google Docs，或与文档生成无关的通用编码任务。"
license: 专有许可。完整条款见 LICENSE.txt
---

# DOCX 创建、编辑与分析

`.docx` 是由 XML 文件组成的 ZIP 压缩包。请根据任务选择处理方式：

| 任务 | 方法 |
|---|---|
| **创建**新文档 | 编写 `docx` (npm) 脚本——参见下方注意事项 |
| **编辑**现有文档 | `unzip` → 编辑 `word/document.xml` → `zip`（docx-js 无法打开现有文件） |
| **读取**内容 | `pandoc -t markdown file.docx` |

> 下方脚本路径均相对于此技能所在目录。

## 使用 docx-js 创建——注意事项

`docx` 已预安装——不要先运行 `npm install`；直接编写脚本并使用 `require('docx')`。仅当该 require 失败时，才运行：`npm install docx`。模型了解其 API；以下是容易踩坑之处：

- **页面大小默认为 A4。** 如需使用 US Letter，请设置 `page: { size: { width: 12240, height: 15840 } }`（DXA；1440 = 1″）。
- **横向页面：** 传入纵向尺寸并设置 `orientation: PageOrientation.LANDSCAPE`——docx-js 会在内部交换宽度和高度。
- **表格需要双重宽度设置：** 在表格上设置 `columnWidths`，并在每个单元格上设置 `width`，两者均使用 `WidthType.DXA`（`PERCENTAGE` 在 Google Docs 中会失效）。各列宽度之和必须等于表格宽度。
- **表格底纹：** 使用 `ShadingType.CLEAR`，绝不要使用 `SOLID`（会渲染成黑色）。
- **列表：** 绝不要直接插入 `•`；应使用包含 `LevelFormat.BULLET` 的 `numbering` 配置。
- **`ImageRun` 必须包含 `type:`**（`"png"`、`"jpg"` 等）。
- **`PageBreak` 必须位于 `Paragraph` 内。**
- **绝不要使用 `\n`**——请使用独立的 `Paragraph` 元素。
- **目录：** 标题必须使用内置的 `HeadingLevel.*`；自定义标题样式必须设置 `outlineLevel`，否则不会出现在目录中。
- **不要使用表格作为水平分隔线**——请改用段落底部边框。
- **点引导符／同一行右对齐：** 在 `TextRun` 内使用 `PositionalTab`（`alignment: PositionalTabAlignment.RIGHT`、`leader: PositionalTabLeader.DOT`），不要使用字面量 `.` 或空格填充。

## 验证输出

写入 `.docx` 后，请将其渲染并进行目视检查：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 100 output.pdf page
ls page-*.jpg   # then Read the images
```

`pdftoppm` 会根据总页数的位数，用零填充页码（`page-01.jpg`…`page-12.jpg`）。

## 编辑现有文档

旧版 `.doc` 文件必须先进行转换：`python scripts/office/soffice.py --headless --convert-to docx file.doc`。

```bash
unzip -q doc.docx -d unpacked/
find unpacked -type l -delete   # strip symlink entries — docx from external parties is untrusted
python scripts/merge_runs.py unpacked/   # coalesce fragmented runs so text is findable
# edit unpacked/word/document.xml in place — do NOT reformat or pretty-print
(cd unpacked && rm -f ../out.docx && zip -Xr ../out.docx .)
python scripts/office/validate.py out.docx --original doc.docx   # XSD checks; --auto-repair fixes common issues
# redlining? add --author "<the name you redlined under>" to check every edit is tracked
```

Word 会将文本拆分到许多 `<w:r>` run 中（修订 ID、拼写检查标记），因此文档中肉眼可见的短语，在 XML 中往往并不是连续字符串。`merge_runs.py` 会合并 `word/document.xml` 中格式完全相同且相邻的 run，同时不改变内容或渲染效果；它也可以直接接收 `.docx` 文件（`python scripts/merge_runs.py doc.docx -o merged.docx`）。

**修订：** 进行红线修订时，请使用 `--author "<the name you redlined under>"` 进行验证（需要同时提供 `--original`）——它会报告所有未被 `<w:ins>`/`<w:del>` 包裹的文本更改。这种错误很容易意外发生，并且在接受修订后的视图中不可见。使用带有 `w:id`、`w:author`、`w:date` 属性的 `<w:ins>`/`<w:del>` 包裹 run。在 `<w:del>` 内，文本元素应为 `<w:delText>`，而不是 `<w:t>`。被删除的段落标记（`<w:pPr><w:rPr><w:del w:id=".." w:author=".." w:date=".."/></w:rPr></w:pPr>`）表示“将此段落合并到下一段”——因此，要彻底删除一个段落，需要使用该标记，并用 `<w:del>` 包裹其中的每个 run。`<w:del/>` 必须位于 rPr 的其他子元素之前；其顺序由 schema 强制规定。

如需生成接受了所有修订的干净副本：`python scripts/accept_changes.py in.docx out.docx`。

接受被删除的段落标记时，应将该段落与其下方段落合并，因此 run 被*全部*删除的段落会消失。Word 会这样处理；但 `accept_changes.py` 和 `pandoc --track-changes=accept` 并不总能做到。两者会以相同方式失败——它们会移除已删除的文本，却留下清空后的段落；如果该段落采用自动编号，阅读时就会显示为一个多余的空项目符号：

- `pandoc --track-changes=accept` 从不合并段落。
- `accept_changes.py`（LibreOffice）能够正确合并段落，但当被删除的段落后面紧跟一个空白间隔段落时除外。

任一视图中的空项目符号都是该视图产生的伪影，并非文档缺陷。请在 XML 中检查段落删除情况。

## 批注

批注需要六个相互关联的文件。请使用辅助脚本——如果还要编辑 `document.xml`，请使用目录模式（可省去一次解压／重新压缩）；否则使用直接处理 `.docx` 的模式：

```bash
# Against an already-unpacked directory (preferred when also placing markers)
python scripts/comment.py unpacked/ "Fees & expenses cap is too low"
python scripts/comment.py unpacked/ "Agreed" --parent 0

# Against a .docx directly
python scripts/comment.py contract.docx "This cap is too low" -o annotated.docx
```

该脚本会写入 `comments.xml`、`commentsExtended.xml`、`commentsIds.xml`、`commentsExtensible.xml`、关系文件以及内容类型覆盖项。批注 ID 会自动分配。随后，它会输出需要添加到 `word/document.xml` 中的 `<w:commentRangeStart>`/`<w:commentRangeEnd>`/`<w:commentReference>` 片段，使批注锚定到特定文本——在放置这些标记之前，批注虽已存在，但不可见。

## 依赖项

`docx`（npm，已预安装——仅当 `require('docx')` 失败时安装）· `pandoc` · LibreOffice（`soffice`）· `pdftoppm`（Poppler）
