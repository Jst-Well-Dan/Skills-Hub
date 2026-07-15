# 安装与提炼说明

这个仓库保留两份内容：

- `libraries/<library-id>/`：上游 GitHub 项目快照，用来同步和对照来源。
- `extracted-skills/<library-id>/<skill-id>/`：从上游项目中提炼出的可复制 skill。

安装时优先使用上游推荐的 `npx skills` 命令；没有明确命令时，直接复制 `extracted-skills/` 里的对应目录到 `~/.claude/skills/`。

## 项目安装方式

### agent-browser

推荐 `npx skills add vercel-labs/agent-browser`；也可从 [`extracted-skills/agent-browser`](../extracted-skills/agent-browser) 手动复制。

- `agent-browser`：[`extracted-skills/agent-browser/agent-browser`](../extracted-skills/agent-browser/agent-browser)
- `agentcore`：[`extracted-skills/agent-browser/agentcore`](../extracted-skills/agent-browser/agentcore)
- `core`：[`extracted-skills/agent-browser/core`](../extracted-skills/agent-browser/core)
- `dogfood`：[`extracted-skills/agent-browser/dogfood`](../extracted-skills/agent-browser/dogfood)
- `electron`：[`extracted-skills/agent-browser/electron`](../extracted-skills/agent-browser/electron)
- `slack`：[`extracted-skills/agent-browser/slack`](../extracted-skills/agent-browser/slack)
- `vercel-sandbox`：[`extracted-skills/agent-browser/vercel-sandbox`](../extracted-skills/agent-browser/vercel-sandbox)

### agent-skills

推荐 `npx skills add supabase/agent-skills`；也可从 [`extracted-skills/agent-skills`](../extracted-skills/agent-skills) 手动复制。

- `supabase`：[`extracted-skills/agent-skills/supabase`](../extracted-skills/agent-skills/supabase)
- `supabase-postgres-best-practices`：[`extracted-skills/agent-skills/supabase-postgres-best-practices`](../extracted-skills/agent-skills/supabase-postgres-best-practices)

### anthropic

复制 [`extracted-skills/anthropic`](../extracted-skills/anthropic) 下需要的 skill 到 `~/.claude/skills/`。

- `algorithmic-art`：[`extracted-skills/anthropic/algorithmic-art`](../extracted-skills/anthropic/algorithmic-art)
- `brand-guidelines`：[`extracted-skills/anthropic/brand-guidelines`](../extracted-skills/anthropic/brand-guidelines)
- `canvas-design`：[`extracted-skills/anthropic/canvas-design`](../extracted-skills/anthropic/canvas-design)
- `claude-api`：[`extracted-skills/anthropic/claude-api`](../extracted-skills/anthropic/claude-api)
- `doc-coauthoring`：[`extracted-skills/anthropic/doc-coauthoring`](../extracted-skills/anthropic/doc-coauthoring)
- `docx`：[`extracted-skills/anthropic/docx`](../extracted-skills/anthropic/docx)
- `frontend-design`：[`extracted-skills/anthropic/frontend-design`](../extracted-skills/anthropic/frontend-design)
- `internal-comms`：[`extracted-skills/anthropic/internal-comms`](../extracted-skills/anthropic/internal-comms)
- `mcp-builder`：[`extracted-skills/anthropic/mcp-builder`](../extracted-skills/anthropic/mcp-builder)
- `pdf`：[`extracted-skills/anthropic/pdf`](../extracted-skills/anthropic/pdf)
- `pptx`：[`extracted-skills/anthropic/pptx`](../extracted-skills/anthropic/pptx)
- `skill-creator`：[`extracted-skills/anthropic/skill-creator`](../extracted-skills/anthropic/skill-creator)
- `slack-gif-creator`：[`extracted-skills/anthropic/slack-gif-creator`](../extracted-skills/anthropic/slack-gif-creator)
- `template-skill`：[`extracted-skills/anthropic/template-skill`](../extracted-skills/anthropic/template-skill)
- `theme-factory`：[`extracted-skills/anthropic/theme-factory`](../extracted-skills/anthropic/theme-factory)
- `web-artifacts-builder`：[`extracted-skills/anthropic/web-artifacts-builder`](../extracted-skills/anthropic/web-artifacts-builder)
- `webapp-testing`：[`extracted-skills/anthropic/webapp-testing`](../extracted-skills/anthropic/webapp-testing)
- `xlsx`：[`extracted-skills/anthropic/xlsx`](../extracted-skills/anthropic/xlsx)

### baoyu-skills

推荐 `npx skills add jimliu/baoyu-skills`；也可从 [`extracted-skills/baoyu-skills`](../extracted-skills/baoyu-skills) 手动复制。

- `baoyu-article-illustrator`：[`extracted-skills/baoyu-skills/baoyu-article-illustrator`](../extracted-skills/baoyu-skills/baoyu-article-illustrator)
- `baoyu-comic`：[`extracted-skills/baoyu-skills/baoyu-comic`](../extracted-skills/baoyu-skills/baoyu-comic)
- `baoyu-compress-image`：[`extracted-skills/baoyu-skills/baoyu-compress-image`](../extracted-skills/baoyu-skills/baoyu-compress-image)
- `baoyu-cover-image`：[`extracted-skills/baoyu-skills/baoyu-cover-image`](../extracted-skills/baoyu-skills/baoyu-cover-image)
- `baoyu-danger-gemini-web`：[`extracted-skills/baoyu-skills/baoyu-danger-gemini-web`](../extracted-skills/baoyu-skills/baoyu-danger-gemini-web)
- `baoyu-danger-x-to-markdown`：[`extracted-skills/baoyu-skills/baoyu-danger-x-to-markdown`](../extracted-skills/baoyu-skills/baoyu-danger-x-to-markdown)
- `baoyu-diagram`：[`extracted-skills/baoyu-skills/baoyu-diagram`](../extracted-skills/baoyu-skills/baoyu-diagram)
- `baoyu-electron-extract`：[`extracted-skills/baoyu-skills/baoyu-electron-extract`](../extracted-skills/baoyu-skills/baoyu-electron-extract)
- `baoyu-format-markdown`：[`extracted-skills/baoyu-skills/baoyu-format-markdown`](../extracted-skills/baoyu-skills/baoyu-format-markdown)
- `baoyu-image-gen`：[`extracted-skills/baoyu-skills/baoyu-image-gen`](../extracted-skills/baoyu-skills/baoyu-image-gen)
- `baoyu-infographic`：[`extracted-skills/baoyu-skills/baoyu-infographic`](../extracted-skills/baoyu-skills/baoyu-infographic)
- `baoyu-markdown-to-html`：[`extracted-skills/baoyu-skills/baoyu-markdown-to-html`](../extracted-skills/baoyu-skills/baoyu-markdown-to-html)
- `baoyu-post-to-wechat`：[`extracted-skills/baoyu-skills/baoyu-post-to-wechat`](../extracted-skills/baoyu-skills/baoyu-post-to-wechat)
- `baoyu-post-to-weibo`：[`extracted-skills/baoyu-skills/baoyu-post-to-weibo`](../extracted-skills/baoyu-skills/baoyu-post-to-weibo)
- `baoyu-post-to-x`：[`extracted-skills/baoyu-skills/baoyu-post-to-x`](../extracted-skills/baoyu-skills/baoyu-post-to-x)
- `baoyu-slide-deck`：[`extracted-skills/baoyu-skills/baoyu-slide-deck`](../extracted-skills/baoyu-skills/baoyu-slide-deck)
- `baoyu-translate`：[`extracted-skills/baoyu-skills/baoyu-translate`](../extracted-skills/baoyu-skills/baoyu-translate)
- `baoyu-url-to-markdown`：[`extracted-skills/baoyu-skills/baoyu-url-to-markdown`](../extracted-skills/baoyu-skills/baoyu-url-to-markdown)
- `baoyu-wechat-summary`：[`extracted-skills/baoyu-skills/baoyu-wechat-summary`](../extracted-skills/baoyu-skills/baoyu-wechat-summary)
- `baoyu-xhs-images`：[`extracted-skills/baoyu-skills/baoyu-xhs-images`](../extracted-skills/baoyu-skills/baoyu-xhs-images)
- `baoyu-youtube-transcript`：[`extracted-skills/baoyu-skills/baoyu-youtube-transcript`](../extracted-skills/baoyu-skills/baoyu-youtube-transcript)

### codex-complexity-optimizer

复制 [`extracted-skills/codex-complexity-optimizer`](../extracted-skills/codex-complexity-optimizer) 下需要的 skill 到 `~/.claude/skills/`。

- `complexity-optimizer`：[`extracted-skills/codex-complexity-optimizer/complexity-optimizer`](../extracted-skills/codex-complexity-optimizer/complexity-optimizer)

### content-research-writer

复制 [`extracted-skills/content-research-writer`](../extracted-skills/content-research-writer) 下需要的 skill 到 `~/.claude/skills/`。

- `content-research-writer`：[`extracted-skills/content-research-writer/content-research-writer`](../extracted-skills/content-research-writer/content-research-writer)

### context7-cli

复制 [`extracted-skills/context7-cli`](../extracted-skills/context7-cli) 下需要的 skill 到 `~/.claude/skills/`。

- `context7-cli`：[`extracted-skills/context7-cli/context7-cli`](../extracted-skills/context7-cli/context7-cli)

### edgeone-pages-skills

推荐 `npx skills add edgeone-pages/edgeone-pages-skills`；也可从 [`extracted-skills/edgeone-pages-skills`](../extracted-skills/edgeone-pages-skills) 手动复制。

- `edgeone-pages-deploy`：[`extracted-skills/edgeone-pages-skills/edgeone-pages-deploy`](../extracted-skills/edgeone-pages-skills/edgeone-pages-deploy)
- `edgeone-pages-dev`：[`extracted-skills/edgeone-pages-skills/edgeone-pages-dev`](../extracted-skills/edgeone-pages-skills/edgeone-pages-dev)

### frontend-slides

复制 [`extracted-skills/frontend-slides`](../extracted-skills/frontend-slides) 下需要的 skill 到 `~/.claude/skills/`。

- `frontend-slides`：[`extracted-skills/frontend-slides/frontend-slides`](../extracted-skills/frontend-slides/frontend-slides)
- `frontend-slides-2`：[`extracted-skills/frontend-slides/frontend-slides-2`](../extracted-skills/frontend-slides/frontend-slides-2)

### gsap-skills

复制 [`extracted-skills/gsap-skills`](../extracted-skills/gsap-skills) 下需要的 skill 到 `~/.claude/skills/`。

- `gsap-core`：[`extracted-skills/gsap-skills/gsap-core`](../extracted-skills/gsap-skills/gsap-core)
- `gsap-frameworks`：[`extracted-skills/gsap-skills/gsap-frameworks`](../extracted-skills/gsap-skills/gsap-frameworks)
- `gsap-performance`：[`extracted-skills/gsap-skills/gsap-performance`](../extracted-skills/gsap-skills/gsap-performance)
- `gsap-plugins`：[`extracted-skills/gsap-skills/gsap-plugins`](../extracted-skills/gsap-skills/gsap-plugins)
- `gsap-react`：[`extracted-skills/gsap-skills/gsap-react`](../extracted-skills/gsap-skills/gsap-react)
- `gsap-scrolltrigger`：[`extracted-skills/gsap-skills/gsap-scrolltrigger`](../extracted-skills/gsap-skills/gsap-scrolltrigger)
- `gsap-timeline`：[`extracted-skills/gsap-skills/gsap-timeline`](../extracted-skills/gsap-skills/gsap-timeline)
- `gsap-utils`：[`extracted-skills/gsap-skills/gsap-utils`](../extracted-skills/gsap-skills/gsap-utils)

### guizang-ppt-skill

推荐 `npx skills add https://github.com/op7418/guizang-ppt-skill --skill guizang-ppt-skill`；也可从 [`extracted-skills/guizang-ppt-skill`](../extracted-skills/guizang-ppt-skill) 手动复制。

- `guizang-ppt-skill`：[`extracted-skills/guizang-ppt-skill/guizang-ppt-skill`](../extracted-skills/guizang-ppt-skill/guizang-ppt-skill)

### guizang-social-card-skill

推荐 `npx skills add https://github.com/op7418/guizang-social-card-skill --skill guizang-social-card-skill`；也可从 [`extracted-skills/guizang-social-card-skill`](../extracted-skills/guizang-social-card-skill) 手动复制。

- `guizang-social-card-skill`：[`extracted-skills/guizang-social-card-skill/guizang-social-card-skill`](../extracted-skills/guizang-social-card-skill/guizang-social-card-skill)

### html-anything

复制 [`extracted-skills/html-anything`](../extracted-skills/html-anything) 下需要的 skill 到 `~/.claude/skills/`。

- `article-magazine`：[`extracted-skills/html-anything/article-magazine`](../extracted-skills/html-anything/article-magazine)
- `blog-post`：[`extracted-skills/html-anything/blog-post`](../extracted-skills/html-anything/blog-post)
- `card-twitter`：[`extracted-skills/html-anything/card-twitter`](../extracted-skills/html-anything/card-twitter)
- `card-xiaohongshu`：[`extracted-skills/html-anything/card-xiaohongshu`](../extracted-skills/html-anything/card-xiaohongshu)
- `competitive-teardown`：[`extracted-skills/html-anything/competitive-teardown`](../extracted-skills/html-anything/competitive-teardown)
- `dashboard`：[`extracted-skills/html-anything/dashboard`](../extracted-skills/html-anything/dashboard)
- `data-report`：[`extracted-skills/html-anything/data-report`](../extracted-skills/html-anything/data-report)
- `dating-web`：[`extracted-skills/html-anything/dating-web`](../extracted-skills/html-anything/dating-web)
- `deck-blueprint`：[`extracted-skills/html-anything/deck-blueprint`](../extracted-skills/html-anything/deck-blueprint)
- `deck-course-module`：[`extracted-skills/html-anything/deck-course-module`](../extracted-skills/html-anything/deck-course-module)
- `deck-dir-key-nav`：[`extracted-skills/html-anything/deck-dir-key-nav`](../extracted-skills/html-anything/deck-dir-key-nav)
- `deck-graphify-dark`：[`extracted-skills/html-anything/deck-graphify-dark`](../extracted-skills/html-anything/deck-graphify-dark)
- `deck-guizang-editorial`：[`extracted-skills/html-anything/deck-guizang-editorial`](../extracted-skills/html-anything/deck-guizang-editorial)
- `deck-hermes-cyber`：[`extracted-skills/html-anything/deck-hermes-cyber`](../extracted-skills/html-anything/deck-hermes-cyber)
- `deck-magazine-web`：[`extracted-skills/html-anything/deck-magazine-web`](../extracted-skills/html-anything/deck-magazine-web)
- `deck-obsidian-claude`：[`extracted-skills/html-anything/deck-obsidian-claude`](../extracted-skills/html-anything/deck-obsidian-claude)
- `deck-open-slide-canvas`：[`extracted-skills/html-anything/deck-open-slide-canvas`](../extracted-skills/html-anything/deck-open-slide-canvas)
- `deck-pitch`：[`extracted-skills/html-anything/deck-pitch`](../extracted-skills/html-anything/deck-pitch)
- `deck-presenter-mode`：[`extracted-skills/html-anything/deck-presenter-mode`](../extracted-skills/html-anything/deck-presenter-mode)
- `deck-product-launch`：[`extracted-skills/html-anything/deck-product-launch`](../extracted-skills/html-anything/deck-product-launch)
- `deck-replit`：[`extracted-skills/html-anything/deck-replit`](../extracted-skills/html-anything/deck-replit)
- `deck-safety-alert`：[`extracted-skills/html-anything/deck-safety-alert`](../extracted-skills/html-anything/deck-safety-alert)
- `deck-simple`：[`extracted-skills/html-anything/deck-simple`](../extracted-skills/html-anything/deck-simple)
- `deck-swiss-international`：[`extracted-skills/html-anything/deck-swiss-international`](../extracted-skills/html-anything/deck-swiss-international)
- `deck-tech-sharing`：[`extracted-skills/html-anything/deck-tech-sharing`](../extracted-skills/html-anything/deck-tech-sharing)
- `deck-xhs-pastel`：[`extracted-skills/html-anything/deck-xhs-pastel`](../extracted-skills/html-anything/deck-xhs-pastel)
- `deck-xhs-post`：[`extracted-skills/html-anything/deck-xhs-post`](../extracted-skills/html-anything/deck-xhs-post)
- `deck-xhs-white`：[`extracted-skills/html-anything/deck-xhs-white`](../extracted-skills/html-anything/deck-xhs-white)
- `digital-eguide`：[`extracted-skills/html-anything/digital-eguide`](../extracted-skills/html-anything/digital-eguide)
- `doc-kami-parchment`：[`extracted-skills/html-anything/doc-kami-parchment`](../extracted-skills/html-anything/doc-kami-parchment)
- `docs-page`：[`extracted-skills/html-anything/docs-page`](../extracted-skills/html-anything/docs-page)
- `email-marketing`：[`extracted-skills/html-anything/email-marketing`](../extracted-skills/html-anything/email-marketing)
- `eng-runbook`：[`extracted-skills/html-anything/eng-runbook`](../extracted-skills/html-anything/eng-runbook)
- `exec-briefing-memo`：[`extracted-skills/html-anything/exec-briefing-memo`](../extracted-skills/html-anything/exec-briefing-memo)
- `experiment-readout`：[`extracted-skills/html-anything/experiment-readout`](../extracted-skills/html-anything/experiment-readout)
- `finance-report`：[`extracted-skills/html-anything/finance-report`](../extracted-skills/html-anything/finance-report)
- `flowai-team-dashboard`：[`extracted-skills/html-anything/flowai-team-dashboard`](../extracted-skills/html-anything/flowai-team-dashboard)
- `frame-data-chart-nyt`：[`extracted-skills/html-anything/frame-data-chart-nyt`](../extracted-skills/html-anything/frame-data-chart-nyt)
- `frame-flowchart-sticky`：[`extracted-skills/html-anything/frame-flowchart-sticky`](../extracted-skills/html-anything/frame-flowchart-sticky)
- `frame-glitch-title`：[`extracted-skills/html-anything/frame-glitch-title`](../extracted-skills/html-anything/frame-glitch-title)
- `frame-light-leak-cinema`：[`extracted-skills/html-anything/frame-light-leak-cinema`](../extracted-skills/html-anything/frame-light-leak-cinema)
- `frame-liquid-bg-hero`：[`extracted-skills/html-anything/frame-liquid-bg-hero`](../extracted-skills/html-anything/frame-liquid-bg-hero)
- `frame-logo-outro`：[`extracted-skills/html-anything/frame-logo-outro`](../extracted-skills/html-anything/frame-logo-outro)
- `frame-macos-notification`：[`extracted-skills/html-anything/frame-macos-notification`](../extracted-skills/html-anything/frame-macos-notification)
- `gamified-app`：[`extracted-skills/html-anything/gamified-app`](../extracted-skills/html-anything/gamified-app)
- `hr-onboarding`：[`extracted-skills/html-anything/hr-onboarding`](../extracted-skills/html-anything/hr-onboarding)
- `invoice`：[`extracted-skills/html-anything/invoice`](../extracted-skills/html-anything/invoice)
- `kanban-board`：[`extracted-skills/html-anything/kanban-board`](../extracted-skills/html-anything/kanban-board)
- `live-dashboard`：[`extracted-skills/html-anything/live-dashboard`](../extracted-skills/html-anything/live-dashboard)
- `magazine-poster`：[`extracted-skills/html-anything/magazine-poster`](../extracted-skills/html-anything/magazine-poster)
- `meeting-notes`：[`extracted-skills/html-anything/meeting-notes`](../extracted-skills/html-anything/meeting-notes)
- `mobile-app`：[`extracted-skills/html-anything/mobile-app`](../extracted-skills/html-anything/mobile-app)
- `mobile-onboarding`：[`extracted-skills/html-anything/mobile-onboarding`](../extracted-skills/html-anything/mobile-onboarding)
- `mockup-device-3d`：[`extracted-skills/html-anything/mockup-device-3d`](../extracted-skills/html-anything/mockup-device-3d)
- `motion-frames`：[`extracted-skills/html-anything/motion-frames`](../extracted-skills/html-anything/motion-frames)
- `pm-spec`：[`extracted-skills/html-anything/pm-spec`](../extracted-skills/html-anything/pm-spec)
- `poster-hero`：[`extracted-skills/html-anything/poster-hero`](../extracted-skills/html-anything/poster-hero)
- `ppt-keynote`：[`extracted-skills/html-anything/ppt-keynote`](../extracted-skills/html-anything/ppt-keynote)
- `pricing-page`：[`extracted-skills/html-anything/pricing-page`](../extracted-skills/html-anything/pricing-page)
- `prototype-web`：[`extracted-skills/html-anything/prototype-web`](../extracted-skills/html-anything/prototype-web)
- `resume-modern`：[`extracted-skills/html-anything/resume-modern`](../extracted-skills/html-anything/resume-modern)
- `saas-landing`：[`extracted-skills/html-anything/saas-landing`](../extracted-skills/html-anything/saas-landing)
- `social-carousel`：[`extracted-skills/html-anything/social-carousel`](../extracted-skills/html-anything/social-carousel)
- `social-media-dashboard`：[`extracted-skills/html-anything/social-media-dashboard`](../extracted-skills/html-anything/social-media-dashboard)
- `social-media-matrix`：[`extracted-skills/html-anything/social-media-matrix`](../extracted-skills/html-anything/social-media-matrix)
- `social-reddit-card`：[`extracted-skills/html-anything/social-reddit-card`](../extracted-skills/html-anything/social-reddit-card)
- `social-spotify-card`：[`extracted-skills/html-anything/social-spotify-card`](../extracted-skills/html-anything/social-spotify-card)
- `social-x-post-card`：[`extracted-skills/html-anything/social-x-post-card`](../extracted-skills/html-anything/social-x-post-card)
- `sprite-animation`：[`extracted-skills/html-anything/sprite-animation`](../extracted-skills/html-anything/sprite-animation)
- `team-okrs`：[`extracted-skills/html-anything/team-okrs`](../extracted-skills/html-anything/team-okrs)
- `vfx-text-cursor`：[`extracted-skills/html-anything/vfx-text-cursor`](../extracted-skills/html-anything/vfx-text-cursor)
- `video-hyperframes`：[`extracted-skills/html-anything/video-hyperframes`](../extracted-skills/html-anything/video-hyperframes)
- `waitlist-page`：[`extracted-skills/html-anything/waitlist-page`](../extracted-skills/html-anything/waitlist-page)
- `web-proto-brutalist`：[`extracted-skills/html-anything/web-proto-brutalist`](../extracted-skills/html-anything/web-proto-brutalist)
- `web-proto-editorial`：[`extracted-skills/html-anything/web-proto-editorial`](../extracted-skills/html-anything/web-proto-editorial)
- `web-proto-soft`：[`extracted-skills/html-anything/web-proto-soft`](../extracted-skills/html-anything/web-proto-soft)
- `weekly-update`：[`extracted-skills/html-anything/weekly-update`](../extracted-skills/html-anything/weekly-update)
- `wireframe-sketch`：[`extracted-skills/html-anything/wireframe-sketch`](../extracted-skills/html-anything/wireframe-sketch)

### huashu-md-html

推荐 `npx skills add alchaincyf/huashu-md-html`；也可从 [`extracted-skills/huashu-md-html`](../extracted-skills/huashu-md-html) 手动复制。

- `huashu-md-html`：[`extracted-skills/huashu-md-html/huashu-md-html`](../extracted-skills/huashu-md-html/huashu-md-html)

### huashu-skills

复制 [`extracted-skills/huashu-skills`](../extracted-skills/huashu-skills) 下需要的 skill 到 `~/.claude/skills/`。

- `huashu-agent-swarm`：[`extracted-skills/huashu-skills/huashu-agent-swarm`](../extracted-skills/huashu-skills/huashu-agent-swarm)
- `huashu-article-edit`：[`extracted-skills/huashu-skills/huashu-article-edit`](../extracted-skills/huashu-skills/huashu-article-edit)
- `huashu-article-to-x`：[`extracted-skills/huashu-skills/huashu-article-to-x`](../extracted-skills/huashu-skills/huashu-article-to-x)
- `huashu-data-pro`：[`extracted-skills/huashu-skills/huashu-data-pro`](../extracted-skills/huashu-skills/huashu-data-pro)
- `huashu-design`：[`extracted-skills/huashu-skills/huashu-design`](../extracted-skills/huashu-skills/huashu-design)
- `huashu-douyin-script`：[`extracted-skills/huashu-skills/huashu-douyin-script`](../extracted-skills/huashu-skills/huashu-douyin-script)
- `huashu-image-upload`：[`extracted-skills/huashu-skills/huashu-image-upload`](../extracted-skills/huashu-skills/huashu-image-upload)
- `huashu-info-search`：[`extracted-skills/huashu-skills/huashu-info-search`](../extracted-skills/huashu-skills/huashu-info-search)
- `huashu-material-search`：[`extracted-skills/huashu-skills/huashu-material-search`](../extracted-skills/huashu-skills/huashu-material-search)
- `huashu-md-to-pdf`：[`extracted-skills/huashu-skills/huashu-md-to-pdf`](../extracted-skills/huashu-skills/huashu-md-to-pdf)
- `huashu-prompt-save`：[`extracted-skills/huashu-skills/huashu-prompt-save`](../extracted-skills/huashu-skills/huashu-prompt-save)
- `huashu-proofreading`：[`extracted-skills/huashu-skills/huashu-proofreading`](../extracted-skills/huashu-skills/huashu-proofreading)
- `huashu-research`：[`extracted-skills/huashu-skills/huashu-research`](../extracted-skills/huashu-skills/huashu-research)
- `huashu-script-polish`：[`extracted-skills/huashu-skills/huashu-script-polish`](../extracted-skills/huashu-skills/huashu-script-polish)
- `huashu-slides`：[`extracted-skills/huashu-skills/huashu-slides`](../extracted-skills/huashu-skills/huashu-slides)
- `huashu-speech-coach`：[`extracted-skills/huashu-skills/huashu-speech-coach`](../extracted-skills/huashu-skills/huashu-speech-coach)
- `huashu-topic-gen`：[`extracted-skills/huashu-skills/huashu-topic-gen`](../extracted-skills/huashu-skills/huashu-topic-gen)
- `huashu-video-check`：[`extracted-skills/huashu-skills/huashu-video-check`](../extracted-skills/huashu-skills/huashu-video-check)
- `huashu-video-outline`：[`extracted-skills/huashu-skills/huashu-video-outline`](../extracted-skills/huashu-skills/huashu-video-outline)
- `huashu-wechat-image`：[`extracted-skills/huashu-skills/huashu-wechat-image`](../extracted-skills/huashu-skills/huashu-wechat-image)
- `huashu-xhs-image`：[`extracted-skills/huashu-skills/huashu-xhs-image`](../extracted-skills/huashu-skills/huashu-xhs-image)

### impeccable

推荐 `npx impeccable skills install`；也可从 [`extracted-skills/impeccable`](../extracted-skills/impeccable) 手动复制。

- `impeccable`：[`extracted-skills/impeccable/impeccable`](../extracted-skills/impeccable/impeccable)

### kami

推荐 `npx skills add tw93/kami/plugins/kami/skills/kami -a '*' -g -y`；也可从 [`extracted-skills/kami`](../extracted-skills/kami) 手动复制。

- `kami`：[`extracted-skills/kami/kami`](../extracted-skills/kami/kami)
- `kami-2`：[`extracted-skills/kami/kami-2`](../extracted-skills/kami/kami-2)

### ljg-skills

推荐 `npx skills add lijigang/ljg-skills -g --all`；也可从 [`extracted-skills/ljg-skills`](../extracted-skills/ljg-skills) 手动复制。

- `ljg-book`：[`extracted-skills/ljg-skills/ljg-book`](../extracted-skills/ljg-skills/ljg-book)
- `ljg-card`：[`extracted-skills/ljg-skills/ljg-card`](../extracted-skills/ljg-skills/ljg-card)
- `ljg-invest`：[`extracted-skills/ljg-skills/ljg-invest`](../extracted-skills/ljg-skills/ljg-invest)
- `ljg-learn`：[`extracted-skills/ljg-skills/ljg-learn`](../extracted-skills/ljg-skills/ljg-learn)
- `ljg-library`：[`extracted-skills/ljg-skills/ljg-library`](../extracted-skills/ljg-skills/ljg-library)
- `ljg-map`：[`extracted-skills/ljg-skills/ljg-map`](../extracted-skills/ljg-skills/ljg-map)
- `ljg-paper`：[`extracted-skills/ljg-skills/ljg-paper`](../extracted-skills/ljg-skills/ljg-paper)
- `ljg-paper-flow`：[`extracted-skills/ljg-skills/ljg-paper-flow`](../extracted-skills/ljg-skills/ljg-paper-flow)
- `ljg-paper-river`：[`extracted-skills/ljg-skills/ljg-paper-river`](../extracted-skills/ljg-skills/ljg-paper-river)
- `ljg-plain`：[`extracted-skills/ljg-skills/ljg-plain`](../extracted-skills/ljg-skills/ljg-plain)
- `ljg-present`：[`extracted-skills/ljg-skills/ljg-present`](../extracted-skills/ljg-skills/ljg-present)
- `ljg-push`：[`extracted-skills/ljg-skills/ljg-push`](../extracted-skills/ljg-skills/ljg-push)
- `ljg-qa`：[`extracted-skills/ljg-skills/ljg-qa`](../extracted-skills/ljg-skills/ljg-qa)
- `ljg-rank`：[`extracted-skills/ljg-skills/ljg-rank`](../extracted-skills/ljg-skills/ljg-rank)
- `ljg-read`：[`extracted-skills/ljg-skills/ljg-read`](../extracted-skills/ljg-skills/ljg-read)
- `ljg-relationship`：[`extracted-skills/ljg-skills/ljg-relationship`](../extracted-skills/ljg-skills/ljg-relationship)
- `ljg-roundtable`：[`extracted-skills/ljg-skills/ljg-roundtable`](../extracted-skills/ljg-skills/ljg-roundtable)
- `ljg-skill-map`：[`extracted-skills/ljg-skills/ljg-skill-map`](../extracted-skills/ljg-skills/ljg-skill-map)
- `ljg-think`：[`extracted-skills/ljg-skills/ljg-think`](../extracted-skills/ljg-skills/ljg-think)
- `ljg-travel`：[`extracted-skills/ljg-skills/ljg-travel`](../extracted-skills/ljg-skills/ljg-travel)
- `ljg-word`：[`extracted-skills/ljg-skills/ljg-word`](../extracted-skills/ljg-skills/ljg-word)
- `ljg-word-flow`：[`extracted-skills/ljg-skills/ljg-word-flow`](../extracted-skills/ljg-skills/ljg-word-flow)
- `ljg-writes`：[`extracted-skills/ljg-skills/ljg-writes`](../extracted-skills/ljg-skills/ljg-writes)

### lottie

复制 [`extracted-skills/lottie`](../extracted-skills/lottie) 下需要的 skill 到 `~/.claude/skills/`。

- `text-to-lottie`：[`extracted-skills/lottie/text-to-lottie`](../extracted-skills/lottie/text-to-lottie)

### mattpocock-skills

复制 [`extracted-skills/mattpocock-skills`](../extracted-skills/mattpocock-skills) 下需要的 skill 到 `~/.claude/skills/`。

- `ask-matt`：[`extracted-skills/mattpocock-skills/ask-matt`](../extracted-skills/mattpocock-skills/ask-matt)
- `code-review`：[`extracted-skills/mattpocock-skills/code-review`](../extracted-skills/mattpocock-skills/code-review)
- `codebase-design`：[`extracted-skills/mattpocock-skills/codebase-design`](../extracted-skills/mattpocock-skills/codebase-design)
- `design-an-interface`：[`extracted-skills/mattpocock-skills/design-an-interface`](../extracted-skills/mattpocock-skills/design-an-interface)
- `diagnosing-bugs`：[`extracted-skills/mattpocock-skills/diagnosing-bugs`](../extracted-skills/mattpocock-skills/diagnosing-bugs)
- `domain-modeling`：[`extracted-skills/mattpocock-skills/domain-modeling`](../extracted-skills/mattpocock-skills/domain-modeling)
- `edit-article`：[`extracted-skills/mattpocock-skills/edit-article`](../extracted-skills/mattpocock-skills/edit-article)
- `git-guardrails-claude-code`：[`extracted-skills/mattpocock-skills/git-guardrails-claude-code`](../extracted-skills/mattpocock-skills/git-guardrails-claude-code)
- `grill-me`：[`extracted-skills/mattpocock-skills/grill-me`](../extracted-skills/mattpocock-skills/grill-me)
- `grill-with-docs`：[`extracted-skills/mattpocock-skills/grill-with-docs`](../extracted-skills/mattpocock-skills/grill-with-docs)
- `grilling`：[`extracted-skills/mattpocock-skills/grilling`](../extracted-skills/mattpocock-skills/grilling)
- `handoff`：[`extracted-skills/mattpocock-skills/handoff`](../extracted-skills/mattpocock-skills/handoff)
- `implement`：[`extracted-skills/mattpocock-skills/implement`](../extracted-skills/mattpocock-skills/implement)
- `improve-codebase-architecture`：[`extracted-skills/mattpocock-skills/improve-codebase-architecture`](../extracted-skills/mattpocock-skills/improve-codebase-architecture)
- `loop-me`：[`extracted-skills/mattpocock-skills/loop-me`](../extracted-skills/mattpocock-skills/loop-me)
- `migrate-to-shoehorn`：[`extracted-skills/mattpocock-skills/migrate-to-shoehorn`](../extracted-skills/mattpocock-skills/migrate-to-shoehorn)
- `obsidian-vault`：[`extracted-skills/mattpocock-skills/obsidian-vault`](../extracted-skills/mattpocock-skills/obsidian-vault)
- `prototype`：[`extracted-skills/mattpocock-skills/prototype`](../extracted-skills/mattpocock-skills/prototype)
- `qa`：[`extracted-skills/mattpocock-skills/qa`](../extracted-skills/mattpocock-skills/qa)
- `request-refactor-plan`：[`extracted-skills/mattpocock-skills/request-refactor-plan`](../extracted-skills/mattpocock-skills/request-refactor-plan)
- `resolving-merge-conflicts`：[`extracted-skills/mattpocock-skills/resolving-merge-conflicts`](../extracted-skills/mattpocock-skills/resolving-merge-conflicts)
- `scaffold-exercises`：[`extracted-skills/mattpocock-skills/scaffold-exercises`](../extracted-skills/mattpocock-skills/scaffold-exercises)
- `setup-matt-pocock-skills`：[`extracted-skills/mattpocock-skills/setup-matt-pocock-skills`](../extracted-skills/mattpocock-skills/setup-matt-pocock-skills)
- `setup-pre-commit`：[`extracted-skills/mattpocock-skills/setup-pre-commit`](../extracted-skills/mattpocock-skills/setup-pre-commit)
- `tdd`：[`extracted-skills/mattpocock-skills/tdd`](../extracted-skills/mattpocock-skills/tdd)
- `teach`：[`extracted-skills/mattpocock-skills/teach`](../extracted-skills/mattpocock-skills/teach)
- `to-issues`：[`extracted-skills/mattpocock-skills/to-issues`](../extracted-skills/mattpocock-skills/to-issues)
- `to-prd`：[`extracted-skills/mattpocock-skills/to-prd`](../extracted-skills/mattpocock-skills/to-prd)
- `triage`：[`extracted-skills/mattpocock-skills/triage`](../extracted-skills/mattpocock-skills/triage)
- `ubiquitous-language`：[`extracted-skills/mattpocock-skills/ubiquitous-language`](../extracted-skills/mattpocock-skills/ubiquitous-language)
- `wayfinder`：[`extracted-skills/mattpocock-skills/wayfinder`](../extracted-skills/mattpocock-skills/wayfinder)
- `wizard`：[`extracted-skills/mattpocock-skills/wizard`](../extracted-skills/mattpocock-skills/wizard)
- `writing-beats`：[`extracted-skills/mattpocock-skills/writing-beats`](../extracted-skills/mattpocock-skills/writing-beats)
- `writing-fragments`：[`extracted-skills/mattpocock-skills/writing-fragments`](../extracted-skills/mattpocock-skills/writing-fragments)
- `writing-great-skills`：[`extracted-skills/mattpocock-skills/writing-great-skills`](../extracted-skills/mattpocock-skills/writing-great-skills)
- `writing-shape`：[`extracted-skills/mattpocock-skills/writing-shape`](../extracted-skills/mattpocock-skills/writing-shape)

### mineru

复制 [`extracted-skills/mineru`](../extracted-skills/mineru) 下需要的 skill 到 `~/.claude/skills/`。

- `mineru-document-extractor`：[`extracted-skills/mineru/mineru-document-extractor`](../extracted-skills/mineru/mineru-document-extractor)

### notebooklm

推荐 `npx skills add teng-lin/notebooklm-py`；也可从 [`extracted-skills/notebooklm`](../extracted-skills/notebooklm) 手动复制。

- `notebooklm`：[`extracted-skills/notebooklm/notebooklm`](../extracted-skills/notebooklm/notebooklm)

### obsidian-skills

推荐 `npx skills add git@github.com:kepano/obsidian-skills.git`；也可从 [`extracted-skills/obsidian-skills`](../extracted-skills/obsidian-skills) 手动复制。

- `defuddle`：[`extracted-skills/obsidian-skills/defuddle`](../extracted-skills/obsidian-skills/defuddle)
- `json-canvas`：[`extracted-skills/obsidian-skills/json-canvas`](../extracted-skills/obsidian-skills/json-canvas)
- `obsidian-bases`：[`extracted-skills/obsidian-skills/obsidian-bases`](../extracted-skills/obsidian-skills/obsidian-bases)
- `obsidian-cli`：[`extracted-skills/obsidian-skills/obsidian-cli`](../extracted-skills/obsidian-skills/obsidian-cli)
- `obsidian-markdown`：[`extracted-skills/obsidian-skills/obsidian-markdown`](../extracted-skills/obsidian-skills/obsidian-markdown)

### ponytail

复制 [`extracted-skills/ponytail`](../extracted-skills/ponytail) 下需要的 skill 到 `~/.claude/skills/`。

- `ponytail`：[`extracted-skills/ponytail/ponytail`](../extracted-skills/ponytail/ponytail)
- `ponytail-audit`：[`extracted-skills/ponytail/ponytail-audit`](../extracted-skills/ponytail/ponytail-audit)
- `ponytail-debt`：[`extracted-skills/ponytail/ponytail-debt`](../extracted-skills/ponytail/ponytail-debt)
- `ponytail-gain`：[`extracted-skills/ponytail/ponytail-gain`](../extracted-skills/ponytail/ponytail-gain)
- `ponytail-help`：[`extracted-skills/ponytail/ponytail-help`](../extracted-skills/ponytail/ponytail-help)
- `ponytail-review`：[`extracted-skills/ponytail/ponytail-review`](../extracted-skills/ponytail/ponytail-review)

### punk-skill

复制 [`extracted-skills/punk-skill`](../extracted-skills/punk-skill) 下需要的 skill 到 `~/.claude/skills/`。

- `punk-avatar`：[`extracted-skills/punk-skill/punk-avatar`](../extracted-skills/punk-skill/punk-avatar)
- `punk-cover`：[`extracted-skills/punk-skill/punk-cover`](../extracted-skills/punk-skill/punk-cover)

### skillhub-ingest

复制 [`extracted-skills/skillhub-ingest`](../extracted-skills/skillhub-ingest) 下需要的 skill 到 `~/.claude/skills/`。

- `skillhub-ingest`：[`extracted-skills/skillhub-ingest/skillhub-ingest`](../extracted-skills/skillhub-ingest/skillhub-ingest)

### SoftwareCopyright-Skill

复制 [`extracted-skills/softwarecopyright-skill`](../extracted-skills/softwarecopyright-skill) 下需要的 skill 到 `~/.claude/skills/`。

- `software-copyright-materials`：[`extracted-skills/softwarecopyright-skill/software-copyright-materials`](../extracted-skills/softwarecopyright-skill/software-copyright-materials)

### stop-slop

复制 [`extracted-skills/stop-slop`](../extracted-skills/stop-slop) 下需要的 skill 到 `~/.claude/skills/`。

- `stop-slop`：[`extracted-skills/stop-slop/stop-slop`](../extracted-skills/stop-slop/stop-slop)

### swyxio-skills

复制 [`extracted-skills/swyxio-skills`](../extracted-skills/swyxio-skills) 下需要的 skill 到 `~/.claude/skills/`。

- `accelevents-api`：[`extracted-skills/swyxio-skills/accelevents-api`](../extracted-skills/swyxio-skills/accelevents-api)
- `accelevents-speaker-sync`：[`extracted-skills/swyxio-skills/accelevents-speaker-sync`](../extracted-skills/swyxio-skills/accelevents-speaker-sync)
- `antislop-codebase`：[`extracted-skills/swyxio-skills/antislop-codebase`](../extracted-skills/swyxio-skills/antislop-codebase)
- `app-ux-paradigms`：[`extracted-skills/swyxio-skills/app-ux-paradigms`](../extracted-skills/swyxio-skills/app-ux-paradigms)
- `autoreview`：[`extracted-skills/swyxio-skills/autoreview`](../extracted-skills/swyxio-skills/autoreview)
- `claude-session-introspect`：[`extracted-skills/swyxio-skills/claude-session-introspect`](../extracted-skills/swyxio-skills/claude-session-introspect)
- `codebase-maintainability-guardrails`：[`extracted-skills/swyxio-skills/codebase-maintainability-guardrails`](../extracted-skills/swyxio-skills/codebase-maintainability-guardrails)
- `conference-developer-endpoints`：[`extracted-skills/swyxio-skills/conference-developer-endpoints`](../extracted-skills/swyxio-skills/conference-developer-endpoints)
- `conference-transcribe`：[`extracted-skills/swyxio-skills/conference-transcribe`](../extracted-skills/swyxio-skills/conference-transcribe)
- `data-chatbots`：[`extracted-skills/swyxio-skills/data-chatbots`](../extracted-skills/swyxio-skills/data-chatbots)
- `download-video`：[`extracted-skills/swyxio-skills/download-video`](../extracted-skills/swyxio-skills/download-video)
- `download-x-video`：[`extracted-skills/swyxio-skills/download-x-video`](../extracted-skills/swyxio-skills/download-x-video)
- `europe-developer-api`：[`extracted-skills/swyxio-skills/europe-developer-api`](../extracted-skills/swyxio-skills/europe-developer-api)
- `media-transform`：[`extracted-skills/swyxio-skills/media-transform`](../extracted-skills/swyxio-skills/media-transform)
- `multimodal-extraction`：[`extracted-skills/swyxio-skills/multimodal-extraction`](../extracted-skills/swyxio-skills/multimodal-extraction)
- `new-mac-setup`：[`extracted-skills/swyxio-skills/new-mac-setup`](../extracted-skills/swyxio-skills/new-mac-setup)
- `observability-hardening`：[`extracted-skills/swyxio-skills/observability-hardening`](../extracted-skills/swyxio-skills/observability-hardening)
- `podcast-publishing-assistant`：[`extracted-skills/swyxio-skills/podcast-publishing-assistant`](../extracted-skills/swyxio-skills/podcast-publishing-assistant)
- `productionize-app-with-services`：[`extracted-skills/swyxio-skills/productionize-app-with-services`](../extracted-skills/swyxio-skills/productionize-app-with-services)
- `public-qa-chatbot`：[`extracted-skills/swyxio-skills/public-qa-chatbot`](../extracted-skills/swyxio-skills/public-qa-chatbot)
- `release-readiness-hardening`：[`extracted-skills/swyxio-skills/release-readiness-hardening`](../extracted-skills/swyxio-skills/release-readiness-hardening)
- `schedule-design`：[`extracted-skills/swyxio-skills/schedule-design`](../extracted-skills/swyxio-skills/schedule-design)
- `security-hardening`：[`extracted-skills/swyxio-skills/security-hardening`](../extracted-skills/swyxio-skills/security-hardening)
- `slackbot-builder`：[`extracted-skills/swyxio-skills/slackbot-builder`](../extracted-skills/swyxio-skills/slackbot-builder)
- `smart-entity-resolution`：[`extracted-skills/swyxio-skills/smart-entity-resolution`](../extracted-skills/swyxio-skills/smart-entity-resolution)
- `summarize-anything`：[`extracted-skills/swyxio-skills/summarize-anything`](../extracted-skills/swyxio-skills/summarize-anything)
- `sync-accelevents`：[`extracted-skills/swyxio-skills/sync-accelevents`](../extracted-skills/swyxio-skills/sync-accelevents)
- `sync-url-navigation`：[`extracted-skills/swyxio-skills/sync-url-navigation`](../extracted-skills/swyxio-skills/sync-url-navigation)
- `test-strategy-hardening`：[`extracted-skills/swyxio-skills/test-strategy-hardening`](../extracted-skills/swyxio-skills/test-strategy-hardening)
- `testing-schedule-preview`：[`extracted-skills/swyxio-skills/testing-schedule-preview`](../extracted-skills/swyxio-skills/testing-schedule-preview)
- `thumbnail-extraction`：[`extracted-skills/swyxio-skills/thumbnail-extraction`](../extracted-skills/swyxio-skills/thumbnail-extraction)
- `transcribe-anything`：[`extracted-skills/swyxio-skills/transcribe-anything`](../extracted-skills/swyxio-skills/transcribe-anything)
- `twitter-x-scraping`：[`extracted-skills/swyxio-skills/twitter-x-scraping`](../extracted-skills/swyxio-skills/twitter-x-scraping)
- `web-animation-perf`：[`extracted-skills/swyxio-skills/web-animation-perf`](../extracted-skills/swyxio-skills/web-animation-perf)
- `youtube-api`：[`extracted-skills/swyxio-skills/youtube-api`](../extracted-skills/swyxio-skills/youtube-api)
- `youtube-publish`：[`extracted-skills/swyxio-skills/youtube-publish`](../extracted-skills/swyxio-skills/youtube-publish)
- `youtube-studio-batch-upload`：[`extracted-skills/swyxio-skills/youtube-studio-batch-upload`](../extracted-skills/swyxio-skills/youtube-studio-batch-upload)
- `youtube-thumbnails`：[`extracted-skills/swyxio-skills/youtube-thumbnails`](../extracted-skills/swyxio-skills/youtube-thumbnails)
- `zoom-download`：[`extracted-skills/swyxio-skills/zoom-download`](../extracted-skills/swyxio-skills/zoom-download)

### taste-skill

复制 [`extracted-skills/taste-skill`](../extracted-skills/taste-skill) 下需要的 skill 到 `~/.claude/skills/`。

- `brandkit`：[`extracted-skills/taste-skill/brandkit`](../extracted-skills/taste-skill/brandkit)
- `design-taste-frontend`：[`extracted-skills/taste-skill/design-taste-frontend`](../extracted-skills/taste-skill/design-taste-frontend)
- `design-taste-frontend-v1`：[`extracted-skills/taste-skill/design-taste-frontend-v1`](../extracted-skills/taste-skill/design-taste-frontend-v1)
- `full-output-enforcement`：[`extracted-skills/taste-skill/full-output-enforcement`](../extracted-skills/taste-skill/full-output-enforcement)
- `gpt-taste`：[`extracted-skills/taste-skill/gpt-taste`](../extracted-skills/taste-skill/gpt-taste)
- `high-end-visual-design`：[`extracted-skills/taste-skill/high-end-visual-design`](../extracted-skills/taste-skill/high-end-visual-design)
- `image-to-code`：[`extracted-skills/taste-skill/image-to-code`](../extracted-skills/taste-skill/image-to-code)
- `imagegen-frontend-mobile`：[`extracted-skills/taste-skill/imagegen-frontend-mobile`](../extracted-skills/taste-skill/imagegen-frontend-mobile)
- `imagegen-frontend-web`：[`extracted-skills/taste-skill/imagegen-frontend-web`](../extracted-skills/taste-skill/imagegen-frontend-web)
- `industrial-brutalist-ui`：[`extracted-skills/taste-skill/industrial-brutalist-ui`](../extracted-skills/taste-skill/industrial-brutalist-ui)
- `minimalist-ui`：[`extracted-skills/taste-skill/minimalist-ui`](../extracted-skills/taste-skill/minimalist-ui)
- `redesign-existing-projects`：[`extracted-skills/taste-skill/redesign-existing-projects`](../extracted-skills/taste-skill/redesign-existing-projects)
- `stitch-design-taste`：[`extracted-skills/taste-skill/stitch-design-taste`](../extracted-skills/taste-skill/stitch-design-taste)

### vercel-labsagent-skills

推荐 `npx skills add vercel-labs/agent-skills`；也可从 [`extracted-skills/vercel-labsagent-skills`](../extracted-skills/vercel-labsagent-skills) 手动复制。

- `deploy-to-vercel`：[`extracted-skills/vercel-labsagent-skills/deploy-to-vercel`](../extracted-skills/vercel-labsagent-skills/deploy-to-vercel)
- `vercel-cli-with-tokens`：[`extracted-skills/vercel-labsagent-skills/vercel-cli-with-tokens`](../extracted-skills/vercel-labsagent-skills/vercel-cli-with-tokens)
- `vercel-composition-patterns`：[`extracted-skills/vercel-labsagent-skills/vercel-composition-patterns`](../extracted-skills/vercel-labsagent-skills/vercel-composition-patterns)
- `vercel-optimize`：[`extracted-skills/vercel-labsagent-skills/vercel-optimize`](../extracted-skills/vercel-labsagent-skills/vercel-optimize)
- `vercel-react-best-practices`：[`extracted-skills/vercel-labsagent-skills/vercel-react-best-practices`](../extracted-skills/vercel-labsagent-skills/vercel-react-best-practices)
- `vercel-react-native-skills`：[`extracted-skills/vercel-labsagent-skills/vercel-react-native-skills`](../extracted-skills/vercel-labsagent-skills/vercel-react-native-skills)
- `vercel-react-view-transitions`：[`extracted-skills/vercel-labsagent-skills/vercel-react-view-transitions`](../extracted-skills/vercel-labsagent-skills/vercel-react-view-transitions)
- `web-design-guidelines`：[`extracted-skills/vercel-labsagent-skills/web-design-guidelines`](../extracted-skills/vercel-labsagent-skills/web-design-guidelines)
- `writing-guidelines`：[`extracted-skills/vercel-labsagent-skills/writing-guidelines`](../extracted-skills/vercel-labsagent-skills/writing-guidelines)
