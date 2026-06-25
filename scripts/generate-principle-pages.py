#!/usr/bin/env python3
"""从 principles-affinity.html 生成 principles-{code}.html 细则页。"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AFFINITY = ROOT / "principles-affinity.html"

# 已有独立页：不覆盖，侧栏仍指向这些文件
EXISTING = {
    "a1": "principles-timeliness.html",
    "a4": "principles-structure-metadata.html",
    "a5": "principles-structure-llms.html",
    "b3": "principles-tab.html",
    "b5": "principles-format.html",
    "c2": "principles-structure-cross.html",
    "c3": "principles-structure-single.html",
    "e1": "principles-image.html",
    "e2": "principles-hotzone.html",
    "e3": "principles-table.html",
    "e4": "principles-code.html",
    "e5": "principles-link.html",
    "e8": "principles-note.html",
}

DOMAIN_BY_CODE = {
    "a": "A. 可发现性",
    "b": "B. 可解析性",
    "c": "C. 可切分性",
    "d": "D. 可理解性",
    "e": "E. 非文本元素语义转译",
    "f": "F. 可溯源性与可信度",
}

ROW_RE = re.compile(
    r'<tr id="principle-([a-f]\d+)">\s*'
    r'(?:<td class="col-dim" rowspan="\d+">[^<]+</td>\s*)?'
    r'<td class="col-id">([A-F]\d+)</td>\s*'
    r"<td>([^<]+)</td>\s*"
    r"<td>(.*?)</td>\s*"
    r"<td>(.*?)</td>\s*"
    r"<td>(.*?)</td>\s*"
    r"</tr>",
    re.S,
)

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · 亲和原则 · 大模型知识获取研究</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="inner-page" data-module="principles" data-page="{code}">

<header class="site-header">
  <div class="site-logo">大模型知识获取研究</div>
  <nav class="site-nav">
    <a href="index.html">首页</a>
    <a href="background-motivation.html">研究概览</a>
    <a href="problems-answer-search.html">问题论证</a>
    <a href="principles-affinity.html" class="active">亲和原则</a>
  </nav>
</header>

<div class="page-wrapper">

  <aside id="module-sidebar"></aside>

  <main class="main-content">

    <div class="page-header">
      <h1>{name}</h1>
      <p class="page-desc">{code_upper} · {domain} · 完整条目见 <a href="principles-affinity.html#principle-{code}">亲和性原则汇总表</a>。</p>
    </div>

    <section class="section" id="solution">
      <h2 id="design">设计侧改造建议</h2>
      <div class="surface-card principle-deliverable">{design}</div>

      <h2 id="content-side">内容侧改造建议</h2>
      <div class="surface-card principle-deliverable">{content}</div>

      <h2 id="code-side">代码侧改造建议</h2>
      <div class="surface-card principle-deliverable">{dev}</div>
    </section>

  </main></div>

<footer class="site-footer">
  模块 03 · 亲和原则 · Ascend C 文档大模型亲和规则研究
</footer>

<script src="assets/js/module-sidebar.js"></script>
</body>
</html>
"""


def cell_html(raw: str) -> str:
    s = raw.strip()
    if not s or s == "—":
        return "<p>—</p>"
    return s


def main() -> None:
    text = AFFINITY.read_text(encoding="utf-8")
    rows = ROW_RE.findall(text)
    if not rows:
        raise SystemExit("未解析到汇总表行")

    created = 0
    for code, _id, name, design, content, dev in rows:
        code = code.lower()
        if code in EXISTING:
            continue
        out = ROOT / f"principles-{code}.html"
        domain = DOMAIN_BY_CODE[code[0]]
        out.write_text(
            TEMPLATE.format(
                title=html.escape(name.strip()),
                code=code,
                code_upper=code.upper(),
                name=html.escape(name.strip()),
                domain=html.escape(domain),
                design=cell_html(design),
                content=cell_html(content),
                dev=cell_html(dev),
            ),
            encoding="utf-8",
        )
        created += 1
        print(f"  {out.name}")

    print(f"已生成 {created} 个细则页（跳过 {len(EXISTING)} 个已有页）")


if __name__ == "__main__":
    main()
