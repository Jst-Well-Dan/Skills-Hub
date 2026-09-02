<!-- source-sha256: 9c22116f64ba00347d6bd8a4658865621346eaf52744a14ab4f6e2b8755ddb6b -->
---
name: hyperframes-cli
description: >
  使用 HyperFrames CLI 开发循环：init、add、catalog、capture、lint、check、snapshot、
  compare、grade-compare、preview、play、present、beats、keyframes、单次或批量 render、publish、
  cloud、cloudrun、feedback、lambda、doctor、browser、info、upgrade、skills、compositions、docs、
  benchmark、telemetry、transcribe、auth、tts 和 remove-background。诊断构建或渲染失败时也要使用。
  validate、inspect 和 layout 是已弃用的别名；请使用 check。涵盖本地、HeyGen 托管云、AWS Lambda
  和 Google Cloud Run 渲染。
---

# HyperFrames CLI

除非项目说明提供了包装器，否则将命令作为 `npx hyperframes ...` 运行。存在包装器时必须遵守。CLI 需要 Node.js 22 或更高版本以及 FFmpeg。

## 开发循环

1. **脚手架：**`npx hyperframes init <project>` 或捕获一个站点。在非 TTY 模式下，传入 `--non-interactive --example=<name>`。
2. **创作：**使用 `/hyperframes-core` 编写合成。
3. **编辑时获取快速反馈：**在首次完成 HTML 后以及结构变更后运行 `npx hyperframes lint`。
4. **运行最终关卡：**运行 `npx hyperframes check`；它会在打开浏览器前重新运行 lint。不要在前面加上冗余的独立 lint 调用。添加 `--snapshots` 以获取带注释的概览帧和问题裁剪图。
5. **检查子合成：**当 `index.html` 挂载 `data-composition-src` 时，捕获中点快照并检查每个已挂载场景。
6. **打开最终 Studio 预览：**运行 `npx hyperframes preview`，将时间线项目 URL 交给用户，并询问是修改还是渲染。
7. **仅在获得批准后渲染：**迭代时使用草稿质量，交付时使用高质量。
8. **验证输出：**确认文件存在、非空，并且时长合理。

```bash
# 快速迭代检查；创作期间按需重复。
npx hyperframes lint

# 必需的最终关卡；包含 lint。
npx hyperframes check
npx hyperframes preview
npx hyperframes render --quality high --output out.mp4
test -s out.mp4
ffprobe -v error -show_format out.mp4
```

`check` 会先运行 lint，然后使用一个浏览器会话和一次 seek 遍历来审计运行时错误、失败请求、布局、`*.motion.json` 断言和 WCAG 对比度。持续存在的问题会影响退出码；短暂的入场或退场问题仅供参考。使用 `--strict` 使警告影响退出码。`validate`、`inspect` 和 `layout` 为兼容性而保留为别名，但不得出现在新说明或脚本中。

## 两种不同的预览界面

不要混淆这些状态：

| 界面                     | 可打开的时机                                           | 用途                                                                              |
| ------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------- |
| 分镜板                   | 合成检查之前，且仅当 `storyboard: yes` 时              | 审阅规划卡片和线框草图。打开 `?view=storyboard#project/<name>`。                  |
| 最终合成预览             | `check` 通过后                                         | 在渲染前审阅已组装的时间线。打开 `#project/<name>`。                              |

早期分镜板不代表最终视频已获批准。渲染始终需要 `hyperframes-core/references/review-loop.md` 中定义的最终批准。

## 子合成冒烟测试

静态审计无法捕获所有挂载失败。当项目使用子合成时，为每个宿主槽至少捕获一个可见中点：

```bash
npx hyperframes snapshot --at <t1>,<t2>,<t3>
```

将微小的无样式内容、画布大小的图标、缺失的主视觉元素或时间线注册超时视为阻止渲染的挂载缺陷。相应的修复方法请参阅 `hyperframes-core/references/sub-compositions.md`。

## Agent 约定

- 对 Agent 和 CI 调用优先使用 `--json`。服务器模式的 `render`、`preview` 和 `play` 不提供普通 JSON 输出；`preview --selection --json` 与 `preview --context --json` 是查询模式例外。
- `doctor --json` 始终以零退出。根据其载荷进行关卡判断：

  ```bash
  npx hyperframes doctor --json | jq -e '.ok' >/dev/null
  ```

- 非 TTY 模式会自动启用。此模式下 `init` 需要 `--example`；使用 `--non-interactive` 在 TTY 上强制确定性行为。
- 在同一验证循环中的所有命令使用同一个 `HYPERFRAMES_RUN_ID`。
- 当相应的警告、变量或 CI 条件必须阻止渲染时，使用 `--strict`、`--strict-all` 和 `--strict-variables`。
- JSON 路径会将主目录脱敏为 `$HOME`；不要尝试逆转该脱敏。
- 当托管云项目接近或超过 200 MB 上传限制时，使用 `cloud render --dry-run --json`，并遵循 `references/cloud.md` 中的 `.hyperframesignore` 排查流程。绝不可仅因资源很大而忽略它。
- 绝不可仅因检查通过就渲染。在最终预览处暂停并等待批准。

## Studio 定向编辑

当用户提及“此元素”或当前选择时，查询 Studio 而不是猜测：

```bash
npx hyperframes preview --context --json --context-fields selection
```

可用时使用 `selection.target.hfId`，否则使用其选择器和源文件。如果结果报告 `no-selection`，请用户点击该元素后重新运行。仅请求所需的上下文切片；仅在需要计算样式或可编辑文本元数据时使用 `--context-detail full`。完整行为和失败代码位于 `references/preview-render.md`。

## 渲染选项

| 需求                                     | 命令                                                                          |
| ---------------------------------------- | ----------------------------------------------------------------------------- |
| 快速本地迭代                             | `npx hyperframes render --quality draft`                                      |
| 最终本地交付                             | `npx hyperframes render --quality high --output out.mp4`                      |
| 可复现的容器渲染                         | `npx hyperframes render --docker --strict --output out.mp4`                   |
| 本地变量驱动的批量渲染                   | `npx hyperframes render --batch rows.json --output "renders/{name}.mp4"`      |
| HeyGen 托管的零基础设施渲染              | `npx hyperframes cloud render`                                                |
| 自行管理的分布式 AWS 渲染                | `npx hyperframes lambda render <project> --width 1920 --height 1080 --wait`   |
| 自行管理的分布式 GCP 渲染                | `npx hyperframes cloudrun render <project> --width 1920 --height 1080 --wait` |

Skill 归属会自动处理——以上示例不需要 `--skill`。通过工作流脚手架创建的项目（`hyperframes init --skill=<workflow>`）会在 `hyperframes.json` 中记录其所属 skill，之后的每次渲染都会在匿名遥测中继承它：重新渲染、`npm run render` 和 `--batch` 均是如此。仅对并非通过工作流创建的项目显式传入 `--skill=<slug>` 以进行标记（其首次渲染随后会持久化该标记）。

当用户希望无需本地 Chrome、FFmpeg 或 AWS 的托管渲染时，使用云渲染。仅当 AWS 所有权是要求时使用 Lambda。仅当 GCP 所有权是要求时使用 Cloud Run。运行任何云路径前，请阅读对应参考文档。

验证渲染成功后，除非遥测被禁用或用户选择退出，否则发送一份反馈报告：

```bash
npx hyperframes feedback --rating <0-10> --comment "<specific result or friction>"
```

无问题运行的反馈应保持简洁。对于任何 bug 或阻碍，提交前先捕获一份**复现包**；不要只发送症状摘要。包括可重新运行的命令（相对于项目目录——反馈提交至公开渠道，因此**不要**粘贴绝对路径、主目录前缀或用户/机器标识符）、预期与实际行为、确切错误信息（同样要从堆栈跟踪中移除绝对路径——保留文件名 + 行号，删除前导目录）、输出是完成/回退/失败、解决方法和复现项目状态。对于描述视觉缺陷且评分 ≤ 7 的情况（黑帧、闪烁、损坏输出、错误帧、空白输出或其他视觉异常），还应包含一个 `COMPOSITION_STRUCTURE:` 块——用于保护隐私的结构解剖信息（元素清单 + 属性存在情况 + 时间线形状），以便维护者无需合成 ZIP 就能与已知 bug 类别进行模式匹配。Agent 会通过 composition-census 辅助工具自动填充它；人类用户无需手动填写。如果问题未再次复现，请说明这一点，仍应包含最后一次失败的命令和日志。仅在获得同意时使用 `--file-issue`：它会将最小复现发布到公开 URL。所需包格式和隐私警告位于 `references/preview-render.md`。

## 运行命令前阅读对应参考文档

以下参考文档及其所属 skill 是强制性命令契约，而非可选的背景阅读材料。在运行表格中的命令前，阅读其对应行。

| 需求                                                                                   | 参考文档                              |
| -------------------------------------------------------------------------------------- | ------------------------------------- |
| `init`、`capture`、`skills`                                                           | `references/init-and-scaffold.md`     |
| `lint`、`check`、motion sidecar、`snapshot`                                            | `references/lint-validate-inspect.md` |
| `compare`、`grade-compare`、变量驱动的 `render --batch`                               | `references/compare-and-batch.md`     |
| 现有项目 Studio 节拍网格的 `beats`                                                    | `references/beats.md`                 |
| `preview`、`play`、`render`、`publish`、Studio 上下文、反馈                            | `references/preview-render.md`        |
| `doctor`、浏览器管理                                                                  | `references/doctor-browser.md`        |
| `auth`、HeyGen 托管云渲染和模板变量                                                   | `references/cloud.md`                 |
| AWS Lambda 部署和渲染                                                                  | `references/lambda.md`                |
| Google Cloud Run 部署和渲染                                                            | `references/cloudrun.md`              |
| `info`、`upgrade`、`compositions`、`docs`、`benchmark`、遥测、媒体预处理               | `references/upgrade-info-misc.md`     |

对于合成变量，还要阅读 `/hyperframes-core` → `references/variables-and-media.md`。对于 `hyperframes add` 和 `hyperframes catalog`，使用 `/hyperframes-registry`。运行 `hyperframes present` 前，阅读 `/slideshow`；运行 `hyperframes keyframes` 前，阅读 `/hyperframes-keyframes`。对于 TTS、转录、字幕或背景移除选项，使用 `/media-use`。

专用命令有意由其所属工作流记录：

```bash
npx hyperframes present <project-dir> --port 3004 --no-open
npx hyperframes beats <project-dir> --json
npx hyperframes keyframes <project-dir> --json
```

`present` 提供具有演示者和观众同步功能的可导航演示文稿。`beats` 是 `references/beats.md` 中定义的独立 Studio 节拍网格工具。`keyframes` 提供可安全 seek 的动画和运动路径诊断。
