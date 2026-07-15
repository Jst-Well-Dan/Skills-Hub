# Skills-Hub Project Guidance

## Repository Layout

- `libraries/` contains source snapshots of upstream projects. Do not edit these
  copies unless a task explicitly requires it.
- `extracted-skills/` is generated installable output. Regenerate it with
  `scripts/extract_skills.py`; do not hand-edit it.
- `registry/projects.yaml` and `registry/tags.yaml` are the source of truth for
  the catalog.
- `README.md`, `docs/`, and `site/index.html` are generated from the registry.
  Regenerate them instead of making isolated manual edits.

## When Catalog Data Changes

After changing project or tag registry data, run the relevant commands:

```powershell
python scripts\extract_skills.py [--project <project-id>]
python scripts\generate_docs.py
python scripts\generate_site.py
```

Validate JSON-formatted registry files with `python -m json.tool` and ensure no
failed `libraries/.*.tmp/` directory remains. Preserve unrelated worktree
changes, including intake repositories that may be in progress.

## Scope-Specific Workflows

For importing GitHub-hosted skills, category classification, or publication,
follow the `skillhub-ingest` skill. It contains the operational details and
fallback procedures for those tasks.
