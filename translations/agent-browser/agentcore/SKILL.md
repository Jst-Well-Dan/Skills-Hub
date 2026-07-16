<!-- source-sha256: f616b6dbce7cce388eb62701f254d87a78a3650a9c365db653fee1da3d7388a0 -->
---
name: agentcore
description: 在 AWS Bedrock AgentCore 云浏览器上运行 agent-browser。当用户希望使用 AgentCore、在 AWS 上运行浏览器自动化、通过 AWS 凭证使用云浏览器，或需要由 AWS 基础设施支持的托管浏览器会话时使用。触发条件包括 "use agentcore"、"run on AWS"、"cloud browser with AWS"、"bedrock browser"、"agentcore session"，或任何需要 AWS 托管浏览器自动化的任务。
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# AWS Bedrock AgentCore

在 AWS Bedrock AgentCore 托管的云浏览器会话上运行 agent-browser。所有标准 agent-browser 命令的工作方式完全相同；唯一的区别是浏览器运行的位置。

## 设置

凭证会自动解析：

1. 环境变量（`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`，以及可选的 `AWS_SESSION_TOKEN`）
2. AWS CLI 回退机制（`aws configure export-credentials`），支持 SSO、IAM 角色和命名配置文件

如果用户已有可用的 AWS 凭证，则无需进行额外设置。

## 核心工作流程

```bash
# Open a page on an AgentCore cloud browser
agent-browser -p agentcore open https://example.com

# Everything else is the same as local Chrome
agent-browser snapshot -i
agent-browser click @e1
agent-browser screenshot page.png
agent-browser close
```

## 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `AGENTCORE_REGION` | AWS 区域 | `us-east-1` |
| `AGENTCORE_BROWSER_ID` | 浏览器标识符 | `aws.browser.v1` |
| `AGENTCORE_PROFILE_ID` | 持久化浏览器配置文件（cookies、localStorage） | （无） |
| `AGENTCORE_SESSION_TIMEOUT` | 会话超时时间（秒） | `3600` |
| `AWS_PROFILE` | 用于解析凭证的 AWS CLI 配置文件 | `default` |

## 持久化配置文件

使用 `AGENTCORE_PROFILE_ID` 跨会话保留浏览器状态。这对于保持登录会话非常有用：

```bash
# First run: log in
AGENTCORE_PROFILE_ID=my-app agent-browser -p agentcore open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser close

# Future runs: already authenticated
AGENTCORE_PROFILE_ID=my-app agent-browser -p agentcore open https://app.example.com/dashboard
```

## 实时视图

会话启动时，AgentCore 会将实时视图 URL 输出到 stderr。请在浏览器中打开该 URL，以便通过 AWS 控制台实时观看会话：

```
Session: abc123-def456
Live View: https://us-east-1.console.aws.amazon.com/bedrock-agentcore/browser/aws.browser.v1/session/abc123-def456#
```

## 区域选择

```bash
# Default: us-east-1
agent-browser -p agentcore open https://example.com

# Explicit region
AGENTCORE_REGION=eu-west-1 agent-browser -p agentcore open https://example.com
```

## 凭证使用方式

```bash
# Explicit credentials (CI/CD, scripts)
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
agent-browser -p agentcore open https://example.com

# SSO (interactive)
aws sso login --profile my-profile
AWS_PROFILE=my-profile agent-browser -p agentcore open https://example.com

# IAM role / default credential chain
agent-browser -p agentcore open https://example.com
```

## 与 AGENT_BROWSER_PROVIDER 配合使用

通过环境变量设置提供商，以避免在每条命令中都传递 `-p agentcore`：

```bash
export AGENT_BROWSER_PROVIDER=agentcore
export AGENTCORE_REGION=us-east-2

agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e1
agent-browser close
```

## 常见问题

**"Failed to run aws CLI"** 表示 AWS CLI 未安装或不在 PATH 中。请安装 AWS CLI，或直接设置 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`。

**"AWS CLI failed: ... Run 'aws sso login'"** 表示 SSO 凭证已过期。运行 `aws sso login` 以刷新凭证。

**会话超时：** 默认值为 3600 秒（1 小时）。对于耗时更长的任务，请使用 `AGENTCORE_SESSION_TIMEOUT=7200` 增加超时时间。
