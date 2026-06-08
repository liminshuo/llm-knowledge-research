#!/usr/bin/env python3
"""将独立「解决方案」模块并入问题论证各页，移除顶栏入口。"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

REDIRECTS = {
    "solutions-architecture.html": "problems-format.html#solution",
    "solutions-format-priority.html": "problems-format.html#solution",
    "solutions-pipeline.html": "problems-format.html#solution",
    "solutions-roadmap.html": "problems-format.html#solution",
    "solutions-light-ia.html": "problems-structure-metadata.html#solution",
    "solutions-metadata.html": "problems-structure-metadata.html#solution",
    "solutions-kb-integration.html": "problems-structure-metadata.html#solution",
    "solutions-ref-dialogs.html": "principles-ref-dialogs.html",
}

LINK_MAP = {
    "solutions-architecture.html": "problems-format.html#solution",
    "solutions-format-priority.html": "problems-format.html#solution",
    "solutions-pipeline.html": "problems-format.html#solution",
    "solutions-roadmap.html": "problems-format.html#solution",
    "solutions-light-ia.html": "problems-structure-metadata.html#solution",
    "solutions-metadata.html": "problems-structure-metadata.html#solution",
    "solutions-kb-integration.html": "problems-structure-metadata.html#solution",
    "solutions-ref-dialogs.html": "principles-ref-dialogs.html",
}

NAV_SOLUTIONS = re.compile(
    r'\n\s*<a href="solutions-architecture\.html"[^>]*>解决方案</a>'
)

META_0204 = re.compile(r"模块 02 / 04")
META_0304 = re.compile(r"模块 03 / 04")
META_0404 = re.compile(r"模块 04 / 04")


def redirect_page(target: str) -> str:
    label = target.split("#")[0].replace(".html", "")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={target}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>已并入问题论证 · 大模型知识获取研究</title>
  <link rel="canonical" href="{target}">
</head>
<body>
  <p>解决方案内容已并入 <a href="{target}">问题论证</a> 对应页的「解决方案」页签。</p>
</body>
</html>
"""


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text

    text = NAV_SOLUTIONS.sub("", text)

    for old, new in LINK_MAP.items():
        text = text.replace(f'href="{old}"', f'href="{new}"')

    if "data-module=\"problems\"" in text:
        text = META_0204.sub("模块 02 / 03", text)
    if "data-module=\"principles\"" in text:
        text = META_0404.sub("模块 03 / 03", text)

    # 顶栏：问题论证 active 时不再指向 solutions
    text = text.replace(
        '下一模块 →</span>\n        <span class="nav-title">解决方案</span>',
        '下一模块 →</span>\n        <span class="nav-title">亲和原则</span>',
    )
    text = text.replace(
        'href="solutions-architecture.html" class="next"',
        'href="principles-general.html" class="next"',
    )

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    for src, dst in REDIRECTS.items():
        (ROOT / src).write_text(redirect_page(dst), encoding="utf-8")

    changed = 0
    for html in ROOT.glob("**/*.html"):
        if html.name.startswith(".") or "assets/mirror" in str(html):
            continue
        if patch_html(html):
            changed += 1
            print("patched", html.relative_to(ROOT))

    # index 模块卡片
    index = ROOT / "index.html"
    t = index.read_text(encoding="utf-8")
    t = t.replace(
        '<a class="module-card" href="solutions-architecture.html">',
        '<a class="module-card" href="problems-format.html#solution">',
    )
    t = t.replace("模块 03 · 解决方案", "模块 02 · 交付格式（含方案）")
    index.write_text(t, encoding="utf-8")
    print("patched index.html")


if __name__ == "__main__":
    main()
