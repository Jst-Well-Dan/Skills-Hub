from __future__ import annotations

import json
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

from content_sources import load_reviews, reviews_by_skill, translation_file
from skillhub_common import ROOT, load_category_labels, load_registry, parse_frontmatter

# 单语分类：由 registry/categories.yaml 驱动，动态加载
CATEGORY_LABELS = load_category_labels()


SITE_DIR = ROOT / "site"
ASSETS_DIR = SITE_DIR / "assets"
REPO_URL = "https://github.com/Jst-Well-Dan/Skills-Hub"
# 英文标签仅作兼容保留，新建分类自动复用中文名
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
}
# 为动态新增分类补齐 EN（复用中文名）
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
    *{box-sizing:border-box}body{margin:0;min-width:320px;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.55}
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
    .layout{max-width:1240px;margin:0 auto;padding:28px 24px 48px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:28px}
    .sidebar{align-self:start;position:sticky;top:72px}
    .filter-panel{border:1px solid var(--line);background:var(--cream)}
    .filter-head{padding:11px 14px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}
    .filter-title{margin:0;font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--ink)}
    .filter-list{display:grid}
    .facet{width:100%;min-height:38px;padding:9px 12px;border:0;border-bottom:1px solid var(--grid);background:var(--cream);display:flex;justify-content:space-between;gap:8px;align-items:center;text-align:left;cursor:pointer;color:var(--ink);font-size:13px}
    .facet:hover{background:var(--paper)}
    .facet.active{background:var(--ink);color:white}
    .facet.active .count{background:rgba(255,255,255,.15);color:white;border-color:rgba(255,255,255,.2)}
    .count{min-width:22px;padding:2px 6px;border-radius:999px;border:1px solid var(--line);background:var(--paper);color:var(--muted);font-family:var(--mono);font-size:11px;text-align:center}
    .workspace{min-width:0;display:grid;gap:16px}
    .catalog-intro{position:relative;overflow:hidden;background:var(--paper);border:1px solid var(--line);padding:20px 18px 16px}
    .catalog-intro::before{content:"";position:absolute;inset:-40px;opacity:.10;background:repeating-radial-gradient(ellipse 900px 600px at 18% 30%, transparent 0 18px, var(--moss) 19px 19px),repeating-radial-gradient(ellipse 700px 500px at 72% 70%, transparent 0 14px, var(--orange) 15px 15px)}
    .catalog-intro::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg, transparent 40%, var(--paper) 92%);pointer-events:none}
    .catalog-intro>*{position:relative;z-index:1}
    .catalog-title{margin:0;font-family:var(--display);font-size:30px;line-height:1.1;letter-spacing:-.03em;color:var(--ink)}
    .catalog-title i{font-style:italic;color:var(--orange)}
    .catalog-copy{margin:8px 0 0;max-width:65ch;color:var(--muted);font-size:13px;line-height:1.6}
    .toolbar{padding:10px 0 12px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
    .toolbar-actions{display:flex;align-items:center;gap:8px}
    .segmented{display:inline-grid;grid-auto-flow:column;gap:3px;padding:3px;background:var(--line);border-radius:9px}
    .segment{min-width:52px;height:30px;padding:0 12px;border:0;border-radius:7px;background:transparent;color:var(--muted);cursor:pointer;font-family:var(--mono);font-size:11px}
    .segment.active{background:var(--cream);color:var(--ink);font-weight:700;box-shadow:0 1px 3px rgba(15,26,20,.12)}
    .sort-select{height:36px;border:1px solid var(--line);background:var(--cream);color:var(--ink);padding:0 10px;font-family:var(--mono);font-size:12px}
    .result-meta{color:var(--ink);font-family:var(--mono);font-size:12px;letter-spacing:.06em}
    .project-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
    .project-list{display:grid;grid-template-columns:1fr;gap:10px}
    .project-card{position:relative;border:1px solid var(--line);background:var(--cream);overflow:hidden;transition:transform .16s var(--ease), box-shadow .16s var(--ease)}
    .project-card:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(15,26,20,.08)}
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
    .github-link{color:var(--ink);border-bottom:1px solid var(--ink);padding-bottom:1px;font-weight:600;white-space:nowrap}
    .gh-icon{width:32px;height:32px;border:1px solid var(--line);background:var(--cream);display:grid;place-items:center;color:var(--ink);flex:0 0 auto;transition:border-color .15s var(--ease), background .15s var(--ease), color .15s var(--ease)}
    .gh-icon:hover{border-color:var(--ink);background:var(--paper);color:var(--orange)}
    .gh-icon:active{background:var(--grid)}
    .gh-icon:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
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
    /* Admin — product register: restrained, one sans, state-rich, tokens only */
    .admin-bar{display:none;position:sticky;top:56px;z-index:29;background:var(--ink);color:var(--paper);border-bottom:1px solid var(--ink);padding:10px 24px;gap:10px;align-items:center;flex-wrap:wrap}
    .admin-bar.open{display:flex}
    .admin-bar strong{color:var(--paper);font-family:var(--mono);font-size:11px;letter-spacing:.08em;font-weight:600}
    .admin-hint{color:rgba(244,239,230,.72);font-family:var(--mono);font-size:11px;line-height:1.4}
    .admin-chip{min-height:36px;padding:0 12px;border:1px solid var(--line);background:var(--cream);color:var(--ink);font-family:var(--mono);font-size:12px;cursor:pointer;transition:border-color .15s var(--ease), background .15s var(--ease), color .15s var(--ease)}
    .admin-bar .admin-chip{background:transparent;border-color:rgba(244,239,230,.22);color:var(--paper)}
    .admin-bar .admin-chip option{color:var(--ink);background:var(--cream)}
    .admin-bar select.admin-chip{padding-right:28px}
    .admin-bar .admin-chip:hover{border-color:var(--paper);background:rgba(244,239,230,.08)}
    .admin-bar .admin-chip:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
    .admin-bar .admin-chip:active{background:rgba(244,239,230,.14)}
    .admin-chip:hover{border-color:var(--ink);background:var(--paper)}
    .admin-chip:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
    .admin-chip:active{background:var(--grid)}
    .admin-chip:disabled{opacity:.45;cursor:not-allowed}
    .admin-chip.primary{background:var(--orange);color:white;border-color:var(--orange)}
    .admin-chip.primary:hover{background:#C45A2A;border-color:#C45A2A}
    .admin-bar .admin-chip.primary{background:var(--orange);border-color:var(--orange);color:white}
    .admin-bar .admin-chip.primary:hover{background:#C45A2A;border-color:#C45A2A}
    .admin-deploy{display:none;position:sticky;top:98px;z-index:28;background:var(--grid);border-bottom:1px solid var(--line);padding:10px 24px;gap:10px;align-items:center;flex-wrap:wrap}
    .admin-deploy.open{display:flex}
    .admin-deploy strong{color:var(--ink);font-family:var(--mono);font-size:11px;letter-spacing:.06em}
    .admin-deploy input[type="text"]{height:36px;border:1px solid var(--line);background:var(--cream);color:var(--ink);padding:0 10px;min-width:240px;flex:1;font-family:var(--mono);font-size:12px}
    .admin-deploy input[type="text"]:focus{border-color:var(--ink);outline:2px solid rgba(216,108,58,.18);outline-offset:0}
    .admin-deploy select{height:36px;border:1px solid var(--line);background:var(--cream);color:var(--ink);padding:0 8px;font-family:var(--mono);font-size:12px}
    .admin-deploy .deploy-log{font-family:var(--mono);font-size:11px;color:var(--muted);max-height:32px;overflow:auto}
    /* facet admin */
    .facet.drag-over{background:rgba(216,108,58,.08);outline:2px dashed var(--orange);outline-offset:-2px}
    .facet-row{display:contents}
    .admin-mode .facet-row{display:flex;align-items:center;gap:0;border-bottom:1px solid var(--grid)}
    .admin-mode .facet-row .facet{flex:1;border-bottom:0}
    .facet-actions{display:none;gap:6px;align-items:center;padding:4px 6px 4px 0}
    .admin-mode .facet-actions{display:inline-flex}
    .facet-actions button{min-height:32px;padding:0 10px;border:1px solid var(--ink);background:var(--paper);color:var(--ink);font-family:var(--mono);font-size:11px;font-weight:600;cursor:pointer;white-space:nowrap}
    .facet-actions button:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}
    .facet-actions button[data-act="delete"]{border-color:var(--orange);color:var(--orange)}
    .facet-actions button[data-act="delete"]:hover{background:var(--orange);color:white;border-color:var(--orange)}
    .facet-actions button:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
    @media(max-width:980px){.admin-mode .facet-row{flex:0 0 auto;border-bottom:0;border-right:1px solid var(--grid)}.admin-mode .facet-row .facet{white-space:nowrap}}
    /* card admin */
    .project-card.admin-selectable{position:relative;padding-left:0}
    .project-card.admin-selectable .project-main{padding-left:44px}
    .project-card.selected{outline:2px solid var(--ink);outline-offset:-2px;background:var(--cream)}
    .project-card.selected .project-main{background:rgba(216,108,58,.04)}
    .project-card.dragging{opacity:.55;transform:rotate(.6deg);box-shadow:0 12px 24px rgba(15,26,20,.18)}
    .admin-check-wrap{position:absolute;top:0;left:0;width:44px;height:44px;display:grid;place-items:center;z-index:5;cursor:pointer}
    .admin-checkbox{width:20px;height:20px;accent-color:var(--ink);cursor:pointer;margin:0}
    .admin-checkbox:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
    .project-card.admin-selectable .stamp{right:10px;left:auto}
    /* modal — product */
    .admin-modal{position:fixed;inset:0;z-index:50;display:none;place-items:center;background:rgba(15,26,20,.38);padding:16px}
    .admin-modal.open{display:grid}
    .admin-modal-box{width:min(440px,92vw);background:var(--cream);border:1px solid var(--ink);padding:20px;display:grid;gap:14px}
    .admin-modal-box h3{margin:0;font-family:var(--sans);font-size:16px;font-weight:700;color:var(--ink)}
    .admin-modal-box input{height:40px;border:1px solid var(--line);background:var(--paper);padding:0 12px;color:var(--ink);font-family:var(--sans);font-size:13px}
    .admin-modal-box input:focus{border-color:var(--ink);outline:2px solid rgba(216,108,58,.18);outline-offset:0}
    .admin-fab{position:fixed;right:20px;bottom:20px;z-index:45;min-height:44px;padding:0 16px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);font-family:var(--mono);font-size:12px;letter-spacing:.04em;display:inline-flex;align-items:center;gap:8px;cursor:pointer;box-shadow:0 8px 20px rgba(15,26,20,.18)}
    .admin-fab:hover{background:#1a2b22}
    .fab-count{min-width:20px;height:20px;padding:0 6px;border-radius:999px;background:var(--orange);color:white;display:grid;place-items:center;font-size:11px}
    .admin-workbench{position:fixed;top:0;right:0;bottom:0;width:min(380px,92vw);z-index:46;background:var(--cream);border-left:1px solid var(--ink);transform:translateX(100%);transition:transform .24s var(--ease);display:grid;grid-template-rows:auto 1fr;box-shadow:-12px 0 32px rgba(15,26,20,.12)}
    .admin-workbench.open{transform:translateX(0)}
    .admin-workbench-head{padding:14px 16px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;background:var(--paper)}
    .admin-workbench-body{overflow:auto;padding:16px;display:grid;gap:18px;align-content:start}
    .wb-section{border:1px solid var(--line);background:var(--paper);padding:14px;display:grid;gap:10px}
    .wb-title{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:var(--ink);display:flex;justify-content:space-between;align-items:center}
    .wb-hint{color:var(--muted);font-size:10px;letter-spacing:0}
    .wb-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
    .wb-row .admin-chip{flex:0 0 auto}
    .wb-row input[type="text"]{flex:1;min-width:160px;height:36px;border:1px solid var(--line);background:var(--cream);padding:0 10px;font-family:var(--mono);font-size:12px}
    .admin-workbench-backdrop{position:fixed;inset:0;z-index:44;background:rgba(15,26,20,.08);opacity:0;pointer-events:none;transition:opacity .2s}
    .admin-workbench-backdrop.open{opacity:1;pointer-events:none}
    .admin-modal-actions{display:flex;gap:8px;justify-content:flex-end}
    @media(max-width:980px){.topbar-inner{grid-template-columns:1fr auto}.search-box{grid-column:1 / -1;order:3}.layout{display:flex;flex-direction:column;gap:18px}.workspace{display:contents}.catalog-intro{order:1}.sidebar{order:2;position:static}.filter-panel{display:flex;align-items:center;gap:10px}.filter-head{padding:0;flex:0 0 auto;border:0}.filter-list{display:flex;flex:1;min-width:0;gap:6px;overflow:auto;padding-bottom:4px}.facet{flex:0 0 auto;white-space:nowrap}.toolbar{order:3}.project-grid,.project-list{order:4;grid-template-columns:1fr}}
    @media(max-width:680px){.topbar-inner,.layout{padding-left:14px;padding-right:14px}.catalog-title{font-size:26px}}
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
  <button id="adminWorkbenchToggle" class="admin-fab" aria-label="打开工作台" style="display:none">工作台 <span id="fabCount" class="fab-count">0</span></button>
  <div class="admin-workbench" id="adminWorkbench" aria-hidden="true">
    <div class="admin-workbench-head">
      <div style="display:flex;align-items:center;gap:8px"><strong>工作台</strong><span class="admin-hint" id="adminHint">拖拽到分类或勾选后批量移动</span></div>
      <button class="icon-button" id="adminWorkbenchClose" aria-label="关闭工作台">×</button>
    </div>
    <div class="admin-workbench-body">
      <section class="wb-section" aria-label="移动">
        <div class="wb-title">移动 <span class="wb-hint">勾选后批量操作</span></div>
        <div class="wb-row"><select class="admin-chip" id="adminBatchTarget" aria-label="目标分类"></select><button class="admin-chip primary" id="adminBatchMove">批量移动</button></div>
        <div class="wb-row"><button class="admin-chip" id="adminNewCategory">新建分类</button><button class="admin-chip" id="adminRegenerate">重新生成</button></div>
        <span class="admin-hint" id="adminStatus" role="status" aria-live="polite"></span>
      </section>
      <section class="wb-section" aria-label="部署">
        <div class="wb-title">部署 <span class="wb-hint">覆盖同名</span></div>
        <div class="wb-row"><input type="text" id="deployTargetRoot" placeholder="目标项目路径，如 E:\Code\my-app" /><button class="admin-chip" id="deployBrowseBtn" title="浏览本地目录">浏览</button></div>
        <div class="wb-row"><select id="deploySkillDir" title="skill 存放子目录"><option value=".claude">.claude</option><option value=".codex">.codex</option><option value=".agents">.agents</option><option value=".pi">.pi</option><option value="custom">自定义…</option></select><input type="text" id="deployCustomDir" placeholder="自定义目录" style="display:none;min-width:120px" /></div>
        <button class="admin-chip primary" id="deployBtn">部署选中</button>
        <span class="admin-hint" id="deployHint">勾选项目或 skill 后部署</span><span id="deployStatus" class="deploy-log"></span>
      </section>
    </div>
  </div>
  <div class="admin-workbench-backdrop" id="adminWorkbenchBackdrop" aria-hidden="true"></div>

  <main class="layout">
    <aside class="sidebar" id="sidebar" aria-label="分类筛选">
      <section class="filter-panel">
        <div class="filter-head"><h2 class="filter-title" id="filterTitle">分类</h2></div>
        <div class="filter-list" id="categoryFilters"></div>
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
    const CAT_ABBREV = {"coding-tools":"COD","daily-tools":"DLY","personal-collection":"PER","frontend-presentation":"FED","animation-motion":"ANI","content-creation":"CNT","document-data":"DOC","research-learning":"RES","automation-workflow":"AUT","uncategorized":"UNC","video-image":"IMG"};
    function distinctiveTags(tags){const f=(tags||[]).filter(t=>t!=="coding"&&t!=="docs");if(f.length>0) return f.slice(0,3);return (tags||[]).slice(0,2)}
    function catAbbrev(id){return CAT_ABBREV[id]||id.slice(0,3).toUpperCase()}
    const state={query:"",category:"all",sort:"name",view:"grid",selected:null,language:"zh"};
    const data=window.SKILL_HUB_DATA;
    const copy={zh:{brandMeta:"CATALOG · "+data.summary.project_count+" PROJECTS",search:"搜索项目或 skill",clear:"清空搜索",docs:"完整索引",github:"项目 GitHub",filter:"分类",all:"全部",title:"Agent Skills 目录",intro:""+data.summary.project_count+" 个项目 · "+data.summary.skill_count+" 个 Skills，支持按分类、关键词及来源筛选。",grid:"网格",list:"列表",sortName:"按名称",sortSkills:"按 skill 数",sortUpdated:"按检查日期",noDescription:"暂无简介",openGithub:"打开 GitHub",viewDirectory:"查看目录",empty:"没有匹配的 skill 库",projectDirectory:"查看项目目录",installHelp:"查看源仓库安装说明",category:"分类",install:"安装",viewContent:"查看内容",collapseContent:"收起内容",loading:"加载中…",loadFailed:"加载失败，请重试",reviews:"相关点评",projects:"个项目"},en:{brandMeta:"CATALOG · "+data.summary.project_count+" PROJECTS",search:"Search projects or skills",clear:"Clear search",docs:"Full index",github:"Project GitHub",filter:"Category",all:"All",title:"Agent Skills Catalog",intro:""+data.summary.project_count+" projects · "+data.summary.skill_count+" skills. Filter by category, keyword and source.",grid:"Grid",list:"List",sortName:"By name",sortSkills:"By skill count",sortUpdated:"By check date",noDescription:"No description",openGithub:"Open GitHub",viewDirectory:"View directory",empty:"No matching skill libraries",projectDirectory:"View project directory",installHelp:"View installation instructions in the source repository",category:"Category",install:"Install",viewContent:"View content",collapseContent:"Collapse content",loading:"Loading…",loadFailed:"Failed to load. Try again.",reviews:"Related reviews",projects:"projects"}};
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
    function renderCategories(){const visible=[{id:"all",count:data.summary.project_count},...data.facets.categories.filter(c=>c.count>0)];const buttons=visible.map(item=>`
          <div class="facet-row" data-row="${escapeHtml(item.id)}"><button class="facet ${state.category===item.id?"active":""}" data-category="${escapeHtml(item.id)}">
            <span>${escapeHtml(item.id==="all"?t("all"):categoryLabel(item.id))}</span>
            <span class="count">${item.count}</span>
          </button></div>
        `).join("");el("categoryFilters").innerHTML=buttons}
    const GH_SVG='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>';
    const FOLDER_SVG='<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M2 2.5A1.5 1.5 0 013.5 1h3.38a1 1 0 01.89.55L8.62 3.5H12.5A1.5 1.5 0 0114 5v7a1.5 1.5 0 01-1.5 1.5H3.5A1.5 1.5 0 012 12V2.5zm.5.5V12a.5.5 0 00.5.5h9a.5.5 0 00.5-.5V5a.5.5 0 00-.5-.5H8.62a1 1 0 01-.89-.55L6.88 2H3.5a.5.5 0 00-.5.5z"/></svg>';
    function projectCard(project){const isGh=!!project.source?.repo;const ghUrl=escapeHtml(sourceUrl(project));const ghLabel=isGh?`上游仓库 ${project.source.repo}`:`本地目录 ${project.path}`;const ghIcon=isGh?GH_SVG:FOLDER_SVG;const dt=distinctiveTags(project.tags||[]);const tagsHtml=dt.length?`<div class="card-tags">${dt.map(tag=>`<span>#${escapeHtml(tag)}</span>`).join("")}</div>`:`<span style="color:var(--muted);font-family:var(--mono);font-size:11px">— 无区分标签</span>`;return `
        <article class="project-card">
          <button class="project-main" data-project-id="${escapeHtml(project.id)}">
            <div class="eyebrow">${escapeHtml(categoryLabel(project.category))} · ${project.skill_count||0} skills</div>
            <div class="project-row">
              <h3 class="project-name">${escapeHtml(project.name)}</h3>
              <span class="badge">${project.skill_count||0} skills</span>
            </div>
            <p class="description">${escapeHtml(descriptionOf(project)||t("noDescription"))}</p>
          </button>
          <div class="project-foot">
            ${tagsHtml}
            <a class="gh-icon" href="${ghUrl}" target="_blank" rel="noreferrer" aria-label="${escapeHtml(ghLabel)}" title="${escapeHtml(ghLabel)}">${ghIcon}</a>
          </div>
        </article>
      `}
    function renderProjects(projects){const grid=el("projectGrid");grid.className=state.view==="list"?"project-list":"project-grid";if(!projects.length){grid.innerHTML=`<div class="empty">${t("empty")}</div>`;return}grid.innerHTML=projects.map(projectCard).join("")}
    function renderDrawer(project){if(!project) return;state.selected=project.id;el("drawerTitle").textContent=project.name;el("drawerDescription").textContent=readableText(descriptionOf(project)||t("noDescription"));const dsl=el("drawerSourceLink");dsl.href=sourceUrl(project);const isGh=!!project.source?.repo;const dslLabel=isGh?`上游仓库 ${project.source.repo}`:`本地目录 ${project.path}`;dsl.setAttribute("aria-label",dslLabel);dsl.title=dslLabel;const install=project.install?.method==="npx"&&project.install.command?`<code>${escapeHtml(project.install.command)}</code>`:`<a href="${escapeHtml(sourceUrl(project))}" target="_blank" rel="noreferrer">${t("installHelp")}</a>`;const skills=[...(project.skills||[])].sort((a,b)=>a.name.localeCompare(b.name));function skillGhUrl(skill){if(project.source?.repo){let rel=skill.path||"";const prefix=`libraries/${project.id}/`;if(rel.startsWith(prefix)) rel=rel.slice(prefix.length);else if(rel.startsWith("libraries/")) rel=rel.split("/").slice(2).join("/");return `https://github.com/${project.source.repo}/tree/main/${rel}`;}return `${REPO_URL}/tree/main/${skill.path||project.path}`;}const skillHtml=skills.map((skill,index)=>{const sIsGh=!!project.source?.repo;const sUrl=escapeHtml(skillGhUrl(skill));const sLabel=sIsGh?`原 Skill 源码 ${project.source.repo}`:`本地 Skill ${skill.name}`;const sIcon=sIsGh?GH_SVG:FOLDER_SVG;return `
        <article class="skill-item">
          <div style="display:flex;justify-content:space-between;gap:12px;align-items:start"><div style="min-width:0"><div class="skill-name">${escapeHtml(skill.name)}</div><p class="skill-description">${escapeHtml(descriptionOf(skill)||t("noDescription"))}</p></div><a class="gh-icon small" href="${sUrl}" target="_blank" rel="noreferrer" aria-label="${escapeHtml(sLabel)}" title="${escapeHtml(sLabel)}">${sIcon}</a></div>
          <div class="links"><button class="text-link" data-skill-path="${escapeHtml(skill.path)}" data-panel-id="skill-panel-${index}" aria-expanded="false">${t("viewContent")}</button></div>
          <section class="skill-panel" id="skill-panel-${index}" aria-live="polite" hidden></section>
        </article>
      `}).join("");el("drawerBody").innerHTML=`<div class="detail-grid"><div class="detail"><div class="detail-label">${t("category")}</div><div class="detail-value">${escapeHtml(categoryLabel(project.category))}</div></div><div class="detail"><div class="detail-label">${t("install")}</div><div class="detail-value">${install}</div></div></div><h3 class="section-title">Skills · ${skills.length}</h3><div class="skill-list">${skillHtml}</div>`;el("drawer").classList.add("open");el("drawer").setAttribute("aria-hidden","false")}
    function setContentLanguage(panel){const record=panel.skillRecord;const content=panel.querySelector(".skill-content");content.textContent=text(record.original);content.dataset.language="original"}
    function renderSkillPanel(panel,record){panel.skillRecord=record;const reviews=(record.reviews||[]).length?`<section class="related-reviews"><h4 class="review-title">${t("reviews")}</h4>${record.reviews.map(r=>`<a class="review-link" href="${REPO_URL}/blob/main/docs/reviews/${encodeURIComponent(r.slug)}.md" target="_blank" rel="noreferrer"><span>${escapeHtml(r.title)}</span><span class="review-meta">${escapeHtml(r.type_label)} →</span></a>`).join("")}</section>`:"";panel.innerHTML=`<pre class="skill-content"></pre>${reviews}`;setContentLanguage(panel)}
    function closeDrawer(){el("drawer").classList.remove("open");el("drawer").setAttribute("aria-hidden","true");state.selected=null}
    function render(){const projects=sortProjects(data.projects.filter(matches));renderCategories();renderProjects(projects);el("resultMeta").textContent=state.query||state.category!=="all"?`${projects.length} / ${data.summary.project_count} ${t("projects")}`:`${data.summary.project_count} ${t("projects")} · ${data.summary.skill_count} skills`;document.querySelectorAll(".segment").forEach(b=>b.classList.toggle("active",b.dataset.view===state.view))}
    function applyLanguage(){document.documentElement.lang="zh-CN";document.title="Skills-Hub - Agent Skills 目录";el("brandMeta").textContent=t("brandMeta");el("searchInput").placeholder=t("search");el("clearSearch").title=el("clearSearch").ariaLabel=t("clear");el("docsLink")?.textContent && (el("docsLink").textContent=t("docs"));const _gl=el("githubLink"); if(_gl){ if(!_gl.querySelector("svg")) _gl.textContent=t("github"); else { _gl.setAttribute("aria-label","Skills-Hub 本体仓库"); _gl.title="Skills-Hub 本体仓库（GitHub）"; } }el("filterTitle").textContent=t("filter");el("catalogTitle").innerHTML=t("title");el("catalogCopy").textContent=t("intro");el("gridView").textContent=t("grid");el("listView").textContent=t("list");el("sortName").textContent=t("sortName");el("sortSkills").textContent=t("sortSkills");el("sortUpdated").textContent=t("sortUpdated");render();if(state.selected){renderDrawer(data.projects.find(p=>p.id===state.selected))}}
    document.addEventListener("click", async (event)=>{
      const skillButton=event.target.closest("[data-skill-path]");
      if(skillButton){
        const panel=el(skillButton.dataset.panelId);
        if(!panel.hidden){panel.hidden=true;skillButton.textContent=t("viewContent");skillButton.setAttribute("aria-expanded","false");return}
        skillButton.textContent=t("loading");skillButton.disabled=true;
        try{const docs=await loadSkillContent();const record=docs[skillButton.dataset.skillPath];if(!record) throw new Error("missing");renderSkillPanel(panel,record);panel.hidden=false;skillButton.textContent=t("collapseContent");skillButton.setAttribute("aria-expanded","true")}catch{skillButton.textContent=t("loadFailed")}finally{skillButton.disabled=false}
        return;
      }
      const category=event.target.closest("[data-category]");
      if(category){state.category=category.dataset.category;render();return}
      const projectButton=event.target.closest("[data-project-id]");
      if(projectButton){renderDrawer(data.projects.find(p=>p.id===projectButton.dataset.projectId))}
    });
    el("searchInput").addEventListener("input",e=>{state.query=e.target.value;render()});
    el("clearSearch").addEventListener("click",()=>{state.query="";el("searchInput").value="";render()});
    el("sortSelect").addEventListener("change",e=>{state.sort=e.target.value;render()});
    document.querySelectorAll(".segment").forEach(b=>b.addEventListener("click",()=>{state.view=b.dataset.view;render()}));
    el("closeDrawer").addEventListener("click",closeDrawer);
    el("drawerBackdrop").addEventListener("click",closeDrawer);
    document.addEventListener("keydown",e=>{if(e.key==="Escape"){closeDrawer();const m=el("adminModal");if(m) m.classList.remove("open")}});
    const ADMIN_API="http://127.0.0.1:5173";
    const isAdmin=new URLSearchParams(location.search).has("admin")||localStorage.getItem("skill-hub-admin")==="1";
    const adminState={selected:new Set(),dragging:null};
    function adminSetStatus(msg,isError){const s=el("adminStatus");if(s){s.textContent=msg;s.style.color=isError?"#b42318":"#8A6D00"}}
    async function adminFetch(path,opts){try{const r=await fetch(ADMIN_API+path,opts);const j=await r.json();if(!r.ok) throw new Error(j.error||r.statusText);return j}catch(e){throw e}}
    function adminSlug(v){return String(v||"").trim().toLowerCase().replace(/[^a-z0-9\u4e00-\u9fff]+/g,"-").replace(/^-|-$/g,"")||""}
    function adminRefreshBatchTargets(){const sel=el("adminBatchTarget");if(!sel) return;sel.innerHTML=Object.entries(data.category_labels).map(([id,label])=>`<option value="${escapeHtml(id)}">${escapeHtml(label)} (${escapeHtml(id)})</option>`).join("")}
    const _origRenderCategories=renderCategories;
    renderCategories=function(){_origRenderCategories();if(!isAdmin) return;document.body.classList.add("admin-mode");adminRefreshBatchTargets();document.querySelectorAll("[data-row]").forEach(row=>{const cid=row.dataset.row;if(cid==="all") return;const btn=row.querySelector("[data-category]");if(!btn) return;btn.addEventListener("dragover",e=>{e.preventDefault();row.classList.add("drag-over")});btn.addEventListener("dragleave",()=>row.classList.remove("drag-over"));row.addEventListener("dragover",e=>{e.preventDefault();row.classList.add("drag-over")});row.addEventListener("dragleave",()=>row.classList.remove("drag-over"));row.addEventListener("drop",async e=>{e.preventDefault();row.classList.remove("drag-over");const ids=adminState.dragging?[adminState.dragging]:[...adminState.selected];if(!ids.length) return;adminSetStatus("移动中…");try{try{await adminFetch("/api/projects/move",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({ids,category:cid})})}catch(_){}ids.forEach(id=>{const p=data.projects.find(x=>x.id===id);if(p){p.category=cid;p.category_locked=true}});const counts={};data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});data.facets.categories=Object.entries(data.category_labels).map(([id,label])=>({id,label,count:counts[id]||0}));adminState.selected.clear();render();adminSetStatus(`已移动 ${ids.length} 个项目到 ${data.category_labels[cid]||cid}`)}catch(err){adminSetStatus("移动失败: "+err.message,true)}});if(!row.querySelector(".facet-actions")){const acts=document.createElement("span");acts.className="facet-actions";acts.innerHTML=`<button title="重命名分类" aria-label="重命名 ${escapeHtml(data.category_labels[cid]||cid)}" data-act="rename" data-id="${escapeHtml(cid)}">重命名</button><button title="删除分类" aria-label="删除 ${escapeHtml(data.category_labels[cid]||cid)}" data-act="delete" data-id="${escapeHtml(cid)}">删除</button>`;row.appendChild(acts);acts.querySelectorAll("button").forEach(b=>b.addEventListener("click",async e=>{e.stopPropagation();const act=b.dataset.act,id=b.dataset.id;if(act==="delete"){if(!confirm(`删除分类「${data.category_labels[id]||id}」？旗下项目将移入“未分类”。`)) return;adminSetStatus("删除中…");try{try{await adminFetch("/api/categories",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({action:"delete",id})})}catch(_){}const moved=data.projects.filter(p=>p.category===id);moved.forEach(p=>{p.category="uncategorized";p.category_locked=true});delete data.category_labels[id];delete data.category_labels_en[id];if(!data.category_labels["uncategorized"]){data.category_labels["uncategorized"]="未分类";data.category_labels_en["uncategorized"]="Uncategorized"}const counts={};data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});data.facets.categories=Object.entries(data.category_labels).map(([i,l])=>({id:i,label:l,count:counts[i]||0}));render();adminSetStatus(`已删除分类，已移动 ${moved.length} 个项目`)}catch(err){adminSetStatus(err.message,true)}} else if(act==="rename"){adminOpenModal("rename",id)}}))}})};
    const _origProjectCard=projectCard;
    projectCard=function(project){const html=_origProjectCard(project);if(!isAdmin) return html;const checked=adminState.selected.has(project.id)?"checked":"";return html.replace('<article class="project-card">',`<article class="project-card admin-selectable ${adminState.selected.has(project.id)?"selected":""}" draggable="true" data-drag-id="${escapeHtml(project.id)}">`).replace('</article>',`<label class="admin-check-wrap" aria-label="选择 ${escapeHtml(project.name)}"><input class="admin-checkbox" type="checkbox" data-check-id="${escapeHtml(project.id)}" ${checked} /></label></article>`)};
    function adminWireCardEvents(){if(!isAdmin) return;document.querySelectorAll("[data-drag-id]").forEach(card=>{card.addEventListener("dragstart",e=>{adminState.dragging=card.dataset.dragId;card.classList.add("dragging");e.dataTransfer.effectAllowed="move"});card.addEventListener("dragend",()=>{adminState.dragging=null;card.classList.remove("dragging")})});document.querySelectorAll(".admin-check-wrap").forEach(w=>{w.addEventListener("click",e=>e.stopPropagation());w.addEventListener("mousedown",e=>e.stopPropagation())});document.querySelectorAll("[data-check-id]").forEach(cb=>{cb.addEventListener("mousedown",e=>e.stopPropagation());cb.addEventListener("click",e=>{e.stopPropagation();const id=cb.dataset.checkId;if(cb.checked) adminState.selected.add(id);else adminState.selected.delete(id);cb.closest(".project-card")?.classList.toggle("selected",cb.checked);updateAdminFab();});cb.addEventListener("change",e=>{e.stopPropagation();const id=cb.dataset.checkId;if(cb.checked) adminState.selected.add(id);else adminState.selected.delete(id);cb.closest(".project-card")?.classList.toggle("selected",cb.checked);updateAdminFab();})})}
    const _origRenderProjects=renderProjects;
    renderProjects=function(projects){_origRenderProjects(projects);if(isAdmin) setTimeout(adminWireCardEvents,0)};
    const _origRender=render;
    render=function(){_origRender();if(isAdmin){const fab=el("adminWorkbenchToggle"); if(fab) fab.style.display="inline-flex"; updateAdminFab();}};
    function updateAdminFab(){const c=adminState.selected.size; const fc=el("fabCount"); if(fc) fc.textContent=c||"0"; const hint=el("adminHint"); if(hint) hint.textContent=c?`已选 ${c} 个，选目标后移动或部署`:"拖拽卡片到分类或勾选后批量移动";}
    function openWorkbench(){el("adminWorkbench")?.classList.add("open"); el("adminWorkbenchBackdrop")?.classList.add("open"); el("adminWorkbench")?.setAttribute("aria-hidden","false");}
    function closeWorkbench(){el("adminWorkbench")?.classList.remove("open"); el("adminWorkbenchBackdrop")?.classList.remove("open"); el("adminWorkbench")?.setAttribute("aria-hidden","true");}
    function adminOpenModal(mode,cid){const modal=el("adminModal"),title=el("adminModalTitle"),idInput=el("adminModalId"),labelInput=el("adminModalLabel"),hint=el("adminModalHint");hint.textContent="";if(mode==="rename"){title.textContent="重命名分类";idInput.value=cid;idInput.placeholder="新 ID（留空则不改 ID）";labelInput.value=data.category_labels[cid]||"";modal.dataset.mode="rename";modal.dataset.cid=cid}else{title.textContent="新建分类";idInput.value="";labelInput.value="";modal.dataset.mode="create";modal.dataset.cid=""}modal.classList.add("open");labelInput.focus()}
    if(isAdmin){
      el("adminNewCategory")?.addEventListener("click",()=>adminOpenModal("create"));
      el("adminBatchMove")?.addEventListener("click",async()=>{const ids=[...adminState.selected];const target=el("adminBatchTarget")?.value;if(!ids.length) return adminSetStatus("请先勾选项目",true);if(!target) return adminSetStatus("请选择目标分类",true);adminSetStatus("批量移动中…");try{try{await adminFetch("/api/projects/move",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({ids,category:target})})}catch(_){}ids.forEach(id=>{const p=data.projects.find(x=>x.id===id);if(p){p.category=target;p.category_locked=true}});const counts={};data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});data.facets.categories=Object.entries(data.category_labels).map(([id,label])=>({id,label,count:counts[id]||0}));adminState.selected.clear();render();adminSetStatus(`已移动 ${ids.length} 个项目到 ${data.category_labels[target]||target}`)}catch(e){adminSetStatus(e.message,true)}});
      el("adminRegenerate")?.addEventListener("click",async()=>{adminSetStatus("重新生成中…");try{await adminFetch("/api/regenerate",{method:"POST"});adminSetStatus("已重新生成 docs/site")}catch(e){adminSetStatus("后端未启动，仅本地预览已更新。运行 python scripts/admin_server.py 后可一键落盘生成。",true)}});
      el("adminModalCancel")?.addEventListener("click",()=>el("adminModal").classList.remove("open"));
      el("adminModal")?.addEventListener("click",e=>{if(e.target===el("adminModal")) el("adminModal").classList.remove("open")});
      el("adminModalOk")?.addEventListener("click",async()=>{const modal=el("adminModal"),mode=modal.dataset.mode,cid=modal.dataset.cid;const idRaw=el("adminModalId")?.value.trim(),labelRaw=el("adminModalLabel")?.value.trim();const hint=el("adminModalHint");if(mode==="create"){const nid=adminSlug(idRaw||labelRaw);if(!nid) return hint.textContent="请填写 ID 或名称";if(!labelRaw) return hint.textContent="请填写分类名称";if(data.category_labels[nid]) return hint.textContent="ID 已存在";try{try{await adminFetch("/api/categories",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({action:"create",id:nid,label:labelRaw})})}catch(_){}data.category_labels[nid]=labelRaw;data.category_labels_en[nid]=labelRaw;const counts={};data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});counts[nid]=counts[nid]||0;data.facets.categories=Object.entries(data.category_labels).map(([id,l])=>({id,label:l,count:counts[id]||0}));render();hint.textContent="";modal.classList.remove("open");adminSetStatus(`已新建分类 ${labelRaw} (${nid})`)}catch(e){hint.textContent=e.message}} else {const newIdRaw=el("adminModalId")?.value.trim();const newId=newIdRaw?adminSlug(newIdRaw):cid;const newLabel=labelRaw||data.category_labels[cid];if(!newLabel) return hint.textContent="请填写名称";if(newId!==cid&&data.category_labels[newId]) return hint.textContent="新 ID 已存在";try{try{await adminFetch("/api/categories",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({action:"update",id:cid,label:cid,new_id:newId,new_label:newLabel})})}catch(_){}if(newId!==cid){data.projects.filter(p=>p.category===cid).forEach(p=>{p.category=newId;p.category_locked=true});const oldLabel=data.category_labels[cid];delete data.category_labels[cid];delete data.category_labels_en[cid];data.category_labels[newId]=newLabel;data.category_labels_en[newId]=newLabel}else{data.category_labels[cid]=newLabel;data.category_labels_en[cid]=newLabel}const counts={};data.projects.forEach(p=>{counts[p.category]=(counts[p.category]||0)+1});data.facets.categories=Object.entries(data.category_labels).map(([id,l])=>({id,label:l,count:counts[id]||0}));render();modal.classList.remove("open");adminSetStatus(`已重命名分类`)}catch(e){hint.textContent=e.message}}});
      el("adminWorkbenchToggle")?.addEventListener("click", ()=>{ const wb=el("adminWorkbench"); if(wb?.classList.contains("open")) closeWorkbench(); else openWorkbench(); });
      el("adminWorkbenchClose")?.addEventListener("click", closeWorkbench);
      el("adminWorkbenchBackdrop")?.addEventListener("click", closeWorkbench);
      document.addEventListener("keydown", e=>{ if(e.key==="Escape") closeWorkbench(); });
    }
    // ===== Deploy: 本机任意路径 + 可配置 skill 目录，一键本地拷贝 =====
    const deployState = { skillSelected: new Set(), targetRoot: localStorage.getItem("skill-hub-deploy-root")||"", skillDir: localStorage.getItem("skill-hub-deploy-dir")||".claude" };
    function deploySetHint(msg,isError){ const h=el("deployHint"), s=el("deployStatus"); if(h) h.textContent=msg; if(s) s.textContent=""; if(isError && h) h.style.color="#b42318"; else if(h) h.style.color="#166534"; }
    function deployGetSkillDir(){ const sel=el("deploySkillDir")?.value; if(sel==="custom") return el("deployCustomDir")?.value.trim()||".claude"; return sel||".claude"; }
    if(isAdmin){
      const bar=el("adminDeployBar"); if(bar) bar.classList.add("open");
      const tr=el("deployTargetRoot"), sd=el("deploySkillDir"), cd=el("deployCustomDir");
      if(tr) tr.value=deployState.targetRoot;
      if(sd) { sd.value=[".claude",".codex",".agents",".pi"].includes(deployState.skillDir)?deployState.skillDir:"custom"; if(sd.value==="custom" && cd){ cd.style.display=""; cd.value=deployState.skillDir; } }
      tr?.addEventListener("input", ()=>{ deployState.targetRoot=tr.value.trim(); localStorage.setItem("skill-hub-deploy-root", deployState.targetRoot); });
      sd?.addEventListener("change", ()=>{ if(sd.value==="custom"){ cd.style.display=""; cd.focus(); } else { cd.style.display="none"; deployState.skillDir=sd.value; localStorage.setItem("skill-hub-deploy-dir", deployState.skillDir); } });
      cd?.addEventListener("input", ()=>{ deployState.skillDir=cd.value.trim()||".claude"; localStorage.setItem("skill-hub-deploy-dir", deployState.skillDir); });
      // 覆盖 renderDrawer：注入 skill 级复选框（project 级勾选 = 全选其下 skills）
      const _origRenderDrawer = renderDrawer;
      renderDrawer = function(project){
        _origRenderDrawer(project);
        if(!isAdmin || !project) return;
        // 为每个 skill 注入复选框
        const list = el("drawerBody")?.querySelector(".skill-list");
        if(!list) return;
        [...list.querySelectorAll(".skill-item")].forEach((item, idx)=>{
          const skill = [...(project.skills||[])].sort((a,b)=>a.name.localeCompare(b.name))[idx];
          if(!skill) return;
          const key = skill.path || skill.id;
          const cb=document.createElement("input"); cb.type="checkbox"; cb.className="admin-checkbox"; cb.style.position="static"; cb.style.marginRight="6px";
          cb.dataset.deploySkill=key; cb.checked=deployState.skillSelected.has(key);
          const nameEl=item.querySelector(".skill-name"); if(nameEl){ nameEl.prepend(cb); }
          cb.addEventListener("click", e=>{ e.stopPropagation(); if(cb.checked) deployState.skillSelected.add(key); else deployState.skillSelected.delete(key); deploySetHint(`已选 ${deployState.skillSelected.size} 个 skill（+ ${adminState.selected.size} 个 project）`); });
        });
        // 抽屉顶部增加“全选本 project”
        const title = el("drawerBody")?.querySelector(".section-title");
        if(title && !title.querySelector("[data-deploy-all]")){
          const btn=document.createElement("button"); btn.className="admin-chip"; btn.dataset.deployAll="1"; btn.textContent="全选本项目"; btn.style.marginLeft="8px";
          btn.addEventListener("click", ()=>{
            const all = [...(project.skills||[])].map(s=>s.path||s.id);
            const allSelected = all.every(k=>deployState.skillSelected.has(k));
            all.forEach(k=>{ if(allSelected) deployState.skillSelected.delete(k); else deployState.skillSelected.add(k); });
            list.querySelectorAll("[data-deploy-skill]").forEach(cb=>{ cb.checked=deployState.skillSelected.has(cb.dataset.deploySkill); });
            deploySetHint(`已选 ${deployState.skillSelected.size} 个 skill（+ ${adminState.selected.size} 个 project）`);
          });
          title.appendChild(btn);
        }
      };
      // 项目卡片勾选同步到 deploy 提示
      const _origAdminWire = adminWireCardEvents;
      adminWireCardEvents = function(){ _origAdminWire(); // 保留原有分类拖拽逻辑
        document.querySelectorAll("[data-check-id]").forEach(cb=>{
          cb.addEventListener("change", ()=>{ deploySetHint(`已选 ${deployState.skillSelected.size} 个 skill（+ ${adminState.selected.size} 个 project）`); });
        });
      };
      el("deployBtn")?.addEventListener("click", async ()=>{
        const targetRoot = el("deployTargetRoot")?.value.trim();
        if(!targetRoot) return deploySetHint("请先填写目标项目路径", true);
        localStorage.setItem("skill-hub-deploy-root", targetRoot);
        const skillDir = deployGetSkillDir();
        localStorage.setItem("skill-hub-deploy-dir", skillDir);
        // 收集：skill 级选中 + project 级勾选展开为其所有 skills
        const skillIds = [...deployState.skillSelected];
        const projectIds = [...adminState.selected];
        // project 展开
        for(const pid of projectIds){
          const proj=data.projects.find(p=>p.id===pid);
          if(proj){ for(const sk of proj.skills||[]) skillIds.push(sk.path||sk.id); }
        }
        if(!skillIds.length) return deploySetHint("请先勾选项目或 skill", true);
        deploySetHint(`部署中… ${skillIds.length} 个 skill → ${targetRoot}\\${skillDir}`);
        el("deployStatus").textContent="";
        try{
          const res = await adminFetch("/api/deploy", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({targetRoot, skillDir, skillIds})});
          const ok = res.deployed||[], over=res.overwritten||[], err=res.errors||[];
          el("deployStatus").textContent = `完成：新增 ${ok.length}，覆盖 ${over.length}` + (err.length?`，失败 ${err.length}`:"");
          if(err.length) console.warn(err);
          deploySetHint(`已部署到 ${res.destBase}（${skillDir}）`, err.length>0);
        }catch(e){
          deploySetHint("部署失败："+e.message+"（确认后端已启动 python scripts/admin_server.py）", true);
        }
      });
      // 初始化提示
      deploySetHint(`已选 ${deployState.skillSelected.size} 个 skill（+ ${adminState.selected.size} 个 project）`);
      // 浏览目录弹窗
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
      el("deployBrowseBtn")?.addEventListener("click", ()=>{ el("browseModal")?.classList.add("open"); const cur=el("deployTargetRoot")?.value.trim()||""; browseLoad(cur); });
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
        el("deployTargetRoot").value=cur;
        deployState.targetRoot=cur; localStorage.setItem("skill-hub-deploy-root", cur);
        el("browseModal")?.classList.remove("open");
        deploySetHint(`已选目录：${cur}`);
      });
      el("browsePathInput")?.addEventListener("keydown", e=>{ if(e.key==="Enter") browseLoad(e.target.value.trim()); });
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
