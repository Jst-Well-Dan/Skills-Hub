# Punk Cover Style Catalog

Use these user-visible style names. This catalog references reusable style atoms in the repository-level `styles/` directory. `punk-cover` may list only styles whose `META.md` metadata includes `cover` or `poster` in `outputs`.

Do not copy prompt bodies into this catalog. Read the selected style's `META.md` and `STYLE.md` after the user chooses a style.

| Style | Style ID | Metadata | Style | Best For |
| --- | --- | --- | --- | --- |
| 黑白极简概念 | `black-white-minimal-concept` | `styles/black-white-minimal-concept/META.md` | `styles/black-white-minimal-concept/STYLE.md` | Abstract, editorial, philosophical, strategic, restrained covers with strong typography and visual metaphor. |
| 语义转译极简 | `semantic-minimal-translation` | `styles/semantic-minimal-translation/META.md` | `styles/semantic-minimal-translation/STYLE.md` | One word, short phrase, slogan, or concept that needs a clever minimal visual translation. |
| 复古手撕拼贴 | `retro-torn-collage` | `styles/retro-torn-collage/META.md` | `styles/retro-torn-collage/STYLE.md` | Social posts, cultural topics, controversy, growth, street energy, retro editorial covers. |
| 方块世界 | `block-world` | `styles/block-world/META.md` | `styles/block-world/STYLE.md` | Playful tutorials, tools, systems, building, upgrade, learning, game-like or constructive themes. |
| 巨型透视中文标题 | `giant-perspective-chinese-title` | `styles/giant-perspective-chinese-title/META.md` | `styles/giant-perspective-chinese-title/STYLE.md` | Chinese title-led covers needing maximum impact, spatial depth, speed, conflict, or event-poster energy. |
| 积木世界 | `brick-world` | `styles/brick-world/META.md` | `styles/brick-world/STYLE.md` | Playful systems, building, teamwork, plans, toys, family, education, and constructive metaphors. |
| 咨询报告视觉 | `consulting-report-visual` | `styles/consulting-report-visual/META.md` | `styles/consulting-report-visual/STYLE.md` | Business strategy, frameworks, operations, product thinking, consulting reports, and structured analysis. |
| 科研期刊概念 | `research-journal-concept` | `styles/research-journal-concept/META.md` | `styles/research-journal-concept/STYLE.md` | Science, research, medicine, materials, mechanisms, academic or lab-themed covers. |
| 复古弥散渐变 | `retro-diffuse-gradient` | `styles/retro-diffuse-gradient/META.md` | `styles/retro-diffuse-gradient/STYLE.md` | Art, design, music, brand, emotion, atmospheric essays, independent magazine-style covers. |
| 极简公共空间摄影 | `minimal-public-space-photography` | `styles/minimal-public-space-photography/META.md` | `styles/minimal-public-space-photography/STYLE.md` | Opinion essays, long-form articles, cultural observation, spatial order, individual-space metaphors, and restrained editorial photography covers. |
| 商业杂志头版 | `business-magazine-front-page` | `styles/business-magazine-front-page/META.md` | `styles/business-magazine-front-page/STYLE.md` | Business, technology, AI, startups, investment, trend analysis, sharp magazine-like editorial covers. |
| 黑白灰先锋几何 | `black-white-gray-avant-geometry` | `styles/black-white-gray-avant-geometry/META.md` | `styles/black-white-gray-avant-geometry/STYLE.md` | Experimental, stark, geometric, modernist, poster-like covers with restrained color. |

## Non-Cover Style Atoms

These reusable style atoms exist in `styles/`, but are not part of the default `punk-cover` menu because their `outputs` metadata does not include `cover` or `poster`.

| Style | Style ID | Outputs |
| --- | --- | --- |
| 像素头像 | `pixel-avatar` | `avatar` |
| 凌乱蜡笔宠物肖像 | `messy-crayon-pet-portrait` | `portrait` |
| 拍立得纪念卡 | `polaroid-keepsake` | `polaroid`, `portrait` |
| 时尚速写观察页 | `fashion-sketch-observation` | `portrait`, `editorial_page` |
| 怪诞灵魂手绘 | `grotesque-soul-sketch` | `portrait` |

## Automatic Recommendations

- For Xiaohongshu tutorials, prefer `巨型透视中文标题`, `复古手撕拼贴`, `方块世界`, or `积木世界`.
- For WeChat public account explainers, prefer `商业杂志头版`, `咨询报告视觉`, `黑白极简概念`, `极简公共空间摄影`, or `复古弥散渐变`.
- For X covers, prefer `商业杂志头版`, `黑白极简概念`, `黑白灰先锋几何`, `极简公共空间摄影`, or `语义转译极简`.
- For research-heavy material, prefer `科研期刊概念`.
- For a single abstract term, prefer `语义转译极简` or `黑白极简概念`.
