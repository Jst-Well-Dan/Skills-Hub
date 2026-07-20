---
name: skillhub-review
description: Create, edit, associate, publish, and validate review articles for projects and skills in the Skills-Hub repository. Use when the user asks to write a skill review, comparison, usage guide, test record, or learning note; add content under reviews/; attach a review to one or more catalog projects or individual skills; make a review appear in the website's related-review section; regenerate review documentation or site data; or troubleshoot review front matter and linkage.
---

# SkillHub Review

Read the repository `AGENTS.md` and root `REVIEWS.md` completely before changing review content. Treat `REVIEWS.md` as the source of truth for format, relationships, generation, and validation.

## Workflow

1. Inspect `git status --short` and preserve unrelated or in-progress work.
2. Read every source `SKILL.md` needed to support the requested review. Do not infer contents from names or registry descriptions alone.
3. Resolve project and skill IDs from `registry/projects.yaml`.
4. Create or edit only the source article under `reviews/<slug>.md`; choose `related_projects` for a whole collection or `related_skills` for exact skills.
5. Run the existing loader check and generators exactly as documented in `REVIEWS.md`.
6. Verify the generated article, index entry, and website associations. Inspect the final diff and remove only unrelated changes caused by the generation run.

Do not place auxiliary Markdown such as `reviews/README.md` in `reviews/`; every `*.md` there is parsed as an article. Do not hand-edit `docs/reviews/`, `site/index.html`, or `site/skill-content.json` instead of regenerating them.

## Reporting

Report the source article, generated article, relationship scope, generated files, and validation result. Mention unrelated worktree changes only when they affect verification or remain present.
