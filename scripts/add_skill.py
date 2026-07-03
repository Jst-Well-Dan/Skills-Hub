from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

from skillhub_common import (
    LIBRARIES_DIR,
    ROOT,
    download_github_directory,
    github_latest_commit,
    load_registry,
    project_entry,
    save_registry,
)


def parse_repo(url_or_repo: str) -> str:
    if "/" in url_or_repo and "github.com" not in url_or_repo and not url_or_repo.endswith(".git"):
        return url_or_repo.strip("/")
    match = re.search(r"github\.com[:/](?P<repo>[^/]+/[^/.]+)(?:\.git)?", url_or_repo)
    if not match:
        raise SystemExit("Expected GitHub URL or owner/repo.")
    return match.group("repo")


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a GitHub project or skill directory as a project library.")
    parser.add_argument("repo", help="GitHub URL or owner/repo.")
    parser.add_argument("--path", required=True, help="Path to the skill directory inside the source repo.")
    parser.add_argument("--ref", default="main", help="Branch, tag, or commit. Default: main.")
    parser.add_argument("--target", help="Local target directory. Default: <repo-name> or <repo-name>-<path-name>.")
    parser.add_argument("--tag", action="append", default=[], help="Tag to attach. Repeatable.")
    args = parser.parse_args()

    repo = parse_repo(args.repo)
    latest = github_latest_commit(repo, args.ref)
    target_name = args.target or (repo.split("/")[-1] if args.path in {"", "."} else f"{repo.split('/')[-1]}-{Path(args.path).name}")
    target = LIBRARIES_DIR / target_name
    LIBRARIES_DIR.mkdir(exist_ok=True)
    download_github_directory(repo, latest, args.path.strip("/"), target)

    if not list(target.rglob("SKILL.md")):
        raise SystemExit(f"No SKILL.md found under {target}")

    entry = project_entry(target)
    entry["source"] = {
        "type": "github",
        "repo": repo,
        "ref": args.ref,
        "commit": latest,
        "original_path": args.path.strip("/"),
    }
    if args.tag:
        entry["tags"] = args.tag
    today = date.today().isoformat()
    entry["added_at"] = today
    entry["last_checked_at"] = today
    entry["last_synced_at"] = today

    data = load_registry()
    projects = [item for item in data.get("projects", []) if item.get("id") != entry["id"]]
    projects.append(entry)
    data["projects"] = sorted(projects, key=lambda item: item["id"])
    save_registry(data)
    print(f"Added project {entry['id']} with {entry['skill_count']} skill(s) at {entry['path']}")


if __name__ == "__main__":
    main()
