from __future__ import annotations

import base64
import configparser
import hashlib
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LIBRARIES_DIR = ROOT / "libraries"
EXTRACTED_SKILLS_DIR = ROOT / "extracted-skills"
REGISTRY_DIR = ROOT / "registry"
PROJECTS_FILE = REGISTRY_DIR / "projects.yaml"
TAGS_FILE = REGISTRY_DIR / "tags.yaml"
CATEGORIES_FILE = REGISTRY_DIR / "categories.yaml"
DOCS_DIR = ROOT / "docs"


DEFAULT_TAGS = [
    "browser",
    "image",
    "docs",
    "finance",
    "coding",
    "obsidian",
    "data",
    "workflow",
    "mcp",
    "cli",
    "frontend",
    "animation",
    "pdf",
    "automation",
    "research",
]

_DEFAULT_CATEGORY_LABELS = {
    "coding-tools": "编程工具类",
    "daily-tools": "日常工具类",
    "personal-collection": "个人合集类",
    "frontend-presentation": "前端展示类",
    "animation-motion": "动画动效类",
    "content-creation": "内容创作类",
    "document-data": "文档与数据类",
    "research-learning": "研究学习类",
    "automation-workflow": "自动化流程类",
    "uncategorized": "未分类",
}

def _load_category_labels() -> dict[str, str]:
    if CATEGORIES_FILE.exists():
        try:
            data = json.loads(CATEGORIES_FILE.read_text(encoding="utf-8"))
            # 支持两种格式：{id: label} 或 {categories: {id: label}} 或 {id: {label: ""}}
            if isinstance(data, dict) and "categories" in data and isinstance(data["categories"], dict):
                data = data["categories"]
            cleaned: dict[str, str] = {}
            for k, v in data.items():
                if isinstance(v, str):
                    cleaned[k] = v
                elif isinstance(v, dict):
                    cleaned[k] = v.get("label") or v.get("zh") or v.get("name") or k
            if cleaned:
                return cleaned
        except Exception:
            pass
    return dict(_DEFAULT_CATEGORY_LABELS)

CATEGORY_LABELS = _load_category_labels()

def load_category_labels() -> dict[str, str]:
    # 动态 reload 供 admin 使用
    return _load_category_labels()

def save_category_labels(labels: dict[str, str]) -> None:
    REGISTRY_DIR.mkdir(exist_ok=True)
    CATEGORIES_FILE.write_text(json.dumps(labels, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # 同步内存中的全局字典
    CATEGORY_LABELS.clear()
    CATEGORY_LABELS.update(labels)

CATEGORY_KEYWORDS = {
    "coding-tools": [
        "code",
        "coding",
        "api",
        "sdk",
        "react",
        "typescript",
        "python",
        "frontend",
        "mcp",
        "cli",
        "deploy",
        "vercel",
        "supabase",
        "browser",
        "testing",
        "gpt",
        "claude",
        "agent",
    ],
    "daily-tools": [
        "obsidian",
        "notebooklm",
        "notebook",
        "menu",
        "vault",
        "calendar",
        "日常",
        "笔记",
        "知识库",
    ],
    "content-creation": [
        "image",
        "photo",
        "comic",
        "cover",
        "wechat",
        "weibo",
        "xhs",
        "youtube",
        "article",
        "slides",
        "ppt",
        "speech",
        "script",
        "写作",
        "文章",
        "封面",
        "小红书",
        "公众号",
        "视频",
    ],
    "frontend-presentation": [
        "frontend-slides",
        "guizang-ppt-skill",
        "impeccable",
        "presentation",
        "slides",
        "slide",
        "ppt",
        "deck",
        "frontend-design",
        "interface",
        "ui",
        "ux",
        "design",
        "typography",
        "layout",
        "animation",
        "演示",
        "幻灯片",
        "前端展示",
        "界面",
        "设计",
    ],
    "animation-motion": [
        "animation",
        "motion",
        "lottie",
        "bodymovin",
        "gsap",
        "scrolltrigger",
        "timeline",
        "three.js",
        "threejs",
        "webgl",
        "3d map",
        "动效",
        "动画",
    ],
    "document-data": [
        "doc",
        "document",
        "markdown",
        "pdf",
        "pptx",
        "docx",
        "xlsx",
        "spreadsheet",
        "json",
        "table",
        "data",
        "mineru",
        "copyright",
        "文档",
        "数据",
    ],
    "research-learning": [
        "research",
        "search",
        "paper",
        "learn",
        "read",
        "rank",
        "knowledge",
        "调研",
        "论文",
        "学习",
        "阅读",
    ],
    "automation-workflow": [
        "workflow",
        "automation",
        "agent",
        "coauthor",
        "process",
        "flow",
        "deploy",
        "upload",
        "自动化",
        "流程",
    ],
}


TAG_KEYWORDS = {
    "browser": ["browser", "playwright", "chrome", "webapp", "web app"],
    "image": ["image", "photo", "draw", "illustration", "canvas", "gif"],
    "docs": ["doc", "document", "markdown", "readme", "pdf", "pptx", "docx", "xlsx"],
    "finance": ["finance", "invest", "stock", "market"],
    "coding": ["code", "api", "sdk", "react", "frontend", "typescript", "python"],
    "obsidian": ["obsidian", "vault", "canvas"],
    "data": ["data", "json", "table", "spreadsheet", "xlsx"],
    "workflow": ["workflow", "coauthor", "process", "flow"],
    "mcp": ["mcp"],
    "cli": ["cli", "command", "terminal"],
    "frontend": ["frontend", "react", "web design", "ui", "css"],
    "animation": ["animation", "motion", "lottie", "gsap", "timeline", "scrolltrigger", "three.js", "webgl", "动效", "动画"],
    "pdf": ["pdf"],
    "automation": ["automation", "agent", "testing", "deploy"],
    "research": ["research", "search", "paper", "learn"],
}


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "skill"


def run(args: list[str], cwd: Path | None = None, check: bool = True) -> str:
    result = subprocess.run(
        args,
        cwd=cwd or ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def load_registry() -> dict[str, Any]:
    if not PROJECTS_FILE.exists():
        return {"projects": []}
    return json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))


def save_registry(data: dict[str, Any]) -> None:
    REGISTRY_DIR.mkdir(exist_ok=True)
    PROJECTS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_tags(tags: list[str] | None = None) -> None:
    REGISTRY_DIR.mkdir(exist_ok=True)
    payload = {"tags": tags or DEFAULT_TAGS}
    TAGS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_frontmatter_text(text: str) -> dict[str, Any]:
    if text.startswith("<!-- source-sha256: "):
        text = text.partition("\n")[2]
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    meta: dict[str, Any] = {}
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            index += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value in {"", "|", ">", "|-", ">-", "|+", ">+"}:
            folded = value == "" or value.startswith(">")
            collected: list[str] = []
            index += 1
            while index < len(lines):
                next_line = lines[index]
                if next_line and not next_line.startswith((" ", "\t")):
                    break
                collected.append(next_line.strip())
                index += 1
            text = (" " if folded else "\n").join(item for item in collected if item).strip()
            if key in {"name", "description", "version", "license"}:
                meta[key] = text
            continue
        if key in {"name", "description", "version", "license"}:
            meta[key] = value
        index += 1
    return meta


def parse_frontmatter(path: Path) -> dict[str, Any]:
    return parse_frontmatter_text(path.read_text(encoding="utf-8", errors="replace"))


def find_repo_root(path: Path) -> Path | None:
    current = path.parent
    while current != ROOT.parent:
        if (current / ".git").exists():
            return current
        if current == ROOT:
            return None
        current = current.parent
    return None


def top_level_projects() -> list[Path]:
    if not LIBRARIES_DIR.exists():
        return []
    # 内部运维 skill 不进入公开目录，例如 skillhub-ingest
    _HIDDEN_PROJECTS = {"skillhub-ingest"}
    return sorted(
        [
            item
            for item in LIBRARIES_DIR.iterdir()
            if item.is_dir() and not item.name.startswith(".") and item.name not in _HIDDEN_PROJECTS
        ],
        key=lambda p: p.name.lower(),
    )


def parse_git_source(repo_root: Path) -> dict[str, str] | None:
    config_path = repo_root / ".git" / "config"
    if not config_path.exists():
        return None
    parser = configparser.ConfigParser()
    parser.read(config_path, encoding="utf-8")
    section = 'remote "origin"'
    if section not in parser:
        return None
    url = parser[section].get("url", "")
    match = re.search(r"github\.com[:/](?P<repo>[^/]+/[^/.]+)(?:\.git)?$", url)
    if not match:
        return None
    branch = "main"
    current_branch = run(["git", "-C", str(repo_root), "branch", "--show-current"], check=False)
    if current_branch:
        branch = current_branch
    else:
        for section_name in parser.sections():
            if section_name.startswith('branch "') and parser[section_name].get("remote") == "origin":
                merge = parser[section_name].get("merge", "")
                if merge.startswith("refs/heads/"):
                    branch = merge.removeprefix("refs/heads/")
                    break
    commit = run(["git", "-C", str(repo_root), "rev-parse", "HEAD"], check=False)
    return {"type": "github", "repo": match.group("repo"), "ref": branch, "commit": commit}


def infer_tags(name: str, description: str, path: Path) -> list[str]:
    haystack = f"{name} {description} {path.as_posix()}".lower()
    tags = [tag for tag, words in TAG_KEYWORDS.items() if any(word in haystack for word in words)]
    return tags[:5] or ["workflow"]


def infer_category(project: dict[str, Any]) -> str:
    project_name = project.get("name", "").lower()
    if any(word in project_name for word in ["obsidian", "notebooklm", "notebook-lm", "menu"]):
        return "daily-tools"
    if any(word in project_name for word in ["frontend-slides", "guizang-ppt-skill", "impeccable"]):
        return "frontend-presentation"
    if any(word in project_name for word in ["ppt", "slides", "baoyu", "huashu", "ljg"]):
        return "content-creation"
    text_parts = [
        project.get("name", ""),
        project.get("description", ""),
        " ".join(project.get("tags", [])),
    ]
    for skill in project.get("skills", []):
        text_parts.extend([skill.get("name", ""), skill.get("description", ""), " ".join(skill.get("tags", []))])
    haystack = " ".join(text_parts).lower()
    scores = {
        category: sum(1 for word in words if word.lower() in haystack)
        for category, words in CATEGORY_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] else "uncategorized"


def skill_entry(skill_path: Path, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    meta = parse_frontmatter(skill_path)
    name = meta.get("name") or skill_path.parent.name
    description = meta.get("description") or first_heading_or_line(skill_path) or ""
    path = rel(skill_path.parent)
    entry_id = slug(name)
    today = date.today().isoformat()
    previous = existing or {}
    entry = {
        "id": previous.get("id", entry_id),
        "name": name,
        "path": path,
        "original_path": original_skill_path(skill_path),
        "tags": previous.get("tags") or infer_tags(name, description, skill_path),
        "description": description,
        "added_at": previous.get("added_at", today),
    }
    if meta.get("version"):
        entry["version"] = meta["version"]
    if previous.get("extracted_path"):
        entry["extracted_path"] = previous["extracted_path"]
    return entry


def original_skill_path(skill_path: Path) -> str:
    repo_root = find_repo_root(skill_path)
    if repo_root:
        return skill_path.parent.resolve().relative_to(repo_root.resolve()).as_posix()
    parts = skill_path.relative_to(ROOT).parts
    project_root = LIBRARIES_DIR / parts[1] if len(parts) > 1 and parts[0] == LIBRARIES_DIR.name else ROOT / parts[0]
    return skill_path.parent.resolve().relative_to(project_root.resolve()).as_posix()


def first_heading_or_line(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line == "---" or line.startswith("name:") or line.startswith("description:"):
            continue
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def discover_project_skills(project_root: Path) -> list[Path]:
    ignored = {".git", "docs", "registry", "scripts", "__pycache__", "node_modules", "vendor", "tests"}
    candidates = []
    for path in project_root.rglob("SKILL.md"):
        relative_parts = path.relative_to(project_root).parts
        parts = set(relative_parts)
        if parts & ignored:
            continue
        candidates.append(path)

    paths = []
    has_canonical = any(not any(part.startswith(".") for part in path.relative_to(project_root).parts) for path in candidates)
    for path in candidates:
        has_hidden_part = any(part.startswith(".") for part in path.relative_to(project_root).parts)
        if has_canonical and has_hidden_part:
            continue
        paths.append(path)
    return sorted(paths, key=lambda p: p.as_posix().lower())


def project_description(project_root: Path) -> str:
    for name in ["README.md", "README.zh.md", "README.en.md"]:
        readme = project_root / name
        if readme.exists():
            return first_heading_or_line(readme)
    skills = discover_project_skills(project_root)
    if skills:
        return first_heading_or_line(skills[0])
    return ""


def project_entry(project_root: Path, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    today = date.today().isoformat()
    previous = existing or {}
    source = parse_git_source(project_root) if (project_root / ".git").exists() else None
    if not source and previous.get("source", {}).get("type") == "github":
        source = previous["source"]
    if not source:
        source = {"type": "local"}
    existing_skills: dict[str, dict[str, Any]] = {}
    for item in previous.get("skills", []):
        item_path = item.get("path", "")
        existing_skills[item_path] = item
        if item_path and not item_path.startswith(f"{LIBRARIES_DIR.name}/"):
            existing_skills[f"{LIBRARIES_DIR.name}/{item_path}"] = item
    # 去重：kami 等项目的根 SKILL.md 与 plugins/kami/skills/kami/SKILL.md 内容完全相同，需按文件哈希去重，保留更深路径的 canonical skill
    discovered = discover_project_skills(project_root)
    seen_hash: dict[str, Path] = {}
    deduped: list[Path] = []
    for p in sorted(discovered, key=lambda x: len(x.as_posix()), reverse=True):
        try:
            h = hashlib.sha256(p.read_bytes()).hexdigest()
        except Exception:
            h = p.as_posix()
        if h not in seen_hash:
            seen_hash[h] = p
            deduped.append(p)
    discovered = sorted(deduped, key=lambda p: p.as_posix().lower())
    skills = []
    used_ids: set[str] = set()
    for skill_path in discovered:
        entry = skill_entry(skill_path, existing_skills.get(rel(skill_path.parent)))
        base_id = slug(entry["name"])
        candidate = base_id
        counter = 2
        while candidate in used_ids:
            candidate = f"{base_id}-{counter}"
            counter += 1
        entry["id"] = candidate
        used_ids.add(candidate)
        skills.append(entry)
    tags = sorted({tag for skill in skills for tag in skill.get("tags", [])})
    entry = {
        "id": previous.get("id", slug(project_root.name)),
        "name": previous.get("name", project_root.name),
        "path": rel(project_root),
        "source": source,
        "tags": previous.get("tags") or tags[:8],
        "description": previous.get("description") or project_description(project_root),
        "added_at": previous.get("added_at", today),
        "last_checked_at": previous.get("last_checked_at", today),
        "last_synced_at": previous.get("last_synced_at", today if source.get("type") == "github" else None),
        "skill_count": len(skills),
        "skills": skills,
    }
    if previous.get("install"):
        entry["install"] = previous["install"]
    if previous.get("extracted"):
        entry["extracted"] = previous["extracted"]
    entry["category"] = previous.get("category") if previous.get("category_locked") else infer_category(entry)
    if previous.get("category_locked"):
        entry["category_locked"] = True
    return entry


def refresh_registry() -> dict[str, Any]:
    existing_by_path: dict[str, dict[str, Any]] = {}
    for item in load_registry().get("projects", []):
        path = item.get("path", "")
        existing_by_path[path] = item
        if path and not path.startswith(f"{LIBRARIES_DIR.name}/"):
            existing_by_path[f"{LIBRARIES_DIR.name}/{Path(path).name}"] = item
    projects = []
    used_ids: set[str] = set()
    for path in top_level_projects():
        entry = project_entry(path, existing_by_path.get(rel(path)))
        base_id = entry["id"]
        natural_id = slug(entry["name"])
        if re.fullmatch(rf"{re.escape(natural_id)}-\d+", base_id):
            base_id = natural_id
            entry["id"] = natural_id
        candidate = base_id
        counter = 2
        while candidate in used_ids:
            candidate = f"{base_id}-{counter}"
            counter += 1
        entry["id"] = candidate
        used_ids.add(candidate)
        projects.append(entry)
    data = {"projects": projects}
    save_registry(data)
    save_tags()
    return data


def github_latest_commit(repo: str, ref: str) -> str:
    return run(["gh", "api", f"repos/{repo}/commits/{ref}", "--jq", ".sha"])


def github_compare_summary(repo: str, base: str, head: str) -> str:
    output = run(
        ["gh", "api", f"repos/{repo}/compare/{base}...{head}", "--jq", ".status + \" \" + (.total_commits|tostring)"],
        check=False,
    )
    return output or "changed"


def github_changed_paths(repo: str, base: str, head: str) -> list[str]:
    output = run(
        ["gh", "api", f"repos/{repo}/compare/{base}...{head}", "--jq", ".files[].filename"],
        check=False,
    )
    return [line.strip() for line in output.splitlines() if line.strip()]


def source_path_matches(filename: str, source_path: str) -> bool:
    normalized = source_path.strip("/")
    if not normalized or normalized == ".":
        return True
    return filename == normalized or filename.startswith(f"{normalized}/")


def download_github_directory(repo: str, ref: str, remote_path: str, target: Path) -> None:
    temp = target.with_name(f".{target.name}.tmp")
    if temp.exists():
        shutil.rmtree(temp)
    temp.mkdir(parents=True)
    download_contents(repo, ref, remote_path, temp)
    if target.exists():
        shutil.rmtree(target)
    shutil.move(str(temp), str(target))


def download_contents(repo: str, ref: str, remote_path: str, target: Path) -> None:
    path_part = remote_path.strip("/")
    endpoint = f"repos/{repo}/contents/{path_part}?ref={ref}" if path_part else f"repos/{repo}/contents?ref={ref}"
    data = json.loads(run(["gh", "api", endpoint]))
    if isinstance(data, dict) and data.get("type") == "file":
        if target.exists() and target.is_dir():
            target = target / data["name"]
        elif not target.suffix and not target.name == data["name"]:
            target = target / data["name"]
        target.parent.mkdir(parents=True, exist_ok=True)
        content = data.get("content", "")
        target.write_bytes(base64.b64decode(content))
        return
    for item in data:
        item_target = target / item["name"]
        if item["type"] == "dir":
            download_contents(repo, ref, item["path"], item_target)
        elif item["type"] == "file":
            file_data = json.loads(run(["gh", "api", f"repos/{repo}/contents/{item['path']}?ref={ref}"]))
            item_target.parent.mkdir(parents=True, exist_ok=True)
            item_target.write_bytes(base64.b64decode(file_data.get("content", "")))
