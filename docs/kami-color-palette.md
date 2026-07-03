# Kami 配色方案提取

本文档提取自 `libraries/kami` 的 `references/tokens.json`、`styles.css`、`CHEATSHEET.md` 与 `references/design.md`。这套配色的核心不是丰富色相，而是：**暖纸色画布、暖灰文字、单一墨蓝强调色**。

## 设计原则

1. 页面背景使用暖纸色 `#f5f4ed`，避免纯白。
2. 只使用一个主要强调色：墨蓝 `#1B365D`。
3. 所有灰色都保持暖调，避免冷灰、蓝灰和中性纯灰。
4. 墨蓝只用于焦点、操作、关键数字、当前状态和轻量装饰，面积建议不超过页面的 5%。
5. 标签和浅色强调底必须使用实体十六进制颜色，不使用 `rgba()` 叠色。
6. 阴影应非常轻，优先使用边框、细线和低透明度柔和阴影表达层级。

## 核心色板

| Token | Hex | 中文名 | 用途 |
| --- | --- | --- | --- |
| `--parchment` | `#f5f4ed` | 暖纸色 | 页面背景、主画布 |
| `--ivory` | `#faf9f5` | 象牙白 | 卡片、抽屉、浮层、输入框 |
| `--border` | `#e8e6dc` | 暖砂边框 | 主要边框、分隔线、按钮浅底 |
| `--border-soft` | `#e5e3d8` | 柔和边框 | 次级分隔线、列表行线 |
| `--brand` | `#1B365D` | 墨蓝 | 主强调色、CTA、当前状态、关键数据 |
| `--brand-light` | `#2D5A8A` | 亮墨蓝 | 深色表面上的链接或悬停态 |
| `--brand-tint` | `#EEF2F7` | 极浅蓝灰 | 轻量标签、浅选中背景、代码内联底 |
| `--tag-bg` | `#E4ECF5` | 标签蓝灰 | 默认标签背景、较强的浅强调底 |
| `--near-black` | `#141413` | 近黑 | 一级正文、标题 |
| `--dark-warm` | `#3d3d3a` | 暖深灰 | 二级正文、表头、说明性链接 |
| `--charcoal` | `#4d4c48` | 炭灰 | 日文/韩文字体较细时的正文补偿色 |
| `--olive` | `#504e49` | 橄榄灰 | 描述、摘要、辅助正文 |
| `--stone` | `#6b6a64` | 石灰 | 元信息、日期、弱提示 |
| `--breaking-bg` | `#f0e0d8` | 暖桃底 | 破坏性变更或谨慎提示背景 |
| `--breaking-fg` | `#8b4513` | 暖棕字 | 破坏性变更或谨慎提示文字 |

## 角色分层

### 背景与容器

| 层级 | 推荐颜色 | 说明 |
| --- | --- | --- |
| 页面背景 | `#f5f4ed` | 全站主背景，形成温暖纸面感 |
| 普通卡片 | `#faf9f5` | 比背景略亮，依靠边框建立层级 |
| 交互浅底 | `#e8e6dc` | 次级按钮、轻量控件、分隔块 |
| 深色容器 | `#30302e` | 仅用于展示型深色区域，不作为默认站点背景 |
| 深色页面 | `#141413` | 极少使用，当前项目偏好浅色时应避免 |

### 文本

| 层级 | 推荐颜色 | 用途 |
| --- | --- | --- |
| 一级 | `#141413` | 标题、主要正文、重要名称 |
| 二级 | `#3d3d3a` | 普通说明、表头、较重要的辅助文本 |
| 三级 | `#504e49` | 描述、caption、卡片摘要 |
| 四级 | `#6b6a64` | 元信息、时间、计数、弱提示 |

文字层级建议保持四级即可，不再新增第五种灰色。判断暖灰是否合格的简单方法：RGB 中 B 值通常低于或接近 R/G，不出现明显偏蓝的冷灰。

### 强调与状态

| 场景 | 推荐颜色 | 说明 |
| --- | --- | --- |
| 主按钮 | 背景 `#1B365D`，文字 `#faf9f5` | 页面最强操作 |
| 次按钮 | 背景 `#e8e6dc`，文字 `#3d3d3a` | 辅助操作 |
| 当前选中 | 边框/文字 `#1B365D`，背景 `#EEF2F7` | 避免大面积纯蓝填充 |
| 标签 | 背景 `#E4ECF5`，文字 `#1B365D` | 默认技能标签 |
| 轻标签 | 背景 `#EEF2F7`，文字 `#1B365D` | 更克制的信息标签 |
| 警示标签 | 背景 `#f0e0d8`，文字 `#8b4513` | 唯一允许的暖色语义例外 |

## 墨蓝透明度的实体色替代

Kami 明确避免在标签中使用 `rgba()`，推荐把墨蓝在暖纸背景上的透明叠色换算为实体色：

| 等效透明度 | 实体色 | 用途 |
| --- | --- | --- |
| 8% | `#EEF2F7` | 最轻标签、浅选中底 |
| 14% | `#E4ECF5` | 默认标签背景 |
| 18% | `#E4ECF5` | 默认标签背景，保持和 14% 同一实体色 |
| 22% | `#D0DCE9` | 较强选中底，慎用 |
| 30% | `#D6E1EE` | 渐变刷或局部强调，少用 |

## 可直接复用的 CSS 变量

```css
:root {
  --parchment: #f5f4ed;
  --ivory: #faf9f5;
  --border: #e8e6dc;
  --border-soft: #e5e3d8;

  --brand: #1B365D;
  --brand-light: #2D5A8A;
  --brand-tint: #EEF2F7;
  --tag-bg: #E4ECF5;

  --near-black: #141413;
  --dark-warm: #3d3d3a;
  --charcoal: #4d4c48;
  --olive: #504e49;
  --stone: #6b6a64;

  --breaking-bg: #f0e0d8;
  --breaking-fg: #8b4513;
}
```

## 在 Skills-Hub 网站中的建议用法

| 网站元素 | 建议配色 |
| --- | --- |
| 页面背景 | `--parchment` |
| 顶部导航、筛选区、详情抽屉 | `--ivory` + `--border` |
| 项目卡片 | `--ivory` 背景，`--border` 边框，hover 使用轻阴影 |
| 卡片标题 | `--near-black` |
| 卡片描述 | `--olive` |
| 元信息和数量 | `--stone` |
| 主要按钮、激活筛选、关键数字 | `--brand` |
| 技能标签 | `--tag-bg` 背景 + `--brand` 文字 |
| 搜索框 | `--ivory` 背景 + `--border` 边框，focus 用 `--brand` |
| 分隔线 | `--border-soft` |

## 阴影与边框

推荐：

```css
/* 轻边框层级 */
box-shadow: 0 0 0 1px var(--border);

/* 极轻 hover 阴影 */
box-shadow: 0 4px 24px rgba(20, 19, 19, 0.05);
```

避免：

```css
/* 太硬、太重 */
box-shadow: 0 16px 48px rgba(0, 0, 0, 0.22);

/* 冷灰背景 */
background: #f8f9fa;
background: #f3f4f6;
```

## 禁用清单

- 不用纯白 `#ffffff` 作为页面主背景。
- 不引入黄色作为强调色。
- 不引入紫色、绿色、红色等第二套品牌强调色。
- 不使用冷灰背景，例如 `#f8f9fa`、`#f3f4f6`、`#e5e7eb`。
- 不在标签背景中使用 `rgba()`。
- 不让 `#1B365D` 大面积铺满页面，墨蓝只承担焦点。
- 不使用强烈投影制造层级，优先用暖色边框、留白和轻阴影。

## 快速组合

### 默认浅色页面

```css
body {
  background: var(--parchment);
  color: var(--near-black);
}

.panel {
  background: var(--ivory);
  border: 1px solid var(--border);
}
```

### 卡片

```css
.card {
  background: var(--ivory);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--dark-warm);
}

.card:hover {
  box-shadow: 0 4px 24px rgba(20, 19, 19, 0.05);
}
```

### 标签

```css
.tag {
  background: var(--tag-bg);
  color: var(--brand);
  border-radius: 4px;
}
```

### 主按钮

```css
.button-primary {
  background: var(--brand);
  color: var(--ivory);
  border: 1px solid var(--brand);
}
```

## 一句话总结

Kami 的配色可以概括为：**用暖纸色承载内容，用暖灰建立阅读层级，用极少量墨蓝制造焦点**。
