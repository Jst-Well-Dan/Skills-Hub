<!-- source-sha256: f6992fc7332d7b72385d930985457ece5130e7f6f96978d267063459baa63b9b -->
---
name: twitter-x-scraping
description: 适用于通过 Nitter 风格镜像抓取公开的 Twitter/X 时间线或列表，并使用 axios 以及 Playwright 回退方案，包括反机器人挑战处理和分页限制。
---

# Skill：从 Nitter.net 抓取推文

此代码库会抓取 [nitter.net](https://nitter.net)（一个开源 Twitter 前端），以收集指定时间范围内某个列表或个人资料中的推文。此方法无需 Twitter API 密钥即可使用。

## 核心方法

### 1. URL 结构

Nitter 镜像沿用了 Twitter 的 URL 布局：

| 目标 | Nitter 路径 |
|--------|------------|
| Twitter 列表 | `/i/lists/<listId>` |
| 用户资料 | `/<handle>` |
| 分页 | 追加 `?cursor=<cursor>` |

### 2. 获取策略：axios → Playwright 回退

首先使用普通 HTTP（`axios`）。如果 Nitter 返回反机器人挑战页面（通过检测 HTML 中的字符串 `"Verifying your request"`），则在本次运行的剩余过程中永久切换到有头 Playwright/Chrome 会话。

```ts
// challengeSolver.ts — detect challenge
const CHALLENGE_MARKER = 'Verifying your request';
export function isChallengePage(html: string): boolean {
  return html.includes(CHALLENGE_MARKER);
}

// scrapeNitterList.ts — switch modes on detection
if (isChallengePage(html)) {
  useBrowserMode = true;
  const browserHtml = await fetchWithBrowser(url, debug);
  return { html: browserHtml, url };
}
```

### 3. 浏览器反机器人绕过

检测到挑战时，启动真实的系统 Chrome（非无头模式），并抑制自动化特征：

```ts
import { chromium } from 'playwright';

const browser = await chromium.launch({
  channel: 'chrome',
  headless: false,
  args: ['--disable-blink-features=AutomationControlled'],
});

const context = await browser.newContext({ locale: 'en-US' });
await context.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
});

const page = await context.newPage();
await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

// Wait for challenge to auto-resolve
await page.waitForSelector('.timeline-item', { timeout: 30000 });
const html = await page.content();
```

**关键点**：在之后的所有获取操作中复用同一个浏览器/页面实例（单例模式），不要为每一页重新启动。

### 4. 带退避的重试逻辑

对于 HTTP 429 / 502 / 503，使用指数退避最多重试 10 次（基础延迟 2 秒，最大 60 秒），并遵循 `Retry-After` 和 `X-Rate-Limit-Reset` 响应头：

```ts
const maxRetries = 10;
const baseDelayMs = 2000;

for (let attempt = 0; attempt <= maxRetries; attempt++) {
  const res = await axios.get(url, {
    headers: FETCH_HEADERS,
    timeout: 30000,
    validateStatus: (s) => (s >= 200 && s < 400) || s === 429 || s === 502 || s === 503,
  });

  if (res.status === 429 || res.status === 502 || res.status === 503) {
    const ra = res.headers['retry-after'];
    if (ra && /^\d+$/.test(ra)) {
      await sleep(Math.min((parseInt(ra) + 2) * 1000, 5 * 60 * 1000));
      continue;
    }
    const jitter = Math.floor(Math.random() * 250);
    const waitMs = Math.min(baseDelayMs * Math.pow(2, attempt) + jitter, 60_000);
    await sleep(waitMs);
    continue;
  }

  if (res.status === 200) return res.data;
}
```

使用类似浏览器的 User-Agent 请求头：

```ts
const FETCH_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (compatible; MyBot/1.0) Node.js',
  'Accept-Language': 'en-US,en;q=0.9',
  'Accept': 'text/html,application/xhtml+xml',
  'Accept-Encoding': 'gzip, compress, deflate, br',
};
```

### 5. 使用 Cheerio 解析 HTML

Nitter 会在服务端渲染 HTML。使用 `cheerio`（类似 jQuery 的 API）解析它：

```ts
import * as cheerio from 'cheerio';

const $ = cheerio.load(html);

// All tweets on the page
const $items = $('.timeline .timeline-item').filter((_, el) =>
  $(el).find('.tweet-body').length > 0
);

$items.each((_, el) => {
  const $el = $(el);

  // Tweet URL and ID
  const href = $el.find('a.tweet-link').first().attr('href'); // e.g. "/user/status/12345"
  const id = href?.match(/status\/(\d+)/)?.[1];

  // Timestamp — from the `title` attribute of the date link
  const title = $el.find('.tweet-date a').attr('title'); // e.g. "Apr 15, 2026 · 10:00 AM UTC"
  const timestamp = new Date(title?.replace(/\s*[·•]\s*/g, ' ') ?? '');

  // Tweet text
  const text = $el.find('.tweet-content.media-body').text().trim();

  // Author
  const username = $el.find('.tweet-header a.username').attr('title');
  const displayName = $el.find('.tweet-header a.fullname').attr('title');

  // Images
  $el.find('.attachments .attachment.image').each((_, img) => {
    const src = $(img).find('img').attr('src');  // relative URL
    const fullSrc = `https://nitter.net${src}`;
  });

  // Engagement stats
  $el.find('.tweet-stats .tweet-stat').each((_, stat) => {
    const icon = $(stat).find('.icon-container > span').attr('class') ?? '';
    const n = parseInt($(stat).text().replace(/\D/g, '') || '0');
    if (icon.includes('icon-heart')) console.log('likes:', n);
    if (icon.includes('icon-retweet')) console.log('retweets:', n);
  });

  // Is a retweet?
  const retweetedBy = $el.find('.retweet-header').text().trim() || undefined;

  // Quoted tweet
  const $quote = $el.find('.quote').first();
  if ($quote.length) {
    const quoteText = $quote.find('.quote-text').text().trim();
    const quoteUser = $quote.find('.tweet-name-row a.username').text().trim();
  }
});
```

### 6. 基于游标的分页

Nitter 会提供一个带有 `?cursor=` 参数的“显示更多”链接：

```ts
function findNextCursor($: cheerio.CheerioAPI): string | undefined {
  const href = $('div.show-more a').last().attr('href') ?? '';
  const m = href.match(/[?&]cursor=([^&]+)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

// In the pagination loop:
let cursor: string | undefined;
while (pagesFetched < maxPages) {
  const url = `https://nitter.net/i/lists/${listId}${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''}`;
  const html = await fetchPage(url);
  const $ = cheerio.load(html);
  // ... parse tweets ...
  const next = findNextCursor($);
  if (!next) break;
  cursor = next;
}
```

### 7. 按日期范围停止

只要某一页中最早的非转推早于 `startDate`，就停止分页，以避免不必要的获取：

```ts
// After parsing all tweets on a page:
const oldestNonRTMs = Math.min(
  ...pageTweets.filter(t => !t.retweetedBy).map(t => t.timestampMs)
);

if (oldestNonRTMs < startDate.getTime()) {
  console.log('Reached tweets older than start date; stopping.');
  break;
}
```

***

## 快速开始：最小端到端示例

```ts
import axios from 'axios';
import * as cheerio from 'cheerio';

const LIST_ID = '1585430245762441216';
const BASE = 'https://nitter.net';
const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (compatible; MyBot/1.0) Node.js',
  'Accept': 'text/html,application/xhtml+xml',
};

async function scrapeListPage(cursor?: string) {
  const url = `${BASE}/i/lists/${LIST_ID}${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''}`;
  const res = await axios.get(url, { headers: HEADERS, timeout: 30000 });
  const $ = cheerio.load(res.data);

  const tweets: { id: string; text: string; timestamp: string }[] = [];

  $('.timeline .timeline-item').filter((_, el) =>
    $(el).find('.tweet-body').length > 0
  ).each((_, el) => {
    const $el = $(el);
    const href = $el.find('a.tweet-link').first().attr('href') ?? '';
    const id = href.match(/status\/(\d+)/)?.[1] ?? href;
    const title = $el.find('.tweet-date a').attr('title') ?? '';
    const timestamp = new Date(title.replace(/\s*[·•]\s*/g, ' ')).toISOString();
    const text = $el.find('.tweet-content.media-body').text().trim();
    tweets.push({ id, text, timestamp });
  });

  const nextHref = $('div.show-more a').last().attr('href') ?? '';
  const nextCursor = nextHref.match(/[?&]cursor=([^&]+)/)?.[1];

  return { tweets, nextCursor: nextCursor ? decodeURIComponent(nextCursor) : undefined };
}

async function main() {
  let cursor: string | undefined;
  let allTweets: { id: string; text: string; timestamp: string }[] = [];

  for (let page = 0; page < 5; page++) {
    const { tweets, nextCursor } = await scrapeListPage(cursor);
    allTweets.push(...tweets);
    console.log(`Page ${page + 1}: +${tweets.length} tweets (${allTweets.length} total)`);
    if (!nextCursor) break;
    cursor = nextCursor;
    await new Promise(r => setTimeout(r, 1000)); // polite delay
  }

  console.log(JSON.stringify(allTweets, null, 2));
}

main();
```

***

## 实证发现（2026 年 4 月）

### 实例选择

`nitter.net` 本身通常可以访问，但**无头 Playwright 会返回“Oh noes!”（受到速率限制/被阻止）**。始终使用 `headless: false` 或 `channel: 'chrome'`。以下可用实例已于 2026 年 4 月 15 日确认：

| 实例 | 状态 |
|----------|--------|
| `nitter.tiekoetter.com` | ✅ 可靠，已成功使用 |
| `nitter.privacyredirect.com` | ⚠️ TLS 超时 |
| `nitter.catsarch.com` | ✅ 列为在线 |
| `xcancel.com` | ✅ 列为在线 |
| `nitter.net` | ✅ 在线，但可能阻止无头浏览器 |

在此处查看实时状态：**https://status.d420.de/**

建立一个优先级列表并自动回退。仅在 DOM 中找到 `.timeline-item` 后才将实例视为有效，而不能只根据页面标题判断：

```ts
const ok = await page.waitForSelector('.timeline-item', { timeout: 10000 })
  .then(() => true).catch(() => false);
// Don't trust page.title() — error pages can spoof it
```

### 无头模式始终失败

Nitter 实例会主动检测无头 Chromium，并返回空白或错误页面。**始终使用 `headless: false`**（或者使用隐含有头模式的 `channel: 'chrome'`）。`--disable-blink-features=AutomationControlled` 参数和对 `navigator.webdriver` 的覆盖也必不可少：

```ts
const browser = await chromium.launch({
  headless: false, // REQUIRED — headless gets blocked
  args: ['--disable-blink-features=AutomationControlled'],
});
await context.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
});
```

### 分页：游标 URL 构造

`div.show-more a` 的 href 是类似 `?cursor=DAA...` 的**相对 URL**。不要简单地构造 `baseUrl + href`，正确形式是：

```ts
// ✅ correct
const nextUrl = `${baseUrl}/${handle}${nextHref}`; // nextHref starts with "?"

// ❌ wrong — this double-encodes or drops the path
const nextUrl = new URL(nextHref, baseUrl).href;
```

在调用 `page.goto()` 之前，通过日志验证构造出的 URL。

### 时间戳解析

`.tweet-date a` 元素具有两个有用的属性：

- `title` — **完整的绝对日期**：`"Apr 14, 2026 · 5:47 PM UTC"`——进行截止日期比较时始终使用此属性
- `textContent` — **相对显示值**：`"19h"` 或 `"Apr 14"`——不适合可靠解析

`·` 分隔符是 Unicode 中点（`\u00B7`），而不是 ASCII 字符。按此字符拆分：

```ts
const datePart = title.split('·')[0].trim(); // "Apr 14, 2026 "
const date = new Date(datePart); // reliable
```

不要尝试解析 `"19h"`——如果缺少 `title`，请跳过该推文，或不要根据该推文进行截止判断。

### 置顶帖子

第一个 `.timeline-item` 通常是可能已有多年历史的**置顶帖子**，会导致错误地提前截止。跳过它：

```ts
const isPinned = item.classList.contains('pinned') ||
  !!item.querySelector('.pinned-icon, .icon-pin');
if (isPinned) continue;
```

另外：应使用**最早的非置顶**推文日期进行截止判断，而不只是使用最早的推文。

### 头像抓取（无需认证）

CSS 选择器参考中列出了 `.tweet-header a.tweet-avatar img.avatar[src]`——**使用此选择器代替 unavatar.io**，无需第三方服务即可直接从 Nitter 获取头像：

```ts
const avatarSrc = $el.find('.tweet-header a.tweet-avatar img.avatar').attr('src');
// Returns a relative path like /pic/pbs.twimg.com%2F...
// Decode it:
const avatarUrl = avatarSrc
  ? 'https://pbs.twimg.com/' + decodeURIComponent(avatarSrc.replace('/pic/', '').replace('pbs.twimg.com%2F', ''))
  : undefined;
```

或者直接存储 Nitter 代理后的 URL：`${instance}${avatarSrc}`（如果实例发生变化，该 URL 将失效）。

**避免使用 `unavatar.io/twitter/<handle>`**——它会通过 301 重定向至 `/x/<handle>`，且匿名用户的每日速率限制较低（批量回填许多用户时很快就会触发）。仅在无法获取 Nitter 头像时将其用作回退方案。

### 转推中的推文作者 URL 指向原始内容

在转推中，`a.tweet-link href` 指向的是**原作者的推文**（例如 `/originalAuthor/status/123`），而不是 `/@swyx/status/...`。这正是链接到来源时所需要的结果。请从 href 中提取作者：

```ts
const authorMatch = href.match(/^\/([^/]+)\/status/);
const author = authorMatch?.[1]; // original author's handle
```

***

## 依赖项

```json
{
  "axios": "^1.7.2",
  "cheerio": "^1.0.0",
  "playwright": "^1.58.2"
}
```

只需安装一次 Playwright 浏览器：`npx playwright install chrome`

***

## CSS 选择器参考

| 数据 | 选择器 |
|------|----------|
| 推文容器 | `.timeline .timeline-item`（筛选条件：包含 `.tweet-body`） |
| 推文链接 / ID | `a.tweet-link[href]` → 提取 `/status/(\d+)/` |
| 时间戳 | `.tweet-date a[title]` |
| 推文文本 | `.tweet-content.media-body` |
| 作者用户名 | `.tweet-header a.username[title]` |
| 作者显示名称 | `.tweet-header a.fullname[title]` |
| 头像 | `.tweet-header a.tweet-avatar img.avatar[src]` |
| 图片 | `.attachments .attachment.image img[src]` |
| 视频 | `.attachments .gallery-video img[src]`（封面图） |
| 链接卡片 | `.card a.card-container[href]` |
| 点赞数 | `.tweet-stat span.icon-heart` → 同级文本 |
| 转推数 | `.tweet-stat span.icon-retweet` → 同级文本 |
| 回复数 | `.tweet-stat span.icon-comment` → 同级文本 |
| 引用推文数 | `.tweet-stat span.icon-quote` → 同级文本 |
| 转推横幅 | `.retweet-header`（非空 = 是转推） |
| 引用推文块 | `.quote` |
| 引用文本 | `.quote .quote-text` |
| 下一页游标 | `div.show-more a[href]` → 提取 `?cursor=` |
