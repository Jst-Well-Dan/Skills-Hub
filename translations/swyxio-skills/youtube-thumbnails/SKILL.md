<!-- source-sha256: 0510e7b430240dd7884eecefb37a8b80f53f2276444f4515d38510ed0d7b67f2 -->
---
name: youtube-thumbnails
description: >
  当用户要求“创建 YouTube 缩略图”“生成缩略图”“制作视频缩略图”，
  或需要通过 Google Gemini 为 YouTube 视频生成 AI 缩略图时，
  应使用此技能。涵盖提示词工程、图像生成、压缩以及上传到 YouTube Studio。
version: 0.1.0
---

# 通过 Gemini 生成 YouTube 缩略图

## 概述
使用 Google Gemini 的图像生成功能（Pro 模式）生成自定义 YouTube 缩略图。每张缩略图均为 1280x720 图像，包含醒目的文字叠加层、主题视觉元素和品牌标识。

## 分步工作流程

### 1. 收集视频信息
对于每个需要缩略图的视频，收集：
- **标题**（已在 YouTube 上设置）
- **内容类型**：“AI in Action”每周分享会或“Paper Club”论文研读
- **主题摘要**：展示或演示了什么内容（通过提取视频帧或标题确定）
- **演讲者姓名**（可选，用作副标题文字）
- **日期**，采用 `D Mon YYYY` 格式

### 2. 前往 Gemini
- 打开 `gemini.google.com`
- 点击 **工具** 按钮（底部工具栏）
- 启用 **创建图片**
- 点击模型下拉菜单（默认显示“Fast”），然后选择 **Pro**
- 确认聊天输入区域中出现“Image”标签和“Pro”标识

### 3. 编写缩略图提示词
使用以下提示词模板，并针对每个视频进行定制：

```
为标题为“[FULL TITLE]”的视频创建一张 YouTube 缩略图（1280x720）。
[用 1-2 句话说明视频内容——演示、论文或主题]。
视觉风格应为[THEME DESCRIPTION]：[与主题相关的具体视觉元素]。
醒目的文字叠加层：突出显示“[MAIN TITLE]”，并在下方以较小文字显示“[SUBTITLE]”。
添加底部栏，并以粗体显示“[SERIES NAME] [D MON YYYY]”。
请在一角加入 Latent Space 播客徽标——在网络上搜索“Latent Space podcast logo”以找到它。
使用[COLOR PALETTE]，搭配深色[THEME]背景。
```

#### 按内容类型定制提示词

**AI in Action（演示/展示）**：
- 底部栏文字：`AI IN ACTION [D MON YYYY]`
- 视觉主题：与演示主题相匹配（太空、游戏、开发工具等）
- 颜色：鲜艳、激动人心——霓虹蓝、绿色、紫色和电光色调

**Paper Club（论文研读）**：
- 底部栏文字：`PAPER CLUB [D MON YYYY]`
- 视觉主题：学术但引人入胜——神经网络、大脑可视化、公式
- 颜色：深蓝、橙色、白色——兼具学术感和现代感
- 主文字：论文缩写或简称（例如“SDPO”）
- 副标题：论文全名

#### 提示词关键技巧
- 始终要求 Gemini **搜索网络**，查找相关徽标和参考图片
- 明确指定 **1280x720** 尺寸
- 要求主标题使用**醒目、大号文字**——确保在缩略图尺寸下清晰可读
- 添加带有系列名称和日期的**彩色底部栏**
- 保持**深色**背景，使文字更加突出

### 4. 生成并保存
- 提交提示词，等待 Pro 模式生成约 30-45 秒
- 点击生成的图像将其展开
- 点击 **保存**，下载到 ~/Downloads
- 生成的文件将命名为 `Gemini_Generated_Image_[hash].jpeg`

### 5. 压缩到 2MB 以下
YouTube 要求缩略图小于 2MB。Gemini Pro 生成的图像通常为 3-4MB。

```bash
convert "Gemini_Generated_Image_[hash].jpeg" -resize 1280x720 -quality 85 thumb_[label].jpg
```

**命名约定**：`thumb_[abbreviated_date].jpg`（例如 `thumb_jan31.jpg`、`thumb_feb7.jpg`）

### 6. 将缩略图上传到 YouTube Studio
对于每个视频：
1. 前往 YouTube Studio → 内容 → 点击视频
2. 点击左侧边栏中的铅笔/编辑图标（详细信息标签页）
3. 滚动到**缩略图**部分
4. 点击**上传文件**按钮（可能处于隐藏状态——使用 `find` 工具定位其 ref）
5. 选择正确的 `thumb_[date].jpg` 文件
6. 确认缩略图出现在预览中
7. 点击右上角的**保存**

**文件选择器自动化**（macOS）：
点击“上传文件”后，使用 osascript 操作原生文件对话框：
```applescript
tell application "System Events"
    delay 1
    keystroke "g" using {command down, shift down}
    delay 1
    keystroke "/path/to/thumb_[date].jpg"
    delay 0.5
    keystroke return
    delay 1
    keystroke return
end tell
```

### 7. 验证
截取每个视频详细信息页面的屏幕截图，确认自定义缩略图已设置成功。

## 文件大小参考
- Gemini Pro 原始输出：约 3-4MB（过大）
- 执行 `convert -resize 1280x720 -quality 85` 后：约 200-250KB（远低于 2MB 限制）
- YouTube 缩略图大小上限：2MB
- YouTube 缩略图尺寸：1280x720（16:9）
- 支持的格式：JPG、PNG、GIF

## 提示词示例

### 技术演示缩略图
```
为标题为“SpaceMolt - 多人太空游戏中的 AI 智能体”的视频创建一张 YouTube 缩略图（1280x720）。
视频内容是 SpaceMolt 的演示。这是一款多人太空贸易与采矿游戏，AI 智能体会与人类玩家一起自主游玩。
视觉效果应令人兴奋并具有太空主题：宇宙飞船、小行星、霓虹光效和深色宇宙背景。
醒目的文字叠加层：突出显示“SPACEMOLT”，并在下方以较小文字显示“太空游戏中的 AI 智能体”。
添加底部栏，并以粗体显示“AI IN ACTION 7 FEB 2026”。
请在一角加入 Latent Space 播客徽标——在网络上搜索“Latent Space podcast logo”。
使用鲜艳的科幻色彩——电光蓝、绿色和紫色霓虹色调。
```

### 学术论文缩略图
```
为标题为“通过自蒸馏进行强化学习（SDPO）论文研读”的视频创建一张 YouTube 缩略图（1280x720）。
这是关于 SDPO——自蒸馏偏好优化的学术论文研读活动。
视觉效果应具有学术感但又引人入胜：神经网络或大脑可视化，并配有数学公式。
醒目的文字叠加层：突出显示“SDPO”，并在下方以较小文字显示“自蒸馏偏好优化”。
添加底部栏，并以粗体显示“PAPER CLUB 12 FEB 2026”。
请在一角加入 Latent Space 播客徽标——在网络上搜索“Latent Space podcast logo”。
使用深蓝色、橙色和白色配色，并搭配深色学术主题背景。
```

## 故障排除
- **“文件大于 2MB”**：使用 ImageMagick `convert -resize 1280x720 -quality 85` 进行压缩
- **Gemini 生成耗时较长**：Pro 模式需要 30-45 秒。等待并通过屏幕截图检查
- **上传按钮不可见**：使用 `find` 工具通过 ref 定位隐藏的“上传文件”按钮
- **文件选择器自动化失败**：让用户手动选择文件
