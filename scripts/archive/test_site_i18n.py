from generate_site import build_payload, html_template
from skillhub_common import load_registry


payload = build_payload(load_registry()["projects"])
skills = [skill for project in payload["projects"] for skill in project.get("skills", [])]
html = html_template()

assert skills and all(skill.get("description_zh") for skill in skills)
assert 'id="languageToggle"' in html and 'id="drawerLanguageToggle"' in html
assert 'data-language="translation"' not in html
print(f"Validated bilingual UI data for {len(skills)} skills.")
