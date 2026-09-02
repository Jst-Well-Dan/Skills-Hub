# AI 动效导演元 Skill

用于把一个主题、想法、文章、脚本或简报转成 motion-first 视频方案，并控制后续制作流程，避免 AI 生成的视频变成一页页 PPT 式讲解。

它不是某一种固定视觉风格，也不是一个单独渲染器。它是视频制作前面的导演层：先确定运动隐喻、镜头节奏、组件选择、素材需求和反 PPT 质检标准，再把任务交给 HyperFrames / Remotion / image generation / 视频生产 skill 执行。

## 做什么类型的视频

- 主题驱动的原创动效视频
- AI 根据内容自由选择组件的视频
- 历史、科技、产品、观点、教程类 motion graphic
- 从脚本到 beat graph 的视频制作规划
- HyperFrames / Remotion 项目前的动效导演方案
- 反 PPT 质检和返修判断

## 核心方法

这个 skill 不从页面、卡片或 bullet list 开始，而是先找一个能运动的视觉隐喻。

典型输出流程：

1. `Motion thesis`：一句话定义这个视频如何运动。
2. `Beat graph`：按时间线规划每一段的叙事功能、主运动对象、状态变化、镜头运动、文本角色和素材需求。
3. `Motion grammar`：从路径运动、状态变形、遮罩揭示、相机推进、信息流、粒子聚合、时间轴等动效语法里选择 2-4 个核心动作。
4. `Asset plan`：判断哪些内容需要生图、图标、SVG、截图、代码生成或 footage。
5. `Implementation route`：决定走 HyperFrames、Remotion、Lottie、Rive、Three.js，或调用现有视频生产 skill。
6. `Anti-PPT gate`：检查是否只是标题 + 文本 + 卡片入场；不通过就重写动效方案。

## 适合使用

- "主题是人类进化历史，做一个非 PPT 式动效视频。"
- "给我一个主题，让 AI 自由选择组件做成视频。"
- "先别写代码，先做 motion thesis 和 beat graph。"
- "这个视频为什么像 PPT，帮我改成真正有动效的视频。"
- "我要长期搭一套视频组件库，让 AI 根据内容自动调度。"

## 不适合使用

- 不用于逐帧复刻参考视频。那更适合 `rn-replica-qc`。
- 不用于固定暗色 SaaS / Magic UI 风格短片。那更适合 `rn-dark-saas-video`。
- 不用于单独制作黑底白字打字片头。那更适合 `rn-bw-text-opener`。
- 不替代最终渲染、音频、字幕、抽帧和归档流程；它负责导演和控制。

## 关键参考

- `references/motion-grammar.md`：运动隐喻和动效语法。
- `references/anti-ppt-gate.md`：反 PPT 检查清单。

## 安装

```bash
npx skills add https://github.com/Pluviobyte/rnskill --skill rn-motion-director
```
