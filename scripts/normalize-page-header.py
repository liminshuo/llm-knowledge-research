#!/usr/bin/env python3
"""Move page-desc / component-problem out of .page-header (match problems-answer-search layout)."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def find_div_block(html, class_name, start_at=0):
    marker = f'<div class="{class_name}">'
    start = html.find(marker, start_at)
    if start == -1:
        return None
    i = start + len(marker)
    depth = 1
    while i < len(html) and depth > 0:
        next_open = html.find("<div", i)
        next_close = html.find("</div>", i)
        if next_close == -1:
            return None
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            end = next_close + len("</div>")
            if depth == 0:
                return start, end, html[start:end]
            i = next_close + len("</div>")
    return None


def inner_html(outer):
    open_end = outer.find(">") + 1
    return outer[open_end : -len("</div>")]


def transform(html):
    block = find_div_block(html, "page-header")
    if not block:
        return html, False
    start, end, outer = block
    inner = inner_html(outer).strip()
    moved = []
    work = inner

    while True:
        m = re.search(r'(?s)<p class="page-desc[^"]*"[^>]*>.*?</p>\s*', work)
        if m:
            moved.append(m.group(0).strip())
            work = (work[: m.start()] + work[m.end() :]).strip()
            continue
        cp = find_div_block(work, "component-problem")
        if cp and work.find('<div class="component-problem">') == cp[0]:
            cs, ce, cp_html = cp
            moved.append(cp_html.strip())
            work = (work[:cs] + work[ce:]).strip()
            continue
        break

    if not moved:
        after = html[end:].lstrip()
        if (after.startswith('<p class="page-desc') or after.startswith('<div class="component-problem')) and "page-desc" not in work and "component-problem" not in work:
            return html, False
        return html, False

    header_inner = work.strip()
    new_header = f'<div class="page-header">\n      {header_inner}\n    </div>'
    moved_block = "\n\n    ".join(moved)
    return html[:start] + new_header + "\n\n    " + moved_block + html[end:], True


def main():
    paths = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else sorted(ROOT.glob("problems-*.html"))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        new_text, ok = transform(text)
        if ok:
            path.write_text(new_text, encoding="utf-8")
            print("updated", path.name)


if __name__ == "__main__":
    main()
