# Reference Video Replica QC

用于参考视频复刻、拆解、对齐质检和动效组件沉淀。它先锁定帧率、分辨率、起止帧和编码基线，用采样帧定位问题，再用完整帧序列通过素材门、运行时门和交付门。HyperFrames / Remotion 重制会把逐帧重放与参数化组件分开记录，避免把“看起来相似”误写成像素级一致。

## 示例成片：Presenton 复刻 Bitexact 成片

[▶ Watch Presenton Replica Bitexact Showcase](https://github.com/user-attachments/assets/f792bd12-d8b3-43b7-b751-98aeb033713b)

- 类型：参考视频复刻结果
- 级别：bit-exact / pixel-aligned 交付成片
- 时长：35.136 秒
- 规格：1920x1080，30fps，H.264 + AAC
- 文件：`rn-replica-qc/assets/showcases/presenton-replica-pixel-aligned-bitexact.mp4`

0.5 秒对照抽帧：

![0.5 秒对照图](../assets/images/rn-replica-qc-compare.jpg)

## 做什么类型的视频

- 参考视频复刻
- HyperFrames / Remotion 动效重制
- 可复用视频动效组件沉淀
- 源码一致、渲染帧像素一致、编码成片帧对齐、视觉对齐、风格对齐五级判断
- HyperFrames / Remotion 重制视频的质检
- “当前仍然没有对齐”这类返修定位

## 长期意义

这个 skill 的重点不是复制某一个视频文件，而是把参考视频中真正有视频感的运动语言拆出来：镜头节奏、线条轨道、模型列表、卡片状态切换、标题入场、遮罩、缩放、转场、字幕层级和 CTA 动效。每个被复刻并验证过的段落，都可以进一步整理成 HyperFrames / Remotion 能写、能组合、能参数化的组件。

组件库积累起来以后，AI 制作视频时就能根据内容自由选择：这个段落用模型切换组件，那个段落用流程推进组件，结尾用 CTA 组件，解释概念时用卡片展开组件。这样视频会越来越像真正的动态内容，而不是传统代码生成视频里常见的一页页 PPT 式切换。

## 风格与方法

这是一个质检和拆解 skill，本身不固定某种视觉风格。它关注三道可失败的证据门：

- 素材门：完整帧抽取数量正确，精灵图逐像素回读一致
- 运行时门：真实生产时间轴逐帧截图与参考帧序列对齐
- 交付门：正式 MP4 解码后检查完整帧、边界帧、时间偏移与编码基线

定位和返修仍保留这些证据：

- 每 `0.5s` 抽帧
- 失败窗口用 `0.1s` 或指定时间点密采样
- 秒级行为时间线
- side-by-side contact sheet
- 局部 crop / overlay / 组件级对齐证据
- 返修日志和相邻时间点回测
- 全帧 MAE、最大通道差、变化像素数、时间偏移、边界帧、PSNR / SSIM / 哈希 / `cmp` 等硬指标
- 第一个失败时间点和修复清单

逐帧重放只证明某段参考片已被准确复现，不自动等于可复用组件。入库时必须把 `exact-replay` 与 `parametric-motion` 分开记录。每个可复用组件都应该记录：

- 组件描述和适用场景
- 输入参数和内容槽位
- 时间线、缓动、状态变化
- 技术栈：HyperFrames / Remotion / React / CSS / SVG / GSAP
- 对齐证据和已知限制

## 适合使用

- "复刻这个视频。"
- "每 0.5 秒抽帧分析原视频。"
- "检查新视频和参考视频是否对齐。"
- "我要像素级对齐。"
- "把这个动效复刻成 HyperFrames/Remotion 组件。"
- "把这段参考视频里的模型列表/线条/卡片动效沉淀到组件库。"

## 不适合使用

- 只想做一个同风格原创短片。那更适合 `dark-saas-magic-video`。
- 只想做黑底白字开场。那更适合 `black-white-text-opener`。
- 想在没有完整帧、真实运行时截图和正式成片解码证据时宣称像素级一致。证据不足时只能降级为视觉对齐或风格对齐。

## 配套工具

- `extract_frame_range.py`：按起止帧提取无损完整帧序列
- `build_frame_sprite_rows.py`：构建宽度受控的无损精灵图行
- `verify_frame_sprite_rows.py`：验证每个精灵格与源帧逐像素一致
- `verify_timeline_playback.cjs`：驱动真实生产时间轴并逐帧截图
- `verify_frame_sequence.py`：计算全帧、边界帧与时间偏移证据
- `compare_videos.py`：解码正式视频并汇总哈希、MAE、PSNR、SSIM 和编码基线

## 安装

```bash
npx skills add https://github.com/Pluviobyte/rnskill --skill rn-replica-qc
```
