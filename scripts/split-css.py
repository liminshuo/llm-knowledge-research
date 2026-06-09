#!/usr/bin/env python3
"""Split assets/css/style.monolith.css into modular files and regenerate style.css imports.

Run from repo root after editing style.monolith.css:
  python3 scripts/split-css.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "assets" / "css"
MONOLITH = ROOT / "style.monolith.css"
ENTRY = ROOT / "style.css"

IMPORT_ORDER = [
    "tokens.css",
    "base.css",
    "layout.css",
    "page.css",
    "components/summary-card.css",
    "components/surface-card.css",
    "components/content-widgets.css",
    "components/badges.css",
    "components/misc.css",
    "components/ui-demo.css",
    "components/answer-card.css",
    "components/drawers.css",
    "components/ui-system-page.css",
]

LAYOUT = [1, 2, 3, 4, 5, 6, 7, 8, 21, 22]
PAGE = [9, 10, 13, 20]
WIDGETS = [14, 15, 16, 17, 18]
MISC = [23, 24, 25, 26]


def join_sections(parts, indices):
    return "\n".join(parts[i].strip() for i in indices) + "\n"


def main():
    original = MONOLITH.read_text()
    parts = re.split(r"\n(?=/\* ── )", original)

    reset = parts[0]
    root_match = re.search(r":root\s*\{[^}]*\}", reset, re.S)
    if not root_match:
        raise SystemExit("no :root block in monolith")

    tokens_css = "/* ── Design tokens (docs/ui-system.md §1) ── */\n\n" + root_match.group(0) + "\n"
    base_css = reset.replace(root_match.group(0), "").strip() + "\n"

    files = {
        "tokens.css": tokens_css,
        "base.css": base_css,
        "layout.css": join_sections(parts, LAYOUT),
        "page.css": join_sections(parts, PAGE),
        "components/summary-card.css": join_sections(parts, [11]),
        "components/surface-card.css": join_sections(parts, [12]),
        "components/content-widgets.css": join_sections(parts, WIDGETS),
        "components/badges.css": join_sections(parts, [19]),
        "components/misc.css": join_sections(parts, MISC),
        "components/ui-demo.css": join_sections(parts, [27]),
        "components/answer-card.css": join_sections(parts, [28]),
        "components/drawers.css": join_sections(parts, [29, 30]),
        "components/ui-system-page.css": join_sections(parts, [31]),
    }

    (ROOT / "components").mkdir(exist_ok=True)
    for rel, content in files.items():
        (ROOT / rel).write_text(content)

    entry = "/* Entry point — modular CSS. See /AGENTS.md */\n\n"
    entry += "\n".join(f'@import url("{p}");' for p in IMPORT_ORDER) + "\n"
    ENTRY.write_text(entry)
    print(f"Regenerated {len(files)} modules + {ENTRY.name}")


if __name__ == "__main__":
    main()
