<!-- source-sha256: 9e8fce92d9060e2bc12cf692773d7490f52f9cf3dc9d376beb0a988c1fedc425 -->
---
name: huashu-agent-swarm
description: 多智能体蜂群并行协作，纯 Git 自组织，适合大型项目开发。当用户提到"蜂群模式"、"多agent"、"并行开发"、"agent swarm"时使用。
---

# 无限智能体循环——无限智能体蜂群模式

> 受 Nicholas Carlini 使用 16 个 Claude 实例自主构建 C 编译器的启发。
> 没有主智能体，纯 Git 自组织，每个智能体独立认领任务、编写代码、推送。

## 触发条件

当用户提到「蜂群模式」「多agent并行」「infinite loop」「agent swarm」「启动蜂群」时使用此技能。

## 前置要求

- tmux（`brew install tmux`）
- Claude CLI（已安装）
- Git 仓库（已有或新建）

## 使用流程

### 步骤 1：描述项目

用户告诉我：

- 项目目录路径（必须是 Git 仓库）
- 项目目标和总体描述
- 初始任务列表（或让智能体自行拆解）
- 智能体数量（默认 8 个）
- 代码规范和测试命令

### 步骤 2：初始化项目

```bash
bash SKILL_DIR/scripts/setup_project.sh <项目目录>
```

这会在项目中创建：

- `AGENT_PROMPT.md` - 从模板生成，需要我根据用户需求定制
- `TASKS.md` - 初始任务清单
- `current_tasks/` - 任务认领目录
- `agent_logs/` - 日志目录

然后我根据 `references/agent-prompt-template.md` 定制 `AGENT_PROMPT.md`，填入项目具体信息。

### 步骤 3：启动蜂群

```bash
bash SKILL_DIR/scripts/start_swarm.sh <agent数量> <项目目录>
```

这会：

1. 为每个智能体创建 Git 工作树（共享 `.git` 对象库，不浪费磁盘）
2. 创建 tmux 会话，每个窗格一个智能体
3. 每个智能体进入无限循环：拉取 → 认领任务 → 执行 → 推送 → 下一个

### 步骤 4：打开观测台

```bash
python3 SKILL_DIR/scripts/dashboard.py <项目目录> 8420
```

浏览器打开 http://localhost:8420，可以：

- 实时查看所有智能体状态、Git 日志、任务进度
- 查看每个智能体的最新日志
- 在输入框中直接向智能体发送指令（写入 `HUMAN_INPUT.md`）
- 一键停止所有智能体

也可以用命令行监控：

```bash
# 终端状态
bash SKILL_DIR/scripts/status.sh <项目目录>

# 发送指令
bash SKILL_DIR/scripts/send_input.sh <项目目录> "你的指令"

# 直接进入 tmux 观察
tmux attach -t swarm-<项目名>
```

### 步骤 5：停止

```bash
bash SKILL_DIR/scripts/stop_swarm.sh <项目目录>
```

自动停止所有智能体 + 合并分支 + 清理工作树。

## 核心机制

### Git 自组织协调

- 每个智能体通过 `current_tasks/*.lock` 文件认领任务
- 通过 `TASKS.md` 了解全局进度
- 通过 `git log` 了解其他智能体的工作
- 冲突由智能体自行解决

### Git 工作树隔离

- 不使用多份克隆，通过 `git worktree` 实现隔离
- 所有工作树共享同一个 `.git` 对象库
- 每个智能体在自己的工作树中独立工作

### 无限循环

- 每个智能体完成一个会话后自动开始下一个
- 通过 `git pull` 获取其他智能体的最新成果
- 通过休眠间隔避免 API 限流

## 关键配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 智能体数量 | 8 | 可在启动时指定 |
| 休眠间隔 | 5 秒 | `agent_loop.sh` 中可调 |
| 模型 | `claude-opus-4-6` | `agent_loop.sh` 中可调 |

## 风险和应对

| 风险 | 应对 |
|------|------|
| API 限流 | 休眠间隔 + 可调智能体数量 |
| 合并冲突 | `AGENT_PROMPT` 指导进行小粒度提交 |
| 死循环无用功 | 日志监控 + 停止条件 |
| 磁盘空间 | `stop_swarm.sh` 自动清理 |
| 成本失控 | 可在 `AGENT_PROMPT` 中限制会话数量 |

---

> **花叔出品** | AI 原生编程者 · 独立开发者
> 公众号「花叔」| 30 万+粉丝 | AI 工具与效率提升
> 代表作：小猫补光灯（App Store 付费榜第 1 名）·《一本书玩转 DeepSeek》
