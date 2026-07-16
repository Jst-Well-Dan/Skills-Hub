<!-- source-sha256: df7575dec2fe74f0f400de394e612b7ca75365934215ed33a7053ffd27a437cc -->
---
name: notebooklm
description: Google NotebookLM 的完整 API——提供全面的编程访问能力，包括 Web UI 中未提供的功能。可创建笔记本、添加来源、生成所有类型的工件，并以多种格式下载。用户明确使用 /notebooklm 或表达类似“创建一个关于 X 的播客”的意图时激活
---

# NotebookLM 自动化

以编程方式完整访问 Google NotebookLM，包括 Web UI 中未公开的功能。创建笔记本，添加来源（URL、YouTube、PDF、音频、视频、图片），与内容对话，生成所有类型的工件，并以多种格式下载结果。

## 安装

**从 PyPI 安装（推荐 AI 智能体使用——可感知 Python 版本）：**
```bash
pip install "notebooklm-py[browser]"   # mandatory; errors must propagate

# [cookies] (rookiepy) is optional and known to FAIL TO BUILD on Python 3.13+.
# Skip it deliberately on 3.13+ rather than swallowing the error — that lets
# *real* install failures (typos, network, PyPI outages) surface for the agent.
if python -c "import sys; sys.exit(0 if sys.version_info < (3, 13) else 1)"; then
    pip install "notebooklm-py[cookies]"   # errors propagate
else
    echo "Skipping [cookies] on Python 3.13+ (rookiepy unavailable). Use 'notebooklm login' interactively."
fi
```

> 完整安装矩阵（额外依赖、无头服务器、贡献者流程）：[GitHub 上的安装指南](https://github.com/teng-lin/notebooklm-py/blob/main/docs/installation.md)。

**从 GitHub 安装（使用最新发布标签，不要使用 main 分支）：**
```bash
# Get the latest release tag (requires curl + jq)
if ! command -v jq >/dev/null; then
    echo "jq is required to read the latest release tag" >&2
    exit 1
fi
LATEST_TAG=$(
    curl -fsSL https://api.github.com/repos/teng-lin/notebooklm-py/releases/latest |
    jq -r '.tag_name'
)
# Includes [browser] so the interactive `notebooklm login` flow works.
pip install "notebooklm-py[browser] @ git+https://github.com/teng-lin/notebooklm-py@${LATEST_TAG}"
```

⚠️ **不要从 main 分支安装**（`pip install git+https://github.com/teng-lin/notebooklm-py`）。main 分支可能包含尚未发布或不稳定的更改。除非你正在测试未发布的功能，否则始终使用 PyPI 或特定发布标签。

**Skill 安装方式：**

- `notebooklm skill install` 将此 Skill 安装到由 CLI 管理的受支持本地智能体目录中。
- `npx skills add teng-lin/notebooklm-py` 从 GitHub 仓库将此 Skill 安装到兼容的智能体 Skill 目录中。
- 如果你已经在智能体 Skill 目录中阅读此文件，则说明该 Skill 已安装。你只需安装下面的 Python 包并完成身份验证。

**CLI 管理的安装：**
```bash
notebooklm skill install
```

## 前置条件

**重要：** 使用任何命令之前，你都必须完成身份验证：

```bash
notebooklm login          # Opens browser for Google OAuth
notebooklm list           # Verify authentication works
```

如果命令因身份验证错误而失败，请重新运行 `notebooklm login`。

### CI/CD、多账户和并行智能体

对于自动化环境、多账户或并行智能体工作流：

| 变量 | 用途 |
|----------|---------|
| `NOTEBOOKLM_HOME` | 自定义配置目录（默认：`~/.notebooklm`） |
| `NOTEBOOKLM_PROFILE` | 当前配置文件名称（默认：`default`） |
| `NOTEBOOKLM_AUTH_JSON` | 内联身份验证 JSON——无需写入文件 |

**CI/CD 设置：** 将 `NOTEBOOKLM_AUTH_JSON` 设置为包含 `storage_state.json` 内容的密钥。

**多账户：** 使用命名配置文件（先运行 `notebooklm profile create work`，再运行 `notebooklm -p work login`）。或者为每个账户使用不同的 `NOTEBOOKLM_HOME` 目录。

**并行智能体：** CLI 按配置文件存储笔记本上下文（`~/.notebooklm/profiles/<profile>/context.json`；隐式默认配置文件还会向后兼容回退到 `~/.notebooklm/context.json`）。如果多个并发智能体共享同一配置文件并使用 `notebooklm use`，它们可能互相覆盖上下文——请使用下面的一种隔离策略。

**并行工作流解决方案：**

1. **始终使用明确的笔记本 ID**（推荐）：在以笔记本为作用域的命令中传入 `-n <notebook_id>` / `--notebook <notebook_id>`，不要依赖 `use`
2. **通过配置文件实现每个智能体隔离：** `export NOTEBOOKLM_PROFILE=agent-$ID`（每个配置文件都有自己的上下文文件）
3. **通过主目录实现每个智能体隔离：** 为每个智能体设置唯一的 `NOTEBOOKLM_HOME`：`export NOTEBOOKLM_HOME=/tmp/agent-$ID`
4. **使用完整 UUID：** 自动化中避免使用部分 ID（它们可能变得不明确）

## 智能体设置验证

开始工作流之前，请验证身份验证已经就绪。**使用 `--test --json`（不要只使用 `--json`）**——单独使用 `--json` 只能证明 cookie 文件可以解析；`--test` 会发起网络调用，并证明这些 cookie 仍能通过 Google 身份验证。

1. `notebooklm auth check --test --json` → 必须同时满足 `"status": "ok"` 和 `"checks.token_fetch": true`。仅有 `"status": "ok"`（未使用 `--test`）是一个容易造成误判的陷阱——过期的 cookie 文件也能通过解析检查。
2. `notebooklm list --json` → 应返回有效 JSON（新账户可能为空）。
3. **如果身份验证失败或缺失 → 首先运行 `notebooklm login`。** 这是主要身份验证路径：打开浏览器，用户登录一次 Google，生成的 `storage_state.json` 会在后续每次运行时重复使用。适用于任何带显示环境的系统。
   - 在无法打开浏览器的无头环境中，改用 `notebooklm login --browser-cookies <browser>`——它会从 Chrome、Firefox 等浏览器中提取用户已登录的 cookie（需要 `[cookies]` 额外依赖；rookiepy 在 Python 3.13+ 上可能无法安装）。使用 `chrome::<profile-name-or-directory>` 指定一个 Chromium 用户配置文件，或使用 `firefox::<container-name>` / `firefox::none` 指定一个 Firefox 容器。
   - 在选择账户前查看已登录的 Google 账户：`notebooklm auth inspect --browser <browser>`（只读；传入 `-v` 可查看每个账户来自哪个 Chromium 用户配置文件，传入 `--json` 可供工具处理）。`notebooklm auth inspect --browser 'chrome::Profile 1'` 等限定形式只检查指定浏览器配置文件。
   - 登录后重新运行步骤 1 进行确认。
4. **如果身份验证此前有效，但 cookie 已过期**（Google 轮换了 SIDTS，或者你刚在浏览器中重新登录）**→ 就地刷新当前配置文件，而不是完整地重新登录：**
   - `notebooklm auth refresh`——根据现有 `storage_state.json` 在服务器端刷新 SIDTS。成本低、无输出；可以安全地通过 cron / launchd / systemd 按 15–20 分钟的频率定时运行，让无人值守的配置文件保持可用。
   - `notebooklm auth refresh --browser-cookies <browser>`——从正在运行的浏览器重新提取 cookie，并根据 `context.json` 中记录的电子邮件地址将其匹配回配置文件。当磁盘上的 `storage_state.json` 已经过期到无法通过服务器端路径刷新，但你刚刚在浏览器中重新登录 Google 时使用。对于具有多个用户配置文件（Chrome 的 `Default`、`Profile 1` 等）的 Chromium 系浏览器，刷新操作会遍历所有配置文件来查找相应电子邮件地址——与 `auth inspect` 使用相同路径（问题 #571）。如果已知确切的浏览器配置文件，请使用 `chrome::<profile-name-or-directory>`。
   - 两种形式都会保留相同的 `--profile`（不会创建新配置文件）。

> **注意：** `notebooklm status` 报告的是*上下文状态*（已选择的笔记本）；不要用它验证身份。

## 此 Skill 的激活条件

**明确触发：** 用户说出“/notebooklm”“使用 notebooklm”，或直接提及该工具名称

**意图检测：** 识别以下类型的请求：

- “创建一个关于[主题]的播客”
- “总结这些 URL/文档”
- “根据我的研究生成测验”
- “把这个转换成音频概览”
- “创建学习用抽认卡”
- “生成视频讲解”
- “制作信息图”
- “创建概念思维导图”
- “将测验下载为 Markdown”
- “将这些来源添加到 NotebookLM”

## 自主操作规则

**自动运行（无需确认）：**

- `notebooklm status`——检查上下文
- `notebooklm auth check`——诊断身份验证问题
- `notebooklm auth inspect`——列出浏览器中可见的 Google 账户（只读）
- `notebooklm auth refresh`——在服务器端刷新当前配置文件的 SIDTS（不创建新配置文件，不执行破坏性写入）
- `notebooklm auth refresh --browser-cookies <browser>`——从浏览器重新提取 cookie 到当前配置文件（为同一 `--profile` 重建 `storage_state.json`，而不是创建新配置文件）
- `notebooklm list`——列出笔记本
- `notebooklm source list`——列出来源
- `notebooklm artifact list`——列出工件
- `notebooklm language list`——列出支持的语言
- `notebooklm language get`——获取当前语言
- `notebooklm language set`——设置语言（全局设置）
- `notebooklm artifact wait`——等待工件完成（在子智能体上下文中）
- `notebooklm source wait`——等待来源处理完成（在子智能体上下文中）
- `notebooklm research status`——检查研究状态
- `notebooklm research wait`——等待研究完成（在子智能体上下文中）
- `notebooklm use <id>`——设置上下文（⚠️ 仅限单智能体——并行工作流中使用 `-n` 标志）
- `notebooklm create`——创建笔记本
- `notebooklm ask "..."`——对话查询（不带 `--save-as-note`）
- `notebooklm suggest-prompts`——为笔记本提供 AI 建议的提示词（只读，不改变状态）
- `notebooklm history`——显示对话历史（只读）
- `notebooklm source add`——添加来源
- `notebooklm profile list`——列出配置文件
- `notebooklm profile create`——创建配置文件
- `notebooklm profile switch`——切换当前配置文件
- `notebooklm doctor`——检查环境健康状况

**运行前询问：**

- `notebooklm delete`、`source delete`、`source delete-by-title`、`source clean`、`note delete`、`artifact delete`、`label delete`、`share remove`、`auth logout`、`clear`、`profile delete` 或 `ask --new`——具有破坏性或会改变状态。获得批准后，在命令支持时传入 `--yes`/`-y`。大多数破坏性 `--json` 命令仍要求明确传入 `--yes`，否则会返回结构化确认错误（根据命令系列不同，为 `CONFIRM_REQUIRED` 或 `VALIDATION_ERROR`）；目前的例外包括 `share remove --json` 和 `ask --new --json`，它们会为非交互调用方跳过提示。
- `notebooklm generate *`——运行时间长，可能失败
- `notebooklm download *`——写入文件系统
- `notebooklm artifact wait`——运行时间长（位于主对话中时）
- `notebooklm source wait`——运行时间长（位于主对话中时）
- `notebooklm research wait`——运行时间长（位于主对话中时）
- `notebooklm research cancel <run_id>`——会改变状态；取消正在运行的研究任务（进行中的任务将转为 FAILED）。触发后即不再等待：它不会确认是否成功——请使用 `notebooklm research status` 重新检查。
- `notebooklm ask "..." --save-as-note`——写入笔记
- `notebooklm history --save`——写入笔记

## 快速参考

| 任务 | 命令 |
|------|---------|
| 身份验证 | `notebooklm login` |
| 使用浏览器 cookie 进行身份验证 | `notebooklm login --browser-cookies <browser>` |
| 使用一个 Chromium 配置文件进行身份验证 | `notebooklm login --browser-cookies 'chrome::Profile 1'` |
| 使用一个 Firefox 容器进行身份验证 | `notebooklm login --browser-cookies 'firefox::Work'` |
| 将所有已登录账户分别导入各自的配置文件 | `notebooklm login --browser-cookies <browser> --all-accounts` |
| 检查已登录账户（只读，按电子邮件地址） | `notebooklm auth inspect --browser <browser>` |
| 检查一个浏览器配置文件/容器 | `notebooklm auth inspect --browser 'chrome::Profile 1'` |
| 诊断身份验证问题 | `notebooklm auth check` |
| 完整诊断身份验证 | `notebooklm auth check --test` |
| 就地刷新当前配置文件（服务器端） | `notebooklm auth refresh` |
| 从重新登录的浏览器刷新当前配置文件 | `notebooklm auth refresh --browser-cookies <browser>` |
| 从一个 Chromium 配置文件刷新 | `notebooklm auth refresh --browser-cookies 'chrome::Profile 1'` |
| 单次保持 cookie 活跃（用于 cron） | `notebooklm auth refresh --quiet` |
| 列出笔记本 | `notebooklm list` |
| 创建笔记本 | `notebooklm create "Title"` |
| 设置上下文 | `notebooklm use <notebook_id>` |
| 显示上下文 | `notebooklm status` |
| 添加 URL 来源 | `notebooklm source add "https://..."` |
| 添加文件 | `notebooklm source add ./file.pdf` |
| 添加 YouTube | `notebooklm source add "https://youtube.com/..."` |
| 列出来源 | `notebooklm source list` |
| 列出标签中的来源 | `notebooklm source list --label <label_id_or_name>` |
| 按 ID 删除来源 | `notebooklm source delete <source_id>` |
| 按精确标题删除来源 | `notebooklm source delete-by-title "Exact Title"` |
| 等待来源处理 | `notebooklm source wait <source_id>` |
| 列出标签 | `notebooklm label list` |
| 将标签展开为来源 | `notebooklm label sources <label_id_or_name>` |
| 生成标签 | `notebooklm label generate --scope unlabeled` |
| 创建标签 | `notebooklm label create "Topic"` |
| 将来源添加到标签 | `notebooklm label add <label_id_or_name> <source_id>...` |
| 从标签移除来源 | `notebooklm label remove <label_id_or_name> <source_id>...` |
| 删除标签 | `notebooklm label delete <label_id_or_name> --yes` |
| Web 研究（快速） | `notebooklm source add-research "query"` |
| Web 研究（深度） | `notebooklm source add-research "query" --mode deep --no-wait` |
| Web 研究（从文件读取查询） | `notebooklm source add-research --prompt-file research_query.txt --mode deep` |
| 检查研究状态 | `notebooklm research status` |
| 等待研究 | `notebooklm research wait --import-all` |
| 取消研究 | `notebooklm research cancel <run_id>`（run_id = `research status` 返回的 `task_id`） |
| 建议可提问的问题 | `notebooklm suggest-prompts` |
| 对话 | `notebooklm ask "question"` |
| 对话（从文件读取长提示词） | `notebooklm ask --prompt-file question.txt` |
| 对话（指定来源） | `notebooklm ask "question" -s src_id1 -s src_id2` |
| 对话（带引用） | `notebooklm ask "question" --json` |
| 对话（将回答保存为笔记） | `notebooklm ask "question" --save-as-note` |
| 对话（使用标题保存） | `notebooklm ask "question" --save-as-note --note-title "Title"` |
| 显示对话历史 | `notebooklm history` |
| 将所有历史保存为笔记 | `notebooklm history --save` |
| 继续指定对话 | `notebooklm ask "question" -c <conversation_id>` |
| 使用标题保存历史 | `notebooklm history --save --note-title "My Research"` |
| 获取来源全文 | `notebooklm source fulltext <source_id>` |
| 获取来源指南 | `notebooklm source guide <source_id>` |
| 生成播客 | `notebooklm generate audio "instructions"` |
| 生成内容（从文件读取长提示词） | `notebooklm generate audio --prompt-file instructions.txt` |
| 生成播客（JSON） | `notebooklm generate audio --json` |
| 生成播客（指定来源） | `notebooklm generate audio -s src_id1 -s src_id2` |
| 生成视频 | `notebooklm generate video "instructions"` |
| 生成报告 | `notebooklm generate report --format briefing-doc` |
| 生成报告（追加说明） | `notebooklm generate report --format study-guide --append "Target audience: beginners"` |
| 生成测验 | `notebooklm generate quiz` |
| 修改幻灯片 | `notebooklm generate revise-slide "prompt" --artifact <id> --slide 0` |
| 检查工件状态 | `notebooklm artifact list` |
| 等待完成 | `notebooklm artifact wait <artifact_id>` |
| 删除工件 | `notebooklm artifact delete <artifact_id> --yes` |
| 下载音频 | `notebooklm download audio ./output.mp3` |
| 下载视频 | `notebooklm download video ./output.mp4` |
| 下载电影级视频 | `notebooklm download cinematic-video ./cinematic.mp4`（`download video` 的别名） |
| 下载信息图 | `notebooklm download infographic ./infographic.png` |
| 下载幻灯片组（PDF） | `notebooklm download slide-deck ./slides.pdf` |
| 下载幻灯片组（PPTX） | `notebooklm download slide-deck ./slides.pptx --format pptx` |
| 下载报告 | `notebooklm download report ./report.md` |
| 下载思维导图 | `notebooklm download mind-map ./map.json` |
| 下载数据表 | `notebooklm download data-table ./data.csv` |
| 下载测验 | `notebooklm download quiz quiz.json` |
| 下载测验（Markdown） | `notebooklm download quiz --format markdown quiz.md` |
| 下载抽认卡 | `notebooklm download flashcards cards.json` |
| 下载抽认卡（Markdown） | `notebooklm download flashcards --format markdown cards.md` |
| 删除笔记本 | `notebooklm delete -n <id>`（添加 `--yes` 可在非交互方式下跳过提示） |
| 列出语言 | `notebooklm language list` |
| 获取语言 | `notebooklm language get` |
| 设置语言 | `notebooklm language set zh_Hans` |
| 列出配置文件 | `notebooklm profile list` |
| 创建配置文件 | `notebooklm profile create work` |
| 切换配置文件 | `notebooklm profile switch work` |
| 删除配置文件 | `notebooklm profile delete old --yes`（`-y`；`--confirm` 是已弃用的别名） |
| 重命名配置文件 | `notebooklm profile rename old new` |
| 单次使用配置文件 | `notebooklm -p work list` |
| 健康检查 | `notebooklm doctor` |
| 健康检查（自动修复） | `notebooklm doctor --fix` |

**并行安全：** 在并行工作流中使用明确的笔记本 ID。以笔记本为作用域的命令普遍支持 `-n/--notebook`（ask/history、source、artifact、generate、download、note、label、share、research，以及笔记本的 delete/rename/summary/metadata）。下载命令还支持 `-a/--artifact`。对于对话，使用 `-c <conversation_id>` 指定特定对话。

**部分 ID：** 使用 UUID 的前 6 个或更多字符。它必须是唯一前缀（如果不明确则失败）。适用于 `use`、`source delete` 和 `wait` 等基于 ID 的命令。若要按精确来源标题删除，请使用 `source delete-by-title "Title"`。自动化中优先使用完整 UUID，以避免歧义。

## 命令输出格式

带 `--json` 的命令返回用于解析的结构化数据：

**创建笔记本：**
```bash
$ notebooklm create "Research" --json
{"notebook": {"id": "abc123de-...", "title": "Research", "created_at": null}}
# parse with: jq -r .notebook.id
```

**添加来源：**
```bash
$ notebooklm source add "https://example.com" --json
{"source": {"id": "def456...", "title": "Example", "type": "web_page", "url": "https://example.com"}}
# parse with: jq -r .source.id
# Note: no `status` field on add — use `source list --json` or `source wait` to check processing state.
```

**生成工件：**
```bash
$ notebooklm generate audio "Focus on key points" --json
{"task_id": "xyz789...", "status": "pending"}
# When run with --wait, completed status also includes a `url` field.
```

**带引用的对话：**
```bash
$ notebooklm ask "What is X?" --json
{"answer": "X is... [1] [2]", "conversation_id": "...", "turn_number": 1, "is_follow_up": false, "references": [{"source_id": "abc123...", "citation_number": 1, "cited_text": "Relevant passage from source..."}, {"source_id": "def456...", "citation_number": 2, "cited_text": "Another passage..."}]}
```

**来源全文（获取已索引内容）：**
```bash
$ notebooklm source fulltext <source_id> --json
{"source_id": "...", "title": "...", "kind": "web_page", "content": "Full indexed text...", "url": null, "char_count": 12345}
```

**理解引用：** 引用中的 `cited_text` 通常是片段或章节标题，而不是完整的引用段落。`start_char`/`end_char` 位置指向 NotebookLM 内部分块索引，而不是原始全文。使用 `SourceFulltext.find_citation_context()` 定位引用：
```python
fulltext = await client.sources.get_fulltext(notebook_id, ref.source_id)
matches = fulltext.find_citation_context(ref.cited_text)  # Returns list[(context, position)]
if matches:
    context, pos = matches[0]  # First match; check len(matches) > 1 for duplicates
```

**提取 ID：** 单项端点会将结果包装在一个信封结构中——解析 `.notebook.id`（来自 `create`）、`.source.id`（来自 `source add`）或 `.task_id`（来自 `generate *`）。对话的 `--json` 引用列表使用 `.references[].source_id`。

## 生成类型

常用生成选项因子命令而异：

- `-n, --notebook` 指定笔记本。
- `-s, --source` 将内容生成器的生成范围限制为特定来源（不适用于 `revise-slide`）。
- `--language` 在支持的情况下设置输出语言（默认为已配置语言或 `en`）。
- `--wait`、`--timeout` 和 `--interval` 是支持等待时共用的轮询控制选项。
- `--json` 返回机器可读的输出。
- `--retry N` 在支持的子命令中自动重试速率限制错误（不适用于 `mind-map`）。
- `--prompt-file PATH` 在 `ask`、除 `mind-map` 之外的生成子命令以及 `source add-research` 中从文件读取描述/查询文本。

| 类型 | 命令 | 选项 | 下载格式 |
|------|---------|---------|----------|
| 播客 | `generate audio` | `--format [deep-dive\|brief\|critique\|debate]`、`--length [short\|default\|long]` | .mp3 |
| 视频 | `generate video` | `--format [explainer\|brief\|cinematic]`（⁴）、`--style [auto\|custom\|classic\|whiteboard\|kawaii\|anime\|watercolor\|retro-print\|heritage\|paper-craft]`、与 `--style custom` 搭配使用的 `--style-prompt` | .mp4 |
| 幻灯片组 | `generate slide-deck` | `--format [detailed\|presenter]`、`--length [default\|short]`（²） | .pdf / .pptx |
| 幻灯片修改 | `generate revise-slide "prompt" --artifact <id> --slide N` | `--wait`、`--notebook` | *（重新下载父幻灯片组）* |
| 信息图 | `generate infographic` | `--orientation [landscape\|portrait\|square]`、`--detail [concise\|standard\|detailed]`、`--style [auto\|sketch-note\|professional\|bento-grid\|editorial\|instructional\|bricks\|clay\|anime\|kawaii\|scientific]` | .png |
| 报告 | `generate report` | `--format [briefing-doc\|study-guide\|blog-post\|custom]`、`--append "extra instructions"`（¹） | .md |
| 思维导图 | `generate mind-map` | `--kind [interactive\|note-backed]`（³）*（默认：interactive）* | .json |
| 数据表 | `generate data-table` | 必须提供描述 | .csv |
| 测验 | `generate quiz` | `--difficulty [easy\|medium\|hard]`、`--quantity [fewer\|standard\|more]` | .json/.md/.html |
| 抽认卡 | `generate flashcards` | `--difficulty [easy\|medium\|hard]`、`--quantity [fewer\|standard\|more]` | .json/.md/.html |

¹ `--append` 仅用于自定义内置模板。使用 `--format custom` 时，请将提示词作为位置参数 `DESCRIPTION` 传入（`notebooklm generate report "PROMPT" --format custom`）；在该模式下，`--append` 会被静默忽略（CLI 会输出警告）。

³ **两种思维导图（问题 #1256）。** `generate mind-map --kind interactive`（默认值）创建**交互式**工作室工件（即 Web 应用现在创建的类型）；系统会轮询直至完成。`generate mind-map --kind note-backed` 创建**笔记支持型**工件——同步生成的 JSON 节点树。两者都会输出相同的 `{mind_map, note_id, kind}` JSON，在 `artifact list --type mind-map` 下列出，并通过 `download mind-map` 导出。`--instructions` 仅适用于笔记支持型。

⁴ **电影级视频（Veo 3）。** `generate video --format cinematic` 通过 Veo 3 生成 AI 纪录片素材；它会**忽略 `--style`**，耗时约 30–40 分钟，并且需要 Google AI Ultra 订阅。也可以通过 `generate cinematic-video` 别名使用（该别名会强制使用 `--format cinematic` 并采用更长的默认超时时间）。使用 `download video` 或 `download cinematic-video` 别名下载。

² **通过提示词生成纵向幻灯片组。** 与信息图不同，slide-deck 没有 `--orientation` 标志。应将纵向幻灯片视为 Skill 层的提示词指导，而不是强类型的 CLI/API 契约：NotebookLM 当前会遵循位置参数 `DESCRIPTION` 中写明的方向提示。加入 `"9:16 portrait"`、`"vertical layout"`、`"portrait mobile format"` 或 `"vertical 9:16 layout"` 等短语，可以让 NotebookLM 将每张幻灯片渲染为 9:16 纵向图片。根据经验：

- `.pptx` 画布本身可能仍是 16:9，但每张幻灯片中嵌入的图片可以渲染为 9:16 纵向格式——适合使用 `python-pptx` 提取为竖屏/移动端视频素材。
- 方向仅在生成时引导一次。`generate revise-slide` 会编辑现有幻灯片中的内容，但不会改变其方向；如果某张幻灯片回退为横向（偶尔会出现不一致），请重新生成整个幻灯片组，而不是修改单页。
- 在提示词中结合明确的页数（例如 `"Create exactly 8 pages, using a vertical 9:16 portrait layout"`），可获得最可预测的输出。

```bash
# Skill prompt hint: ask NotebookLM to render each slide as a 9:16 portrait image
notebooklm generate slide-deck "Create an 8-page deck in 9:16 portrait orientation for mobile viewing" --length default
```

## Web UI 之外的功能

以下能力可通过 CLI 使用，但 NotebookLM 的 Web 界面中并未提供：

| 功能 | 命令 | 说明 |
|---------|---------|-------------|
| **批量下载** | `download <type> --all` | 一次下载某一类型的所有工件 |
| **测验/抽认卡导出** | `download quiz --format json` | 导出为 JSON、Markdown 或 HTML（Web UI 仅显示交互视图） |
| **思维导图提取** | `download mind-map` | 导出供可视化工具使用的分层 JSON |
| **数据表导出** | `download data-table` | 将结构化表格下载为 CSV |
| **以 PPTX 格式下载幻灯片组** | `download slide-deck --format pptx` | 将幻灯片组下载为可编辑的 .pptx（Web UI 仅提供 PDF） |
| **幻灯片修改** | `generate revise-slide "prompt" --artifact <id> --slide N` | 使用自然语言提示词修改单张幻灯片 |
| **追加报告模板说明** | `generate report --format study-guide --append "..."` | 在不丢失格式类型的情况下，为内置格式模板追加自定义说明 |
| **来源全文** | `source fulltext <id>` | 获取任意来源的已索引文本内容 |
| **将对话保存为笔记** | `ask "..." --save-as-note` / `history --save` | 将问答结果或对话历史保存为笔记本笔记 |
| **以编程方式共享** | `share` 命令 | 无需 UI 即可管理共享权限 |

## 常见工作流

### 从研究到播客（交互式）

**时间：** 总计 5–10 分钟

1. `notebooklm create "Research: [topic]"`——*如果失败：使用 `notebooklm login` 检查身份验证*
2. 为每个 URL/文档运行 `notebooklm source add`——*如果某个来源失败：记录警告并继续处理其他来源*
3. 等待来源：运行 `notebooklm source list --json`，直到所有 status=READY——*生成前必须完成*
4. `notebooklm generate audio "Focus on [specific angle]"`（收到询问时确认）——*如果遇到速率限制：等待 5 分钟，然后重试一次*
5. 记下返回的工件 ID
6. 稍后运行 `notebooklm artifact list` 检查状态
7. 完成后运行 `notebooklm download audio ./podcast.mp3`（收到询问时确认）

### 从研究到播客（使用子智能体自动执行）

**时间：** 5–10 分钟，但会在后台继续运行

当用户希望完全自动执行（就绪后生成并下载）时：

1. 像往常一样创建笔记本并添加来源
2. 等待来源就绪（使用 `source wait` 或检查 `source list --json`）
3. 运行 `notebooklm generate audio "..." --json` → 从输出中解析 `task_id`
4. **使用 Task 工具生成后台智能体：**
   ```python
   Task(
     prompt="Wait for artifact {task_id} in notebook {notebook_id} to complete, then download.
             Use: notebooklm artifact wait {task_id} -n {notebook_id} --timeout 1200
             Then: notebooklm download audio ./podcast.mp3 -a {task_id} -n {notebook_id}",
     subagent_type="general-purpose"
   )
   ```
5. 智能体等待期间，主对话继续进行

**子智能体中的错误处理：**

- 如果 `artifact wait` 返回退出代码 2（超时）：报告超时，建议检查 `artifact list`
- 如果下载失败：先检查工件状态是否为 COMPLETED

**优点：** 非阻塞，用户可以进行其他工作，完成后自动下载

### 文档分析

**时间：** 1–2 分钟

1. `notebooklm create "Analysis: [project]"`
2. `notebooklm source add ./doc.pdf`（或 URL）
3. `notebooklm ask "Summarize the key points"`
4. `notebooklm ask "What are the main arguments?"`
5. 根据需要继续对话

### 批量导入

**时间：** 因来源数量而异

1. `notebooklm create "Collection: [name]"`
2. 添加多个来源：
   ```bash
   notebooklm source add "https://url1.com"
   notebooklm source add "https://url2.com"
   notebooklm source add ./local-file.pdf
   ```
3. 使用 `notebooklm source list` 验证

**来源限制：** 因套餐而异——Standard：每个笔记本 50 个，Plus：100 个，Pro：300 个，Ultra：600 个来源。详情请参阅 [NotebookLM 套餐](https://support.google.com/notebooklm/answer/16213268)。CLI 不会强制执行这些限制；限制由你的 NotebookLM 账户应用。
**支持的类型：** PDF、YouTube URL、Web URL、Google Docs、文本文件、Markdown、Word 文档、EPUB、音频文件、视频文件、图片

### 批量导入并等待来源（子智能体模式）

**时间：** 因来源数量而异

添加多个来源，并且需要等待处理完成后再进行对话/生成时：

1. 使用 `--json` 添加来源以获取 ID（使用 `jq -r .source.id` 解析）：
   ```bash
   notebooklm source add "https://url1.com" --json  # → {"source": {"id": "abc...", ...}}
   notebooklm source add "https://url2.com" --json  # → {"source": {"id": "def...", ...}}
   ```
2. **生成后台智能体**，等待所有来源：
   ```
   Task(
     prompt="Wait for sources {source_ids} in notebook {notebook_id} to be ready.
             For each: notebooklm source wait {id} -n {notebook_id} --timeout 600
             Report when all ready or if any fail.",
     subagent_type="general-purpose"
   )
   ```
3. 智能体等待期间，主对话继续进行
4. 来源就绪后，继续对话或生成

**为什么要等待来源？** 来源必须完成索引后才能用于对话或生成。每个来源大约需要 30 秒到几分钟（参见下方的处理时间表）。

### 深度 Web 研究（子智能体模式）

**时间：** 15–30 分钟以上，在后台运行

深度研究会查找并分析某个主题的 Web 来源：

1. 创建笔记本：`notebooklm create "Research: [topic]"`
2. 启动深度研究（非阻塞）：
   ```bash
   notebooklm source add-research "topic query" --mode deep --no-wait
   ```
3. **生成后台智能体**，等待并导入：
   ```
   Task(
     prompt="Wait for research in notebook {notebook_id} to complete and import sources.
             Use: notebooklm research wait -n {notebook_id} --import-all --timeout 1800
             Report how many sources were imported.",
     subagent_type="general-purpose"
   )
   ```
4. 智能体等待期间，主对话继续进行
5. 智能体完成后，来源会自动导入

**替代方案（阻塞式）：** 对于简单情况，省略 `--no-wait`：
```bash
notebooklm source add-research "topic" --mode deep --import-all
# Blocks until research completes (deep mode: 15-30+ min)
```

**何时使用各模式：**

- `--mode fast`：特定主题，需要快速概览（5–10 个来源，数秒）
- `--mode deep`：宽泛主题，需要全面分析（20 个以上来源，15–30 分钟以上）

**研究来源：**

- `--from web`：搜索 Web（默认）
- `--from drive`：搜索 Google Drive

## 输出风格

**进度更新：** 简要说明每一步的状态

- “正在创建笔记本 ‘Research: AI’……”
- “正在添加来源：https://example.com……”
- “正在启动音频生成……（任务 ID：abc123）”

**长时间操作触发后即不再等待：**

- 启动生成后立即返回工件 ID
- 不要在主对话中轮询或等待——生成需要 5–45 分钟（参见时间表）
- 用户手动检查状态，或者使用带 `artifact wait` 的子智能体

**JSON 输出：** 使用 `--json` 标志获取机器可读的输出：
```bash
notebooklm list --json
notebooklm auth check --test --json   # use --test for network-validated auth (see § Agent Setup Verification)
notebooklm source list --json
notebooklm artifact list --json
```

**JSON 架构（关键字段）：**

`notebooklm list --json`：
```json
{"notebooks": [{"index": 1, "id": "...", "title": "...", "is_owner": true, "created_at": "..."}], "count": 1}
```

`notebooklm auth check --test --json`（使用 `--test` 触发网络令牌获取——单独使用 `--json` 会使 `"token_fetch": null`）：
```json
{"status": "ok", "checks": {"storage_exists": true, "json_valid": true, "cookies_present": true, "sid_cookie": true, "token_fetch": true}, "details": {"storage_path": "...", "auth_source": "file", "cookies_found": ["SID", "HSID", "..."], "cookie_domains": [".google.com"]}}
```

`notebooklm source list --json`：
```json
{"notebook_id": "...", "notebook_title": "...", "sources": [{"index": 1, "id": "...", "title": "...", "type": "web_page", "url": "...", "status": "ready|processing|error", "status_id": 1, "created_at": "..."}], "count": 1}
```

`notebooklm artifact list --json`：
```json
{"notebook_id": "...", "notebook_title": "...", "artifacts": [{"index": 1, "id": "...", "title": "...", "type": "Audio", "type_id": 1, "status": "in_progress|pending|completed|unknown", "status_id": 1, "created_at": "..."}], "count": 1}
```

**状态值：**

- 来源：`processing` → `ready`（或 `error`）
- 工件：`pending` 或 `in_progress` → `completed`（或 `unknown`）

## 错误处理

**失败时，为用户提供以下选择：**

1. 重试操作
2. 跳过并继续处理其他内容
3. 调查错误

**错误决策树：**

| 错误 | 原因 | 操作 |
|-------|-------|--------|
| 身份验证/cookie 错误 | 会话已过期 | 运行 `notebooklm auth check`，然后运行 `notebooklm login` |
| `"No notebook context"` | 未设置上下文 | 使用 `-n <id>` 或 `--notebook <id>` 标志（并行），或者使用 `notebooklm use <id>`（单智能体） |
| `"No result found for RPC ID"` | 速率限制 | 等待 5–10 分钟后重试 |
| `GENERATION_FAILED` | Google 速率限制 | 等待并稍后重试 |
| 下载失败 | 生成尚未完成 | 使用 `artifact list` 检查状态 |
| 笔记本/来源 ID 无效 | ID 错误 | 运行 `notebooklm list` 进行验证 |
| RPC 协议错误 | Google 更改了 API | 可能需要更新 CLI |

## 退出代码

所有命令使用一致的退出代码：

| 代码 | 含义 | 操作 |
|------|---------|--------|
| 0 | 成功 | 继续 |
| 1 | 错误（未找到、处理失败） | 检查 stderr，参见错误处理 |
| 2 | 超时（仅等待命令） | 延长超时时间或手动检查状态 |

**示例：**

- 如果未找到来源或处理失败，`source wait` 返回 1
- 如果完成前达到超时时间，`artifact wait` 返回 2
- 如果遇到速率限制，`generate` 返回 1（查看 stderr 获取详情）

## 长提示词

当提示词或查询超过 shell 命令行长度限制时，使用 `--prompt-file` 从文件读取：

```bash
notebooklm ask --prompt-file ./long_question.txt
notebooklm generate report --prompt-file ./custom_report_prompt.txt
notebooklm source add-research --prompt-file ./research_query.txt --mode deep
```

`--prompt-file` 与位置文本参数互斥。文件以 UTF-8 读取，并去除末尾空白。支持范围：`ask`、所有 `generate` 子命令（`mind-map` 除外）以及 `source add-research`。

> **注意：** `--prompt-file` 读取的是*提示词/查询文本文件*，而不是来源文档。若要将文件上传为笔记本来源，请使用 `source add ./file.pdf`。

## 已知限制

**速率限制：** 音频、视频、测验、抽认卡、信息图和幻灯片组生成可能因 Google 的速率限制而失败。这是 API 限制，不是程序错误。

**可靠操作：** 以下操作始终有效：

- 笔记本（列出、创建、删除、重命名）
- 来源（添加、列出、删除）
- 对话/查询
- 思维导图、学习指南、报告和数据表生成

**不可靠操作：** 以下操作可能因速率限制而失败：

- 音频（播客）生成
- 视频生成
- 测验和抽认卡生成
- 信息图和幻灯片组生成

**解决方法：** 如果生成失败：

1. 检查状态：`notebooklm artifact list`
2. 等待 5–10 分钟后重试
3. 使用 NotebookLM Web UI 作为后备方案

**处理时间差异很大。** 长时间操作请使用子智能体模式：

| 操作 | 典型时间 | 建议超时时间 |
|-----------|--------------|-------------------|
| 来源处理 | 30 秒–10 分钟 | 600 秒 |
| 研究（快速） | 30 秒–2 分钟 | 180 秒 |
| 研究（深度） | 15–30 分钟以上 | 1800 秒 |
| 笔记 | 即时 | 不适用 |
| 思维导图 | 即时（同步） | 不适用 |
| 测验、抽认卡 | 5–15 分钟 | 900 秒 |
| 报告、数据表 | 5–15 分钟 | 900 秒 |
| 音频生成 | 10–20 分钟 | 1200 秒 |
| 视频生成 | 15–45 分钟 | 2700 秒 |

**轮询间隔：** 手动检查状态时，每隔 15–30 秒轮询一次，以避免过多 API 调用。

## 语言配置

语言设置控制所生成工件（音频、视频等）的输出语言。

**重要：** 语言是影响账户中所有笔记本的**全局**设置。

```bash
# List all 80+ supported languages with native names
notebooklm language list

# Show current language setting
notebooklm language get

# Set language for artifact generation
notebooklm language set zh_Hans  # Simplified Chinese
notebooklm language set ja       # Japanese
notebooklm language set en       # English (default)
```

**常用语言代码：**

| 代码 | 语言 |
|------|----------|
| `en` | 英语 |
| `zh_Hans` | 中文（简体） |
| `zh_Hant` | 中文（繁體）——繁体中文 |
| `ja` | 日本語——日语 |
| `ko` | 한국어——韩语 |
| `es` | Español——西班牙语 |
| `fr` | Français——法语 |
| `de` | Deutsch——德语 |
| `pt_BR` | Português (Brasil) |

**按命令覆盖：** 在生成命令中使用 `--language` 标志：
```bash
notebooklm generate audio --language ja   # Japanese podcast
notebooklm generate video --language zh_Hans  # Chinese video
```

**离线模式：** 使用 `--local` 标志跳过服务器同步：
```bash
notebooklm language set zh_Hans --local  # Save locally only
notebooklm language get --local  # Read local config only
```

## 故障排除

```bash
notebooklm --help              # Main commands
notebooklm auth check          # Diagnose auth issues
notebooklm auth check --test   # Full auth validation with network test
notebooklm source --help       # Source management
notebooklm research --help     # Research status/wait/cancel
notebooklm generate --help     # Content generation
notebooklm artifact --help     # Artifact management
notebooklm download --help     # Download content
notebooklm language --help     # Language settings
```

**诊断身份验证：** `notebooklm auth check`——显示 cookie 域、存储路径和验证状态  
**重新进行身份验证：** `notebooklm login`  
**检查版本：** `notebooklm --version`  
**刷新由 CLI 管理的安装：** `notebooklm skill install`
