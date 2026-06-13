# BEJSON Experimental CMS (Experimental_CMS_2)
> Advanced Multi-Tenant CMS Engine with Dynamic Component Rendering.

![Agent-Ready](https://img.shields.io/badge/Agent-Ready-red) ![llms.txt](https://img.shields.io/badge/llms.txt-Verified-black) ![Version](https://img.shields.io/badge/Version-2.5.0-blue)

## Overview
Experimental_CMS_2 is the bleeding-edge iteration of the BEJSON content management ecosystem. It introduces a modular component architecture, allowing for hot-swappable headers, footers, and body sections mapped to MFDB backend entities.

## Visual Architecture
```mermaid
graph TD
    A[Experimental_CMS Root] --> B[Lib]
    A --> C[Components]
    A --> D[Data/Workspace]
    B --> B1[CMS Orchestrator]
    B --> B2[BECSS Renderer]
    C --> C1[Headers/Footers]
    D --> D1[MFDB Content]
    D --> D2[MFDB Global]
```

## Quick Start
```bash
# Initialize and build a local site
python3 ExpCSS_CMS.py
```

## Core Innovation
- **Modular Components**: Template-driven HTML sections stored in `/Components`.
- **Dual MFDB Workspaces**: Separation of `db_content` (pages/apps) and `db_global` (nav/config).
- **AX-Ready**: Native support for agentic content ingestion and automated layout calibration.

## Documentation
- [AGENTS.md](./AGENTS.md) — Operational constraints.
- [ExperimentalCMS Bugs.md](./ExperimentalCMS%20Bugs.md) — Known issues and tracker.

---
**Elton Boehnen** · eltonboehnen@gmail.com · [github.com/boehnenelton](https://github.com/boehnenelton)
