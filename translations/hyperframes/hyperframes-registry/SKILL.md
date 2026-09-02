<!-- source-sha256: 19ca0bf6b757d91963e57b182c3bbf2304362752670bf47093035c75c760e820 -->
---
name: hyperframes-registry
description: 安装、发现并将注册表区块和组件接入 HyperFrames 合成。适用于运行 hyperframes add 或 hyperframes catalog、安装单个条目或所有匹配标签的区块、将已安装条目接入 index.html，或处理 hyperframes.json 的场景。涵盖发现、安装位置、区块子合成接入、组件片段合并，以及编写新的区块或组件以贡献至上游（创意 → 脚手架 → 验证 → PR）。
---

# HyperFrames 注册表

注册表提供可通过 `hyperframes add <name>` 安装的可复用区块和组件。

- **区块** — 独立的子合成（具有自身尺寸、时长和时间线）。通过宿主合成中的 `data-composition-src` 引入。
- **组件** — 效果片段（没有自身尺寸）。直接粘贴到宿主合成的 HTML 中。

## 快速参考

```bash
hyperframes add data-chart              # 安装一个区块
hyperframes add grain-overlay           # 安装一个组件
hyperframes add captions                # 安装所有带 captions 标签的区块
hyperframes add shimmer-sweep --dir .   # 指定特定项目作为目标
hyperframes add data-chart --json       # 机器可读的输出
hyperframes add data-chart --no-clipboard  # 跳过剪贴板（CI/无头环境）
```

安装后，CLI 会输出写入了哪些文件，以及一段可粘贴到宿主合成中的片段。该片段只是起点——在接入区块时，你还需要添加 `data-composition-id`（必须与区块内部合成 ID 匹配）、`data-start` 和 `data-track-index` 属性。

位置参数会优先解析为精确条目名称。如果没有条目匹配且该值是一个标签，该命令会安装所有带有该标签的区块。注册表依赖项会在请求的条目之前安装。`hyperframes add` 仅适用于区块和组件；对于示例，请改用 `hyperframes init <dir> --example <name>`。

## 安装位置

默认情况下，区块安装至 `compositions/<name>.html`。组件默认安装至 `compositions/components/<name>.html`。

这些路径可在 `hyperframes.json` 中配置：

```json
{
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

完整详情请参阅 [install-locations.md](./references/install-locations.md)。

## 接入区块

区块是独立的合成——请通过宿主 `index.html` 中的 `data-composition-src` 引入：

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

关键属性：

- `data-composition-src` — 区块 HTML 文件的路径
- `data-composition-id` — 必须与区块内部 ID 匹配
- `data-start` — 区块在宿主时间线中出现的时间（秒）
- `data-duration` — 区块播放时长
- `data-width` / `data-height` — 区块画布尺寸
- `data-track-index` — 图层顺序（数值越高越靠前）

完整详情请参阅 [wiring-blocks.md](./references/wiring-blocks.md)。

## 接入组件

组件是片段——将其 HTML 粘贴到合成的标记中，将其 CSS 粘贴到样式块中，并将其 JS 粘贴到脚本中（如有）：

1. 阅读已安装的文件（例如 `compositions/components/grain-overlay.html`）
2. 将 HTML 元素复制到合成的 `<div data-composition-id="...">` 中
3. 将 `<style>` 块复制到合成的样式中
4. 将所有 `<script>` 内容复制到合成的脚本中（放在时间线代码之前）
5. 如果组件提供 GSAP 时间线集成（请参阅片段中的注释块），请将这些调用添加到时间线中

完整详情请参阅 [wiring-components.md](./references/wiring-components.md)。

## 发现

使用 CLI 作为主要发现入口：

```bash
npx hyperframes catalog
npx hyperframes catalog --type block
npx hyperframes catalog --type component
npx hyperframes catalog --type block --tag social
npx hyperframes catalog --json
npx hyperframes catalog --human-friendly
```

普通表格和 `--json` 模式只列出匹配项；请使用 `hyperframes add <name>` 安装选定名称。`--human-friendly` 会打开交互式选择器，并立即安装所选条目。在 CI 或代理工作流中，优先使用 `--json`，然后执行显式的 `add`。

如果 CLI 无法访问已配置的注册表，请检查原始清单作为备用方案：

```bash
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

每个条目的 `registry-item.json` 包含：名称、类型、标题、描述、标签、尺寸（仅区块）、时长（仅区块）和文件列表。

有关按类型和标签筛选的详细信息，请参阅 [discovery.md](./references/discovery.md)。

## 贡献新的区块或组件

如需编写一个新的注册表条目（字幕样式、VFX 区块、转场、下三分之一字幕条或可复用组件），并将其作为上游 PR 提交——而非安装现有条目——请遵循 [contributing.md](./references/contributing.md) 中完整的创意 → 脚手架 → 构建 → 验证 → 预览 → 提交流程。可直接复制粘贴的起始模板（字幕 / VFX / 组件 / `registry-item.json`）位于 [templates.md](./references/templates.md)。
