from __future__ import annotations

import json
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

from content_sources import load_reviews, reviews_by_skill, translation_file
from skillhub_common import CATEGORY_LABELS, ROOT, load_registry


SITE_DIR = ROOT / "site"
ASSETS_DIR = SITE_DIR / "assets"
REPO_URL = "https://github.com/Jst-Well-Dan/Skills-Hub"


def source_label(project: dict) -> str:
    source = project.get("source", {})
    return source.get("repo") or source.get("type") or "local"


def build_payload(projects: list[dict]) -> dict:
    category_counts = Counter(project.get("category", "uncategorized") for project in projects)
    skill_count = sum(project.get("skill_count", len(project.get("skills", []))) for project in projects)

    return {
        "generated_at": date.today().isoformat(),
        "summary": {
            "project_count": len(projects),
            "skill_count": skill_count,
        },
        "category_labels": CATEGORY_LABELS,
        "facets": {
            "categories": [
                {"id": category, "label": CATEGORY_LABELS.get(category, category), "count": category_counts[category]}
                for category in CATEGORY_LABELS
                if category_counts[category]
            ],
        },
        "projects": projects,
    }


def build_skill_content(projects: list[dict]) -> dict[str, dict]:
    content = {}
    review_map = reviews_by_skill(projects, load_reviews())
    for project in projects:
        for skill in project.get("skills", []):
            skill_file = ROOT / skill["path"] / "SKILL.md"
            translated = translation_file(project, skill)
            content[skill["path"]] = {
                "original": skill_file.read_text(encoding="utf-8"),
                "translation": translated.read_text(encoding="utf-8") if translated.exists() else None,
                "reviews": review_map.get(skill["path"], []),
            }
    return content


def html_template() -> str:
    return r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="浏览、筛选并直达优质 Agent Skills 的开源目录。">
  <title>Skills-Hub - Agent Skills 目录</title>
  <style>
    @font-face {
      font-family: "TsangerJinKai02";
      src: url("assets/fonts/TsangerJinKai02-W04.ttf") format("truetype");
      font-weight: 400 500;
      font-style: normal;
      font-display: swap;
    }
    @font-face {
      font-family: "JetBrains Mono";
      src: url("assets/fonts/JetBrainsMono.woff2") format("woff2");
      font-weight: 400 500;
      font-style: normal;
      font-display: swap;
    }
    :root {
      color-scheme: light dark;
      --bg: #f6f8fa;
      --bg-deep: #eaeef2;
      --ivory: #ffffff;
      --panel: #ffffff;
      --panel-muted: #f6f8fa;
      --panel-lift: #f3f4f6;
      --text: #1f2328;
      --body-text: #3b434b;
      --muted: #59636e;
      --faint: #6e7781;
      --stone: #59636e;
      --line: #d0d7de;
      --line-strong: #8c959f;
      --accent: #0969da;
      --accent-strong: #0550ae;
      --accent-soft: #ddf4ff;
      --accent-text: #ffffff;
      --shadow: 0 3px 12px rgba(140, 149, 159, .14);
      --ease: cubic-bezier(.16, 1, .3, 1);
      --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", "Microsoft YaHei", sans-serif;
      --mono: "JetBrains Mono", "SF Mono", Consolas, Monaco, monospace;
    }

    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #0d1117;
        --bg-deep: #21262d;
        --ivory: #161b22;
        --panel: #161b22;
        --panel-muted: #0d1117;
        --panel-lift: #21262d;
        --text: #f0f6fc;
        --body-text: #c9d1d9;
        --muted: #9da7b1;
        --faint: #8b949e;
        --stone: #9da7b1;
        --line: #30363d;
        --line-strong: #6e7681;
        --accent: #58a6ff;
        --accent-strong: #79c0ff;
        --accent-soft: #0c2d4a;
        --accent-text: #0d1117;
        --shadow: 0 3px 12px rgba(1, 4, 9, .32);
      }
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-width: 320px;
      background: var(--bg);
      color: var(--body-text);
      font-family: var(--sans);
      font-size: 14px;
      line-height: 1.55;
      letter-spacing: 0;
    }
    a { color: inherit; text-decoration: none; }
    button, input, select { font: inherit; }
    :focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: 3px;
    }

    .topbar {
      position: sticky;
      top: 0;
      z-index: 30;
      border-bottom: 1px solid var(--line);
      background: color-mix(in srgb, var(--ivory) 94%, transparent);
      backdrop-filter: blur(16px);
    }
    .topbar-inner {
      max-width: 1240px;
      margin: 0 auto;
      padding: 12px 24px;
      display: grid;
      grid-template-columns: 220px minmax(280px, 1fr) auto;
      gap: 20px;
      align-items: center;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }
    .mark {
      width: 34px;
      height: 34px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      border: 1px solid var(--accent);
      background: var(--accent);
      color: var(--accent-text);
      font-weight: 800;
      letter-spacing: 0;
      box-shadow: none;
    }
    .brand-title {
      margin: 0;
      color: var(--text);
      font-size: 17px;
      line-height: 1.1;
      font-weight: 720;
    }
    .brand-meta {
      margin-top: 2px;
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .search-box {
      position: relative;
      min-width: 0;
    }
    .search-box input {
      width: 100%;
      height: 42px;
      padding: 0 44px 0 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--text);
      outline: none;
    }
    .search-box input::placeholder { color: var(--muted); }
    .search-box input:focus {
      border-color: var(--line-strong);
      box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 22%, transparent);
    }
    .search-icon, .clear-search {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      color: var(--muted);
    }
    .search-icon { left: 14px; }
    .clear-search {
      right: 8px;
      width: 30px;
      height: 30px;
      border: 0;
      border-radius: 4px;
      background: transparent;
      cursor: pointer;
    }
    .clear-search:hover { background: var(--panel-lift); color: var(--accent); }
    .actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .nav-link {
      min-height: 38px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--panel);
      color: var(--text);
      font-size: 13px;
      font-weight: 600;
      white-space: nowrap;
      transition: border-color .18s var(--ease), background .18s var(--ease);
    }
    .nav-link:hover { border-color: var(--line-strong); background: var(--panel-lift); }
    .icon-button {
      width: 38px;
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      display: grid;
      place-items: center;
      background: var(--panel);
      color: var(--accent);
      cursor: pointer;
      transition: transform .18s var(--ease), border-color .18s var(--ease), background .18s var(--ease);
    }
    .icon-button:hover { border-color: var(--line-strong); background: var(--panel-lift); transform: translateY(-1px); }

    .layout {
      max-width: 1240px;
      margin: 0 auto;
      padding: 42px 24px 56px;
      display: grid;
      grid-template-columns: 208px minmax(0, 1fr);
      gap: 40px;
    }
    .sidebar {
      align-self: start;
      position: sticky;
      top: 88px;
      padding-right: 24px;
      border-right: 1px solid var(--line);
    }
    .filter-panel {
      min-width: 0;
    }
    .filter-head {
      padding: 0 10px 10px;
      display: flex;
      align-items: center;
    }
    .filter-title {
      margin: 0;
      font-size: 14px;
      color: var(--text);
      font-weight: 680;
    }
    .filter-list {
      display: grid;
      gap: 2px;
    }
    .facet {
      width: 100%;
      min-height: 38px;
      padding: 8px 10px;
      border: 0;
      border-radius: 7px;
      background: transparent;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      align-items: center;
      text-align: left;
      cursor: pointer;
      color: var(--text);
      transition: background .16s var(--ease), color .16s var(--ease);
    }
    .facet:hover { background: var(--panel-lift); }
    .facet.active {
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 650;
    }
    .facet span:first-child {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .count {
      min-width: 24px;
      padding: 1px 5px;
      border-radius: 4px;
      background: var(--panel-lift);
      color: var(--muted);
      text-align: center;
      font-size: 12px;
    }
    .facet.active .count { background: var(--accent-soft); color: var(--accent); }

    .workspace {
      min-width: 0;
      display: grid;
      gap: 20px;
    }
    .catalog-intro {
      padding: 0 0 6px;
    }
    .catalog-title {
      margin: 0;
      color: var(--text);
      font-size: 32px;
      line-height: 1.15;
      letter-spacing: -.025em;
      text-wrap: balance;
    }
    .catalog-copy {
      margin: 8px 0 0;
      max-width: 65ch;
      color: var(--muted);
      font-size: 14px;
      text-wrap: pretty;
    }
    .toolbar {
      padding: 0 0 14px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .toolbar-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .segmented {
      display: inline-grid;
      grid-auto-flow: column;
      gap: 3px;
      padding: 3px;
      border-radius: 9px;
      background: var(--bg-deep);
      border: 0;
    }
    .segment {
      min-width: 58px;
      height: 32px;
      padding: 0 12px;
      border: 0;
      border-radius: 7px;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
    }
    .segment.active {
      background: var(--panel);
      color: var(--text);
      box-shadow: 0 1px 3px rgba(31, 35, 40, .12);
      font-weight: 650;
    }
    .sort-select {
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 9px;
      background: var(--panel);
      color: var(--text);
      padding: 0 10px;
    }
    .result-meta {
      color: var(--text);
      font-size: 14px;
      font-weight: 650;
    }
    .project-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }
    .project-list {
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }
    .project-card {
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel);
      min-width: 0;
      overflow: hidden;
      transition: transform .18s var(--ease), border-color .18s var(--ease), box-shadow .18s var(--ease);
    }
    .project-card:hover {
      border-color: var(--line-strong);
      box-shadow: var(--shadow);
    }
    .project-main {
      width: 100%;
      border: 0;
      background: transparent;
      color: inherit;
      padding: 20px 20px 14px;
      text-align: left;
      cursor: pointer;
      display: grid;
      gap: 10px;
    }
    .project-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
      align-items: start;
    }
    .project-name {
      margin: 0;
      color: var(--text);
      font-size: 17px;
      line-height: 1.25;
      overflow-wrap: anywhere;
      text-wrap: balance;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--muted);
      background: var(--panel-muted);
      font-size: 12px;
      white-space: nowrap;
    }
    .description {
      margin: 0;
      color: var(--muted);
      line-height: 1.65;
      font-size: 13px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .project-foot {
      padding: 0 20px 18px;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
      color: var(--muted);
      font-size: 12px;
    }
    .card-category { white-space: nowrap; }
    .github-link, .primary-link {
      min-height: 34px;
      padding: 0;
      border: 0;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
      line-height: 1;
      white-space: nowrap;
      transition: background .18s var(--ease), transform .18s var(--ease);
    }
    .github-link:hover, .primary-link:hover { color: var(--accent-strong); text-decoration: underline; }
    .github-link:active, .primary-link:active { transform: translateY(1px); }
    .empty {
      border: 1px dashed var(--line-strong);
      border-radius: 6px;
      padding: 38px;
      text-align: center;
      color: var(--muted);
      background: var(--panel);
    }

    .drawer {
      position: fixed;
      inset: 0;
      z-index: 40;
      pointer-events: none;
    }
    .drawer.open { pointer-events: auto; }
    .drawer-backdrop {
      position: absolute;
      inset: 0;
      background: rgba(20, 20, 19, .34);
      opacity: 0;
      transition: opacity .18s ease;
    }
    .drawer.open .drawer-backdrop { opacity: 1; }
    .drawer-panel {
      position: absolute;
      top: 0;
      right: 0;
      width: min(760px, 100vw);
      height: 100%;
      background: var(--bg);
      border-left: 1px solid var(--line-strong);
      transform: translateX(100%);
      transition: transform .2s ease;
      display: grid;
      grid-template-rows: auto 1fr;
    }
    .drawer.open .drawer-panel { transform: translateX(0); }
    .drawer-head {
      padding: 18px;
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 12px;
      align-items: start;
    }
    .drawer-head-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .drawer-title {
      margin: 0;
      color: var(--text);
      font-size: 26px;
      line-height: 1.2;
      overflow-wrap: anywhere;
    }
    .drawer-body {
      overflow: auto;
      padding: 18px;
      display: grid;
      gap: 16px;
      align-content: start;
    }
    .detail-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    .detail {
      border-bottom: 1px solid var(--line);
      padding: 10px 0;
      min-width: 0;
    }
    .detail-label {
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 6px;
    }
    .detail-value {
      font-size: 13px;
      overflow-wrap: anywhere;
    }
    .section-title {
      margin: 0;
      font-size: 15px;
    }
    .skill-list {
      display: grid;
      gap: 8px;
    }
    .skill-item {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      display: grid;
      gap: 8px;
      background: var(--panel);
    }
    .skill-name {
      font-weight: 680;
      color: var(--text);
      overflow-wrap: anywhere;
    }
    .skill-description {
      margin: 0;
      color: var(--muted);
      line-height: 1.55;
      font-size: 13px;
    }
    .links {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .text-link {
      border: 0;
      padding: 0;
      background: transparent;
      color: var(--accent);
      font-size: 13px;
      font-weight: 650;
      cursor: pointer;
    }
    .text-link:hover { color: var(--accent-strong); text-decoration: underline; }
    .text-link:disabled { color: var(--muted); cursor: wait; text-decoration: none; }
    .skill-panel {
      margin-top: 4px;
      padding-top: 12px;
      border-top: 1px solid var(--line);
      display: grid;
      gap: 12px;
    }
    .skill-panel[hidden] { display: none; }
    .content-tabs {
      display: inline-flex;
      width: fit-content;
      border-bottom: 1px solid var(--line);
    }
    .content-tab {
      min-width: 68px;
      min-height: 44px;
      padding: 0 14px;
      border: 0;
      border-bottom: 2px solid transparent;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font-weight: 650;
    }
    .content-tab[aria-selected="true"] { border-color: var(--accent); color: var(--accent); }
    .translation-empty { margin: 0; color: var(--muted); font-size: 13px; }
    .skill-content {
      margin: 0;
      max-height: 520px;
      overflow: auto;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--panel-muted);
      color: var(--body-text);
      font: 14px/1.7 var(--sans);
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }
    .skill-content[data-language="original"] { font: 12px/1.65 var(--mono); }
    .related-reviews {
      padding-top: 12px;
      border-top: 1px solid var(--line);
      display: grid;
      gap: 2px;
    }
    .review-title { margin: 0 0 6px; color: var(--text); font-size: 15px; }
    .review-link {
      min-height: 44px;
      padding: 8px 0;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
      border-bottom: 1px solid var(--line);
      color: var(--accent);
      font-weight: 650;
    }
    .review-link:last-child { border-bottom: 0; }
    .review-meta { color: var(--muted); font-size: 12px; font-weight: 400; white-space: nowrap; }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: .001ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: .001ms !important;
      }
    }

    @media (max-width: 980px) {
      .topbar-inner {
        grid-template-columns: 1fr auto;
      }
      .search-box {
        grid-column: 1 / -1;
        order: 3;
      }
      .layout {
        display: flex;
        flex-direction: column;
        gap: 24px;
      }
      .workspace { display: contents; }
      .catalog-intro { order: 1; }
      .sidebar {
        order: 2;
        position: static;
        align-self: stretch;
        min-width: 0;
        padding-right: 0;
        border-right: 0;
      }
      .filter-panel { display: flex; align-items: center; gap: 10px; }
      .filter-head { padding: 0; flex: 0 0 auto; }
      .filter-list {
        display: flex;
        flex: 1;
        min-width: 0;
        gap: 4px;
        overflow-x: auto;
        scrollbar-width: thin;
        padding-bottom: 3px;
      }
      .facet { width: auto; flex: 0 0 auto; }
      .toolbar { order: 3; }
      .project-grid, .project-list { order: 4; grid-template-columns: 1fr; }
    }
    @media (max-width: 680px) {
      .topbar-inner, .layout {
        padding-left: 14px;
        padding-right: 14px;
      }
      .layout { padding-top: 28px; }
      .catalog-title { font-size: 28px; }
      .toolbar { align-items: stretch; }
      .toolbar-actions { width: 100%; justify-content: space-between; }
      .sort-select { width: auto; flex: 1; }
      .detail-grid { grid-template-columns: 1fr; }
      .project-main { padding: 17px 17px 12px; }
      .project-foot { padding: 0 17px 15px; }
      .nav-link { padding: 0 10px; }
      .nav-docs { display: none; }
    }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="#" aria-label="Skills-Hub">
        <div class="mark">SH</div>
        <div>
          <h1 class="brand-title">Skills-Hub</h1>
          <div class="brand-meta">Agent Skills 目录</div>
        </div>
      </a>
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input id="searchInput" type="search" placeholder="搜索项目或 skill" autocomplete="off">
        <button class="clear-search" id="clearSearch" title="清空搜索" aria-label="清空搜索">×</button>
      </div>
      <div class="actions">
        <a class="nav-link nav-docs" href="https://github.com/Jst-Well-Dan/Skills-Hub/blob/main/docs/index.md">完整索引</a>
        <a class="nav-link" href="https://github.com/Jst-Well-Dan/Skills-Hub" target="_blank" rel="noreferrer">项目 GitHub</a>
      </div>
    </div>
  </header>

  <main class="layout">
    <aside class="sidebar" aria-label="分类筛选">
      <section class="filter-panel">
        <div class="filter-head"><h2 class="filter-title">分类</h2></div>
        <div class="filter-list" id="categoryFilters"></div>
      </section>
    </aside>

    <section class="workspace">
      <header class="catalog-intro">
        <h2 class="catalog-title">找到合适的 Agent Skill</h2>
        <p class="catalog-copy">按分类浏览，或搜索项目和能力。点击项目查看包含的 skills，也可以直接前往原始仓库。</p>
      </header>
      <div class="toolbar">
        <div class="result-meta" id="resultMeta"></div>
        <div class="toolbar-actions">
          <div class="segmented" role="tablist" aria-label="展示模式">
            <button class="segment active" data-view="grid">网格</button>
            <button class="segment" data-view="list">列表</button>
          </div>
          <select class="sort-select" id="sortSelect" aria-label="排序">
            <option value="name">按名称</option>
            <option value="skills">按 skill 数</option>
            <option value="updated">按检查日期</option>
          </select>
        </div>
      </div>
      <div class="project-grid" id="projectGrid"></div>
    </section>
  </main>

  <div class="drawer" id="drawer" aria-hidden="true">
    <div class="drawer-backdrop" id="drawerBackdrop"></div>
    <section class="drawer-panel" role="dialog" aria-modal="true" aria-label="项目详情">
      <div class="drawer-head">
        <div>
          <h2 class="drawer-title" id="drawerTitle"></h2>
          <p class="description" id="drawerDescription"></p>
        </div>
        <div class="drawer-head-actions">
          <a class="primary-link" id="drawerSourceLink" href="#" target="_blank" rel="noreferrer">打开 GitHub</a>
          <button class="icon-button" id="closeDrawer" title="关闭" aria-label="关闭">×</button>
        </div>
      </div>
      <div class="drawer-body" id="drawerBody"></div>
    </section>
  </div>

  <script>
    window.SKILL_HUB_DATA = __SKILL_HUB_PAYLOAD__;
    const REPO_URL = "https://github.com/Jst-Well-Dan/Skills-Hub";

    const state = {
      query: "",
      category: "all",
      sort: "name",
      view: "grid",
      selected: null,
    };

    const data = window.SKILL_HUB_DATA;
    let skillContentPromise;
    const el = (id) => document.getElementById(id);
    const text = (value) => String(value ?? "");
    const categoryLabel = (id) => data.category_labels[id] || id || "未分类";
    const sourceOf = (project) => project.source?.repo || project.source?.type || "local";
    const sourceUrl = (project) => project.source?.repo
      ? `https://github.com/${project.source.repo}`
      : `${REPO_URL}/tree/main/${project.path}`;
    const normalize = (value) => text(value).toLowerCase();
    const readableText = (value) => text(value).replaceAll("—", " - ").replaceAll("–", "-");
    const loadSkillContent = () => skillContentPromise ||= fetch("skill-content.json").then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    });

    function escapeHtml(value) {
      return readableText(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function projectHaystack(project) {
      const skills = (project.skills || []).flatMap((skill) => [
        skill.name, skill.id, skill.description, skill.path, ...(skill.tags || [])
      ]);
      return normalize([
        project.name, project.id, project.description, project.path, categoryLabel(project.category),
        ...(project.tags || []), sourceOf(project), ...skills
      ].join(" "));
    }

    function matches(project) {
      if (state.category !== "all" && project.category !== state.category) return false;
      const terms = normalize(state.query).split(/\s+/).filter(Boolean);
      return terms.every((term) => projectHaystack(project).includes(term));
    }

    function sortProjects(projects) {
      const sorted = [...projects];
      sorted.sort((a, b) => {
        if (state.sort === "skills") return (b.skill_count || 0) - (a.skill_count || 0) || a.name.localeCompare(b.name);
        if (state.sort === "updated") return text(b.last_checked_at).localeCompare(text(a.last_checked_at)) || a.name.localeCompare(b.name);
        return a.name.localeCompare(b.name);
      });
      return sorted;
    }

    function renderCategories() {
      const buttons = [{ id: "all", label: "全部分类", count: data.summary.project_count }, ...data.facets.categories]
        .map((item) => `
          <button class="facet ${state.category === item.id ? "active" : ""}" data-category="${escapeHtml(item.id)}" title="${escapeHtml(item.label)}">
            <span>${escapeHtml(item.label)}</span>
            <span class="count">${item.count}</span>
          </button>
        `).join("");
      el("categoryFilters").innerHTML = buttons;
    }

    function projectCard(project) {
      const sourceLabel = project.source?.repo ? "打开 GitHub →" : "查看目录 →";
      return `
        <article class="project-card">
          <button class="project-main" data-project-id="${escapeHtml(project.id)}">
            <div class="project-row">
              <h3 class="project-name">${escapeHtml(project.name)}</h3>
              <span class="badge">${project.skill_count || 0} skills</span>
            </div>
            <p class="description">${escapeHtml(project.description || "暂无简介")}</p>
          </button>
          <div class="project-foot">
            <span class="card-category">${escapeHtml(categoryLabel(project.category))}</span>
            <a class="github-link" href="${escapeHtml(sourceUrl(project))}" target="_blank" rel="noreferrer" aria-label="在 GitHub 打开 ${escapeHtml(project.name)}">${sourceLabel}</a>
          </div>
        </article>
      `;
    }

    function renderProjects(projects) {
      const grid = el("projectGrid");
      grid.className = state.view === "list" ? "project-list" : "project-grid";
      if (!projects.length) {
        grid.innerHTML = '<div class="empty">没有匹配的 skill 库</div>';
        return;
      }
      grid.innerHTML = projects.map(projectCard).join("");
    }

    function renderDrawer(project) {
      if (!project) return;
      state.selected = project.id;
      el("drawerTitle").textContent = project.name;
      el("drawerDescription").textContent = readableText(project.description || "暂无简介");
      el("drawerSourceLink").href = sourceUrl(project);
      el("drawerSourceLink").textContent = project.source?.repo ? "打开 GitHub" : "查看项目目录";
      const install = project.install?.method === "npx" && project.install.command
        ? `<code>${escapeHtml(project.install.command)}</code>`
        : `<a href="${escapeHtml(sourceUrl(project))}" target="_blank" rel="noreferrer">查看源仓库安装说明</a>`;
      const skills = [...(project.skills || [])].sort((a, b) => a.name.localeCompare(b.name));
      const skillHtml = skills.map((skill, index) => `
        <article class="skill-item">
          <div class="skill-name">${escapeHtml(skill.name)}</div>
          <p class="skill-description">${escapeHtml(skill.description || "暂无简介")}</p>
          <div class="links">
            <button class="text-link" data-skill-path="${escapeHtml(skill.path)}" data-panel-id="skill-panel-${index}" aria-expanded="false">查看内容</button>
          </div>
          <section class="skill-panel" id="skill-panel-${index}" aria-live="polite" hidden></section>
        </article>
      `).join("");

      el("drawerBody").innerHTML = `
        <div class="detail-grid">
          <div class="detail"><div class="detail-label">分类</div><div class="detail-value">${escapeHtml(categoryLabel(project.category))}</div></div>
          <div class="detail"><div class="detail-label">安装</div><div class="detail-value">${install}</div></div>
        </div>
        <h3 class="section-title">Skills · ${skills.length}</h3>
        <div class="skill-list">${skillHtml}</div>
      `;
      el("drawer").classList.add("open");
      el("drawer").setAttribute("aria-hidden", "false");
    }

    function setContentLanguage(panel, language) {
      const record = panel.skillRecord;
      const content = panel.querySelector(".skill-content");
      const value = language === "translation" ? record.translation : record.original;
      content.textContent = language === "translation"
        ? text(value).replace(/^<!-- source-sha256: [a-f0-9]+ -->\r?\n/, "")
        : text(value);
      content.dataset.language = language === "translation" ? "translation" : "original";
      panel.querySelectorAll("[data-language]").forEach((tab) => {
        const selected = tab.dataset.language === language;
        tab.setAttribute("aria-selected", String(selected));
        tab.tabIndex = selected ? 0 : -1;
      });
    }

    function renderSkillPanel(panel, record) {
      panel.skillRecord = record;
      const tabs = record.translation ? `
        <div class="content-tabs" role="tablist" aria-label="内容语言">
          <button class="content-tab" role="tab" data-language="translation" aria-selected="true">中文</button>
          <button class="content-tab" role="tab" data-language="original" aria-selected="false" tabindex="-1">原文</button>
        </div>
      ` : '<p class="translation-empty">暂无中文版本，当前显示原文。</p>';
      const reviews = (record.reviews || []).length ? `
        <section class="related-reviews">
          <h4 class="review-title">相关点评</h4>
          ${record.reviews.map((review) => `
            <a class="review-link" href="${REPO_URL}/blob/main/docs/reviews/${encodeURIComponent(review.slug)}.md" target="_blank" rel="noreferrer">
              <span>${escapeHtml(review.title)}</span>
              <span class="review-meta">${escapeHtml(review.type_label)} →</span>
            </a>
          `).join("")}
        </section>
      ` : "";
      panel.innerHTML = `${tabs}<pre class="skill-content"></pre>${reviews}`;
      setContentLanguage(panel, record.translation ? "translation" : "original");
    }

    function closeDrawer() {
      el("drawer").classList.remove("open");
      el("drawer").setAttribute("aria-hidden", "true");
      state.selected = null;
    }

    function render() {
      const projects = sortProjects(data.projects.filter(matches));
      renderCategories();
      renderProjects(projects);
      el("resultMeta").textContent = state.query || state.category !== "all"
        ? `${projects.length} / ${data.summary.project_count} 个项目`
        : `${data.summary.project_count} 个项目 · ${data.summary.skill_count} 个 skills`;
      document.querySelectorAll(".segment").forEach((button) => {
        button.classList.toggle("active", button.dataset.view === state.view);
      });
    }

    document.addEventListener("click", async (event) => {
      const skillButton = event.target.closest("[data-skill-path]");
      if (skillButton) {
        const panel = el(skillButton.dataset.panelId);
        if (!panel.hidden) {
          panel.hidden = true;
          skillButton.textContent = "查看内容";
          skillButton.setAttribute("aria-expanded", "false");
          return;
        }
        skillButton.textContent = "加载中…";
        skillButton.disabled = true;
        try {
          const docs = await loadSkillContent();
          const record = docs[skillButton.dataset.skillPath];
          if (!record) throw new Error("missing content");
          renderSkillPanel(panel, record);
          panel.hidden = false;
          skillButton.textContent = "收起内容";
          skillButton.setAttribute("aria-expanded", "true");
        } catch {
          skillButton.textContent = "加载失败，请重试";
        } finally {
          skillButton.disabled = false;
        }
        return;
      }
      const languageTab = event.target.closest("[data-language]");
      if (languageTab) {
        setContentLanguage(languageTab.closest(".skill-panel"), languageTab.dataset.language);
        return;
      }
      const category = event.target.closest("[data-category]");
      if (category) {
        state.category = category.dataset.category;
        render();
        return;
      }
      const projectButton = event.target.closest("[data-project-id]");
      if (projectButton) {
        renderDrawer(data.projects.find((project) => project.id === projectButton.dataset.projectId));
      }
    });

    el("searchInput").addEventListener("input", (event) => {
      state.query = event.target.value;
      render();
    });
    el("clearSearch").addEventListener("click", () => {
      state.query = "";
      el("searchInput").value = "";
      render();
    });
    el("sortSelect").addEventListener("change", (event) => {
      state.sort = event.target.value;
      render();
    });
    document.querySelectorAll(".segment").forEach((button) => {
      button.addEventListener("click", () => {
        state.view = button.dataset.view;
        render();
      });
    });
    el("closeDrawer").addEventListener("click", closeDrawer);
    el("drawerBackdrop").addEventListener("click", closeDrawer);
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeDrawer();
      const tab = event.target.closest?.("[data-language]");
      if (tab && ["ArrowLeft", "ArrowRight"].includes(event.key)) {
        event.preventDefault();
        const tabs = [...tab.parentElement.querySelectorAll("[data-language]")];
        const next = tabs[(tabs.indexOf(tab) + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length];
        next.focus();
        setContentLanguage(next.closest(".skill-panel"), next.dataset.language);
      }
    });

    render();
  </script>
</body>
</html>
"""


def write_site(payload: dict) -> Path:
    SITE_DIR.mkdir(exist_ok=True)
    font_dir = ASSETS_DIR / "fonts"
    font_dir.mkdir(parents=True, exist_ok=True)
    for font_name in ["TsangerJinKai02-W04.ttf", "JetBrainsMono.woff2"]:
        source = ROOT / "libraries" / "kami" / "assets" / "fonts" / font_name
        if source.exists():
            shutil.copyfile(source, font_dir / font_name)
    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    skill_content = build_skill_content(payload["projects"])
    (SITE_DIR / "skill-content.json").write_text(
        json.dumps(skill_content, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    html = html_template().replace("__SKILL_HUB_PAYLOAD__", serialized)
    output = SITE_DIR / "index.html"
    output.write_text(html, encoding="utf-8")
    return output


def main() -> None:
    projects = load_registry().get("projects", [])
    payload = build_payload(projects)
    output = write_site(payload)
    summary = payload["summary"]
    print(
        f"Generated {output.relative_to(ROOT).as_posix()} for "
        f"{summary['project_count']} projects and {summary['skill_count']} skills."
    )


if __name__ == "__main__":
    main()
