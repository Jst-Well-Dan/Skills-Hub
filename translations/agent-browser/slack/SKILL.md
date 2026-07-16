<!-- source-sha256: 16817a09c54f503c1d47b326706bdd228b80bf395b297c882c68df7eb4b21fa9 -->
---
name: slack
description: 使用浏览器自动化与 Slack 工作区交互。当用户需要检查未读频道、浏览 Slack、发送消息、提取数据、查找信息、搜索对话或自动执行任何 Slack 任务时使用。触发语句包括“检查我的 Slack”“哪些频道有未读消息”“向……发送消息”“在 Slack 中搜索……”“从 Slack 提取……”“查找是谁说的……”，或任何需要以编程方式与 Slack 交互的任务。
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Slack 自动化

与 Slack 工作区交互，以检查消息、提取数据并自动执行常见任务。

## 快速开始

连接到现有 Slack 浏览器会话或打开 Slack：

```bash
# 连接到端口 9222 上的现有会话（通常用于已经打开的 Slack）
agent-browser connect 9222

# 或者在 Slack 尚未运行时打开 Slack
agent-browser open https://app.slack.com
```

然后生成快照，查看可用内容：

```bash
agent-browser snapshot -i
```

## 核心工作流程

1. **连接/导航**：打开或连接到 Slack
2. **生成快照**：获取带有引用（`@e1`、`@e2` 等）的交互元素
3. **导航**：点击标签页、展开分区或前往特定频道
4. **提取/交互**：读取数据或执行操作
5. **截图**：捕获调查结果的证据

```bash
# 示例：检查未读频道
agent-browser connect 9222
agent-browser snapshot -i
# 查找“更多未读消息”按钮
agent-browser click @e21  # “更多未读消息”按钮的引用
agent-browser screenshot slack-unreads.png
```

## 常见任务

### 检查未读消息

```bash
# 连接到 Slack
agent-browser connect 9222

# 生成快照以定位未读消息按钮
agent-browser snapshot -i

# 查找：
# - “更多未读消息”按钮（通常位于侧边栏顶部附近）
# - “活动”标签页中的“未读”开关（显示未读数量）
# - 带有徽标或粗体文本的频道名称，表示存在未读消息

# 前往“活动”标签页，在一个视图中查看所有未读消息
agent-browser click @e14  # “活动”标签页（引用可能有所不同）
agent-browser wait 1000
agent-browser screenshot activity-unreads.png

# 或检查“私信”标签页
agent-browser click @e13  # “私信”标签页
agent-browser screenshot dms.png

# 或展开侧边栏中的“更多未读消息”
agent-browser click @e21  # “更多未读消息”按钮
agent-browser wait 500
agent-browser screenshot expanded-unreads.png
```

### 前往频道

```bash
# 在侧边栏中或按名称搜索频道
agent-browser snapshot -i

# 在列表中查找频道名称（例如“engineering”“product-design”）
# 点击该频道的 treeitem 引用
agent-browser click @e94  # 示例：engineering 频道引用
agent-browser wait --load networkidle
agent-browser screenshot channel.png
```

### 查找消息/帖子串

```bash
# 使用 Slack 搜索
agent-browser snapshot -i
agent-browser click @e5  # 搜索按钮（典型引用）
agent-browser fill @e_search "keyword"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser screenshot search-results.png
```

### 提取频道信息

```bash
# 获取所有可见频道的列表
agent-browser snapshot --json > slack-snapshot.json

# 解析频道名称和元数据
# 查找 level=2 的 treeitem 元素（分区下的子频道）
```

### 检查频道详情

```bash
# 打开频道
agent-browser click @e_channel_ref
agent-browser wait 1000

# 获取频道信息（成员、描述等）
agent-browser snapshot -i
agent-browser screenshot channel-details.png

# 滚动浏览消息
agent-browser scroll down 500
agent-browser screenshot channel-messages.png
```

### 记录笔记/捕获状态

需要记录 Slack 中的调查结果时：

```bash
# 拍摄带标注的截图（显示元素编号）
agent-browser screenshot --annotate slack-state.png

# 拍摄完整页面截图
agent-browser screenshot --full slack-full.png

# 获取当前 URL 以供参考
agent-browser get url

# 获取页面标题
agent-browser get title
```

## 侧边栏结构

了解 Slack 的侧边栏有助于高效导航：

```
- 帖子串
- 讨论
- 草稿和已发送
- 目录
- [分区标题——外部连接、已加星标、频道等]
  - [以 treeitem 形式列出的频道]
- 私信
  - [列出的私信]
- 应用
  - [应用快捷方式]
- [更多未读消息]按钮（切换未读频道列表）
```

需要查找的关键引用：
- `@e12` - “主页”标签页（通常）
- `@e13` - “私信”标签页
- `@e14` - “活动”标签页
- `@e5` - 搜索按钮
- `@e21` - “更多未读消息”按钮（因会话而异）

## Slack 中的标签页

点击频道后，你将看到以下标签页：
- **消息** - 频道对话
- **文件** - 共享文件
- **已置顶** - 已置顶消息
- **添加画布** - 协作画布
- 其他标签页取决于工作区设置

点击标签页引用即可切换视图并获取不同的信息。

## 从 Slack 提取数据

### 获取文本内容

```bash
# 获取消息或元素的文本
agent-browser get text @e_message_ref
```

### 解析无障碍树

```bash
# 获取 JSON 格式的完整快照，以便以编程方式解析
agent-browser snapshot --json > output.json

# 查找：
# - 频道名称（treeitem 中的 name 字段）
# - 消息内容（位于 listitem/document 元素中）
# - 用户名（包含用户信息的 button 元素）
# - 时间戳（包含时间信息的 link 元素）
```

### 统计未读数量

```bash
# 展开未读消息分区后：
agent-browser snapshot -i | grep -c "treeitem"
# 未读消息分区中每个带有频道名称的 treeitem 代表一个未读频道
```

## 最佳实践

- **连接到现有会话**：如果 Slack 已打开，请使用 `agent-browser connect 9222`。这比打开新浏览器更快。
- **点击前生成快照**：点击按钮前始终执行 `snapshot -i` 以识别引用。
- **导航后重新生成快照**：前往新频道或分区后，生成新快照以查找新的引用。
- **使用 JSON 快照进行解析**：需要提取结构化数据时，使用 `snapshot --json` 获取机器可读输出。
- **控制交互节奏**：在快速连续的交互之间添加 `sleep 1`，让界面有时间更新。
- **检查无障碍树**：无障碍树展示屏幕阅读器（以及自动化工具）能够看到的内容。如果某个元素未出现在快照中，它可能处于隐藏状态或需要滚动后才能显示。
- **在侧边栏中滚动**：如果频道列表很长，请使用 `agent-browser scroll down 300 --selector ".p-sidebar"` 在 Slack 侧边栏内滚动。

## 限制

- **无法访问 Slack API**：此方法使用浏览器自动化，而非 Slack API。无需 OAuth、webhook 或机器人令牌。
- **特定于会话**：截图和快照与当前浏览器会话绑定。
- **速率限制**：Slack 可能会限制快速交互的频率。如有需要，请在命令之间添加延迟。
- **特定于工作区**：你只能与自己的工作区交互，无法进行跨工作区自动化。

## 调试

### 检查控制台错误

```bash
agent-browser console
agent-browser errors
```

### 获取当前页面状态

```bash
agent-browser get url
agent-browser get title
agent-browser screenshot page-state.png
```

## 示例：完整的未读消息检查

```bash
#!/bin/bash

# 连接到 Slack
agent-browser connect 9222

# 生成初始快照
echo "=== Checking Slack unreads ==="
agent-browser snapshot -i > snapshot.txt

# 检查“活动”标签页中的未读消息
agent-browser click @e14  # “活动”标签页
agent-browser wait 1000
agent-browser screenshot activity.png
ACTIVITY_RESULT=$(agent-browser get text @e_main_area)
echo "Activity: $ACTIVITY_RESULT"

# 检查私信
agent-browser click @e13  # “私信”标签页
agent-browser wait 1000
agent-browser screenshot dms.png

# 检查侧边栏中的未读频道
agent-browser click @e21  # “更多未读消息”按钮
agent-browser wait 500
agent-browser snapshot -i > unreads-expanded.txt
agent-browser screenshot unreads.png

# 摘要
echo "=== Summary ==="
echo "See activity.png, dms.png, and unreads.png for full details"
```

## 参考资料

- **Slack 文档**：https://slack.com/help
- **网页版**：https://app.slack.com
- **键盘快捷键**：在 Slack 中输入 `?` 查看快捷键列表
