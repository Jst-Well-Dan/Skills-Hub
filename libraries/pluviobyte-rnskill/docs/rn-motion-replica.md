# RN Motion Replica

把公开链接或本地参考视频的指定时间段拆成视觉证据，再制作成原创、可验证、可继续修改的 HyperFrames 动效工程。它复用参考片的运动语法和节奏，不交付原片画面、文案、人物或独有品牌资产。

## 适合使用

- 复刻卡片、方框、折线、节点和状态切换的运动方式
- 拆解布局、色彩、入场顺序、停留节奏和转场
- 生成可编辑的 HyperFrames 工程与最终 MP4
- 对成片执行媒体探针、黑帧扫描、代表帧和 contact sheet 质检

## 与 RN Replica QC 的区别

- `rn-motion-replica` 负责制作原创、可编辑的参数化动效工程。
- `rn-replica-qc` 负责定义保真度、验证逐帧证据，并区分精确重放与参数化组件。
- 需要“同样的运动语言、替换内容”时先用本 Skill；需要宣称像素一致或判断对齐等级时必须再经过 `rn-replica-qc`。

## 内置资源

- `scripts/analyze_reference.py`：生成媒体探针、概览图、密集 contact sheet 和场景变化帧
- `scripts/init_motion_project.py`：初始化可编辑的 HyperFrames 方框动效工程
- `references/box-motion-pattern.md`：卡片、连接线、状态替换和推镜转场规则
- `references/qc-checklist.md`：预渲染与最终 MP4 质检清单
- `assets/templates/box-motion-hyperframes/`：可编辑模板
- `assets/showcases/box-motion-replica-35s.mp4`：35 秒样片

## 安装

```bash
npx skills add https://github.com/Pluviobyte/rnskill --skill rn-motion-replica
```
