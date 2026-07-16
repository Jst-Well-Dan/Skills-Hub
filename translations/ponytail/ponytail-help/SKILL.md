<!-- source-sha256: 2264d1615117b02b0fd5a69ec84cd2757006471a78e4d6c22eed6d581c1d37a4 -->
---
name: ponytail-help
description: >
  所有 ponytail 模式、技能和命令的快速参考卡。
  单次显示，并非持久模式。触发方式：/ponytail-help、
  "ponytail help"、"what ponytail commands"、"how do I use ponytail"。
---

# Ponytail 帮助

调用时显示此参考卡。仅单次生效，请勿更改模式、
写入标志文件或持久化任何内容。

## 级别

| 级别 | 触发方式 | 变化 |
|-------|---------|-------------|
| **Lite** | `/ponytail lite` | 完成所要求的内容，并用一行指出更省事的替代方案。 |
| **Full** | `/ponytail` | 强制执行阶梯原则：YAGNI → stdlib → 原生功能 → 一行代码 → 最小实现。默认级别。 |
| **Ultra** | `/ponytail ultra` | YAGNI 极端主义。先删除，后添加。构建前先质疑需求。 |

级别会持续生效，直到更改或会话结束。

## 技能

| 技能 | 触发方式 | 功能 |
|-------|---------|--------------|
| **ponytail** | `/ponytail` | 懒人模式本身。采用能正常工作的最简单方案。 |
| **ponytail-review** | `/ponytail-review` | 过度工程审查：`L42: yagni: factory, one product. Inline.` |
| **ponytail-audit** | `/ponytail-audit` | 全仓库过度工程审计：按优先级排列应删除的内容。 |
| **ponytail-debt** | `/ponytail-debt` | 收集 `ponytail:` 捷径注释，整理为可跟踪的债务清单。 |
| **ponytail-gain** | `/ponytail-gain` | 实测影响记分板：更少代码、更低成本、更快速度。 |
| **ponytail-help** | `/ponytail-help` | 本参考卡。 |

Codex 使用 `@ponytail`、`@ponytail-review` 和 `@ponytail-help`；Claude Code
和 OpenCode 使用上述斜杠命令形式（OpenCode 将全部六项都作为
斜杠命令提供）。

## 停用

说出 "stop ponytail" 或 "normal mode"。随时可用 `/ponytail` 恢复。
`/ponytail off` 也有效。

## 配置默认模式

默认模式 = `full`，每次会话都会自动激活。更改方式：

**环境变量**（最高优先级）：
```bash
export PONYTAIL_DEFAULT_MODE=ultra
```

**配置文件**（`~/.config/ponytail/config.json`，Windows：`%APPDATA%\ponytail\config.json`）：
```json
{ "defaultMode": "lite" }
```

设置为 `"off"` 可禁止在会话启动时自动激活，需要时再使用
`/ponytail` 手动激活。

解析优先级：环境变量 > 配置文件 > `full`。

## 更新

启用一次自动更新：打开 `/plugin`，进入 Marketplaces，选择 ponytail，然后启用 Enable auto-update。此后 Claude Code 会在启动时拉取新版本（出现提示时运行 `/reload-plugins`）。手动刷新：先运行 `/plugin marketplace update ponytail`，再运行 `/reload-plugins`。

如果无法识别 `/plugin`，说明你的 Claude Code 版本过旧。请更新（`npm install -g @anthropic-ai/claude-code@latest`，或 `brew upgrade claude-code`）并重启。其他宿主使用各自的更新流程。

## 更多

完整文档和示例：https://github.com/DietrichGebert/ponytail
