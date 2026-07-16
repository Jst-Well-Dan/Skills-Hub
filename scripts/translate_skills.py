from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from content_sources import source_hash, translation_file, translation_source_hash
from skillhub_common import ROOT, load_registry


def select_skills(project_id: str | None, skill_id: str | None, all_skills: bool) -> list[tuple[dict, dict]]:
    selected = []
    for project in load_registry().get("projects", []):
        if project_id and project["id"] != project_id:
            continue
        for skill in project.get("skills", []):
            if skill_id and skill["id"] != skill_id:
                continue
            selected.append((project, skill))
    if not all_skills and not project_id and not skill_id:
        raise SystemExit("Specify --project, --skill, or --all.")
    if not selected:
        raise SystemExit("No matching skills.")
    return selected


def translate(source: str) -> str:
    prompt = """Translate the following complete SKILL.md into Simplified Chinese.
Preserve all Markdown structure, front matter keys, code, commands, paths, identifiers, URLs, and placeholders exactly where translation would break behavior.
Translate all natural-language prose, including the front matter description.
Return only the complete translated Markdown with no fence, preface, note, or omission.

""" + source
    with tempfile.TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "translation.md"
        result = subprocess.run(
            ["codex", "exec", "--ephemeral", "--sandbox", "read-only", "-C", str(ROOT), "-o", str(output), "-"],
            input=prompt,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            shell=os.name == "nt",
        )
        if result.returncode or not output.exists():
            raise RuntimeError(f"Codex translation failed: {result.returncode}")
        return output.read_text(encoding="utf-8").strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate missing or stale Chinese SKILL.md translations with Codex.")
    parser.add_argument("--project")
    parser.add_argument("--skill")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--check", action="store_true", help="Report status without translating.")
    args = parser.parse_args()

    translated = 0
    for project, skill in select_skills(args.project, args.skill, args.all):
        source = (ROOT / skill["path"] / "SKILL.md").read_text(encoding="utf-8")
        digest = source_hash(source)
        target = translation_file(project, skill)
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        status = "current" if translation_source_hash(current) == digest else "stale" if current else "missing"
        print(f"{status.upper():7} {project['id']}/{skill['id']}")
        if args.check or (status == "current" and not args.force):
            continue
        translated_text = translate(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"<!-- source-sha256: {digest} -->\n{translated_text}", encoding="utf-8")
        translated += 1
    if translated:
        print(f"Translated {translated} skill(s).")


if __name__ == "__main__":
    main()
