from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from skillhub_common import ROOT


TRANSLATIONS_DIR = ROOT / "translations"
REVIEWS_DIR = ROOT / "reviews"
REVIEW_TYPES = {"comparison": "横向比较", "review": "使用点评", "test": "测试记录"}


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("review must start with JSON front matter")
    marker = text.find("\n---\n", 4)
    if marker < 0:
        raise ValueError("review front matter is not closed")
    return json.loads(text[4:marker]), text[marker + 5 :]


def load_reviews() -> list[dict[str, Any]]:
    reviews = []
    if not REVIEWS_DIR.exists():
        return reviews
    for path in sorted(REVIEWS_DIR.glob("*.md")):
        meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
        if not isinstance(meta.get("title"), str) or meta.get("type") not in REVIEW_TYPES:
            raise ValueError(f"invalid review metadata: {path}")
        for field in ("related_projects", "related_skills"):
            if not isinstance(meta.get(field, []), list) or not all(isinstance(item, str) for item in meta.get(field, [])):
                raise ValueError(f"{field} must be a string list: {path}")
        reviews.append({**meta, "slug": path.stem, "body": body, "type_label": REVIEW_TYPES[meta["type"]]})
    return reviews


def reviews_by_skill(projects: list[dict], reviews: list[dict]) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    for project in projects:
        for skill in project.get("skills", []):
            key = f"{project['id']}/{skill['id']}"
            matches = [
                {field: review[field] for field in ("slug", "title", "type", "type_label")}
                for review in reviews
                if project["id"] in review.get("related_projects", []) or key in review.get("related_skills", [])
            ]
            if matches:
                result[skill["path"]] = matches
    return result


def translation_file(project: dict, skill: dict) -> Path:
    return TRANSLATIONS_DIR / project["id"] / skill["id"] / "SKILL.md"


def source_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def translation_source_hash(text: str) -> str | None:
    first_line = text.splitlines()[0] if text else ""
    prefix = "<!-- source-sha256: "
    return first_line[len(prefix) : -4].strip() if first_line.startswith(prefix) and first_line.endswith(" -->") else None


if __name__ == "__main__":
    meta, body = split_frontmatter('---\n{"title":"T","type":"review"}\n---\n# Body\n')
    assert meta["title"] == "T" and body == "# Body\n"
    digest = source_hash("source")
    assert translation_source_hash(f"<!-- source-sha256: {digest} -->\n译文") == digest
