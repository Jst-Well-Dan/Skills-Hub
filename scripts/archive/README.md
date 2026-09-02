# scripts/archive

已归档、不再参与主流水线的脚本。

| 文件 | 归档原因 | 归档时间 |
|---|---|---|
| `test_site_i18n.py` | 双语 UI 已下线（`site/index.html` 的 `languageToggle` 已 `display:none`，`PRODUCT.md` 转为单语），原断言 `description_zh` / `languageToggle` 与现状冲突 | 2026-09-02 |

> 如需恢复校验，可将此文件移回 `scripts/` 后运行 `python scripts/test_site_i18n.py`，或参考其逻辑改写为 `test_site_integrity.py`。
