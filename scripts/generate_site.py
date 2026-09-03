from __future__ import annotations

import json
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

from content_sources import load_reviews, reviews_by_skill, translation_file
from skillhub_common import ROOT, load_category_labels, load_registry, parse_frontmatter

CATEGORY_LABELS = load_category_labels()

SITE_DIR = ROOT / "site"
ASSETS_DIR = SITE_DIR / "assets"
REPO_URL = "https://github.com/Jst-Well-Dan/Skills-Hub"
CATEGORY_LABELS_EN = {
    "coding-tools": "Coding tools",
    "daily-tools": "Daily tools",
    "personal-collection": "Personal collections",
    "frontend-presentation": "Frontend & presentation",
    "animation-motion": "Animation & motion",
    "content-creation": "Content creation",
    "document-data": "Documents & data",
    "research-learning": "Research & learning",
    "automation-workflow": "Automation & workflow",
    "uncategorized": "Uncategorized",
    "video-image": "IMG",
}
for _cid, _label in CATEGORY_LABELS.items():
    CATEGORY_LABELS_EN.setdefault(_cid, _label)


def source_label(project: dict) -> str:
    source = project.get("source", {})
    return source.get("repo") or source.get("type") or "local"


def build_payload(projects: list[dict]) -> dict:
    for project in projects:
        for skill in project.get("skills", []):
            translated = translation_file(project, skill)
            skill["description_zh"] = (
                parse_frontmatter(translated).get("description", skill.get("description", ""))
                if translated.exists()
                else skill.get("description", "")
            )
        description = project.get("description", "")
        if any("\u4e00" <= char <= "\u9fff" for char in description):
            project["description_zh"] = description
        elif len(project.get("skills", [])) == 1:
            project["description_zh"] = project["skills"][0].get("description_zh", description)
        else:
            project["description_zh"] = f"{project['name']} 收录了 {len(project.get('skills', []))} 个 Agent Skills。"
    category_counts = Counter(project.get("category", "uncategorized") for project in projects)
    skill_count = sum(project.get("skill_count", len(project.get("skills", []))) for project in projects)

    return {
        "generated_at": date.today().isoformat(),
        "summary": {
            "project_count": len(projects),
            "skill_count": skill_count,
        },
        "category_labels": CATEGORY_LABELS,
        "category_labels_en": CATEGORY_LABELS_EN,
        "facets": {
            "categories": [
                {"id": category, "label": CATEGORY_LABELS.get(category, category), "count": category_counts[category]}
                for category in CATEGORY_LABELS
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
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,ital,wght@9..144,0,700;9..144,1,700&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root{--ink:#0F1A14;--paper:#F4EFE6;--line:#E8E0D1;--grid:#EDE7DA;--orange:#D86C3A;--moss:#3A7D6B;--muted:#6B7A74;--cream:#FFFFFF;--sans:Inter,sans-serif;--mono:IBM Plex Mono,monospace;--display:Fraunces,serif;--ease:cubic-bezier(.16,1,.3,1)}
    *{box-sizing:border-box}body{margin:0;min-width:320px;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.55;padding-bottom:0}
    body.admin-b2{padding-bottom:86px}
    a{color:inherit;text-decoration:none}button,input,select{font:inherit}:focus-visible{outline:2px solid var(--orange);outline-offset:3px}
    .topbar{position:sticky;top:0;z-index:30;border-bottom:1px solid var(--line);background:color-mix(in srgb, var(--paper) 96%, white);backdrop-filter:blur(10px)}
    .topbar-inner{max-width:1240px;margin:0 auto;padding:12px 24px;display:grid;grid-template-columns:220px minmax(280px,1fr) auto;gap:16px;align-items:center}
    .brand{display:flex;align-items:center;gap:12px;min-width:0}
    .mark{width:32px;height:32px;border:1.4px solid var(--ink);background:var(--cream);color:var(--ink);display:grid;place-items:center;font-family:var(--mono);font-weight:700;font-size:13px}
    .brand-title{margin:0;color:var(--ink);font-size:16px;font-weight:700;letter-spacing:-.02em}
    .brand-meta{margin-top:1px;color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.08em}
    .search-box{position:relative;min-width:0}
    .search-box input{width:100%;height:40px;padding:0 40px 0 38px;border:1px solid var(--line);background:var(--cream);color:var(--ink);outline:none}
    .search-box input::placeholder{color:var(--muted)}
    .search-box input:focus{border-color:var(--ink);box-shadow:0 0 0 3px rgba(216,108,58,.12)}
    .search-icon,.clear-search{position:absolute;top:50%;transform:translateY(-50%);color:var(--muted)}
    .search-icon{left:12px}.clear-search{right:6px;width:28px;height:28px;border:0;background:transparent;cursor:pointer}
    .clear-search:hover{color:var(--orange)}
    .actions{display:flex;align-items:center;gap:8px}
    .nav-link{min-height:36px;padding:0 12px;border:1px solid var(--line);background:var(--cream);color:var(--ink);font-family:var(--mono);font-size:12px;letter-spacing:.04em;white-space:nowrap;display:inline-flex;align-items:center;justify-content:center}
    .nav-link:hover{border-color:var(--ink)}
    .icon-button{width:36px;height:36px;border:1px solid var(--line);background:var(--cream);display:grid;place-items:center;cursor:pointer;color:var(--ink)}
    /* admin bar B2 dual-mode */
    .admin-bar{display:none;position:sticky;top:56px;z-index:29;background:var(--ink);color:var(--paper);border-bottom:1px solid var(--ink);padding:0;justify-content:center}
    .admin-bar.open{display:flex}
    .admin-bar-inner{max-width:1240px;width:100%;margin:0 auto;padding:10px 24px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;justify-content:space-between}
    .admin-bar-left{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
    .admin-bar strong{color:var(--paper);font-family:var(--mono);font-size:11px;letter-spacing:.08em;font-weight:600}
    .admin-hint{color:rgba(244,239,230,.72);font-family:var(--mono);font-size:11px;line-height:1.4}
    .segmented{display:inline-grid;grid-auto-flow:column;gap:3px;padding:3px;background:rgba(244,239,230,.14);border-radius:9px}
    .segment{min-width:84px;height:30px;padding:0 14px;border:0;border-radius:7px;background:transparent;color:rgba(244,239,230,.72);cursor:pointer;font-family:var(--mono);font-size:11px;transition:all .18s var(--ease)}
    .segment.active{background:var(--cream);color:var(--ink);font-weight:700;box-shadow:0 1px 3px rgba(0,0,0,.18)}
    .segment:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
    .admin-chip{min-height:36px;padding:0 12px;border:1px solid var(--line);background:var(--cream);color:var(--ink);font-family:var(--mono);font-size:12px;cursor:pointer;transition:border-color .15s var(--ease), background .15s var(--ease), color .15s var(--ease)}
    .admin-bar .admin-chip{background:transparent;border-color:rgba(244,239,230,.22);color:var(--paper)}
    .admin-bar .admin-chip option{color:var(--ink);background:var(--cream)}
    .admin-bar .admin-chip:hover{border-color:var(--paper);background:rgba(244,239,230,.08)}
    .admin-bar .admin-chip:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
    .admin-chip:hover{border-color:var(--ink);background:var(--paper)}
    .admin-chip:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
    .admin-chip:active{background:var(--grid)}
    .admin-chip:disabled{opacity:.45;cursor:not-allowed}
    .admin-chip.primary{background:var(--orange);color:white;border-color:var(--orange)}
    .admin-chip.primary:hover{background:#C45A2A;border-color:#C45A2A}
    .admin-bar .admin-chip.primary{background:var(--orange);border-color:var(--orange);color:white}
    .admin-bar .admin-chip.primary:hover{background:#C45A2A;border-color:#C45A2A}
    .layout{max-width:1240px;margin:0 auto;padding:28px 24px 48px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:28px}
    .sidebar{align-self:start;position:sticky;top:72px}
    body.admin-b2 .sidebar{top:110px}
    .filter-panel{border:1px solid var(--line);background:var(--cream)}
    .filter-head{padding:11px 14px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}
    .filter-title{margin:0;font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--ink)}
    .filter-list{display:grid}
    .facet{width:100%;min-height:38px;padding:9px 12px;border:0;border-bottom:1px solid var(--grid);background:var(--cream);display:flex;justify-content:space-between;gap:8px;align-items:center;text-align:left;cursor:pointer;color:var(--ink);font-size:13px}
    .facet:hover{background:var(--paper)}
    .facet.active{background:var(--ink);color:white}
    .facet.active .count{background:rgba(255,255,255,.15);color:white;border-color:rgba(255,255,255,.2)}
    .count{min-width:22px;padding:2px 6px;border-radius:999px;border:1px solid var(--line);background:var(--paper);color:var(--muted);font-family:var(--mono);font-size:11px;text-align:center}
    .facet.drag-over{background:rgba(216,108,58,.08);outline:2px dashed var(--orange);outline-offset:-2px}
    .facet-row{display:contents}
    .mode-organize .facet-row{display:flex;align-items:center;gap:0;border-bottom:1px solid var(--grid)}
    .mode-organize .facet-row .facet{flex:1;border-bottom:0}
    .facet-actions{display:none;gap:6px;align-items:center;padding:4px 6px 4px 0}
    .mode-organize .facet-actions{display:inline-flex}
    .facet-actions button{min-height:28px;padding:0 8px;border:1px solid var(--ink);background:var(--paper);color:var(--ink);font-family:var(--mono);font-size:11px;font-weight:600;cursor:pointer;white-space:nowrap}
    .facet-actions button:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}
    .facet-actions button[data-act="delete"]{border-color:var(--orange);color:var(--orange)}
    .facet-actions button[data-act="delete"]:hover{background:var(--orange);color:white;border-color:var(--orange)}
    .facet-actions button:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
    .workspace{min-width:0;display:grid;gap:16px}
    .catalog-intro{position:relative;overflow:hidden;background:var(--paper);border:1px solid var(--line);padding:20px 18px 16px}
    .catalog-intro::before{content:"";position:absolute;width:220px;height:220px;left:-40px;bottom:-60px;border:1px solid rgba(58,125,107,.18);border-radius:50%;pointer-events:none}
    .catalog-intro::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg, transparent 30%, var(--paper) 92%);pointer-events:none}
    .catalog-intro>*{position:relative;z-index:1}
    .catalog-title{margin:0;font-family:var(--display);font-size:30px;line-height:1.1;letter-spacing:-.03em;color:var(--ink)}
    .catalog-title i{font-style:italic;color:var(--orange)}
    .catalog-copy{margin:8px 0 0;max-width:65ch;color:var(--muted);font-size:13px;line-height:1.6}
    .toolbar{padding:10px 0 12px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
    .toolbar-actions{display:flex;align-items:center;gap:8px}
    .sort-select{height:36px;border:1px solid var(--line);background:var(--cream);color:var(--ink);padding:0 10px;font-family:var(--mono);font-size:12px}
    .result-meta{color:var(--ink);font-family:var(--mono);font-size:12px;letter-spacing:.06em}
    .project-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
    .project-list{display:grid;grid-template-columns:1fr;gap:10px}
    .project-card{position:relative;border:1px solid var(--line);background:var(--cream);overflow:hidden;transition:transform .16s var(--ease), box-shadow .16s var(--ease)}
    .project-card:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(15,26,20,.08)}
    .project-card.selected{outline:2px solid var(--ink);outline-offset:-2px}
    .project-card.dragging{opacity:.55;transform:rotate(.6deg);box-shadow:0 12px 24px rgba(15,26,20,.18)}
    .project-card.has-check .project-main{padding-left:44px}
    .admin-check-wrap{position:absolute;top:0;left:0;width:44px;height:44px;display:grid;place-items:center;z-index:5;cursor:pointer}
    .admin-checkbox{width:18px;height:18px;accent-color:var(--ink);cursor:pointer;margin:0}
    .stamp{position:absolute;top:10px;right:10px;transform:rotate(7deg);border:1.6px solid var(--orange);color:var(--orange);font-family:var(--mono);font-size:10px;letter-spacing:.12em;padding:3px 6px;opacity:.9;pointer-events:none}
    .project-main{width:100%;border:0;background:transparent;color:inherit;padding:16px 16px 12px;text-align:left;cursor:pointer;display:grid;gap:8px}
    .eyebrow{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--moss);display:flex;gap:6px;align-items:center}
    .eyebrow::before{content:"\25C9";color:var(--orange);font-size:9px}
    .project-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:start}
    .project-name{margin:0;color:var(--ink);font-size:16px;line-height:1.25;font-weight:700;overflow-wrap:anywhere}
    .badge{display:inline-flex;align-items:center;min-height:22px;padding:3px 7px;border:1px solid var(--line);background:var(--paper);color:var(--muted);font-family:var(--mono);font-size:11px;white-space:nowrap}
    .description{margin:0;color:var(--muted);line-height:1.6;font-size:13px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:42px}
    .project-foot{padding:0 16px 14px;display:flex;justify-content:space-between;gap:12px;align-items:center;border-top:1px dashed var(--line);margin:0 16px;padding-top:10px;font-family:var(--mono);font-size:11px;color:var(--muted)}
    .card-tags{display:flex;gap:6px;flex-wrap:wrap}
    .card-tags span{padding:3px 6px;border:1px solid var(--line);background:var(--paper);font-size:11px}
    .gh-icon{width:32px;height:32px;border:1px solid var(--line);background:var(--cream);display:grid;place-items:center;color:var(--ink);flex:0 0 auto;transition:border-color .15s var(--ease), background .15s var(--ease), color .15s var(--ease)}
    .gh-icon:hover{border-color:var(--ink);background:var(--paper);color:var(--orange)}
    .gh-icon.small{width:28px;height:28px}
    .gh-icon svg{width:18px;height:18px;fill:currentColor;display:block}
    .gh-icon.small svg{width:14px;height:14px}
    .gh-icon--topbar{width:36px;height:36px}
    .gh-icon--topbar svg{width:18px;height:18px}
    .empty{border:1px dashed var(--line);background:var(--cream);padding:32px;text-align:center;color:var(--muted)}
    .drawer{position:fixed;inset:0;z-index:40;pointer-events:none}
    .drawer.open{pointer-events:auto}
    .drawer-backdrop{position:absolute;inset:0;background:rgba(15,26,20,.24);opacity:0;transition:opacity .18s}
    .drawer.open .drawer-backdrop{opacity:1}
    .drawer-panel{position:absolute;top:0;right:0;width:min(760px,100vw);height:100%;background:var(--paper);border-left:1px solid var(--ink);transform:translateX(100%);transition:transform .2s var(--ease);display:grid;grid-template-rows:auto 1fr}
    .drawer.open .drawer-panel{transform:translateX(0)}
    .drawer-head{padding:18px;border-bottom:1px solid var(--line);background:var(--cream);display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px}
    .drawer-head-actions{display:flex;gap:8px;align-items:center}
    .drawer-title{margin:0;color:var(--ink);font-family:var(--display);font-size:26px;line-height:1.2}
    .drawer-body{overflow:auto;padding:18px;display:grid;gap:16px;align-content:start}
    .detail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
    .detail{border-bottom:1px solid var(--line);padding:10px 0}
    .detail-label{color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.08em;margin-bottom:4px}
    .detail-value{font-size:13px;overflow-wrap:anywhere}
    .section-title{margin:0;font-family:var(--display);font-size:18px}
    .skill-list{display:grid;gap:8px}
    .skill-item{border:1px solid var(--line);background:var(--cream);padding:12px;display:grid;gap:6px}
    .skill-name{font-weight:700;color:var(--ink)}
    .skill-description{margin:0;color:var(--muted);font-size:13px;line-height:1.6}
    .links{display:flex;gap:8px;flex-wrap:wrap}
    .text-link{border:0;background:transparent;color:var(--orange);font-family:var(--mono);font-size:12px;font-weight:600;cursor:pointer}
    .skill-panel{margin-top:6px;padding-top:10px;border-top:1px solid var(--line);display:grid;gap:10px}
    .skill-panel[hidden]{display:none}
    .skill-content{margin:0;max-height:520px;overflow:auto;padding:12px;border:1px solid var(--line);background:var(--paper);font:12px/1.65 var(--mono);white-space:pre-wrap;overflow-wrap:anywhere}
    .related-reviews{padding-top:10px;border-top:1px solid var(--line);display:grid;gap:2px}
    .review-title{margin:0 0 6px;color:var(--ink);font-family:var(--display);font-size:16px}
    .review-link{min-height:40px;padding:8px 0;display:flex;justify-content:space-between;gap:12px;align-items:center;border-bottom:1px solid var(--line);color:var(--ink);font-weight:600}
    .review-meta{color:var(--muted);font-family:var(--mono);font-size:11px;white-space:nowrap}
    #languageToggle,#drawerLanguageToggle{display:none !important}
    /* bottom dock B2 - floating card */
    .bottom-dock{position:fixed;left:50%;bottom:20px;z-index:45;background:var(--cream);border:1px solid var(--ink);border-radius:16px;box-shadow:0 20px 40px rgba(15,26,20,.18), 0 4px 12px rgba(15,26,20,.10);transform:translateX(-50%) translateY(calc(100% + 28px)) scale(.97);opacity:0;transition:transform .36s var(--ease), opacity .28s var(--ease);display:flex;align-items:center;gap:10px;padding:14px 16px;flex-wrap:wrap;width:min(760px, calc(100vw - 32px));max-width:92vw;pointer-events:none}
    .bottom-dock.open{transform:translateX(-50%) translateY(0) scale(1);opacity:1;pointer-events:auto}
    .bottom-dock::before{content:"";position:absolute;top:6px;left:50%;transform:translateX(-50%);width:36px;height:4px;border-radius:999px;background:var(--line);opacity:.9}
    .bottom-dock strong{font-family:var(--mono);font-size:12px}
    .bottom-dock .hint{font-family:var(--mono);font-size:11px;color:var(--muted)}
    .bottom-dock input[type="text"]{height:36px;border:1px solid var(--line);background:var(--cream);padding:0 10px;font-family:var(--mono);font-size:12px;min-width:200px;flex:1}
    .bottom-dock select{height:36px;border:1px solid var(--line);background:var(--cream);padding:0 8px;font-family:var(--mono);font-size:12px}
    .flash{animation:flash .9s var(--ease)}
    @keyframes flash{0%{background:rgba(216,108,58,.18)}100%{background:var(--cream)}}
    .admin-modal{position:fixed;inset:0;z-index:50;display:none;place-items:center;background:rgba(15,26,20,.38);padding:16px}
    .admin-modal.open{display:grid}
    .admin-modal-box{width:min(440px,92vw);background:var(--cream);border:1px solid var(--ink);padding:20px;display:grid;gap:14px}
    .admin-modal-box h3{margin:0;font-family:var(--sans);font-size:16px;font-weight:700;color:var(--ink)}
    .admin-modal-box input{height:40px;border:1px solid var(--line);background:var(--paper);padding:0 12px;color:var(--ink);font-family:var(--sans);font-size:13px}
    .admin-modal-box input:focus{border-color:var(--ink);outline:2px solid rgba(216,108,58,.18);outline-offset:0}
    .admin-modal-actions{display:flex;gap:8px;justify-content:flex-end}
    @media(max-width:980px){.topbar-inner{grid-template-columns:1fr auto}.search-box{grid-column:1 / -1;order:3}.layout{display:flex;flex-direction:column;gap:18px}.layout .sidebar{order:2;position:static}.workspace{display:contents}.catalog-intro{order:1}.toolbar{order:3}.project-grid,.project-list{order:4;grid-template-columns:1fr}.filter-panel{display:flex;align-items:center;gap:10px}.filter-head{flex:0 0 auto;border:0;padding:0 8px}.filter-list{display:flex;flex:1;min-width:0;gap:6px;overflow:auto;padding-bottom:4px}.facet{flex:0 0 auto;white-space:nowrap}.mode-organize .facet-row{flex:0 0 auto;border-bottom:0;border-right:1px solid var(--grid)}}
    @media(max-width:680px){.topbar-inner,.layout{padding-left:14px;padding-right:14px}.catalog-title{font-size:26px}.bottom-dock{bottom:12px;padding:12px 14px;border-radius:14px;width:calc(100vw - 16px);max-width:calc(100vw - 16px)}}
    @media(prefers-reduced-motion:reduce){.drawer-panel,.bottom-dock,.project-card{transition:none}.bottom-dock{transform:translateX(-50%) translateY(calc(100% + 28px));opacity:0}.bottom-dock.open{transform:translateX(-50%) translateY(0);opacity:1}}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="#" aria-label="Skills-Hub">
        <div class="mark" aria-hidden="true"><svg viewBox="0 0 32 32" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="7" width="20" height="5.5" rx="1.1"/><rect x="6" y="13.2" width="20" height="5.5" rx="1.1"/><rect x="6" y="19.5" width="20" height="5.5" rx="1.1"/><path d="M10 9.7h3M10 16h5.5M10 22.2h7" opacity=".85"/></svg></div>
        <div>
          <h1 class="brand-title">Skills-Hub</h1>
          <div class="brand-meta" id="brandMeta">CATALOG</div>
        </div>
      </a>
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input id="searchInput" type="search" placeholder="搜索项目或 skill" autocomplete="off">
        <button class="clear-search" id="clearSearch" title="清空搜索" aria-label="清空搜索">×</button>
      </div>
      <div class="actions">
        <button class="nav-link" id="languageToggle" type="button">EN</button>
        <a class="gh-icon gh-icon--topbar" id="githubLink" href="https://github.com/Jst-Well-Dan/Skills-Hub" target="_blank" rel="noreferrer" aria-label="Skills-Hub 本体仓库" title="Skills-Hub 本体仓库（GitHub）"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></a>
      </div>
    </div>
  </header>
  <div class="admin-bar" id="adminBar" role="tablist" aria-label="管理模式">
    <div class="admin-bar-inner">
      <div class="admin-bar-left">
        <strong>ADMIN 模式</strong>
        <div class="segmented" id="modeSwitch">
          <button class="segment active" data-mode="organize" role="tab" aria-selected="true">整理模式</button>
          <button class="segment" data-mode="deploy" role="tab" aria-selected="false">部署模式</button>
        </div>
        <span class="admin-hint" id="adminHint">目录策展 · 拖拽卡片到左栏可移动</span>
      </div>
    </div>
  </div>

  <main class="layout" id="layoutRoot">
    <aside class="sidebar" id="sidebar" aria-label="分类筛选">
      <section class="filter-panel">
        <div class="filter-head"><h2 class="filter-title" id="filterTitle">分类</h2><button class="admin-chip" id="newCatBtn" style="min-height:28px;padding:0 8px;font-size:11px;display:none">+ 新建</button></div>
        <div class="filter-list" id="categoryFilters"></div>
        <div id="sidebarFoot" style="padding:10px 12px;border-top:1px solid var(--line);display:none"><span class="admin-hint">整理模式可改名/删除/拖拽</span></div>
      </section>
    </aside>

    <section class="workspace">
      <header class="catalog-intro">
        <h2 class="catalog-title" id="catalogTitle">Agent Skills 目录</h2>
        <p class="catalog-copy" id="catalogCopy">收录 35 个项目 · 441 个 Skills，支持按分类、关键词及来源筛选。</p>
      </header>
      <div class="toolbar">
        <div class="result-meta" id="resultMeta"></div>
        <div class="toolbar-actions">
          <div class="segmented" id="viewModes" role="tablist" aria-label="展示模式">
            <button class="segment active" id="gridView" data-view="grid">网格</button>
            <button class="segment" id="listView" data-view="list">列表</button>
          </div>
          <select class="sort-select" id="sortSelect" aria-label="排序">
            <option value="name" id="sortName">按名称</option>
            <option value="skills" id="sortSkills">按 skill 数</option>
            <option value="updated" id="sortUpdated">按检查日期</option>
          </select>
        </div>
      </div>
      <div class="project-grid" id="projectGrid"></div>
    </section>
  </main>

  <!-- bottom docks B2 - floating cards -->
  <div class="bottom-dock" id="bottomDockOrganize" aria-label="整理底坞">
    <strong id="dockOrganizeCount">已选 0 个项目</strong>
    <span class="hint">移动到</span>
    <select class="admin-chip" id="batchTargetOrganize" aria-label="目标分类"></select>
    <button class="admin-chip primary" id="batchMoveBtn">批量移动</button>
    <button class="admin-chip" id="dockNewCatBtn">新建分类</button>
    <button class="admin-chip" id="regenBtn">重新生成</button>
    <span class="hint" id="dockOrganizeHint" role="status" aria-live="polite"></span>
  </div>
  <div class="bottom-dock" id="bottomDockDeploy" aria-label="部署底坞">
    <strong id="dockDeployCount">已选 0 个 skill + 0 个项目</strong>
    <button class="admin-chip" id="selectCategorySkillsBtn" title="全选当前过滤分类下所有 skills">全选当前分类的 skills</button>
    <input type="text" id="deployRoot" placeholder="目标路径，如 E:\Code\my-app">
    <button class="admin-chip" id="browseBtn">浏览</button>
    <select id="deployDir"><option value=".claude">.claude</option><option value=".codex">.codex</option><option value=".agents">.agents</option><option value=".pi">.pi</option><option value="custom">自定义…</option></select>
    <input type="text" id="deployCustomDir" placeholder="自定义目录" style="display:none;min-width:120px">
    <button class="admin-chip primary" id="deployBtn">部署选中</button>
    <span class="hint" id="deployHint"></span>
  </div>

  <div class="drawer" id="drawer" aria-hidden="true">
    <div class="drawer-backdrop" id="drawerBackdrop"></div>
    <section class="drawer-panel" id="drawerPanel" role="dialog" aria-modal="true" aria-label="项目详情">
      <div class="drawer-head">
        <div>
          <h2 class="drawer-title" id="drawerTitle"></h2>
          <p class="description" id="drawerDescription"></p>
        </div>
        <div class="drawer-head-actions">
          <button class="nav-link language-toggle" id="drawerLanguageToggle" type="button">EN</button>
          <a class="gh-icon" id="drawerSourceLink" href="#" target="_blank" rel="noreferrer" aria-label="上游仓库" title="上游仓库"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></a>
          <button class="icon-button" id="closeDrawer" title="关闭" aria-label="关闭">×</button>
        </div>
      </div>
      <div class="drawer-body" id="drawerBody"></div>
    </section>
  </div>
  <!-- admin dual drawers: organize/deploy detail overlays (share style) -->
  <div class="drawer" id="drawerOrganize" aria-hidden="true">
    <div class="drawer-backdrop" data-close="organize"></div>
    <section class="drawer-panel" role="dialog" aria-modal="true" aria-label="整理详情">
      <div class="drawer-head">
        <div><h2 class="drawer-title" id="drawerOrganizeTitle"></h2><p class="description" id="drawerOrganizeDesc"></p>
          <label style="display:flex;gap:8px;align-items:center;margin-top:10px;font-family:var(--mono);font-size:12px"><input type="checkbox" id="drawerOrganizeCheck"> 选择此项目加入批量移动</label>
        </div>
        <button class="icon-button" data-close="organize" aria-label="关闭">×</button>
      </div>
      <div class="drawer-body" id="drawerOrganizeBody"></div>
      <div style="padding:12px 18px;border-top:1px solid var(--line);background:var(--cream)"><div style="padding:8px;border:1px dashed var(--line);background:var(--cream);font-family:var(--mono);font-size:11px;color:var(--muted)">整理抽屉仅项目级勾选，skill 不可勾 — 移动以项目为单位。</div></div>
    </section>
  </div>
  <div class="drawer" id="drawerDeploy" aria-hidden="true">
    <div class="drawer-backdrop" data-close="deploy"></div>
    <section class="drawer-panel" role="dialog" aria-modal="true" aria-label="部署详情">
      <div class="drawer-head">
        <div><h2 class="drawer-title" id="drawerDeployTitle"></h2><p class="description" id="drawerDeployDesc"></p>
          <div style="margin-top:10px;display:flex;gap:8px"><button class="admin-chip" id="drawerSelectAllSkills">全选本项目 skills</button><button class="admin-chip" id="drawerClearAllSkills">全不选本项目</button></div>
        </div>
        <button class="icon-button" data-close="deploy" aria-label="关闭">×</button>
      </div>
      <div class="drawer-body" id="drawerDeployBody"></div>
      <div style="padding:12px 18px;border-top:1px solid var(--line);background:var(--cream)"><div style="padding:8px;border:1px dashed var(--line);background:var(--cream);font-family:var(--mono);font-size:11px;color:var(--muted)">部署抽屉可到单 skill 粒度勾选。</div></div>
    </section>
  </div>

  <div class="admin-modal" id="browseModal" style="z-index:55">
    <div class="admin-modal-box" style="width:min(560px,92vw)">
      <h3>选择目标目录</h3>
      <div style="display:flex;gap:8px;align-items:center">
        <input id="browsePathInput" style="flex:1" placeholder="E:\Code\my-app" />
        <button class="admin-chip" id="browseUpBtn" title="上级目录">⬆ 上级</button>
        <button class="admin-chip primary" id="browseSelectBtn">选定此目录</button>
      </div>
      <div id="browseList" style="max-height:320px;overflow:auto;border:1px solid var(--line);border-radius:8px;padding:6px;display:grid;gap:4px;background:var(--paper)"></div>
      <div class="admin-modal-actions">
        <button class="admin-chip" id="browseCancelBtn">取消</button>
      </div>
    </div>
  </div>
  <div class="admin-modal" id="adminModal">
    <div class="admin-modal-box">
      <h3 id="adminModalTitle">新建分类</h3>
      <input id="adminModalId" placeholder="ID（英文小写，如 content-creation）" />
      <input id="adminModalLabel" placeholder="分类名称（中文，如 内容创作类）" />
      <div class="admin-modal-actions">
        <button class="admin-chip" id="adminModalCancel">取消</button>
        <button class="admin-chip primary" id="adminModalOk">确定</button>
      </div>
      <div class="admin-hint" id="adminModalHint" style="font-size:12px;color:#b45309"></div>
    </div>
  </div>

  <script>
    window.SKILL_HUB_DATA = __SKILL_HUB_PAYLOAD__;
    const REPO_URL = "https://github.com/Jst-Well-Dan/Skills-Hub";
    function distinctiveTags(tags){const f=(tags||[]).filter(t=>t!=="coding"&&t!=="docs");if(f.length>0) return f.slice(0,3);return (tags||[]).slice(0,2)}
    const state={query:"",category:"all",sort:"name",view:"grid",selected:null,language:"zh"};
    const data=window.SKILL_HUB_DATA;
    const copy={zh:{brandMeta:"CATALOG · "+data.summary.project_count+" PROJECTS",search:"搜索项目或 skill",clear:"清空搜索",filter:"分类",all:"全部",title:"Agent Skills 目录",intro:""+data.summary.project_count+" 个项目 · "+data.summary.skill_count+" 个 Skills，支持按分类、关键词及来源筛选。",grid:"网格",list:"列表",sortName:"按名称",sortSkills:"按 skill 数",sortUpdated:"按检查日期",noDescription:"暂无简介",openGithub:"打开 GitHub",viewDirectory:"查看目录",empty:"没有匹配的 skill 库",projectDirectory:"查看项目目录",installHelp:"查看源仓库安装说明",category:"分类",install:"安装",viewContent:"查看内容",collapseContent:"收起内容",loading:"加载中…",loadFailed:"加载失败，请重试",reviews:"相关点评",projects:"个项目"},en:{brandMeta:"CATALOG · "+data.summary.project_count+" PROJECTS",search:"Search projects or skills",clear:"Clear search",filter:"Category",all:"All",title:"Agent Skills Catalog",intro:""+data.summary.project_count+" projects · "+data.summary.skill_count+" skills. Filter by category, keyword and source.",grid:"Grid",list:"List",sortName:"By name",sortSkills:"By skill count",sortUpdated:"By check date",noDescription:"No description",openGithub:"Open GitHub",viewDirectory:"View directory",empty:"No matching skill libraries",projectDirectory:"View project directory",installHelp:"View installation instructions in the source repository",category:"Category",install:"Install",viewContent:"View content",collapseContent:"Collapse content",loading:"Loading…",loadFailed:"Failed to load. Try again.",reviews:"Related reviews",projects:"projects"}};
    let skillContentPromise;
    const el=(id)=>document.getElementById(id);
    const text=(v)=>String(v??"");
    const t=(k)=>copy[state.language][k];
    const categoryLabel=(id)=>data.category_labels[id]||id;
    const descriptionOf=(item)=>item.description;
    const sourceOf=(p)=>p.source?.repo||p.source?.type||"local";
    const sourceUrl=(p)=>p.source?.repo?`https://github.com/${p.source.repo}`:`${REPO_URL}/tree/main/${p.path}`;
    const normalize=(v)=>text(v).toLowerCase();
    const readableText=(v)=>text(v).replaceAll("—"," - ").replaceAll("–","-");
    const loadSkillContent=()=>skillContentPromise||=fetch("skill-content.json").then(r=>{if(!r.ok) throw new Error(`HTTP ${r.status}`);return r.json()});
    function escapeHtml(v){return readableText(v).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;")}
    function projectHaystack(p){const skills=(p.skills||[]).flatMap(s=>[s.name,s.id,s.description,s.description_zh,s.path,...(s.tags||[])]);return normalize([p.name,p.id,p.description,p.description_zh,p.path,data.category_labels[p.category],...(p.tags||[]),sourceOf(p),...skills].join(" "))}
    function matches(p){if(state.category!=="all"&&p.category!==state.category) return false;const terms=normalize(state.query).split(/\s+/).filter(Boolean);return terms.every(term=>projectHaystack(p).includes(term))}
    function sortProjects(list){const sorted=[...list];sorted.sort((a,b)=>{if(state.sort==="skills") return (b.skill_count||0)-(a.skill_count||0)||a.name.localeCompare(b.name);if(state.sort==="updated") return text(b.last_checked_at).localeCompare(text(a.last_checked_at))||a.name.localeCompare(b.name);return a.name.localeCompare(b.name)});return sorted}
    const GH_SVG='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>';
    const FOLDER_SVG='<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M2 2.5A1.5 1.5 0 013.5 1h3.38a1 1 0 01.89.55L8.62 3.5H12.5A1.5 1.5 0 0114 5v7a1.5 1.5 0 01-1.5 1.5H3.5A1.5 1.5 0 012 12V2.5zm.5.5V12a.5.5 0 00.5.5h9a.5.5 0 00.5-.5V5a.5.5 0 00-.5-.5H8.62a1 1 0 01-.89-.55L6.88 2H3.5a.5.5 0 00-.5.5z"/></svg>';
    // base renderers (non-admin)
    function baseProjectCard(project){
      const isGh=!!project.source?.repo;const ghUrl=escapeHtml(sourceUrl(project));const ghLabel=isGh?`上游仓库 ${project.source.repo}`:`本地目录 ${project.path}`;const ghIcon=isGh?GH_SVG:FOLDER_SVG;const dt=distinctiveTags(project.tags||[]);const tagsHtml=dt.length?`<div class="card-tags">${dt.map(tag=>`<span>#${escapeHtml(tag)}</span>`).join("")}</div>`:`<span style="color:var(--muted);font-family:var(--mono);font-size:11px">— 无区分标签</span>`;
      return `<article class="project-card"><button class="project-main" data-project-id="${escapeHtml(project.id)}"><div class="eyebrow">${escapeHtml(categoryLabel(project.category))} · ${project.skill_count||0} skills</div><div class="project-row"><h3 class="project-name">${escapeHtml(project.name)}</h3><span class="badge">${project.skill_count||0} skills</span></div><p class="description">${escapeHtml(descriptionOf(project)||t("noDescription"))}</p></button><div class="project-foot">${tagsHtml}<a class="gh-icon" href="${ghUrl}" target="_blank" rel="noreferrer" aria-label="${escapeHtml(ghLabel)}" title="${escapeHtml(ghLabel)}">${ghIcon}</a></div></article>`;
    }
    let projectCard = baseProjectCard;
    function renderCategoriesBase(){
      const visible=[{id:"all",count:data.summary.project_count},...data.facets.categories.filter(c=>c.count>0)];
      const buttons=visible.map(item=>`<div class="facet-row" data-row="${escapeHtml(item.id)}"><button class="facet ${state.category===item.id?"active":""}" data-category="${escapeHtml(item.id)}"><span>${escapeHtml(item.id==="all"?t("all"):categoryLabel(item.id))}</span><span class="count">${item.count}</span></button></div>`).join("");
      el("categoryFilters").innerHTML=buttons;
    }
    let renderCategories = renderCategoriesBase;
    function renderProjectsBase(projects){
      const grid=el("projectGrid");grid.className=state.view==="list"?"project-list":"project-grid";if(!projects.length){grid.innerHTML=`<div class="empty">${t("empty")}</div>`;return}grid.innerHTML=projects.map(projectCard).join("");
    }
    let renderProjects = renderProjectsBase;
    function renderDrawer(project){
      if(!project) return;state.selected=project.id;el("drawerTitle").textContent=project.name;el("drawerDescription").textContent=readableText(descriptionOf(project)||t("noDescription"));const dsl=el("drawerSourceLink");dsl.href=sourceUrl(project);const isGh=!!project.source?.repo;const dslLabel=isGh?`上游仓库 ${project.source.repo}`:`本地目录 ${project.path}`;dsl.setAttribute("aria-label",dslLabel);dsl.title=dslLabel;const install=project.install?.method==="npx"&&project.install.command?`<code>${escapeHtml(project.install.command)}</code>`:`<a href="${escapeHtml(sourceUrl(project))}" target="_blank" rel="noreferrer">${t("installHelp")}</a>`;const skills=[...(project.skills||[])].sort((a,b)=>a.name.localeCompare(b.name));function skillGhUrl(skill){if(project.source?.repo){let rel=skill.path||"";const prefix=`libraries/${project.id}/`;if(rel.startsWith(prefix)) rel=rel.slice(prefix.length);else if(rel.startsWith("libraries/")) rel=rel.split("/").slice(2).join("/");return `https://github.com/${project.source.repo}/tree/main/${rel}`;}return `${REPO_URL}/tree/main/${skill.path||project.path}`;}const skillHtml=skills.map((skill,index)=>{const sIsGh=!!project.source?.repo;const sUrl=escapeHtml(skillGhUrl(skill));const sLabel=sIsGh?`原 Skill 源码 ${project.source.repo}`:`本地 Skill ${skill.name}`;const sIcon=sIsGh?GH_SVG:FOLDER_SVG;return `<article class="skill-item"><div style="display:flex;justify-content:space-between;gap:12px;align-items:start"><div style="min-width:0"><div class="skill-name">${escapeHtml(skill.name)}</div><p class="skill-description">${escapeHtml(descriptionOf(skill)||t("noDescription"))}</p></div><a class="gh-icon small" href="${sUrl}" target="_blank" rel="noreferrer" aria-label="${escapeHtml(sLabel)}" title="${escapeHtml(sLabel)}">${sIcon}</a></div><div class="links"><button class="text-link" data-skill-path="${escapeHtml(skill.path)}" data-panel-id="skill-panel-${index}" aria-expanded="false">${t("viewContent")}</button></div><section class="skill-panel" id="skill-panel-${index}" aria-live="polite" hidden></section></article>`}).join("");el("drawerBody").innerHTML=`<div class="detail-grid"><div class="detail"><div class="detail-label">${t("category")}</div><div class="detail-value">${escapeHtml(categoryLabel(project.category))}</div></div><div class="detail"><div class="detail-label">${t("install")}</div><div class="detail-value">${install}</div></div></div><h3 class="section-title">Skills · ${skills.length}</h3><div class="skill-list">${skillHtml}</div>`;el("drawer").classList.add("open");el("drawer").setAttribute("aria-hidden","false");
    }
    function setContentLanguage(panel){const record=panel.skillRecord;const content=panel.querySelector(".skill-content");content.textContent=text(record.original);content.dataset.language="original"}
    function renderSkillPanel(panel,record){panel.skillRecord=record;const reviews=(record.reviews||[]).length?`<section class="related-reviews"><h4 class="review-title">${t("reviews")}</h4>${record.reviews.map(r=>`<a class="review-link" href="${REPO_URL}/blob/main/docs/reviews/${encodeURIComponent(r.slug)}.md" target="_blank" rel="noreferrer"><span>${escapeHtml(r.title)}</span><span class="review-meta">${escapeHtml(r.type_label)} →</span></a>`).join("")}</section>`:"";panel.innerHTML=`<pre class="skill-content"></pre>${reviews}`;setContentLanguage(panel)}
    function closeDrawer(){el("drawer").classList.remove("open");el("drawer").setAttribute("aria-hidden","true");state.selected=null}
    function closeAdminDrawers(){el("drawerOrganize")?.classList.remove("open");el("drawerOrganize")?.setAttribute("aria-hidden","true");el("drawerDeploy")?.classList.remove("open");el("drawerDeploy")?.setAttribute("aria-hidden","true");}
    function render(){
      const projects=sortProjects(data.projects.filter(matches));
      renderCategories();
      renderProjects(projects);
      el("resultMeta").textContent=state.query||state.category!=="all"?`${projects.length} / ${data.summary.project_count} ${t("projects")}`:`${data.summary.project_count} ${t("projects")} · ${data.summary.skill_count} skills`;
      document.querySelectorAll("#viewModes .segment").forEach(b=>b.classList.toggle("active",b.dataset.view===state.view));
      if(isAdmin) updateAdminDocks();
    }
    function applyLanguage(){document.documentElement.lang="zh-CN";document.title="Skills-Hub - Agent Skills 目录";el("brandMeta").textContent=t("brandMeta");el("searchInput").placeholder=t("search");el("clearSearch").title=el("clearSearch").ariaLabel=t("clear");const _gl=el("githubLink"); if(_gl){ _gl.setAttribute("aria-label","Skills-Hub 本体仓库"); _gl.title="Skills-Hub 本体仓库（GitHub）"; }el("filterTitle").textContent=t("filter");el("catalogTitle").innerHTML=t("title");el("catalogCopy").textContent=t("intro");el("gridView").textContent=t("grid");el("listView").textContent=t("list");el("sortName").textContent=t("sortName");el("sortSkills").textContent=t("sortSkills");el("sortUpdated").textContent=t("sortUpdated");render();if(state.selected){const p=data.projects.find(x=>x.id===state.selected); if(p) renderDrawer(p)}}
    document.addEventListener("click", async (event)=>{
      const skillButton=event.target.closest("[data-skill-path]");
      if(skillButton){
        const panel=document.getElementById(skillButton.dataset.panelId);
        if(!panel) return;
        if(!panel.hidden){panel.hidden=true;skillButton.textContent=t("viewContent");skillButton.setAttribute("aria-expanded","false");return}
        skillButton.textContent=t("loading");skillButton.disabled=true;
        try{const docs=await loadSkillContent();const record=docs[skillButton.dataset.skillPath];if(!record) throw new Error("missing");renderSkillPanel(panel,record);panel.hidden=false;skillButton.textContent=t("collapseContent");skillButton.setAttribute("aria-expanded","true")}catch{skillButton.textContent=t("loadFailed")}finally{skillButton.disabled=false}
        return;
      }
      const category=event.target.closest("[data-category]");
      if(category){state.category=category.dataset.category;render();return}
      const projectButton=event.target.closest("[data-project-id]");
      if(projectButton){
        const proj=data.projects.find(p=>p.id===projectButton.dataset.projectId);
        if(isAdmin){
          // admin dual-mode detail: open mode-specific drawer
          openAdminDetail(proj.id);
        } else {
          renderDrawer(proj);
        }
      }
    });
    el("searchInput").addEventListener("input",e=>{state.query=e.target.value;render()});
    el("clearSearch").addEventListener("click",()=>{state.query="";el("searchInput").value="";render()});
    el("sortSelect").addEventListener("change",e=>{state.sort=e.target.value;render()});
    document.querySelectorAll("#viewModes .segment").forEach(b=>b.addEventListener("click",()=>{state.view=b.dataset.view;render()}));
    el("closeDrawer").addEventListener("click",closeDrawer);
    el("drawerBackdrop").addEventListener("click",closeDrawer);
    document.addEventListener("keydown",e=>{if(e.key==="Escape"){closeDrawer();closeAdminDrawers();const m=el("adminModal");if(m) m.classList.remove("open");const bm=el("browseModal");if(bm) bm.classList.remove("open")}});
    // ===== Admin B2 dual-mode =====
    const ADMIN_API="http://127.0.0.1:5173";
    const isAdmin=new URLSearchParams(location.search).has("admin")||localStorage.getItem("skill-hub-admin")==="1";
    const adminState={selected:new Set(), dragging:null, mode: localStorage.getItem("skill-hub-admin-mode")||"organize", skillSelected: new Set(), currentDrawerId:null};
    function isOrganize(){return adminState.mode==="organize";}
    function updateAdminDocks(){
      if(!isAdmin) return;
      const org=el("bottomDockOrganize"), dep=el("bottomDockDeploy");
      if(isOrganize()){ org?.classList.add("open"); dep?.classList.remove("open"); if(el("dockOrganizeCount")) el("dockOrganizeCount").textContent=`已选 ${adminState.selected.size} 个项目`; }
      else { dep?.classList.add("open"); org?.classList.remove("open"); if(el("dockDeployCount")) el("dockDeployCount").textContent=`已选 ${adminState.skillSelected.size} 个 skill + ${adminState.selected.size} 个项目`; }
      const hint=el("adminHint"); if(hint) hint.textContent = isOrganize() ? "目录策展· 拖拽卡片到左栏可移动" : "文件分发 · 按分类筛选后批量部署";
    }
    function flash(el2, msg){
      if(!el2) return; el2.textContent=msg; el2.parentElement?.classList.add("flash"); setTimeout(()=> el2.parentElement?.classList.remove("flash"), 900);
    }
    async function adminFetch(path,opts){try{const r=await fetch(ADMIN_API+path,opts);const j=await r.json();if(!r.ok) throw new Error(j.error||r.statusText);return j}catch(e){throw e}}
    function adminSlug(v){return String(v||"").trim().toLowerCase().replace(/[^a-z0-9\u4e00-\u9fff]+/g,"-").replace(/^-|-$/g,"")||""}
    function adminRefreshBatchTargets(){
      const sel=el("batchTargetOrganize"); if(!sel) return;
      sel.innerHTML=Object.entries(data.category_labels).map(([id,label])=>`<option value="${escapeHtml(id)}">${escapeHtml(label)} (${escapeHtml(id)})</option>`).join("");
    }
    // override renderCategories for B2
    const _origRenderCategoriesB2 = renderCategories;
    renderCategories = function(){
      _origRenderCategoriesB2();
      if(!isAdmin) return;
      document.body.classList.add("admin-b2");
      el("adminBar")?.classList.add("open");
      const layout=el("layoutRoot"); if(layout) layout.className = isOrganize() ? "layout mode-organize" : "layout";
      const newCatBtn=el("newCatBtn"), foot=el("sidebarFoot");
      if(newCatBtn) newCatBtn.style.display = isOrganize() ? "" : "none";
      if(foot) foot.style.display = isOrganize() ? "" : "none";
      adminRefreshBatchTargets();
      // bind rename/delete and drag for organize mode
      document.querySelectorAll("[data-row]").forEach(row=>{
        const cid=row.dataset.row; if(cid==="all") return;
        const btn=row.querySelector("[data-category]");
        if(btn){
          btn.addEventListener("dragover",e=>{ if(!isOrganize()) return; e.preventDefault(); row.classList.add("drag-over"); });
          btn.addEventListener("dragleave",()=> row.classList.remove("drag-over"));
        }
        row.addEventListener("dragover",e=>{ if(!isOrganize()) return; e.preventDefault(); row.classList.add("drag-over"); });
        row.addEventListener("dragleave",()=> row.classList.remove("drag-over"));
        row.addEventListener("drop", async e=>{
          if(!isOrganize()) return;
          e.preventDefault(); row.classList.remove("drag-over");
          const targetCat=row.dataset.row;
          const ids=adminState.dragging?[adminState.dragging]:[...adminState.selected];
          if(!ids.length || targetCat==="all") return;
          flash(el("dockOrganizeHint"),"移动中…");
          try{ try{await adminFetch("/api/projects/move",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({ids,category:targetCat})})}catch(_){ }
            ids.forEach(id=>{const p=data.projects.find(x=>x.id===id); if(p){p.category=targetCat;p.category_locked=true;}});
            const counts={}; data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});
            data.facets.categories=Object.entries(data.category_labels).map(([id,label])=>({id,label,count:counts[id]||0}));
            adminState.selected.clear(); adminState.dragging=null;
            render(); flash(el("dockOrganizeHint"),`已移动 ${ids.length} 项 → ${data.category_labels[targetCat]||targetCat}`);
          }catch(err){ flash(el("dockOrganizeHint"),"移动失败: "+err.message); }
        });
        if(!row.querySelector(".facet-actions")){
          const acts=document.createElement("span"); acts.className="facet-actions";
          acts.innerHTML=`<button title="重命名分类" data-act="rename" data-id="${escapeHtml(cid)}">改名</button><button title="删除分类" data-act="delete" data-id="${escapeHtml(cid)}">删除</button>`;
          row.appendChild(acts);
          acts.querySelectorAll("button").forEach(b=> b.addEventListener("click", async e=>{
            e.stopPropagation(); const act=b.dataset.act,id=b.dataset.id;
            if(act==="delete"){
              if(!confirm(`删除分类「${data.category_labels[id]||id}」？旗下项目将移入“未分类”。`)) return;
              flash(el("dockOrganizeHint"),"删除中…");
              try{ try{await adminFetch("/api/categories",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({action:"delete",id})})}catch(_){}
                const moved=data.projects.filter(p=>p.category===id);
                moved.forEach(p=>{p.category="uncategorized";p.category_locked=true;});
                delete data.category_labels[id]; delete data.category_labels_en[id];
                if(!data.category_labels["uncategorized"]){data.category_labels["uncategorized"]="未分类";data.category_labels_en["uncategorized"]="Uncategorized";}
                const counts={}; data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});
                data.facets.categories=Object.entries(data.category_labels).map(([i,l])=>({id:i,label:l,count:counts[i]||0}));
                if(state.category===id) state.category="all";
                render(); flash(el("dockOrganizeHint"),`已删除，已移动 ${moved.length} 个项目`);
              }catch(err){ flash(el("dockOrganizeHint"),err.message); }
            } else if(act==="rename"){ adminOpenModal("rename",id); }
          }));
        }
      });
      updateAdminDocks();
    };
    // override projectCard for B2
    const _origProjectCardB2 = projectCard;
    projectCard = function(project){
      const html=_origProjectCardB2(project);
      if(!isAdmin) return html;
      const checked=adminState.selected.has(project.id)?"checked":"";
      const draggable = isOrganize() ? ` draggable="true" data-drag-id="${escapeHtml(project.id)}"` : "";
      const selClass = adminState.selected.has(project.id) ? " selected" : "";
      return html.replace('<article class="project-card">', `<article class="project-card has-check${selClass}"${draggable} data-id="${escapeHtml(project.id)}">`)
                 .replace('</article>', `<label class="admin-check-wrap" aria-label="选择 ${escapeHtml(project.name)}"><input class="admin-checkbox" type="checkbox" data-check-id="${escapeHtml(project.id)}" ${checked} /></label></article>`);
    };
    function adminWireCardEventsB2(){
      if(!isAdmin) return;
      document.querySelectorAll("[data-drag-id]").forEach(card=>{
        card.addEventListener("dragstart",e=>{ adminState.dragging=card.dataset.dragId||card.dataset.id; card.classList.add("dragging"); e.dataTransfer.effectAllowed="move"; if(card.dataset.id) e.dataTransfer.setData("text/plain", card.dataset.id); });
        card.addEventListener("dragend",()=>{ adminState.dragging=null; card.classList.remove("dragging"); });
      });
      document.querySelectorAll(".admin-check-wrap").forEach(w=>{ w.addEventListener("click",e=>e.stopPropagation()); w.addEventListener("mousedown",e=>e.stopPropagation()); });
      document.querySelectorAll("[data-check-id]").forEach(cb=>{
        const handler = (e)=>{
          e.stopPropagation(); const id=cb.dataset.checkId;
          const isChecked = cb.checked;
          if(isOrganize()){
            if(isChecked) adminState.selected.add(id); else adminState.selected.delete(id);
            cb.closest(".project-card")?.classList.toggle("selected", isChecked);
            syncOrganizeDrawerCheck();
          } else {
            const proj=data.projects.find(x=>x.id===id);
            if(isChecked){ adminState.selected.add(id); (proj?.skills||[]).forEach(sk=> adminState.skillSelected.add(sk.path||sk.id)); }
            else { adminState.selected.delete(id); (proj?.skills||[]).forEach(sk=> adminState.skillSelected.delete(sk.path||sk.id)); }
          }
          updateAdminDocks(); renderProjects(sortProjects(data.projects.filter(matches)));
          // re-wire after re-render will happen via renderProjects wrapper, but update docks immediately
          setTimeout(adminWireCardEventsB2,0);
        };
        cb.addEventListener("click", handler);
        cb.addEventListener("change", handler);
      });
    }
    const _origRenderProjectsB2 = renderProjects;
    renderProjects = function(projects){
      _origRenderProjectsB2(projects);
      if(isAdmin) setTimeout(adminWireCardEventsB2,0);
    };
    const _origRenderB2 = render;
    render = function(){ _origRenderB2(); if(isAdmin) { updateAdminDocks(); } };
    function syncOrganizeDrawerCheck(){
      const cb=el("drawerOrganizeCheck"); if(cb && adminState.currentDrawerId) cb.checked = adminState.selected.has(adminState.currentDrawerId);
    }
    function skillListHtml(project, forDeploy){
      const sorted=[...(project.skills||[])].sort((a,b)=>a.name.localeCompare(b.name));
      return sorted.map((skill, idx)=>{
        const key=skill.path||skill.id;
        const checked = adminState.skillSelected.has(key);
        const deployCheck = forDeploy ? `<label style="display:flex;gap:8px;align-items:center;font-family:var(--mono);font-size:12px"><input type="checkbox" data-skill="${escapeHtml(skill.path)}" data-project="${escapeHtml(project.id)}" ${checked?'checked':''}> 勾选此 skill</label>` : '';
        const ghUrl = project.source?.repo ? `https://github.com/${project.source.repo}/tree/main/${(skill.path||"").replace(/^libraries\//,"").split("/").slice(1).join("/")}` : `${REPO_URL}/tree/main/${skill.path||project.path}`;
        // reuse skill panel logic with loadSkillContent
        return `<div class="skill-item">${deployCheck}<div class="skill-name">${escapeHtml(skill.name)}</div><p class="skill-description">${escapeHtml(descriptionOf(skill)||t("noDescription"))}</p><div style="display:flex;gap:8px;align-items:center"><a class="gh-icon small" href="${escapeHtml(ghUrl)}" target="_blank" rel="noreferrer" title="${escapeHtml(skill.path)}">${GH_SVG}</a><button class="text-link" data-skill-path="${escapeHtml(skill.path)}" data-panel-id="skill-panel-${forDeploy?'deploy':'organize'}-${idx}" aria-expanded="false">${t("viewContent")}</button></div><section class="skill-panel" id="skill-panel-${forDeploy?'deploy':'organize'}-${idx}" hidden></section></div>`;
      }).join("");
    }
    function openAdminDetail(id){
      const project=data.projects.find(x=>x.id===id); if(!project) return;
      adminState.currentDrawerId=id;
      // ensure skill panels use correct handler (reuse document click for data-skill-path)
      if(isOrganize()){
        el("drawerDeploy")?.classList.remove("open"); el("drawerDeploy")?.setAttribute("aria-hidden","true");
        el("drawerOrganizeTitle").textContent=project.name; el("drawerOrganizeDesc").textContent=readableText(descriptionOf(project)||t("noDescription"));
        const chk=el("drawerOrganizeCheck"); if(chk) chk.checked=adminState.selected.has(id);
        el("drawerOrganizeBody").innerHTML = skillListHtml(project,false);
        el("drawerOrganize")?.classList.add("open"); el("drawerOrganize")?.setAttribute("aria-hidden","false");
        // bind view-content inside
        el("drawerOrganizeBody").querySelectorAll("[data-skill-path]").forEach(btn=>{
          // document click handler already handles, no extra
        });
      } else {
        el("drawer")?.classList.remove("open"); el("drawer")?.setAttribute("aria-hidden","true");
        el("drawerOrganize")?.classList.remove("open"); el("drawerOrganize")?.setAttribute("aria-hidden","true");
        el("drawerDeployTitle").textContent=project.name; el("drawerDeployDesc").textContent=readableText(descriptionOf(project)||t("noDescription"));
        el("drawerDeployBody").innerHTML = skillListHtml(project,true);
        el("drawerDeploy")?.classList.add("open"); el("drawerDeploy")?.setAttribute("aria-hidden","false");
        el("drawerDeployBody").querySelectorAll("[data-skill]").forEach(cb=>{
          cb.addEventListener("change", e=>{
            const key=e.currentTarget.dataset.project+":"+e.currentTarget.dataset.skill; // not used, actual key is path
            const pathKey=e.currentTarget.dataset.skill;
            if(e.currentTarget.checked) adminState.skillSelected.add(pathKey); else adminState.skillSelected.delete(pathKey);
            if(e.currentTarget.checked) adminState.selected.add(e.currentTarget.dataset.project);
            updateAdminDocks();
          });
          // correct handler using path
          cb.addEventListener("change", e=>{
            const p=e.currentTarget.dataset.skill;
            if(e.currentTarget.checked) adminState.skillSelected.add(p); else adminState.skillSelected.delete(p);
            updateAdminDocks();
          });
        });
        // bind skill checkbox for deploy (dataset.skill)
        el("drawerDeployBody").querySelectorAll("[data-skill]").forEach(cb=>{
          // already bound
        });
        // also support input with data-skill attribute
        el("drawerDeployBody").querySelectorAll("input[data-skill]").forEach(cb=>{
          cb.addEventListener("change", ()=>{
            const p=cb.dataset.skill;
            if(cb.checked) adminState.skillSelected.add(p); else adminState.skillSelected.delete(p);
            if(cb.checked) adminState.selected.add(cb.dataset.project);
            updateAdminDocks();
          });
        });
      }
    }
    function adminOpenModal(mode,cid){
      const modal=el("adminModal"),title=el("adminModalTitle"),idInput=el("adminModalId"),labelInput=el("adminModalLabel"),hint=el("adminModalHint");
      hint.textContent="";
      if(mode==="rename"){title.textContent="重命名分类";idInput.value=cid;idInput.placeholder="新 ID（留空则不改 ID）";labelInput.value=data.category_labels[cid]||"";modal.dataset.mode="rename";modal.dataset.cid=cid}
      else {title.textContent="新建分类";idInput.value="";labelInput.value="";modal.dataset.mode="create";modal.dataset.cid=""}
      modal.classList.add("open"); labelInput.focus();
    }
    // admin bar mode switch
    document.querySelectorAll("#modeSwitch .segment").forEach(btn=>{
      btn.addEventListener("click",()=>{
        const mode=btn.dataset.mode; adminState.mode=mode; localStorage.setItem("skill-hub-admin-mode", mode);
        document.querySelectorAll("#modeSwitch .segment").forEach(b=>{ b.classList.toggle("active", b.dataset.mode===mode); b.setAttribute("aria-selected", b.dataset.mode===mode); });
        closeAdminDrawers(); closeDrawer();
        render();
      });
    });
    // drawer organize check
    el("drawerOrganizeCheck")?.addEventListener("change", e=>{
      const id=adminState.currentDrawerId; if(!id) return;
      if(e.currentTarget.checked) adminState.selected.add(id); else adminState.selected.delete(id);
      updateAdminDocks(); renderProjects(sortProjects(data.projects.filter(matches)));
    });
    document.querySelectorAll("[data-close]").forEach(b=> b.addEventListener("click", ()=>{ closeAdminDrawers(); }));
    document.addEventListener("click", e=>{ if(e.target.closest(".drawer-backdrop[data-close]")) closeAdminDrawers(); });
    el("drawerSelectAllSkills")?.addEventListener("click", ()=>{
      const id=adminState.currentDrawerId; if(!id) return; const p=data.projects.find(x=>x.id===id); (p?.skills||[]).forEach(sk=> adminState.skillSelected.add(sk.path||sk.id)); adminState.selected.add(id); updateAdminDocks(); openAdminDetail(id);
    });
    el("drawerClearAllSkills")?.addEventListener("click", ()=>{
      const id=adminState.currentDrawerId; if(!id) return; const p=data.projects.find(x=>x.id===id); (p?.skills||[]).forEach(sk=> adminState.skillSelected.delete(sk.path||sk.id)); updateAdminDocks(); openAdminDetail(id);
    });
    // bottom dock actions
    el("batchMoveBtn")?.addEventListener("click", async()=>{
      if(adminState.selected.size===0) return flash(el("dockOrganizeHint"),"请先勾选项目");
      const target=el("batchTargetOrganize")?.value;
      if(!target) return flash(el("dockOrganizeHint"),"请选择目标分类");
      flash(el("dockOrganizeHint"),"批量移动中…");
      const ids=[...adminState.selected];
      try{ try{await adminFetch("/api/projects/move",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({ids,category:target})})}catch(_){}
        ids.forEach(id=>{const p=data.projects.find(x=>x.id===id); if(p){p.category=target;p.category_locked=true;}});
        const counts={}; data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});
        data.facets.categories=Object.entries(data.category_labels).map(([id,label])=>({id,label,count:counts[id]||0}));
        adminState.selected.clear(); render(); flash(el("dockOrganizeHint"),`已移动 ${ids.length} 项 → ${data.category_labels[target]||target}`);
      }catch(e){ flash(el("dockOrganizeHint"),"失败: "+e.message); }
    });
    el("dockNewCatBtn")?.addEventListener("click", ()=> adminOpenModal("create"));
    el("newCatBtn")?.addEventListener("click", ()=> adminOpenModal("create"));
    el("regenBtn")?.addEventListener("click", async()=>{ flash(el("dockOrganizeHint"),"重新生成中…"); try{ await adminFetch("/api/regenerate",{method:"POST"}); flash(el("dockOrganizeHint"),"已重新生成 docs/site"); }catch(e){ flash(el("dockOrganizeHint"),"后端未启动，仅本地预览已更新"); } });
    el("adminModalCancel")?.addEventListener("click",()=> el("adminModal").classList.remove("open"));
    el("adminModal")?.addEventListener("click", e=>{ if(e.target===el("adminModal")) el("adminModal").classList.remove("open"); });
    el("adminModalOk")?.addEventListener("click", async()=>{
      const modal=el("adminModal"),mode=modal.dataset.mode,cid=modal.dataset.cid;
      const idRaw=el("adminModalId")?.value.trim(),labelRaw=el("adminModalLabel")?.value.trim();
      const hint=el("adminModalHint");
      if(mode==="create"){
        const nid=adminSlug(idRaw||labelRaw); if(!nid) return hint.textContent="请填写 ID 或名称"; if(!labelRaw) return hint.textContent="请填写分类名称"; if(data.category_labels[nid]) return hint.textContent="ID 已存在";
        try{ try{await adminFetch("/api/categories",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({action:"create",id:nid,label:labelRaw})})}catch(_){}
          data.category_labels[nid]=labelRaw; data.category_labels_en[nid]=labelRaw;
          const counts={}; data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1}); counts[nid]=counts[nid]||0;
          data.facets.categories=Object.entries(data.category_labels).map(([id,l])=>({id,label:l,count:counts[id]||0}));
          render(); hint.textContent=""; modal.classList.remove("open"); flash(el("dockOrganizeHint"),`已新建 ${labelRaw} (${nid})`);
        }catch(e){ hint.textContent=e.message; }
      } else {
        const newIdRaw=el("adminModalId")?.value.trim(); const newId=newIdRaw?adminSlug(newIdRaw):cid; const newLabel=labelRaw||data.category_labels[cid];
        if(!newLabel) return hint.textContent="请填写名称"; if(newId!==cid && data.category_labels[newId]) return hint.textContent="新 ID 已存在";
        try{ try{await adminFetch("/api/categories",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({action:"update",id:cid,label:cid,new_id:newId,new_label:newLabel})})}catch(_){}
          if(newId!==cid){ data.projects.filter(p=>p.category===cid).forEach(p=>{p.category=newId;p.category_locked=true;}); delete data.category_labels[cid]; delete data.category_labels_en[cid]; data.category_labels[newId]=newLabel; data.category_labels_en[newId]=newLabel; if(state.category===cid) state.category=newId; } else { data.category_labels[cid]=newLabel; data.category_labels_en[cid]=newLabel; }
          const counts={}; data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});
          data.facets.categories=Object.entries(data.category_labels).map(([id,l])=>({id,label:l,count:counts[id]||0}));
          render(); modal.classList.remove("open"); flash(el("dockOrganizeHint"),"已重命名");
        }catch(e){ hint.textContent=e.message; }
      }
    });
    // deploy logic
    const deployState = { targetRoot: localStorage.getItem("skill-hub-deploy-root")||"", skillDir: localStorage.getItem("skill-hub-deploy-dir")||".claude" };
    function deploySetHint(msg,isError){ const h=el("deployHint"); if(h){ h.textContent=msg; h.style.color=isError?"#b42318":"#166534"; } }
    function deployGetSkillDir(){ const sel=el("deployDir")?.value; if(sel==="custom") return el("deployCustomDir")?.value.trim()||".claude"; return sel||".claude"; }
    if(isAdmin){
      const tr=el("deployRoot"), sd=el("deployDir"), cd=el("deployCustomDir");
      if(tr) tr.value=deployState.targetRoot;
      if(sd){ sd.value=[".claude",".codex",".agents",".pi"].includes(deployState.skillDir)?deployState.skillDir:"custom"; if(sd.value==="custom" && cd){ cd.style.display=""; cd.value=deployState.skillDir; } }
      tr?.addEventListener("input", ()=>{ deployState.targetRoot=tr.value.trim(); localStorage.setItem("skill-hub-deploy-root", deployState.targetRoot); });
      sd?.addEventListener("change", ()=>{ if(sd.value==="custom"){ cd.style.display=""; cd.focus(); } else { cd.style.display="none"; deployState.skillDir=sd.value; localStorage.setItem("skill-hub-deploy-dir", deployState.skillDir); } });
      cd?.addEventListener("input", ()=>{ deployState.skillDir=cd.value.trim()||".claude"; localStorage.setItem("skill-hub-deploy-dir", deployState.skillDir); });
      el("selectCategorySkillsBtn")?.addEventListener("click", ()=>{
        if(state.category==="all") return flash(el("deployHint"),"请先在左栏选择一个分类");
        const list=data.projects.filter(p=>p.category===state.category);
        list.forEach(p=>{ adminState.selected.add(p.id); (p.skills||[]).forEach(sk=> adminState.skillSelected.add(sk.path||sk.id)); });
        flash(el("deployHint"),`已全选「${categoryLabel(state.category)}」下 ${adminState.skillSelected.size} 个 skills`); updateAdminDocks(); render();
      });
      el("deployBtn")?.addEventListener("click", async ()=>{
        const targetRoot = el("deployRoot")?.value.trim();
        if(!targetRoot) return flash(el("deployHint"),"请先填写目标路径");
        localStorage.setItem("skill-hub-deploy-root", targetRoot);
        const skillDir = deployGetSkillDir();
        localStorage.setItem("skill-hub-deploy-dir", skillDir);
        const skillIds = [...adminState.skillSelected];
        for(const pid of [...adminState.selected]){
          const proj=data.projects.find(p=>p.id===pid);
          if(proj){ for(const sk of proj.skills||[]) if(!skillIds.includes(sk.path||sk.id)) skillIds.push(sk.path||sk.id); }
        }
        if(!skillIds.length) return flash(el("deployHint"),"请先勾选 skill 或项目");
        flash(el("deployHint"),`部署中… ${skillIds.length} 个 skill → ${targetRoot}\\${skillDir}`);
        try{
          const res = await adminFetch("/api/deploy", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({targetRoot, skillDir, skillIds})});
          const ok = res.deployed||[], over=res.overwritten||[], err=res.errors||[];
          flash(el("deployHint"), `完成：新增 ${ok.length}，覆盖 ${over.length}` + (err.length?`，失败 ${err.length}`:""));
        }catch(e){
          flash(el("deployHint"),"部署失败："+e.message);
        }
      });
      // browse modal
      async function browseLoad(path){
        const input=el("browsePathInput"), list=el("browseList");
        if(input) input.value=path||"";
        if(list) list.innerHTML='<div style="padding:12px;color:var(--muted)">加载中…</div>';
        try{
          const qs=path?`?path=${encodeURIComponent(path)}`:"";
          const res=await adminFetch("/api/browse"+qs);
          const cur=res.path||path||"";
          if(input) input.value=cur;
          if(!list) return;
          if(res.error) { list.innerHTML=`<div style="padding:12px;color:#b42318">${escapeHtml(res.error)}</div>`; return; }
          const dirs=res.dirs||[];
          if(!dirs.length) { list.innerHTML='<div style="padding:12px;color:var(--muted)">无子目录</div>'; return; }
          list.innerHTML=dirs.map(d=>`<button class="admin-chip" data-browse-path="${escapeHtml(d.path)}" style="text-align:left;justify-content:flex-start;overflow:hidden;text-overflow:ellipsis">📁 ${escapeHtml(d.name)}</button>`).join("");
          list.querySelectorAll("[data-browse-path]").forEach(b=>b.addEventListener("click", ()=>browseLoad(b.dataset.browsePath)));
        }catch(e){
          if(list) list.innerHTML=`<div style="padding:12px;color:#b42318">${escapeHtml(e.message)}</div>`;
        }
      }
      el("browseBtn")?.addEventListener("click", ()=>{ el("browseModal")?.classList.add("open"); const cur=el("deployRoot")?.value.trim()||""; browseLoad(cur); });
      el("browseCancelBtn")?.addEventListener("click", ()=>el("browseModal")?.classList.remove("open"));
      el("browseModal")?.addEventListener("click", e=>{ if(e.target===el("browseModal")) el("browseModal").classList.remove("open"); });
      el("browseUpBtn")?.addEventListener("click", async ()=>{
        const cur=el("browsePathInput")?.value.trim();
        if(!cur) return browseLoad("");
        try{ const res=await adminFetch("/api/browse?path="+encodeURIComponent(cur)); if(res.parent) browseLoad(res.parent); else browseLoad(""); }catch(_){}
      });
      el("browseSelectBtn")?.addEventListener("click", ()=>{
        const cur=el("browsePathInput")?.value.trim();
        if(!cur) return;
        el("deployRoot").value=cur;
        deployState.targetRoot=cur; localStorage.setItem("skill-hub-deploy-root", cur);
        el("browseModal")?.classList.remove("open");
        flash(el("deployHint"),`已选目录：${cur}`);
      });
      el("browsePathInput")?.addEventListener("keydown", e=>{ if(e.key==="Enter") browseLoad(e.target.value.trim()); });
      // init mode UI
      document.querySelectorAll("#modeSwitch .segment").forEach(b=>{ b.classList.toggle("active", b.dataset.mode===adminState.mode); b.setAttribute("aria-selected", b.dataset.mode===adminState.mode); });
    }
    // hide admin UI when not admin
    if(!isAdmin){
      el("adminBar")?.classList.remove("open");
      el("bottomDockOrganize")?.classList.remove("open");
      el("bottomDockDeploy")?.classList.remove("open");
    }
    applyLanguage();
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
