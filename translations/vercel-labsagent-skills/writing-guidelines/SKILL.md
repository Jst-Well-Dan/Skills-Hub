<!-- source-sha256: 89a5f581193289b80af58b980090aeed535047c8df2b55ccbaae0de40283a99d -->
---
name: writing-guidelines
description: 审查文档/文章是否符合写作指南。当用户要求“审查我的文档”“检查写作风格”“审核文章”“审查文档的语言风格和语气”或“根据写作手册检查此页面”时使用。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# 写作指南

审查文件是否符合写作指南。

## 工作原理

1. 从下方源 URL 获取最新指南
2. 读取指定文件（或提示用户提供文件/模式）
3. 根据获取到的指南检查所有规则
4. 以简洁的 `file:line` 格式输出发现的问题

## 指南来源

每次审查前获取最新指南：

```
https://raw.githubusercontent.com/vercel-labs/writing-guidelines/main/command.md
```

使用 WebFetch 获取最新规则。获取到的内容包含所有规则和输出格式说明。

## 用法

当用户提供文件或模式参数时：
1. 从上方源 URL 获取指南
2. 读取指定文件
3. 应用获取到的指南中的所有规则
4. 使用指南中指定的格式输出发现的问题

如果未指定文件，请询问用户要审查哪些文件。
