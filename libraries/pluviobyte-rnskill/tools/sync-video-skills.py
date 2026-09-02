#!/usr/bin/env python3
"""Sync canonical video skills into rnskill with rn-prefixed names."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile


MAPPINGS = {
    "ai-motion-director": "rn-motion-director",
    "reference-video-replica-qc": "rn-replica-qc",
    "dark-saas-magic-video": "rn-dark-saas-video",
    "black-white-text-opener": "rn-bw-text-opener",
}

TEXT_SUFFIXES = {
    ".cjs",
    ".css",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".sh",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy video-production-skills into rnskill and normalize names."
    )
    parser.add_argument(
        "--source",
        default=os.environ.get("VIDEO_PRODUCTION_SKILLS_DIR"),
        help="Path to the canonical video-production-skills checkout.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        help="Source or rn-prefixed skill name to sync. Repeat as needed; defaults to all.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare generated content with the repository without modifying files.",
    )
    return parser.parse_args()


def resolve_targets(requested: list[str] | None) -> list[tuple[str, str]]:
    if not requested:
        return list(MAPPINGS.items())

    reverse = {destination: source for source, destination in MAPPINGS.items()}
    selected: list[tuple[str, str]] = []
    for name in requested:
        source = reverse.get(name, name)
        if source not in MAPPINGS:
            valid = ", ".join(sorted(set(MAPPINGS) | set(reverse)))
            raise ValueError(f"Unknown skill {name!r}. Expected one of: {valid}")
        pair = (source, MAPPINGS[source])
        if pair not in selected:
            selected.append(pair)
    return selected


def rewrite_text_files(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rewritten = original
        for source_name, destination_name in MAPPINGS.items():
            rewritten = rewritten.replace(source_name, destination_name)
        if rewritten != original:
            path.write_text(rewritten, encoding="utf-8")


def generate_skill(source_root: Path, output_root: Path, source_name: str, destination_name: str) -> None:
    source = source_root / source_name
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(f"Missing canonical skill: {source}")

    destination = output_root / destination_name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    rewrite_text_files(destination)


def tree_manifest(root: Path) -> dict[str, tuple[str, int]]:
    manifest: dict[str, tuple[str, int]] = {}
    if not root.exists():
        return manifest
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        mode = stat.S_IMODE(path.stat().st_mode)
        manifest[path.relative_to(root).as_posix()] = (digest, mode)
    return manifest


def main() -> int:
    args = parse_args()
    if not args.source:
        print(
            "error: pass --source or set VIDEO_PRODUCTION_SKILLS_DIR",
            file=sys.stderr,
        )
        return 2

    source_root = Path(args.source).expanduser().resolve()
    repository_root = Path(__file__).resolve().parents[1]
    skills_root = repository_root / "skills"

    try:
        targets = resolve_targets(args.skill)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if args.check:
        failed = False
        with tempfile.TemporaryDirectory(prefix="rnskill-sync-check-") as temporary:
            generated_root = Path(temporary)
            for source_name, destination_name in targets:
                generate_skill(source_root, generated_root, source_name, destination_name)
                expected = tree_manifest(generated_root / destination_name)
                actual = tree_manifest(skills_root / destination_name)
                if expected == actual:
                    print(f"ok: {destination_name}")
                    continue
                failed = True
                expected_paths = set(expected)
                actual_paths = set(actual)
                changed = sorted(
                    path
                    for path in expected_paths & actual_paths
                    if expected[path] != actual[path]
                )
                print(
                    f"mismatch: {destination_name} "
                    f"missing={len(expected_paths - actual_paths)} "
                    f"extra={len(actual_paths - expected_paths)} changed={len(changed)}"
                )
                for path in sorted(expected_paths - actual_paths):
                    print(f"  missing: {path}")
                for path in sorted(actual_paths - expected_paths):
                    print(f"  extra: {path}")
                for path in changed:
                    print(f"  changed: {path}")
        return 1 if failed else 0

    for source_name, destination_name in targets:
        generate_skill(source_root, skills_root, source_name, destination_name)
        print(f"synced: {source_name} -> {destination_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
