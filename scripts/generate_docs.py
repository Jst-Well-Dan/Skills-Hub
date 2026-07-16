from __future__ import annotations

from collections import defaultdict
from content_sources import REVIEW_TYPES, load_reviews
from skillhub_common import CATEGORY_LABELS, DOCS_DIR, ROOT, load_registry


START = "<!-- SKILLS_INDEX_START -->"
END = "<!-- SKILLS_INDEX_END -->"


def short_text(value: str, limit: int = 140) -> str:
    text = " ".join((value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def category_label(category: str) -> str:
    return CATEGORY_LABELS.get(category or "uncategorized", category or "未分类")


def project_line(project: dict) -> str:
    tags = ", ".join(project.get("tags", [])) or "untagged"
    source = project.get("source", {}).get("repo", project.get("source", {}).get("type", "local"))
    category = category_label(project.get("category", "uncategorized"))
    description = short_text(project.get("description", ""))
    lines = [
        f"- [{project['name']}]({project['path']}) `{project['id']}` - {project['skill_count']} 个 skills",
        f"  分类：{category} | 标签：{tags} | 来源：{source}",
    ]
    install = install_line(project)
    if install:
        lines.append(f"  安装：{install}")
    if description:
        lines.append(f"  简介：{description}")
    return "  \n".join(lines)


def install_line(project: dict, link_prefix: str = "") -> str:
    install = project.get("install", {})
    if install.get("method") == "npx" and install.get("command"):
        fallback = install.get("extracted_root")
        if fallback:
            return f"推荐 `{install['command']}`；也可从 [`{fallback}`]({link_prefix}{fallback}) 手动复制。"
        return f"推荐 `{install['command']}`。"
    extracted_root = install.get("extracted_root") or project.get("extracted", {}).get("root")
    if extracted_root:
        return f"复制 [`{extracted_root}`]({link_prefix}{extracted_root}) 下需要的 skill 到 `~/.claude/skills/`。"
    return ""


def skill_line(skill: dict) -> str:
    description = short_text(skill.get("description", ""), 110)
    suffix = f" - {description}" if description else ""
    extracted = skill.get("extracted_path")
    install = f" | 可复制：[`{extracted}`]({extracted})" if extracted else ""
    return f"  - [{skill['name']}]({skill['path']}/SKILL.md) `{skill['id']}`{install}{suffix}"


def build_index(projects: list[dict]) -> str:
    skill_count = sum(project["skill_count"] for project in projects)
    lines = [
        "# Skill 库总览",
        "",
        f"当前共收藏 {len(projects)} 个 Skill 库，包含 {skill_count} 个 skills。",
        "",
        "另见：[专题点评与测试](reviews/index.md)",
        "",
    ]
    for project in sorted(projects, key=lambda x: x["id"]):
        lines.append(project_line(project))
        for skill in sorted(project.get("skills", []), key=lambda x: x["id"]):
            lines.append(skill_line(skill))
        lines.append("")
    return "\n".join(lines) + "\n"


def build_by_category(projects: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for project in projects:
        grouped[project.get("category", "uncategorized")].append(project)
    lines = ["# 按分类查看 Skill 库", ""]
    for category in CATEGORY_LABELS:
        items = grouped.get(category, [])
        if not items:
            continue
        lines.extend([f"## {CATEGORY_LABELS[category]}", ""])
        for project in sorted(items, key=lambda x: x["id"]):
            lines.append(project_line(project))
        lines.append("")
    return "\n".join(lines)


def build_by_tag(projects: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for project in projects:
        for tag in project.get("tags", []) or ["untagged"]:
            grouped[tag].append(project)
    lines = ["# 按标签查看 Skill 库", ""]
    for tag in sorted(grouped):
        lines.extend([f"## {tag}", ""])
        for project in sorted(grouped[tag], key=lambda x: x["id"]):
            lines.append(project_line(project))
        lines.append("")
    return "\n".join(lines)


def build_by_source(projects: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for project in projects:
        source = project.get("source", {}).get("repo", project.get("source", {}).get("type", "local"))
        grouped[source].append(project)
    lines = ["# 按来源查看 Skill 库", ""]
    for source in sorted(grouped):
        lines.extend([f"## {source}", ""])
        for project in sorted(grouped[source], key=lambda x: x["id"]):
            lines.append(project_line(project))
            for skill in sorted(project.get("skills", []), key=lambda x: x["id"]):
                lines.append(skill_line(skill))
        lines.append("")
    return "\n".join(lines)


def build_readme_index(projects: list[dict]) -> str:
    skill_count = sum(project["skill_count"] for project in projects)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for project in projects:
        grouped[project.get("category", "uncategorized")].append(project)

    lines = [
        "## 收藏概览",
        "",
        f"当前共收藏 **{len(projects)}** 个 Skill 库，包含 **{skill_count}** 个 skills。",
        "",
        "## 按分类查看",
        "",
    ]
    for category in CATEGORY_LABELS:
        items = sorted(grouped.get(category, []), key=lambda x: x["id"])
        if not items:
            continue
        lines.extend([f"### {CATEGORY_LABELS[category]}", ""])
        for project in items:
            lines.append(project_line(project))
            preview = sorted(project.get("skills", []), key=lambda x: x["id"])[:6]
            for skill in preview:
                lines.append(skill_line(skill))
            remaining = project.get("skill_count", 0) - len(preview)
            if remaining > 0:
                lines.append(f"  - 另有 {remaining} 个 skills，见 [{project['name']}]({project['path']}) 或 [完整索引](docs/index.md)。")
            lines.append("")
    lines.extend(
        [
            "## 完整索引",
            "",
            "- [完整 Skill 库索引](docs/index.md)",
            "- [按分类查看](docs/by-category.md)",
            "- [按标签查看](docs/by-tag.md)",
            "- [按来源查看](docs/by-source.md)",
            "- [安装与提炼说明](docs/install.md)",
            "- [专题点评与测试](docs/reviews/index.md)",
        ]
    )
    return "\n".join(lines) + "\n"


def write_reviews() -> int:
    reviews = load_reviews()
    output_dir = DOCS_DIR / "reviews"
    output_dir.mkdir(parents=True, exist_ok=True)
    for old_file in output_dir.glob("*.md"):
        old_file.unlink()
    lines = ["# 专题点评与测试", ""]
    for review in reviews:
        output = output_dir / f"{review['slug']}.md"
        output.write_text(review["body"], encoding="utf-8")
        lines.append(f"- [{review['title']}]({output.name}) · {REVIEW_TYPES[review['type']]}")
    if not reviews:
        lines.append("暂时还没有点评文章。")
    (output_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(reviews)


def build_install_doc(projects: list[dict]) -> str:
    lines = [
        "# 安装与提炼说明",
        "",
        "这个仓库保留两份内容：",
        "",
        "- `libraries/<library-id>/`：上游 GitHub 项目快照，用来同步和对照来源。",
        "- `extracted-skills/<library-id>/<skill-id>/`：从上游项目中提炼出的可复制 skill。",
        "",
        "安装时优先使用上游推荐的 `npx skills` 命令；没有明确命令时，直接复制 `extracted-skills/` 里的对应目录到 `~/.claude/skills/`。",
        "",
        "## 项目安装方式",
        "",
    ]
    for project in sorted(projects, key=lambda x: x["id"]):
        lines.extend([f"### {project['name']}", ""])
        install = install_line(project, "../")
        lines.append(install or "暂未记录安装方式。")
        lines.append("")
        for skill in sorted(project.get("skills", []), key=lambda x: x["id"]):
            extracted = skill.get("extracted_path")
            if extracted:
                lines.append(f"- `{skill['id']}`：[`{extracted}`](../{extracted})")
        lines.append("")
    return "\n".join(lines)


def readme_template(index: str) -> str:
    return f"""# Skills-Hub

这是一个个人 Skill 库收藏仓库。根目录只保留管理文件，实际收藏的 GitHub 项目放在 `libraries/` 下；每个项目库作为一级目录，项目里的多个 `SKILL.md` 作为二级 skill 管理。

## 常用命令

```bash
python scripts/scan_skills.py
python scripts/extract_skills.py
python scripts/list_skills.py
python scripts/list_skills.py --skills
python scripts/list_skills.py --category coding-tools --skills
python scripts/search_skills.py pdf
python scripts/sync_skills.py --check
python scripts/translate_skills.py --project impeccable
python scripts/generate_docs.py
python scripts/generate_site.py
```

## 汉化与点评

- 完整译文放在 `translations/<project-id>/<skill-id>/SKILL.md`；用 `translate_skills.py` 按项目或 skill 生成，`--check` 只检查缺失和过期状态。
- 点评源放在 `reviews/*.md`，使用 JSON front matter 的 `related_projects` 或 `related_skills` 关联目录项；`generate_docs.py` 会生成 `docs/reviews/`。

{START}
{index}
{END}
"""


def update_readme(index: str) -> None:
    readme = ROOT / "README.md"
    block = f"{START}\n{index}\n{END}"
    if not readme.exists():
        readme.write_text(readme_template(index), encoding="utf-8")
        return
    text = readme.read_text(encoding="utf-8")
    if START in text and END in text:
        before = text.split(START, 1)[0]
        after = text.split(END, 1)[1]
        text = before + block + after
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    readme.write_text(text, encoding="utf-8")


def main() -> None:
    projects = load_registry().get("projects", [])
    DOCS_DIR.mkdir(exist_ok=True)
    index = build_index(projects)
    readme_index = build_readme_index(projects)
    (DOCS_DIR / "index.md").write_text(index, encoding="utf-8")
    (DOCS_DIR / "by-category.md").write_text(build_by_category(projects), encoding="utf-8")
    (DOCS_DIR / "by-tag.md").write_text(build_by_tag(projects), encoding="utf-8")
    (DOCS_DIR / "by-source.md").write_text(build_by_source(projects), encoding="utf-8")
    (DOCS_DIR / "install.md").write_text(build_install_doc(projects), encoding="utf-8")
    review_count = write_reviews()
    update_readme(readme_index)
    skill_count = sum(project["skill_count"] for project in projects)
    print(f"Generated docs for {len(projects)} projects, {skill_count} skills, and {review_count} reviews.")


if __name__ == "__main__":
    main()
