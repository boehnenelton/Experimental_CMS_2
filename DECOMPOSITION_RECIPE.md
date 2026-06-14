# Experimental_CMS - Decomposition Recipe
**Type:** Python / Flask / HTML3
**Purpose:** Experimental dashboard for modular CMS component development.
**Date Analyzed:** 2026-06-14

## Identity
- **Name:** Experimental_CMS
- **Type:** Research & Development CMS
- **Purpose:** Testbed for HTML3 Layouts, List Renderers, and Dynamic Tables.
- **Status:** Active (Experimental)
- **Dependencies:** Flask, lib_expcms_mfdb, lib_html3_list_renderer, lib_html3_sidemenu, lib_expcms_chunker_wrapper.

## Architecture Overview
Experimental_CMS utilizes a modular architecture focused on UI component prototyping. It isolated its own library family (`Lib_EXPCMS`) to prevent collision with stable CMS versions. It features a telemetry-style HUD and real-time dashboard stats via MFDBCore.

## File Structure
```
Experimental_CMS/
├── Components/ (Reusable HTML sections: Hero, Footer, HUD)
├── Lib_EXPCMS/ (Isolated library fork)
├── HTML_Skeletons/ (Base layouts: Article, Category, Global)
├── templates/ (Administrative dashboard views)
├── ExpCSS_CMS.py (Main entry point)
├── ExpCSS_Builder.py (Component builder tool)
└── project_tracker.json (Version and state tracking)
```

## Styling
### Color Palette
- **Primary:** #DE2626 (Accent Red)
- **Secondary:** #222222 (Background Card)

### Typography
- **Headings:** Inter
- **Body:** Inter / Source Code Pro

### CSS Patterns
- HTML3 Layout (HUD/Telemetry style)
- Dynamic List Rendering

## Classes & Interfaces
### MFDB_CMS_Manager (Lib_EXPCMS/lib_expcms_mfdb)
- **Purpose:** Manages workspace MFDB databases (`db_content`, `db_global`).
- **Methods:**
  - `initialize_system()` -> Bootstraps workspace and manifests.

## Functions
### dashboard()
- **Purpose:** Renders the main admin view with real-time MFDB stats.

### serve_assets(filename)
- **Purpose:** Static asset delivery route.

## Features (Categorized)
### UI Prototyping
- ✓ HTML3 HUD — Telemetry-inspired administrative header.
- ✓ Component-Based Layout — Modular hero and section sections.
- ✓ Dynamic Tables — Brutal-style data tables with auto-population.

### Management
- ✓ Isolated Libraries — Clean-room environment for experimental logic.
- ✓ Preview Server — Built-in local server for real-time site testing.

## Reconstruction Checklist
- [ ] Initialize `Lib_EXPCMS` dependencies.
- [ ] Bootstrap `Data/workspace` MFDB manifests.
- [ ] Launch via `python3 ExpCSS_CMS.py`.
