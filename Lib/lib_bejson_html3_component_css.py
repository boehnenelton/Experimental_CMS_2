"""
FILE:         lib_bejson_html3_component_css.py
DESCRIPTION:  BECSS Component Layer CSS — injected into CSS_CORE_SKELETON via replace().
              All braces are doubled ({{ / }}) because the parent CSS_CORE_SKELETON
              goes through str.format(**COLOR) after this is substituted in.
VERSION:      1.0.0
DATE:         2026-06-03
AUTHOR:       Elton Boehnen
EMAIL:        boehnenelton@gmail.com
SITE:         boehnenelton2024.pages.dev
GITHUB:       github.com/boehnenelton
RELATIONAL_ID: e1f2a3b4-5c6d-7e8f-9a0b-1c2d3e4f5a6b
CHANGELOG:
  1.0.0 — 2026-06-03 — Initial creation. Provides the missing @layer components
                        and @layer utilities blocks that CSS_CORE_SKELETON expects
                        from this module.
"""

# ─────────────────────────────────────────────────────────────────────────────
# NOTE ON BRACE ESCAPING
# CSS_CORE_SKELETON uses str.format(**COLOR) on the assembled CSS string.
# Because COMPONENT_CSS is inserted via str.replace() *before* .format() runs,
# every CSS brace must be doubled: { → {{ and } → }}
# The only un-doubled tokens are COLOR keys like {primary}, {bg_page}, etc.
# ─────────────────────────────────────────────────────────────────────────────

COMPONENT_CSS = """

/* ═══════════════════════════════════════════════════
   BECSS COMPONENT LAYER (v2026)
   Cards · Buttons · Tables · Utilities · Badges
   ═══════════════════════════════════════════════════ */

@layer components {{

    /* ── SIDEBAR (base) ── */
    .c-sidebar {{
        display: flex;
        flex-direction: column;
        height: 100%;
        background: var(--bg-page);
        border-right: 1px solid var(--border);
        overflow: hidden;
    }}
    .c-sidebar__links {{
        display: flex;
        flex-direction: column;
        gap: 2px;
    }}

    /* ── HAMBURGER ── */
    .c-hamburger {{
        cursor: pointer;
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 6px;
        background: none;
        border: none;
        flex-shrink: 0;
    }}
    .c-hamburger span {{
        display: block;
        width: 20px;
        height: 2px;
        background: currentColor;
        transition: var(--transition);
    }}
    @media (min-width: 1025px) {{
        .c-hamburger {{ display: none; }}
    }}

    /* ── CARD ── */
    .c-card {{
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-sm);
    }}
    .c-card__title {{
        font-weight: 800;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-main);
        margin-bottom: 0.5rem;
    }}
    .c-card__body {{
        font-size: 0.85rem;
        color: var(--text-muted);
        line-height: 1.6;
    }}
    .c-card-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1rem;
    }}

    /* ── PRIMARY BUTTON / CODE-BOX COPY (c-code-box__copy acts as the
       primary action button across the CMS) ── */
    .c-code-box__copy {{
        display: inline-block;
        background: var(--primary);
        color: #fff;
        border: none;
        border-radius: var(--radius);
        padding: 8px 16px;
        font-family: var(--font-mono);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        cursor: pointer;
        text-decoration: none;
        transition: var(--transition);
        white-space: nowrap;
    }}
    .c-code-box__copy:hover {{
        opacity: 0.88;
        text-decoration: none;
        color: #fff;
    }}

    /* ── CODE BOX (full) ── */
    .c-code-box {{
        background: var(--bg-alt);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        margin-bottom: 1rem;
    }}
    .c-code-box__header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 12px;
        background: oklch(12% 0 0);
        border-bottom: 1px solid var(--border);
    }}
    .c-code-box__title {{
        font-family: var(--font-mono);
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: oklch(70% 0 0);
    }}
    .c-code-box__pre {{
        margin: 0;
        padding: 1rem;
        overflow-x: auto;
        font-size: 0.85rem;
        background: oklch(10% 0 0);
    }}
    .c-code-box__code {{
        font-family: var(--font-mono);
        color: oklch(90% 0 0);
    }}

    /* ── STATS BAR ── */
    .c-stats-bar {{
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 0.75rem 1rem;
        background: var(--bg-alt);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        margin-bottom: 1rem;
    }}
    .c-stats-bar__item {{
        display: flex;
        flex-direction: column;
        gap: 2px;
        min-width: 80px;
    }}
    .c-stats-bar__label {{
        font-family: var(--font-mono);
        font-size: 0.55rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-muted);
    }}
    .c-stats-bar__value {{
        font-size: 1.1rem;
        font-weight: 800;
        color: var(--text-main);
    }}

    /* ── TABLE ── */
    .c-table-container {{
        overflow-x: auto;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        margin-bottom: 1rem;
    }}
    .c-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }}
    .c-table th {{
        padding: 10px 12px;
        text-align: left;
        font-family: var(--font-mono);
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        background: var(--bg-alt);
        border-bottom: 1px solid var(--border);
        white-space: nowrap;
    }}
    .c-table td {{
        padding: 10px 12px;
        border-bottom: 1px solid var(--border-muted);
        color: var(--text-main);
        vertical-align: middle;
    }}
    .c-table tr:last-child td {{ border-bottom: none; }}
    .c-table tr:hover td {{ background: var(--bg-alt); }}

    /* ── INPUT ── */
    .c-input {{
        display: block;
        width: 100%;
        background: var(--bg-page);
        color: var(--text-main);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 10px 12px;
        font-family: var(--font-sans);
        font-size: 0.85rem;
        transition: border-color 0.2s ease;
        outline: none;
    }}
    .c-input:focus {{ border-color: var(--primary); }}

    /* ── ACCORDION ── */
    .c-accordion {{ border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; margin-bottom: 1rem; }}
    .c-accordion__item {{ border-bottom: 1px solid var(--border); }}
    .c-accordion__item:last-child {{ border-bottom: none; }}
    .c-accordion__header {{
        display: flex; align-items: center; justify-content: space-between;
        padding: 12px 16px; cursor: pointer; font-weight: 700;
        font-size: 0.85rem; background: var(--bg-alt);
        transition: var(--transition);
    }}
    .c-accordion__header:hover {{ color: var(--primary); }}
    .c-accordion__icon {{ transition: transform 0.2s ease; font-size: 0.8rem; }}
    .c-accordion__item[open] .c-accordion__icon {{ transform: rotate(90deg); }}
    .c-accordion__content {{ padding: 12px 16px; font-size: 0.85rem; color: var(--text-muted); }}

    /* ── PROGRESS BAR ── */
    .c-progress-container {{ margin-bottom: 1rem; }}
    .c-progress-label {{
        display: flex; justify-content: space-between;
        font-family: var(--font-mono); font-size: 0.65rem;
        text-transform: uppercase; letter-spacing: 0.05em;
        color: var(--text-muted); margin-bottom: 4px;
    }}
    .c-progress-bar {{
        height: 6px; background: var(--bg-alt);
        border-radius: 999px; overflow: hidden;
        border: 1px solid var(--border-muted);
    }}
    .c-progress-fill {{
        height: 100%; background: var(--primary);
        border-radius: 999px; transition: width 0.4s ease;
    }}

    /* ── SUBTABS ── */
    .c-subtabs {{
        display: flex; gap: 4px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem; overflow-x: auto;
    }}
    .c-subtabs__btn {{
        padding: 8px 16px; border: none; background: none;
        font-family: var(--font-mono); font-size: 0.7rem;
        text-transform: uppercase; letter-spacing: 0.05em;
        cursor: pointer; color: var(--text-muted);
        border-bottom: 2px solid transparent;
        transition: var(--transition); white-space: nowrap;
    }}
    .c-subtabs__btn:hover {{ color: var(--primary); }}
    .c-subtabs__btn--active {{ color: var(--primary); border-bottom-color: var(--primary); }}
    .c-tab-content {{ display: none; }}
    .c-tab-content--active {{ display: block; }}

    /* ── DEFINITION LIST ── */
    .c-dl {{ display: flex; flex-direction: column; gap: 8px; }}
    .c-dl__item {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 8px 0; border-bottom: 1px solid var(--border-muted);
        font-size: 0.85rem;
    }}
    .c-dl__item:last-child {{ border-bottom: none; }}
    .c-dl__term {{ color: var(--text-muted); font-family: var(--font-mono); font-size: 0.75rem; text-transform: uppercase; }}
    .c-dl__desc {{ font-weight: 600; }}

    /* ── EMPTY STATE ── */
    .c-empty-state {{
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; padding: 48px 24px; text-align: center;
        color: var(--text-muted);
    }}
    .c-empty-state__icon {{ font-size: 2rem; margin-bottom: 12px; opacity: 0.4; }}
    .c-empty-state__title {{ font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 6px; }}
    .c-empty-state__text {{ font-size: 0.8rem; line-height: 1.6; }}

    /* ── TOAST ── */
    .c-toast-container {{
        position: fixed; bottom: 80px; right: 16px;
        display: flex; flex-direction: column; gap: 8px;
        z-index: 9000;
    }}

    /* ── BEJSON FORM ── */
    .c-bejson-form {{ display: flex; flex-direction: column; gap: 1rem; }}
    .c-bejson-form__field {{ display: flex; flex-direction: column; gap: 4px; }}
    .c-bejson-form__label {{
        font-family: var(--font-mono); font-size: 0.6rem;
        text-transform: uppercase; letter-spacing: 0.08em;
        color: var(--text-muted);
    }}
    .c-bejson-form__type {{
        font-family: var(--font-mono); font-size: 0.6rem;
        color: var(--primary); margin-left: 4px;
    }}
    .c-bejson-form__input, .c-bejson-form__textarea {{
        width: 100%; background: var(--bg-page);
        border: 1px solid var(--border); border-radius: var(--radius);
        padding: 8px 10px; font-family: var(--font-mono);
        font-size: 0.8rem; color: var(--text-main);
        transition: border-color 0.2s ease; outline: none;
    }}
    .c-bejson-form__input:focus,
    .c-bejson-form__textarea:focus {{ border-color: var(--primary); }}
    .c-bejson-form__actions {{ display: flex; gap: 8px; }}
    .c-bejson-form__btn-submit {{ /* inherits from c-code-box__copy */ }}
    .c-bejson-form__btn-reset {{
        background: var(--bg-alt); color: var(--text-muted);
        border: 1px solid var(--border); border-radius: var(--radius);
        padding: 8px 16px; font-family: var(--font-mono);
        font-size: 0.7rem; cursor: pointer; transition: var(--transition);
    }}
    .c-bejson-form__btn-reset:hover {{ border-color: var(--primary); color: var(--primary); }}
    .c-bejson-form__form {{ display: contents; }}

    /* ── BEJSON TABLE BUTTON ── */
    .c-bejson-table__btn {{
        background: none; border: none; cursor: pointer;
        font-family: var(--font-mono); font-size: 0.65rem;
        text-transform: uppercase; padding: 4px 8px;
        color: var(--text-muted); border-radius: var(--radius);
        transition: var(--transition);
    }}
    .c-bejson-table__btn:hover {{ color: var(--primary); background: var(--bg-alt); }}

    /* ── DASHBOARD / STATS ── */
    .c-stats-dashboard {{ /* container for dashboard content */ }}

    /* ── ARTICLE ── */
    .c-article {{ max-width: 760px; }}

    /* ── BACKUP MANAGER ── */
    .c-backup-manager {{ /* container */ }}

    /* ── IMAGE GALLERY ── */
    .c-image-gallery {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 1rem;
    }}

}}

/* ═══════════════════════════════════════════════════
   BECSS UTILITY LAYER (v2026)
   Spacing · Flex · Color · Display
   ═══════════════════════════════════════════════════ */

@layer utilities {{

    /* Flex */
    .u-flex  {{ display: flex; }}
    .u-grid  {{ display: grid; }}
    .u-block {{ display: block; }}
    .u-hidden {{ display: none !important; }}

    .u-flex-col     {{ flex-direction: column; }}
    .u-flex-wrap    {{ flex-wrap: wrap; }}
    .u-flex-1       {{ flex: 1; }}

    .u-justify-between {{ justify-content: space-between; }}
    .u-justify-center  {{ justify-content: center; }}
    .u-justify-end     {{ justify-content: flex-end; }}

    .u-align-center  {{ align-items: center; }}
    .u-align-start   {{ align-items: flex-start; }}
    .u-align-end     {{ align-items: flex-end; }}

    .u-gap-8  {{ gap: 0.5rem; }}
    .u-gap-16 {{ gap: 1rem; }}
    .u-gap-24 {{ gap: 1.5rem; }}
    .u-gap-32 {{ gap: 2rem; }}

    /* Margin bottom */
    .u-mb-8  {{ margin-bottom: 0.5rem; }}
    .u-mb-16 {{ margin-bottom: 1rem; }}
    .u-mb-24 {{ margin-bottom: 1.5rem; }}
    .u-mb-32 {{ margin-bottom: 2rem; }}

    /* Margin top */
    .u-mt-8  {{ margin-top: 0.5rem; }}
    .u-mt-16 {{ margin-top: 1rem; }}
    .u-mt-24 {{ margin-top: 1.5rem; }}
    .u-mt-32 {{ margin-top: 2rem; }}

    /* Text */
    .u-text-muted   {{ color: var(--text-muted); }}
    .u-text-primary {{ color: var(--primary); }}
    .u-text-main    {{ color: var(--text-main); }}
    .u-text-upper   {{ text-transform: uppercase; }}
    .u-text-mono    {{ font-family: var(--font-mono); }}

    .u-fs-small {{ font-size: 0.75rem; }}
    .u-fs-xsmall {{ font-size: 0.65rem; }}

    .u-fw-bold  {{ font-weight: 700; }}
    .u-fw-black {{ font-weight: 800; }}

    /* Overflow */
    .u-truncate {{
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }}

    /* ── BADGE ── */
    .u-badge {{
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        border-radius: 999px;
        font-family: var(--font-mono);
        font-size: 0.6rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        background: var(--bg-alt);
        color: var(--text-muted);
        border: 1px solid var(--border);
    }}
    .u-badge--active {{
        background: oklch(95% 0.06 150);
        color: oklch(35% 0.12 150);
        border-color: oklch(80% 0.08 150);
    }}
    .u-badge--inactive {{
        background: var(--bg-alt);
        color: var(--text-muted);
        opacity: 0.65;
    }}
    .u-badge--warn {{
        background: oklch(95% 0.08 80);
        color: oklch(35% 0.12 80);
        border-color: oklch(80% 0.1 80);
    }}

    /* Full width */
    .u-w-full {{ width: 100%; }}
    .u-max-w-sm {{ max-width: 400px; }}
    .u-max-w-md {{ max-width: 640px; }}

}}

"""
