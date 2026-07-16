<!-- source-sha256: 20f4041c098154f583bf48d543b52cecaaea0a62cbc62dc11e2b4fc5b23c0197 -->
---
name: vercel-sandbox
description: 在 Vercel Sandbox microVM 中运行 agent-browser + Chrome，以便从任何部署到 Vercel 的应用执行浏览器自动化。当用户需要在 Vercel 应用（Next.js、SvelteKit、Nuxt、Remix、Astro 等）中实现浏览器自动化、希望运行不受二进制文件大小限制的无头 Chrome、需要在多条命令之间保持浏览器会话，或需要临时隔离的浏览器环境时使用。触发词包括 "Vercel Sandbox browser"、"microVM Chrome"、"agent-browser in sandbox"、"browser automation on Vercel"，或任何需要在 Vercel Sandbox 中使用 Chrome 的任务。
---

# 使用 Vercel Sandbox 进行浏览器自动化

在临时 Vercel Sandbox microVM 中运行 agent-browser + 无头 Chrome。Linux VM 按需启动、执行浏览器命令，然后关闭。适用于任何部署到 Vercel 的框架（Next.js、SvelteKit、Nuxt、Remix、Astro 等）。

## 依赖项

```bash
pnpm add @agent-browser/sandbox @vercel/sandbox
```

沙箱 VM 需要 Chromium 的系统依赖项以及 agent-browser 本身。对于新沙箱，`@agent-browser/sandbox` 辅助函数默认会安装它们，并使用沙箱快照（见下文）实现亚秒级启动。仅当沙箱镜像已提供 Chromium 所需的库时，才传入 `installSystemDependencies: false`。

## 核心模式

```ts
import {
  createAgentBrowserSnapshot,
  runAgentBrowserCommand,
  withAgentBrowserSandbox,
  type VercelSandboxSession,
} from "@agent-browser/sandbox/vercel";

async function withBrowser<T>(
  fn: (sandbox: VercelSandboxSession) => Promise<T>,
): Promise<T> {
  return withAgentBrowserSandbox(fn);
}
```

## 截图

`screenshot --json` 命令会将截图保存到文件并返回其路径。以 base64 格式读回该文件：

```ts
export async function screenshotUrl(url: string) {
  return withBrowser(async (sandbox) => {
    await runAgentBrowserCommand(sandbox, ["open", url]);

    const titleResult = await runAgentBrowserCommand<{ data?: { title?: string } }>(sandbox, [
      "get", "title",
    ]);
    const title = titleResult.json?.data?.title || url;

    const ssResult = await runAgentBrowserCommand<{ data?: { path?: string } }>(sandbox, [
      "screenshot",
    ]);
    const ssPath = ssResult.json?.data?.path;
    if (!ssPath) throw new Error("Screenshot did not return a file path.");
    const b64Result = await sandbox.runCommand("base64", ["-w", "0", ssPath]);
    const screenshot = (await b64Result.stdout()).trim();

    await runAgentBrowserCommand(sandbox, ["close"], { json: false });

    return { title, screenshot };
  });
}
```

## 无障碍快照

```ts
export async function snapshotUrl(url: string) {
  return withBrowser(async (sandbox) => {
    await runAgentBrowserCommand(sandbox, ["open", url]);

    const titleResult = await runAgentBrowserCommand<{ data?: { title?: string } }>(sandbox, [
      "get", "title",
    ]);
    const title = titleResult.json?.data?.title || url;

    const snapResult = await runAgentBrowserCommand(sandbox, ["snapshot", "-i", "-c"], {
      json: false,
    });

    await runAgentBrowserCommand(sandbox, ["close"], { json: false });

    return { title, snapshot: snapResult.stdout };
  });
}
```

## 多步骤工作流

沙箱会在多条命令之间保持状态，因此可以运行完整的自动化序列：

```ts
export async function fillAndSubmitForm(url: string, data: Record<string, string>) {
  return withBrowser(async (sandbox) => {
    await runAgentBrowserCommand(sandbox, ["open", url]);

    const snapResult = await runAgentBrowserCommand(sandbox, ["snapshot", "-i"], {
      json: false,
    });
    const snapshot = snapResult.stdout;
    // Parse snapshot to find element refs...

    for (const [ref, value] of Object.entries(data)) {
      await runAgentBrowserCommand(sandbox, ["fill", ref, value]);
    }

    await runAgentBrowserCommand(sandbox, ["click", "@e5"]);
    await runAgentBrowserCommand(sandbox, ["wait", "--load", "networkidle"]);

    const ssResult = await runAgentBrowserCommand<{ data?: { path?: string } }>(sandbox, [
      "screenshot",
    ]);
    const ssPath = ssResult.json?.data?.path;
    if (!ssPath) throw new Error("Screenshot did not return a file path.");
    const b64Result = await sandbox.runCommand("base64", ["-w", "0", ssPath]);
    const screenshot = (await b64Result.stdout()).trim();

    await runAgentBrowserCommand(sandbox, ["close"], { json: false });

    return { screenshot };
  });
}
```

## 沙箱快照（快速启动）

**沙箱快照**是 Vercel Sandbox 的已保存 VM 镜像，其中已安装系统依赖项 + agent-browser + Chromium。可以将它理解为 Docker 镜像：沙箱无需每次都从头安装依赖项，而是直接从预构建镜像启动。

这与 agent-browser 的*无障碍快照*功能（`agent-browser snapshot`）无关，后者会导出页面的无障碍树。沙箱快照是用于快速启动 VM 的 Vercel 基础设施概念。

如果没有沙箱快照，每次运行都要安装系统依赖项 + agent-browser + Chromium（约 30 秒）。使用快照后，启动时间可缩短至一秒以内。

### 创建沙箱快照

快照必须包含系统依赖项（通过 `dnf` 安装）、agent-browser 和 Chromium：

```ts
const snapshotId = await createAgentBrowserSnapshot();
```

运行一次，然后设置环境变量：

```bash
AGENT_BROWSER_SNAPSHOT_ID=snap_xxxxxxxxxxxx
```

演示应用中提供了辅助脚本：

```bash
npx tsx examples/environments/scripts/create-snapshot.ts
```

建议任何使用 Sandbox 模式的生产部署都采用此方式。

## 身份验证

在 Vercel 部署中，Sandbox SDK 会通过 OIDC 自动进行身份验证。对于本地开发或需要显式控制的场景，请设置：

```bash
VERCEL_TOKEN=<personal-access-token>
VERCEL_TEAM_ID=<team-id>
VERCEL_PROJECT_ID=<project-id>
```

这些变量会被展开传入 `Sandbox.create()` 调用。如果未设置，SDK 会回退使用 `VERCEL_OIDC_TOKEN`（在 Vercel 上自动提供）。

## 定时工作流（Cron）

与 Vercel Cron Jobs 结合，用于执行周期性浏览器任务：

```ts
// app/api/cron/route.ts  (or equivalent in your framework)
export async function GET() {
  const result = await withBrowser(async (sandbox) => {
    await sandbox.runCommand("agent-browser", ["open", "https://example.com/pricing"]);
    const snap = await sandbox.runCommand("agent-browser", ["snapshot", "-i", "-c"]);
    await sandbox.runCommand("agent-browser", ["close"]);
    return await snap.stdout();
  });

  // Process results, send alerts, store data...
  return Response.json({ ok: true, snapshot: result });
}
```

```json
// vercel.json
{ "crons": [{ "path": "/api/cron", "schedule": "0 9 * * *" }] }
```

## 环境变量

| 变量 | 是否必需 | 说明 |
|---|---|---|
| `AGENT_BROWSER_SNAPSHOT_ID` | 否（但建议使用） | 用于实现亚秒级启动的预构建沙箱快照 ID（见上文） |
| `VERCEL_TOKEN` | 否 | Vercel 个人访问令牌（用于本地开发；在 Vercel 上会自动使用 OIDC） |
| `VERCEL_TEAM_ID` | 否 | Vercel 团队 ID（用于本地开发） |
| `VERCEL_PROJECT_ID` | 否 | Vercel 项目 ID（用于本地开发） |

## 框架示例

此模式在各个框架中的工作方式完全相同，唯一的区别是服务器端代码的放置位置：

| 框架 | 服务器代码位置 |
|---|---|
| Next.js | Server actions、API routes、route handlers |
| SvelteKit | `+page.server.ts`、`+server.ts` |
| Nuxt | `server/api/`、`server/routes/` |
| Remix | `loader`、`action` 函数 |
| Astro | `.astro` frontmatter、API routes |

## 示例

有关采用 Vercel Sandbox 模式的可运行应用，请参阅 agent-browser 仓库中的 `examples/environments/`，其中包括沙箱快照创建脚本、流式进度 UI 和速率限制。
