<!-- source-sha256: 2efca615ce55a3edd8fc05c779068a8085816617991987e446606403cd3abb22 -->
---
name: slack-gif-creator
description: 用于创建针对 Slack 优化的动画 GIF 的知识和实用工具。提供约束条件、验证工具和动画概念。当用户请求为 Slack 制作动画 GIF 时使用，例如“为我制作一个 X 做 Y 的 GIF，用于 Slack。”
license: 完整条款见 LICENSE.txt
---

# Slack GIF 创建器

一个提供实用工具和相关知识的工具包，用于创建针对 Slack 优化的动画 GIF。

## Slack 要求

**尺寸：**
- 表情 GIF：128x128（推荐）
- 消息 GIF：480x480

**参数：**
- FPS：10-30（越低，文件越小）
- 颜色：48-128（越少，文件越小）
- 时长：表情 GIF 应保持在 3 秒以内

## 核心工作流程

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. Create builder
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. Generate frames
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # Draw your animation using PIL primitives
    # (circles, polygons, lines, etc.)

    builder.add_frame(frame)

# 3. Save with optimization
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 绘制图形

### 使用用户上传的图像

如果用户上传了图像，请判断他们是希望：
- **直接使用它**（例如，“为这个制作动画”“将这个拆分成帧”）
- **将它用作灵感**（例如，“制作一个类似这样的东西”）

使用 PIL 加载和处理图像：
```python
from PIL import Image

uploaded = Image.open('file.png')
# Use directly, or just as reference for colors/style
```

### 从头绘制

从头绘制图形时，请使用 PIL ImageDraw 图元：

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# Circles/ovals
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# Stars, triangles, any polygon
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# Lines
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# Rectangles
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

**不要使用：** 表情符号字体（在不同平台上并不可靠），也不要假设此技能中存在预打包的图形。

### 让图形更美观

图形应该精致且富有创意，而不是过于基础。可以采用以下方法：

**使用更粗的线条**——轮廓和线条始终将 `width=2` 或更高。细线（width=1）看起来断断续续且不够专业。

**增加视觉深度**：
- 为背景使用渐变（`create_gradient_background`）
- 叠加多个形状以增加复杂度（例如，在一颗星星内部再放一颗较小的星星）

**让形状更有趣**：
- 不要只绘制一个普通圆形——添加高光、圆环或图案
- 星星可以带有光晕（在其后方绘制更大、半透明的版本）
- 组合多个形状（星星 + 闪光、圆形 + 圆环）

**注意颜色搭配**：
- 使用鲜艳的互补色
- 增加对比度（浅色形状使用深色轮廓，深色形状使用浅色轮廓）
- 考虑整体构图

**对于复杂形状**（心形、雪花等）：
- 组合使用多边形和椭圆
- 仔细计算各点以确保对称
- 添加细节（心形可以带有高光曲线，雪花可以带有精细的分枝）

发挥创意并注重细节！优秀的 Slack GIF 应该看起来精致，而不是像占位图形。

## 可用实用工具

### GIFBuilder（`core.gif_builder`）

组装帧并针对 Slack 进行优化：
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # Add PIL Image
builder.add_frames(frames)  # Add list of frames
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### 验证器（`core.validators`）

检查 GIF 是否符合 Slack 要求：
```python
from core.validators import validate_gif, is_slack_ready

# Detailed validation
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# Quick check
if is_slack_ready('my.gif'):
    print("Ready!")
```

### 缓动函数（`core.easing`）

使用平滑运动代替线性运动：
```python
from core.easing import interpolate

# Progress from 0.0 to 1.0
t = i / (num_frames - 1)

# Apply easing
y = interpolate(start=0, end=400, t=t, easing='ease_out')

# Available: linear, ease_in, ease_out, ease_in_out,
#           bounce_out, elastic_out, back_out
```

### 帧辅助工具（`core.frame_composer`）

用于常见需求的便捷函数：
```python
from core.frame_composer import (
    create_blank_frame,         # Solid color background
    create_gradient_background,  # Vertical gradient
    draw_circle,                # Helper for circles
    draw_text,                  # Simple text rendering
    draw_star                   # 5-pointed star
)
```

## 动画概念

### 抖动/振动

通过振荡偏移对象的位置：
- 将 `math.sin()` 或 `math.cos()` 与帧索引结合使用
- 添加少量随机变化，使效果更加自然
- 应用于 x 和/或 y 位置

### 脉冲/心跳

有节奏地缩放对象大小：
- 使用 `math.sin(t * frequency * 2 * math.pi)` 实现平滑脉冲
- 对于心跳效果：快速跳动两次，然后暂停（调整正弦波）
- 在基础大小的 0.8 到 1.2 倍之间缩放

### 弹跳

对象下落并弹起：
- 着地时使用带有 `easing='bounce_out'` 的 `interpolate()`
- 下落时使用 `easing='ease_in'`（加速）
- 通过逐帧增加 y 方向速度来应用重力

### 旋转/转动

使对象围绕中心旋转：
- PIL：`image.rotate(angle, resample=Image.BICUBIC)`
- 对于摇摆效果：使用正弦波控制角度，而不是线性变化

### 淡入/淡出

逐渐出现或消失：
- 创建 RGBA 图像并调整 alpha 通道
- 或使用 `Image.blend(image1, image2, alpha)`
- 淡入：alpha 从 0 变为 1
- 淡出：alpha 从 1 变为 0

### 滑动

将对象从屏幕外移动到指定位置：
- 起始位置：画面边界之外
- 结束位置：目标位置
- 使用带有 `easing='ease_out'` 的 `interpolate()` 实现平滑停止
- 对于越过目标后回弹的效果：使用 `easing='back_out'`

### 缩放

通过缩放和定位实现变焦效果：
- 放大：比例从 0.1 变为 2.0，并裁剪中心
- 缩小：比例从 2.0 变为 1.0
- 可以添加运动模糊来增强戏剧效果（PIL 滤镜）

### 爆炸/粒子爆发

创建向外辐射的粒子：
- 使用随机角度和速度生成粒子
- 更新每个粒子：`x += vx`、`y += vy`
- 添加重力：`vy += gravity_constant`
- 让粒子随时间淡出（降低 alpha）

## 优化策略

仅当用户要求减小文件大小时，实施以下几种方法：

1. **减少帧数**——降低 FPS（使用 10 而不是 20）或缩短时长
2. **减少颜色数量**——使用 `num_colors=48` 而不是 128
3. **减小尺寸**——使用 128x128 而不是 480x480
4. **移除重复帧**——在 save() 中使用 `remove_duplicates=True`
5. **表情模式**——使用 `optimize_for_emoji=True` 自动优化

```python
# Maximum optimization for emoji
builder.save(
    'emoji.gif',
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True
)
```

## 理念

此技能提供：
- **知识**：Slack 的要求和动画概念
- **实用工具**：GIFBuilder、验证器、缓动函数
- **灵活性**：使用 PIL 图元创建动画逻辑

它不提供：
- 固定的动画模板或预制函数
- 表情符号字体渲染（在不同平台上并不可靠）
- 内置于此技能中的预打包图形库

**关于用户上传内容的说明**：此技能不包含预制图形，但如果用户上传了图像，请使用 PIL 加载并处理它——根据用户的请求判断他们是希望直接使用该图像，还是仅将其作为灵感。

发挥创意！组合不同概念（弹跳 + 旋转、脉冲 + 滑动等），并充分利用 PIL 的全部功能。

## 依赖项

```bash
pip install pillow imageio numpy
```
