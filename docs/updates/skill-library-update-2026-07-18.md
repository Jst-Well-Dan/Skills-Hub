# Skill 库同步更新说明（2026-07-18）

本次检查并同步了 30 个 GitHub 上游项目，其中 15 个项目存在有效更新。同步后目录包含 31 个项目、315 个 skills；本轮净增 8 个 skills。

> 内容概览依据各上游仓库的 commit 标题和变更文件整理。对于只跟踪子目录的项目，仅说明实际进入本库的变更。

## 项目更新概览

| 项目 | 提交范围 | Skill 数量 | 主要更新 |
| --- | --- | ---: | --- |
| `agent-browser` | `7379f7d` → `6ede7a9`（16） | 7 → 7 | 发布 v0.31.2 至 v0.32.2；增加状态定期保存、WebGPU 启动预设和新版 eve 扩展；修复 WebRTC 域名白名单绕过与页面等待逻辑。 |
| `agent-skills` | `1356046` → `1ad9aae`（2） | 2 → 2 | Supabase skill 增加声明式 schema 管理说明，并更新两个 skill 的变更日志。 |
| `anthropic` | `5754626` → `fa0fa64`（3） | 18 → 18 | Claude API 文档按 SDK 拆分，补充 Claude Sonnet 5、Managed Agents 与平台能力；同步更新 DOCX、PPTX、XLSX 工作流及脚本。 |
| `baoyu-skills` | `348dc82` → `6b7a2e4`（4） | 21 → 21 | 修复 X Articles 中紧贴中文的粗体/斜体渲染；微信总结增加归因校验、群主查证、记忆留痕、初始化说明，并调整输出顺序。 |
| `context7-cli` | `0647bb3` → `23843e9`（19） | 1 → 1 | 本库跟踪的 `references/docs.md` 改进查询建议：一个查询聚焦一个主题，并补充“过宽查询”的反例。 |
| `guizang-social-card-skill` | `032782f` → `cf4b810`（4） | 1 → 1 | 新增 Live Photo 生产规则、平台限制、拼图与长视频处理、发布提醒；加入打包、元数据、视频联系表和文档检查脚本。 |
| `html-anything` | `8fd5227` → `d0efb1e`（5） | 78 → 81 | 新增 `article-sketchnote-editorial`、`deck-ljg-present`、`info-funnel` 三个 HTML 模板 skill。 |
| `impeccable` | `d2ab4dd` → `8967edc`（68） | 1 → 1 | 增加 iOS/Android 及 native audit/adapt 指南；强化项目初始化上下文、设计检测和 CLI；修复 Node 22、嵌套目标与文档 UI 问题，并加入 OpenAI plugin 提交包。 |
| `kami` | `594bfb8` → `f97bfc9`（17） | 2 → 2 | 发布 1.9.3/1.9.4；统一多类模板占位提示，强化 PDF/测试检查；加入仓库级维护图表流程和大量 diagram 示例，并补充落地页布局规则。 |
| `ljg-skills` | `52d8ac2` → `df4e2ff`（42） | 23 → 21 | 新增 `ljg-blind`、`ljg-constraint`、`ljg-structure`；移除 `ljg-paper-flow`、`ljg-paper-river`、`ljg-skill-map`、`ljg-travel`、`ljg-word-flow`；同时更新 book、card、paper、present、push、roundtable 等技能。 |
| `lottie` | `a4e20b8` → `d8973f9`（38） | 1 → 1 | `text-to-lottie` 增加动画设计、播放器契约、文字槽位、镜头/图表/Logo/UI 动效等参考与评测数据；修复 seek 边界和内存清理问题。 |
| `mattpocock-skills` | `7a83a3a` → `9603c1c`（121） | 36 → 41 | 新增 research、to-spec、to-tickets、batch-grill-me、claude-handoff、setup-ts-deep-modules、to-questionnaire；移除 to-issues、to-prd；补充 Codex 元数据、Claude plugin 与工程工作流更新。 |
| `notebooklm` | `5b4c57e` → `8f3cd95`（201） | 1 → 1 | 推进 v0.8.0；文档跟进 Gemini Notebook 品牌调整；新增 Docker/Compose 部署；修复 MCP OAuth 状态隔离、来源标题导入和服务版本溯源等问题。 |
| `punk-skill` | `08d4226` → `288376c`（14） | 2 → 2 | `punk-cover` 新增黑红剪影、先锋复古建筑、油墨点阵、现代主义、银色锡纸、构成主义、日式科幻、法式极简和品牌协同等封面风格，并更新校验脚本与风格目录。 |
| `swyxio-skills` | `b5bf58c` → `0ab390e`（6） | 39 → 41 | 新增 `reserved-handle-policy` 和 `youtube-studio-computer-use`；改进 YouTube Studio 弹窗等待与批量上传元数据边界说明。 |

## Skill 增删汇总

- 新增 15 个：HTML Anything 3 个、LJG 3 个、Matt Pocock 7 个、Swyx 2 个。
- 移除 7 个：LJG 5 个、Matt Pocock 2 个。
- 净增加 8 个，目录总数由 307 增至 315。

## 同步说明

- 15 个项目均已同步到对应的 `libraries/`。
- 完整仓库快照改用浅克隆，后续可直接快进更新；子目录项目继续只下载被跟踪路径。
- `content-research-writer` 的上游分支配置已由无效的 `main` 修正为实际默认分支 `master`；该项目本轮内容无变化。
- `punk-skill` 首次下载遇到 GitHub EOF，重试后同步成功。
