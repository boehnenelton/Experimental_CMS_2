# Experimental CMS — Library Isolation Rules & Remediation Report

**Date:** 2026-06-14
**Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
**Scope:** Define the hard boundary between what Experimental CMS may and may not touch, relative to BEJSON CMS (v18 beta), which is the authoritative source of truth and is frozen from this project's perspective.

---

## The Rule (Non-Negotiable)

**BEJSON CMS is not touched. Not one line.**

Experimental CMS must:
- Use the **Core libraries exactly as they exist in BEJSON CMS** — frozen, verbatim copies.
- Work around the Core API. If something is missing, add it in EXPCMS-specific libs, not in Core.
- **Copy and rename** any non-Core library it needs to diverge from, under the `lib_expcms_` prefix.
- Never introduce a file into its `Lib_EXPCMS/` that shares a name with a Core library.

---

## BEJSON CMS Authoritative Lib Inventory (v18 beta — frozen baseline)

Located at: `src/src/lib/`

### CORE LIBRARIES — Experimental CMS copies verbatim, never modifies

These are the shared foundation. ExpCMS gets identical copies. Any future update to these originates in BEJSON CMS and flows downstream — never the other way.

| File | Version | Role |
|------|---------|------|
| `lib_bejson_core.py` | 2.0.3 | Atomic I/O, field map, BEJSON primitives |
| `lib_bejson_env.py` | 2.1.2 | Path resolution |
| `lib_bejson_errors.py` | 2.0.1 | Error codes and exception classes |
| `lib_bejson_schema.py` | 2.1.2 | Unified schema registry |
| `lib_bejson_state_management.py` | 2.0.1 | Granular state / change tracking |
| `lib_bejson_validator.py` | 2.0.2 | Structural BEJSON validation |
| `lib_bejson_list_validator.py` | 1.1.1 | List-type BEJSON validation |
| `lib_bejson_parse.py` | 2.1.0 | High-level parse/write |
| `lib_bejson_path_guard.py` | 1.0.0 | Path traversal guard |
| `lib_bejson_provider.py` | 2.1.1 | Provider abstraction |
| `lib_bejson_utility.py` | 2.3.2 | Misc utility |
| `lib_bejson_mfdb_core.py` | 2.0.1 | Alias shim → lib_mfdb_core |
| `lib_bejson_mfdb_validator.py` | 2.0.1 | Alias shim → lib_mfdb_validator |
| `lib_mfdb_core.py` | 2.0.1 | MFDB manifest/entity orchestrator |
| `lib_mfdb_validator.py` | 2.0.1 | Bidirectional MFDB validation |
| `lib_mfdb_extensions.py` | 2.0.1 | MFDB plugin/extension layer |
| `lib_bejson_static_backend.py` | 2.1.0 | Static site backend |
| `lib_be_core.py` | 2.1.3 | Backend engine core |
| `lib_be_project_service.py` | 2.2.1 | Project service layer |
| `lib_av_manager.py` | 2.0.1 | Audio/video subprocess manager |

**Total Core files: 20**

---

### CMS-FAMILY LIBRARIES — BEJSON CMS owns these. ExpCMS copies and renames under `lib_expcms_` prefix.

These are CMS-specific — not generic shared infrastructure. BEJSON CMS owns the canonical copies under `lib_cms_*`. Experimental CMS **must not use those filenames**. It copies what it needs and renames them.

| BEJSON CMS file | Version | ExpCMS renamed copy | Notes |
|-----------------|---------|---------------------|-------|
| `lib_cms_core.py` | 17.0+ | `lib_expcms_core.py` | Primary CMS engine — ExpCMS diverges here |
| `lib_cms_mfdb.py` | 2.0.4 | `lib_expcms_mfdb.py` | MFDB ops layer — ExpCMS may diverge |
| `lib_cms_config.py` | 2.0.1 | `lib_expcms_config.py` | Config management |
| `lib_cms_content.py` | 2.1.0 | `lib_expcms_content.py` | Content handler |
| `lib_cms_orchestrator.py` | 2.0.1 | `lib_expcms_orchestrator.py` | Master controller |
| `lib_cms_taxonomy.py` | 2.0.1 | `lib_expcms_taxonomy.py` | Tag/category manager |
| `lib_cms_persona_writer.py` | — | `lib_expcms_persona_writer.py` | Persona writer (if needed) |

**Total CMS-family files: 7**

These renamed copies are ExpCMS's property. Modify them freely. They will never collide with BEJSON CMS's `lib_cms_*` namespace.

---

### HTML3-FAMILY LIBRARIES — ExpCMS copies and renames only what it actually uses

From the Experimental CMS dependency trace (prior report), these HTML3 files are actually used:

| File | Action for ExpCMS |
|------|-------------------|
| `lib_bejson_html3_skeletons.py` | **Copy verbatim** — presentational constants, no logic to diverge |
| `lib_html3_app_layout.py` | **Copy verbatim** |
| `lib_html3_body.py` | **Copy verbatim** |
| `lib_html3_list_renderer.py` | **Copy verbatim** |
| `lib_html3_sidemenu.py` | **Copy verbatim** |
| `lib_html3_tables.py` | **Copy verbatim** |
| `lib_html3_text.py` | **Copy verbatim** |
| `lib_html3_widgets.py` | **Copy verbatim** |

If ExpCMS ever needs to modify HTML3 behavior, it renames those specific files to `lib_expcms_html3_*.py` before touching them.

**Total HTML3 files needed: 8**

---

### CHUNKER LIBRARIES — ExpCMS-specific, no BEJSON CMS equivalent

These exist in ExpCMS's current `Lib/` but have no counterpart in BEJSON CMS. They stay as-is under their current names — no rename needed since there's no collision.

| File | Status |
|------|--------|
| `lib_mfdb_chunker_v6.py` | Keep as-is |
| `lib_cms_chunker_wrapper.py` | **Rename → `lib_expcms_chunker_wrapper.py`** (uses `lib_cms_` prefix — must be disambiguated) |

---

## Final `Lib_EXPCMS/` File List (35 files total)

### Frozen Core (copy verbatim from BEJSON CMS, never modify)
```
lib_bejson_core.py
lib_bejson_env.py
lib_bejson_errors.py
lib_bejson_schema.py
lib_bejson_state_management.py
lib_bejson_validator.py
lib_bejson_list_validator.py
lib_bejson_parse.py
lib_bejson_path_guard.py
lib_bejson_provider.py
lib_bejson_utility.py
lib_bejson_mfdb_core.py
lib_bejson_mfdb_validator.py
lib_mfdb_core.py
lib_mfdb_validator.py
lib_mfdb_extensions.py
lib_bejson_static_backend.py
lib_be_core.py
lib_be_project_service.py
lib_av_manager.py
```

### ExpCMS-Owned CMS Layer (renamed copies — modify freely)
```
lib_expcms_core.py           ← was lib_cms_core.py
lib_expcms_mfdb.py           ← was lib_cms_mfdb.py
lib_expcms_config.py         ← was lib_cms_config.py
lib_expcms_content.py        ← was lib_cms_content.py
lib_expcms_orchestrator.py   ← was lib_cms_orchestrator.py
lib_expcms_taxonomy.py       ← was lib_cms_taxonomy.py
lib_expcms_persona_writer.py ← was lib_cms_persona_writer.py (if used)
```

### HTML3 Presentational (copy verbatim, rename only if diverging)
```
lib_bejson_html3_skeletons.py
lib_html3_app_layout.py
lib_html3_body.py
lib_html3_list_renderer.py
lib_html3_sidemenu.py
lib_html3_tables.py
lib_html3_text.py
lib_html3_widgets.py
```

### Chunker (ExpCMS-specific)
```
lib_mfdb_chunker_v6.py
lib_expcms_chunker_wrapper.py  ← was lib_cms_chunker_wrapper.py
```

---

## Required Code Changes in Experimental CMS

### 1. `LIB_DIR` in both entry points
```python
# ExpCSS_CMS.py and ExpCSS_Builder.py
LIB_DIR = os.path.join(BASE_DIR, "Lib_EXPCMS")  # was "Lib"
```

### 2. Import renames in entry points and internal libs

Wherever any ExpCMS file currently imports a `lib_cms_*` symbol, update to `lib_expcms_*`:

| Old import | New import |
|-----------|-----------|
| `import lib_cms_core as CMSCore` | `import lib_expcms_core as CMSCore` |
| `import lib_cms_mfdb as CMSMFDB` | `import lib_expcms_mfdb as CMSMFDB` |
| `import lib_cms_config as CMSConfig` | `import lib_expcms_config as CMSConfig` |
| `import lib_cms_content as CMSContent` | `import lib_expcms_content as CMSContent` |
| `import lib_cms_orchestrator as CMSOrch` | `import lib_expcms_orchestrator as CMSOrch` |
| `import lib_cms_taxonomy as CMSTaxonomy` | `import lib_expcms_taxonomy as CMSTaxonomy` |
| `import lib_cms_chunker_wrapper` | `import lib_expcms_chunker_wrapper` |

The alias (`as CMSCore`, `as CMSMFDB`, etc.) stays identical — so all downstream code that calls `CMSCore.something()` needs zero changes. Only the import line itself changes.

### 3. Internal cross-references inside the renamed lib files

Each `lib_expcms_*.py` file's own header `Library:` field and any internal self-references update to the new name. The `Family:` field changes from `CMS` to `EXPCMS`.

---

## The Boundary in One Sentence

> Experimental CMS reads Core libraries like a consumer — never a contributor. Everything CMS-specific it owns under `lib_expcms_*`. BEJSON CMS never knows ExpCMS exists.

---

*Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton*
