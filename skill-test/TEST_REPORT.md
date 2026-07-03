# Skill Test Report

Date: 2026-06-26

## Summary

Test outputs for the remaining newly ingested skill libraries are stored under `skill-test/`.

| Skill library | Test directory | Result |
| --- | --- | --- |
| `lottie` / `text-to-lottie` | `skill-test/lottie`, `skill-test/lottie-player` | Passed JSON validation and official player runtime HTTP probe |
| `gsap-skills` | `skill-test/gsap` | Static GSAP demo generated and pattern-checked |
| `huashu-md-html` | `skill-test/huashu-md-html` | Passed any-to-md, md-to-html, html-to-md, and md-to-docx script tests |

## Lottie

Files:

- `skill-test/lottie/public/projects/skillhub-motion/scene-1/lottie.json`
- `skill-test/lottie/public/projects/skillhub-motion/scene-1/controls.json`
- `skill-test/lottie-player/public/projects/skillhub-motion/scene-1/lottie.json`
- `skill-test/lottie-player/public/projects/skillhub-motion/scene-1/controls.json`

Validation:

```powershell
node -e "JSON.parse(require('fs').readFileSync('skill-test/lottie/public/projects/skillhub-motion/scene-1/lottie.json','utf8')); JSON.parse(require('fs').readFileSync('skill-test/lottie/public/projects/skillhub-motion/scene-1/controls.json','utf8')); console.log('lottie json ok')"
npx degit diffusionstudio/lottie skill-test/lottie-player
npm install
npm run dev -- --host 127.0.0.1
Invoke-WebRequest http://127.0.0.1:3030/__context
Invoke-WebRequest http://127.0.0.1:3030/skillhub-motion/scene-1?frame=60
```

Notes:

- `npm install` copied `public/canvaskit.wasm`.
- `GET /__context` returned HTTP 200 and listed `skillhub-motion/scene-1`.
- `GET /skillhub-motion/scene-1?frame=60` returned HTTP 200.
- `npm run build` currently fails inside upstream `@kobalte/core` declaration files with `TS2693`; the dev server path required by the skill works.

## GSAP Skills

File:

- `skill-test/gsap/index.html`

Validation:

```powershell
rg "gsap\.timeline|gsap\.matchMedia|ScrollTrigger|registerPlugin|autoAlpha|stagger" skill-test\gsap\index.html
```

Coverage:

- Core tween defaults, transform aliases, `autoAlpha`, stagger.
- Timeline sequencing and position parameters.
- ScrollTrigger registration, top-level timeline trigger, scrub and pin.
- `gsap.matchMedia()` with `prefers-reduced-motion`.

## Huashu Md Html

Files:

- `skill-test/huashu-md-html/input.md`
- `skill-test/huashu-md-html/output-article.html`
- `skill-test/huashu-md-html/roundtrip.md`
- `skill-test/huashu-md-html/markitdown.md`
- `skill-test/huashu-md-html/output.docx`

Validation:

```powershell
python extracted-skills\huashu-md-html\huashu-md-html\scripts\md_to_html.py skill-test\huashu-md-html\input.md --theme article -o skill-test\huashu-md-html\output-article.html
python extracted-skills\huashu-md-html\huashu-md-html\scripts\html_to_md.py skill-test\huashu-md-html\output-article.html -o skill-test\huashu-md-html\roundtrip.md
python extracted-skills\huashu-md-html\huashu-md-html\scripts\any_to_md.py skill-test\huashu-md-html\output-article.html -o skill-test\huashu-md-html\markitdown.md
python extracted-skills\huashu-md-html\huashu-md-html\scripts\md_to_docx.py skill-test\huashu-md-html\input.md --page-size a4 -o skill-test\huashu-md-html\output.docx
```

Notes:

- Installed missing package `html-to-markdown`; `trafilatura` and `markdownify` were already present.
- All four conversion scripts produced outputs.
