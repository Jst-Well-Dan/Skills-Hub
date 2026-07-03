from __future__ import annotations

import argparse
from datetime import date
from skillhub_common import (
    ROOT,
    download_github_directory,
    github_changed_paths,
    github_compare_summary,
    github_latest_commit,
    load_registry,
    run,
    save_registry,
    source_path_matches,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check or sync GitHub-backed project libraries.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Only check upstream updates.")
    mode.add_argument("--apply", action="store_true", help="Download and overwrite changed skills.")
    parser.add_argument("--id", help="Limit to one project id.")
    args = parser.parse_args()

    data = load_registry()
    today = date.today().isoformat()
    changed = 0
    checked = 0

    for project in data.get("projects", []):
        if args.id and project.get("id") != args.id:
            continue
        source = project.get("source", {})
        if source.get("type") != "github":
            continue
        checked += 1
        repo = source["repo"]
        ref = source.get("ref", "main")
        current = source.get("commit", "")
        original_path = source.get("original_path", "")
        latest = github_latest_commit(repo, ref)
        project["last_checked_at"] = today
        if latest == current:
            print(f"OK      {project['id']} {repo}@{ref}")
            continue
        changed_paths = github_changed_paths(repo, current, latest) if current and original_path else []
        relevant_paths = [path for path in changed_paths if source_path_matches(path, original_path)]
        if original_path and current and not relevant_paths:
            source["commit"] = latest
            print(f"OKPATH  {project['id']} {repo}@{ref} no changes under {original_path}")
            continue
        changed += 1
        summary = github_compare_summary(repo, current, latest) if current else "changed"
        if original_path and current:
            path_summary = f", {len(relevant_paths)} path change(s) under {original_path}"
        elif original_path:
            path_summary = f", tracking {original_path}"
        else:
            path_summary = ""
        print(f"UPDATE  {project['id']} {repo}@{ref} {current[:7]} -> {latest[:7]} ({summary}{path_summary})")
        if args.apply:
            target = ROOT / project["path"]
            if (target / ".git").exists():
                run(["git", "-C", str(target), "pull", "--ff-only"])
            elif original_path:
                download_github_directory(repo, latest, original_path, target)
            else:
                print(f"SKIP    {project['id']} has no .git directory; update it manually.")
                continue
            source["commit"] = latest
            project["last_synced_at"] = today
            print(f"APPLIED {project['id']} -> {project['path']}")

    if args.apply:
        save_registry(data)
    elif checked:
        save_registry(data)
    print(f"Checked {checked} GitHub-backed projects; {changed} update(s) found.")


if __name__ == "__main__":
    main()
