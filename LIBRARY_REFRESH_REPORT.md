# ExpCSS CMS — Library Refresh Report
**CMS Version:** v2.4.4 → **v2.4.5**
**Date:** 2026-06-13
**Source libraries:** Chunked_Lib_{PY,JS,TS,SH}_v2_104db_bejson.txt

---

## 1. What Was Done

The CMS's `Lib/` folder (flat Python deployment, 71 files) was refreshed against
your new v2 PY library (80 files across `Core/`, `HTML/`, `CMS/`, `AI/`, `System/`,
`Gaming/`, `Cognition/`, `Utility/`).

| Action | Count | Detail |
|---|---|---|
| **Replaced** | 69 files | Matched by basename, flattened from `Core/`, `HTML/`, `CMS/`, `AI/`, `System/`, `Utility/` subfolders into `Lib/` |
| **Added** | 1 file | `lib_html3_text.py` — new dependency required by 4 of the replaced files (see §3) |
| **Kept untouched** | 2 files | `lib_cms_chunker_wrapper.py`, `lib_mfdb_chunker_v6.py` — CMS-specific, not part of the general library, verified compatible with new core (§4) |
| **Not added** | 5 items | `GEMINI.md`, `chunker_config.json`, `gemini_model_registry.104a.bejson`, `lib_cms_core.py`, `stress_test_bejson.py` — see §5 |

CMS header version bumped **v2.4.4 → v2.4.5** per Section 8.1 (every change bumps version).

---

## 2. Verification (Section 4 — Goal-Driven Execution)

| Step | Check | Result |
|---|---|---|
| 1. Syntax | `ast.parse()` on all 70 files in `Lib/` | ✅ Pass |
| 2. Compile | `py_compile.compile()` on all `Lib/*.py` | ✅ Pass, 0 errors |
| 3. Import | All 23 core/HTML3/CMS modules import individually | ✅ Pass |
| 4. CMS import | `import ExpCSS_CMS` and `import ExpCSS_Builder` | ✅ Pass |
| 5. App init | Flask app constructs, all 35 routes register | ✅ Pass |
| 6. Wrapper compat | `lib_mfdb_chunker_v6.py` calls into new `lib_bejson_core` (`bejson_core_atomic_write`, `bejson_core_create_104`, `bejson_core_load_file`) | ✅ All present, signatures unchanged |

---

## 3. Critical Fix Required During Integration: Relative Imports

**This is the one real issue found — without this fix, the CMS would crash on startup.**

The new v2 library is organized as proper Python packages (`HTML/__init__.py`,
etc.) and 9 of the replaced HTML3 files use **package-relative imports**
(`from .lib_html3_text import ...`).

The CMS deploys `Lib/` as a **flat directory added to `sys.path`** (see
`ExpCSS_CMS.py` line 28-29: `sys.path.append(LIB_DIR)`), not as an imported
package — so `from .module import x` raises `ImportError: attempted relative
import with no known parent package` the moment Flask tries to import
`lib_html3_widgets` or `lib_html3_body` (both imported directly by
`ExpCSS_CMS.py`).

**Fix applied:** Converted `from .module import x` → `from module import x`
(flat absolute import) in the 9 affected files. This matches the existing
flat-deployment convention already used by every other file in `Lib/`.

| File | Relative imports fixed |
|---|---|
| `lib_html3_body.py` | `lib_html3_text` |
| `lib_html3_widgets.py` | `lib_html3_text` |
| `lib_html3_feed_templates.py` | `lib_html3_text` |
| `lib_html3_flask.py` | `lib_bejson_html3_skeletons`, `lib_html3_page_templates`, `lib_html3_tables`, `lib_html3_body` |
| `lib_html3_page_templates.py` | `lib_bejson_html3_skeletons`, `lib_html3_sidemenu` |
| `lib_html3_bejson_renderer.py` | `lib_html3_body`, `lib_html3_tables`, `lib_html3_charts`, `lib_bejson_to_html`, `lib_html3_showcase` |
| `lib_bejson_to_html.py` | `lib_html3_body`, `lib_html3_text` |
| `lib_bejson_validator_diagram.py` | `lib_bejson_diagram_html` |
| `lib_html3_error_pages.py` | `lib_html3_page_templates` |
| `__init__.py` | all 13 relative imports (file is dead weight in flat layout either way — was already unreferenced before this update, left flattened for consistency) |

**New dependency added:** `lib_html3_text.py` (v3.0.0) — provides
`html_render_text()` / `is_html()`, used by `lib_html3_body`, `lib_html3_widgets`,
`lib_html3_feed_templates`, and `lib_bejson_to_html`. Uses `python-markdown` if
available (confirmed installed in this environment), falls back to basic
paragraph/line-break HTML escaping otherwise.

---

## 4. CMS-Specific Files — Kept As-Is

`lib_cms_chunker_wrapper.py` and `lib_mfdb_chunker_v6.py` exist only in the CMS
project, not in your general library. They were left untouched and verified
against the new `lib_bejson_core.py` — all three functions they call
(`bejson_core_atomic_write`, `bejson_core_create_104`, `bejson_core_load_file`)
exist with unchanged signatures in the new core. No action needed.

---

## 5. Available But Not Added (Confirm If Wanted)

These exist in your new v2 PY library but are **not referenced anywhere** in
the current CMS codebase. Per Section 3 (Surgical Changes — "do not add
features beyond what was asked"), they were left out of `Lib/`:

- **`lib_cms_core.py`** — new CMS-family module; not imported by `ExpCSS_CMS.py`, `lib_cms_*`, or `lib_mfdb_chunker_v6.py`.
- **`lib_html3_text.py`** — *(already added — required dependency, see §3)*
- **`stress_test_bejson.py`** — dev/test utility, not a runtime dependency.
- **`GEMINI.md`, `chunker_config.json`, `gemini_model_registry.104a.bejson`** — library-project metadata, not CMS runtime files.

If `lib_cms_core.py` is meant to supersede or extend functionality currently
split across `lib_cms_config.py` / `lib_cms_content.py` / `lib_cms_orchestrator.py`,
let me know and I'll wire it in with a proper integration pass rather than
dropping it in unreferenced.

---

## 6. Status of Previously-Reported Issues (from prior session)

All confirmed **resolved** in this v2 batch:

| ID | Issue | Status |
|---|---|---|
| TS1 | 6 missing `BEJSON_CORE_CODES` in `lib_bejson_types.ts` | ✅ Present (60–65) |
| TS2 | `lib_bejson_field_map.ts` missing doc-level cache injection | ✅ `_bejson_field_map` injection present |
| JS1/JS2 | `lib_mfdb_core.js` missing `mfdb_core_load_entity` / `mfdb_core_get_stats` | ✅ Both present |
| JS4 | MFDB version string `"1.21"` → `"1.31"` | ✅ Fixed |
| PY1/PY2 | `lib_bejson_utility.py` `CORE_DIR` path bug + dead double-try | ✅ `_OWN_DIR` fix present |
| PY3/PY4 | Validator bool/number type-check message + bool-as-integer bug | ✅ Both fixed (independently, same outcome) |
| ENC-COMPAT | TS/JS encryption format mismatch | ✅ TS `decryptRecord` now handles both string and object formats |

No outstanding tracked issues from the prior audit remain.

---

## 7. Files Changed Summary

```
ExperimentalCMS_v2/
├── ExpCSS_CMS.py          (version bump v2.4.4 → v2.4.5 only)
└── Lib/
    ├── lib_html3_text.py           [NEW]
    ├── lib_html3_body.py           [REPLACED + import fix]
    ├── lib_html3_widgets.py        [REPLACED + import fix]
    ├── lib_html3_feed_templates.py [REPLACED + import fix]
    ├── lib_html3_flask.py          [REPLACED + import fix]
    ├── lib_html3_page_templates.py [REPLACED + import fix]
    ├── lib_html3_bejson_renderer.py[REPLACED + import fix]
    ├── lib_bejson_to_html.py       [REPLACED + import fix]
    ├── lib_bejson_validator_diagram.py [REPLACED + import fix]
    ├── lib_html3_error_pages.py    [REPLACED + import fix]
    ├── __init__.py                 [REPLACED + import fix]
    └── ... 59 other files          [REPLACED, no import changes needed]
```

---

*Elton Boehnen · eltonboehnen@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton*
