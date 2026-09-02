# Product

## Users

Developers, prompt engineers, and AI-agent users (Claude, Codex, Cursor, Antigravity, Pi, etc.) who want to discover, evaluate, read, and deploy curated Agent Skills into local environments with minimal friction.

## Product Purpose

Skills-Hub is a curated catalog, immersive reader, and local distribution workbench for AI Agent Skills.

It solves three critical problems:
1. **Discovery & Evaluation**: Cuts through fragmented GitHub repositories to provide structured, categorized, and searchable skill collections with real-world review guides.
2. **Immersive Reading**: Offers a zero-friction slide-over drawer to inspect full skill prompts, frontmatter schemas, trigger keywords, and installation commands without opening external tabs.
3. **Local Management & Deployment**: Provides a local visual admin workbench to curate categories and batch-deploy selected skills directly into target project agent directories (`.claude/skills/`, `.agents/skills/`, `.codex/skills/`).

## Core Capabilities

- **Curated Multi-Dimensional Exploration**: Filter by functional categories (Coding, Daily Tools, Frontend, Content Creation, Documents & Data, Curated Collections) and keyword tags, with real-time full-text search.
- **Drawer-Based Skill Reader**: Inspect complete `SKILL.md` content, YAML frontmatter configurations, description summaries, and source repository links.
- **One-Click Prompt & Install Actions**: Quick copy for `npx skills` commands or raw prompt texts, and direct deep-links to upstream repositories.
- **Local Admin Workbench (`?admin=1`)**:
  - Visual category lifecycle management (create, rename, reorder, delete).
  - Multi-select projects or individual skills to batch reassign categories.
  - One-click batch deployment directly copying skill packages to any local project path.
  - In-browser trigger for rebuilding static pages and markdown docs.
- **In-Depth Reviews & Guides**: Dedicated evaluation articles covering skill combinations (e.g. Taste + Impeccable), architectural anti-patterns, and testing benchmarks.

## Brand Personality & Design Principles

- **Material Design & Modern Flat Aesthetic**: Restrained, clear, and trustworthy developer-tool aesthetic. Subtle elevations, crisp typography, and high contrast.
- **Zero-Build & Zero-Bloat**: Implemented with pure vanilla HTML5, CSS3, and modern JavaScript. No compilation overhead, instant millisecond load time, and full offline/static host portability.
- **Progressive Disclosure**: High-level scannability on project cards; deep metadata, raw prompt code, and schema definitions presented within the contextual drawer.
- **Dark/Light Mode & Accessibility**: Automatic adaptation to system color schemes, WCAG AA compliant contrast ratios, full keyboard navigation, and responsive mobile-to-desktop layouts.

