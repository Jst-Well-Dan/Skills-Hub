from __future__ import annotations

import argparse

from skillhub_common import CATEGORY_LABELS, load_registry


def main() -> None:
    parser = argparse.ArgumentParser(description="List indexed projects or skills.")
    parser.add_argument("--tag", help="Filter by tag.")
    parser.add_argument("--source", help="Filter by GitHub repo, for example owner/repo.")
    parser.add_argument("--name", help="Filter by name substring.")
    parser.add_argument("--category", help="Filter by category id, for example coding-tools.")
    parser.add_argument("--skills", action="store_true", help="Show skills nested under matching projects.")
    args = parser.parse_args()

    projects = load_registry().get("projects", [])
    for project in projects:
        source = project.get("source", {})
        if args.tag and args.tag not in project.get("tags", []):
            continue
        if args.source and source.get("repo") != args.source:
            continue
        if args.name and args.name.lower() not in project.get("name", "").lower():
            continue
        if args.category and project.get("category") != args.category:
            continue
        tags = ", ".join(project.get("tags", []))
        repo = source.get("repo", source.get("type", "local"))
        category = CATEGORY_LABELS.get(project.get("category", "uncategorized"), project.get("category", "未分类"))
        print(f"{project['id']}\t{project['name']}\t{category}\t{project['skill_count']} skills\t{tags}\t{repo}\t{project['path']}")
        if args.skills:
            for skill in project.get("skills", []):
                skill_tags = ", ".join(skill.get("tags", []))
                print(f"  - {skill['id']}\t{skill['name']}\t{skill_tags}\t{skill['path']}")


if __name__ == "__main__":
    main()
