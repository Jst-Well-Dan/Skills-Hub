---
name: skillhub-ingest
description: Add, classify, extract, document, and validate GitHub-hosted skills in the Skills-Hub repository. Use when the user asks to add one or more skill repositories, import skills from GitHub URLs, process todo.md skill intake items, recover from partial GitHub downloads, create a new category or tag for incoming skills, refresh the Skills-Hub registry/docs after intake, or repeat the repository's skill入库 workflow.
---

# SkillHub Ingest

## Purpose

Use this workflow to add external GitHub skill repositories to this Skills-Hub project without missing intake, classification, extraction, or publishing steps. Read the repository `AGENTS.md` first for the project-wide layout, generated-output rules, and baseline validation requirements.

## Intake Sources

If the user references `todo.md`, read it first and extract GitHub URLs. Treat blank lines as separators, not errors. Process repositories sequentially because registry writes are not concurrency-safe.

If the user provides URLs directly, normalize each GitHub URL to `owner/repo` and continue with the same workflow.

Before changing files, inspect local state:

```powershell
Get-ChildItem -Force
rg --files
git status --short
```

If the directory is not a Git repository, continue without git-based diff assumptions.

## Repository Discovery

For each incoming repository, choose a stable local target name before downloading:

- Prefer the upstream repo name when it is specific, such as `kami`.
- Add owner or purpose when the repo name is generic, such as `mattpocock-skills` instead of `skills`.
- Reuse an existing target only when it is clearly the same source.

Check whether it already exists:

```powershell
Test-Path libraries\<target-name>
rg '"id": "<target-name>"' registry\projects.yaml
python scripts\list_skills.py --name <target-name> --skills
```

Discover upstream skill paths:

```powershell
gh api repos/<owner>/<repo>/git/trees/<ref>?recursive=1 --jq '.tree[].path' | rg '(^|/)SKILL\.md$'
```

Choose the smallest source path that preserves the useful skill context:

- Use `.` when the repo root contains install docs, scripts, plugin metadata, or multiple skill areas that should stay together.
- Use `skills` when all intended skills live there and root-level context is not needed.
- Use a specific skill directory when only one skill should be tracked.

When unsure, prefer preserving repository context over over-narrow extraction.

## Add Repositories

Try `scripts/add_skill.py` first for ordinary GitHub directory intake:

```powershell
python scripts\add_skill.py https://github.com/<owner>/<repo> --path <source-path> --target <target-name> --tag <tag1> --tag <tag2>
```

If a GitHub API download times out or leaves a partial temp directory, remove only the failed temp directory after verifying it is under `libraries/`:

```powershell
$tmp = Resolve-Path libraries\.<target-name>.tmp -ErrorAction SilentlyContinue
if ($tmp -and $tmp.Path.StartsWith((Resolve-Path libraries).Path)) {
  Remove-Item -LiteralPath $tmp.Path -Recurse -Force
}
```

Then fall back to shallow clone when the whole repository should be tracked:

```powershell
git clone --depth 1 https://github.com/<owner>/<repo>.git libraries\<target-name>
python scripts\scan_skills.py
```

Use shallow clone especially for large repositories or repositories with many files under multiple skill directories. After cloning, `scan_skills.py` reads `.git/config` and records the GitHub source.

## Categories And Tags

Use existing categories unless the user explicitly requests or clearly implies a new durable category.

When adding a category:

1. Add it to `CATEGORY_LABELS` in `scripts/skillhub_common.py`.
2. Add useful keywords to `CATEGORY_KEYWORDS`.
3. Add any new tags to `DEFAULT_TAGS`, `TAG_KEYWORDS`, and `registry/tags.yaml`.
4. Lock projects that must remain in the new category:

```json
"category": "<category-id>",
"category_locked": true
```

Locking matters because later registry refreshes infer categories again unless `category_locked` is set.

Avoid inventing project tags that are not present in `registry/tags.yaml`. Prefer existing tags such as `docs`, `frontend`, `pdf`, `workflow`, `coding`, `data`, `image`, `automation`, and repository-specific new tags only when they are reusable.

## Extraction And Docs

After all projects are added and classifications are correct, extract the installable skills.

For `add_skill.py` imports, extracting only new projects is usually enough:

```powershell
python scripts\extract_skills.py --project <project-id>
```

For shallow-clone fallback or batch `todo.md` intake, rebuilding all extracted skills is acceptable when project count is modest:

```powershell
python scripts\extract_skills.py
```

Generate complete Chinese translations before rebuilding the website. The
translated front matter `description` is also the Chinese description shown on
skill cards:

```powershell
python scripts\translate_skills.py --project <project-id>
```

For batch intake, translate all missing or stale skills after the registry is
updated:

```powershell
python scripts\translate_skills.py --all
```

Then regenerate generated docs:

```powershell
python scripts\generate_docs.py
```

Then regenerate the static website HTML. The website is generated output; update
`scripts/generate_site.py` when behavior or styling needs to change, then rebuild
`site/index.html` from the registry:

```powershell
python scripts\generate_site.py
```

## Website Deployment

When the user asks to publish or deploy the Skills-Hub website, use GitHub Pages.
The repository includes `.github/workflows/pages.yml`, which regenerates
`site/index.html` and publishes the `site/` directory whenever `main` is pushed.

For a new public GitHub repository:

```powershell
python scripts\generate_site.py
git init
git branch -M main
git add .
git commit -m "Publish Skills-Hub"
gh repo create Skills-Hub --public --source=. --remote=origin --push
```

Then enable GitHub Pages with GitHub Actions as the build source:

```powershell
gh api --method POST repos/<owner>/Skills-Hub/pages -f build_type=workflow
```

If the Pages endpoint already exists, update it instead:

```powershell
gh api --method PUT repos/<owner>/Skills-Hub/pages -f build_type=workflow
```

After pushing, check the Pages workflow run and capture the Pages URL:

```powershell
gh run list --workflow pages.yml --limit 1
gh repo view --web
```

If GitHub Pages is not immediately available, wait for the first workflow run to
finish and query the Pages endpoint:

```powershell
gh api repos/<owner>/Skills-Hub/pages
```

## Validation

Run these checks before reporting completion:

```powershell
python -m json.tool registry\projects.yaml > $null
python -m json.tool registry\tags.yaml > $null
python scripts\list_skills.py --name <target-name> --skills
python scripts\list_skills.py --category <category-id> --skills
python scripts\translate_skills.py --project <project-id> --check
python scripts\generate_site.py
```

Also verify:

- No failed temp directories remain under `libraries/`.
- Each new project has the expected source snapshot under `libraries/<project-id>/`.
- Each extracted skill exists under `extracted-skills/<project-id>/`.
- Translation checks for the new project report no `MISSING` or `STALE` skills.
- `README.md`, `docs/index.md`, and `docs/by-category.md` mention the new projects.
- `registry/projects.yaml` does not point at a missing `libraries/<project-id>` directory.
- `site/index.html` exists and was regenerated after registry or generator changes.

Use `rg` for focused checks:

```powershell
rg '<project-id>|<category-label>' README.md docs\by-category.md docs\index.md
```

If intake came from `todo.md`, ask before deleting entries unless the user already requested cleanup. If cleanup is requested, remove only successfully imported URLs.

## Reporting

In the final response, include:

- Added project IDs and skill counts.
- Any new category or tag created.
- Main files updated.
- Validation commands that passed.
- GitHub repository URL and GitHub Pages URL when publishing succeeds, or the exact publishing blocker when it does not.
- Any retry or limitation that matters, such as a transient GitHub API failure or shallow-clone fallback.
