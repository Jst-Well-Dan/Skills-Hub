from __future__ import annotations

import json
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

from skillhub_common import CATEGORY_LABELS, ROOT, load_registry


SITE_DIR = ROOT / "site"
ASSETS_DIR = SITE_DIR / "assets"
REPO_URL = "https://github.com/Jst-Well-Dan/Skills-Hub"


def source_label(project: dict) -> str:
    source = project.get("source", {})
    return source.get("repo") or source.get("type") or "local"


def build_payload(projects: list[dict]) -> dict:
    category_counts = Counter(project.get("category", "uncategorized") for project in projects)
    tag_counts = Counter(tag for project in projects for tag in project.get("tags", []))
    source_counts = Counter(source_label(project) for project in projects)
    skill_count = sum(project.get("skill_count", len(project.get("skills", []))) for project in projects)

    return {
        "generated_at": date.today().isoformat(),
        "summary": {
            "project_count": len(projects),
            "skill_count": skill_count,
            "tag_count": len(tag_counts),
            "source_count": len(source_counts),
        },
        "category_labels": CATEGORY_LABELS,
        "facets": {
            "categories": [
                {"id": category, "label": CATEGORY_LABELS.get(category, category), "count": category_counts[category]}
                for category in CATEGORY_LABELS
                if category_counts[category]
            ],
            "tags": [{"id": tag, "label": tag, "count": count} for tag, count in sorted(tag_counts.items())],
            "sources": [
                {"id": source, "label": source, "count": count}
                for source, count in sorted(source_counts.items(), key=lambda item: item[0].lower())
            ],
        },
        "projects": projects,
    }


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
      --tag-bg: #ddf4ff;
      --accent-text: #ffffff;
      --shadow: 0 8px 24px rgba(140, 149, 159, .18);
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
        --tag-bg: #0c2d4a;
        --accent-text: #0d1117;
        --shadow: 0 8px 24px rgba(1, 4, 9, .38);
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
      max-width: 1360px;
      margin: 0 auto;
      padding: 10px 24px;
      display: grid;
      grid-template-columns: minmax(180px, 260px) 1fr auto;
      gap: 18px;
      align-items: center;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }
    .mark {
      width: 38px;
      height: 38px;
      border-radius: 10px;
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
      font-size: 19px;
      line-height: 1.1;
      font-weight: 720;
    }
    .brand-meta {
      margin-top: 3px;
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
      height: 44px;
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
      max-width: 1360px;
      margin: 0 auto;
      padding: 32px 24px 48px;
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
      gap: 24px;
    }
    .sidebar {
      align-self: start;
      position: sticky;
      top: 76px;
      display: grid;
      gap: 14px;
    }
    .filter-panel {
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel);
      overflow: hidden;
    }
    .filter-head {
      padding: 13px 14px;
      border-bottom: 1px solid var(--line);
      background: var(--panel-muted);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .filter-title {
      margin: 0;
      font-size: 13px;
      color: var(--text);
      letter-spacing: 0;
    }
    .filter-list {
      padding: 8px;
      max-height: 250px;
      overflow: auto;
    }
    .facet {
      width: 100%;
      min-height: 34px;
      padding: 7px 8px;
      border: 0;
      border-radius: 8px;
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
      box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 24%, var(--line));
    }
    .facet span:first-child {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .count {
      min-width: 28px;
      padding: 2px 6px;
      border-radius: 4px;
      background: var(--panel-lift);
      color: var(--muted);
      text-align: center;
      font-size: 12px;
    }
    .facet.active .count { background: var(--tag-bg); color: var(--accent); }

    .workspace {
      min-width: 0;
      display: grid;
      gap: 16px;
    }
    .catalog-intro {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 24px;
      align-items: end;
      padding: 4px 2px 8px;
    }
    .catalog-title {
      margin: 0;
      color: var(--text);
      font-size: clamp(28px, 4vw, 44px);
      line-height: 1.08;
      letter-spacing: -.035em;
    }
    .catalog-copy {
      margin: 10px 0 0;
      max-width: 58ch;
      color: var(--muted);
      font-size: 15px;
    }
    .catalog-source {
      color: var(--accent);
      font-weight: 650;
      white-space: nowrap;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 0;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel);
      overflow: hidden;
    }
    .stat {
      border-right: 1px solid var(--line);
      padding: 14px 16px;
      min-height: 78px;
      display: grid;
      align-content: space-between;
    }
    .stat:last-child { border-right: 0; }
    .stat-label {
      color: var(--muted);
      font-size: 12px;
      letter-spacing: .04em;
    }
    .stat-value {
      margin-top: 8px;
      color: var(--text);
      font-size: 27px;
      line-height: 1;
      font-weight: 760;
    }
    .toolbar {
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel);
      padding: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .segmented {
      display: inline-grid;
      grid-auto-flow: column;
      gap: 3px;
      padding: 3px;
      border-radius: 9px;
      background: var(--bg-deep);
      border: 1px solid var(--line);
    }
    .segment {
      min-width: 72px;
      height: 32px;
      padding: 0 12px;
      border: 0;
      border-radius: 7px;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
    }
    .segment.active {
      background: var(--accent);
      color: var(--accent-text);
      box-shadow: 0 0 0 1px var(--accent);
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
      color: var(--muted);
      font-size: 13px;
    }
    .project-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }
    .project-list {
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }
    .project-card {
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel);
      min-width: 0;
      overflow: hidden;
      transition: transform .18s var(--ease), border-color .18s var(--ease), box-shadow .18s var(--ease);
    }
    .project-card:hover {
      border-color: var(--line-strong);
      box-shadow: var(--shadow);
      transform: translateY(-2px);
    }
    .project-main {
      width: 100%;
      border: 0;
      background: transparent;
      color: inherit;
      padding: 18px;
      text-align: left;
      cursor: pointer;
      display: grid;
      gap: 12px;
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
      color: var(--accent);
      background: var(--tag-bg);
      font-size: 12px;
      white-space: nowrap;
    }
    .description {
      margin: 0;
      color: var(--muted);
      line-height: 1.65;
      font-size: 13px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .tag {
      min-height: 23px;
      padding: 3px 7px;
      border: 1px solid color-mix(in srgb, var(--accent) 24%, var(--line));
      border-radius: 6px;
      background: var(--tag-bg);
      color: var(--accent);
      font-size: 12px;
    }
    .project-foot {
      padding: 10px 12px 10px 18px;
      border-top: 1px solid var(--line);
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto auto;
      gap: 12px;
      align-items: center;
      color: var(--muted);
      font-size: 12px;
    }
    .path {
      color: var(--stone);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
    }
    .card-category { white-space: nowrap; }
    .github-link, .primary-link {
      min-height: 34px;
      padding: 0 11px;
      border: 1px solid var(--accent);
      border-radius: 8px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--accent);
      color: var(--accent-text);
      font-size: 12px;
      font-weight: 700;
      line-height: 1;
      white-space: nowrap;
      transition: background .18s var(--ease), transform .18s var(--ease);
    }
    .github-link:hover, .primary-link:hover { background: var(--accent-strong); }
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
    .drawer-panel::before {
      content: "";
      position: absolute;
      inset: 0 auto 0 0;
      width: 1px;
      background: linear-gradient(var(--accent), var(--line), transparent);
      pointer-events: none;
    }
    .drawer-head {
      padding: 18px;
      border-bottom: 1px solid var(--line);
      background:
        linear-gradient(135deg, var(--accent-soft), transparent 48%),
        var(--panel);
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
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 11px;
      background: var(--panel);
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
    .skill-top {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
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
      color: var(--accent);
      font-size: 13px;
      font-weight: 650;
    }
    .text-link:hover { color: var(--accent-strong); }

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
      }
      .workspace { display: contents; }
      .catalog-intro { order: 1; }
      .sidebar {
        order: 2;
        position: static;
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
      .stats { order: 3; grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .toolbar { order: 4; }
      .project-grid, .project-list { order: 5; grid-template-columns: 1fr; }
      .catalog-intro { grid-template-columns: 1fr; gap: 8px; }
    }
    @media (max-width: 680px) {
      .topbar-inner, .layout {
        padding-left: 14px;
        padding-right: 14px;
      }
      .sidebar { grid-template-columns: 1fr; }
      .filter-list { max-height: 118px; }
      .stats { grid-template-columns: 1fr 1fr; }
      .stat:nth-child(2) { border-right: 0; }
      .stat:nth-child(-n+2) { border-bottom: 1px solid var(--line); }
      .stat-value { font-size: 23px; }
      .toolbar { align-items: stretch; }
      .segmented { width: 100%; grid-template-columns: 1fr 1fr; grid-auto-flow: row; }
      .sort-select { width: 100%; }
      .detail-grid { grid-template-columns: 1fr; }
      .project-foot { grid-template-columns: minmax(0, 1fr) auto; }
      .card-category { display: none; }
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
          <div class="brand-meta" id="generatedAt"></div>
        </div>
      </a>
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input id="searchInput" type="search" placeholder="搜索 skill、项目、标签、描述" autocomplete="off">
        <button class="clear-search" id="clearSearch" title="清空搜索" aria-label="清空搜索">×</button>
      </div>
      <div class="actions">
        <a class="nav-link nav-docs" href="https://github.com/Jst-Well-Dan/Skills-Hub/blob/main/docs/index.md">完整索引</a>
        <a class="nav-link" href="https://github.com/Jst-Well-Dan/Skills-Hub" target="_blank" rel="noreferrer">项目 GitHub</a>
      </div>
    </div>
  </header>

  <main class="layout">
    <aside class="sidebar" aria-label="筛选">
      <section class="filter-panel">
        <div class="filter-head"><h2 class="filter-title">分类</h2></div>
        <div class="filter-list" id="categoryFilters"></div>
      </section>
      <section class="filter-panel">
        <div class="filter-head"><h2 class="filter-title">标签</h2></div>
        <div class="filter-list" id="tagFilters"></div>
      </section>
      <section class="filter-panel">
        <div class="filter-head"><h2 class="filter-title">来源</h2></div>
        <div class="filter-list" id="sourceFilters"></div>
      </section>
    </aside>

    <section class="workspace">
      <header class="catalog-intro">
        <div>
          <h2 class="catalog-title">找到值得使用的 Agent Skills</h2>
          <p class="catalog-copy">从开源项目中筛选、比较并直达原始仓库。点击卡片查看详情，或直接打开目标 GitHub。</p>
        </div>
        <a class="catalog-source" href="https://github.com/Jst-Well-Dan/Skills-Hub" target="_blank" rel="noreferrer">在 GitHub 查看本目录</a>
      </header>
      <div class="stats" id="stats"></div>
      <div class="toolbar">
        <div class="segmented" role="tablist" aria-label="展示模式">
          <button class="segment active" data-view="grid">网格</button>
          <button class="segment" data-view="list">列表</button>
        </div>
        <div class="result-meta" id="resultMeta"></div>
        <select class="sort-select" id="sortSelect" aria-label="排序">
          <option value="name">按名称</option>
          <option value="skills">按 skill 数</option>
          <option value="updated">按检查日期</option>
          <option value="category">按分类</option>
        </select>
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
      tag: "all",
      source: "all",
      sort: "name",
      view: "grid",
      selected: null,
    };

    const data = window.SKILL_HUB_DATA;
    const el = (id) => document.getElementById(id);
    const text = (value) => String(value ?? "");
    const categoryLabel = (id) => data.category_labels[id] || id || "未分类";
    const sourceOf = (project) => project.source?.repo || project.source?.type || "local";
    const sourceUrl = (project) => project.source?.repo
      ? `https://github.com/${project.source.repo}`
      : `${REPO_URL}/tree/main/${project.path}`;
    const normalize = (value) => text(value).toLowerCase();
    const readableText = (value) => text(value).replaceAll("—", " - ").replaceAll("–", "-");

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
      if (state.tag !== "all" && !(project.tags || []).includes(state.tag)) return false;
      if (state.source !== "all" && sourceOf(project) !== state.source) return false;
      const terms = normalize(state.query).split(/\s+/).filter(Boolean);
      return terms.every((term) => projectHaystack(project).includes(term));
    }

    function sortProjects(projects) {
      const sorted = [...projects];
      sorted.sort((a, b) => {
        if (state.sort === "skills") return (b.skill_count || 0) - (a.skill_count || 0) || a.name.localeCompare(b.name);
        if (state.sort === "updated") return text(b.last_checked_at).localeCompare(text(a.last_checked_at)) || a.name.localeCompare(b.name);
        if (state.sort === "category") return categoryLabel(a.category).localeCompare(categoryLabel(b.category)) || a.name.localeCompare(b.name);
        return a.name.localeCompare(b.name);
      });
      return sorted;
    }

    function renderStats(projects) {
      const skillCount = projects.reduce((sum, project) => sum + (project.skill_count || 0), 0);
      const categories = new Set(projects.map((project) => project.category || "uncategorized")).size;
      const tags = new Set(projects.flatMap((project) => project.tags || [])).size;
      const stats = [
        ["项目", projects.length],
        ["Skills", skillCount],
        ["分类", categories],
        ["标签", tags],
      ];
      el("stats").innerHTML = stats.map(([label, value]) => `
        <div class="stat">
          <div class="stat-label">${label}</div>
          <div class="stat-value">${value}</div>
        </div>
      `).join("");
    }

    function renderFacet(containerId, items, key) {
      const active = state[key];
      const allLabel = key === "category" ? "全部分类" : key === "tag" ? "全部标签" : "全部来源";
      const buttons = [{ id: "all", label: allLabel, count: data.summary.project_count }, ...items]
        .map((item) => `
          <button class="facet ${active === item.id ? "active" : ""}" data-filter-key="${key}" data-filter-value="${escapeHtml(item.id)}" title="${escapeHtml(item.label)}">
            <span>${escapeHtml(item.label)}</span>
            <span class="count">${item.count}</span>
          </button>
        `).join("");
      el(containerId).innerHTML = buttons;
    }

    function renderFilters() {
      renderFacet("categoryFilters", data.facets.categories, "category");
      renderFacet("tagFilters", data.facets.tags, "tag");
      renderFacet("sourceFilters", data.facets.sources, "source");
    }

    function projectCard(project) {
      const tags = (project.tags || []).slice(0, 7).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("");
      const sourceLabel = project.source?.repo ? "GitHub" : "查看目录";
      return `
        <article class="project-card">
          <button class="project-main" data-project-id="${escapeHtml(project.id)}">
            <div class="project-row">
              <h3 class="project-name">${escapeHtml(project.name)}</h3>
              <span class="badge">${project.skill_count || 0} skills</span>
            </div>
            <p class="description">${escapeHtml(project.description || "暂无简介")}</p>
            <div class="tags">${tags}</div>
          </button>
          <div class="project-foot">
            <span class="path">${escapeHtml(project.path)}</span>
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
      const install = project.install?.command || project.install?.method || "未记录";
      const skills = [...(project.skills || [])].sort((a, b) => a.name.localeCompare(b.name));
      const skillHtml = skills.map((skill) => `
        <article class="skill-item">
          <div class="skill-top">
            <div class="skill-name">${escapeHtml(skill.name)}</div>
            <span class="badge">${escapeHtml(skill.id)}</span>
          </div>
          <p class="skill-description">${escapeHtml(skill.description || "暂无简介")}</p>
          <div class="links">
            <a class="text-link" href="${REPO_URL}/blob/main/${escapeHtml(skill.path)}/SKILL.md">查看 SKILL.md</a>
            ${skill.extracted_path ? `<a class="text-link" href="${REPO_URL}/tree/main/${escapeHtml(skill.extracted_path)}">复制目录</a>` : ""}
          </div>
        </article>
      `).join("");

      el("drawerBody").innerHTML = `
        <div class="detail-grid">
          <div class="detail"><div class="detail-label">分类</div><div class="detail-value">${escapeHtml(categoryLabel(project.category))}</div></div>
          <div class="detail"><div class="detail-label">来源</div><div class="detail-value">${escapeHtml(sourceOf(project))}</div></div>
          <div class="detail"><div class="detail-label">安装</div><div class="detail-value">${escapeHtml(install)}</div></div>
          <div class="detail"><div class="detail-label">路径</div><div class="detail-value">${escapeHtml(project.path)}</div></div>
        </div>
        <div class="tags">${(project.tags || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}</div>
        <h3 class="section-title">Skills</h3>
        <div class="skill-list">${skillHtml}</div>
      `;
      el("drawer").classList.add("open");
      el("drawer").setAttribute("aria-hidden", "false");
    }

    function closeDrawer() {
      el("drawer").classList.remove("open");
      el("drawer").setAttribute("aria-hidden", "true");
      state.selected = null;
    }

    function render() {
      const projects = sortProjects(data.projects.filter(matches));
      renderStats(projects);
      renderFilters();
      renderProjects(projects);
      el("resultMeta").textContent = `显示 ${projects.length} / ${data.summary.project_count} 个项目`;
      el("generatedAt").textContent = `${data.summary.project_count} 个库 / ${data.summary.skill_count} 个 skills / ${data.generated_at}`;
      document.querySelectorAll(".segment").forEach((button) => {
        button.classList.toggle("active", button.dataset.view === state.view);
      });
    }

    document.addEventListener("click", (event) => {
      const filter = event.target.closest("[data-filter-key]");
      if (filter) {
        state[filter.dataset.filterKey] = filter.dataset.filterValue;
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
