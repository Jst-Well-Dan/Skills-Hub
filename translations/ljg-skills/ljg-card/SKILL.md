<!-- source-sha256: dfc34922cf3d4fbaee6bfe28f104845d71ec16cdfd23c5522749da0644b7175d -->
---
name: ljg-card
description: "内容铸造器（铸）。将内容转换为 PNG 视觉图。七种模具：-l（默认）长阅读卡，-i 信息图，-m 多张阅读卡（1080x1440），-v 编辑式视觉笔记（问题→失败→转折→顿悟→命名，杂志 + 档案布局），-c 漫画（日式黑白风格），-w 白板（马克笔风格白板布局），-b 大字附件卡（1080x1440，适合小红书的风化碑刻风格）。输出到 ~/Downloads/。当用户说‘铸’、‘cast’、‘做成图’、‘做成卡片’、‘做成信息图’、‘做成海报’、‘视觉笔记’、‘sketchnote’、‘杂志’、‘editorial’、‘漫画’、‘comic’、‘manga’、‘白板’、‘whiteboard’、‘大字’、‘附件图’、‘big fonts’、‘小红书卡片’时使用。取代 ljg-cards 和 ljg-infograph。"
user_invocable: true
version: "2.3.0"
---

# ljg-card: 铸

将内容铸成可见的形态。内容进去，PNG 出来。模具决定形状。

## 参数

| 参数 | 模具 | 尺寸 | 说明 |
|------|------|------|------|
| `-l`（默认） | 长图 | 1080 x auto | 单张阅读卡，内容自动撑高 |
| `-i` | 信息图 | 1080 x auto | 内容驱动的自适应视觉布局 |
| `-m` | 多卡 | 1080 x 1440 | 自动切分为多张阅读卡片 |
| `-v` | 视觉笔记 | 1080 x auto | 编辑式杂志专题：问题→失败→转折→顿悟→命名（6 种布局模具 / 4 种字族对比 / 探案档案细节）|
| `-c` | 漫画 | 1080 x auto | 日式黑白漫画风格，动态选择漫画家视觉语言 |
| `-w` | 白板 | 1080 x auto | 白板马克笔风格，结构化框图+箭头+彩色标记 |
| `-b` | 大字 | 1080 x 1440 | 碑刻大字 + 和紙 + 外阴影，小红书附件风格（单句/短段） |

## 约束

本技能输出为视觉文件（PNG），不适用 L0 中的 Org-mode、Denote 和仅限 ASCII 规范。

## 共享基础

### 获取内容

- URL --> 使用 WebFetch 获取
- 粘贴文本 --> 直接使用
- 文件路径 --> 使用 Read 获取

### 文件命名

从内容提取标题或核心思想作为 `{name}`（中文直接用，去标点，≤ 20 字符）。

### 截图工具

```bash
node assets/capture.js <html> <png> <width> <height> [fullpage]
```

从技能根目录运行。依赖技能根目录下 `node_modules/` 中的 playwright。如报错：

```bash
npm install playwright && npx playwright install chromium
```

### 页脚

- 左侧：标志 + 李继刚（已硬编码在模板中）
- 右侧：内容来源（可选）——有明确来源时显示（如作者名、arxiv ID、网站名等），无来源时留空。使用 `{{SOURCE_LINE}}` 变量：有来源时填 `<span class="info-source">来源文字</span>`，否则为空字符串。适用于 `-l`、`-i`、`-v`、`-c`、`-w` 模具（`-m` 多卡无页脚，不适用）。

### 交付

1. 报告文件路径

## 品味准则

**所有模具共享**。执行任何模具前，先 Read `references/taste.md`，作为视觉质量底线贯穿全流程。

核心：反 AI 生成痕迹——禁 Inter 字体、禁纯黑、禁三等分卡片、禁居中主视觉、禁 AI 文案腔、禁假数据。

## 执行

根据参数选择模具，Read `references/taste.md` + 对应的模式文件，按步骤执行：

### -l（默认）：长图

Read `references/mode-long.md`，按其步骤执行。

模板：`assets/long_template.html`

### -i：信息图

Read `references/mode-infograph.md`，按其步骤执行。

模板：`assets/infograph_template.html`

### -m：多卡

Read `references/mode-poster.md`，按其步骤执行。

模板：`assets/poster_template.html`

### -v：视觉笔记

Read `references/mode-sketchnote.md`，按其步骤执行。

模板：`assets/sketchnote_template.html`

### -c：漫画

Read `references/mode-comic.md`，按其步骤执行。

模板：`assets/comic_template.html`

### -w：白板

Read `references/mode-whiteboard.md`，按其步骤执行。

模板：`assets/whiteboard_template.html`

### -b：大字

Read `references/mode-big.md`，按其步骤执行。

模板：`assets/big_template.html`
