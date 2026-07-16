<!-- source-sha256: b54257cdc0e5d04488b35b0c797bfe427b24359f0848d3c73924dcacf8da6358 -->
---
name: obsidian-cli
description: 使用 Obsidian CLI 与 Obsidian 仓库交互，以读取、创建、搜索和管理笔记、任务、属性等内容。还支持插件和主题开发，可通过命令重新加载插件、运行 JavaScript、捕获错误、截取屏幕截图以及检查 DOM。当用户要求与其 Obsidian 仓库交互、管理笔记、搜索仓库内容、从命令行执行仓库操作，或开发和调试 Obsidian 插件和主题时使用。
---

# Obsidian CLI

使用 `obsidian` CLI 与正在运行的 Obsidian 实例交互。需要保持 Obsidian 处于打开状态。

## 命令参考

运行 `obsidian help` 查看所有可用命令。此信息始终为最新版本。完整文档：https://help.obsidian.md/cli

## 语法

**参数**使用 `=` 赋值。包含空格的值需使用引号：

```bash
obsidian create name="My Note" content="Hello world"
```

**标志**是不带值的布尔开关：

```bash
obsidian create name="My Note" silent overwrite
```

对于多行内容，使用 `\n` 表示换行，使用 `\t` 表示制表符。

## 文件定位

许多命令接受 `file` 或 `path` 来指定目标文件。如果两者均未提供，则使用当前活动文件。

- `file=<name>` — 按照维基链接的方式解析（仅需名称，无需路径或扩展名）
- `path=<path>` — 从仓库根目录开始的精确路径，例如 `folder/note.md`

## 仓库定位

默认情况下，命令以最近获得焦点的仓库为目标。将 `vault=<name>` 作为第一个参数，可指定特定仓库：

```bash
obsidian vault="My Vault" search query="test"
```

## 常用模式

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

在任何命令中使用 `--copy` 可将输出复制到剪贴板。使用 `silent` 可防止文件打开。在列表命令中使用 `total` 可获取总数。

## 插件开发

### 开发/测试周期

修改插件或主题的代码后，请遵循以下工作流程：

1. **重新加载**插件以应用更改：
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **检查错误**——如果出现错误，请修复后从第 1 步开始重复：
   ```bash
   obsidian dev:errors
   ```
3. 使用屏幕截图或 DOM 检查进行**视觉验证**：
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **检查控制台输出**中是否有警告或非预期日志：
   ```bash
   obsidian dev:console level=error
   ```

### 其他开发者命令

在应用上下文中运行 JavaScript：

```bash
obsidian eval code="app.vault.getFiles().length"
```

检查 CSS 值：

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

切换移动端模拟：

```bash
obsidian dev:mobile on
```

运行 `obsidian help` 查看其他开发者命令，包括 CDP 和调试器控制命令。
