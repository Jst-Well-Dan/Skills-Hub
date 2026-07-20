<!-- source-sha256: d2e5e6151f07e8660d8458c8bbcf7ba8b0f02caa04c1d535f523352a0d8442fd -->
---
name: text-to-lottie
description: 为本地 Skia Skottie 播放器创建、编辑或修复 Lottie/Bodymovin JSON 动画。适用于文本转 Lottie、SVG/徽标/文字动画、加载器/图标、状态反馈、UI 微交互、下三分之一字幕、图表、数据/统计/图表动画、产品宣传、场景/相机运动、视觉效果、场景编辑、插槽/控件以及 Skottie 调试。
---

# 文本转 Lottie

为官方本地 Skia Skottie 播放器制作可用于生产环境的 Lottie JSON。
交付物是在播放器中可渲染的场景，而不是孤立的 JSON。

## 工作模式

- 使用官方播放器项目并在 Skia Skottie 中验证。不要自行制作自定义查看器，也不要为了验证而切换渲染器。
- 确保此技能可在不同的 Agent Skills 客户端中移植。技能说明中应避免使用特定于宿主的命令、命令模式或编排约定。
- 尽量少提问并采用更可靠的默认值。仅当某项决策会实质性改变输出时才提问，例如透明背景还是全画幅背景、品牌约束、目标格式或用户提供的源素材。
- 优先追求干净、用心且专业的动效，而不是仅仅满足提示词的字面要求。

## 参考资料加载

此 `SKILL.md` 是精简的控制平面。仅加载与任务匹配的一级参考资料。不要打开整个参考资料库。

在创建、编辑、修复或验证场景前，始终阅读 `references/player-contract.md`。如果路由到的参考资料不可用，则继续使用本文件中的内联规则。

| 用户意图 | 存在时应读取的参考资料 |
| --- | --- |
| 任何新建/编辑/修复 Lottie 场景 | `references/player-contract.md` |
| JSON 结构、关键帧、插槽、形状、素材 | `references/lottie-spec-map.md` |
| 徽标动画 | `references/recipe-logo.md`、`references/motion-taste.md`、`references/design-taste.md` |
| 排版、标题、引语、文本显现 | `references/recipe-typography.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 下三分之一字幕、姓名标签、字幕条、叠加层 | `references/recipe-lower-thirds.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 加载器、图标、旋转指示器、徽章动画 | `references/recipe-loaders-icons.md`、`references/motion-taste.md` |
| 成功、错误、警告、完成、空状态 | `references/recipe-loaders-icons.md`、`references/design-taste.md`、`references/motion-taste.md` |
| UI 微交互 | `references/recipe-ui-microinteractions.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 通用的“为此 SVG 添加动画”或 SVG 转 Lottie | `references/recipe-svg-animation.md`、`references/svg-compatibility.md`、`references/motion-taste.md` |
| 相机跟随、平移、缩放、视差、场景运动 | `references/recipe-camera-scene-motion.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 图表、技术线条动画、标注、流程轨迹 | `references/recipe-diagram-technical.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 数据、统计、KPI、图表、指标、仪表板数字 | `references/recipe-data-stats.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 产品发布、功能公告、社交媒体宣传 | `references/recipe-product-promo.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 长文本、多个创意、列表/功能/步骤、时间线、前后对比、问题/解决方案、引语+证明、回顾/故事、产品演示、多语言变体、章节、多节拍序列、单集、跳切/硬切、转场语法 | `references/chapterization-transition-grammar.md`、`references/motion-taste.md` |
| 发光、玻璃、金属、渐变、填充、气泡/爆裂效果 | `references/recipe-visual-effects.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 徽标/图标/UI/下三分之一字幕工作中的 SVG 输入 | 任务配方以及 `references/svg-compatibility.md` |
| 起始简报或可复用的项目方向 | `references/recipe-starter-projects.md`、`references/design-taste.md`、`references/motion-taste.md` |
| 任何“高端”“干净”“极简”“现代”“流畅”或“精致”的限定词 | `references/design-taste.md`（克制的默认设置），以及路由到的配方 |

对于混合提示词，根据主要交付物选择一个主要配方，然后添加源格式或视觉处理所需的辅助参考资料。例如：带发光效果的 SVG 徽标以徽标配方为主，并添加 SVG 兼容性和视觉效果参考；带平移/缩放的产品发布动画使用产品宣传配方，并添加相机场景运动参考；技术 SVG 图表轨迹动画使用图表/技术配方，并添加 SVG 兼容性参考；带玻璃扫光的动态标题使用排版配方，并添加视觉效果参考。

## 工作流程

1. 使用上表对任务进行路由。仅阅读实际存在的相关参考资料。
2. 找到官方播放器项目，并按照下方的目标优先级解析目标场景。编辑前，确认解析后的路径为 `public/projects/<project>/<scene-N>/lottie.json`；覆盖前立即重新读取该当前文件，因为 UI 可能会将插槽编辑写回源文件。
3. 制作前确定背景策略。
4. 编写或更新 `public/projects/<project>/<scene-N>/lottie.json`，并在有帮助时编写或更新 `controls.json`。
5. 验证 JSON，运行或复用开发服务器，使用 `?frame=N` 检查精确帧，并在完成前修复渲染、设计和动效问题。

## 内联规则

### 设计默认规则（始终适用）

以下少量默认规则不可协商，适用于每个经过设计的场景。阅读 `references/design-taste.md` 以了解完整的设计理由，尤其是针对任何包含“高端”“干净”“极简”“现代”或“卡片”要求的提示词。

- 高端意味着做减法，而不是做加法。当提示词提到高端、干净、极简、现代、流畅或精致时，默认保持克制：先移除装饰性界面元素，再考虑添加。高端感来自尺寸、字重、亮度、间距和时序，绝不来自卡片、边框、分隔线、阴影、发光或层叠色调。
- 装饰性界面元素/容器的默认预算为 `0`。除非框架卡片、容器、边框或分隔线能完成留白与对齐无法完成的工作，否则不要添加。分隔网格和列时，首先使用负空间和对齐，其次使用一条细线，最后才考虑填充或带边框的卡片，并且仅在明确合理时使用。
- 只使用一种表面色调。使用一种背景色调。不要叠加两种近黑色或两种近白色色调来伪造“表面”；这样会显得浑浊。如果卡片表面必须与背景不同，应只做一次有明确目的的刻意层级变化。
- 一种分隔线样式，一种颜色。如果确实需要分隔线，所有分隔线都使用同一种粗细和颜色，包括标题线和列分隔线。绝不要为不同分隔线使用略有差异的颜色或粗细。

### 场景规则

- 场景文件位于 `public/projects/<project>/<scene-N>/lottie.json`。
- 按权限优先级解析目标场景：显式文件路径优先；其次是类似 `/<project>/<scene>` 的浏览器 URL 路由；再次是任务中已知的项目/场景；否则创建一个新的安全场景。除非任务明确要求编辑当前屏幕上显示的内容，并且不存在更具体的目标，否则仅将 `/__context` 用于发现、验证或获取播放状态。不要让 `/__context.live` 覆盖已知的文件路径、URL 或项目/场景。仅当 `main-project/scene-1` 仍是未经改动的占位场景时才覆盖它；否则创建新场景。
- 全画幅独立合成应包含一个可见背景图层，并配有 `bgColor` 插槽和 `controls.json` 条目。
- 默认透明的输出包括徽标、图标、加载器、叠加层、下三分之一字幕和从 SVG 派生的素材，除非用户要求添加背景。
- 包含顶层 `v`、`fr`、`ip`、`op`、`w`、`h`、`nm`、`assets` 和 `layers`。将 `op` 视为不包含端点。
- 使用有目的的缓动和分阶段编排。避免默认使用线性运动。根据 `motion-taste.md` 中基于行为的锚点选择缓动（依据运动行为选择，焦点元素的效果最强）；不要退化为所有图层统一使用一种缓动。
- 对重要的可编辑值使用插槽，并在 `controls.json` 标签/范围能够改善属性面板时添加它们。
- 对于 SVG 输入，应保留 viewBox、规范化样式、留意填充规则和交叉区域，并在 Skottie 中验证结果。
- 当场景附带其字体时，原生 Lottie 文本/文本插槽（`ty:5`）可在此播放器中渲染：将 `.ttf`/`.otf`/`.ttc` 放在 `lottie.json` 旁边，在 `fonts.list` 中声明它，并使 `fFamily` 与字体嵌入的字体家族名称一致，然后从文本文档中引用它。加载器会将场景的每种字体传递给 Skottie。优先使用原生文本；仅为有意设计的路径效果（描边显现、字形变形、手写）使用矢量/形状文本。请参阅 player-contract 中的“Native Text”参考资料。

## 验证

完成前：

1. 确认预期目标文件路径为 `public/projects/<project>/<scene-N>/lottie.json`。
2. 验证 JSON：

   ```bash
   node -e "JSON.parse(require('fs').readFileSync('public/projects/<project>/<scene-N>/lottie.json','utf8'))"
   ```

3. 确认官方播放器正在运行，并且场景出现在 `GET /__context` 中。
4. 在浏览器中检查固定帧。对于新场景，检查第 `0` 帧、中间帧和 `op - 1` 帧。
5. 确认背景策略符合使用场景。
6. 检查空白画布、素材缺失、未设置样式的形状、错误的图层顺序、不良缓动、不自然的时序、内容裁切、文本溢出以及可见的 SVG 瑕疵。
7. 仅当动画渲染干净且呈现出明确设计意图时才完成任务。

## 维护评估

正常制作动画时不要读取评估文件。仅在测试或更改此技能时使用它们：

- `evals/trigger-prompts.json`
- `evals/routing-prompts.json`
- `evals/reference-loading-prompts.json`
- `evals/output-rubric.md`
