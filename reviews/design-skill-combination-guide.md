---
{"title":"Taste 与 Impeccable UI 设计组合指南","type":"comparison","related_projects":["impeccable","taste-skill"]}
---
# Taste 与 Impeccable UI 设计组合指南

Taste 和 Impeccable 都能改善前端界面，但它们并不是两套应该完整叠加的平行流程。

Taste 是由 13 个可独立安装 skill 组成的视觉工具箱，重点是审美方向、品牌感、反模板化、图像生成和图片驱动实现。Impeccable 在 Skills-Hub 中只有一个可安装的 `impeccable` skill，内部通过 `shape`、`craft`、`critique`、`audit`、`polish` 等命令完成产品设计与工程质量流程；这些命令不是独立安装的 skill。

> 推荐分工：Impeccable 管产品上下文、UX、复杂状态和工程质量；Taste 管视觉方向、品牌与参考图，以及营销页面的反模板化实现。

## 1. 总体定位

| 合集 | 核心角色 | 优势范围 | 更适合的界面 |
|---|---|---|---|
| Taste | 视觉导演和图像优先工具箱 | 审美方向、品牌视觉、营销页面、风格强化、视觉稿和图片还原 | Landing Page、品牌官网、作品集、营销页面和视觉改版 |
| Impeccable | 产品设计师和交付质量负责人 | 产品上下文、信息架构、复杂状态、设计系统、UX 评审、可访问性、适配和性能 | Dashboard、后台、工具、表单、设置、Onboarding 和复杂产品 UI |

当两者规则冲突时：

- 营销页、品牌页和作品集由 Taste 主导视觉方向。
- Dashboard、后台、工具和多步骤流程由 Impeccable 主导 UX 和实现。
- 已有品牌 token、组件库和设计系统优先于两个合集的默认偏好。

## 2. 能力重合关系

| Taste skill | 对应的 Impeccable 能力 | 重合程度 | 主要区别 |
|---|---|---:|---|
| `design-taste-frontend` V2 | `shape`、`craft`、`layout`、`typeset`、`colorize`、`animate`、`audit` | 高 | V2 偏营销页、品牌页和作品集；Impeccable 可以处理产品 UI、Dashboard、表单和复杂状态 |
| `redesign-existing-projects` | `critique` → `audit` → `polish` | 高 | Taste 用一个流程完成视觉审计和改版；Impeccable 将 UX 评价、技术检查和最终修整拆开 |
| `high-end-visual-design` | `bolder`、`delight`、`typeset`、`layout`、`animate` | 高 | Taste 提供固定的高端机构风格；Impeccable 根据现有设计系统逐项增强 |
| `minimalist-ui` | `quieter`、`distill`、`typeset`、`layout` | 高 | Taste 是具体的极简视觉配方；Impeccable 是对当前界面降噪和精简 |
| `industrial-brutalist-ui` | `bolder`、`overdrive`、`layout`、`typeset` | 中 | Impeccable 可以增强视觉强度，但没有完整的瑞士工业或战术终端固定语言 |
| `gpt-taste` | `overdrive`、`bolder`、`animate`、`delight` | 中高 | `gpt-taste` 是更激进、更强动效的固定路线；Impeccable 会先判断这种强度是否适合用户任务 |
| `image-to-code` | `shape` 的视觉方向探索 + `craft` | 中 | Impeccable 可以参考视觉稿实现，但没有固定的“生成图 → 分析 → 编码”协议 |
| `stitch-design-taste` | `init`、`document`、`extract` | 高 | 两者都能建立 `DESIGN.md`；Impeccable 更强调从真实代码和 token 提取系统 |
| `imagegen-frontend-mobile` | `shape`、`adapt` 和平台规范 | 低 | Taste 输出移动端参考图；Impeccable 设计、实现并检查真实界面 |
| `full-output-enforcement` | Impeccable 的完整交付要求 | 低 | Impeccable 没有单独的防截断命令 |

### 2.1 Taste 基本没有对应能力的部分

- `brandkit`：生成 Logo、字体、色板和应用场景组成的品牌视觉板。
- `imagegen-frontend-web`：为网站每个 section 生成独立参考图。
- `imagegen-frontend-mobile`：专门生成移动端屏幕图和流程图。
- `full-output-enforcement`：专门处理对话输出截断。
- `design-taste-frontend-v1`：旧版兼容，不应进入新项目的默认流程。

### 2.2 Impeccable 独有或明显更完整的部分

- `clarify`：UX 文案、错误消息、表单标签和 CTA。
- `onboard`：首次使用、引导、空状态和激活流程。
- `harden`：极端输入、错误状态、国际化、RTL、CJK 和边界条件。
- `adapt`：响应式、触控、不同设备及原生平台适配。
- `optimize`：性能诊断和 Core Web Vitals。
- `critique`：带启发式评分的 UX 评价。
- `live`：在浏览器中选择元素并生成视觉变体。
- `extract`：把重复组件和硬编码样式提炼成设计系统。
- 产品 UI、Dashboard、复杂表单和多状态界面的完整处理。

## 3. 完整 UI 工作流

正常流程不应把两个合集的所有能力串起来。每个阶段只选一个主能力，专项 skill 只在问题确实存在时介入。

### 阶段一：建立产品上下文

新项目首先运行：

```text
/impeccable init
```

它负责建立 `PRODUCT.md`、初始 `DESIGN.md`、目标用户、平台、品牌性格和设计原则。

已有代码但缺少设计文档时使用：

```text
/impeccable document
```

当重复组件和硬编码值已经很多，才继续使用：

```text
/impeccable extract
```

`document` 负责记录现有系统，`extract` 负责真正提炼 token 和共享组件。它们不是每个项目都必须连续执行。

### 阶段二：补充品牌资产，可选

项目没有品牌方向，并且确实需要 Logo、字体、色板和视觉应用板时使用：

```text
Taste: brandkit
```

完成后把选定的资产和规则写回 `DESIGN.md`。已有成熟品牌时跳过这一阶段。

### 阶段三：设计 UX 和信息架构

需要在编码前确认页面目标、用户路径、内容、状态和交互时使用：

```text
/impeccable shape <功能或页面>
```

如果不需要单独审批方案，可以直接使用：

```text
/impeccable craft <功能或页面>
```

`craft` 已包含 shape 和实现流程。通常在 `shape` 与 `craft` 中二选一；只有需要先确认设计 brief 时，才使用 `shape → craft`。

### 阶段四：选择视觉路线

营销页、品牌页和作品集优先使用：

```text
Taste: design-taste-frontend V2
```

视觉方向已经明确时，最多附加一个风格 skill：

```text
high-end-visual-design
或 minimalist-ui
或 industrial-brutalist-ui
```

明确需要更激进、更强动效的实验性营销路线时，可以使用：

```text
gpt-taste
```

`gpt-taste` 应视为 V2 的更严格替代方案，不建议与 V2 同时完整加载。

Dashboard、后台、设置页和复杂表单则由 Impeccable `craft` 主导，不应以 Taste V2 作为主要实现技能。

### 阶段五：决定是否需要视觉参考图

没有参考图需求时直接跳过。

只需要网站视觉稿：

```text
Taste: imagegen-frontend-web
```

只需要移动端屏幕和流程图：

```text
Taste: imagegen-frontend-mobile
```

需要从参考图一直做到代码：

```text
Taste: image-to-code
```

使用 `image-to-code` 后，不需要再完整运行 `imagegen-frontend-web → design-taste-frontend → impeccable craft`，否则会重复设计和实现。

### 阶段六：选择一个主实现能力

| 界面类型 | 主实现能力 |
|---|---|
| 营销页、品牌页、作品集 | Taste `design-taste-frontend` V2 |
| 产品 UI、Dashboard、表单和设置页 | Impeccable `craft` |
| 严格依照生成图实现 | Taste `image-to-code` |

不要让 V2、`image-to-code` 和 `craft` 各自重新设计同一页面。

### 阶段七：UX 与技术检查

实现完成后依次使用：

```text
/impeccable critique <页面>
→ /impeccable audit <页面>
```

- `critique` 检查信息架构、认知负担、视觉层级、情绪体验和启发式原则。
- `audit` 检查可访问性、性能、响应式和技术质量。

如果已经完整使用 `redesign-existing-projects` 做过同类审计，可以只在最终阶段使用 Impeccable 验证，不必马上重复全套检查。

### 阶段八：根据问题专项修复

| 检查发现 | 使用 |
|---|---|
| 布局、留白和层级问题 | `/impeccable layout` |
| 字体和阅读层级问题 | `/impeccable typeset` |
| 色彩单调或对比度问题 | `/impeccable colorize` |
| 动效不足或状态变化生硬 | `/impeccable animate` |
| 页面太吵 | `/impeccable quieter` 或 `distill` |
| 页面太保守 | `/impeccable bolder` 或 `delight` |
| 文案和错误消息不清楚 | `/impeccable clarify` |
| 缺少空状态和首次使用体验 | `/impeccable onboard` |
| 响应式或设备适配问题 | `/impeccable adapt` |
| 错误、国际化和边界状态 | `/impeccable harden` |
| 性能问题 | `/impeccable optimize` |

不要机械执行全部命令，只处理 `critique` 和 `audit` 实际发现的问题。

### 阶段九：最终交付

```text
/impeccable polish <页面>
```

`polish` 是最后一步，用于统一设计系统漂移、间距、字体、颜色、交互状态、图片、表单和细节一致性。

只有模型在对话中持续截断完整代码时，才附加：

```text
Taste: full-output-enforcement
```

## 4. 推荐的精简调用链

### 普通产品 UI

```text
Impeccable init
→ Impeccable shape 或 craft
→ Impeccable critique
→ Impeccable audit
→ harden / adapt / optimize（按检查结果）
→ Impeccable polish
```

Taste 通常只在品牌板或特殊视觉方向阶段介入。

### 营销网站

```text
Impeccable init
→ Impeccable shape
→ Taste design-taste-frontend V2
→ Impeccable critique
→ Impeccable audit
→ Impeccable polish
```

### 图像驱动网站

```text
Impeccable init
→ Impeccable shape
→ Taste image-to-code
→ Impeccable critique
→ Impeccable audit
→ Impeccable polish
```

### 已有项目改版

二选一：

```text
Taste redesign-existing-projects
→ Impeccable audit
→ Impeccable polish
```

或者：

```text
Impeccable critique
→ Impeccable audit
→ 对应专项修复
→ Impeccable polish
```

## 5. 避免重复调用

- 不要同时让 V2、`image-to-code` 和 `craft` 各自设计并实现同一页面。
- 不要把 `high-end-visual-design`、`minimalist-ui` 和 `industrial-brutalist-ui` 同时叠加。
- 不要把 `gpt-taste` 与 V2 当成必须同时加载的组合。
- 不要在没有视觉稿需求时运行图像生成 skill。
- 不要在 `redesign-existing-projects` 完成审计后，立刻重复一套同范围评审。
- 不要把 `audit`、`harden`、`adapt`、`optimize` 和 `polish` 视为固定流水线；除最终 `polish` 外，其余按问题选择。

## 6. 最终建议

最稳定的组合方式不是“两个合集全部开启”，而是：

```text
Impeccable 定义产品和 UX
→ Taste 在需要时确定视觉方向或生成参考图
→ 选择一个主技能完成实现
→ Impeccable 完成评审、专项修复和交付检查
```

营销和品牌页面可以让 Taste 主导中间的视觉与实现阶段；产品 UI、Dashboard、表单和复杂流程应让 Impeccable 从设计到实现全程主导。这样既能获得 Taste 的视觉差异化，也不会牺牲 Impeccable 对复杂状态、可访问性、适配和生产质量的控制。
