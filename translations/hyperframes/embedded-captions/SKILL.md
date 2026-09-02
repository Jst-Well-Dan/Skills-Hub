<!-- source-sha256: e7c07111b78dcd74b60eeccfb375c32ad1af4fa65383d1aea45e3beb25482bac -->
---
name: embedded-captions
description: >
  为现有的单主体口播视频添加字幕或台词，而不编辑
  原始视频。适用于普通逐字字幕、嵌在主体后方的电影感字幕、VFX
  字幕、“炸/特效/酷炫字幕”，或 35 种风格目录中的指定身份。按视觉
  身份路由，而非按后端引擎。安静的 `anchor` 轨道是默认选择；仅当用户明确想要完整的电影化处理时，
  才嵌入每一个词。该工作流端到端在本地运行，
  包括转录和主体抠像；在应用前先拆分多镜头视频。
---

> **首先，保持此技能为最新状态——静默运行，不要询问：** `npx hyperframes skills update embedded-captions`。当所有内容均为最新时这是一次快速无操作；否则会在依赖它之前刷新此技能及其依赖的核心领域技能。

# 嵌入式字幕

**一个目录，预先选定**（[CATALOG.md](CATALOG.md) — 35 种身份；其背后的引擎只是后端细节）。**标准**（默认）构建干净的逐字**轨道**（承载大部分文本的下三分之一字幕）+ 在峰值处合成到场景中、位于主体后方的 **嵌入**高潮。**电影感**为纯嵌入——没有轨道，每条字幕都在主体后方合成（主角字体、累积、遮挡即效果）。**主题**是完整的主题宪法——正文范式 × 主角场景 × 前景特效 × 底片反应，由注册表组合而成（[themes/README.md](themes/README.md)）：`ordnance` `terminal` `neonsign` `stardust` `stomp`。大多数解说 / 配音使用**标准**；**嵌入是稀缺且需赢得的峰值**——嵌入每一个词是常见错误；主题适用于 VFX 级需求（“炸”、“特效”、“像 AE 做的”）。

---

## 操作流程（TL;DR）

经由 `/hyperframes` 路由，意图层仅确认输入（哪个片段），并将身份选择**声明**为延后提问——候选列表需要探测后的片段，因此保留在下面的第 1 步；该层的运行形态问题不适用（视频未改动，没有要审阅的分镜）。存在 `BRIEF.md` 时，其中包含已确认的输入和所有用户备注——先阅读它。

下方的工艺说明很长；但**管线本身很短**——所有确定性内容均经计算或编译，绝不手写：

1. **决策关卡**（拒绝不良片段）→ **从 [CATALOG.md](CATALOG.md) 中选择一个身份**（35 种身份；引擎/编译器通过查找派生——绝不展示模式/类别问题）
2. `hyperframes init`（如果项目目录已存在且其中已有视频则跳过——`matte.cjs`/`transcribe.cjs` 会将目录中的任意视频采纳为 source.mp4）→ **`bash scripts/prepare.sh <project>`**（并行执行抠像 ∥ 转录 ∥ 音频包络，然后使用场景调色板/光学/照明执行 safe-zones v2——一个命令，不遗漏任何内容）
3. **编写一小段创意选择 JSON**（先阅读 `safe-zones.json`）：电影感 → `plan.json` → `fill-timings.cjs` → `fit-fonts.cjs` → `make-composition.cjs`；主题 → `theme.json` → `make-theme.cjs`（轨道/面板/诗歌/接管范式；`anchor` 是安静轨道默认值）
4. **视觉 QA**：`node scripts/preview-frames.cjs <project>` → 约 2 秒/帧的忠实合成预览（不渲染）。在为渲染付费前检查 § Visual QA。
5. `render-and-composite.sh` → 关卡（时序 / 遮挡+主角 / 溢出 / 交接）→ `final.mp4`

容易忽略的承重规则：

- **轨道（默认）+ 嵌入（晋级）。** `drop`（填充词，不显示）/ `rail`（逐字下三分之一字幕，前景，承载大部分文本）/ `embed`（在主体后方合成的峰值词）。**标准模式两者都做**，仅嵌入峰值。参见**§ Caption model**。
- **视频以未改动状态交付（标准/电影感；**主题模式的 PLATE 预算是唯一获准的例外**——由注册表控制的反应节拍（充能变暗、重击、抖动、颗粒）按各主题 DNA 定义，并在抠像合成后应用，因此主体+文字+底片作为一个画面移动）**——字幕是唯一添加内容；抠像只是让主体遮挡嵌入轨道。绝不调色/重着色/为视频添加扫描线。
- 两本规则书：**轨道 → [references/rail.md](references/rail.md)**（简洁），**嵌入工艺 → [references/composition-craft.md](references/composition-craft.md)**（丰富，仅嵌入）。按需略读。

---

## 字幕模型——轨道 + 嵌入

每个口语短语属于以下三者之一：

|           | 含义                                             | 呈现方式                                                                                                                                                    |
| --------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **drop**  | 填充——嗯/呃、口吃、自我修正       | 不显示                                                                                                                                                         |
| **rail**  | 默认——普通口语内容（逐字） | 干净的下三分之一字幕，**前景**，可读。重点词可获得内联 `emphasis` 高亮（强调色 / 活动词弹出）——它仍留在轨道上。 |
| **embed** | 晋级的峰值——标题节拍              | 一个大词在主体**后方**合成（抠像遮挡），设计入场 + 退场                                                                        |

**轨道承载大部分文本；嵌入是稀缺且需赢得的峰值。** 稀缺性按**节拍/块，而非片段**计算：每个块（思想）≤1 个主角，绝不两个同时可见，主角窗口间至少留一个节拍的空气（编译器会对低于 0.6 秒发出警告）。短片段 → 通常 1–2 个；长解说 → 每节约一个。在多个主角中，**作者设定尺寸最大的一个是 APEX**（仅它获得完整锁定嵌入 + 宽度适配提升）；较小的是 **MINOR 峰值**，作为超大强调行沿其列运行（fg，阻尼运动）——不是每个节拍都需要抠像展示，这正是让 apex 成为事件的原因。嵌入每个词仍然是常见错误。

轨道表面身份恰好构建此模型（轨道 = `rail.html`，嵌入 = `index.html` 中的高潮）。列流身份移除轨道并让一切都采用嵌入式——仅为氛围优先于逐字内容的需求推荐，绝不用于必须读清文字的解说 / 配音（CATALOG.md 按身份对此编码）。

---

## 第 0 步——从 CATALOG 中选择一个身份

**一个前端，背后有三种引擎。** 用户从 [CATALOG.md](CATALOG.md) 选择一个身份（35 个条目：10 个经典 + 25 个主题）；引擎、编译器和创作文件均从目录行查找派生。**绝不将“标准 vs 电影感 vs 主题”作为问题展示**——它们是后端名称（即使存在多个引擎，一个产品也只有一个 UX）。目录编码了路由所需的一切：阅读表面、声音、推荐场景、场景需求，以及真正接近的成对身份的邻接说明（loud↔ordnance、neon↔neonsign、cream↔stardust）。

身份选择是一个**偏好关卡**（`../hyperframes-core/references/brief-contract.md` § 1）：在自主模式（“给我惊喜” / “你来决定”）下，自己从候选列表中选择，并说明单行原因，而不是提问。

流程：探测片段 → 从目录中列出 2–3 个身份候选 → 推荐**一个**并给出单行原因 → **用户选择**（自主模式：你选择，同时说明原因）→ 编写该身份的文件。身份与引擎锁定（不可跨组合；打开其中一个即为验证事件——参见 dna/README.md）。

**始终呈现你的推荐并让用户在创作前选择。** 不要静默默认。

（完整身份表位于 [CATALOG.md](CATALOG.md)——路由的唯一事实来源。下方引擎文档描述每个后端的创作契约。）

**推荐启发式**：使用 [CATALOG.md](CATALOG.md) 中的“Shortlisting heuristics”——它们针对身份级别（例如，“炸”会将 ordnance/stomp/terminal/loud 列为候选，并按什么应该爆炸选择），绝不针对类别级别。不确定 → `anchor`。

- **电影感** → 为锁定模板编写 `plan.json`，由 `make-composition.cjs` 编译。
- **主题** → 阅读 [themes/README.md](themes/README.md)，编写 `theme.json`，运行 `scripts/render-theme.sh`（编译 + 渲染 + 底片反应 → **final_fx.mp4**）。

---

## 决策关卡——首先运行

在任一模式前探测视频并分类场景。

```bash
ffprobe <video.mp4>                    # 规格
ffmpeg -ss <t> -i <video.mp4> -vframes 1 sample.png   # 在 20/50/80%
```

阅读样本。若出现以下情况则拒绝：

- 多个说话者 / 硬切（拆分并分别渲染每个镜头，或拒绝）
- 没有人类主体（此技能用于口播）
- 少于 3 秒、**无语音**，或人脸从未清晰可见——`transcribe.cjs` 会在音频接近静音时发出警告（Whisper 会在静音上幻觉出如“Thank you.”这样的词）；**应遵从并拒绝**，而不是给虚构的词添加字幕
- **源视频已有烧录字幕 / 字幕条 / 大量文字图形**——添加第二套字幕系统会冲突，且视频必须保持未改动交付（不覆盖/修补）。烧录文字常常仅在片段中段出现：采样 **1fps 联系表**（`ffmpeg -i in.mp4 -vf "fps=1,scale=160:-1,tile=10x5" sheet.png`），不要相信 3 个抽样帧。
- **转录文本是乱码**——非母语/重口音语音可能被转录为看似自信的胡言乱语。创作前审读 `transcript.json`；如果它不像自然语言，尝试一次 `WHISPER_MODEL=medium`，否则拒绝（逐字轨道上的虚构词比没有字幕更糟）。
- 快速运动的繁忙手持镜头（抠像闪烁）

### 起飞前探测（不花成本，避免最严重的失败）

1. **镜头切换探测。** 在 20%、50%、80% 抽样帧。若出现不同主体/场景，**在切换前裁剪片段**。
2. **信箱 / 柱状黑边探测。** 首帧存在黑边？计算安全内容矩形，并将字幕位置限制在其中。
3. **亮度探测。** 采样字幕区域平均亮度——`under 60` → 浅色文字可直接阅读，`60-180` → 添加字形幕布，`180+` → 不透明文字 + 幕布（绝不使用裸露浅色文字）。**电影感模板为 cream+`screen` 且已锁定**——使用此探测来_选择合适身份_（明亮场景 → `ink`，或不透明轨道的 `anchor` 主题），绝不对其重着色。
4. **按语调推荐身份（你推荐；用户选择——参见第 0 步 + CATALOG.md）。** 解说 / 采访 / 必须读清的文字 → 轨道/面板表面身份；诗意 / 社交 / “电影感” → 按语域选择列流身份；“炸 / 特效 / VFX” / 指定世界观 → 主题身份。不确定 → `anchor`（文字可读，场景安全）——但应提供候选列表并让用户选择。

---

## 管线——5 步

```
1. hyperframes init <project> --non-interactive --video <video.mp4> --skill=embedded-captions
2. bash scripts/prepare.sh <project>       # 抠像 ∥ 转录（并行）→ safe-zones。一个命令。
                                           #   → frames_fg/ transcript.json safe-zones.json
3. [AGENT STEP — 唯一的创意步骤] 编写一小段 JSON；按模式参见下方
   Cinematic: 编写 plan.json → node scripts/fill-timings.cjs → fit-fonts.cjs → make-composition.cjs
   Theme:     编写 theme.json → bash scripts/render-theme.sh <project>   （编译 + 渲染 + 底片 fx）
4. node scripts/preview-frames.cjs <project>   # 约 2 秒/帧合成预览 → § Visual QA（渲染前）
5. bash scripts/render-and-composite.sh <project>  # 关卡 → final.mp4 + history/ 快照
   （主题模式：跳过步骤 3b/5——render-theme.sh 已运行 compile + render-and-composite
    + _postfx.sh；交付物为 final_fx.mp4，final.mp4 为底片反应前版本）
```

第 1 步中的 `init` 会检查已安装技能与 GitHub 上的最新版本，并在存在任何过期项时更新全局集合。

第 3 步因模式而异：

### 第 3 步——电影感模式（纯嵌入）

1. **先阅读 `safe-zones.json`。** 叙事平面应位于 **`zones.hugLeft`/`hugRight`**——紧贴轮廓的干净条带（远离身体的文字会显得漂浮而非嵌入；远角是后备选择，而非默认）。主角默认使用 `heroAnchor`/`heroBands.best`（居中位于主体**上**，约 30–55% 被遮挡）。`recommendation:"fg"` 会将叙事内容移到前景以提高可读性；**只要 `heroBands.feasible`，主角仍保持嵌入**——hero-fg 是最后手段。
2. **DNA 是你在第 0 步选择的身份**（CATALOG.md）——此处不要重新打开选择。根据场景做合理性检查（明亮主角带 luma > 150 需要 `ink`；完整选择指南位于目录，涵盖包括 neon / glitch / chrome / velocity 在内的全部十种）。说明你的选择 + 原因；用户决定。DNA 锁定字体/调色板/混合/运动 + 主角三幕；safe-zones v2（`palette`/`optics`/`lighting`）会自动将其参数化到此场景。
3. **编写 `<project>/cinematic.json`**——`"dna": "<name>"` + 思想**块**，而非原始组：每个块 = 词语行（在分句边界以 2–5 个词分组）+ 它堆叠的平面 + 每行 `css`（仅尺寸/字重/样式——无位置）+ 最多一行标记 `"hero": true`（晋级词；`"text"` 用于显示形式）。模式：`scripts/make-cinematic.cjs` 头部。
4. **编译**：`node scripts/make-cinematic.cjs <project>`——将块降级为 plan.json → index.html。为你生成：遵循转录顺序的时序、块内累积、块间翻页、**主角锁定组合**（主角块的前置上下文、HERO 和后置上下文堆叠为一个以主体为中心的绑定组合——阅读顺序从上到下 = 天然构建的口语顺序；上下文在**前景**漂浮，而主角在**后景**嵌入 = 深度三明治；质量规则确保主角压过上下文）、apex/minor 主角拆分、**天然构建的阅读顺序**、按 safe-zones 的 fg 回退。然后照常运行关卡。_（直接手写 plan.json 仍适用于块无法表达的设计——随后自行运行 `fill-timings.cjs` + `fit-fonts.cjs` + `make-composition.cjs`。）_

### 第 3 步——主题模式（主题宪法）

**首先阅读 [themes/README.md](themes/README.md)**——范式/场景注册表、关联、硬规则和精确的 `theme.json` 模式。

1. 按内容语域**选择主题 DNA**（每个 `themes/<name>.json` 都有 `voice` + `when`）。说明你的选择 + 原因；用户决定。
2. **编写 `<project>/theme.json`**——`dna`、`lines`（逐字、转录顺序；每条 1–5 个词——对于 `takeover`，每行是一张 CARD）、`minors`（强调词）、`hero:{match}`（高潮词/短语；嵌入场景将其排除在 `lines` 外，内联场景和 panel+redact 中则保留）。
3. **渲染**：`bash scripts/render-theme.sh <project>`——编译（编译时逐字完整性关卡）、渲染两层、合成、应用底片反应 → `final_fx.mp4`。在编译和渲染之间使用 `preview-frames.cjs` 进行 Visual QA。

---

## 视觉 QA——渲染前预览

`node scripts/preview-frames.cjs <project> [t…]` 会合成**约 2 秒每帧的忠实预览帧**（在 seek-time 截取字幕层 + 真实视频帧 + 抠像遮挡 + 轨道叠加 = 最终合成在该时刻的外观）。默认样本 = 每个组/高潮窗口。完整渲染需耗时数分钟——绝不要用它来_发现_布局问题。

按此清单检查预览（`<project>/preview/sheet.png`）——这些是几何关卡**无法**捕获的失败：

1. **泛白**——明亮区域（窗口/标志/天空）上的浅色文字：不可读 → 移动平面或更换 DNA/模式（明亮场景 → `ink`）。
2. **文字压文字**——字幕覆盖场景自身文字/图形，或两组字幕相撞。
3. **阅读顺序**——屏幕上的垂直顺序必须匹配口语顺序；主角不得位于后续文字下方。
4. **主角存在感**——高潮应当大，并明显位于主体后方（约 30–55% 被遮挡），而不是边缘中的漂浮标签。
5. **平衡**——一个连贯的列/带，而非散落碎片；边距有呼吸；无任何裁切。

然后执行 [references/reference-bar.md](references/reference-bar.md) 中的**5 项正向检查**（海报测试 · 胆怯测试 · 一瞥层级 · 场景握手 · 空白审计）——失败清单能避免渲染出损坏成品；正向清单才让它_有设计感_。两者均通过时再交付。

**新鲜视角审查（任何面向用户的内容均推荐）：** 你对自己的布局会有确认偏差。若可以生成子代理，只给它预览表和此清单，并要求其逐帧给出 PASS/FIX 结论（“根据 5 点清单审查这些字幕预览；每帧回答 PASS 或具体修复”）。在 plan.json / theme.json 中应用修复，重新编译、重新预览——每轮只花几秒。预览通过后再渲染一次。

---

## DNA 注册表——十种视觉语言（取代模板目录）

两种模式均取自 **[dna/](dna/README.md)**——十种可按场景**参数化**的艺术指导视觉语言（从视频采样强调色、沿测得光线方向的接触阴影、深度匹配模糊、RMS 耦合的主角振幅）：

| DNA             | 语域       | 场景适配                                       | 声音                                                                                              |
| --------------- | -------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **cream**       | 高级-温暖   | 暗/中等亮度暖色场景                            | Inter + 暖奶油色 + screen；发光涌现主角（cinematic-cream 的继承者）                 |
| **ink**         | 高级        | **明亮场景（luma > 150）**                  | 近黑 multiply——文字印在墙上；明亮场景的答案                            |
| **editorial**   | 编辑-奢华 | 内省 / 时尚 / 诗意                | Bodoni Moda，小写斜体主角——杂志优雅                                             |
| **keynote**     | 科技-高级   | 产品 / 发布                                | 不透明白色 Inter 800，正中心静止                                                      |
| **documentary** | 正式         | 采访 / 严肃                             | 烧录式显现，无主角——庄重**就是**风格                                                   |
| **loud**        | 张扬           | 高燃 / 运动 / 社交                           | Anton + 场景采样强调色，单元猛击 + 涟漪；正文在前景**宣布**（`bodyLayer: fg`） |
| **neon**        | 张扬-霓虹      | 霓虹黑色电影 / 夜生活 / 科技黑色电影（暗场景） | 电光青色招牌，点火闪烁，主角像招牌一样通电                            |
| **glitch**      | 张扬-霓虹      | 数字 / 黑客 / AI                           | RGB 分离回声落地时吸附在一起；机器打击乐式时序                               |
| **chrome**      | 张扬-奢华      | Y2K / 时尚科技 / 音乐                      | 液态金属渐变主角 + 保持期间的一次光泽扫过                                       |
| **velocity**    | 张扬-运动     | 运动 / 汽车 / 健身                          | 每个词沿其运动向量到达（拖影+倾斜），主角携速度尾迹掠过            |

按 `safe-zones.json`（`heroAnchor.bandLuma`、`palette.temperature`）× 内容语域选择——[dna/README.md](dna/README.md) 包含决策规则。创作：`cinematic.json` 接受 `"dna": "<name>"`。

引擎由 DNA 生成**主角三幕**（无需创作）：共同可见字幕变暗（铺垫）→ 单字母入场，振幅 ∝ 口语响度（冲击）→ 呼吸 + 发光直至退出（余晖）。

（旧版：`plan.template:"cinematic-cream"` 自动映射到 `dna:"cream"`。已退役的 54 模板库位于技能之外的 `~/Downloads/embedded-captions-archive/standard-templates-54/`；`_motion.md` 仍保留在技能内，作为运动动词参考目录。）

---

## 美学决策——语调 × 镜头 × 平台（作为目录候选输入，而非第二路由器）

按 3 个轴分类片段，并将结果输入 CATALOG.md 的候选筛选——本节绝不自行选择模式/引擎：

**语调**（内容的感觉是什么？）

- 纪录片 | 对话式 | 高能 | 诗意 | keynote | 调查式 | 音乐视频

**镜头**（构图是什么？）

- 特写（头部 + 肩膀）| 中景（躯干+）| 广角（全身+）| 剪辑蒙太奇（混合镜头）

**平台**（将在哪里播放？）

- 9:16 竖屏（TikTok/IG/Shorts）| 16:9 横屏（YouTube/web）| 1:1 方形 | 广播导出

在 [references/direction-catalog.md § Classification matrix](references/direction-catalog.md) 中交叉参考方向语言——随后返回 [CATALOG.md](CATALOG.md) 筛选身份候选（此矩阵用于候选筛选；目录是唯一的路由表面）。

## 构图工艺（嵌入轨道）——嵌入前阅读

完整的**嵌入轨道**手册位于 **[references/composition-craft.md](references/composition-craft.md)**：转录角色标注、短语分组、平面与干净区域锚定、区域一致性、高潮弹出与可读性、边缘呼吸、遮挡三步判断，以及累积/持久性。它规定一个_晋级_短语如何置入场景——在创作任何嵌入内容前阅读（电影感 `plan.json` 或标准 `index.html`）。默认的**轨道**有自己的、更简单的规范 → **[references/rail.md](references/rail.md)**。

---

## 共享知识

| 文档                                                                      | 内容                                                                                                                               |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| [references/rail.md](references/rail.md)                                 | **轨道**——标准下三分之一字幕规范（默认；承载大部分文本）。                                          |
| [references/composition-craft.md](references/composition-craft.md)       | **嵌入轨道手册**——分组、平面、高潮弹出、遮挡判断、累积/持久性。嵌入前阅读。 |
| [dna/README.md](dna/README.md)                                           | **DNA 注册表**——十种场景参数化视觉语言；如何选择。                                                      |
| [references/reference-bar.md](references/reference-bar.md)               | **品味标准**——每个语域的世界级参考 + 5 项正向检查。                                                   |
| [references/aesthetic-principles.md](references/aesthetic-principles.md) | **18 条规则。** 在品味上胜过 Veed AI。首先阅读。                                                                               |
| [references/motion-vocabulary.md](references/motion-vocabulary.md)       | 10 个命名运动原语 + 语调→时序查找                                                                                    |
| [references/direction-catalog.md](references/direction-catalog.md)       | 10 种可交付美学 + 语调×镜头×平台矩阵                                                                               |
| [references/anti-patterns.md](references/anti-patterns.md)               | 已锁定排除的错误（CoreML、letter-spacing 重排等）                                                                      |
| [references/scene-types.md](references/scene-types.md)                   | 墙面何时可用（4 个条件）                                                                                       |
| [references/layout-heuristics.md](references/layout-heuristics.md)       | 平面定位、干净区域选择、crown 3 个条件、pillarbox 数学                                                        |
| [references/typography-presets.md](references/typography-presets.md)     | 字号 × 列宽矩阵（起点）                                                                                  |
| [references/caption-grouping.md](references/caption-grouping.md)         | 词 → 分组规则（停顿、句子边界）                                                                                   |
| [references/failure-modes.md](references/failure-modes.md)               | 开发陷阱的长尾                                                                                                           |
| [references/bespoke-vs-presets.md](references/bespoke-vs-presets.md)     | 预设有时为何失败；克隆并微调模式                                                                                |

**首先阅读美学原则和方向目录。** 其他一切都是实现细节。

---

## 不可协商项

- **人脸绝不能持续 100% 被遮住**——每个 0.3 秒窗口中，人脸 bbox 至少有 30% 未被遮挡。
- **WCAG 对比度**——最终渲染会进行 lint；若失败则修复调色板。
- **确定性**——不使用 `Math.random()`、`Date.now()`、`repeat:-1`。
- **绝不对视频调色/重着色。** 视频保持未改动交付——字幕是唯一添加内容。不得在 a-roll 上添加全帧扫描线 / 双色调 / 变暗 / 暗角。neon-noir/CRT 纹理应属于_字幕元素内部_，而不是覆盖整个画面。
- **口播 / 解说优先轨道。** 不要嵌入整段转录——大部分文字是轨道；仅嵌入峰值。嵌入一切是默认错误。
- **嵌入应稀缺且有间隔。** 每句/节拍 ≤1 个嵌入，绝不相邻或同时可见，至少间隔一个节拍，最多一个 `apex`。高潮 = 每节拍的峰值，**不是**“整段片段的唯一回报”。
- **抠像 = 人（hyperframes `remove-background`，u2net_human_seg，Apache-2.0）。** 按意图进行人体分割，但不是外科级精细：细的偏移家具（麦克风悬臂）通常被排除——字幕会渲染在其上、在人后——而主体附近的大型显著物体（望远镜、桌面设备）仍可能泄漏进抠像并遮挡字幕。主体手持的物体（产品、手机）可能间歇性掉出，导致字幕从其前方穿过。绝不假设：放置主角前在 2-3 个时间戳抽样 `frames_fg/`，并优先选择避开任何泄漏家具的主角位置（`heroAnchor` 可能被泄漏影响而偏离主体——与 frames_bg 交叉检查）。
- **safe-zones 对道具盲目——目测每一条使用的带。** Zones/heroBands 仅对_主体_遮挡 + 亮度评分：位于“干净”区域内的麦克风、望远镜或屏幕对它们不可见（泄漏**进入**抠像的道具会让 `heroAnchor.centerXPct` 偏离人）。创作前提取每个拟用带的**一帧**；若其中存在道具，测量其 bbox 并移动/缩小平面。有两个真实案例之所以能干净交付，只是因为代理确实这样做了。（自动道具显著性是已知缺口；zones 的 `peakLuma` 只捕捉_移动_的明亮物体。）
- **字幕留在画面内。** 电影感模式硬性关卡检查帧溢出；标准模式将 `check-overflow.cjs` 作为警告运行（故意出血是唯一例外——阅读警告）。
- **每条字幕在屏幕上 ≥ 0.5 秒**——更短则不可读。
- **词级时序必须与 transcript.json 相差不超过 80ms**——字幕早/晚 500ms 触发会毁掉场景幻觉。电影感会在渲染前运行 `check-timing.cjs --strict`（经由 render-and-composite.sh）；主题模式则在编译时强制相同的时序（make-theme 的顺序转录匹配器 + 逐字完整性关卡——漂移为编译错误）。绝不要把多个转录词打包到一个条目中（例如 `"FUTURE OF"`，或者一个带有 `IT` + 换行 + `ALL` 堆叠却仅有一个 start/end 的条目）——第二个词会继承第一个词的时间戳并过早触发。即使希望它们在同一视觉行，也要将其拆分为拥有各自时序的独立词条目（使用 CSS `white-space` / 自然换行，而非 `<br>`）。字幕文字 ≠ 转录内容的创意替换（例如用 `"15%"` 替代 `"fifteen percent"`）受支持——在 `check-timing.cjs` 内的 `CREATIVE_SUBS` 中注册。
- **组窗口必须包住其词。** 对每个组，`group.in ≤ min(word.start)` 且 `group.out ≥ max(word.end)`。若 `group.in` 晚于词的开始，词会被静默延迟至容器挂载时（我们曾交付过 800ms 延迟错误）。验证器会强制执行。
- **两个字幕组不得同时在时间和屏幕区域重叠。** 时间重叠的字幕会造成文字压文字堆叠。选项：(a) **空间分离**——将各组置于不重叠的垂直带，使其可以共存（记忆墙级联风格）；(b) **交接**——设置较早组的 `out` ≤ 下一组的 `in`，让屏幕上仅有一组；(c) **有意的分层字体**——在某一组上添加 `"allow_overlap": true` 以静默验证器。验证器从 CSS 估计每个组的垂直 bbox 并标记碰撞。默认选择 (a)——这正是让 cinematic-cream 感觉像逐渐累积的诗，而不是不断替换的字幕轨道。
- **screen 混合在明亮背景（>180 亮度）上失败。** **电影感**模板是 cream + `screen`，且该 DNA **已锁定**（plan 无法对它们重着色）→ 在明亮背景上会泛白，因此选择 `ink`（为明亮表面而打造的凸版印刷）或 `anchor` 主题（不透明轨道表面），而不是覆盖一种视觉风格。
- **不要在词入场时动画化 `letter-spacing` 或 `filter:blur`**——inline-block 重排会导致行跳动。
- **禁止使用 CoreML 抠像**——onnxruntime CoreML EP 的混合精度分区会破坏人脸 alpha（先前 RVM 引擎中已观察到；不要重试）。抠像仅使用 CPU（约 2 fps @1080p ≈ 每 10 秒片段 2-3 分钟；长片段需预留时间）。

---

## 依赖项

- **hyperframes**，已构建（`packages/cli/dist/cli.js`）。脚本会自动解析 checkout：`HYPERFRAMES_ROOT` 环境变量 → 若此技能随 hyperframes _内部_分发则为 repo 根目录 → `~/Downloads/hyperframes`。使用 `bun install && bun run build` 构建。
- **Node 优先；经由 `uvx` 的两个 Python 接触点（无需手动安装）：** 转录通过 `uvx` 运行 WhisperX（词级时序；按 SKILL §transcription 回退），Theme 的 `drawon` 场景在编译时调用 `python3 scripts/gen-stroke-path.py`。其他所有内容均在 hyperframes 已提供的工具链上运行：通过 hyperframes CLI 的 **`remove-background`** 进行抠像（u2net_human_seg；权重自动一次下载，约 168 MB，到 `~/.cache/hyperframes/`），通过 **`sharp`** 进行图像/alpha 数学，通过 **`puppeteer`** 进行布局/遮挡/溢出，以及 **`ffmpeg`**。脚本会从 hyperframes checkout 自动解析这些内容——无需额外安装。
- **转录 = 通过 `uvx` 的 WhisperX**（词级时序 + 对齐；无需手动安装——`transcribe.cjs` 驱动 `uvx whisperx`）。若存在，则回退到现有的词级 `transcript.json`。
- **源视频**——`matte.cjs` / `transcribe.cjs` 会自动解析 `source.mp4`（或 glob 片段 / 读取 `hyperframes.json`），因此 `hyperframes init --video X.mp4` 不需要手动重命名。
- **fps**——`matte.cjs` 按源文件原生帧率提取并记录 `matte.fps`；`render-and-composite.sh` 使用它，以使抠像保持帧对齐。
- 抠像权重**未**内置：`matte.cjs` 调用 hyperframes CLI 的 `remove-background`，它会将 u2net_human_seg（约 168 MB，Apache-2.0）一次下载至 `~/.cache/hyperframes/background-removal/models/`。新机器的首次 prepare 需要网络来进行这一次下载。

若缺少硬依赖，停止并询问用户——不要静默跳过步骤。
