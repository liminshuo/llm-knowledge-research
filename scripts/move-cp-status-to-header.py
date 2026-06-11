#!/usr/bin/env python3
"""Move page-header status badge from .cp-status sibling into h1 (inline after title)."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

HEADER_BADGE_RE = re.compile(
    r'(\s*<h1>)([^<]*)(</h1>\s*\n\s*)'
    r'<span class="cp-status">(<span class="badge badge-status badge-[^"]+">[^<]+</span>)</span>',
)


def transform(html: str) -> tuple[str, bool]:
    new_html, n = HEADER_BADGE_RE.subn(r"\1\2 \4\3", html)
    return new_html, n > 0


def main():
    for path in sorted(ROOT.glob("problems-*.html")):
        text = path.read_text(encoding="utf-8")
        new_text, ok = transform(text)
        if ok:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path.name}")


if __name__ == "__main__":
    main()
