# Skills-Hub

这是一个个人 Skill 库收藏仓库。根目录只保留管理文件，实际收藏的 GitHub 项目放在 `libraries/` 下；从项目中提炼出的可复制 Skill 放在 `extracted-skills/` 下。两个目录都以 GitHub 项目库作为一级目录，方便对照来源与安装版本。

## 常用命令

```bash
python scripts/scan_skills.py
python scripts/extract_skills.py
python scripts/list_skills.py
python scripts/list_skills.py --skills
python scripts/list_skills.py --category coding-tools --skills
python scripts/search_skills.py pdf
python scripts/sync_skills.py --check
python scripts/generate_docs.py
python scripts/generate_site.py
```

## 网站展示

运行 `python scripts/generate_site.py` 会读取 `registry/projects.yaml` 并生成静态站点到 `site/index.html`。生成后的页面可直接在浏览器打开，也可以部署到 GitHub Pages、Nginx 或任意静态文件服务。

本仓库使用 GitHub Actions 自动发布 GitHub Pages：推送到 `main` 后，`.github/workflows/pages.yml` 会重新生成 `site/` 并发布为公开网站。

<!-- SKILLS_INDEX_START -->
## 收藏概览

当前共收藏 **29** 个 Skill 库，包含 **288** 个 skills。

## 按分类查看

### 编程工具类

- [agent-browser](libraries/agent-browser) `agent-browser` - 7 个 skills  
  分类：编程工具类 | 标签：browser, cli, coding, data, docs | 来源：vercel-labs/agent-browser  
  安装：推荐 `npx skills add vercel-labs/agent-browser`；也可从 [`extracted-skills/agent-browser`](extracted-skills/agent-browser) 手动复制。  
  简介：agent-browser
  - [agent-browser](libraries/agent-browser/skills/agent-browser/SKILL.md) `agent-browser` | 可复制：[`extracted-skills/agent-browser/agent-browser`](extracted-skills/agent-browser/agent-browser) - Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigati...
  - [agentcore](libraries/agent-browser/skill-data/agentcore/SKILL.md) `agentcore` | 可复制：[`extracted-skills/agent-browser/agentcore`](extracted-skills/agent-browser/agentcore) - Run agent-browser on AWS Bedrock AgentCore cloud browsers. Use when the user wants to use AgentCore, run br...
  - [core](libraries/agent-browser/skill-data/core/SKILL.md) `core` | 可复制：[`extracted-skills/agent-browser/core`](extracted-skills/agent-browser/core) - Core agent-browser usage guide. Read this before running any agent-browser commands. Covers the snapshot-an...
  - [dogfood](libraries/agent-browser/skill-data/dogfood/SKILL.md) `dogfood` | 可复制：[`extracted-skills/agent-browser/dogfood`](extracted-skills/agent-browser/dogfood) - Systematically explore and test a web application to find bugs, UX issues, and other problems. Use when ask...
  - [electron](libraries/agent-browser/skill-data/electron/SKILL.md) `electron` | 可复制：[`extracted-skills/agent-browser/electron`](extracted-skills/agent-browser/electron) - Automate Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify, etc.) using agent-browser...
  - [slack](libraries/agent-browser/skill-data/slack/SKILL.md) `slack` | 可复制：[`extracted-skills/agent-browser/slack`](extracted-skills/agent-browser/slack) - Interact with Slack workspaces using browser automation. Use when the user needs to check unread channels,...
  - 另有 1 个 skills，见 [agent-browser](libraries/agent-browser) 或 [完整索引](docs/index.md)。

- [agent-skills](libraries/agent-skills) `agent-skills` - 2 个 skills  
  分类：编程工具类 | 标签：automation, cli, coding, data, docs, mcp | 来源：supabase/agent-skills  
  安装：推荐 `npx skills add supabase/agent-skills`；也可从 [`extracted-skills/agent-skills`](extracted-skills/agent-skills) 手动复制。  
  简介：Supabase Agent Skills
  - [supabase](libraries/agent-skills/skills/supabase/SKILL.md) `supabase` | 可复制：[`extracted-skills/agent-skills/supabase`](extracted-skills/agent-skills/supabase) - Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Re...
  - [supabase-postgres-best-practices](libraries/agent-skills/skills/supabase-postgres-best-practices/SKILL.md) `supabase-postgres-best-practices` | 可复制：[`extracted-skills/agent-skills/supabase-postgres-best-practices`](extracted-skills/agent-skills/supabase-postgres-best-practices) - Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing,...

- [codex-complexity-optimizer](libraries/codex-complexity-optimizer) `codex-complexity-optimizer` - 1 个 skills  
  分类：编程工具类 | 标签：coding, docs | 来源：Kappaemme-git/codex-complexity-optimizer  
  安装：复制 [`extracted-skills/codex-complexity-optimizer`](extracted-skills/codex-complexity-optimizer) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Codex Complexity Optimizer
  - [complexity-optimizer](libraries/codex-complexity-optimizer/complexity-optimizer/SKILL.md) `complexity-optimizer` | 可复制：[`extracted-skills/codex-complexity-optimizer/complexity-optimizer`](extracted-skills/codex-complexity-optimizer/complexity-optimizer) - Analyze a software codebase for algorithmic complexity and performance hotspots, then propose or implement...

- [context7-cli](libraries/context7-cli) `context7-cli` - 1 个 skills  
  分类：编程工具类 | 标签：automation, cli, coding, docs, mcp | 来源：upstash/context7  
  安装：复制 [`extracted-skills/context7-cli`](extracted-skills/context7-cli) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：ctx7 CLI
  - [context7-cli](libraries/context7-cli/SKILL.md) `context7-cli` | 可复制：[`extracted-skills/context7-cli/context7-cli`](extracted-skills/context7-cli/context7-cli) - Use the ctx7 CLI to fetch library documentation, manage AI coding skills, and configure Context7 MCP. Activ...

- [edgeone-pages-skills](libraries/edgeone-pages-skills) `edgeone-pages-skills` - 2 个 skills  
  分类：编程工具类 | 标签：automation, coding, docs, frontend, workflow | 来源：edgeone-pages/edgeone-pages-skills  
  安装：推荐 `npx skills add edgeone-pages/edgeone-pages-skills`；也可从 [`extracted-skills/edgeone-pages-skills`](extracted-skills/edgeone-pages-skills) 手动复制。  
  简介：EdgeOne Pages Skills
  - [edgeone-pages-deploy](libraries/edgeone-pages-skills/skills/edgeone-pages-deploy/SKILL.md) `edgeone-pages-deploy` | 可复制：[`extracted-skills/edgeone-pages-skills/edgeone-pages-deploy`](extracted-skills/edgeone-pages-skills/edgeone-pages-deploy) - This skill deploys frontend and full-stack projects to EdgeOne Pages (Tencent EdgeOne). It should be used w...
  - [edgeone-pages-dev](libraries/edgeone-pages-skills/skills/edgeone-pages-dev/SKILL.md) `edgeone-pages-dev` | 可复制：[`extracted-skills/edgeone-pages-skills/edgeone-pages-dev`](extracted-skills/edgeone-pages-skills/edgeone-pages-dev) - This skill guides development of full-stack features on EdgeOne Pages — Edge Functions, Cloud Functions (No...

- [vercel-labsagent-skills](libraries/vercel-labsagent-skills) `vercel-labsagent-skills` - 9 个 skills  
  分类：编程工具类 | 标签：automation, cli, coding, data, docs, frontend | 来源：vercel-labs/agent-skills  
  安装：推荐 `npx skills add vercel-labs/agent-skills`；也可从 [`extracted-skills/vercel-labsagent-skills`](extracted-skills/vercel-labsagent-skills) 手动复制。  
  简介：Agent Skills
  - [deploy-to-vercel](libraries/vercel-labsagent-skills/skills/deploy-to-vercel/SKILL.md) `deploy-to-vercel` | 可复制：[`extracted-skills/vercel-labsagent-skills/deploy-to-vercel`](extracted-skills/vercel-labsagent-skills/deploy-to-vercel) - Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my a...
  - [vercel-cli-with-tokens](libraries/vercel-labsagent-skills/skills/vercel-cli-with-tokens/SKILL.md) `vercel-cli-with-tokens` | 可复制：[`extracted-skills/vercel-labsagent-skills/vercel-cli-with-tokens`](extracted-skills/vercel-labsagent-skills/vercel-cli-with-tokens) - Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI usi...
  - [vercel-composition-patterns](libraries/vercel-labsagent-skills/skills/composition-patterns/SKILL.md) `vercel-composition-patterns` | 可复制：[`extracted-skills/vercel-labsagent-skills/vercel-composition-patterns`](extracted-skills/vercel-labsagent-skills/vercel-composition-patterns) - React Composition Patterns
  - [vercel-optimize](libraries/vercel-labsagent-skills/skills/vercel-optimize/SKILL.md) `vercel-optimize` | 可复制：[`extracted-skills/vercel-labsagent-skills/vercel-optimize`](extracted-skills/vercel-labsagent-skills/vercel-optimize) - Use for Vercel cost and performance optimization on deployed projects, especially Next.js, SvelteKit, Nuxt,...
  - [vercel-react-best-practices](libraries/vercel-labsagent-skills/skills/react-best-practices/SKILL.md) `vercel-react-best-practices` | 可复制：[`extracted-skills/vercel-labsagent-skills/vercel-react-best-practices`](extracted-skills/vercel-labsagent-skills/vercel-react-best-practices) - React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used wh...
  - [vercel-react-native-skills](libraries/vercel-labsagent-skills/skills/react-native-skills/SKILL.md) `vercel-react-native-skills` | 可复制：[`extracted-skills/vercel-labsagent-skills/vercel-react-native-skills`](extracted-skills/vercel-labsagent-skills/vercel-react-native-skills) - React Native Skills
  - 另有 3 个 skills，见 [vercel-labsagent-skills](libraries/vercel-labsagent-skills) 或 [完整索引](docs/index.md)。

### 日常工具类

- [mineru](libraries/mineru) `mineru` - 1 个 skills  
  分类：日常工具类 | 标签：coding, data, docs, image, workflow | 来源：opendatalab/MinerU-Ecosystem  
  安装：复制 [`extracted-skills/mineru`](extracted-skills/mineru) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Document Extraction with mineru-open-api
  - [MinerU Document Extractor](libraries/mineru/SKILL.md) `mineru-document-extractor` | 可复制：[`extracted-skills/mineru/mineru-document-extractor`](extracted-skills/mineru/mineru-document-extractor) - MinerU document extraction — convert PDFs, scanned documents, images, Word (DOC/DOCX), PowerPoint (PPT/PPTX...

- [notebooklm](libraries/notebooklm) `notebooklm` - 1 个 skills  
  分类：日常工具类 | 标签：coding, docs, frontend | 来源：teng-lin/notebooklm-py  
  安装：推荐 `npx skills add teng-lin/notebooklm-py`；也可从 [`extracted-skills/notebooklm`](extracted-skills/notebooklm) 手动复制。  
  简介：NotebookLM Automation
  - [notebooklm](libraries/notebooklm/SKILL.md) `notebooklm` | 可复制：[`extracted-skills/notebooklm/notebooklm`](extracted-skills/notebooklm/notebooklm) - Complete API for Google NotebookLM - full programmatic access including features not in the web UI. Create...

- [obsidian-skills](libraries/obsidian-skills) `obsidian-skills` - 5 个 skills  
  分类：日常工具类 | 标签：cli, coding, data, docs, image, obsidian, research | 来源：kepano/obsidian-skills  
  安装：推荐 `npx skills add git@github.com:kepano/obsidian-skills.git`；也可从 [`extracted-skills/obsidian-skills`](extracted-skills/obsidian-skills) 手动复制。  
  简介：Installation
  - [defuddle](libraries/obsidian-skills/skills/defuddle/SKILL.md) `defuddle` | 可复制：[`extracted-skills/obsidian-skills/defuddle`](extracted-skills/obsidian-skills/defuddle) - Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save t...
  - [json-canvas](libraries/obsidian-skills/skills/json-canvas/SKILL.md) `json-canvas` | 可复制：[`extracted-skills/obsidian-skills/json-canvas`](extracted-skills/obsidian-skills/json-canvas) - Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working wi...
  - [obsidian-bases](libraries/obsidian-skills/skills/obsidian-bases/SKILL.md) `obsidian-bases` | 可复制：[`extracted-skills/obsidian-skills/obsidian-bases`](extracted-skills/obsidian-skills/obsidian-bases) - Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working...
  - [obsidian-cli](libraries/obsidian-skills/skills/obsidian-cli/SKILL.md) `obsidian-cli` | 可复制：[`extracted-skills/obsidian-skills/obsidian-cli`](extracted-skills/obsidian-skills/obsidian-cli) - Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, prop...
  - [obsidian-markdown](libraries/obsidian-skills/skills/obsidian-markdown/SKILL.md) `obsidian-markdown` | 可复制：[`extracted-skills/obsidian-skills/obsidian-markdown`](extracted-skills/obsidian-skills/obsidian-markdown) - Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian...

### 个人合集类

- [anthropic](libraries/anthropic) `anthropic` - 18 个 skills  
  分类：个人合集类 | 标签：automation, browser, coding, data, docs, frontend, image, mcp | 来源：anthropics/skills  
  安装：复制 [`extracted-skills/anthropic`](extracted-skills/anthropic) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：ALGORITHMIC PHILOSOPHY CREATION
  - [algorithmic-art](libraries/anthropic/skills/algorithmic-art/SKILL.md) `algorithmic-art` | 可复制：[`extracted-skills/anthropic/algorithmic-art`](extracted-skills/anthropic/algorithmic-art) - Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this...
  - [brand-guidelines](libraries/anthropic/skills/brand-guidelines/SKILL.md) `brand-guidelines` | 可复制：[`extracted-skills/anthropic/brand-guidelines`](extracted-skills/anthropic/brand-guidelines) - Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from havi...
  - [canvas-design](libraries/anthropic/skills/canvas-design/SKILL.md) `canvas-design` | 可复制：[`extracted-skills/anthropic/canvas-design`](extracted-skills/anthropic/canvas-design) - Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill w...
  - [claude-api](libraries/anthropic/skills/claude-api/SKILL.md) `claude-api` | 可复制：[`extracted-skills/anthropic/claude-api`](extracted-skills/anthropic/claude-api) - Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, tool use, MCP, agents...
  - [doc-coauthoring](libraries/anthropic/skills/doc-coauthoring/SKILL.md) `doc-coauthoring` | 可复制：[`extracted-skills/anthropic/doc-coauthoring`](extracted-skills/anthropic/doc-coauthoring) - Guide users through a structured workflow for co-authoring documentation. Use when user wants to write docu...
  - [docx](libraries/anthropic/skills/docx/SKILL.md) `docx` | 可复制：[`extracted-skills/anthropic/docx`](extracted-skills/anthropic/docx) - Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). T...
  - 另有 12 个 skills，见 [anthropic](libraries/anthropic) 或 [完整索引](docs/index.md)。

- [mattpocock-skills](libraries/mattpocock-skills) `mattpocock-skills` - 36 个 skills  
  分类：个人合集类 | 标签：automation, cli, coding, data, docs, finance, frontend, obsidian | 来源：mattpocock/skills  
  安装：复制 [`extracted-skills/mattpocock-skills`](extracted-skills/mattpocock-skills) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Skills For Real Engineers
  - [ask-matt](libraries/mattpocock-skills/skills/engineering/ask-matt/SKILL.md) `ask-matt` | 可复制：[`extracted-skills/mattpocock-skills/ask-matt`](extracted-skills/mattpocock-skills/ask-matt) - Ask which skill or flow fits your situation. A router over the skills in this repo.
  - [code-review](libraries/mattpocock-skills/skills/engineering/code-review/SKILL.md) `code-review` | 可复制：[`extracted-skills/mattpocock-skills/code-review`](extracted-skills/mattpocock-skills/code-review) - Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (doe...
  - [codebase-design](libraries/mattpocock-skills/skills/engineering/codebase-design/SKILL.md) `codebase-design` | 可复制：[`extracted-skills/mattpocock-skills/codebase-design`](extracted-skills/mattpocock-skills/codebase-design) - Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's inter...
  - [design-an-interface](libraries/mattpocock-skills/skills/deprecated/design-an-interface/SKILL.md) `design-an-interface` | 可复制：[`extracted-skills/mattpocock-skills/design-an-interface`](extracted-skills/mattpocock-skills/design-an-interface) - Generate multiple radically different interface designs for a module using parallel sub-agents. Use when us...
  - [diagnosing-bugs](libraries/mattpocock-skills/skills/engineering/diagnosing-bugs/SKILL.md) `diagnosing-bugs` | 可复制：[`extracted-skills/mattpocock-skills/diagnosing-bugs`](extracted-skills/mattpocock-skills/diagnosing-bugs) - Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", o...
  - [domain-modeling](libraries/mattpocock-skills/skills/engineering/domain-modeling/SKILL.md) `domain-modeling` | 可复制：[`extracted-skills/mattpocock-skills/domain-modeling`](extracted-skills/mattpocock-skills/domain-modeling) - Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubi...
  - 另有 30 个 skills，见 [mattpocock-skills](libraries/mattpocock-skills) 或 [完整索引](docs/index.md)。

- [swyxio-skills](libraries/swyxio-skills) `swyxio-skills` - 39 个 skills  
  分类：个人合集类 | 标签：automation, browser, coding, data, docs, image, research, workflow | 来源：swyxio/skills  
  安装：复制 [`extracted-skills/swyxio-skills`](extracted-skills/swyxio-skills) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：swyxio Skills
  - [accelevents-api](libraries/swyxio-skills/accelevents-api/SKILL.md) `accelevents-api` | 可复制：[`extracted-skills/swyxio-skills/accelevents-api`](extracted-skills/swyxio-skills/accelevents-api) - Use when reading or updating AI Engineer Europe speaker records through the Accelevents REST API, especiall...
  - [accelevents-speaker-sync](libraries/swyxio-skills/accelevents-speaker-sync/SKILL.md) `accelevents-speaker-sync` | 可复制：[`extracted-skills/swyxio-skills/accelevents-speaker-sync`](extracted-skills/swyxio-skills/accelevents-speaker-sync) - Use when website speaker, session, schedule, room, track, or headshot changes must be synchronized back to...
  - [antislop-codebase](libraries/swyxio-skills/antislop-codebase/SKILL.md) `antislop-codebase` | 可复制：[`extracted-skills/swyxio-skills/antislop-codebase`](extracted-skills/swyxio-skills/antislop-codebase) - Analyze and transform messy, prototype, overgrown, slop-prone, or hard-to-maintain software repositories in...
  - [app-ux-paradigms](libraries/swyxio-skills/app-ux-paradigms/SKILL.md) `app-ux-paradigms` | 可复制：[`extracted-skills/swyxio-skills/app-ux-paradigms`](extracted-skills/swyxio-skills/app-ux-paradigms) - Applies standard web app UX for keyboard shortcuts, modals, overlays, forms, and interaction patterns. Use...
  - [autoreview](libraries/swyxio-skills/autoreview/SKILL.md) `autoreview` | 可复制：[`extracted-skills/swyxio-skills/autoreview`](extracted-skills/swyxio-skills/autoreview) - Run structured closeout code review after non-trivial code edits, branch or PR work, or commits using an au...
  - [claude-session-introspect](libraries/swyxio-skills/claude-session-introspect/SKILL.md) `claude-session-introspect` | 可复制：[`extracted-skills/swyxio-skills/claude-session-introspect`](extracted-skills/swyxio-skills/claude-session-introspect) - Inspect Claude Code session JSONL files at ~/.claude/projects/ to extract real conversation telemetry: toke...
  - 另有 33 个 skills，见 [swyxio-skills](libraries/swyxio-skills) 或 [完整索引](docs/index.md)。

### 前端展示类

- [frontend-slides](libraries/frontend-slides) `frontend-slides` - 2 个 skills  
  分类：前端展示类 | 标签：coding, docs, frontend | 来源：zarazhangrui/frontend-slides  
  安装：复制 [`extracted-skills/frontend-slides`](extracted-skills/frontend-slides) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Frontend Slides
  - [frontend-slides](libraries/frontend-slides/plugins/frontend-slides/skills/frontend-slides/SKILL.md) `frontend-slides` | 可复制：[`extracted-skills/frontend-slides/frontend-slides`](extracted-skills/frontend-slides/frontend-slides) - Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when...
  - [frontend-slides](libraries/frontend-slides/SKILL.md) `frontend-slides-2` | 可复制：[`extracted-skills/frontend-slides/frontend-slides-2`](extracted-skills/frontend-slides/frontend-slides-2) - Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when...

- [gsap-skills](libraries/gsap-skills) `gsap-skills` - 8 个 skills  
  分类：前端展示类 | 标签：animation, frontend, coding | 来源：greensock/gsap-skills  
  安装：复制 [`extracted-skills/gsap-skills`](extracted-skills/gsap-skills) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：GSAP Core
  - [gsap-core](libraries/gsap-skills/gsap-core/SKILL.md) `gsap-core` | 可复制：[`extracted-skills/gsap-skills/gsap-core`](extracted-skills/gsap-skills/gsap-core) - Official GSAP skill for the core API — gsap.to(), from(), fromTo(), easing, duration, stagger, defaults, gs...
  - [gsap-frameworks](libraries/gsap-skills/gsap-frameworks/SKILL.md) `gsap-frameworks` | 可复制：[`extracted-skills/gsap-skills/gsap-frameworks`](extracted-skills/gsap-skills/gsap-frameworks) - Official GSAP skill for Vue, Svelte, and other non-React frameworks — lifecycle, scoping selectors, cleanup...
  - [gsap-performance](libraries/gsap-skills/gsap-performance/SKILL.md) `gsap-performance` | 可复制：[`extracted-skills/gsap-skills/gsap-performance`](extracted-skills/gsap-skills/gsap-performance) - Official GSAP skill for performance — prefer transforms, avoid layout thrashing, will-change, batching. Use...
  - [gsap-plugins](libraries/gsap-skills/gsap-plugins/SKILL.md) `gsap-plugins` | 可复制：[`extracted-skills/gsap-skills/gsap-plugins`](extracted-skills/gsap-skills/gsap-plugins) - Official GSAP skill for GSAP plugins — registration, ScrollToPlugin, ScrollSmoother, Flip, Draggable, Inert...
  - [gsap-react](libraries/gsap-skills/gsap-react/SKILL.md) `gsap-react` | 可复制：[`extracted-skills/gsap-skills/gsap-react`](extracted-skills/gsap-skills/gsap-react) - Official GSAP skill for React — useGSAP hook, refs, gsap.context(), cleanup. Use when the user wants animat...
  - [gsap-scrolltrigger](libraries/gsap-skills/gsap-scrolltrigger/SKILL.md) `gsap-scrolltrigger` | 可复制：[`extracted-skills/gsap-skills/gsap-scrolltrigger`](extracted-skills/gsap-skills/gsap-scrolltrigger) - Official GSAP skill for ScrollTrigger — scroll-linked animations, pinning, scrub, triggers. Use when buildi...
  - 另有 2 个 skills，见 [gsap-skills](libraries/gsap-skills) 或 [完整索引](docs/index.md)。

- [guizang-ppt-skill](libraries/guizang-ppt-skill) `guizang-ppt-skill` - 1 个 skills  
  分类：前端展示类 | 标签：coding, docs, frontend | 来源：op7418/guizang-ppt-skill  
  安装：推荐 `npx skills add https://github.com/op7418/guizang-ppt-skill --skill guizang-ppt-skill`；也可从 [`extracted-skills/guizang-ppt-skill`](extracted-skills/guizang-ppt-skill) 手动复制。  
  简介：Guizang PPT Skill · 网页 PPT / 配图 / 封面
  - [guizang-ppt-skill](libraries/guizang-ppt-skill/SKILL.md) `guizang-ppt-skill` | 可复制：[`extracted-skills/guizang-ppt-skill/guizang-ppt-skill`](extracted-skills/guizang-ppt-skill/guizang-ppt-skill) - 生成横向翻页网页 PPT（单 HTML 文件），含 WebGL 背景、章节幕封、数据大字报、图片网格等模板。提供两种风格：① "电子杂志 × 电子墨水"（衬线 + 流体背景 + 暖色） ② "瑞士国际主义"（无衬线...

- [html-anything](libraries/html-anything) `html-anything` - 78 个 skills  
  分类：前端展示类 | 标签：coding, docs, frontend, image, workflow | 来源：nexu-io/html-anything  
  安装：复制 [`extracted-skills/html-anything`](extracted-skills/html-anything) 下需要的 skill 到 `~/.claude/skills/`。
  - [article-magazine](libraries/html-anything/article-magazine/SKILL.md) `article-magazine` | 可复制：[`extracted-skills/html-anything/article-magazine`](extracted-skills/html-anything/article-magazine) - Substack / Medium 高级感长文排版, 适合公众号、博客发布
  - [blog-post](libraries/html-anything/blog-post/SKILL.md) `blog-post` | 可复制：[`extracted-skills/html-anything/blog-post`](extracted-skills/html-anything/blog-post) - 杂志感长文, 含 masthead、hero、figures、pull quote、作者署名
  - [card-twitter](libraries/html-anything/card-twitter/SKILL.md) `card-twitter` | 可复制：[`extracted-skills/html-anything/card-twitter`](extracted-skills/html-anything/card-twitter) - 推特金句 / 数据卡, 适合配推文
  - [card-xiaohongshu](libraries/html-anything/card-xiaohongshu/SKILL.md) `card-xiaohongshu` | 可复制：[`extracted-skills/html-anything/card-xiaohongshu`](extracted-skills/html-anything/card-xiaohongshu) - 小红书风格知识卡片, 多张联排可滑动浏览
  - [competitive-teardown](libraries/html-anything/competitive-teardown/SKILL.md) `competitive-teardown` | 可复制：[`extracted-skills/html-anything/competitive-teardown`](extracted-skills/html-anything/competitive-teardown) - 定位图 + 功能矩阵 + 价格对比 + 机会窗口, 把竞品资料转成产品决策报告
  - [dashboard](libraries/html-anything/dashboard/SKILL.md) `dashboard` | 可复制：[`extracted-skills/html-anything/dashboard`](extracted-skills/html-anything/dashboard) - 固定侧栏 + 顶栏 + KPI 网格 + 1-2 张图
  - 另有 72 个 skills，见 [html-anything](libraries/html-anything) 或 [完整索引](docs/index.md)。

- [impeccable](libraries/impeccable) `impeccable` - 1 个 skills  
  分类：前端展示类 | 标签：automation, coding, docs, frontend, image, workflow | 来源：pbakaus/impeccable  
  安装：推荐 `npx impeccable skills install`；也可从 [`extracted-skills/impeccable`](extracted-skills/impeccable) 手动复制。  
  简介：Impeccable
  - [impeccable](libraries/impeccable/plugin/skills/impeccable/SKILL.md) `impeccable` | 可复制：[`extracted-skills/impeccable/impeccable`](extracted-skills/impeccable/impeccable) - Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, opti...

### 动画动效类

- [lottie](libraries/lottie) `lottie` - 1 个 skills  
  分类：动画动效类 | 标签：animation, frontend, image, coding | 来源：diffusionstudio/lottie  
  安装：复制 [`extracted-skills/lottie`](extracted-skills/lottie) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Authoring Renderable Lottie Files
  - [text-to-lottie](libraries/lottie/text-to-lottie/SKILL.md) `text-to-lottie` | 可复制：[`extracted-skills/lottie/text-to-lottie`](extracted-skills/lottie/text-to-lottie) - Author a Lottie (Bodymovin) JSON animation that renders in a local skia player. Use whenever the user asks...

### 内容创作类

- [baoyu-skills](libraries/baoyu-skills) `baoyu-skills` - 21 个 skills  
  分类：内容创作类 | 标签：browser, cli, coding, data, docs, frontend, image, workflow | 来源：JimLiu/baoyu-skills  
  安装：推荐 `npx skills add jimliu/baoyu-skills`；也可从 [`extracted-skills/baoyu-skills`](extracted-skills/baoyu-skills) 手动复制。  
  简介：baoyu-skills
  - [baoyu-article-illustrator](libraries/baoyu-skills/skills/baoyu-article-illustrator/SKILL.md) `baoyu-article-illustrator` | 可复制：[`extracted-skills/baoyu-skills/baoyu-article-illustrator`](extracted-skills/baoyu-skills/baoyu-article-illustrator) - Analyzes article structure, identifies positions requiring visual aids, generates illustrations with Type ×...
  - [baoyu-comic](libraries/baoyu-skills/skills/baoyu-comic/SKILL.md) `baoyu-comic` | 可复制：[`extracted-skills/baoyu-skills/baoyu-comic`](extracted-skills/baoyu-skills/baoyu-comic) - Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with...
  - [baoyu-compress-image](libraries/baoyu-skills/skills/baoyu-compress-image/SKILL.md) `baoyu-compress-image` | 可复制：[`extracted-skills/baoyu-skills/baoyu-compress-image`](extracted-skills/baoyu-skills/baoyu-compress-image) - Compresses images to WebP (default) or PNG with automatic tool selection. Use when user asks to "compress i...
  - [baoyu-cover-image](libraries/baoyu-skills/skills/baoyu-cover-image/SKILL.md) `baoyu-cover-image` | 可复制：[`extracted-skills/baoyu-skills/baoyu-cover-image`](extracted-skills/baoyu-skills/baoyu-cover-image) - Generates article cover images with 5 dimensions (type, palette, rendering, text, mood) combining 11 color...
  - [baoyu-danger-gemini-web](libraries/baoyu-skills/skills/baoyu-danger-gemini-web/SKILL.md) `baoyu-danger-gemini-web` | 可复制：[`extracted-skills/baoyu-skills/baoyu-danger-gemini-web`](extracted-skills/baoyu-skills/baoyu-danger-gemini-web) - Generates images and text via reverse-engineered Gemini Web API. Supports text generation, image generation...
  - [baoyu-danger-x-to-markdown](libraries/baoyu-skills/skills/baoyu-danger-x-to-markdown/SKILL.md) `baoyu-danger-x-to-markdown` | 可复制：[`extracted-skills/baoyu-skills/baoyu-danger-x-to-markdown`](extracted-skills/baoyu-skills/baoyu-danger-x-to-markdown) - Converts X (Twitter) tweets and articles to markdown with YAML front matter. Uses reverse-engineered API re...
  - 另有 15 个 skills，见 [baoyu-skills](libraries/baoyu-skills) 或 [完整索引](docs/index.md)。

- [content-research-writer](libraries/content-research-writer) `content-research-writer` - 1 个 skills  
  分类：内容创作类 | 标签：docs, research, workflow | 来源：ComposioHQ/awesome-claude-skills  
  安装：复制 [`extracted-skills/content-research-writer`](extracted-skills/content-research-writer) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Content Research Writer
  - [content-research-writer](libraries/content-research-writer/SKILL.md) `content-research-writer` | 可复制：[`extracted-skills/content-research-writer/content-research-writer`](extracted-skills/content-research-writer/content-research-writer) - Assists in writing high-quality content by conducting research, adding citations, improving hooks, iteratin...

- [guizang-social-card-skill](libraries/guizang-social-card-skill) `guizang-social-card-skill` - 1 个 skills  
  分类：内容创作类 | 标签：image, docs, frontend, workflow | 来源：op7418/guizang-social-card-skill  
  安装：推荐 `npx skills add https://github.com/op7418/guizang-social-card-skill --skill guizang-social-card-skill`；也可从 [`extracted-skills/guizang-social-card-skill`](extracted-skills/guizang-social-card-skill) 手动复制。  
  简介：Guizang Social Card Skill · 小红书图文 / 公众号封面对
  - [guizang-social-card-skill](libraries/guizang-social-card-skill/SKILL.md) `guizang-social-card-skill` | 可复制：[`extracted-skills/guizang-social-card-skill/guizang-social-card-skill`](extracted-skills/guizang-social-card-skill/guizang-social-card-skill) - Generate Guizang-style social card image sets and WeChat official account cover pairs from articles, script...

- [huashu-md-html](libraries/huashu-md-html) `huashu-md-html` - 1 个 skills  
  分类：内容创作类 | 标签：docs, frontend, pdf, workflow | 来源：alchaincyf/huashu-md-html  
  安装：推荐 `npx skills add alchaincyf/huashu-md-html`；也可从 [`extracted-skills/huashu-md-html`](extracted-skills/huashu-md-html) 手动复制。  
  简介：huashu-md-html
  - [huashu-md-html](libraries/huashu-md-html/SKILL.md) `huashu-md-html` | 可复制：[`extracted-skills/huashu-md-html/huashu-md-html`](extracted-skills/huashu-md-html/huashu-md-html) - 花叔的「md/html/docx 多向流水线」skill，四个能力 + 两种模式：(1) 用Microsoft markitdown把任意文件（PDF/DOCX/PPTX/XLSX/HTML/图片/音频/YouTu...

- [huashu-skills](libraries/huashu-skills) `huashu-skills` - 21 个 skills  
  分类：内容创作类 | 标签：automation, coding, data, docs, image, pdf, research | 来源：alchaincyf/huashu-skills  
  安装：复制 [`extracted-skills/huashu-skills`](extracted-skills/huashu-skills) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：huashu-skills
  - [huashu-agent-swarm](libraries/huashu-skills/huashu-agent-swarm/SKILL.md) `huashu-agent-swarm` | 可复制：[`extracted-skills/huashu-skills/huashu-agent-swarm`](extracted-skills/huashu-skills/huashu-agent-swarm) - 多Agent蜂群并行协作，纯git自组织，适合大型项目开发。当用户提到"蜂群模式"、"多agent"、"并行开发"、"agent swarm"时使用。
  - [huashu-article-edit](libraries/huashu-skills/huashu-article-edit/SKILL.md) `huashu-article-edit` | 可复制：[`extracted-skills/huashu-skills/huashu-article-edit`](extracted-skills/huashu-skills/huashu-article-edit) - 标准化文章编辑流程，确保修改范围明确、进度可追踪、变更有记录。当用户说"编辑文章"、"修改文章"、"调整内容"、"改一下这篇"时使用此技能。
  - [huashu-article-to-x](libraries/huashu-skills/huashu-article-to-x/SKILL.md) `huashu-article-to-x` | 可复制：[`extracted-skills/huashu-skills/huashu-article-to-x`](extracted-skills/huashu-skills/huashu-article-to-x) - 长文精简为X平台内容（200-500字），保留核心观点和个人风格。当用户提到"转微博"、"发小红书"、"社交媒体"、"缩短文章"时使用。
  - [huashu-data-pro](libraries/huashu-skills/huashu-data-pro/SKILL.md) `huashu-data-pro` | 可复制：[`extracted-skills/huashu-skills/huashu-data-pro`](extracted-skills/huashu-skills/huashu-data-pro) - 数据分析与办公提效全能助手。覆盖数据处理、分析洞察、报告撰写、PPT制作、数据可视化的端到端工作流。 始终从专家视角出发，帮用户多想一步。遇到不确定的问题主动与用户确认。 支持：Excel数据分析、投放数据复盘、R...
  - [huashu-design](libraries/huashu-skills/huashu-design/SKILL.md) `huashu-design` | 可复制：[`extracted-skills/huashu-skills/huashu-design`](extracted-skills/huashu-skills/huashu-design) - 设计哲学顾问，从20种风格中推荐3个方向并生成视觉Demo和AI提示词。当用户提到"设计风格"、"设计方向"、"配色方案"、"视觉风格"、"设计评审"、"推荐风格"时使用。
  - [huashu-douyin-script](libraries/huashu-skills/huashu-douyin-script/SKILL.md) `huashu-douyin-script` | 可复制：[`extracted-skills/huashu-skills/huashu-douyin-script`](extracted-skills/huashu-skills/huashu-douyin-script) - 抖音爆款脚本创作工作流。从竞品视频拆解到脚本生成的完整流程：下载抖音视频→Gemini视频分析→爆款公式提炼→脚本+分镜生成→AI味审校。 当用户提到"抖音脚本"、"爆款拆解"、"竞品分析"、"带货脚本"、"千川素...
  - 另有 15 个 skills，见 [huashu-skills](libraries/huashu-skills) 或 [完整索引](docs/index.md)。

- [ljg-skills](libraries/ljg-skills) `ljg-skills` - 23 个 skills  
  分类：内容创作类 | 标签：automation, coding, data, docs, finance, frontend, pdf, research | 来源：lijigang/ljg-skills  
  安装：推荐 `npx skills add lijigang/ljg-skills -g --all`；也可从 [`extracted-skills/ljg-skills`](extracted-skills/ljg-skills) 手动复制。  
  简介：ljg-skills
  - [ljg-book](libraries/ljg-skills/skills/ljg-book/SKILL.md) `ljg-book` | 可复制：[`extracted-skills/ljg-skills/ljg-book`](extracted-skills/ljg-skills/ljg-book) - 拆一本书，以「问题」为轴心走一条线。五件事：作者在答什么问题（问题），这个问题之前各流派/社会共识怎么答（零点），作者带来什么独特洞见——公式/理论框架/模型/概念四选一——相对共识挪动了什么（位移/delta），...
  - [ljg-card](libraries/ljg-skills/skills/ljg-card/SKILL.md) `ljg-card` | 可复制：[`extracted-skills/ljg-skills/ljg-card`](extracted-skills/ljg-skills/ljg-card) - Content caster (铸). Transforms content into PNG visuals. Seven molds: -l (default) long reading card, -i in...
  - [ljg-invest](libraries/ljg-skills/skills/ljg-invest/SKILL.md) `ljg-invest` | 可复制：[`extracted-skills/ljg-skills/ljg-invest`](extracted-skills/ljg-skills/ljg-invest) - 投资分析, 生成一份深度投资分析报告。不做传统投资分析——核心判断是项目是否是一台「秩序创造机器」。Use when user says '投资报告', '投资分析', '分析这个项目', '写投资报告', 'in...
  - [ljg-learn](libraries/ljg-skills/skills/ljg-learn/SKILL.md) `ljg-learn` | 可复制：[`extracted-skills/ljg-skills/ljg-learn`](extracted-skills/ljg-skills/ljg-learn) - Deep concept anatomist that deconstructs any concept through 8 exploration dimensions (history, dialectics,...
  - [ljg-library](libraries/ljg-skills/skills/ljg-library/SKILL.md) `ljg-library` | 可复制：[`extracted-skills/ljg-skills/ljg-library`](extracted-skills/ljg-skills/ljg-library) - 一本书 → 一幅清晰的「取景框」意向画面 → 一张 2050 图书馆借书卡（PNG）。取景框 = 作者从哪个角度看什么问题、看到了哪幅画面；卡上有真实封面、作者头像、书目信息。取景框 block 用费曼式讲解把这幅...
  - [ljg-map](libraries/ljg-skills/skills/ljg-map/SKILL.md) `ljg-map` | 可复制：[`extracted-skills/ljg-skills/ljg-map`](extracted-skills/ljg-skills/ljg-map) - 一个行业 → 一张生态地形图卡（PNG）。以《千脑智能》参考系理论为地基：把行业摊成一张可俯瞰的「生态地形」——价值像河一样流过地貌，再在地形上标出两处——「瓶颈」（流量/产能在此收窄的隘口/水坝）和「价值捕获点」...
  - 另有 17 个 skills，见 [ljg-skills](libraries/ljg-skills) 或 [完整索引](docs/index.md)。

- [punk-skill](libraries/punk-skill) `punk-skill` - 2 个 skills  
  分类：内容创作类 | 标签：image, workflow | 来源：adrianpunk/Punk-Skill  
  安装：复制 [`extracted-skills/punk-skill`](extracted-skills/punk-skill) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Punk Avatar
  - [punk-avatar](libraries/punk-skill/punk-avatar/SKILL.md) `punk-avatar` | 可复制：[`extracted-skills/punk-skill/punk-avatar`](extracted-skills/punk-skill/punk-avatar) - Generate avatar images and reusable avatar image prompts from the shared Punk style library for people, pet...
  - [punk-cover](libraries/punk-skill/punk-cover/SKILL.md) `punk-cover` | 可复制：[`extracted-skills/punk-skill/punk-cover`](extracted-skills/punk-skill/punk-cover) - Generate cover images and reusable image prompts from the shared Punk style library for articles, Xiaohongs...

- [stop-slop](libraries/stop-slop) `stop-slop` - 1 个 skills  
  分类：内容创作类 | 标签：docs, workflow | 来源：hardikpandya/stop-slop  
  安装：复制 [`extracted-skills/stop-slop`](extracted-skills/stop-slop) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Stop Slop
  - [stop-slop](libraries/stop-slop/SKILL.md) `stop-slop` | 可复制：[`extracted-skills/stop-slop/stop-slop`](extracted-skills/stop-slop/stop-slop) - Remove AI writing patterns from prose. Use when drafting, editing, or reviewing text to eliminate predictab...

### 文档与数据类

- [kami](libraries/kami) `kami` - 2 个 skills  
  分类：文档与数据类 | 标签：coding, data, docs, frontend, pdf | 来源：tw93/Kami  
  安装：推荐 `npx skills add tw93/kami/plugins/kami/skills/kami -a '*' -g -y`；也可从 [`extracted-skills/kami`](extracted-skills/kami) 手动复制。  
  简介：Why
  - [kami](libraries/kami/plugins/kami/skills/kami/SKILL.md) `kami` | 可复制：[`extracted-skills/kami/kami`](extracted-skills/kami/kami) - Typeset professional documents and product landing pages: resumes, one-pagers, white papers, letters, portf...
  - [kami](libraries/kami/SKILL.md) `kami-2` | 可复制：[`extracted-skills/kami/kami-2`](extracted-skills/kami/kami-2) - Typeset professional documents and product landing pages: resumes, one-pagers, white papers, letters, portf...

- [SoftwareCopyright-Skill](libraries/SoftwareCopyright-Skill) `softwarecopyright-skill` - 1 个 skills  
  分类：文档与数据类 | 标签：coding, docs | 来源：Fokkyp/SoftwareCopyright-Skill  
  安装：复制 [`extracted-skills/softwarecopyright-skill`](extracted-skills/softwarecopyright-skill) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：Software Copyright Materials Skill
  - [software-copyright-materials](libraries/SoftwareCopyright-Skill/software-copyright-materials/SKILL.md) `software-copyright-materials` | 可复制：[`extracted-skills/softwarecopyright-skill/software-copyright-materials`](extracted-skills/softwarecopyright-skill/software-copyright-materials) - Generate guided Chinese software copyright application materials from a real project. Use this skill when t...

### 自动化流程类

- [skillhub-ingest](libraries/skillhub-ingest) `skillhub-ingest` - 1 个 skills  
  分类：自动化流程类 | 标签：coding, docs, workflow | 来源：local  
  安装：复制 [`extracted-skills/skillhub-ingest`](extracted-skills/skillhub-ingest) 下需要的 skill 到 `~/.claude/skills/`。  
  简介：SkillHub Ingest
  - [skillhub-ingest](libraries/skillhub-ingest/SKILL.md) `skillhub-ingest` | 可复制：[`extracted-skills/skillhub-ingest/skillhub-ingest`](extracted-skills/skillhub-ingest/skillhub-ingest) - Add, classify, extract, document, and validate GitHub-hosted skills in the Skills-Hub repository. Use when...

## 完整索引

- [完整 Skill 库索引](docs/index.md)
- [按分类查看](docs/by-category.md)
- [按标签查看](docs/by-tag.md)
- [按来源查看](docs/by-source.md)
- [安装与提炼说明](docs/install.md)
- [Kami 配色方案提取](docs/kami-color-palette.md)

<!-- SKILLS_INDEX_END -->
