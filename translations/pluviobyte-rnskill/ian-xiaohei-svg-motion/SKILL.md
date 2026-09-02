<!-- source-sha256: 84ef6a5d61144432e18444bf4b67661efb8c364b5ea6d56850664977c242d344 -->
---
name: ian-xiaohei-svg-motion
description: 为中文文章、脚本、分镜场景、工作流讲解、概念隐喻和短视频视觉辅助创建 Ian 小黑风格的 HTML/SVG 动效插画。当用户要求小黑 SVG、漫画感 HTML、分层 SVG 动效、把小黑生图做成 HTML/SVG、可编辑矢量动效、口播流程动画、手绘漫画动效、正文配图动画，或希望将小黑插画风格适配为可控的 HTML/SVG/GSAP 输出而非栅格图像生成时使用。
---

# Ian 小黑 SVG 动效

将 Ian 小黑正文配图的原则转化为可控的 `HTML + SVG + GSAP timeline` 动效。目标不是复刻生图像素，而是把文章中的一个认知动作重建为分层漫画舞台，以便录制视频、与字幕 cue 对齐，以及后续修改文案和元素。

## 核心规则

不要自动矢量化 PNG 并对生成的大量路径进行动画处理。仅将栅格图像用作构图参考。将场景重建为语义化 SVG 分组：

```text
idea -> shot plan -> SVG layer plan -> HTML/SVG template -> GSAP timeline -> static + motion review
```

## 工作流

1. 从文章、脚本、截图或分镜场景中提取一个认知锚点。
2. 选择一个物理隐喻：分类、搬运、搭桥、泄漏、接住、折叠、称量、打开、改道或坠落。
3. 让小黑执行核心动作。如果移除小黑后含义不变，则重新设计。
4. 设计一个 16:9 的白色画布，包含一个主场景、35% 以上留白，以及最多 3-5 条简短的手写注释。
5. 为每个运动对象构建语义化 SVG 分组。
6. 使用 GSAP timeline 制作动画。使用 `x`、`y`、`rotation`、`scale`、`opacity` 和 SVG 描边绘制。避免布局动画。
7. 同时保存可播放的 HTML 页面和静态审阅截图。
8. 如果这是用于口播成片项目，请在最终渲染前将 timeline 分段映射到字幕/cue 时序。

## 按需阅读

- 在设计新场景或判断结果是否仍具备 Ian 小黑风格之前，阅读 `references/style-rules.md`。
- 在编写或编辑 SVG 结构之前，阅读 `references/svg-layering.md`。
- 在编写 GSAP 动画之前，阅读 `references/motion-rules.md`。

## 输出约定

默认输出文件夹：

```text
output/<slug>-xiaohei-svg-motion/
```

必需文件：

```text
index.html
README.md
preview.png
vendor/gsap.min.js
```

可选文件：

```text
source.png        # reference image, if provided by the user
cue-map.md        # when aligning to spoken script or subtitles
```

## 可复用资源

AI 模型和界面图标位于：

```text
assets/icons/
```

使用 `assets/icons/index.json` 作为唯一事实来源。将原始 SVG 文件保留在子文件夹中，并在生成时将其完整 SVG 内容内联到场景 SVG 中，以保留渐变、描边和品牌颜色。

图标规则：

- 如果 `index.json` 中已有准确的模型、提供商或语义图标，请使用该图标。不要用通用方框、星星、闪光或抽象标记替代 ChatGPT、Claude、Flash 闪电、Step、DeepSeek、Qwen、bug、表格、图表、数据库或网页图标。
- 当用户提供新的 SVG 图标时，将原始 SVG 保存至 `assets/icons/<category>/`，在 `index.json` 中添加条目，然后在场景计划中按 id 引用它。
- 对于对比场景，图标选择是含义的一部分。保持模型图标在尺寸和位置上视觉一致，以便观众能在小黑开始移动物体前识别参与者。

## 模板

当请求类似于带有移动物体、箭头、注释或小黑动作的手绘漫画场景时，使用 `assets/templates/xiaohei-comic-motion/` 作为起始模板。

当请求需要多个变体、可复用系列，或更广泛的口播讲解场景参考集时，使用 `assets/templates/xiaohei-series-reference/`。

将模板复制到项目输出文件夹，然后编辑：

- SVG 分组名称。
- 手写标签。
- 对象位置。
- Timeline 标签和时长。
- README 中关于场景专属隐喻的说明。

## 质量检查

最终回复前：

- 在本地服务器中打开 HTML。
- 检查控制台是否有错误。
- 使用 `?static=1` 捕获静态截图。
- 当场景具有多个节拍时，至少捕获一个播放中间帧。如果可用，使用 `?frame=mid` 获取确定性的审阅帧。
- 目视检查文字、箭头、小黑、道具、传送带、坑洞、卡片和最终落点不会重叠。
- 确认动画具有清晰进展：先展示上下文，其次展示动作，第三展示问题/结果，最后总结。
- 确认注释只在其解释的对象/动作之后出现。
- 如果对象运动已经表现方向，移除装饰性或半透明的引导箭头。
- 确认小黑是动作的一部分。
- 确认页面不只是 `<img>` 标签中的 PNG，除非用户明确要求仅使用 PNG 镜头移动。
