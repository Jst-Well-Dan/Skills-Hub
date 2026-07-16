<!-- source-sha256: 10673a4dc70a0a057612d443243ab7a5aa4abdd4a0fadc3f6eec5fd71ad5a971 -->
---
name: defuddle
description: 使用 Defuddle CLI 从网页中提取干净的 Markdown 内容，移除杂乱元素和导航以节省 token。当用户提供需要阅读或分析的 URL（例如在线文档、文章、博客文章或任何标准网页）时，使用它代替 WebFetch。不要用于以 .md 结尾的 URL——这些内容已经是 Markdown，请直接使用 WebFetch。
---

# Defuddle

使用 Defuddle CLI 从网页中提取干净、易读的内容。对于标准网页，优先使用它而不是 WebFetch——它会移除导航、广告和杂乱元素，从而减少 token 使用量。

如果尚未安装：`npm install -g defuddle`

## 用法

始终使用 `--md` 输出 Markdown：

```bash
defuddle parse <url> --md
```

保存到文件：

```bash
defuddle parse <url> --md -o content.md
```

提取特定元数据：

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## 输出格式

| 标志 | 格式 |
|------|--------|
| `--md` | Markdown（默认选择） |
| `--json` | 同时包含 HTML 和 Markdown 的 JSON |
| （无） | HTML |
| `-p <name>` | 特定元数据属性 |
