from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Any

from skillhub_common import EXTRACTED_SKILLS_DIR, LIBRARIES_DIR, ROOT, load_registry, rel, save_registry


IGNORED_DIRS = {
    ".git",
    ".github",
    ".next",
    ".turbo",
    "__pycache__",
    "coverage",
    "dist",
    "node_modules",
    "test",
    "tests",
}

IGNORED_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}

COMMAND_RE = re.compile(r"\bnpx\s+[^`\r\n]*(?:skills?|impeccable)[^`\r\n]*", re.IGNORECASE)


def should_ignore(path: Path) -> bool:
    if path.name in IGNORED_FILES:
        return True
    if path.is_dir() and path.name in IGNORED_DIRS:
        return True
    return False


def copy_skill_dir(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)

    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored: set[str] = set()
        current = Path(directory)
        for name in names:
            child = current / name
            if should_ignore(child):
                ignored.add(name)
                continue
            if child.is_dir() and any(child.rglob("SKILL.md")):
                ignored.add(name)
        return ignored

    shutil.copytree(source, target, ignore=ignore)


def find_npx_command(project_path: Path) -> str | None:
    candidates = [
        project_path / "README.md",
        project_path / "README.zh.md",
        project_path / "README.en.md",
        project_path / "README.npm.md",
        project_path / "SKILL.md",
    ]
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in COMMAND_RE.finditer(text):
            command = match.group(0).strip()
            command = re.sub(r"\s+", " ", command)
            if "skills add" in command or "skill install" in command or "skills install" in command:
                return command
    return None


def extract_project(project: dict[str, Any], dry_run: bool = False) -> tuple[int, str | None]:
    project_path = ROOT / project["path"]
    target_project = EXTRACTED_SKILLS_DIR / project["id"]
    if not project_path.exists():
        return 0, f"missing source: {project['path']}"

    if target_project.exists() and not dry_run:
        shutil.rmtree(target_project)

    extracted_count = 0
    for skill in project.get("skills", []):
        source = ROOT / skill["path"]
        target = target_project / skill["id"]
        if dry_run:
            extracted_count += 1
            continue
        copy_skill_dir(source, target)
        skill["extracted_path"] = rel(target)
        extracted_count += 1

    if not dry_run:
        install: dict[str, Any] = {
            "method": "npx" if find_npx_command(project_path) else "extracted",
            "extracted_root": rel(target_project),
        }
        command = find_npx_command(project_path)
        if command:
            install["command"] = command
            install["fallback"] = "extracted"
        project["install"] = install

        source = project.get("source", {})
        project["extracted"] = {
            "root": rel(target_project),
            "source_library": project["id"],
            "source_path": project["path"],
            "last_extracted_commit": source.get("commit"),
            "skill_count": extracted_count,
        }

    return extracted_count, None


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract installable skills from libraries/ into extracted-skills/.")
    parser.add_argument("--project", help="Only extract one project id.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be extracted without changing files.")
    args = parser.parse_args()

    data = load_registry()
    projects = data.get("projects", [])
    if args.project:
        projects = [project for project in projects if project.get("id") == args.project]
        if not projects:
            raise SystemExit(f"Project not found: {args.project}")

    if not args.dry_run:
        EXTRACTED_SKILLS_DIR.mkdir(exist_ok=True)

    total = 0
    warnings: list[str] = []
    for project in projects:
        count, warning = extract_project(project, dry_run=args.dry_run)
        total += count
        if warning:
            warnings.append(f"{project.get('id')}: {warning}")

    if not args.dry_run:
        save_registry(data)

    print(f"Extracted {total} skills from {len(projects)} projects into {rel(EXTRACTED_SKILLS_DIR)}.")
    for warning in warnings:
        print(f"WARN {warning}")


if __name__ == "__main__":
    main()
