<!-- source-sha256: 08b3083fa76a92f82d93bf67c9fd2221517e220e4d3872c0c69cf4e565e24a1f -->
---
name: general-video
description: >
  在没有专用工作流适用时，或当 BRIEF.md 将 flow 设置为 companion 时，创作或编辑自定义 HyperFrames
  合成。适用于较长或多场景作品、品牌与宣传短片、蒙太奇、静态循环、静态标题卡、素材混剪和自由创作。
  对于短小、无旁白且以动效为主的单元（包括动态标题），请改用 motion-graphics。
  在使用此技能前，请先通过 hyperframes 路由全新创作。
---

# 通用视频

在依赖此工作流之前，运行：

```bash
npx hyperframes skills update general-video
```

成功的无操作表示该技能已是最新版本。更新失败时应呈现失败信息，而不是继续凭记忆操作。

## 1. 应用跨领域源适配器

- **媒体：** 对于任何音频、图像、图标、徽标、配音、调色、LUT、处理/特效、字幕或媒体操作需求，加载 `/media-use`，并遵循 `../media-use/references/resolve.md`（解析、采用、复用）和 `../media-use/references/setup-providers.md`（提供商、认证）。编辑前，对于模糊的素材反馈和具名风格，先使用 `../media-use/references/media-treatments.md`；不得使用 CSS/SVG/不透明度临时拼凑受支持的媒体效果。在首次执行需要认证的提供商操作前，运行 `npx hyperframes auth status`，并逐字转达其输出。若未登录，应用 `../hyperframes-core/references/brief-contract.md` 中的门控：协作模式等待登录或明确选择离线方案；自动模式说明状态并继续使用可用的离线提供商。当没有离线提供商可满足必需能力时，呈现阻塞项。仅采用本地资源不需要认证门控。
- **Figma：** 若任一输入是 `figma.com` URL，先运行 `/figma`。基于其导出的资产、令牌、组件或分镜帧构建。不得直接使用原始 Figma 连接器调用，因为它们会跳过 SVG 清理、媒体来源追踪和品牌令牌绑定。

这些适配器不会改变由 `/hyperframes` 选择的工作流。

## 2. 从项目状态开始

应用第一个匹配的行；不要评估后续状态行：

| 状态                                                       | 操作                                                                                                           |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 特定编辑                                                   | 进行编辑，保留现有项目决策，然后重新运行受影响的检查。不要重新开启发现流程。                                   |
| 存在 `BRIEF.md`                                            | 阅读它。若 `workflow` 指定其他工作流且 `flow` 不是 `companion`，则移交。不要提出简报问题。                    |
| 没有简报，但存在 `hyperframes.json` 或 `STORYBOARD.md`     | 从文件和已记录的偏好中恢复。仅根据已知事实补充 `BRIEF.md`。                                                   |
| 全新创作                                                   | 运行 `/hyperframes` 及其意图层。仅在 `workflow: general-video` 或 `flow: companion` 时返回此处。             |

对于新项目，从简报中选择 kebab-case 目录名，并在编写简报前搭建项目：

```bash
npx hyperframes init "videos/<project>" --non-interactive --example=blank --skill=general-video
```

然后使用 `../hyperframes-core/references/brief-format.md` 在项目根目录编写 `BRIEF.md`。在现有项目中，根目录是包含 `hyperframes.json` 的目录。仅使用 `node <MEDIA_DIR>/scripts/prefs.mjs record --hyperframes <PROJECT_ROOT>` 记录简报格式中指定、且已确认有偏好依据的字段；绝不记录推断出的默认值。此处 `<MEDIA_DIR>` 是已安装 `/media-use` 技能目录，`<PROJECT_ROOT>` 是包含 `hyperframes.json` 的目录。若意图层采用了配方，现在使用 `node <MEDIA_DIR>/scripts/recipe.mjs use --hyperframes <PROJECT_ROOT> --name <name>` 应用它，且不要再次询问。

## 3. 解读运行形态

仅使用 `../hyperframes-core/references/brief-contract.md` 中的规范术语：

| 字段           | 含义                                  | 作用                                                                                |
| -------------- | ------------------------------------- | ----------------------------------------------------------------------------------- |
| `flow`         | 由谁驱动                              | `automation`：选择并执行路线。`companion`：在对话中共同创作。                      |
| `storyboard`   | 分镜是否是审阅界面                    | `yes`：运行计划和草图审阅。`no`：不使用分镜构建。                                  |
| 派生的 `mode`  | 检查点门控的行为方式                  | 遵循简报契约。绝不要求用户命名模式。                                                |

不得为这些状态杜撰同义词。持续的“直接构建”信号由意图层处理，并以 `flow: automation`、`storyboard: no` 的形式传入。

- 对于 `flow: automation`，选择路线，并在首次进度更新中用一行说明。
- 对于特定编辑，直接进行编辑，不得杜撰新路线。

### 协作流程

当 `flow: companion` 时：

- 阅读 `BRIEF.md`，并将已接受的 `## Assets` 与 `## Customizations` 同项目产物核对。完成仍待处理的已接受工作；不要动已完成工作；不得将已接受能力再次当作新能力提供。
- **以导演身份到场，而非承包商。** 选择协作模式的用户选择了参与和质量；诚实的回应是你能设计出的最佳版本，而非你能辩护的最小版本。首个计划应是上限方案：故事弧线（借用最接近的类型视角——菜单 § Genre lenses）、设计规格、每个场景注明名称的运动处理（§ 5 的计划纪律）、转场、音频特征——音乐和声音标记，或刻意的静默——用户素材的放置，以及经设计的开场和结尾。用一行说明每层增加了什么；在命名时标示昂贵项目（渲染时间、登录、计费）。用户可以精简方案；他们不该被迫逐项批准地拼装方案。
- **上限属于概念，而非工具箱。** 每一层都必须服务于简报的信息——任何视频都能以相同方式装扮的处理只是装饰。技艺提升到上限；内容绝不超出请求范围（§ 6）。
- 在检查点之间，`../hyperframes/references/capability-menu.md` 有两种作用。作为触发列表：当用户提及其输入，或构建到达其需求时，提供相关能力。作为每一轮的升级通道：计划、草图或构建检查点可以携带一两个针对用户正在查看素材的可追溯建议（“场景 3 的统计数据适合 count-up 处理”）。提供前先阅读；绝不倾倒完整目录。
- 用户接受能力后，立即产出其工件，并在对应的 `BRIEF.md` 正文部分记录决定。仅当用户明确更改时，才重写 frontmatter 字段并记录已确认偏好。
- 保持相同的分镜、验证、最终预览和渲染批准门控。协作模式改变谁掌舵，而不改变质量要求。

## 4. 在每个阶段前加载必需知识

当条件匹配时，以下阅读均为强制：

| 条件                                                                                                              | 操作前阅读                                                                                                                                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 任何合成 HTML 或场景布局                                                                                         | `/hyperframes-core`；使用 `references/determinism-rules.md` 获取其布局契约                                                                                                                                                             |
| 任何非平凡创作或视觉处理                                                                                         | `/hyperframes-creative` → `references/house-style.md` 和 `references/video-composition.md`                                                                                                                                            |
| 任何运动、动画或场景转场                                                                                         | `/hyperframes-animation`；遵循其路由前往匹配的规则、适配器、蓝图或转场参考                                                                                                                                                             |
| `storyboard: yes`                                                                                                 | `../hyperframes-core/references/storyboard-format.md` 和 `../hyperframes-core/references/review-loop.md`                                                                                                                              |
| 任何媒体资产或操作，包括旁白、BGM、SFX、字幕、调色或变换                                                        | `/media-use`；对于框架播放和放置，还应阅读 `/hyperframes-core` → `references/variables-and-media.md`                                                                                                                                  |
| 多场景组装                                                                                                       | `../hyperframes-core/references/production-loop.md`                                                                                                                                                                                    |
| `flow: companion`，在第一个计划之前                                                                              | `/hyperframes-creative` → `references/story-spine.md` 和 `references/house-style.md`；最接近的类型视角及完整的 `../hyperframes/references/capability-menu.md`——上限方案从这些内容设计，而非凭记忆回想 |
| 协作能力建议、采集、节拍网格、生成式视频、地图、发布或跨工作流能力                                              | `../hyperframes/references/capability-menu.md`                                                                                                                                                                                         |
| 存在设计规格，在最终批准之前                                                                                      | `/hyperframes-creative` → `references/design-adherence.md`                                                                                                                                                                             |

不得以回忆取代这些阅读。渐进式披露只有在实际加载匹配参考时才会节省上下文。

## 5. 执行合成

使用此依赖顺序。仅当其输入缺失时跳过阶段。

1. **计划。** 说明观众弧线、结构、节奏和时长驱动因素。短单场景使用一个文件；三个或更多硬切场景，或任何复用场景，使用子合成。对于叙事弧线，阅读 `/hyperframes-creative` → `references/story-spine.md`；对于节奏，阅读 `references/beat-direction.md`；对于结构，阅读 `/hyperframes-core` → `references/composition-patterns.md`。对于开放式多场景简报，通过 `/hyperframes-creative` → `references/prompt-expansion.md` 扩展提示词。多场景计划引用每个场景的形态：适用时使用 `/hyperframes-animation` → `blueprints-index.md` 中的蓝图 id；不适用时使用从 `rules-index.md` 组合的具名规则——运动名称必须来自这些索引，绝不杜撰。故事真实决定哪些场景存在；引用负责装扮它们。多场景计划还应记录为派发工件：`STORYBOARD.md` 中每个场景一个 `## Frame N` 块——`status: outline`、声明的 `src:`、蓝图/规则引用及节拍文本——**即使 `storyboard: no` 也是如此**。该块是派发单元；分镜仅是审阅界面。
2. **按需审阅计划。** 对于 `storyboard: yes`，在这些块上运行共享审阅循环。对于 `storyboard: no`，无需打开分镜即可继续。当计划暂停仍然发生时，将子代理委派授权（codex 在第 4 步派发所需）纳入该暂停，而不是稍后再次停止。
3. **解析依赖。** 在并行工作前安装注册表块。暂存用户资产，采用现有媒体，并且只解析简报所需内容。当音频时序决定时长时，尽早开始处理音频。
4. **构建场景。** 对于短单场景作品，在添加运动前，于最显眼时刻实现该场景（存在时，已确认线框图就是该最终状态，绝不可重绘），然后依据其引用的蓝图或规则制作动画——在编写运动前，阅读完整配方正文（`/hyperframes-animation` → `blueprints/<id>.md`、`rules/<id>.md`）。

   **派发仅在规模足够大时才值得。** 编写数据包和预热全新工作者上下文会消耗真实分钟和令牌：最多约 6 个短场景的影片，在此上下文中逐场景内联构建更快（实测：5 个短场景内联 ≈ 9 分钟，而数据包化 ≈ 21 分钟）。仅当计划超过该规模时才展开——更多场景，或单个场景本身较重——并且每位工作者分配 **2–3 个场景**，而非一个；在**单一波次**中启动**所有工作者**（第二波几乎会使窗口翻倍）。派发时：

   `node <SKILL_DIR>/scripts/frame-packets.mjs --project "$PROJECT_DIR" --storyboard "$PROJECT_DIR/STORYBOARD.md"`

   构建器会在 `.hyperframes/frame-packets/` 下为每个场景写入一个有边界的数据包（场景的精确分镜块 + 蓝图正文 + 每个引用规则配方，均内联），并写入 `_role.md`（逐字串联 `../hyperframes-core/references/frame-worker-core.md` 与此技能的 `sub-agents/frame-worker.md`——完整工作者角色）。派发工作者——每位分配 2–3 个场景数据包，全部在一波中进行（`../hyperframes-core/references/subagent-dispatch.md`）；每位工作者的提示词携带完整的 `_role.md` 及其数据包——完整粘贴，或提供文件路径让工作者先阅读（两者等效）——再加上包含 `PROJECT_DIR`、其 `frame_id`s 和画布尺寸的派发上下文。等待每个场景的 `compositions/<frame_id>.html` + `compositions/<frame_id>.motion.json`。工作者仅阅读其数据包和设计真相文件；绝不打开 `STORYBOARD.md` 或技能文档。没有委派通道时，回退为串行：在此上下文中一次处理一个数据包，仍只根据数据包工作。

5. **合并运动侧车文件。** 收集工作者的 `compositions/<frame_id>.motion.json` 文件，并将其时长和出场/入场向量带入组装；如果安装了 doctrine 链（`/motion-doctrine`），则在盖接缝之前将其转换至项目账本。
6. **组装。** 使用生产循环挂载场景、媒体、转场、字幕和音频。真实配音时长优先于估算值。
7. **验证。** 在首次 HTML 通过和结构变更后，使用 `npx hyperframes lint` 获取快速反馈。对于最终门控，运行 `npx hyperframes check`；它会在内部重新运行 lint，因此不要在它之前立即冗余地单独运行 lint。对于子合成，检查中点快照。对于多场景工作，审阅动画地图。
8. **最终批准。** 仅在检查通过后打开最终 Studio 预览。询问是渲染还是修改。仅在获得批准后渲染。

## 6. 始终适用的门控

### 严格保持范围

构建用户要求的内容。标题卡不是标题卡加三个场景、音乐和字幕。添加前先提供附加项。

### 在 HTML 之前确立设计

按此顺序解析设计来源：`frame.md` → `design.md` → `DESIGN.md`。将找到的第一个文件视为品牌真相。

当不存在设计规格时，在编写合成 HTML 前完成以下四项：

1. 在 `house-style.md` 和 `video-composition.md` 中确立视觉识别。
2. 为每个非平凡创作编写一句话，说明概念角度。
3. 从 `/hyperframes-creative` → `references/typography.md` 选择可嵌入的字体配对；不得假定云渲染中存在未捆绑的展示字体。
4. 定义焦点元素、边缘锚点、辅助细节和背景处理。

使密度与所请求的格式和信息相匹配。密度示例是对产出帧的指导，而不是杜撰主张、场景或固定元素数量的许可。

对于具名风格或情绪，阅读 `/hyperframes-creative` → `references/visual-styles.md`。当用户需要进行视觉选择且没有已发布预设适合时，阅读 `/hyperframes-creative` → `references/design-picker.md` 并运行其中的交互式设计选择。

### 保留合成契约

定时元素使用 `class="clip"`；根元素及相关祖先元素具有尺寸；每个合成在 `window.__timelines` 上注册一个暂停且可安全 seek 的时间线；渲染必须确定性。不得使用渲染时网络获取、时钟或未设种子的随机性。

### 安全借用工作流

当作品类似已发布工作流时，借用其类型参考作为示例。先运行 `npx hyperframes skills update <workflow-name>`。借用其故事形态和品味，而非其私有脚本、管线状态或目录契约。通用构建仍由此技能负责。

## 7. 完成

只有在以下条件均满足时，运行才算完成：

- 已实现请求范围；
- 对于 `flow: companion`，交付的是方案而不仅是范围：每个场景的引用蓝图或规则均已实现，音频特征存在（或已选择并说明静默），开场和结尾经过设计而非默认；
- `npx hyperframes check` 通过，包括其内置 lint 阶段；
- 存在设计规格时，已根据 `/hyperframes-creative` → `references/design-adherence.md` 审阅设计遵循度；
- 对比度发现项已解决；
- 适用时已检查子合成快照；
- 自动模式交接包含已检查的联系表或快照表；多场景表使用场景中点；
- 交接按适用情况命名最终预览或渲染产物，并报告基于时间的交付物实际时长；
- 多场景工作已审阅 `hyperframes-animation/scripts/animation-map.mjs`；
- 用户在渲染前批准最终 Studio 预览；
- 请求渲染时已验证渲染文件。

最终批准后，按照 `../hyperframes-core/references/review-loop.md` § 4，提供一次将本次运行冻结为配方的选项。
