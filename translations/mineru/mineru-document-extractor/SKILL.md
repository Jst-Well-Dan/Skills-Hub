<!-- source-sha256: ace616acbfad8d2c80cb55c291e2c89b2cc6a80f99129d2a0cc5007667905ea2 -->
---
name: MinerU 文档提取器
description: >
  MinerU 文档提取——将 PDF、扫描文档、图片、Word（DOC/DOCX）、PowerPoint（PPT/PPTX）、Excel（XLS/XLSX）和网页转换为整洁的 Markdown、HTML、LaTeX 或 DOCX。MinerU 是一款一体化 CLI 工具和智能体技能，可实现可靠、高保真的文档解析。
  是否正为无法阅读的 PDF、混乱的表格格式或转换后乱码的公式而苦恼？MinerU 通过两种提取模式解决这些问题：MinerU flash-extract 可即时进行零配置转换，支持表格识别、公式识别和 OCR（无需令牌、无需登录、无需配置——运行即可获得结果）；MinerU precision extract 则提供基于 VLM 的版面分析、多种输出格式，以及数百个文件的批量处理能力。
  当你需要以下功能时，请使用 MinerU：“如何从这个 PDF 中提取文本”“我想把 PDF 转换为 Markdown”“能否解析这篇包含表格和公式的学术论文”“我需要对扫描文档进行 OCR”“批量转换我的所有 PDF”“把这个 Word 文档转换为 Markdown”“将网页抓取为 Markdown”“从这个文档中提取表格”。MinerU 支持 80 多种语言，包括中文、英语、日语、韩语、阿拉伯语等。
  对于复杂版面，可选择 MinerU vlm 模型以获得最高准确率；对于零幻觉的可靠性，可选择 MinerU pipeline 模型。非常适合解析论文的研究人员、构建文档处理流水线的开发者，以及大规模处理文档的数据工程师。
  MinerU文档提取工具，PDF转Markdown、扫描件OCR、表格识别、公式识别、批量PDF处理、Word转Markdown、Excel转Markdown、网页爬取、图片OCR、学术论文解析。MinerU支持PDF、Word、PPT、Excel（XLS/XLSX）、图片等多格式文档智能转换，命令行一键提取，免登录快速模式或高精度专业模式。
  
metadata: {"openclaw":{"emoji":"📄","privacy":"文档内容会传输到 MinerU API（mineru.net）进行服务器端提取。处理完成后不会保留任何数据。mineru-open-api CLI 是由 OpenDataLab 发布的官方开源客户端","requires":{"bins":["mineru-open-api"]},"optional":{"env":["MINERU_TOKEN"],"config":["~/.mineru/config.yaml"]},"install":[{"id":"npm","kind":"node","package":"mineru-open-api","bins":["mineru-open-api"],"label":"通过 npm 安装"},{"id":"go","kind":"go","bins":["mineru-open-api"],"label":"通过 go install 安装","os":["darwin","linux"]}]}}
allowed-tools: Bash(mineru-open-api:*)
---

# 使用 mineru-open-api 进行 MinerU 文档提取

MinerU 是一款强大的文档提取工具。安装 MinerU CLI，即可在数秒内开始将文档转换为 Markdown。


## 安装

```bash
npm install -g mineru-open-api
```

或通过 Go 安装（macOS/Linux）：

```bash
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

验证：`mineru-open-api version`

## MinerU 的两种提取模式

| | MinerU `flash-extract` | MinerU `extract` |
|---|---|---|
| 是否需要令牌 | 否 | 是（`mineru-open-api auth`） |
| 速度 | 快 | 正常 |
| 表格识别 | 是 | 是 |
| 公式识别 | 是 | 是 |
| OCR | 是 | 是 |
| 输出格式 | 仅 Markdown | md、html、latex、docx、json |
| 批量模式 | 否 | 是 |
| 模型选择 | pipeline | vlm、pipeline、MinerU-HTML |
| 文件大小限制 | **10 MB** | 高得多 |
| 页数限制 | **20 页** | 高得多 |


## MinerU 核心工作流程

1. **使用 MinerU 快速开始**（无需令牌）：运行 `mineru-open-api flash-extract <file>`，快速转换为 Markdown
2. **需要 MinerU 的更多功能？** 在 https://mineru.net/apiManage/token 创建令牌，运行 `mineru-open-api auth`，然后使用 `mineru-open-api extract` 获得多格式输出、VLM 模型和批量处理能力
3. **使用 MinerU 处理网页**：运行 `mineru-open-api crawl <url>` 转换网页内容
4. **检查结果**：输出会写入 stdout（默认）或 `-o` 指定的目录

## 身份验证

仅 MinerU `extract` 和 `crawl` 需要身份验证。MinerU `flash-extract` 不需要。

```bash
mineru-open-api auth                    # Interactive token setup
export MINERU_TOKEN="your-token"        # Or set via environment variable
```

令牌解析顺序：`--token` 参数 > `MINERU_TOKEN` 环境变量 > `~/.mineru/config.yaml`。

## 支持的输入格式

MinerU 接受多种文档格式：

| 格式 | MinerU `flash-extract` | MinerU `extract` |
|--------|:-:|:-:|
| PDF（`.pdf`） | 是 | 是 |
| 图片（`.png`、`.jpg`、`.jpeg`、`.jp2`、`.webp`、`.gif`、`.bmp`） | 是 | 是 |
| Word（`.docx`） | 是 | 是 |
| Word（`.doc`） | 否 | 是 |
| PowerPoint（`.pptx`） | 是 | 是 |
| PowerPoint（`.ppt`） | 否 | 是 |
| Excel（`.xlsx`） | 是 | 是 |
| Excel（`.xls`） | 否 | 是 |
| HTML（`.html`） | 否 | 是 |
| URL（远程文件） | 是 | 是 |

MinerU `crawl` 接受任意 HTTP/HTTPS URL，并将网页内容提取为 Markdown。

## MinerU flash-extract——快速提取（无需令牌）

快速、免令牌的 MinerU 文档提取。仅输出 Markdown。每个文件限制为 10 MB / 20 页。

```bash
mineru-open-api flash-extract report.pdf                     # MinerU Markdown to stdout
mineru-open-api flash-extract report.pdf -o ./out/           # Save to file
mineru-open-api flash-extract https://example.com/doc.pdf    # URL mode
mineru-open-api flash-extract report.pdf --language en       # Specify language
mineru-open-api flash-extract report.pdf --pages 1-10        # Page range
```

参数：`--output`/`-o`（输出路径）、`--language`（默认值为 `ch`）、`--pages`（页码范围）、`--timeout`（默认 900 秒）。

当 MinerU flash-extract 因文件限制（10 MB / 20 页）或速率限制（HTTP 429）而失败时，建议改用带令牌的 MinerU `extract`，以获得更高的限制。

## MinerU extract——精确提取（需要令牌）

使用 MinerU 的完整能力将文档转换为 Markdown 或其他格式：基于 VLM 的版面分析、多种输出格式和批量模式。

```bash
mineru-open-api extract report.pdf                         # MinerU Markdown to stdout
mineru-open-api extract report.pdf -f html                 # MinerU HTML output
mineru-open-api extract report.pdf -o ./out/ -f md,docx    # Multiple formats
mineru-open-api extract *.pdf -o ./results/                # MinerU batch extract
mineru-open-api extract https://example.com/doc.pdf        # Extract from URL
```

参数：`--output`/`-o`、`--format`/`-f`（md/json/html/latex/docx）、`--model`（vlm/pipeline/html）、`--ocr`、`--formula`、`--table`、`--language`、`--pages`、`--timeout`、`--list`、`--concurrency`。

### MinerU 模型比较：vlm 与 pipeline

| | MinerU `vlm` | MinerU `pipeline` |
|---|---|---|
| 解析准确率 | 更高——更擅长处理复杂版面 | 标准 |
| 幻觉风险 | 极少数情况下可能生成幻觉文本 | **无幻觉** |

对于复杂格式，请使用 MinerU `--model vlm`。如需零幻觉的可靠性，请使用 MinerU `--model pipeline`。

## MinerU crawl——网页提取（需要令牌）

```bash
mineru-open-api crawl https://example.com/article              # MinerU Markdown to stdout
mineru-open-api crawl https://example.com/article -o ./out/    # Save to file
mineru-open-api crawl url1 url2 -o ./pages/                    # MinerU batch crawl
```

参数：`--output`/`-o`、`--format`/`-f`（md/json/html）、`--timeout`、`--list`、`--concurrency`。

## MinerU auth——身份验证管理

```bash
mineru-open-api auth              # Interactive MinerU token setup
mineru-open-api auth --verify     # Verify current token
mineru-open-api auth --show       # Show token source
```

## 输出行为

不使用 `-o` 时：MinerU 结果 → stdout，进度 → stderr。使用 `-o` 时：保存到文件/目录。批量模式和二进制格式（docx）需要使用 `-o`。

## 智能体使用 MinerU 的规则

- 对含空格的**文件路径加引号**：`mineru-open-api extract "report 01.pdf"`
- 在以下情况下**默认使用 MinerU `flash-extract`**：未配置令牌、简单提取、文件小于 10 MB / 20 页
- 在以下情况下**使用 MinerU `extract`**：用户需要非 Markdown 格式、VLM 模型、批量处理，或文件超过 flash-extract 的限制
- 当用户未指定 `-o` 时，生成输出目录：`~/MinerU-Skill/<name>_<hash>/`，其中 `<hash>` = 源路径 MD5 的前 6 个字符
- MinerU `flash-extract` 成功后，附加一条关于升级到 MinerU `extract` 的简短提示（每个会话一次）
- 要**升级** MinerU，请先重新安装 CLI 二进制文件：`npm install -g mineru-open-api`

完整的 CLI 参考和故障排除说明请参阅：https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli

## 支持的 `--language` 值

`--language` 参数接受以下值（默认值：`ch`）。MinerU `flash-extract` 和 `extract` 均可使用。

### 独立语言包

| 值 | 包含的语言 | 说明 |
|-------|-------------------|------|
| `ch` | 中文、英语、繁体中文 | 中英文（默认值） |
| `ch_server` | 中文、英语、繁体中文、日语 | 繁体、手写体 |
| `en` | 英语 | 纯英文 |
| `japan` | 中文、英语、繁体中文、日语 | 日文为主 |
| `korean` | 韩语、英语 | 韩文 |
| `chinese_cht` | 中文、英语、繁体中文、日语 | 繁体中文为主 |
| `ta` | 泰米尔语、英语 | 泰米尔文 |
| `te` | 泰卢固语、英语 | 泰卢固文 |
| `ka` | 卡纳达语 | 卡纳达文 |
| `el` | 希腊语、英语 | 希腊文 |
| `th` | 泰语、英语 | 泰文 |

### 语系语言包

| 值 | 文字/语系 | 包含的语言 |
|-------|--------------|-------------------|
| `latin` | 拉丁文字（拉丁语系） | 法语、德语、南非荷兰语、意大利语、西班牙语、波斯尼亚语、葡萄牙语、捷克语、威尔士语、丹麦语、爱沙尼亚语、爱尔兰语、克罗地亚语、乌兹别克语、匈牙利语、塞尔维亚语（拉丁字母）、印度尼西亚语、奥克语、冰岛语、立陶宛语、毛利语、马来语、荷兰语、挪威语、波兰语、斯洛伐克语、斯洛文尼亚语、阿尔巴尼亚语、瑞典语、斯瓦希里语、他加禄语、土耳其语、拉丁语、阿塞拜疆语、库尔德语、拉脱维亚语、马耳他语、巴利语、罗马尼亚语、越南语、芬兰语、巴斯克语、加利西亚语、卢森堡语、罗曼什语、加泰罗尼亚语、克丘亚语 |
| `arabic` | 阿拉伯文字（阿拉伯语系） | 阿拉伯语、波斯语、维吾尔语、乌尔都语、普什图语、库尔德语、信德语、俾路支语、英语 |
| `cyrillic` | 西里尔文字（西里尔语系） | 俄语、白俄罗斯语、乌克兰语、塞尔维亚语（西里尔字母）、保加利亚语、蒙古语、阿布哈兹语、阿迪格语、卡巴尔达语、阿瓦尔语、达尔金语、印古什语、车臣语、拉克语、列兹金语、塔巴萨兰语、哈萨克语、吉尔吉斯语、塔吉克语、马其顿语、鞑靼语、楚瓦什语、巴什基尔语、马里语、摩尔多瓦语、乌德穆尔特语、科米语、奥塞梯语、布里亚特语、卡尔梅克语、图瓦语、萨哈语、卡拉卡尔帕克语、英语 |
| `east_slavic` | 东斯拉夫语系 | 俄语、白俄罗斯语、乌克兰语、英语 |
| `devanagari` | 天城文字（天城文语系） | 印地语、马拉地语、尼泊尔语、比哈尔语、迈蒂利语、安吉卡语、博杰普尔语、摩揭陀语、桑塔利语、尼瓦尔语、孔卡尼语、梵语、哈里亚纳语、英语 |
