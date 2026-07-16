<!-- source-sha256: 8082a4af11e3db2d296642bc28a37542991754ed3fdcf4d6a904ead58b82407b -->
---
name: claude-session-introspect
description: |
  检查位于 ~/.claude/projects/ 的 Claude Code 会话 JSONL 文件，以提取真实的对话遥测数据：令牌计数（输入/输出/缓存读取/缓存写入）、助手轮次、人工提示数、工具使用次数、压缩边界以及压缩摘要的内容。当用户询问“这个会话使用了多少令牌”“我发送了多少条提示”“显示这次对话的统计信息”“哪些内容被压缩了”“压缩边界在哪里”“自省会话”“对 JSONL 做脑部手术”，或需要任何存在于磁盘会话日志而非实时上下文窗口中的数据点时，请使用此技能。灵感来自 Tal Raviv 的文章《I wanted to know how compaction works》。
license: MIT
compatibility: |
  需要 `jq`。会话位于 `~/.claude/projects/<encoded-cwd>/<session-uuid>.jsonl`。encoded-cwd 是绝对工作目录，其中 `/` 被替换为 `-`，并在开头添加一个 `-`。每一行都是一个包含 `type`、`message`、`toolUseResult` 等字段的 JSON 对象。
metadata:
  author: swyxio
  version: "1.0"
  last-updated: "2026-04-08"
  primary-tools: jq, bash
---

# Claude 会话自省

Claude Code 会将每次对话作为 JSONL 文件持久化到磁盘。此技能提供了一套方法，用于打开会话文件并提取你真正需要的数据——令牌用量、提示数、压缩事件、工具调用——无需猜测。

## 会话存储位置

```
~/.claude/projects/<encoded-cwd>/<session-uuid>.jsonl
```

`<encoded-cwd>` 是项目工作目录的绝对路径，其中 `/` 被替换为 `-`，并在开头添加一个 `-`。示例：`/Users/swyx/Work/foo` → `-Users-swyx-Work-foo`。

每一行代表一个事件。值得关注的 `type` 值：

| type | 含义 |
|---|---|
| `user` | 一条真实用户消息**或**一个工具结果（通过 `toolUseResult` 是否非 null 来区分） |
| `assistant` | 一个助手轮次（一次模型响应）。`message.usage` 包含令牌计数。 |
| `system` | 系统消息（大多与压缩有关） |
| `file-history-snapshot` | 用于撤销操作的已编辑文件快照 |
| `attachment` | 图片/文件附件 |
| `permission-mode` | 权限模式切换 |

## 快速定位：查找当前会话

```bash
# 1. encode current working directory
ENC="-$(pwd | sed 's,/,-,g' | sed 's/^-//')"
# 2. list the project's session files, newest first
ls -t "$HOME/.claude/projects/$ENC/"
# 3. the most recent .jsonl is usually the live one
SESSION="$HOME/.claude/projects/$ENC/$(ls -t "$HOME/.claude/projects/$ENC/" | head -1)"
echo "$SESSION"
```

如果你知道会话 UUID（Claude Code 会显示它，图片缓存路径中也会包含它），可以搜索所有项目：

```bash
find ~/.claude/projects -name '<uuid>.jsonl'
```

## 核心统计数据（一次完成）

此技能文件夹中的 `stats.sh` 脚本接受一个会话路径，并输出令牌总量、轮次、提示数、工具使用次数以及所有压缩事件。

```bash
bash stats.sh "$SESSION"
```

如果手边没有该脚本，下面是内联的 jq 单行命令。

### 整个会话的令牌总量

```bash
jq -s '
  [.[] | select(.message.usage)] |
  {
    assistant_turns: length,
    input_tokens:        (map(.message.usage.input_tokens // 0)              | add),
    output_tokens:       (map(.message.usage.output_tokens // 0)             | add),
    cache_read_tokens:   (map(.message.usage.cache_read_input_tokens // 0)   | add),
    cache_create_tokens: (map(.message.usage.cache_creation_input_tokens // 0)| add)
  }
' "$SESSION"
```

`input_tokens` 是全新的（未缓存）输入。在长会话中，`cache_read_tokens` 通常是占主导地位的数字——它表示从提示缓存中重新读取了多少内容。`cache_create_tokens` 表示新写入缓存的内容量。实际处理的令牌总量 = `input + cache_read + cache_create`。

### 按事件类型计数

```bash
jq -r '.type' "$SESSION" | sort | uniq -c
```

### 真实的人工提示（排除工具结果和系统提醒）

仅当 `toolUseResult` 为 null 时，一条 `type:"user"` 记录才是人工消息。即便如此，其内容也可能是系统注入的提醒，而不是用户的话。

```bash
jq -r '
  select(.type == "user" and .toolUseResult == null) |
  (.message.content
    | if type == "string" then .
      else (map(select(.type == "text") | .text) | join("\n"))
      end)
' "$SESSION" > /tmp/prompts.txt

# total non-empty user message blocks
grep -cv '^$' /tmp/prompts.txt

# distinct human messages = blocks not starting with <system-reminder> or <command-
awk '
  BEGIN { n = 0; cur = "" }
  /^$/ { if (cur != "" && cur !~ /^<system-reminder>/ && cur !~ /^<command-/) n++; cur=""; next }
  { if (cur=="") cur=$0 }
  END { if (cur != "" && cur !~ /^<system-reminder>/ && cur !~ /^<command-/) n++; print n }
' /tmp/prompts.txt
```

（方法粗糙但有效。如果你想要手术刀般的精确度，请解析内容数组，并跳过第一个文本元素为 `<system-reminder>` 标签的内容块。）

### 工具调用——调用次数及使用了哪些工具

```bash
jq -r '
  select(.type == "assistant") |
  .message.content[]? |
  select(.type == "tool_use") |
  .name
' "$SESSION" | sort | uniq -c | sort -rn
```

### 压缩边界——位置、原因以及保留下来的内容

压缩操作会插入一个带有 `subtype:"compact_boundary"` 的 `system` 事件（较旧的版本可能会在下一条用户消息上使用 `isCompactSummary`）。摘要本身是紧随其后的用户消息，并以“This session is being continued from a previous conversation that ran out of context.”作为前缀。

```bash
# count compaction events
jq -r 'select(.type=="system" and (.subtype // "") == "compact_boundary") | .timestamp' "$SESSION" | wc -l

# was each one auto or manual?
jq -r '
  select(.type == "system" and (.subtype // "") == "compact_boundary") |
  {ts: .timestamp, trigger: (.compactMetadata.trigger // "unknown"), preTokens: (.compactMetadata.preCompactTokens // null)}
' "$SESSION"

# read the compaction summaries (the actual contents that survived)
jq -r '
  select(.type == "user" and (.isCompactSummary == true or
    ((.message.content // "") | tostring | test("session is being continued from a previous conversation"))))
  | (.message.content | if type == "string" then . else (map(select(.type=="text").text)|join("\n")) end)
' "$SESSION" | less
```

### 每轮令牌用量（用于发现用量暴增）

```bash
jq -r '
  select(.message.usage) |
  [.timestamp,
   (.message.usage.input_tokens // 0),
   (.message.usage.output_tokens // 0),
   (.message.usage.cache_read_input_tokens // 0)]
  | @tsv
' "$SESSION" | column -t
```

这可以帮助你找到导致上下文膨胀的那一次工具结果——按 `cache_read` 对整个会话进行升序排序，然后观察数值在哪里突然跃升。

## 注意事项

- **`type:"user"` 被复用了。** 工具结果同样是 `type:"user"`。要获取人工轮次，请始终使用 `toolUseResult == null` 进行过滤。
- **在长会话中，`input_tokens` 看起来很小。** 这是正确的——它表示未缓存发送的增量。几乎所有内容都通过 `cache_read_input_tokens` 流转。
- **“实时”会话文件并不总是最新的文件。** 如果同一项目中打开了多个 Claude Code 窗口，它们都会写入同一个项目文件夹。请通过 UUID 加以区分——聊天标题和图片缓存路径都会暴露它。
- **JSONL 文件会无限增长。** 一个长期运行的项目文件夹可能包含数百个会话文件。`ls -t | head` 是你的好帮手。
- **不要编辑实时 JSONL。** Claude Code 会在 `/resume` 时重新读取它。如果你想进行“脑部手术”（Tal Raviv 的说法），请将文件复制出来，编辑副本，然后在一个干净的目录中使用 `claude --resume <copied-uuid>`。

## 何时使用此技能

- “这个会话消耗了多少令牌？”
- “我今天发送了多少条提示？”
- “压缩从哪里开始，哪些内容被摘要了？”
- “哪个工具调用让上下文暴增了？”
- 构建需要真实数据的统计信息展示、排行榜或“built with Claude Code”徽章。
- 对出现异常的会话进行取证——按顺序重放工具调用。

## 参考资料

- Tal Raviv，《I wanted to know how compaction works》— https://www.talraviv.co/p/i-wanted-to-know-how-compaction-works
- 关于会话存储的 Claude Code 文档 — `~/.claude/projects/`
