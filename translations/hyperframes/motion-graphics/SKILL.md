<!-- source-sha256: 582c0c29178742b8d921790e357576a39a9740c27d042edf00bdb16816b523b2 -->
---
name: motion-graphics
description: >
  一种简短、设计驱动的动态图形，其中运动本身就是信息——动态
  排版、统计数字递增、图表/数据可视化冲击、Logo 片头 / 品牌组合、
  下三分之一栏 / 标注 / 社交覆盖层、动画地图（高亮区域、
  连接地点、缩放至某个地点）、动画推文 / 新闻文章 /
  标题、网页 / UI 动画（滚动、光标、标注），或将一张
  真实图片的几何结构融入图表。通常不足 10 秒（最长约 30 秒），无
  旁白或真人主体；渲染为 MP4 或透明覆盖层。
  更长 / 有旁白 / 多场景 → /general-video。不明确 → /hyperframes。
---

> **首先，保持此技能为最新版本——静默运行，无需询问：** `npx hyperframes skills update motion-graphics`。当所有内容均为最新时会快速无操作；否则会在你依赖它们之前，刷新此技能及其依赖的核心领域技能。

> **figma 源文件**：如果要基于其构建的 logo/资产/动画来自 figma.com URL，请先运行 `/figma`——若该图形是 Figma Motion 导入，则进行资产导出、品牌令牌处理以及 Motion→GSAP 转换——然后根据其输出构建。不要直接通过原始 MCP 工具操作 Figma：这会跳过 SVG 清理、`.media/manifest.jsonl` 来源记录和品牌令牌 `var()` 绑定，因此后续品牌变更将无法传播，除非完整重新导入。

# motion-graphics — 分发入口

> **入口是 `/hyperframes`。** 此技能制作一个**简短、设计驱动、无旁白的动态图形**（运动即信息；约 10 秒以内，无配音）。任何更长、有旁白或多场景的内容——或任何不确定情况 → 先阅读 `/hyperframes`：意图层负责所有路由决策。

此工作流**设计为自主执行**——最多一个澄清问题（`agents/director.md`），然后无需中间审核，直接构建并验证。意图层（`/hyperframes` → `references/intent-interview.md`）会直接路由至此，无需询问运行形态；对于如此短的作品，故事板和辅助会话价值不大。渲染仍需用户把关：检查和证明快照通过后，询问 `../hyperframes-core/references/brief-contract.md` 中规范的“先预览，还是渲染？”问题。当存在 `BRIEF.md` 时，先阅读它，再询问导演的问题。

一个简短、设计驱动的动态图形。**资产优先**：先决定资产策略并获取真实素材，然后围绕已有素材设计镜头，最后通过复用目录能力进行组合。所有产物均放入 `PROJECT_DIR = videos/<project-name>/`（在步骤 0 创建）；以下所有路径均相对此目录。

| 阶段 | 执行 | 主要产物 | 详细流程 |
| -------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------- |
| 初始化 | Bash | `hyperframes.json` | 步骤 0 |
| 规划 | 子代理 — **决定是否搜索？** + 分类 + 资产策略 | `shot-plan.json`（草稿：类别、`asset_needs` 查询、简述） | `agents/director.md`（第 1 部分） |
| 获取 ◇ | Bash — media-use 解析（若 `asset_needs` 为空则**跳过**） | `assets/` + `assets/index.md` | `phases/source/guide.md` |
| 设计 | 子代理 — 围绕已解析资产设计镜头 | `shot-plan.json`（最终版：区块 + 布局 + 运动 + 位置） | `agents/director.md`（第 2 部分） |
| 构建 | 子代理 — 优先复用的组合 | `compositions/index.html` | `agents/builder.md` |
| 验证 | Bash — `lint`、`check`、证明快照；失败时修复 | `snapshots/contact-sheet.jpg` | 步骤 5 |
| 批准 | 询问预览或渲染；等待回答 | 明确的渲染批准 | 步骤 6 |
| 渲染 | Bash — `hyperframes render`（MP4，或覆盖层使用 `--format webm/mov`） | `renders/video.mp4` 或透明覆盖层 | 步骤 6 |

仅当所选类别声明了资产时才运行 `◇ 获取`。纯代码/文本类别（例如 `kinetic-type`、大多数 `charts`/`stat`）具有 `asset_needs: []`，会直接从规划跳至设计。

## 类别 — 按搜索决策划分

`plan` 的**首个决策是：这是否需要搜索？** 该分支将类别拆为两组；随后选择具体类别——对于搜索驱动类别，**按搜索返回的内容类型**选择。每个类别对应一个 `categories/<id>/module.md`（其中包含规划和构建规则）；共享的运动词汇位于 `references/motion-vocabulary.md`（→ `hyperframes-animation` 规则/蓝图 + 注册表区块）。

**形式类别 — 不搜索；用户提供内容：**

| 类别 | 意图 | 主要依赖 |
| -------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `kinetic-type` | 有冲击力的短句 / 引语 / 标题，文字运动优先 | `caption-*` 区块 + 动画规则 |
| `stat` | 单个主视觉数字 / 递增计数 + 圆环 | `apple-money-count` / `rules/{counting-dynamic-scale, stat-bars-and-fills}` |
| `charts` | 基于数据的柱状 / 折线 / 饼图 / 竞速 / 百分比 | `data-chart` 区块 |
| `logo-reveal` | Logo 片头 / 品牌组合（用户 Logo） | `logo-outro` / `rules/svg-path-draw` |
| `lower-thirds` | 姓名 / 职位栏、标注、社交覆盖层 | `caption-*` + 注册表覆盖层区块 |
| `maps` | 地理运动——高亮区域、连接地点、缩放至某个地点（矢量路径，或烘焙底图路径） | `us-map` / `world-map` 系列 + `bake-basemap.mjs` |

**搜索驱动类别 — 先搜索，再按内容类型制作动画**（RWA 路径）：

| 返回内容 | 类别 | 动画 |
| ---------------- | -------------- | -------------------------------------------------------------- |
| 网页 / 链接 | `webpage` | 网页 / UI 动画（滚动、揭示、光标、标注） |
| 新闻文章 | `news` | 标题揭示 + 来源卡片 + 关键事实标注 |
| 推文 | `tweet` | 动画推文卡片 |
| 图片 / 实体 | `asset-fusion` | 资产的几何结构_成为_图表（RWA 叙事内融合） |

构建顺序：一次一个，覆盖优先（粗糙也可以）。`kinetic-type` 已从原型移植；其余后续跟进。

## 前置条件

macOS Apple Silicon 或 Linux x64。系统工具：`brew install node ffmpeg`。运行一次 `npx hyperframes doctor`。macOS GPU 渲染：`export PRODUCER_BROWSER_GPU_MODE=hardware`。

可选密钥（未设置时使用本地回退）——仅被通过 media-use 获取/生成资产的类别需要：

| 密钥 | 用途 | 回退 |
| ----------------------------------- | ----------------------------------------------------------- | ------------------------------- |
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | 图片生成（media-use resolve） | 跳过生成 / 仅搜索 |
| (asset_scout / 搜索提供商) | `webpage`/`news`/`tweet` + `asset-fusion` 真实资产搜索 | 类别降级为无资产 |

## 流程

### 步骤 0 — 初始化

cwd 是代理工作区根目录；将所有产物写入 `PROJECT_DIR = videos/<project-name>/`。`<project-name>`：使用用户提供的目录，否则根据意图生成简短的 kebab-case 名称（`<subject>-motion`）。不要使用工作区基础名称或时间戳。

仅当 `$PROJECT_DIR/hyperframes.json` 不存在时：

```bash
PROJECT_DIR="${MOTION_GRAPHICS_DIR:-videos/<project-name>}"
mkdir -p "$(dirname "$PROJECT_DIR")"
npx hyperframes init "$PROJECT_DIR" --non-interactive --example=blank --skill=motion-graphics
```

`init` 会根据 GitHub 上的最新版本检查已安装技能，并在任一技能过期时更新全局集合。

**约束：**绝不在工作区根目录执行 `hyperframes init`；绝不于 `PROJECT_DIR` 内嵌套另一个 `hyperframes/`；每条 Bash 命令（主代理 + 子代理）都必须是 `(cd "$PROJECT_DIR" && ...)` 子 shell——绝不使用裸 `cd`。

### 步骤 1 — 规划（子代理：Director 第 1 部分）

分发一个子代理。prompt = 完整 `agents/director.md` + `## Dispatch context`（`SKILL_DIR` / `PROJECT_DIR` / 用户请求 / `Schema: <SKILL_DIR>/references/shot-plan-ir.md`）。它必须：

1. **决定：这是否需要搜索？**（第一个分支）
   - **否** → 选择一个**形式类别**（kinetic-type / stat / charts / logo-reveal / lower-thirds）；内容由用户提供；`asset_needs: []`。
   - **是** → 将**搜索计划**写入 `asset_needs[]`（新闻 / 网页 / 推文 / 图片；双极查询）。具体的**搜索驱动类别**（webpage / news / tweet / asset-fusion）由步骤 2 返回的内容类型确认，并在步骤 3 最终确定。
2. 编写草稿 `shot-plan.json`（封装 + 所选形式类别_或_搜索意图 + `asset_needs` + 一段镜头简述）。Schema：`references/shot-plan-ir.md`。

验证：`[ -s "$PROJECT_DIR/shot-plan.json" ] && echo ok || echo missing`。

### 步骤 2 — 获取 ◇（Bash：media-use，条件执行）

如果 `shot-plan.json.asset_needs` 非空，解析资产（搜索 / 生成 / 获取 → 冻结的项目本地路径 + 台账）。参见 `phases/source/guide.md`（封装 `media-use resolve`；搜索驱动类别使用新闻/网页/推文/图片搜索）。如果 `asset_needs` 为空，**跳至步骤 3**。

```bash
# 示例 — 参见 phases/source/guide.md
(cd "$PROJECT_DIR" && node <SKILL_DIR>/phases/source/resolve.mjs --plan ./shot-plan.json --out ./assets)
```

优雅降级：如果搜索/提供商不可用，类别回退为无资产（在 `context.log` 中记录）。

### 步骤 3 — 设计（子代理：Director 第 2 部分）

分发一个子代理（prompt = `agents/director.md` 第 2 部分 + 分发上下文，其中若运行了步骤 2 则包括已解析的 `assets/index.md` + `catalog-map.md`）。它围绕**可用资产**设计镜头：选择目录区块 + `hyperframes-animation` 规则/蓝图、布局、运动、节拍，以及（对于 `asset-fusion`）`element_positions` + 吸管调色板。最终确定 `shot-plan.json`（`content.block` + `content.customize` + 各类别内容）。

### 步骤 4 — 构建（子代理：Builder，优先复用）

分发一个子代理。prompt = 完整 `agents/builder.md` + 分发上下文（`shot-plan.json`、`catalog-map.md`、类别的 `module.md`、`references/motion-vocabulary.md`、`references/builder-contract.md`）。**优先复用**：`npx hyperframes add <block>` + 原地定制；仅手写缺口内容 + asset-fusion 交互提示。输出符合 HF 合约的 `compositions/index.html`（暂停的 GSAP 时间线位于 `window.__timelines`，`class="clip"` + 稳定 id，`tl.seek(0)`，确定性）。

### 步骤 5 — 验证（Bash → 失败时修复子代理）

```bash
(cd "$PROJECT_DIR" && npx hyperframes lint .)
(cd "$PROJECT_DIR" && npx hyperframes check .)
(cd "$PROJECT_DIR" && npx hyperframes snapshot --at <proof-times>)
```

选择能够展示开场状态、标志性动作和最终停留的证明时间点。继续前检查生成的联系表或快照表。`lint`、`check` 或快照失败时，分发修复子代理（`agents/finalize.md`）进行一次原地修复，然后重新运行失败的关卡。绝不可仅为掩盖缺陷而修改固定时长。

### 步骤 6 — 批准与渲染（Bash）

询问一个问题：“先预览，还是渲染？”如果用户选择预览，打开 Studio，并在修订后返回同一批准关卡：

```bash
(cd "$PROJECT_DIR" && npx hyperframes preview)
```

仅在得到明确的渲染回答后渲染：

```bash
(cd "$PROJECT_DIR" && npx hyperframes render . --skill=motion-graphics -q high -o ./renders/video.mp4)
# 透明覆盖层变体：--format webm  （或 mov）
```

验证输出存在、非空且具有预期时长。最终交付需注明产物、实际时长、composition 或 frame id、证明时间点，以及已检查的联系表或快照表。标志位于 `/hyperframes-cli` → `references/preview-render.md`。

## 恢复表

| 状态 | 从此处继续 |
| -------------------------------------------------------- | -------------------------- |
| 无 `shot-plan.json` | 步骤 1（规划） |
| `shot-plan.json` 包含 `asset_needs`，无 `assets/` | 步骤 2（获取） |
| `shot-plan.json` 已最终确定，无 `compositions/index.html` | 步骤 3/4（设计+构建） |
| `compositions/index.html` 存在，缺少证明快照 | 步骤 5（验证） |
| 检查和证明快照通过，尚无已批准渲染 | 步骤 6（批准） |
| 已批准的渲染存在 | 验证输出，然后报告 |

## 设计说明（维护者 — 执行时不读取此内容）

- **资产优先原理：**资产获取前置，并为镜头设计提供依据（RWA 流程：分析 → 搜索 → 审阅 → 组合）。搜索驱动类别（`webpage`/`news`/`tweet`）和 `asset-fusion` 都依赖 media-use 搜索（新闻/网页/推文/图片），这是 media-use 已记录的 RWA 沿袭。
- **优先复用：**生态系统内与 LLM 生成模板对应的方式是“组合目录区块 + `hyperframes-animation` 规则”。HF 的暂停 GSAP 时间线 ≙ Remotion 的 `useCurrentFrame`。
- **类别模块合约：**一个 `categories/<id>/module.md`（规划 + 构建），共享 `references/motion-vocabulary.md`（+ 可选 eval）。添加类别 = 放入文件夹 + 在 `agents/director.md` 注册其分类器行 + 在 `catalog-map.md` 添加其行；阶段管道不变。
- **目录结构：**
  ```
  videos/<project-name>/
    hyperframes.json  context.log
    shot-plan.json            # IR（Director 输出）
    assets/  assets/index.md  # media-use 输出（如已获取）
    compositions/index.html   # Builder 输出
    renders/video.mp4
  ```
- **注册：**在 `hyperframes` 路由器中——添加“设计驱动的简短动态图形”意图 + Workflow 描述；从 `/general-video` 划分出 motion-graphics 触发器；添加反向 Do-NOT-use 边。参见 `motion-graphics-genre.md` §5-7。
