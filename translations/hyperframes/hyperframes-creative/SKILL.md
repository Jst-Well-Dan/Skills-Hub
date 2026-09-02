<!-- source-sha256: c6023035afc137ac5261a9b6d9fd2917278fae13c19666c67f5d30d84253b295 -->
---
name: hyperframes-creative
description: 面向 HyperFrames 视频的非动画创意指导。用于处理设计规范（frame.md / design.md）、调色板、字体排印、旁白、节拍规划、音频响应式视觉效果、构图模式以及品牌 / 风格决策。对于原子级运动模式和场景蓝图，请使用 `hyperframes-animation`。
---

# HyperFrames 创意

品牌、节奏、风格、旁白和构图指导。在 `hyperframes-core` 的技术契约就绪后使用。

如需运动模式、场景蓝图、转场和 CSS 标记效果，请使用 `hyperframes-animation` — 本技能有意不涉及动画。

> **对于任何非简单构图，请先阅读以下两项——它们优先于网页设计直觉：**
>
> - `references/house-style.md` — “理解提示词，生成真实内容”、需要质疑的懒惰默认项，以及背景/前景分层配方。这能将字面重设计转化为一个 _概念_。
> - `references/video-composition.md` — 视频媒介的尺度、深度和前景细节。它说明了如何避免空洞的网页式布局，同时不强加统一的元素数量。
>
> 跳过它们是产生通用、网页式输出的最大原因。它们不是下方路由表中的可选行——对于任何超过单行编辑的工作，在选择颜色或编写 HTML 前，请同时打开两者。

## 工作流程

1. 如果项目有设计规范，**请先阅读它**，并将其 frontmatter 令牌视为品牌事实（颜色、字体、间距、语气、约束）。要读取哪个文件（优先级 `frame.md` → `design.md` → `DESIGN.md`）以及如何解析它（frontmatter = 规范，正文 = 上下文），均在 [`references/design-spec.md`](references/design-spec.md) 中统一定义——请依照该文档解析并加载。
2. 如果不存在设计规范且用户要求视觉指导，请选择一条路径：
   - 现成的 frame-preset（可选）→ `frame-presets/`（将 `FRAME.md` 采用为 `frame.md`；参见 `references/design-spec.md`）
   - 命名风格或情绪 → `references/visual-styles.md`
   - 快速默认值 → `references/house-style.md`
   - 交互式选择 → `references/design-picker.md`
3. 对于多场景工作，请在编写 HTML 前规划节拍与节奏 → `references/beat-direction.md`。对于场景转场，请跳转至 `hyperframes-animation/transitions/`。
4. 对于运动密集型工作，请阅读 `references/motion-principles.md`（高层护栏），然后前往 `hyperframes-animation` 获取原子规则。

## 路由

| 主题                                                                          | 阅读内容                                       |
| ----------------------------------------------------------------------------- | ---------------------------------------------- |
| 将现成的 frame-preset 采用为 `frame.md`（可选）                               | `frame-presets/` · `references/design-spec.md` |
| 默认调色板、运动、字体排印、需要质疑的懒惰默认值                              | `references/house-style.md`                    |
| 命名风格预设、从情绪到风格的路由                                              | `references/visual-styles.md`                  |
| 调色板专用颜色令牌                                                            | `palettes/*.md`                                |
| 构图模式——PiP、文字置于主体后方、标题卡、幻灯片展示                           | `references/composition-patterns.md`           |
| 统计数据 / 信息图呈现                                                         | `references/data-in-motion.md`                 |
| 面向开放式提示词的结构化扩展                                                  | `references/prompt-expansion.md`               |
| 视频媒介的密度、尺度、颜色、画面构图                                          | `references/video-composition.md`              |
| 按节拍指导、节奏规划、转场时机                                                | `references/beat-direction.md`                 |
| 创作后规范验证（颜色、字体、圆角、间距、深度）                                | `references/design-adherence.md`               |
| 高层运动护栏和 GSAP 质量规则                                                  | `references/motion-principles.md`              |
| 字体选择、搭配、渲染视频中的字体护栏                                          | `references/typography.md`                     |
| 故事准则——钩子语言、价值先于证据、将分镜作为提案                              | `references/story-spine.md`                    |
| 脚本节奏、语气、开场、数字发音                                                | `references/narration.md`                      |
| 映射到运动效果的预计算音频频段                                                | `references/audio-reactive.md`                 |

## 脚本

- `scripts/contrast-report.mjs` — 检查渲染帧中的对比度警告。
- `scripts/extract-audio-data.py` — 为音频响应式构图预先提取音频频段。
- `scripts/package-loader.mjs` — 捆绑创意工具的支持脚本。

`contrast-report.mjs` 会优先从当前项目解析辅助包，然后可以引导加载捆绑的 HyperFrames 包版本。仅当在捆绑 CLI/技能安装环境之外运行该技能，并且需要显式固定该引导版本时，才设置 `HYPERFRAMES_SKILL_PKG_VERSION=<version>`。

从仓库根目录使用显式路径运行，例如：

```bash
python skills/hyperframes-creative/scripts/extract-audio-data.py <audio-file>
```

动画分析（`animation-map.mjs`）位于 `hyperframes-animation/scripts/`。

## 边界

- 不要覆盖 `hyperframes-core` 技术规则。
- 不要为最简技术构图强制要求设计系统。
- 除非请求明确需要，或你先提出扩展建议，否则不要添加额外场景、旁白、音乐、字幕或转场。
- 保持配方引用与任务相关；不要为简单编辑阅读每一份参考资料。
