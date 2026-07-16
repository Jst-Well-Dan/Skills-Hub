<!-- source-sha256: 3f8714f3030dd12e2b11a60ed5e561c0b2297de5b31251b40f6da081e06ae4ee -->
---
name: baoyu-electron-extract
description: 从任何已安装的 Electron 应用（`.asar` 包）中提取资源和 JavaScript；当存在 `.js.map` 文件时，从中还原原始源码，否则使用 Prettier 格式化压缩代码。当用户想要“提取 Electron 应用”“反编译 Electron”“获取 <app> 的源代码”“检查 app.asar”“看 Electron 应用源码”“提取 .asar”，或询问某个 Electron 桌面应用是如何构建的时使用。跳过 `node_modules`，同时支持 macOS 和 Windows。
version: 1.119.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-electron-extract
    requires:
      anyBins:
        - bun
        - npx
---

# Electron 应用提取

从已安装 Electron 应用的 `app.asar` 中提取资源和代码。当存在 `.js.map` 时，从嵌入的 `sourcesContent` 中还原原始源文件；否则使用 Prettier 格式化压缩代码。Source map 路径会优先相对于 `.js.map` 文件进行解析，因此像 `../../src/main.ts` 这样的打包路径会被还原为 `restored/src/main.ts` 等可读路径，而不是哈希占位符。始终跳过 `node_modules`。支持 macOS 和 Windows。

## 用户输入工具

当此技能需要向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具**，即当前智能体运行时提供的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果不存在此类工具，则发送带编号的纯文本消息，并要求用户针对每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持单次调用提出多个问题，请将所有适用问题合并到一次调用中；如果仅支持单个问题，则按优先级逐一提问。

下文对 `AskUserQuestion` 的具体引用仅为示例——在其他运行时中请替换为本地等效工具。

## 脚本目录

脚本位于 `scripts/` 子目录中。`{baseDir}` = 此 SKILL.md 所在的目录路径。解析 `${BUN_X}` 运行时：如果已安装 `bun` → `bun`；如果 `npx` 可用 → `npx -y bun`；否则建议安装 bun。将 `{baseDir}` 和 `${BUN_X}` 替换为实际值。

| 脚本              | 用途                                                               |
| ----------------- | ------------------------------------------------------------------ |
| `scripts/main.ts` | 应用发现 + asar 提取 + source map 还原 + Prettier 格式化           |

## 使用场景

每当用户想要查看已安装 Electron 应用的内部内容或检查其打包代码时，都应使用此技能。触发短语包括：

- “提取 Electron 应用”“反编译此 Electron 应用”“解包 app.asar”
- “显示 <app> 的源码”“查看 <app> 的内部内容”“<app> 是如何构建的”
- “获取 Codex / Cursor / Discord / Slack / VS Code / Notion / Obsidian / ChatGPT 桌面版的源代码”
- “提取 Electron 应用”“看 <app> 的源码”“反编译 Electron”“解包 app.asar”“还原 source map”

既可以接受**应用名称**（例如 `Codex`），也可以接受**绝对路径**（例如 `/Applications/Codex.app`、`.asar` 文件或 Windows 安装目录）。脚本会处理两个平台上的应用发现。

## 工作流程

**1. 确定输入。** 如果用户尚未提供应用名称或路径，请向其询问。如果用户希望使用自定义输出目录，也一并询问。

**2. 运行脚本。**

```bash
${BUN_X} {baseDir}/scripts/main.ts "<app>" [--output <dir>] [--asar <path>] [--force]
```

如果不确定应用发现是否能找到正确的包，请先使用 `--dry-run`——它会打印解析后的路径并退出，不会修改文件系统。

**3. 处理结果。**

- **成功** → 报告输出路径以及数量统计（已提取 / 已还原 / 已格式化）。
- **存在多个匹配项** → 脚本会列出候选项并以非零状态退出。向用户展示候选项，通过 `AskUserQuestion` 或运行时的等效工具询问要使用哪一个，然后使用选定的绝对路径重新运行。
- **现有的非空输出目录** → 未使用 `--force` 时，脚本会拒绝执行。询问用户是覆盖目录（`--force`），还是选择新的 `--output` 路径。
- **不支持的平台 / 未找到匹配项** → 如果用户知道包的位置，建议传入 `--asar /full/path/to/app.asar`。

**4. 引导用户查看结果。** 默认输出目录为 `~/Downloads/<AppName>-electron-extract/`。最值得查看的子目录取决于发现的内容：

- 存在 `restored/` → 已从 `.js.map` 文件重建原始源码树；应优先查看此目录。
- 仅存在 `extracted/`（没有 source map）→ `extracted/` 中的 JS/CSS 已由 Prettier 就地格式化；请从这里查看。

## Source map 路径还原

脚本应尽可能保留 source map 中的原始源文件名称和目录结构：

- 如果存在 `sourceRoot`，先结合它解析每个 `sources[]` 条目，然后相对于 `extracted/` 内 `.js.map` 文件所在的目录进行解析。
- 将常规的打包器相对路径归并到还原后的项目树中。例如，`.vite/main/index.js.map` + `../../src/main.ts` 会变为 `restored/src/main.ts`。
- 如果源文件路径向上超出 `extracted/`，请将剩余的可读路径保留在 `restored/` 下，而不是对其进行哈希处理。例如，`.vite/main/index.js.map` + `../../../shared/src/lib/foo.ts` 会变为 `restored/shared/src/lib/foo.ts`。
- 从源文件名称中移除 URL/查询参数修饰，包括常见的 `webpack://`、`file://` 和 `?loader` 后缀。
- 仅当源文件名称为空或无法规整为安全文件路径时，才使用 `restored/__unknown/<hash>.<ext>`。
- 继续跳过 `node_modules` 和 `webpack/runtime/*` 条目；它们是打包器或运行时噪声，并非应用源码。

## 用法

```bash
# 按应用名称提取（默认输出：~/Downloads/Codex-electron-extract/）
${BUN_X} {baseDir}/scripts/main.ts Codex

# 按绝对路径提取（适用于 .app 包、安装目录或 .asar 文件）
${BUN_X} {baseDir}/scripts/main.ts "/Applications/Visual Studio Code.app"
${BUN_X} {baseDir}/scripts/main.ts "C:\Users\you\AppData\Local\Programs\codex"
${BUN_X} {baseDir}/scripts/main.ts --asar /Applications/Codex.app/Contents/Resources/app.asar Codex

# 自定义输出目录
${BUN_X} {baseDir}/scripts/main.ts Codex --output ~/work/codex-source

# 在不写入任何内容的情况下预览发现结果
${BUN_X} {baseDir}/scripts/main.ts Codex --dry-run

# 覆盖现有输出目录
${BUN_X} {baseDir}/scripts/main.ts Codex --force

# 机器可读的结果（在 stdout 输出一行 JSON）
${BUN_X} {baseDir}/scripts/main.ts Codex --json
```

## 选项

| 选项              | 简写  | 说明                                                          | 默认值                                   |
| ----------------- | ----- | ------------------------------------------------------------- | ---------------------------------------- |
| `<app>`           |       | 应用名称或绝对路径。除非提供 `--asar`，否则为必填项。         | —                                        |
| `--output`        | `-o`  | 输出目录                                                      | `~/Downloads/<AppName>-electron-extract` |
| `--asar`          |       | 覆盖解析得到的 `.asar` 路径                                   | 自动发现                                 |
| `--force`         | `-f`  | 允许写入现有的非空输出目录                                    | false                                    |
| `--skip-format`   |       | 跳过 Prettier 格式化                                          | false                                    |
| `--skip-restore`  |       | 跳过 source map 还原                                          | false                                    |
| `--no-unpacked`   |       | 不同时复制 `app.asar.unpacked/`                               | false                                    |
| `--dry-run`       |       | 打印解析后的路径并退出，不执行写入                            | false                                    |
| `--json`          |       | 在 stdout 输出一行 JSON 摘要（抑制常规输出）                  | false                                    |

## 输出结构

```
~/Downloads/<AppName>-electron-extract/
├── extract-report.json          # JSON 摘要：数量统计、警告、解析后的路径
├── extracted/                   # 原始 asar 内容（没有 source map 时使用 Prettier 格式化 JS/CSS）
│   └── ...                      # node_modules 保持不变（格式化时跳过）
├── extracted.unpacked/          # 如果存在，则从 <asar>.unpacked/ 复制
│   └── ...                      # 原生模块（.node）、大型资源
└── restored/                    # 仅当至少一个 .js.map 可用时存在
    └── <original/source/tree>   # 根据每个 .js.map 中的 sourcesContent 重建
```

## 注意事项

- 始终跳过 **node_modules**——source map 还原和 Prettier 格式化都会跳过——因为检查应用时，捆绑的依赖项只会产生噪声。
- **Source map 还原**仅在 `.js.map` 嵌入 `sourcesContent` 时有效。这是现代打包器（webpack、esbuild、Vite、rollup）的常见情况。如果 source map 引用了外部 `.ts`/`.js` 文件但未嵌入它们，则会跳过该 source map，改为使用 Prettier 格式化相应的 `.js`。跳过的 source map 会列在 `extract-report.json` 的 `warnings` 下。
- **优先使用可读路径，而非哈希**——不要将 source map 路径中的 `../` 片段自动视为不安全。应先从 source map 所在位置解析它们，再清理最终输出路径，确保其仍位于 `restored/` 下。仅对无法使用的源文件名称采用哈希回退。
- **应用发现**会在 macOS 上搜索 `/Applications` + `~/Applications`，在 Windows 上搜索 `%LOCALAPPDATA%\Programs`、`%PROGRAMFILES%`、`%PROGRAMFILES(X86)%`、`%APPDATA%`。如果发现多个匹配项，脚本会退出并列出它们——请使用绝对路径重新运行。在 Linux 或其他平台上，请显式传入 `--asar /path/to/app.asar`。
- **安全性**——脚本拒绝写入 `/`、用户主目录本身或当前工作目录，并且在未使用 `--force` 时，拒绝填充现有的非空输出目录。
- **无需全局安装**——`@electron/asar` 和 `prettier` 会通过 `npx -y` 即时解析。首次运行时，npx 需要缓存它们，因此速度会较慢。
