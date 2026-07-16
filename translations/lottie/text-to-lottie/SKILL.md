<!-- source-sha256: e0eeae89f9f98a389a3e5295a9b0f11a48d1e0674a2bb93d0f031ac83777aa6c -->
---
name: text-to-lottie
description: 编写可在本地 Skia 播放器中渲染的 Lottie（Bodymovin）JSON 动画。每当用户要求创建、生成、编辑或修复 Lottie 动画，或要求加载“动画”时使用。
---

# 编写可渲染的 Lottie 文件

此应用使用 **Skia 的 Skottie** 模块渲染 Lottie，请遵循以下规则并验证结果。

## 设置项目

交付物不只是一个 `lottie.json`：还应设置好查看器，并且动画应能在浏览器中预览。如果播放器项目不存在，请创建它；如果已存在，请根据需要安装或更新依赖项、启动开发服务器，并打开本地预览 URL 进行验证。

**始终使用官方 GitHub 播放器项目——绝不要手写自定义查看器。** 此技能的 JSON 规则（插槽、属性面板、`?frame=` URL 控制、Skottie wasm 接线）仅适用于该特定项目。**不要**构建自己的 HTML 页面、替换为 `lottie-web`，或搭建定制的 canvas 环境——这些做法都会悄然偏离此播放器的渲染方式，使下方的验证步骤不再适用。如果此计算机上尚无播放器项目，请使用 **degit** 创建该仓库的新副本：

```bash
npx degit diffusionstudio/lottie my-animation
cd my-animation
npm install   # postinstall 将 CanvasKit wasm 复制到 /public
npm run dev
```

然后打开输出的本地 URL。开发服务器默认为 **`http://localhost:3030`**。如果项目已存在，只需运行 `npm install && npm run dev`。

## `/public` 中必需的文件夹结构

播放器是一个多场景编辑器：每个场景都位于 `public/projects/` 下各自的文件夹中，应用通过路径路由到相应场景。**你必须严格遵循此布局**——任何不符合布局的内容都会被忽略。

```
public/
├── canvaskit.wasm                 # Skia wasm（由 postinstall 复制——请勿修改）
└── projects/
    └── <project-slug>/            # 例如 main-project
        └── <scene-N>/             # 例如 scene-1、scene-2、……（排序方式见下文）
            ├── lottie.json        # 必需——Bodymovin 动画
            ├── controls.json      # 可选——属性面板元数据（参见插槽）
            └── <image files>      # 可选——.png/.jpg/.jpeg/.webp/.gif/.svg 资源
```

扫描器强制执行的规则：

- **Slug 是 URL 路径段。** `<project-slug>` 和 `<scene-N>` 必须是适合作为文件夹名称、近似小写的名称；它们会组成路径 `/<project>/<scene>`。侧边栏标签通过将 slug 转换为标题格式生成（`main-project` → “Main Project”，`scene-1` → “Scene 1”）。
- **场景排序取决于末尾的 `-N`。** 场景的排序顺序由其 slug 末尾的数字决定（`scene-1`、`scene-2`、……，正则表达式 `/-(\d+)$/`）。将新场景命名为 `scene-<N>` 以确保正确排序；末尾没有数字的 slug 排在最后。
- **`lottie.json` 是必需的。** 不含该文件的场景文件夹会从树中被静默丢弃（没有有效场景的项目也会完全消失）。
- **图片通过纯文件名引用。** 将图片放入场景文件夹，并在 Lottie 的 `assets[].p` 中仅以文件名引用它（例如 `"p": "background.png"`）；加载器会从同一文件夹解析它。

## 文件写入位置（以及加载方式）

- 将动画写入 **`public/projects/<project>/<scene-N>/lottie.json`**。如果你正在创建全新动画且未指定目标场景，请创建项目文件夹（例如 `public/projects/my-animation/scene-1/`），将 `lottie.json` 写入其中，然后打开 `/my-animation/scene-1`。
- 应用通过 **`/:project/:scene`**（[`src/router.tsx`](../../../src/router.tsx)）进行路由；`/` 会重定向到第一个项目的第一个场景。画布提供程序（[`src/context/canvas.tsx`](../../../src/context/canvas.tsx)）会获取该场景的 `lottie.json`（以及其中的图片）并进行渲染。
- 开发服务器运行时，场景插件会**监视文件夹树**。添加、删除或重命名项目或场景文件夹时，侧边栏会通过 Vite 的 HMR socket 实时更新（无需重新加载）。编辑现有 `lottie.json` 的*内容*并不会自动重新加载活动场景——请重新加载页面（或重新导航）以读取手动编辑后的 JSON。

## 示例

```json lottie.json
{
  "v": "5.7.0",
  "fr": 60,
  "ip": 0,
  "op": 90,
  "w": 512,
  "h": 512,
  "nm": "Bouncing ball",
  "assets": [],
  "slots": {
    "ballColor": { "p": { "a": 0, "k": [0.231, 0.6, 1, 1] } },
    "ballOpacity": { "p": { "a": 0, "k": 100 } },
    "ballSize": { "p": { "a": 0, "k": [120, 120] } }
  },
  "layers": [
    {
      "ty": 4,
      "nm": "ball",
      "ip": 0,
      "op": 90,
      "st": 0,
      "ks": {
        "o": { "sid": "ballOpacity" },
        "r": { "a": 0, "k": 0 },
        "a": { "a": 0, "k": [0, 0, 0] },
        "s": { "a": 0, "k": [100, 100, 100] },
        "p": {
          "a": 1,
          "k": [
            { "t": 0, "s": [256, 140, 0], "i": { "x": [0.5], "y": [1] }, "o": { "x": [0.7], "y": [0] } },
            { "t": 45, "s": [256, 380, 0], "i": { "x": [0.3], "y": [1] }, "o": { "x": [0.5], "y": [0] } },
            { "t": 90, "s": [256, 140, 0] }
          ]
        }
      },
      "shapes": [
        {
          "ty": "gr",
          "nm": "ball-group",
          "it": [
            { "ty": "el", "p": { "a": 0, "k": [0, 0] }, "s": { "sid": "ballSize" } },
            { "ty": "fl", "c": { "sid": "ballColor" }, "o": { "a": 0, "k": 100 } },
            { "ty": "tr", "p": { "a": 0, "k": [0, 0] }, "a": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [100, 100] }, "r": { "a": 0, "k": 0 }, "o": { "a": 0, "k": 100 } }
          ]
        }
      ]
    },
    {
      "ty": 4,
      "nm": "background",
      "ip": 0,
      "op": 90,
      "st": 0,
      "ks": {
        "o": { "a": 0, "k": 100 },
        "r": { "a": 0, "k": 0 },
        "a": { "a": 0, "k": [0, 0, 0] },
        "s": { "a": 0, "k": [100, 100, 100] },
        "p": { "a": 0, "k": [256, 256, 0] }
      },
      "shapes": [
        {
          "ty": "gr",
          "nm": "background-group",
          "it": [
            { "ty": "rc", "p": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [512, 512] }, "r": { "a": 0, "k": 0 } },
            { "ty": "fl", "c": { "a": 0, "k": [0.5, 0.5, 0.5, 1] }, "o": { "a": 0, "k": 100 } },
            { "ty": "tr", "p": { "a": 0, "k": [0, 0] }, "a": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [100, 100] }, "r": { "a": 0, "k": 0 }, "o": { "a": 0, "k": 100 } }
          ]
        }
      ]
    }
  ]
}
```

```json controls.json
{
  "controls": [
    { "sid": "ballColor", "label": "Ball color" },
    { "sid": "ballOpacity", "label": "Ball opacity", "min": 0, "max": 100, "step": 1 },
    { "sid": "ballSize", "label": "Ball size", "min": 20, "max": 400, "step": 1 }
  ]
}
```

**建议：使用顶层 `nm` 字符串。** 为文档指定根级 `nm` 名称。播放器会将其作为标签渲染在画布上方，并将其公开到智能体上下文中（参见下方的 `/__context`）。

## 公开可编辑属性（插槽 + 属性面板）

应用可以渲染实时**属性面板**（文本输入框和滑块），实时编辑动画中选定的值。它基于 Skottie 原生的**插槽**功能——无需重新解析，更改会在下一帧显示。

要使属性可编辑，请执行两项操作：

**1. 在 Lottie JSON 中声明插槽。** 添加顶层 `"slots"` 对象，其键为插槽 ID，并使用 `"sid"`（替代或配合内联值）将属性指向某个插槽。插槽的 `"p"` 保存默认值，其结构与该属性通常采用的结构相同。

```jsonc
{
  "v": "5.7.0", "fr": 60, "ip": 0, "op": 90, "w": 512, "h": 512, "assets": [],
  "slots": {
    "ballColor": { "p": { "a": 0, "k": [0.231, 0.6, 1, 1] } },   // 颜色：RGBA 0–1
    "ballSize":  { "p": { "a": 0, "k": 120 } }                    // 标量
  },
  "layers": [ /* ... */
    // 在填充中：    "c": { "sid": "ballColor" }
    // 在标量中：    "s": { "sid": "ballSize" }
  ]
}
```

插槽类型与控件的对应关系如下：

| 插槽值 | 渲染的控件 |
|------------|------------------|
| 标量（单个数字） | 滑块 |
| 颜色（RGBA 0–1） | 颜色选择器 |
| vec2（`[x, y]`） | 两个数字输入框 |
| 文本（字符串） | 文本输入框 |

应用会通过 Skottie 的 `getSlotInfo()` 自动发现插槽——你**不需要**在其他任何位置列出它们即可使其工作。动画只要声明至少一个插槽，面板就会出现。

**你制作的每个动画都必须为背景颜色公开至少一个控件。**


```jsonc
// slots:    "bgColor": { "p": { "a": 0, "k": [1, 1, 1, 1] } }   // 默认白色
// controls: { "sid": "bgColor", "label": "Background color" }
```


**2.（可选）在场景的 `controls.json` 中描述展示方式。** 插槽只公开 ID 和类型，不包含标签或合理的滑块范围。场景的 `lottie.json` 旁边的伴随文件（即 `public/projects/<project>/<scene-N>/controls.json`）可补充这些信息。它是可选的——缺失的条目会回退到插槽 ID 和通用的 0–100 范围。

```jsonc
{
  "controls": [
    { "sid": "ballColor", "label": "Ball color" },
    { "sid": "ballSize",  "label": "Ball size", "min": 40, "max": 240, "step": 1 }
  ]
}
```

- `sid` 必须与插槽 ID 完全匹配。
- `label` 是显示名称；`min`/`max`/`step` 用于设置标量滑块和 vec2 输入框（对颜色或文本无效）。
- `sid` 未匹配任何插槽的条目会被直接忽略；没有对应条目的插槽仍会使用默认值渲染。

## 用户可以创建或编辑的场景

播放器是实时编辑器，因此场景的 `lottie.json` 不仅是输入——**用户（以及 UI）可能会在你不知情的情况下更改它：**

- 可以通过侧边栏的 `+` 按钮、将 `.json`/`.lottie` 文件拖放到画布，或由你在磁盘上创建文件夹来添加**新项目或场景**。监视器会实时更新树，因此你在 `public/projects/<project>/<scene-N>/` 下写入的文件夹无需重启即可显示。
- **控件编辑会写回磁盘。** 当用户拖动滑块或编辑使用插槽的值时，应用会将更新后的文档 POST 到 `/__scenes/lottie`，并覆盖该场景的 `lottie.json`——`public/projects` 是事实来源。因此，在重新编辑文件之前，请**从磁盘重新读取它**，不要信任之前的副本；屏幕上的值可能已经不同。

当你想写入或修改场景时，只需将 `lottie.json` 文件写入正确路径（结构见上文）。如果用户指定了现有场景，请使用该场景；否则，请使用下一个 `scene-<N>` 索引创建新场景文件夹，以免覆盖用户的工作。

**对于新项目，覆盖 `public/projects/main-project/scene-1/lottie.json` 中的占位场景。**

## 检查正在播放的内容——`/__context`

开发服务器在 `GET /__context` 提供一个**上下文端点**。优先使用此端点，而不是根据截图猜测：它会返回完整的项目和场景树（包含 `lastModified` 修改时间）、哪个场景处于**活动**状态，以及**实时播放状态**——包括根据已用时间计算出的当前帧：

```bash
curl -s http://localhost:3030/__context
```

用它确认文件是否已写入（场景是否出现？）、查看用户当前正在查看哪个场景，以及无需截图即可检查播放头位置。浏览器会向同一端点 POST 心跳——你无需进行 POST。

## 控制播放

通过浏览器工具操作页面时，请**在 URL 中固定帧**并读取画布：

```
http://localhost:3030/main-project/scene-1?frame=60
```

- `?frame=N` 会在加载时跳转到帧 `N`，**并暂停**在那里，使画面保持静止以供截图。这是检查特定帧并截图的正确方式。
- 如果没有 `frame` 参数，动画会像平常一样自动播放（首次加载时）。
- 帧设置按场景生效，因此请包含场景路径：`/<project>/<scene>?frame=N`。

要更改检查的帧，请导航到新的 URL（或编辑查询字符串并重新加载）。画布是 `<canvas id="main-canvas">`。如果画布为空，则页面尚未完成加载，或 Lottie 解析失败（检查屏幕上的错误）。

## 验证建议

通过 URL 进行验证：`?frame=N` 会跳转并暂停，因此每张截图都会准确落在一个静止帧上。从 `GET /__context`（`live.totalFrames`）读取帧数，或根据 `op` 和 `fr` 计算。

- **新场景 → 三张跨越时间线的截图**：帧 `0`、中点（`op/2`）以及最后一帧（`op-1`）。这样可以一次检查起始状态、运动中途和结束姿态。
- **小幅编辑 → 一至两张截图**，截取相关区域（更改可见的帧）。无需重新执行完整的三帧检查。
- **寻找瑕疵，而不仅仅检查是否符合提示词。** 除了“是否符合要求”，还要查找会让输出显得未完成的问题。结果应整洁、有明确设计意图，并达到生产就绪水平。

## 最佳实践

- 优先制作高保真、可用于生产的动画。
- 使用适当的缓动和时序。线性缓动通常不是最佳选择。
- 考虑整体动效设计，包括节奏、过渡和视觉连续性。
- 选择最适合任务的实现方式。
  - 对于复杂或程序化动画，在 `script/` 中创建脚本来生成 Lottie 文件可能更简单且更易维护。
  - 对于针对性修改，直接修改 Lottie JSON 可能比重新创建动画更高效。

## 完成前——检查清单

1. 文件位于 `public/projects/<project>/<scene-N>/lottie.json`（遵循文件夹结构；场景命名为 `scene-<N>` 以确保正确排序）。
2. 文件是有效的 JSON（无注释、无尾随逗号）。使用 `node -e "JSON.parse(require('fs').readFileSync('public/projects/<project>/<scene-N>/lottie.json','utf8'))"` 验证。
3. 项目是官方 GitHub 播放器（通过 degit 创建）。
4. 开发服务器正在运行（`npm run dev`）；导航到 `/<project>/<scene>` 查看场景。画布为空（无错误）→ 重新检查组包装。
5. 画布正在渲染所需动画。

## 参考资料

- Lottie 格式规范：<https://github.com/lottie/lottie-spec/tree/main/docs/specs>
