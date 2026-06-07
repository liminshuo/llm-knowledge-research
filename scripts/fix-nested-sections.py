#!/usr/bin/env python3
"""Fix duplicate nested <section> tags in generated pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for path in ROOT.glob("*.html"):
    if path.name in ("index.html", "background.html", "solutions.html", "principles.html", "problems.html"):
        continue
    text = path.read_text(encoding="utf-8")
    fixed = re.sub(
        r'(<section class="section" id="[^"]+">)\s*\1',
        r"\1",
        text,
    )
    if fixed != text:
        path.write_text(fixed, encoding="utf-8")
        print("Fixed", path.name)

print("Done.")
