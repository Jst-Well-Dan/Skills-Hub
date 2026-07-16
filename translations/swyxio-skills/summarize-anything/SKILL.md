<!-- source-sha256: c966db64cfdbebdd248ca92cf7e6815be19feec56e9eee17894a10e43ea1b0fd -->
---
name: summarize-anything
description: |
  使用递归 Map-Reduce 和任意大语言模型后端，对任意长度的文本（1千至100万词）进行摘要。接受原始文本、Markdown、转录稿、文章、代码库或任何纯文本输入。可生成一种或多种输出格式：执行摘要、带时间戳的章节标题、YouTube 描述、Twitter/X 帖子、标题选项、缩略图提示词、博客大纲、重点引语等。支持焦点指令（“聚焦 AI 相关部分”“强调商业角度”）来引导摘要。可插拔后端包括：OpenRouter、Ollama、OpenAI、Anthropic、Gemini 或任何兼容 OpenAI 的端点。当有人说“总结一下”“给我一份摘要”“TL;DR”“把它缩短”“创建 YouTube 描述”“写一条关于这个的推文”“生成标题”“缩略图创意”，或提供长文本并希望获得任何精简输出时，请使用此技能。
license: MIT
compatibility: |
  需要 curl 和至少一个大语言模型后端。除 shell 工具外，无需本地依赖。使用本地推理时，Ollama 必须正在运行。使用云端后端时，必须设置相应的 API 密钥。
metadata:
  author: swyxio
  version: "1.0"
  last-updated: "2026-03-28"
  primary-tools: curl, jq
---

# 总结任何内容

通过递归 Map-Reduce 对任意长度的文本进行摘要，支持可插拔的大语言模型后端和多种输出格式。

## 设置

### 必需工具

```bash
which curl || echo "curl is required (should be pre-installed on macOS)"
which jq || brew install jq
```

### 大语言模型后端（至少需要一个）

```bash
# Local — no API key needed, runs on your machine
# Install Ollama: https://ollama.com
ollama pull llama3.1:8b        # 4.7GB, 128k context
ollama pull qwen2.5:32b        # 18GB, 128k context (if you have RAM)

# Cloud — set the relevant env var
export OPENAI_API_KEY=sk-...           # GPT-4.1 (1M context, $2/M input)
export ANTHROPIC_API_KEY=sk-ant-...    # Claude Sonnet 4 (200k context)
export GEMINI_API_KEY=...              # Gemini 3.1 Pro (1M context, free tier available)
export OPENROUTER_API_KEY=sk-or-...    # Any model via OpenRouter
```

### 验证

```bash
echo "=== Local ==="
curl -s http://localhost:11434/ 2>/dev/null | grep -q "Ollama" && echo "Ollama: running" || echo "Ollama: not running"
ollama list 2>/dev/null | head -5

echo ""
echo "=== Cloud ==="
[ -n "$OPENAI_API_KEY" ] && echo "OpenAI: configured" || echo "OpenAI: not set"
[ -n "$ANTHROPIC_API_KEY" ] && echo "Anthropic: configured" || echo "Anthropic: not set"
[ -n "$GEMINI_API_KEY" ] && echo "Gemini: configured" || echo "Gemini: not set"
[ -n "$OPENROUTER_API_KEY" ] && echo "OpenRouter: configured" || echo "OpenRouter: not set"
```

## 如何使用此技能

### 输入

1. **要总结的文本**——文件路径、通过管道传入的标准输入或内联文本。可以是任何纯文本格式：Markdown、转录稿、文章、代码、日志等。
2. **焦点指令**（可选）——描述需要强调内容的句子。例如：
   - “聚焦技术架构决策”
   - “强调个人故事和情感脉络”
   - “提取可执行的建议”
   - “突出与开发者相关的内容”
3. **输出格式**——从下方输出目录中选择一种或多种格式。
4. **后端**——要使用的大语言模型（默认选择最佳可用后端）。

### 第 1 步：评估输入

读取输入并估算其大小：

```bash
# Word count
wc -w < input.txt

# Rough token estimate (1 token ≈ 0.75 words)
WORDS=$(wc -w < input.txt | tr -d ' ')
TOKENS=$((WORDS * 4 / 3))
echo "~${TOKENS} tokens"
```

### 第 2 步：选择后端和策略

**后端选择优先级**（如果用户未指定）：

| 输入大小 | 最佳后端 | 原因 |
|---|---|---|
| < 50k tokens | 任意可用后端 | 所有后端都能在一次调用中容纳 |
| 50k-150k tokens | Ollama (llama3.1)、OpenAI、Anthropic | 128-200k 上下文 |
| 150k-500k tokens | Gemini 3.1 Pro、GPT-4.1 | 1M 上下文 |
| 500k-1M tokens | Gemini 3.1 Pro、GPT-4.1 | 1M 上下文，可能需要分块 |
| > 1M tokens | 任意后端（使用递归分块） | 必须使用 Map-Reduce |

**策略选择：**

| 输入大小与上下文窗口的关系 | 策略 |
|---|---|
| 输入可在一次调用中容纳（< 上下文的 80%） | **直接处理**——调用大语言模型一次 |
| 输入超出上下文窗口 | **Map-Reduce**——分块、分别总结，然后合并 |
| 输入达到上下文窗口的 5 倍以上 | **递归 Map-Reduce**——可能需要执行多轮 Reduce |

### 第 3 步：调用大语言模型

#### 后端：OpenAI / OpenAI 兼容接口

适用于：OpenAI、OpenRouter、Ollama、Together、Fireworks 以及任何兼容 OpenAI 的端点。

```bash
call_openai_compatible() {
  local BASE_URL="$1"    # e.g., https://api.openai.com/v1
  local API_KEY="$2"
  local MODEL="$3"
  local SYSTEM="$4"
  local USER_MSG="$5"
  local MAX_TOKENS="${6:-4096}"

  curl -s "${BASE_URL}/chat/completions" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg model "$MODEL" \
      --arg system "$SYSTEM" \
      --arg user "$USER_MSG" \
      --argjson max_tokens "$MAX_TOKENS" \
      '{
        model: $model,
        temperature: 0.3,
        max_tokens: $max_tokens,
        messages: [
          {role: "system", content: $system},
          {role: "user", content: $user}
        ]
      }')" \
    | jq -r '.choices[0].message.content'
}
```

**各提供商专用配置：**

```bash
# OpenAI
call_openai_compatible "https://api.openai.com/v1" "$OPENAI_API_KEY" "gpt-4.1-mini" "$SYSTEM" "$TEXT"

# OpenRouter
call_openai_compatible "https://openrouter.ai/api/v1" "$OPENROUTER_API_KEY" "google/gemini-3.1-flash" "$SYSTEM" "$TEXT"

# Ollama (local)
call_openai_compatible "http://localhost:11434/v1" "ollama" "llama3.1:8b" "$SYSTEM" "$TEXT"

# Gemini (OpenAI-compatible endpoint)
call_openai_compatible "https://generativelanguage.googleapis.com/v1beta/openai" "$GEMINI_API_KEY" "gemini-3.1-flash" "$SYSTEM" "$TEXT"
```

#### 后端：Anthropic（格式不同）

```bash
call_anthropic() {
  local MODEL="$1"
  local SYSTEM="$2"
  local USER_MSG="$3"
  local MAX_TOKENS="${4:-4096}"

  curl -s "https://api.anthropic.com/v1/messages" \
    -H "x-api-key: ${ANTHROPIC_API_KEY}" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n \
      --arg model "$MODEL" \
      --arg system "$SYSTEM" \
      --arg user "$USER_MSG" \
      --argjson max_tokens "$MAX_TOKENS" \
      '{
        model: $model,
        temperature: 0.3,
        max_tokens: $max_tokens,
        system: $system,
        messages: [{role: "user", content: $user}]
      }')" \
    | jq -r '.content[0].text'
}

# Usage
call_anthropic "claude-sonnet-4-20250514" "$SYSTEM" "$TEXT" 4096
```

### 第 4 步：递归 Map-Reduce（适用于长输入）

当输入超出上下文窗口时，递归拆分并总结。

#### 分块

```bash
split_into_chunks() {
  local INPUT_FILE="$1"
  local CHUNK_WORDS="${2:-20000}"  # ~26k tokens per chunk
  local OVERLAP_WORDS="${3:-1000}" # ~1.3k tokens overlap
  local OUTPUT_DIR="${4:-.}"

  # Split on paragraph boundaries near the target word count
  python3 << PYEOF
import re, sys, os

with open("${INPUT_FILE}") as f:
    text = f.read()

paragraphs = re.split(r'\n\s*\n', text)
chunks = []
current = []
current_words = 0

for para in paragraphs:
    para_words = len(para.split())
    if current_words + para_words > ${CHUNK_WORDS} and current:
        chunks.append('\n\n'.join(current))
        # Keep last paragraph as overlap
        overlap_paras = []
        overlap_words = 0
        for p in reversed(current):
            pw = len(p.split())
            if overlap_words + pw > ${OVERLAP_WORDS}:
                break
            overlap_paras.insert(0, p)
            overlap_words += pw
        current = overlap_paras
        current_words = overlap_words
    current.append(para)
    current_words += para_words

if current:
    chunks.append('\n\n'.join(current))

for i, chunk in enumerate(chunks):
    with open(f"${OUTPUT_DIR}/chunk_{i:03d}.txt", "w") as f:
        f.write(chunk)

print(f"{len(chunks)} chunks created")
PYEOF
}
```

#### Map 阶段

独立总结每个分块。Map 提示词应根据最终输出格式定制——不要丢弃稍后需要的信息。

```
SYSTEM_MAP="你是一名严谨的摘要撰写者。请总结以下文本片段。
保留：关键事实、姓名、引语、数字、时间戳和叙事脉络。
如果存在时间戳（例如 [HH:MM:SS] 标题），请保留它们。
将内容压缩至原始长度的约 10%-15%。
${FOCUS_DIRECTIVE}"
```

针对每个分块：
```bash
for chunk_file in chunk_*.txt; do
  TEXT=$(cat "$chunk_file")
  SUMMARY=$(call_openai_compatible ... "$SYSTEM_MAP" "$TEXT" 4096)
  echo "$SUMMARY" > "${chunk_file%.txt}_summary.txt"
done
```

#### Reduce 阶段

连接所有分块摘要，并检查它们能否放入一个上下文窗口：

```bash
cat chunk_*_summary.txt > combined_summaries.txt
SUMMARY_WORDS=$(wc -w < combined_summaries.txt | tr -d ' ')
SUMMARY_TOKENS=$((SUMMARY_WORDS * 4 / 3))

if [ "$SUMMARY_TOKENS" -gt "$CONTEXT_LIMIT" ]; then
  # Recurse: split combined summaries and map-reduce again
  split_into_chunks combined_summaries.txt ...
  # ... repeat map phase ...
else
  # Final reduce: produce the desired output format(s)
  # Use the output-specific prompts from the Output Catalog below
fi
```

#### Reduce 提示词

```
SYSTEM_REDUCE="你正在根据一份长文档的各章节摘要生成最终摘要。
这些章节按时间或先后顺序排列。
请将它们整合成连贯的整体——不要只是简单拼接。
删除重叠章节中的重复内容。
${FOCUS_DIRECTIVE}
${OUTPUT_FORMAT_INSTRUCTIONS}"
```

### 第 5 步：生成输出格式

使用合并后的摘要（如果输入能够容纳，则直接使用原始输入）生成所请求的格式。你可以在一次调用中要求生成多种格式，也可以分别调用以获得更高质量。

**在一次调用中生成多种格式**（高效，适合较短输入）：
```
根据此内容生成以下所有项目：

1. TIMESTAMPS——带时间戳的章节标题
2. YOUTUBE_DESCRIPTION——针对 YouTube SEO 优化的描述
3. TWEETS——3 个推文选项
4. TITLES——5 个标题选项
5. THUMBNAIL_PROMPTS——3 个视觉场景描述

请将每项内容置于清晰的标题下。
```

**分别生成高质量输出**（更适合较长或复杂的输入）：
使用下方针对特定格式的提示词，分别调用大语言模型生成每种格式。

***

## 输出目录

### 1. 执行摘要

1-3 段的散文式摘要。未指定格式时默认使用此格式。

```
PROMPT="请用 1-3 段写一份简洁的执行摘要。
开头先给出最重要的一项结论。
包含关键姓名、数字和结论。
对于事件使用第三人称和过去时，对于持续状态使用现在时。
${FOCUS_DIRECTIVE}"
```

### 2. 要点列表（关键结论）

5-15 个要点，每个要点一句话。

```
PROMPT="请以要点列表的形式提取关键结论。
- 每个要点都应是一个完整且可独立理解的句子
- 将最重要或最令人意外的内容放在前面
- 包含具体的姓名、数字和事实——不要使用含糊的表述
- 目标为 8-12 个要点
- 不要使用子级要点
${FOCUS_DIRECTIVE}"
```

### 3. 时间戳／章节标题

适用于带时间戳的转录稿。生成章节标记。

```
PROMPT="请为此转录稿创建带时间戳的目录。
每个条目采用以下格式：
[HH:MM:SS] 章节标题——一句话描述

要求：
- 根据内容长度创建 8-20 个章节
- 章节标题应具体且具有描述性（不要使用“引言”或“讨论”）
- 在自然的话题转换处放置时间戳，而不是按任意固定间隔放置
- 如果存在多位说话者，请包含说话者切换
- 一句话描述应告诉读者将在该章节中了解到什么
${FOCUS_DIRECTIVE}"
```

### 4. YouTube 章节

与时间戳类似，但采用 YouTube 章节功能所需的格式（第一个必须为 0:00）。

```
PROMPT="请为此转录稿创建 YouTube 章节标记。
格式：
0:00 章节标题
M:SS 章节标题
...

要求：
- 第一个章节必须是 0:00
- 章节之间至少间隔 10 秒
- 根据内容长度创建 8-20 个章节
- 章节标题应具有吸引力且具体（思考什么标题会让人点击跳转到那个时刻）
- 标题长度保持在 60 个字符以内
- 不要使用“引言”之类的通用标题——应具体说明内容
${FOCUS_DIRECTIVE}"
```

### 5. YouTube 描述

包含摘要、链接和元数据的 SEO 优化描述。

```
PROMPT="请撰写一份针对搜索和互动进行优化的 YouTube 视频描述。

结构：
1. 开场钩子（1-2 句话，让人产生观看欲望——将关键词前置）
2. 段落摘要（用 3-5 句话概述关键内容）
3. 涵盖的关键主题（包含 5-8 个主题的要点列表，每项为一个短语）
4. 讲者简介（如果可以识别，每位讲者 1-2 句话）

要求：
- 在前两行优先放置搜索量最高的关键词（YouTube 在搜索结果中会于约 100 个字符后截断）
- 使用自然语言，不要堆砌关键词
- 包含相关专有名词（人物、公司、技术）
- 不要包含标签（它们应放在单独的字段中）
- 不要虚构链接或社交媒体账号
- 总长度：150-300 词
${FOCUS_DIRECTIVE}"
```

### 6. YouTube 标签／关键词

```
PROMPT="请为此视频生成 YouTube 标签。
以逗号分隔的列表返回。
要求：
- 15-25 个标签
- 混合使用宽泛术语（例如“人工智能”）和具体术语（例如“骨肉瘤治疗”）
- 包含专有名词（提到的人物、公司、产品）
- 包含常见的搜索变体（例如同时包含“AI”和“人工智能”）
- 按相关性从高到低排序
- 每个标签应为 1-4 个词
${FOCUS_DIRECTIVE}"
```

### 7. Twitter/X——单条帖子

一条推文，最多 280 个字符。

```
PROMPT="请写一条关于此内容的推文（最多 280 个字符）。
要求：
- 包括任何账号或标签在内，必须少于 280 个字符
- 内容应足够吸引人点击或互动
- 包含最有趣或最令人意外的角度
- 使用 0-2 个标签（仅在有助于被发现时使用，不要只作装饰）
- 不要以“刚看完……”或“快来看看……”开头——这些很无聊
- 写出 3 个选项，每个采用不同角度（钩子、洞见、争议／问题）
${FOCUS_DIRECTIVE}"
```

### 8. Twitter/X——帖子串

用于深入介绍内容的多条推文串。

```
PROMPT="请撰写一个关于此内容的 Twitter/X 帖子串。

要求：
- 4-8 条推文，采用 1/N 编号格式
- 第 1 条推文（钩子）：必须能够独立吸引读者——这是人们最先看到的内容。以“🧵”或“帖子串：”结尾
- 每条推文必须少于 280 个字符
- 每条推文应表达一个观点，并且能够独立阅读
- 最后一条推文：关键结论或行动号召
- 使用具体事实、数字和引语——不要使用含糊的摘要
- 不要让每条推文都以“推文 N：”开头——应改变结构
${FOCUS_DIRECTIVE}"
```

### 9. LinkedIn 帖子

采用专业语气，并针对互动进行优化。

```
PROMPT="请撰写一篇关于此内容的 LinkedIn 帖子。

要求：
- 以能让人停止滚动的钩子句开头（令人意外的事实、大胆的主张或问题）
- 使用短段落（每段 1-2 句话），方便在移动设备上阅读
- 如果可能，加入个人角度或反思
- 以一个问题结尾，以促进评论
- 150-250 词
- 专业但不要官腔——保持真实的表达
- 不要在每行开头使用表情符号（LinkedIn 陈词滥调）
- 不要使用“我很高兴与大家分享……”或“非常激动地宣布……”
${FOCUS_DIRECTIVE}"
```

### 10. 标题选项

适用于不同场景的 5-10 个标题变体。

```
PROMPT="请为此内容生成 10 个标题选项。包含多种风格：

1-2 个：直接／描述型（说明内容是什么）
1-2 个：好奇心缺口型（让人想进一步了解）
1-2 个：列表／数字型（如果适用）
1-2 个：引用内容中的引语或关键短语
1-2 个：大胆主张或反直觉框架
1 个：SEO 优化型（将关键词前置）

要求：
- 每个标题少于 70 个字符（YouTube/Google 截断限制）
- 不要使用内容无法兑现的标题党
- 包含最具辨识度的专有名词（人物、公司）
- 使用方括号标注每个标题的风格，例如 [好奇心] [描述型] [引语]
${FOCUS_DIRECTIVE}"
```

### 11. YouTube 缩略图提示词

用于 AI 图像生成（Midjourney、DALL-E、Flux）的视觉场景描述。

```
PROMPT="请为此视频创建 5 个 YouTube 缩略图概念。每个概念需提供：

**概念名称：**（2-3 个词）
**视觉描述：** 适合作为 AI 图像生成提示词的详细场景描述。包括：主体、表情、姿势、背景、光线、配色和风格。
**叠加文字：** 叠加在缩略图上的 2-4 个大字（钩子）
**有效原因：** 用一句话说明其心理吸引力

要求：
- 缩略图必须在小尺寸（移动设备）下仍然有效——构图简单、对比鲜明
- 尽可能使用带有强烈情绪的面部特写（人脸能获得更多点击）
- 明亮、饱和的颜色通常比柔和的颜色表现更好
- 叠加文字最多 2-4 个词（更多文字在缩略图尺寸下无法阅读）
- 至少包含一个使用对比／并置的概念（之前／之后、问题／解决方案）
- 至少包含一个带表情的面部特写概念
- 每个概念在视觉上都应与其他概念明显不同
- 尽可能引用内容中的具体人物或场景
${FOCUS_DIRECTIVE}"
```

### 12. 博客文章大纲

用于长篇写作的结构化大纲。

```
PROMPT="请根据此内容创建一份博客文章大纲。

结构：
- 标题（有吸引力且有利于 SEO）
- 副标题／导语（用一句话扩展标题）
- 引言钩子（2-3 句话）
- 4-8 个主要章节，每章包含：
  - 章节标题
  - 2-3 个说明应涵盖内容的要点
  - 一条应包含的关键引语或数据
- 结论
- 建议的元描述（少于 160 个字符）

要求：
- 此大纲应适用于一篇 1500-2500 词的博客文章
- 章节标题应具体且便于快速浏览
- 包含足够的细节，让其他人能够根据此大纲撰写文章
${FOCUS_DIRECTIVE}"
```

### 13. 重点引语

最值得引用和分享的内容片段。

```
PROMPT="请从此内容中提取 5-10 条最佳重点引语。

对于每条引语：
- 原文引语（如果无法确定确切措辞，则提供非常接近的转述）
- 说话者（如果可以识别）
- 一句话背景说明（为什么这条引语重要）

要求：
- 引语应能独立产生强烈效果——即使只看到这句话，也应觉得有吸引力
- 优先选择：令人意外的洞见、令人难忘的措辞、情感时刻、逆向观点
- 同时包含信息型引语和情感／个人型引语
- 每条引语最多 1-3 句话
- 如果内容是转录稿，请注明大致时间戳
${FOCUS_DIRECTIVE}"
```

### 14. 单句摘要（故事梗概）

用一个句子概括核心内容。

```
PROMPT="请用一个句子（少于 30 个词）概括此内容的核心。
它应回答：这讲的是什么，以及为什么值得关注？
请从不同角度写出 5 个选项。"
```

### 15. 新闻简报短文

用于电子邮件新闻简报的短段落。

```
PROMPT="请撰写一段关于此内容的新闻简报短文（50-80 词）。
要求：
- 第一句是钩子
- 包含一个具体细节，使内容更加明确
- 结尾说明读者为什么应该关注，或他们将学到什么
- 使用对话式语气，就像在向朋友推荐
${FOCUS_DIRECTIVE}"
```

### 16. 节目笔记（播客风格）

```
PROMPT="请为此内容创建播客风格的节目笔记。

结构：
- 单集标题
- 一段摘要
- 讨论的关键主题（要点列表）
- 值得注意的引语（2-3 条）
- 提及的人物（简要说明每个人的背景）
- 提及的资源／链接（注意：不要虚构 URL，只列出内容中提到的资源）
- 关键时刻的时间戳（如果来源中存在）
${FOCUS_DIRECTIVE}"
```

### 17. 一体化内容包

当用户希望一次获得所有内容时，使用单次调用请求所有社交／营销格式：

```
PROMPT="请根据此材料创建一个完整的内容包：

## 故事梗概
一个句子，少于 30 个词。

## 执行摘要
2-3 段。

## 关键结论
8-12 个要点。

## YouTube 描述
经过 SEO 优化，150-300 词。

## YouTube 章节
带时间戳的章节标记（第一个必须为 0:00）。

## 标题
5 个不同风格的选项。

## 推文
3 个单条推文选项（每条少于 280 个字符）。

## Twitter 帖子串
5-8 条推文组成的帖子串。

## 缩略图概念
3 个视觉概念，并附叠加文字建议。

## 标签
20 个以逗号分隔的关键词。

${FOCUS_DIRECTIVE}"
```

***

## 焦点指令

焦点指令会注入每个提示词中，以引导摘要方向。它是附加到系统／用户提示词末尾的一个简单句子。

**格式：**
```
FOCUS_DIRECTIVE="焦点：{用户的指令}"
```

**示例：**
```
焦点：强调 AI 和技术方面。
焦点：聚焦个人／情感故事脉络。
焦点：仅提取可执行的战术建议。
焦点：突出与初创企业创始人相关的内容。
焦点：聚焦医学／科学细节。
焦点：强调商业影响。
焦点：面向开发者受众写作。
焦点：面向非技术受众写作。
```

如果没有给出焦点指令，则将其完全省略（不要说“没有特定焦点”）。大语言模型将生成均衡的摘要。

***

## 实际示例

### 示例 1：总结转录稿文件，生成 YouTube 描述和章节

```bash
# Input: a 48-minute transcript markdown file
# Backend: Gemini (free, 1M context — fits in one call)
# Outputs: YouTube description + chapters

TEXT=$(cat transcript.md)
FOCUS="焦点：强调 AI 和癌症治疗创新方面。"

SYSTEM="你正在根据转录稿创建 YouTube 元数据。请生成两个部分：

## YouTube 描述
经过 SEO 优化，150-300 词。将关键词前置。

## YouTube 章节
采用 0:00 格式，包含 10-20 个章节，具体标题少于 60 个字符。"

call_openai_compatible \
  "https://generativelanguage.googleapis.com/v1beta/openai" \
  "$GEMINI_API_KEY" \
  "gemini-3.1-flash" \
  "$SYSTEM" \
  "${TEXT}\n\n${FOCUS}" \
  8192
```

### 示例 2：使用本地 Ollama 总结一份 20 万词的文档

```bash
# Input exceeds 128k context — needs map-reduce
# Backend: Ollama with llama3.1:8b
# Output: Executive summary

# Step 1: Chunk
split_into_chunks "huge_document.txt" 15000 1000 /tmp/chunks

# Step 2: Map
for f in /tmp/chunks/chunk_*.txt; do
  TEXT=$(cat "$f")
  SUMMARY=$(call_openai_compatible \
    "http://localhost:11434/v1" "ollama" "llama3.1:8b" \
    "总结此章节。保留关键事实、姓名和数字。" \
    "$TEXT" 2048)
  echo "$SUMMARY" > "${f%.txt}_summary.txt"
done

# Step 3: Reduce
COMBINED=$(cat /tmp/chunks/chunk_*_summary.txt)
FINAL=$(call_openai_compatible \
  "http://localhost:11434/v1" "ollama" "llama3.1:8b" \
  "将这些章节摘要整合成一份连贯的三段式执行摘要。删除重复内容。" \
  "$COMBINED" 2048)
echo "$FINAL"
```

### 示例 3：根据播客转录稿生成所有社交媒体内容

```bash
TEXT=$(cat podcast_transcript.md)

# Use the all-in-one content package prompt (Output #17)
call_openai_compatible \
  "https://api.openai.com/v1" "$OPENAI_API_KEY" "gpt-4.1-mini" \
  "$ALL_IN_ONE_PROMPT" \
  "$TEXT" \
  8192 > content_package.md
```

***

## 故障排除

### 大语言模型返回的输出被截断

对于请求的输出而言，`max_tokens` 太低。请提高该值：

- 单一格式：`4096` 通常足够
- 多种格式：使用 `8192-16384`
- 一体化内容包：使用 `16384`

### Map-Reduce 生成的摘要不连贯

分块太小或重叠范围太窄。请增大 `CHUNK_WORDS` 和 `OVERLAP_WORDS`。还要确保 Map 提示词要求保留叙事脉络和过渡信息。

### 摘要中出现虚构事实

将温度降低至 `0.1-0.2`。在提示词中加入：“仅包含文本中明确陈述的信息。不要添加外部知识，也不要推断未陈述的事实。”

### Ollama 处理长输入时速度较慢

在 CPU 上运行本地模型并处理长上下文会很慢。可选方案：

- 使用较小的模型（使用 `llama3.1:8b` 而不是 `70b`）
- 更激进地分块（减小 `CHUNK_WORDS`）
- 在 Reduce 阶段切换到云端后端（本地 Map、云端 Reduce）

### Anthropic 400 错误：必须提供 max_tokens

Anthropic API 要求显式设置 `max_tokens`（不同于 OpenAI，在 OpenAI 中它是可选的）。请始终传入该参数。

### OpenRouter 速率限制

在多次调用之间加入短暂延迟：处理分块时使用 `sleep 1`。或者在 Map 阶段使用本地后端，仅在最终 Reduce 时使用 OpenRouter。

## 后端对比

| 后端 | 配置 | 最佳模型 | 上下文 | 成本 |
|---------|--------|-----------|---------|------|
| Ollama（本地） | `http://localhost:11434/v1` | llama3.1:8b | 128k | 免费 |
| OpenAI | `https://api.openai.com/v1` | gpt-4.1-mini | 1M | 输入 $0.40/M |
| Anthropic | 自定义格式 | claude-sonnet-4 | 200k | 输入 $3/M |
| Gemini | `https://generativelanguage.googleapis.com/v1beta/openai` | gemini-3.1-flash | 1M | 免费套餐／输入 $0.15/M |
| OpenRouter | `https://openrouter.ai/api/v1` | 任意模型 | 因模型而异 | 因模型而异 |

**对大多数用户的建议：** 通过兼容 OpenAI 的端点使用 Gemini 3.1 Flash。它提供免费套餐和 1M 上下文（大多数输入无需分块），速度快且质量良好。
