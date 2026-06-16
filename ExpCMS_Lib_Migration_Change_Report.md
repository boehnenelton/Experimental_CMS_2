# ExpCMS Library Isolation — Migration Change Report

**Date:** 2026-06-14
**Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
**Source plan:** `ExpCMS_Library_Rules_Report.md` (Library Isolation Rules & Remediation Report)
**Source library tree:** `Lib_PY.zip`

---

## What was done

Built `Lib_EXPCMS/` (36 files) exactly per the plan's inventory, sourced from `Lib_PY.zip` (Core / CMS / HTML / Chunker / System / Utility folders), and updated `ExpCSS_CMS.py` to point at it. `ExpCSS_Builder.py` was **not** included in this pass — see "Not done" below.

### 1. Frozen Core — 20 files, copied verbatim, unchanged filenames

All 20 versions in `Lib_PY.zip` matched the plan's frozen baseline table exactly (`lib_bejson_core.py` 2.0.3, `lib_bejson_env.py` 2.1.2, … `lib_av_manager.py` 2.0.1). Copied as-is, no edits.

**Flag — `lib_bejson_path_guard.py` discrepancy in the master tree:** `Lib_PY.zip` contains two non-identical copies of this file, both stamped `Version: 1.0.0 OFFICIAL`:
- `Core/lib_bejson_path_guard.py` — includes an `os.path.expandvars()` step on path components.
- `System/lib_bejson_path_guard.py` — same function without that step.

I used the **`Core/` copy** (the one with `expandvars`) as the frozen copy for `Lib_EXPCMS`, since it's the more permissive/likely-newer of the two. This is the same kind of silent-drift problem this whole migration is meant to stop — worth reconciling in the master `Lib_PY` tree itself so there's only one canonical `lib_bejson_path_guard.py` going forward.

### 2. ExpCMS-Owned CMS Layer — 6 of 7 planned files, copied + renamed

| Source | New file | Header changes |
|---|---|---|
| `lib_cms_core.py` (v18.0) | `lib_expcms_core.py` | `# LIBRARY:` comment updated to new filename |
| `lib_cms_mfdb.py` (v2.0.4) | `lib_expcms_mfdb.py` | `Library:` / `Family: CMS → EXPCMS` |
| `lib_cms_config.py` (v2.0.1) | `lib_expcms_config.py` | `Library:` / `Family: CMS → EXPCMS` |
| `lib_cms_content.py` (v2.1.0) | `lib_expcms_content.py` | `Library:` / `Family: CMS → EXPCMS` |
| `lib_cms_orchestrator.py` (v2.0.1) | `lib_expcms_orchestrator.py` | `Library:` / `Family: CMS → EXPCMS`, plus internal imports renamed (below) |
| `lib_cms_taxonomy.py` (v2.0.1) | `lib_expcms_taxonomy.py` | `Library:` / `Family: CMS → EXPCMS` |
| `lib_cms_persona_writer.py` | — | **Does not exist in `Lib_PY.zip`** ("if needed" in the plan — not needed). Skipped. |

**Internal cross-imports in `lib_expcms_orchestrator.py`** (the only file with `lib_cms_*` cross-references):
```python
import lib_expcms_config as CMSConfig
import lib_expcms_taxonomy as CMSTaxonomy
import lib_expcms_content as CMSContent
import lib_expcms_mfdb as CMSMFDB
```
Aliases unchanged, so `CMSConfig.x()`-style calls inside the file needed no further edits.

**Version numbers were left unchanged** on these 6 renamed files — they're verbatim forks at the moment of the split, just with `Library:`/`Family:` headers and the one internal import block updated. If you want the ExpCMS-owned fork to carry its own version lineage going forward (separate from BEJSON CMS's `lib_cms_*` numbering), say so and I'll set a starting version (e.g. reset to `1.0.0` or stamp `2.0.4-expcms`) across all six.

### 3. HTML3 Presentational — 8 files, copied verbatim, unchanged filenames

`lib_bejson_html3_skeletons.py`, `lib_html3_app_layout.py`, `lib_html3_body.py`, `lib_html3_list_renderer.py`, `lib_html3_sidemenu.py`, `lib_html3_tables.py`, `lib_html3_text.py`, `lib_html3_widgets.py` — no diverging logic found, copied as-is per the plan.

### 4. Chunker — 2 files

- `lib_mfdb_chunker_v6.py` — kept as-is (no BEJSON CMS equivalent, no collision).
- `lib_cms_chunker_wrapper.py` → `lib_expcms_chunker_wrapper.py` — renamed. File had no header block and no internal self-references to its own filename, so only the filename changed. The `CMS_Chunker_Wrapper` class name itself was **not** renamed (the plan only specifies renaming the module/import, and `ExpCSS_CMS.py` already aliases nothing extra — it does `from lib_expcms_chunker_wrapper import CMS_Chunker_Wrapper`).

### 5. `ExpCSS_CMS.py` — updated to v2.4.6

- `LIB_DIR = os.path.join(BASE_DIR, "Lib_EXPCMS")` (was `"Lib"`)
- `from lib_cms_mfdb import MFDB_CMS_Manager` → `from lib_expcms_mfdb import MFDB_CMS_Manager`
- `from lib_cms_chunker_wrapper import CMS_Chunker_Wrapper` → `from lib_expcms_chunker_wrapper import CMS_Chunker_Wrapper`
- All other imports (`lib_bejson_html3_skeletons`, `lib_html3_*`, `lib_mfdb_core`) are frozen-Core/HTML3 names — unchanged.
- Version bumped `v2.4.5 → v2.4.6`, date updated to 2026-06-14, docstring notes the `Lib_EXPCMS` migration.

---

## Verification

All 36 files in `Lib_EXPCMS/` import cleanly under Python 3.12 with `Lib_EXPCMS/` on `sys.path` (zero `ImportError`/`SyntaxError`). Every symbol `ExpCSS_CMS.py` imports — `MFDB_CMS_Manager`, `CMS_Chunker_Wrapper`, `COLOR`/`CSS_CORE`/etc., `HTML3_List_Renderer`, `html_card`/`html_table`/`html_widget`/etc., and `MFDBCore.bejson_core_load_file` / `mfdb_core_get_stats` / `mfdb_core_load_entity` — resolves correctly from the new module names. `ExpCSS_CMS.py` compiles cleanly (`py_compile`).

A final sweep of `Lib_EXPCMS/` confirms **zero remaining references to `lib_cms_*`** anywhere in the new library set.

I did **not** run the Flask app end-to-end (would need `Data/`, `Assets/`, `templates/`, `Processing/www/` directories that weren't part of this upload), so route-level behavior is unverified — only imports and symbol resolution.

---

## Not done — needs your input

1. **`ExpCSS_Builder.py`** was referenced by the plan (same `LIB_DIR` + import-rename treatment) but wasn't uploaded, so it's untouched. If it currently points at `Lib/` and imports `lib_cms_*`, it will break the moment `Lib/` is removed/replaced. Send it over and I'll apply the same edits.
2. **Old `Lib/` folder**: this package only adds `Lib_EXPCMS/` — it doesn't delete or modify whatever currently sits in ExpCMS's `Lib/`. Once you confirm `ExpCSS_Builder.py` (and anything else) is migrated, `Lib/` can be retired.
3. **`lib_bejson_path_guard.py` drift** in the master `Lib_PY` tree (see flag above) — worth fixing at the source so future syncs don't re-introduce the ambiguity.

---

## Package contents

```
ExpCSS_CMS-v2.4.6.zip
├── ExpCSS_CMS.py                  (v2.4.6 — updated entry point)
├── ExpCMS_Lib_Migration_Change_Report.md
└── Lib_EXPCMS/
    ├── lib_bejson_core.py              (frozen, 2.0.3)
    ├── lib_bejson_env.py               (frozen, 2.1.2)
    ├── lib_bejson_errors.py            (frozen, 2.0.1)
    ├── lib_bejson_schema.py            (frozen, 2.1.2)
    ├── lib_bejson_state_management.py  (frozen, 2.0.1)
    ├── lib_bejson_validator.py         (frozen, 2.0.2)
    ├── lib_bejson_list_validator.py    (frozen, 1.1.1)
    ├── lib_bejson_parse.py             (frozen, 2.1.0)
    ├── lib_bejson_path_guard.py        (frozen, 1.0.0 — Core/ variant, see flag)
    ├── lib_bejson_provider.py          (frozen, 2.1.1)
    ├── lib_bejson_utility.py           (frozen, 2.3.2)
    ├── lib_bejson_mfdb_core.py         (frozen, 2.0.1)
    ├── lib_bejson_mfdb_validator.py    (frozen, 2.0.1)
    ├── lib_mfdb_core.py                (frozen, 2.0.1)
    ├── lib_mfdb_validator.py           (frozen, 2.0.1)
    ├── lib_mfdb_extensions.py          (frozen, 2.0.1)
    ├── lib_bejson_static_backend.py    (frozen, 2.1.0)
    ├── lib_be_core.py                  (frozen, 2.1.3)
    ├── lib_be_project_service.py       (frozen, 2.2.1)
    ├── lib_av_manager.py                (frozen, 2.0.1)
    ├── lib_expcms_core.py              (was lib_cms_core.py v18.0)
    ├── lib_expcms_mfdb.py              (was lib_cms_mfdb.py v2.0.4)
    ├── lib_expcms_config.py            (was lib_cms_config.py v2.0.1)
    ├── lib_expcms_content.py           (was lib_cms_content.py v2.1.0)
    ├── lib_expcms_orchestrator.py      (was lib_cms_orchestrator.py v2.0.1)
    ├── lib_expcms_taxonomy.py          (was lib_cms_taxonomy.py v2.0.1)
    ├── lib_bejson_html3_skeletons.py   (verbatim, 3.0.1)
    ├── lib_html3_app_layout.py         (verbatim)
    ├── lib_html3_body.py               (verbatim, 3.0.0)
    ├── lib_html3_list_renderer.py      (verbatim, 2.1.1)
    ├── lib_html3_sidemenu.py           (verbatim, 3.0.0)
    ├── lib_html3_tables.py             (verbatim, 3.1.0)
    ├── lib_html3_text.py               (verbatim, 3.0.0)
    ├── lib_html3_widgets.py            (verbatim, 3.0.0)
    ├── lib_mfdb_chunker_v6.py          (kept as-is)
    └── lib_expcms_chunker_wrapper.py   (was lib_cms_chunker_wrapper.py)
```

---

*Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton*
