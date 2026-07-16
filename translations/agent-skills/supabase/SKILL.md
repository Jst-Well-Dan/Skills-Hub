<!-- source-sha256: 1171386737b231610fa42485707272765c3516a9bbc0bd2c6c161a8cee3d7d33 -->
---
name: supabase
description: "用于处理任何涉及 Supabase 的任务。触发条件：Supabase 产品（Database、Auth、Edge Functions、Realtime、Storage、Vectors、Cron、Queues）；Next.js、React、SvelteKit、Astro、Remix 中的客户端库和 SSR 集成（supabase-js、@supabase/ssr）；身份验证问题（登录、退出、会话、JWT、Cookie、getSession、getUser、getClaims、RLS）；Supabase CLI 或 MCP 服务器；架构变更、迁移、安全审计、Postgres 扩展（pg_graphql、pg_cron、pg_vector）。"
metadata:
  author: supabase
  version: "0.1.2"
---

# Supabase

## 核心原则

**1. Supabase 变化频繁——实施前请对照变更日志和当前文档进行验证。**
不要依赖训练数据来判断 Supabase 功能。函数签名、config.toml 设置和 API 约定会随版本变化。

首先，获取 `https://supabase.com/changelog.md`（一个轻量级摘要索引——不会产生大量数据拉取），扫描与任务相关的 `breaking-change` 标签，并查看其中任何适用条目所链接的页面。然后，使用下述文档访问方式查找相关主题。

**2. 验证你的工作。**
实施任何修复后，运行测试查询以确认变更有效。未经验证的修复是不完整的。

**3. 从错误中恢复，不要循环重试。**
如果一种方法尝试 2-3 次后仍然失败，请停止并重新考虑。尝试其他方法、查阅文档、更仔细地检查错误，并在日志可用时查看相关日志。Supabase 问题不一定能通过反复执行同一命令来解决，答案也不一定总在日志中，但在继续之前通常值得检查日志。

**4. 向 Data API 公开表：** 根据用户的 [Data API 设置](https://supabase.com/dashboard/project/<ref>/integrations/data_api/settings)，新创建的表可能不会自动通过 Data（REST）API 公开。如果属于这种情况，则需要显式授予 `anon` 和 `authenticated` 角色访问权限。

> 请注意，这与 RLS 不同。RLS 控制表可访问后哪些_行_可见，而不是控制表本身是否可访问。

当用户报告通过 SQL 创建的表意外无法访问时，请检查其 Data API 设置，以及是否已经通过显式的 `GRANT` SQL 授予相关角色访问权限。授予公共（`anon`/`authenticated`）访问权限时，也必须始终启用 RLS。完整设置流程请参阅[向 Data API 公开表](https://supabase.com/docs/guides/api/securing-your-api.md)。

**5. 已公开架构中的 RLS。**
对任何已公开架构中的每张表启用 RLS，默认情况下这包括 `public`。这一点在 Supabase 中至关重要，因为当 `anon`/`authenticated` 角色拥有访问权限时，已公开架构中的表可以通过 Data API 访问（参见[向 Data API 公开表](https://supabase.com/docs/guides/api/securing-your-api.md)）。对于私有架构，建议将 RLS 作为纵深防御。启用 RLS 后，应创建符合实际访问模型的策略，而不是默认对每张表使用相同的 `auth.uid()` 模式。

**6. 安全检查清单。**
处理任何涉及身份验证、RLS、视图、存储或用户数据的 Supabase 任务时，请逐项检查此清单。以下是 Supabase 特有、可能在不知不觉中造成漏洞的安全陷阱：

- **身份验证和会话安全**
  - **绝不要在基于 JWT 的授权决策中使用 `user_metadata` 声明。** 在 Supabase 中，`raw_user_meta_data` 可由用户编辑，并且可能出现在 `auth.jwt()` 中，因此不能安全地用于 RLS 策略或任何其他授权逻辑。请改为将授权数据存储在 `raw_app_meta_data` / `app_metadata` 中。
  - **删除用户不会使现有访问令牌失效。** 应先退出或撤销会话；对于敏感应用，应缩短 JWT 有效期；若需要严格保证，则应在敏感操作中对照 `auth.sessions` 验证 `session_id`。
  - **如果使用 `app_metadata` 或 `auth.jwt()` 进行授权，请记住，在用户令牌刷新前，JWT 声明不一定是最新的。**

- **API 密钥和客户端暴露**
  - **绝不要在公共客户端中暴露 `service_role` 或 secret key。** 前端代码应优先使用 publishable key。旧版 `anon` key 仅用于兼容。在 Next.js 中，任何 `NEXT_PUBLIC_` 环境变量都会发送到浏览器。

- **RLS、视图和特权数据库代码**
  - **默认情况下，视图会绕过 RLS。** 在 Postgres 15 及更高版本中，使用 `CREATE VIEW ... WITH (security_invoker = true)`。在较旧版本的 Postgres 中，通过撤销 `anon` 和 `authenticated` 角色的访问权限来保护视图，或将视图放入未公开的架构。
  - **UPDATE 需要 SELECT 策略。** 在 Postgres RLS 中，UPDATE 首先需要 SELECT 该行。如果没有 SELECT 策略，更新会静默返回 0 行——没有错误，只是不发生任何变化。
  - **`auth.role()` 已弃用——请改用 `TO` 子句。** Supabase 已弃用 `auth.role()`，建议通过 `TO authenticated` 或 `TO anon` 直接在策略上指定目标角色。除了弃用问题外，启用匿名登录时，`auth.role() = 'authenticated'` 还会静默失效，因为匿名用户也具有 `authenticated` Postgres 角色，无论用户是否真正登录都能通过检查。
    ```sql
    -- Deprecated (do not use)
    create policy "example" on table_name for select
    using ( auth.role() = 'authenticated' );
    ```
  - **仅使用 `TO authenticated` 只是身份验证，并不包含授权（BOLA / IDOR）。** 使用 `TO authenticated` 只会检查角色——它不会限制用户能够访问哪些行。正确模式应将 `TO authenticated` 与 `USING` 中的所有权谓词结合：
    ```sql
    create policy "example" on table_name for select
    to authenticated
    using ( (select auth.uid()) = user_id );
    ```
  - **UPDATE 策略同时需要 `USING` 和 `WITH CHECK`。** 如果没有 `WITH CHECK`，用户可以将某行的 `user_id` 重新分配给另一用户：
    ```sql
    create policy "example" on table_name for update
    to authenticated
    using ( (select auth.uid()) = user_id )
    with check ( (select auth.uid()) = user_id );
    ```
  - **`SECURITY DEFINER` 函数会绕过 RLS。** `SECURITY DEFINER` 函数使用其创建者的权限运行——创建者通常是具有 `bypassrls` 权限的角色（例如 `postgres`）。绝不要为了消除权限错误而添加 `SECURITY DEFINER`；这种做法会在不修复根本原因的情况下静默移除访问控制。优先使用 `SECURITY INVOKER`。
  - **`public` 中的 `SECURITY DEFINER` 函数可被所有角色调用。** 默认情况下，Postgres 会为每个新函数向 `PUBLIC` 授予 `EXECUTE` 权限，因此 `public` 中的任何 `SECURITY DEFINER` 函数都是一个公共 API 端点，无需额外授权即可由 `anon` 和 `authenticated`（它们继承自 `PUBLIC`）调用。当确实需要 `SECURITY DEFINER` 时（例如绕过内部查找表的 RLS），请将该函数保存在未公开的架构中，始终在函数体中加入 `auth.uid()` 检查，并在变更后运行 `supabase db advisors`。

- **存储访问控制**
  - **Storage upsert 需要 INSERT + SELECT + UPDATE。** 仅授予 INSERT 可以上传新文件，但文件替换（upsert）会静默失败。三项权限缺一不可。

- **依赖项和供应链安全**
  - 安装 Supabase 软件包（`supabase-js`、`@supabase/ssr`、`supabase-py` 等）时，**始终固定软件包版本并提交锁定文件**。完整检查清单请参阅 [npm 安全指南](https://supabase.com/docs/guides/security/npm-security.md)。

对于上述内容未涵盖的任何安全问题，请获取 Supabase 产品安全索引：`https://supabase.com/docs/guides/security/product-security.md`

## Supabase CLI

始终通过 `--help` 探索命令——绝不要猜测。CLI 结构会随版本变化。

```bash
supabase --help                    # All top-level commands
supabase <group> --help            # Subcommands (e.g., supabase db --help)
supabase <group> <command> --help  # Flags for a specific command
```

**Supabase CLI 已知注意事项：**

- `supabase db query` 需要 **CLI v2.79.0+** → 使用 MCP `execute_sql` 或 `psql` 作为后备方案
- `supabase db advisors` 需要 **CLI v2.81.3+** → 使用 MCP `get_advisors` 作为后备方案
- 需要新的迁移 SQL 文件时，**始终**先使用 `supabase migration new <name>` 创建。绝不要自行编造迁移文件名，也不要凭记忆判断预期格式。

**版本检查和升级：** 运行 `supabase --version` 进行检查。有关 CLI 变更日志和特定版本的功能，请查阅 [CLI 文档](https://supabase.com/docs/reference/cli/introduction)或 [GitHub releases](https://github.com/supabase/cli/releases)。

## Supabase MCP 服务器

有关设置说明、服务器 URL 和配置，请参阅 [MCP 设置指南](https://supabase.com/docs/guides/getting-started/mcp)。

**排查连接问题**——请按顺序执行以下步骤：

1. **检查服务器是否可访问：**
   `curl -so /dev/null -w "%{http_code}" https://mcp.supabase.com/mcp`
   预期会返回 `401`（没有令牌），这表示服务器正在运行。超时或出现 "connection refused" 表示服务器可能已关闭。

2. **检查 `.mcp.json` 配置：**
   确认项目根目录中存在有效的 `.mcp.json`，且服务器 URL 正确。如果缺失，请创建一个指向 `https://mcp.supabase.com/mcp` 的配置。

3. **对 MCP 服务器进行身份验证：**
   如果服务器可访问且 `.mcp.json` 正确，但工具不可见，则用户需要进行身份验证。Supabase MCP 服务器使用 OAuth 2.1——请告知用户在其智能体中触发身份验证流程，在浏览器中完成验证，然后重新加载会话。

## Supabase 文档

实施任何 Supabase 功能之前，请找到相关文档。按以下优先级使用这些方法：

1. **MCP `search_docs` 工具**（首选——直接返回相关片段）
2. **以 Markdown 格式获取文档页面**——在任何文档页面的 URL 路径后附加 `.md` 即可获取。
3. 不知道应查看哪个页面时，使用**网页搜索**查找 Supabase 特定主题。

## 创建并提交架构变更

**要创建架构变更，请使用 `execute_sql`（MCP）或 `supabase db query`（CLI）。** 它们会直接在数据库上运行 SQL，而不会创建迁移历史记录，因此你可以自由迭代，并在准备就绪后生成整洁的迁移。

不要使用 `apply_migration` 修改本地数据库架构——它每次调用都会写入一条迁移历史记录，这意味着你无法迭代，并且 `supabase db diff` / `supabase db pull` 会产生空的或相互冲突的差异。如果使用它，你将被首次传入的 SQL 所束缚。

**准备将**变更提交到迁移文件时：

1. **运行 advisors** → `supabase db advisors`（CLI v2.81.3+）或 MCP `get_advisors`。修复所有问题。
2. 如果变更涉及视图、函数、触发器或存储，请**查看上面的安全检查清单**。
3. **生成迁移** → `supabase db pull <descriptive-name> --local --yes`
4. **验证** → `supabase migration list --local`

## 参考指南

- **Skill 反馈** → [references/skill-feedback.md](references/skill-feedback.md)
  当用户报告此 Skill 提供了错误指导或缺少信息时，**必须阅读**。
