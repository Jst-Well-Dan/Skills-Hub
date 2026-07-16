<!-- source-sha256: de09b723bdc7b19d74e508d0b63e2306f03b4e48ab2b83c90ac6c99c0b7de4d0 -->
---
name: baoyu-image-gen
description: 使用 OpenAI GPT Image 2、Azure OpenAI、Google、OpenRouter、DashScope、Z.AI GLM-Image、MiniMax、Jimeng、Seedream、Replicate 和 Agnes API 进行 AI 图像生成。支持文生图、参考图、宽高比以及从已保存的提示词文件批量生成。默认按顺序生成；当用户已有多个提示词或需要稳定的多图吞吐量时，使用批量并行生成。当用户要求生成、创建或绘制图像时使用。
version: 2.1.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-image-gen
    requires:
      anyBins:
        - bun
        - npx
---

# 图像生成（AI SDK）

基于官方 API 生成图像。支持 OpenAI GPT Image 2、Azure OpenAI、Google、OpenRouter、DashScope（阿里通义万象）、Z.AI GLM-Image、MiniMax、Jimeng（即梦）、Seedream（豆包）、Replicate 和 Agnes。

## 用户输入工具

当此技能向用户提问时，请遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具**，即当前智能体运行时暴露的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果不存在此类工具，则输出带编号的纯文本消息，并要求用户针对每个问题回复所选编号或答案。
3. **批量提问**：如果工具支持每次调用提出多个问题，请将所有适用问题合并到一次调用中；如果只支持单个问题，则按优先级逐一提问。

下文中具体的 `AskUserQuestion` 引用仅为示例——在其他运行时中请替换为本地等效工具。

## 脚本目录

`{baseDir}` = 此 SKILL.md 所在的目录。下文所有 `scripts/...` 路径均相对于 `{baseDir}`。主脚本：`{baseDir}/scripts/main.ts`。批处理负载辅助脚本：`{baseDir}/scripts/build-batch.ts`。解析 `${BUN_X}`：优先使用 `bun`；否则使用 `npx -y bun`；再否则建议运行 `brew install oven-sh/bun/bun`。

## 步骤 0：加载偏好设置 ⛔ 阻塞

必须先完成此步骤才能生成任何图像——在 EXTEND.md 存在之前禁止生成。

按顺序检查以下路径；使用第一个找到的文件：

| 路径 | 作用域 |
|------|-------|
| `.baoyu-skills/baoyu-image-gen/EXTEND.md` | 项目 |
| `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-image-gen/EXTEND.md` | XDG |
| `$HOME/.baoyu-skills/baoyu-image-gen/EXTEND.md` | 用户主目录 |

- **已找到** → 加载、解析并应用。如果 `default_model.[provider]` 为 null → 仅询问模型。
- **未找到** → 使用 AskUserQuestion 运行首次设置（`references/config/first-time-setup.md`），收集提供商、模型、质量和保存位置。保存 EXTEND.md，然后继续。在此步骤完成前不要生成图像。

旧版兼容性：如果 `.baoyu-skills/baoyu-imagine/EXTEND.md` 存在而新路径不存在，运行时会将其重命名为 `baoyu-image-gen`。如果两者都存在，运行时不会修改它们，并使用新路径。

**EXTEND.md 键**：默认提供商、默认质量、默认宽高比、默认图像尺寸、OpenAI 图像 API 方言、默认模型、批处理工作进程上限、提供商专属批处理限制。模式：`references/config/preferences-schema.md`。

## 用法

最小可用示例——完整示例集（包括各提供商调用方式和批处理模式）请参阅 `references/usage-examples.md`。

### 保持身份一致的参考图提示词

当用户希望根据参考图保留真实人物、角色或物体的身份时，**不要**用冗长的通用描述替代参考图。应优先使用简短、明确的身份保持措辞：

- “将参考图中的人物或物体作为同一身份使用。不要重新设计，也不要创建一个外观相似的新主体。”
- “仅更改场景、服装、姿势、光照、渲染风格和构图。保留参考图中的面部、比例、发型、关键配饰和整体身份。”
- 如果使用多张参考图，请说明它们是同一主体，并应共同定义其身份。

常见问题：诸如“年轻东亚女性，椭圆脸，眼神清澈……”之类的冗长描述，可能导致模型合成一个符合描述的新人物，而不是保留参考人物。

```bash
# 基础用法
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cat" --image cat.png

# 指定宽高比和高质量
${BUN_X} {baseDir}/scripts/main.ts --prompt "A landscape" --image out.png --ar 16:9 --quality 2k

# 从文件读取提示词
${BUN_X} {baseDir}/scripts/main.ts --promptfiles system.md content.md --image out.png

# 使用参考图
${BUN_X} {baseDir}/scripts/main.ts --prompt "Make blue" --image out.png --ref source.png

# 指定提供商
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cat" --image out.png --provider dashscope --model qwen-image-2.0-pro

# OpenAI GPT Image 2
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cat" --image out.png --provider openai --model gpt-image-2

# Codex CLI（使用已登录的 Codex 订阅——无需 OPENAI_API_KEY；要求 `codex` 位于 PATH 中）
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cat" --image out.png --provider codex-cli --ar 16:9

# 批处理模式
${BUN_X} {baseDir}/scripts/main.ts --batchfile batch.json --jobs 4

# 从 outline.md + prompts/ 构建批处理文件（例如 baoyu-article-illustrator 的输出）
${BUN_X} {baseDir}/scripts/build-batch.ts --outline outline.md --prompts prompts --output batch.json --images-dir attachments
${BUN_X} {baseDir}/scripts/main.ts --batchfile batch.json --jobs 4
```

## 参考图身份保持

当用户希望根据参考图保留人物或物体时：

- 应优先使用一小组精心挑选的现有源参考图（通常为 2–4 张），而不是大量图像；体积较大的多张参考图可能使流式提供商变得不稳定。
- 在提示词中说明这些参考图展示的是同一主体，并且输出必须使用该身份。避免使用冗长、通用的面部特征描述，因为这可能导致模型合成一个外观相似的新人物。
- 除非用户明确要求，否则不要将新生成的输出用作参考图；生成的参考图会累积身份漂移。
- 如果结果变得过于精致或像网红照片，请减少风格化参考图，并添加明确的反美化约束（不要瘦脸、放大眼睛、浓妆、商业旅行摄影或过度磨皮）。
- 如果主体应显得更年轻或更年长，请保留面部身份，通过服装、姿态、场景和造型表现年龄；不要要求模型改变面部身份。

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--prompt <text>`, `-p` | 提示词文本 |
| `--promptfiles <files...>` | 从文件读取提示词（拼接） |
| `--image <path>` | 输出图像路径（单图模式下必填） |
| `--batchfile <path>` | 用于多图生成的 JSON 批处理文件 |
| `--jobs <count>` | 批处理模式的工作进程数（默认：自动；最大值来自配置；内置默认值为 10） |
| `--provider google\|openai\|azure\|openrouter\|dashscope\|zai\|minimax\|jimeng\|seedream\|replicate\|codex-cli\|agnes` | 强制指定提供商（默认：自动检测；永远不会自动选择 `codex-cli`——必须通过 CLI 或 EXTEND.md 固定指定） |
| `--model <id>`, `-m` | 模型 ID——默认值和允许值请参阅提供商参考文档 |
| `--ar <ratio>` | 宽高比（`16:9`、`1:1`、`4:3`……） |
| `--size <WxH>` | 明确指定尺寸（例如 `1024x1024`；对于 `gpt-image-2`，宽度和高度必须是 16 的倍数，最长边不超过 3840px，宽高比不得超过 3:1） |
| `--quality normal\|2k` | 质量预设（默认：`2k`） |
| `--imageSize 1K\|2K\|4K` | Google/OpenRouter 的图像尺寸（默认：根据质量确定） |
| `--imageApiDialect openai-native\|ratio-metadata` | OpenAI 兼容端点方言——对于要求使用宽高比 `size` 加 `metadata.resolution` 的网关，请使用 `ratio-metadata` |
| `--ref <files...>` | 参考图。支持 Google 多模态、OpenAI GPT Image 编辑、Azure OpenAI 编辑（仅限 PNG/JPG）、OpenRouter 多模态模型、Replicate 支持的模型系列、MiniMax 主体参考、Seedream 5.0/4.5/4.0、DashScope `wan2.7-image-pro`/`wan2.7-image`。Jimeng、Seedream 3.0、SeedEdit 3.0 以及 `wan2.7-image*` 系列之外的所有 DashScope 模型均不支持 |
| `--n <count>` | 图像数量。Replicate 要求 `--n 1`（单输出保存语义） |
| `--json` | JSON 输出 |

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API 密钥 |
| `OPENROUTER_API_KEY` | OpenRouter API 密钥 |
| `GOOGLE_API_KEY` | Google API 密钥 |
| `DASHSCOPE_API_KEY` | DashScope API 密钥 |
| `ZAI_API_KEY`（别名 `BIGMODEL_API_KEY`） | Z.AI API 密钥 |
| `MINIMAX_API_KEY` | MiniMax API 密钥 |
| `REPLICATE_API_TOKEN` | Replicate API 令牌 |
| `JIMENG_ACCESS_KEY_ID`, `JIMENG_SECRET_ACCESS_KEY` | Jimeng（即梦）火山引擎凭据 |
| `ARK_API_KEY` | Seedream（豆包）火山引擎 ARK API 密钥 |
| `<PROVIDER>_IMAGE_MODEL` | 各提供商的模型覆盖值（`OPENAI_IMAGE_MODEL`、`GOOGLE_IMAGE_MODEL`、`DASHSCOPE_IMAGE_MODEL`、`ZAI_IMAGE_MODEL`/`BIGMODEL_IMAGE_MODEL`、`MINIMAX_IMAGE_MODEL`、`OPENROUTER_IMAGE_MODEL`、`REPLICATE_IMAGE_MODEL`、`JIMENG_IMAGE_MODEL`、`SEEDREAM_IMAGE_MODEL`、`AGNES_IMAGE_MODEL`） |
| `AZURE_OPENAI_DEPLOYMENT`（别名 `AZURE_OPENAI_IMAGE_MODEL`） | Azure 默认部署 |
| `<PROVIDER>_BASE_URL` | 各提供商的端点覆盖值 |
| `AZURE_API_VERSION` | Azure 图像 API 版本（默认 `2025-04-01-preview`） |
| `JIMENG_REGION` | Jimeng 区域（默认 `cn-north-1`） |
| `OPENAI_IMAGE_API_DIALECT` | `openai-native` \| `ratio-metadata` |
| `OPENROUTER_HTTP_REFERER`, `OPENROUTER_TITLE` | 可选的 OpenRouter 归属信息 |
| `BAOYU_IMAGE_GEN_MAX_WORKERS` | 覆盖批处理工作进程上限 |
| `BAOYU_IMAGE_GEN_<PROVIDER>_CONCURRENCY` | 各提供商的并发数（例如 `BAOYU_IMAGE_GEN_REPLICATE_CONCURRENCY`；对于 codex-cli，使用 `BAOYU_IMAGE_GEN_CODEX_CLI_CONCURRENCY`） |
| `BAOYU_IMAGE_GEN_<PROVIDER>_START_INTERVAL_MS` | 各提供商的启动间隔 |
| `BAOYU_CODEX_IMAGEGEN_BIN` | 覆盖 `codex-cli` 提供商使用的 codex-imagegen 包装器路径（默认：内置的 `scripts/codex-imagegen/main.ts`；接受 `.ts` 或旧版 `.sh`/二进制文件） |
| `BAOYU_CODEX_IMAGEGEN_CACHE_DIR` | 为 `codex-cli` 提供商启用幂等缓存（默认关闭） |
| `BAOYU_CODEX_IMAGEGEN_TIMEOUT_MS` | `codex-cli` 提供商每次尝试执行 `codex exec` 的超时时间（默认：300000 ms） |
| `BAOYU_CODEX_IMAGEGEN_RETRIES` | `codex-cli` 提供商的包装器在可重试错误上的重试次数（默认：2） |
| `BAOYU_CODEX_IMAGEGEN_LOG_FILE` | 为 `codex-cli` 提供商追加 JSONL 诊断日志 |

**加载优先级**：CLI 参数 > EXTEND.md > 环境变量 > `<cwd>/.baoyu-skills/.env` > `~/.baoyu-skills/.env`

### Codex/ChatGPT OAuth 不是 OpenAI API 密钥

`--provider openai --model gpt-image-2` 使用标准 OpenAI Images API（`/v1/images/generations` 或 `/v1/images/edits`），并且需要 `OPENAI_API_KEY`。Codex 或 ChatGPT 桌面端登录属于不同的使用授权，不能直接替代 `OPENAI_API_KEY`；不要将 Codex OAuth 令牌粘贴到 `OPENAI_API_KEY` 中，也不要只将 `OPENAI_BASE_URL` 设置为 Codex 后端。

如果用户希望在没有 OpenAI API 密钥的情况下使用其 Codex 订阅或 GPT Image 2 权益，请通过 Codex 原生后端处理，而不是使用此技能的 `openai` 提供商：

- 在 Codex 运行时中：使用原生 `imagegen` 技能或工具。
- 在已安装并登录 `codex` CLI 的非 Codex 运行时中：使用 `baoyu-image-gen --provider codex-cli`（首选——它提供与其他所有提供商相同的重试、缓存和批处理流程）。该提供商会启动内置的 `scripts/codex-imagegen/main.ts`；同一份代码位于上游的 `packages/baoyu-codex-imagegen/src/main.ts`，供独立调用方使用。
- 在具有原生 `image_generate` 工具的 Hermes 运行时中：将该工具用作回退方案，并说明参考图是被直接传入，还是根据提取出的视觉特征重建。

不要修改现有的 `openai` 提供商，让其静默使用 Codex OAuth。专用的 `codex-cli` 提供商是一级支持的 Codex CLI 路径，拥有自己的身份验证方式（Codex 登录）、路由（`codex exec`）、请求结构和测试。请参阅 `references/codex-oauth-vs-openai-api-key.md`。

## 模型解析

以下优先级（从高到低）适用于每个提供商：

1. CLI 标志 `--model <id>`
2. EXTEND.md `default_model.[provider]`
3. 环境变量 `<PROVIDER>_IMAGE_MODEL`
4. 内置默认值

对于 OpenAI，内置默认值为 `gpt-image-2`。仍可通过 `--model` 或 `OPENAI_IMAGE_MODEL` 选择 `gpt-image-1.5`、`gpt-image-1` 和 GPT Image 快照版本。

对于 Azure，`--model` / `default_model.azure` 是 Azure 部署名称。`AZURE_OPENAI_DEPLOYMENT` 是首选环境变量；`AZURE_OPENAI_IMAGE_MODEL` 保留为向后兼容的别名。如果 Azure 部署名称与底层模型同名，请使用 `gpt-image-2`；否则请使用准确的自定义部署名称。

EXTEND.md 会覆盖环境变量：如果 EXTEND.md 设置了 `default_model.google: "gemini-3-pro-image"`，而环境变量设置了 `GOOGLE_IMAGE_MODEL=gemini-3.1-flash-image`，则以 EXTEND.md 为准。

**每次生成前显示模型信息**：

- `正在使用 [provider] / [model]`
- `切换模型：--model <id> | EXTEND.md default_model.[provider] | 环境变量 <PROVIDER>_IMAGE_MODEL`

## OpenAI 兼容网关方言

`provider=openai` 表示身份验证和路由入口点与 OpenAI 兼容。它**不**保证上游图像 API 使用 OpenAI 原生语义。当网关需要不同的传输格式时，请在 EXTEND.md 中设置 `default_image_api_dialect`，或设置 `OPENAI_IMAGE_API_DIALECT`，或使用 `--imageApiDialect`：

- `openai-native`：像素尺寸 `size`（`1536x1024`）和 OpenAI 原生质量字段
- `ratio-metadata`：宽高比 `size`（`16:9`）加 `metadata.resolution`（`1K|2K|4K`）和 `metadata.orientation`

对于 OpenAI 原生 API 或严格的兼容实现，请使用 `openai-native`；对于 Gemini 或类似模型前端的兼容网关，可以尝试 `ratio-metadata`。当前限制：`ratio-metadata` 仅适用于文生图；参考图编辑仍需使用 `openai-native` 或具备一级编辑支持的提供商。

## 提供商专属指南

每个提供商都有自身特性（模型系列、尺寸规则、参考图支持和限制）。当用户选择相应提供商或要求非默认行为时，请阅读对应指南：

| 提供商 | 参考文档 |
|----------|-----------|
| DashScope（Qwen-Image 系列、自定义尺寸） | `references/providers/dashscope.md` |
| Z.AI（GLM-Image、cogview-4） | `references/providers/zai.md` |
| MiniMax（image-01、主体参考） | `references/providers/minimax.md` |
| OpenRouter（多模态模型、`/chat/completions` 流程） | `references/providers/openrouter.md` |
| Replicate（nano-banana、Seedream、Wan） | `references/providers/replicate.md` |
| Codex CLI（包装内置的 `scripts/codex-imagegen/`；使用 Codex 登录，无需 `OPENAI_API_KEY`） | `references/providers/codex-cli.md` |
| Agnes（agnes-image-2.1-flash、参考图支持） | `references/providers/agnes.md` |

## 提供商选择

1. 提供了 `--ref` 且未提供 `--provider` → 自动选择 Google → OpenAI → Azure → OpenRouter → Replicate → Seedream → MiniMax → Agnes（MiniMax 的主体参考更专注于角色或肖像一致性）
2. 指定了 `--provider` → 使用该提供商（如果使用 `--ref`，则必须为 google/openai/azure/openrouter/replicate/seedream/minimax/codex-cli/agnes）
3. 仅存在一个 API 密钥 → 使用对应提供商
4. 存在多个密钥 → 默认优先级：Google → OpenAI → Azure → OpenRouter → DashScope → Z.AI → MiniMax → Replicate → Jimeng → Seedream → Agnes
5. **永远不会自动选择** `codex-cli`——请在 EXTEND.md 中设置 `default_provider: codex-cli`，或传入 `--provider codex-cli`。它会通过内置的 `scripts/codex-imagegen/main.ts` TS 入口点（使用 `bun` 运行）启动 `codex exec`，并使用用户的 Codex 订阅（无需 `OPENAI_API_KEY`）。要求 `codex` 位于 `PATH` 中，并且已有有效的 `codex login` 登录状态。

## 质量预设

| 预设 | Google imageSize | OpenAI 尺寸 | OpenRouter 尺寸 | Replicate 分辨率 | 使用场景 |
|--------|------------------|-------------|-----------------|----------------------|----------|
| `normal` | 1K | 目标 1024px | 1K | 1K | 快速预览 |
| `2k`（默认） | 2K | 目标 2048px | 2K | 2K | 封面、插图、信息图 |

可以使用 `--imageSize 1K|2K|4K` 覆盖 Google/OpenRouter 的 `imageSize`。

对于 OpenAI 原生 `gpt-image-2`，`normal` 映射为 `quality=medium`，并使用接近所请求宽高比的低延迟有效尺寸；`2k` 映射为 `quality=high`，并使用 `2048x2048`、`2048x1152` 或 `1152x2048` 等 2048px 级别尺寸。对于有效的自定义或 4K 输出，请使用明确的 `--size`，例如 `3840x2160`。

## 宽高比

支持：`1:1`、`16:9`、`9:16`、`4:3`、`3:4`、`2.35:1`。

- Google 多模态：`imageConfig.aspectRatio`
- OpenAI：`gpt-image-2` 使用与请求宽高比最接近的有效自定义尺寸；较旧的 GPT Image 和 DALL·E 模型使用最接近的受支持固定尺寸
- OpenRouter：`imageGenerationOptions.aspect_ratio`；如果仅提供 `--size <WxH>`，则推断宽高比
- Replicate：行为因模型而异——`google/nano-banana*` 使用 `aspect_ratio`，`bytedance/seedream-*` 使用 Replicate 文档中定义的宽高比，Wan 2.7 将 `--ar` 映射为具体的 `size`
- MiniMax：使用官方 `aspect_ratio` 值；如果为 `image-01` 提供了 `--size <WxH>` 而未提供 `--ar`，则发送 `width`/`height`

## 生成模式

**默认**：顺序生成。**批量并行**：当 `--batchfile` 包含 2 个或更多待处理任务时自动启用。

| 情况 | 首选方式 | 原因 |
|-----------|--------|-----|
| 一张图，或 1–2 张简单图像 | 顺序生成 | 协调开销更低，更容易调试 |
| 使用已保存提示词文件生成多张图像 | 批处理（`--batchfile`） | 复用最终确定的提示词，应用共享限流和重试，实现可预测的吞吐量 |
| 每张图像仍需独立推理、编写提示词或探索风格 | 子智能体 | 工作仍处于探索阶段，每张图都需要独立分析 |
| 输入为 `outline.md` + `prompts/`（例如来自 `baoyu-article-illustrator`） | 批处理——使用 `{baseDir}/scripts/build-batch.ts` 组装负载 | 大纲和提示词文件已包含所有所需内容 |

经验法则：提示词文件保存后，如果任务是“生成全部这些图像”，应优先使用批处理而不是子智能体。仅当生成过程与逐图思考或差异较大的创意探索相结合时，才使用子智能体。

**并行行为**：

- 默认工作进程数为自动确定，受配置上限约束，内置默认值为 10
- 提供商专属限流仅适用于批处理模式；默认值已针对吞吐量进行调优，同时避免每分钟请求量突发
- 使用 `--jobs <count>` 覆盖
- 每张图像最多重试 3 次
- 最终输出包括成功数量、失败数量以及每张图像的失败原因

## 错误处理

- 缺少 API 密钥 → 报错并提供设置说明
- 生成失败 → 每张图像自动重试最多 3 次
- 宽高比无效 → 发出警告并使用默认值继续
- 参考图与不受支持的提供商或模型搭配使用 → 报错并提供修复提示

### Codex image2 回退方案

如果 `--provider openai --model gpt-image-2` 因缺少 `OPENAI_API_KEY` 而失败，但当前运行时具有原生图像生成后端，或仓库级 `codex-imagegen` 包装器可用，请使用该路径，不要让用户继续等待。请明确说明回退方案使用的是真正的参考图生成，还是仅根据提取出的视觉特征重建文本提示词。请参阅 `references/codex-image2-fallback.md`。

## 参考文档

| 文件 | 内容 |
|------|---------|
| `references/usage-examples.md` | 涵盖各提供商和批处理模式的扩展 CLI 示例 |
| `references/codex-oauth-vs-openai-api-key.md` | 为什么无法通过 baoyu-image-gen 的标准 OpenAI API 密钥提供商使用 Codex/ChatGPT OAuth image2 权益 |
| `references/codex-image2-fallback.md` | 缺少 OpenAI API 凭据，但 Codex 或原生图像生成可用时的实用回退行为 |
| `references/providers/dashscope.md` | DashScope 系列、尺寸和限制 |
| `references/providers/zai.md` | Z.AI GLM-image / cogview-4 |
| `references/providers/minimax.md` | MiniMax image-01 + 主体参考 |
| `references/providers/openrouter.md` | OpenRouter 多模态流程 |
| `references/providers/replicate.md` | Replicate 支持的模型系列和防护规则 |
| `references/providers/agnes.md` | Agnes（agnes-image-2.1-flash）的尺寸、参考图和限制 |
| `references/config/preferences-schema.md` | EXTEND.md 模式 |
| `references/config/first-time-setup.md` | 首次设置流程 |

## 扩展支持

通过 EXTEND.md 提供自定义配置。路径和模式请参阅步骤 0。
