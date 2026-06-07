#!/usr/bin/env python3
"""Split problems.html into separate pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "problems.html"
text = SRC.read_text(encoding="utf-8")

# Extract main content between page-header end and page-nav
main_match = re.search(
    r'(<div class="page-header">.*?</div>\s*)(.*?)(\s*<nav class="page-nav">)',
    text,
    re.DOTALL,
)
if not main_match:
    raise SystemExit("Could not parse problems.html")

header_block = main_match.group(1)
all_sections = main_match.group(2)

def extract_section(section_id):
    pattern = rf'(<!-- .*? -->\s*)?<section class="section" id="{section_id}"[^>]*>.*?</section>'
    m = re.search(pattern, all_sections, re.DOTALL)
    return m.group(0) if m else ""

sections = {
    "answer": extract_section("answer-quality"),
    "format": extract_section("page-format"),
    "content": extract_section("content-acquire"),
    "structure": extract_section("structure"),
}

# Detail page: divider + all following sections
detail_start = all_sections.find('<!-- 实测详情分隔 -->')
detail_content = all_sections[detail_start:] if detail_start >= 0 else ""

HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · 当前问题 · 大模型知识获取研究</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="inner-page" data-problems-page="{page_id}">

<header class="site-header">
  <div class="site-logo">大模型知识获取研究</div>
  <nav class="site-nav">
    <a href="index.html">首页</a>
    <a href="background.html">研究背景</a>
    <a href="problems.html" class="active">当前问题</a>
    <a href="solutions.html">解决方案</a>
    <a href="principles.html">亲和原则</a>
  </nav>
</header>

<div class="page-wrapper">

  <aside id="problems-sidebar"></aside>

  <main class="main-content">

    {page_header}
{body}
    {page_nav}

  </main>
</div>

<footer class="site-footer">
  模块 02 · 当前问题 · Ascend C 文档大模型亲和规则研究
</footer>

<script src="assets/js/problems-sidebar.js"></script>
{extra_scripts}
</body>
</html>
'''

PAGES = [
    {
        "file": "problems-answer.html",
        "page_id": "answer",
        "title": "大模型回答侧问题",
        "h1": "大模型回答侧问题",
        "desc": "官方内容占比少、版本滞后——大模型回答侧的两类核心痛点，及与文档亲和改造的关联。",
        "body_key": "answer",
        "prev": ("background.html", "← 上一模块", "研究背景"),
        "next": ("problems-format.html", "下一节 →", "页面形式"),
        "scrollspy": False,
    },
    {
        "file": "problems-format.html",
        "page_id": "format",
        "title": "页面形式",
        "h1": "页面形式",
        "desc": "Markdown vs HTML、.md 后缀误导、同页 .md/.html URL 实测对比——页面交付格式如何影响大模型抓取。",
        "body_key": "format",
        "prev": ("problems-answer.html", "← 上一节", "大模型回答侧问题"),
        "next": ("problems-content.html", "下一节 →", "内容获取"),
        "scrollspy": True,
    },
    {
        "file": "problems-content.html",
        "page_id": "content",
        "title": "内容获取",
        "h1": "内容获取",
        "desc": "按组件类型审视：图片、链接、表格、代码块、注意提示、卡片——大模型能否准确提取各类内容元素。",
        "body_key": "content",
        "prev": ("problems-format.html", "← 上一节", "页面形式"),
        "next": ("problems-structure.html", "下一节 →", "结构感知"),
        "scrollspy": True,
    },
    {
        "file": "problems-structure.html",
        "page_id": "structure",
        "title": "结构感知",
        "h1": "结构感知",
        "desc": "跨文档与单文档结构感知——大模型如何理解文档在知识体系中的位置与页内逻辑结构。",
        "body_key": "structure",
        "prev": ("problems-content.html", "← 上一节", "内容获取"),
        "next": ("problems-detail.html", "下一节 →", "实测详情"),
        "scrollspy": True,
    },
    {
        "file": "problems-detail.html",
        "page_id": "detail",
        "title": "实测详情",
        "h1": "实测详情",
        "desc": "Ascend C 四页文档的抓取实测记录——格式噪声、可抓取/不可抓取内容、端点对比与四页诊断。",
        "body_key": "detail",
        "prev": ("problems-structure.html", "← 上一节", "结构感知"),
        "next": ("solutions.html", "下一模块 →", "解决方案"),
        "scrollspy": True,
    },
]

def page_header(h1, desc):
    return f'''    <div class="page-header">
      <div class="module-label">模块 02 · 当前问题</div>
      <h1>{h1}</h1>
      <p class="page-desc">{desc}</p>
    </div>'''

def page_nav(prev, nxt):
    return ""

bodies = {**sections, "detail": detail_content}

for p in PAGES:
    extra = '<script src="assets/js/sidebar-scrollspy.js"></script>\n' if p["scrollspy"] else ""
    html = HEAD.format(
        title=p["title"],
        page_id=p["page_id"],
        page_header=page_header(p["h1"], p["desc"]),
        body=bodies[p["body_key"]],
        page_nav=page_nav(p["prev"], p["next"]),
        extra_scripts=extra,
    )
    (ROOT / p["file"]).write_text(html, encoding="utf-8")
    print("Wrote", p["file"])

print("Done.")
