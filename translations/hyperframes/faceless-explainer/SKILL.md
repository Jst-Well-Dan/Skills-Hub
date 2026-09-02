<!-- source-sha256: 9243ecde0ad20e729c313913c1543d3e9cbecdf8063d05721b1caafa18a5c7d0 -->
---
name: faceless-explainer
description: "将任意文本——文章、笔记、主题、简报——转化为无露脸讲解视频：没有可捕捉的网站或素材，因此为每个场景创作视觉内容（排版、抽象图形、图表、数据可视化）。适用于主题讲解、概念拆解、操作指南、清单式内容。不是基于网站构建的视频（/product-launch-video —— 宣传或导览）。不明确 → /hyperframes。"
---

> **首先，保持此技能为最新状态——静默运行，无需询问：** `npx hyperframes skills update faceless-explainer`。一切为最新时会快速无操作；否则会在依赖它之前刷新此技能及其依赖的核心领域技能。

> **media-use**：在获取音频/图像/徽标之前，调用 `/media-use` 以从 HeyGen 目录解析 BGM/SFX/图像，并从官方来源解析品牌徽标。先运行 `--adopt` 以登记现有资产。参见 `/media-use` 技能。

# 无露脸讲解视频到 HyperFrames

使用此技能将一段文本转化为讲解视频：选择设计系统，规划教学叙事，并在 HyperFrames 中逐帧构建。**无露脸**意味着所有视觉内容都在后续环节中创作——没有捕捉步骤，也没有真实资产清单。

> **入口是 `/hyperframes`。** 你是编排者。运行每一步，验证其关卡，然后才继续。此技能用于**根据文本解释一个主题，且没有产品和网站可供捕捉**。任何其他意图、仅仅一句“制作视频”，或任何不确定性 → 先阅读 `/hyperframes`——意图层拥有所有路由决策，而抵达此处却没有 `BRIEF.md` 的新建请求无论如何都会经过它（Setup 的开场规则）。

你是编排者。在 `videos/<project>/` 中工作。按顺序运行步骤，并在继续前通过每个关卡。用户关卡为步骤 0、步骤 3 和步骤 6。步骤 0 前阅读 `../hyperframes-core/references/brief-contract.md`——它定义关卡类型，以及 `BRIEF.md` 的 `flow`/`storyboard` 如何推导出管理步骤 3/4/6 关卡的模式。除步骤 5 外，所有步骤都由你亲自完成；步骤 5 中，为每一帧分派一个子代理。不要在此处放入设计或运动规则；它们位于帧工作者子代理、此技能本地的 `../hyperframes-animation/rules/` + `../hyperframes-animation/blueprints/`，以及 `hyperframes-creative` 中。

工作流：步骤 0 设置 → `hyperframes.json`；步骤 1 简报 → `capture/extracted/`；步骤 2 设计系统 → `frame.md`；步骤 3 分镜/脚本 → `STORYBOARD.md` 和 `SCRIPT.md`；步骤 3.1 音频 → `audio_meta.json`；步骤 4 视觉设计 → 丰富后的 `STORYBOARD.md`；步骤 5 帧 → `compositions/frames/NN-*.html` 和 `index.html`；步骤 6 最终渲染 → `renders/video.mp4`。

---

## 步骤 0：设置

目标：以已确认的简报进入，创建 HyperFrames 项目，并让简报可持续保留。

**简报由意图层确认，而不是由此处提问来确认。** 开场规则，按顺序：**(1)** `BRIEF.md` 存在 → 阅读它且不提问——简报已确定，其 `flow`/`storyboard` 推导出模式（brief contract § 1）。**(2)** 没有 `BRIEF.md`，但项目已存在（磁盘上有 `hyperframes.json` / `STORYBOARD.md`）→ 从分镜的 frontmatter 和记录的偏好中恢复；绝不重新盘问一个半成品项目。**(3)** 两者皆无——直接到达此处的新建请求 → 阅读 `/hyperframes` 并运行其意图层（`references/intent-interview.md`）：它会检查配方和已记住的默认值，执行此路由的问题（`../hyperframes/references/routes/faceless-explainer.md`），并返回锁定的简报。编辑请求跳过以上所有内容——直接进行编辑。

仅当 `hyperframes.json` 缺失时初始化。根据主题以 kebab-case 命名 `<project>`，例如 `compound-interest-explained`；绝不使用工作区名称或时间戳。

`npx hyperframes init "videos/<project>" --non-interactive --example=blank --skill=faceless-explainer` — `init` 会根据 GitHub 上的最新版本检查已安装的技能，并在有任何过期时更新全局集合。

初始化后，令 `<PROJECT_ROOT>` 为 `videos/<project>`，并以该目录作为工作目录运行后续所有相对路径命令。以下命令中，`.` 表示 `<PROJECT_ROOT>`；绝不在调用者目录中写入 `.media`、`capture` 或输出文件。

**初始化后立即写入 `BRIEF.md`**（绝不能在此之前——`init` 拒绝非空目录）：使用意图层锁定的简报，格式遵循 `../hyperframes-core/references/brief-format.md`。将 `<MEDIA_DIR>` 解析为已安装的 `/media-use` 技能目录。然后使用 `node <MEDIA_DIR>/scripts/prefs.mjs record --hyperframes .` 记录每个基于偏好的回答（`brief-format.md` 列出了子集）。若意图层采用了配方，运行 `node <MEDIA_DIR>/scripts/recipe.mjs use --hyperframes . --name <name>`；它会将其 `frame.md` 复制到项目中（随后跳过步骤 2），并返回步骤 3 据以起草的骨架。配方填充回答，不填充批准；审查关卡仍会运行。

**在越过 Setup 前展示登录状态**——运行 `npx hyperframes auth status` 并逐字转述其输出。它会报告语音/BGM 将使用 HeyGen 还是本地引擎，并在未登录时说明如何登录。应用以下分支：

- **协作式：**等待用户登录，或明确选择 `offline` / `go`。
- **自主式：**说明状态，并通过可用的本地引擎继续。

当不存在离线提供方时，不要悄悄省略所需能力；明确呈现阻塞因素。不要将此决定并入其他问题，也不要将密钥写入每个仓库的 `.env`。认证归属和离线回退：`/media-use` `references/setup-providers.md` § Providers。

**关卡：**`hyperframes.json` 和 `BRIEF.md` 存在；基于偏好的回答已记录（brief contract § 2）；已展示登录状态（已登录，或正在离线继续）。

---

## 步骤 1：简报（不捕捉）

目标：将用户文本作为信息来源纳入项目。这里**没有网站捕捉，也没有真实资产**——这是无露脸讲解视频。

原样保存用户的完整输入，然后手动创建合成捕捉包：

- `capture/extracted/visible-text.txt` — 完整文章 / 笔记 / 主题 / 简报，逐字保存。这是**信息**来源，不是故事模板（步骤 3 会重塑它）。
- `capture/extracted/tokens.json` — `{ "title": "", "description": "", "colors": [], "fonts": [] }`。从简报填入 `title`/`description`。除非用户明确提供品牌颜色或字体，否则将 `colors`/`fonts` 留空——若提供则添加它们（设计预设无论如何都会提供完整调色板）。

若用户粘贴了脚本或希望保留其措辞，将其逐字保存为 `user_script.txt`；`VO_MODE`（逐字或重构）来自 `BRIEF.md`——当提供脚本时，意图层会询问它。仅当简报不知为何缺少它时在此询问一次，并将回答存储供步骤 3 使用。

**不要**运行 `npx hyperframes capture`（没有 URL）。不要创建 `asset-descriptions.md` 或填充 `capture/assets/`——无露脸视觉内容在步骤 4-5 中创作，而非捕捉。唯一例外：若用户提供真实图像，将其放在 `public/<basename>` 下，并为步骤 3 记录它。

**关卡：**`capture/extracted/visible-text.txt` 和 `capture/extracted/tokens.json` 存在；你能用一句清晰的话说明讲解视频的主题和受众。

---

## 步骤 2：设计系统

目标：选择一个随附帧预设；脚本将其转化为本视频的 `frame.md` + 字幕皮肤。

当 `BRIEF.md` 指定 `style_preset` 时——用户在意图层通过展示案例按视觉选定了它——使用它；仅当简报未说明时，才由你进行判断。然后你做出唯一决策——**选择哪个预设**：阅读 `../hyperframes-creative/references/design-spec.md` 并浏览 `../hyperframes-creative/frame-presets/`；选择其外观最契合主题、语调和受众的预设。然后运行：

```bash
node <SKILL_DIR>/scripts/build-frame.mjs --preset <name> --hyperframes .
```

脚本会以确定性方式完成其余工作：将预设的 `FRAME.md` → `frame.md`，并将其**重混**到 `capture/extracted/tokens.json` 中的任何品牌 tokens 上（按角色将品牌颜色映射到预设的颜色键；将预设的展示字体 + 正文字体替换为品牌字体），将预设的字幕皮肤复制到 `.hyperframes/caption-skin.html`，并执行自我验证（映射损坏时以 1 退出）。一旦以 0 退出即可继续——不要手动编辑规范。

无露脸讲解视频通常**没有品牌颜色/字体**（`tokens.json` 的 colors/fonts 为空）→ 脚本保留预设自身的调色板，这是完整且可交付的设计。仅当用户指定品牌颜色/字体时，才在运行前将它们添加到 `tokens.json`；且仅当映射确实需要时，才在之后手动调整 `frame.md`。

**关卡：**`build-frame.mjs` 以 0 退出——`frame.md` 来自命名预设，且（当预设附带时）`.hyperframes/caption-skin.html` 存在，作为字幕皮肤来源；所选预设已记录为偏好（`--key style_preset --workflow <this workflow>`，brief contract § 2）。

---

## 步骤 3：分镜和脚本

目标：将文本转化为经批准的逐帧教学计划。

阅读 `../hyperframes-creative/references/story-spine.md`（钩子语言、价值先于证据、将分镜视作提案）、`references/story-design.md`、`../hyperframes-animation/blueprints-index.md`、`../hyperframes-core/references/storyboard-format.md` 和 `../hyperframes-core/references/script-format.md`。用它们编写 `STORYBOARD.md`，并在需要旁白时编写 `SCRIPT.md`。从简报的 `length` 设置 frontmatter 的 `duration:`——它只是粗略预期；组装时会报告成片相对于它的落点。

使用 `story-design.md` 处理讲解视频结构（概念 / 操作指南 / 清单 / 故事）、钩子策略、清晰度技巧、情绪节拍、类型枚举映射和 `VO_MODE`。视频顺序来自**叙事设计，而非输入文本的段落顺序**——可重新排序、合并、省略、压缩。作为**软性指引**，查阅 `../hyperframes-animation/blueprints-index.md` 中的角色→蓝图菜单：针对每个节拍，以其候选蓝图所暗示的形状编写旁白，并在适用时标记该候选 `blueprint:` id。教学事实仍决定哪些节拍存在——绝不强行让节拍契合某个蓝图，也绝不因为存在已验证的形状而虚构一个节拍。无露脸视觉内容在下游创作，因此帧**不**携带资产清单：除非用户提供了真实 `public/<basename>` 图像，否则保持 `asset_candidates` 为空。使用分镜和脚本参考中要求的精确字段。

起草后，运行审查循环的计划阶段——`../hyperframes-core/references/review-loop.md` § 1：打开面板（不要询问是否打开），将计划作为提案呈现，并询问两个问题——批准还是修改，以及**先看草图**（推荐）还是跳过。反馈通过聊天或面板的评论文件循环，直至批准。这是一个**检查点关卡**（brief contract § 1）：在自主模式下没有面板，也无需提问——将同一摘要作为告知发布后继续；草图并入构建，唯一的预览问题留到步骤 6。

**关卡：**`STORYBOARD.md` 存在，每帧具有所需叙事字段，需要旁白时 `SCRIPT.md` 存在，并且用户已批准逐帧计划（自主模式：摘要已作为告知发布）。

---

## 步骤 3.1：音频

目标：从已批准脚本生成旁白、词级时间、音乐和音频元数据。

在步骤 3 批准后启动音频。将其在后台运行，然后继续步骤 4。（登录状态已在步骤 0 展示；引擎会自动回退。）

**调用前根据用户要求选择旁白声音。** 若请求指定声音、性别或语调，选择匹配的 voice id，并通过 `--voice <id>` 传入。否则管道默认在 HeyGen 上使用 **Marcia（女声）** / 在 Kokoro 上使用 `am_michael`——因此如“男声”这样的请求若不传标志会被静默忽略。voice id 因提供方而异；根据步骤 0 登录状态所选提供方进行解析：**HeyGen**（已登录）通过 `node <MEDIA_DIR>/audio/scripts/heygen-tts.mjs --list`（或 `GET /v3/voices?engine=starfish`）；**Kokoro**（离线）通过 `<MEDIA_DIR>/audio/references/tts.md` 中的语音表（前缀 `am_`/`bm_` 为男声，`af_`/`bf_` 为女声）。当用户未表达偏好时，先回退到已记住的声音（brief contract § 2），再回退到管道默认值，并说明使用了哪个；仅当两者均未指定时省略 `--voice`。当用户本次明确选择声音时，记录它（`prefs.mjs record --key voice`）。

`node <SKILL_DIR>/scripts/audio.mjs --script ./SCRIPT.md --storyboard ./STORYBOARD.md --hyperframes . --out ./audio_meta.json --voice <voice-id> &`

音频脚本会处理旁白、词级时间、从 HeyGen 音乐库查找 BGM，以及时间元数据。BGM 情绪来自分镜的 `music:` 字段。这使用 HeyGen Audio API 进行检索，而非生成，并使用与 TTS 相同的 `~/.heygen` 凭据。有关提供方详情，阅读 `../media-use/audio/references/tts.md`。

若没有旁白且没有 `SCRIPT.md`，跳过语音生成。若分镜具有音乐情绪，BGM 仍可运行。

**规范的完全静音标记**（在复用此音频模型的工作流间共享）：在 STORYBOARD.md 顶层 YAML 块中使用 `music: none` **并且**没有 `SCRIPT.md`。该组合将项目标为静音——没有旁白、BGM 或 SFX。`audio.mjs` 能识别它且不会生成任何内容（它会删除过期的 `audio_meta.json`；缺少 `audio_meta.json` 是 assemble 视为静音的方式），因此此步骤是干净跳过。`music: none` 配合旁白会保留 TTS，仅关闭 BGM。必须使用此精确拼写——不要自创其他标记。

**关卡：**音频任务已启动，或项目已标为静音（`music: none` + 没有 `SCRIPT.md`）。

---

## 步骤 4：帧视觉设计

目标：为每个分镜帧添加视觉指导、布局意图和运动选择。

**先绘制面板草图（仅协作式）。** 计划获批后立即运行草图阶段——`../hyperframes-core/references/review-loop.md` § 2（不要等待步骤 3.1；草图不使用时间信息）：亲自绘制每一帧线框图，将每帧标为 `built`，当面板完整时暂停并提出唯一布局问题，然后仅修订被指定的草图，直至面板确认。只有在这之后，才将下方视觉设计写入已确认布局。在自主模式中，或用户在步骤 3 选择跳过草图时，跳过此阶段——帧在步骤 5 中直接从 `outline` 进入 `animated`。

原地编辑 `STORYBOARD.md`。不要创建另一份分镜。以 `frame.md` 作为颜色、字体、布局感觉和风格的事实来源。

阅读 `references/visual-design.md`、`../hyperframes-animation/blueprints-index.md`、`references/motion-language.md` 和 `../hyperframes-animation/rules-index.md`。使用 `visual-design.md` 获取方法（带时间码的镜头序列、内联 Layout 词汇和创作视觉处理），以及必需的 `## Video direction` 区块。使用 `../hyperframes-animation/blueprints-index.md` 选择每帧的镜头形状。使用 `motion-language.md`（运动词汇 + 运动准则）和 `../hyperframes-animation/rules-index.md`（有效规则名称）处理运动——不要自创运动名称。

针对每一帧，按 `visual-design.md` 的方法将**带时间码的镜头序列**写入 `STORYBOARD.md`：选择该帧蓝图（或组合），用该帧的**创作**内容实例化，并让每个 Scene 的揭示节奏匹配旁白，使帧在完整时长中持续发展，而非前段堆满后冻结。因为讲解视频无露脸，`focal`/`roles` 命名的是**创作的视觉元素**（一个主标题词、一个图表节点、一组数据可视化序列）——你是在设计它们，而不是选择捕捉资产。按每个 Scene **内联**说明布局和运动（词汇见 `visual-design.md` 和 `motion-language.md`）。添加一个全视频的 `## Video direction` 区块。

不要更改故事、脚本、`transition_in` 或源文本。此步骤不要编写 HTML。**没有资产暂存步骤**——无露脸视觉内容由步骤 5 的工作者构建。若用户提供了真实 `public/<basename>` 图像，则在相关帧的 `focal`/`roles` 中通过路径引用它；否则无需暂存任何内容。

**关卡：**每帧都有带时间码的镜头序列，其揭示节奏与旁白匹配（不前置堆叠）；每帧命名其创作的 `focal` 和/或 `roles`；`## Video direction` 存在。协作式：草图面板已确认。

---

## 步骤 5：构建帧

目标：将每个分镜帧构建为 HTML 合成，并组装可播放视频。

若已启动音频，等待步骤 3.1 音频完成。然后同步时长并获取 SFX；若静音则两者都跳过。

`node <SKILL_DIR>/scripts/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md`

`node <SKILL_DIR>/scripts/audio.mjs fetch-sfx --storyboard ./STORYBOARD.md --hyperframes .`

时长同步是机械性的：真实语音时长优先；静音帧保留估算值；绝不手动编辑同步后的时长。

分派前，阅读 `../hyperframes-core/references/subagent-dispatch.md`。构建逐帧数据包和工作者角色载荷：

`node <SKILL_DIR>/scripts/frame-packets.mjs --project "$PROJECT_DIR" --storyboard "$PROJECT_DIR/STORYBOARD.md"`

构建器会在 `.hyperframes/frame-packets/` 下为每帧写入一个有界数据包（该帧精确分镜块 + 蓝图正文 + 每个引用规则配方，均已内联），并写入 `_role.md`（`../hyperframes-core/references/frame-worker-core.md` + 此技能的 `sub-agents/frame-worker.md`，逐字拼接——完整的工作者角色）。为每帧分派一个子代理；可行时并行，否则分批运行工作者。每个工作者仅处理一帧：其提示包含 `_role.md` 和该帧数据包——完整粘贴两者，或提供两个文件路径让工作者先读取（两者等价；无论哪种方式，工作者都严格从这两个文档开始）——外加包含 `PROJECT_DIR`、`frame_id`、该帧是否在磁盘上有**已确认草图**（工作者装饰该布局，而非重绘它——frame-worker core § When a confirmed sketch exists）、画布尺寸、以及启用字幕时的字幕状态 + 禁入带的分派上下文。

工作者只读取其数据包和 `frame.md`；绝不打开 `STORYBOARD.md` 或技能文档（数据包已内联上游选择的内容）。每个工作者仅写入 `compositions/frames/NN-*.html`。工作者绝不得编辑 `STORYBOARD.md`。

**全出血背景必须位于 `class="clip"` 层，而绝不能位于 `#root`。** 一帧的底色（色块 / 渐变 / 网格）是独立的全时长背景 clip——在 `#root` / `data-composition-id` 元素上设置的 `background` 会被限制在帧窗口内，不能作为可靠底色，因此深色内容可能落在黑色宿主 `body` 上而渲染不可见。视频的基础底色由组装器根据 `frame.md` 的 `canvas` 颜色绘制到 index `#root` 上。（完整规则 + 自检：`../hyperframes-core/references/frame-worker-core.md`。）

随着每个工作者返回，编排者在 `STORYBOARD.md` 中将该帧标记为 `animated`。

音频时间信息存在后，在后台构建字幕并组装索引：

`node <SKILL_DIR>/scripts/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json &`

`node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .`

`captions.mjs` 使用项目的 `.hyperframes/caption-skin.html`（在步骤 2 复制）作为字幕外观，并从 `frame.md` 注入品牌 tokens；若没有皮肤，则渲染内置默认胶囊样式。`captions: skipped (<reason>)` 有效。明确跳过时，继续且不使用字幕。

**关卡：**每帧均标记为 `animated`（协作式：草图面板已在步骤 4 确认），`index.html` 存在，且字幕已构建或被明确跳过。

---

## 步骤 6：完成

目标：验证组装的视频，获得用户批准，并渲染最终 MP4。

注入转场，运行检查，暂停供审查，然后渲染。

`node <SKILL_DIR>/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .`

`node <SKILL_DIR>/scripts/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html`

`npx hyperframes lint`

`npx hyperframes check`

`npx hyperframes snapshot --at <frame-midpoints>`

`snapshot` 会将捕捉的帧拼接成一张联系表（`snapshots/contact-sheet.jpg`）。快速查看；若没有明显损坏则继续——不要在这里停留过久。

若命令失败，呈现 stderr 并停止——不要叠加恢复命令。亲自修复：对 `compositions/frames/NN-*.html` 做最廉价且安全的编辑，然后重新运行失败的检查。

**已知误报——不要追查。** `check` 可能会在**字幕**高亮词（选择器 `#caption-word-*` / `.caption-line`）上报告少量约约 1–4px 的 `text_box_overflow`。字幕胶囊使用刻意紧凑的 `line-height`（仅在 `scripts/captions.mjs` 中设置一次）且**没有 `overflow:hidden`**，因此粗重展示字体字形的墨迹会溢出数个 px 到胶囊自身的内边距——实际上没有内容被裁切。将其视为预期并继续。**不要**增大字幕 `line-height`（那会使胶囊膨胀，反而更糟）。仅当 `text_box_overflow` 指向**帧**元素（`#el-NN-*`）而非字幕词时才采取行动。

检查通过后，暂停供用户审查——审查循环的最终外观（`../hyperframes-core/references/review-loop.md` § 4）：在自步骤 3 起就一直打开的 Studio 中提出一个问题——现在渲染，还是需要哪些修改？（自主式：保留的唯一问题，先预览还是渲染。）然后交付 MP4、联系表和帧 id，以便修订可针对单帧进行。

预览：`npx hyperframes preview`

仅在用户批准后渲染（自主模式：在先预览还是渲染的问题之后）：

`npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4`

渲染后不要重新运行 `lint`、`check` 或 `snapshot`，除非用户要求。

**关卡：**渲染前 `lint` 和 `check` 已通过且快照已检查；用户在审查暂停时已批准（自主式：检查已通过且交付物包含联系表）；`renders/video.mp4` 存在。最终回复说明 MP4 路径和最终时长。

---

## 快速参考

**格式：**横向 `1920x1080`；竖向 `1080x1920`；方形 `1080x1080` ——由目标平台推导（brief contract § 2）。在分镜 frontmatter 中仅设置一次格式。

**相较于捕捉资产工作流的无露脸差异：**没有步骤 1 捕捉（合成的 `tokens.json` + `visible-text.txt`）；没有 `asset-descriptions.md`，也没有 `capture/assets/`；步骤 4 没有资产暂存；`asset_candidates` 默认为空；每个视觉内容均由步骤 5 工作者创作（排版 / 抽象图形 / 图表 / 数据可视化）。用户提供的 `public/<basename>` 图像是唯一真实资产路径。

**后台脚本：**此工作流仅在 `scripts/` 下提供以下内容：用于将帧预设采用 + 品牌重混至 `frame.md`（+ 字幕皮肤）的 `build-frame`；用于 TTS、转录、BGM、SFX 和时长同步的 `audio`；`captions`；用于注入和验证的 `transitions`；以及 `assemble-index`。其他所有内容均使用 `hyperframes` CLI。

可复用、与领域无关的镜头形状位于 `../hyperframes-animation/blueprints/`（由 `../hyperframes-animation/blueprints-index.md` 编制索引）。

| 阅读                                                                                                                                                        | 时机                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `[../hyperframes-core/references/brief-contract.md](../hyperframes-core/references/brief-contract.md)`                                                      | 关卡类型、从 `BRIEF.md` 推导模式、字段语义。                  |
| `[../hyperframes-creative/references/story-spine.md](../hyperframes-creative/references/story-spine.md)`                                                    | 步骤 3：故事准则——钩子语言、价值先于证据、提案形态。 |
| `[../hyperframes-creative/frame-presets/](../hyperframes-creative/frame-presets/)`                                                                          | 步骤 2：选择并采用帧预设。                                       |
| `[../hyperframes-creative/references/design-spec.md](../hyperframes-creative/references/design-spec.md)`                                                    | 步骤 2：正确应用品牌 tokens。                                          |
| `[references/story-design.md](references/story-design.md)`                                                                                                  | 步骤 3：规划讲解视频故事。                                              |
| `[../hyperframes-animation/blueprints-index.md](../hyperframes-animation/blueprints-index.md)`                                                              | 步骤 3：角色→蓝图菜单。步骤 4：选择镜头形状。                      |
| `[../hyperframes-core/references/storyboard-format.md](../hyperframes-core/references/storyboard-format.md)`                                                | 步骤 3：编写 `STORYBOARD.md`。                                                 |
| `[../hyperframes-core/references/script-format.md](../hyperframes-core/references/script-format.md)`                                                        | 步骤 3：编写 `SCRIPT.md`。                                                     |
| `[../media-use/audio/references/tts.md](../media-use/audio/references/tts.md)`                                                                              | 步骤 3.1：选择或了解 TTS 提供方和声音。                       |
| `[references/visual-design.md](references/visual-design.md)`                                                                                                | 步骤 4：编写帧的镜头序列（+ Layout 词汇）。                 |
| `[references/motion-language.md](references/motion-language.md)`                                                                                            | 步骤 4：运动词汇 + 运动准则。                           |
| `[references/cut-catalog.md](references/cut-catalog.md)`                                                                                                    | 步骤 4-5：剪辑目录（工作者构建帧内接缝）。                  |
| `[../hyperframes-animation/rules-index.md](../hyperframes-animation/rules-index.md)` + `[../hyperframes-animation/rules/](../hyperframes-animation/rules/)` | 步骤 5：引用运动的本地规则配方正文。                        |
| `[../hyperframes-core/references/frame-worker-core.md](../hyperframes-core/references/frame-worker-core.md)`                                                | 步骤 5：共享工作者契约（数据包构建器将其前置到增量内容）。  |
| `[sub-agents/frame-worker.md](sub-agents/frame-worker.md)`                                                                                                  | 步骤 5：该工作流的帧工作者增量。                                     |
| `[../hyperframes-core/references/subagent-dispatch.md](../hyperframes-core/references/subagent-dispatch.md)`                                                | 步骤 5：安全分派子代理。                                            |
