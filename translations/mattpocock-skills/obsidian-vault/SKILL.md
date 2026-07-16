<!-- source-sha256: 7bed1d552aa5e9345e493cd62cb13e65c5d829d153c349afdb2cb91c809fa6c4 -->
---
name: obsidian-vault
description: 使用维基链接和索引笔记在 Obsidian 仓库中搜索、创建和管理笔记。当用户想要在 Obsidian 中查找、创建或整理笔记时使用。
---

# Obsidian 仓库

## 仓库位置

`/mnt/d/Obsidian Vault/AI Research/`

根目录下基本采用扁平结构。

## 命名约定

- **索引笔记**：汇总相关主题（例如 `Ralph Wiggum Index.md`、`Skills Index.md`、`RAG Index.md`）
- 所有笔记名称使用**标题式大小写**
- 不使用文件夹进行组织，而是使用链接和索引笔记

## 链接

- 使用 Obsidian 的 `[[wikilinks]]` 语法：`[[Note Title]]`
- 在笔记底部链接到依赖笔记或相关笔记
- 索引笔记仅包含 `[[wikilinks]]` 列表

## 工作流程

### 搜索笔记

```bash
# 按文件名搜索
find "/mnt/d/Obsidian Vault/AI Research/" -name "*.md" | grep -i "keyword"

# 按内容搜索
grep -rl "keyword" "/mnt/d/Obsidian Vault/AI Research/" --include="*.md"
```

或者直接对仓库路径使用 Grep/Glob 工具。

### 创建新笔记

1. 文件名使用**标题式大小写**
2. 将内容写成一个学习单元（遵循仓库规则）
3. 在底部添加指向相关笔记的 `[[wikilinks]]`
4. 如果属于编号序列，则使用分层编号方案

### 查找相关笔记

在整个仓库中搜索 `[[Note Title]]` 以查找反向链接：

```bash
grep -rl "\\[\\[Note Title\\]\\]" "/mnt/d/Obsidian Vault/AI Research/"
```

### 查找索引笔记

```bash
find "/mnt/d/Obsidian Vault/AI Research/" -name "*Index*"
```
