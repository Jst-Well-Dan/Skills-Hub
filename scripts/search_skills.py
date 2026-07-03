from __future__ import annotations

import argparse
from pathlib import Path

from skillhub_common import ROOT, load_registry


def main() -> None:
    parser = argparse.ArgumentParser(description="Search indexed skills.")
    parser.add_argument("query", nargs="+", help="Keyword(s) to search.")
    args = parser.parse_args()

    terms = [term.lower() for term in args.query]
    for project in load_registry().get("projects", []):
        project_hits = []
        for skill in project.get("skills", []):
            skill_file = ROOT / skill["path"] / "SKILL.md"
            body = ""
            if skill_file.exists():
                body = skill_file.read_text(encoding="utf-8", errors="replace")
            haystack = " ".join(
                [
                    project.get("name", ""),
                    project.get("description", ""),
                    skill.get("name", ""),
                    skill.get("description", ""),
                    " ".join(project.get("tags", [])),
                    " ".join(skill.get("tags", [])),
                    body,
                ]
            ).lower()
            if all(term in haystack for term in terms):
                project_hits.append(skill)
        if project_hits:
            source = project.get("source", {}).get("repo", project.get("source", {}).get("type", "local"))
            print(f"{project['id']} ({project['name']}) - {len(project_hits)} match(es) - {source}")
            for skill in project_hits:
                description = skill.get("description", "").replace("\n", " ")
                if len(description) > 120:
                    description = description[:117] + "..."
                print(f"  - {skill['id']}  {skill['path']}  {description}")
            print()


if __name__ == "__main__":
    main()
