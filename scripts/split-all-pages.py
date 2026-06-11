#!/usr/bin/env python3
"""Split all module pages: one sidebar menu item = one HTML page.

DEPRECATED — NAV / page IA in this script is out of sync with
assets/js/module-sidebar.js. Do not run without a full review and merge.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADER_NAV = {
    "background": ("background-motivation.html", "研究概览"),
    "problems": ("problems-answer.html", "问题论证"),
    "solutions": ("solutions-architecture.html", "解决方案"),
    "principles": ("principles-general.html", "亲和原则"),
}

MODULE_META = {
    "background": ("模块 01 · 研究概览", "01"),
    "problems": ("模块 02 · 问题论证", "02"),
    "solutions": ("模块 03 · 解决方案", "03"),
    "principles": ("模块 04 · 亲和原则", "04"),
}


def extract_sections(html: str) -> dict[str, str]:
    pattern = re.compile(
        r'<section class="section" id="([^"]+)"[^>]*>(.*?)</section>',
        re.DOTALL,
    )
    return {m.group(1): m.group(0) for m in pattern.finditer(html)}


def split_section_by_headings(section_html: str, headings: list[tuple[str, str]]) -> dict[str, str]:
    """Split section inner content by h3/h4 id markers. headings: [(tag, id), ...]"""
    inner = re.sub(r"^<section[^>]*>|</section>$", "", section_html.strip(), flags=re.DOTALL)
    inner = re.sub(r"^\s*<h2>[^<]*</h2>\s*", "", inner, count=1, flags=re.DOTALL)
    inner = re.sub(r"^\s*<p>[^<]*(?:<(?!/p>)[^>]*>[^<]*)*</p>\s*", "", inner, count=1, flags=re.DOTALL)

    parts: dict[str, str] = {}
    for i, (tag, hid) in enumerate(headings):
        pat = rf'<{tag}\s+id="{re.escape(hid)}"[^>]*>'
        m = re.search(pat, inner)
        if not m:
            raise ValueError(f"Heading {tag}#{hid} not found")
        start = m.start()
        if i + 1 < len(headings):
            ntag, nhid = headings[i + 1]
            npat = rf'<{ntag}\s+id="{re.escape(nhid)}"[^>]*>'
            nm = re.search(npat, inner[start + 1 :])
            end = start + 1 + nm.start() if nm else len(inner)
        else:
            end = len(inner)
        chunk = inner[start:end].strip()
        title_m = re.match(rf"<{tag}[^>]*>(.*?)</{tag}>", chunk, re.DOTALL)
        title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else hid
        body = re.sub(rf"^<{tag}[^>]*>.*?</{tag}>\s*", "", chunk, count=1, flags=re.DOTALL)
        parts[hid] = (title, body)
    return parts


def section_page(section_html: str, page_id: str) -> str:
    html = re.sub(r'id="[^"]+"', f'id="{page_id}"', section_html, count=1)
    html = re.sub(r"<h2>[^<]*</h2>\s*", "", html, count=1)
    return f"    {html.strip()}"


def intro_page(intro_html: str, page_id: str) -> str:
    return f'    <section class="section" id="{page_id}">\n{intro_html.strip()}\n    </section>'


def heading_page(title: str, body: str, page_id: str, heading_tag: str = "h2") -> str:
    return (
        f'    <section class="section" id="{page_id}">\n'
        f"      <{heading_tag}>{title}</{heading_tag}>\n"
        f"{body.strip()}\n"
        f"    </section>"
    )


def page_nav(prev_href, prev_label, prev_title, next_href, next_label, next_title):
    return ""


def render_page(
    *,
    module: str,
    page_id: str,
    filename: str,
    title: str,
    desc: str,
    body: str,
    prev: tuple[str, str, str],
    nxt: tuple[str, str, str],
):
    mod_label, _mod_num = MODULE_META[module]
    module_label_html = ""

    nav_order = [
        ("index.html", "首页", None),
        ("background", "研究概览", HEADER_NAV["background"][0]),
        ("problems", "问题论证", HEADER_NAV["problems"][0]),
        ("solutions", "解决方案", HEADER_NAV["solutions"][0]),
        ("principles", "亲和原则", HEADER_NAV["principles"][0]),
    ]
    nav_links = []
    for key, name, href in nav_order:
        if key == "index.html":
            nav_links.append(f'    <a href="index.html">首页</a>')
        else:
            active = ' class="active"' if key == module else ""
            nav_links.append(f'    <a href="{href}"{active}>{name}</a>')

    is_wide = module == "background"
    body_tag_attrs = (
        ""
        if is_wide
        else f' class="inner-page" data-module="{module}" data-page="{page_id}"'
    )
    sidebar_html = "" if is_wide else "  <aside id=\"module-sidebar\"></aside>\n\n"
    main_class = "main-content content-wide" if is_wide else "main-content"
    sidebar_script = "" if is_wide else '\n<script src="assets/js/module-sidebar.js"></script>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · {mod_label.split(" · ")[1]} · 大模型知识获取研究</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body{body_tag_attrs}>

<header class="site-header">
  <div class="site-logo">大模型知识获取研究</div>
  <nav class="site-nav">
{chr(10).join(nav_links)}
  </nav>
</header>

<div class="page-wrapper">

{sidebar_html}  <main class="{main_class}">

    <div class="page-header">
{module_label_html}      <h1>{title}</h1>
{("      <p class=\"page-desc\">" + desc + "</p>\n") if desc else ""}    </div>

{body}

{page_nav(prev[0], prev[1], prev[2], nxt[0], nxt[1], nxt[2])}

  </main>
</div>

<footer class="site-footer">
  {mod_label} · Ascend C 文档大模型亲和规则研究
</footer>
{sidebar_script}
</body>
</html>
"""
    (ROOT / filename).write_text(html, encoding="utf-8")


def redirect_page(old_name: str, target: str):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <script>location.replace('{target}');</script>
</head>
<body></body>
</html>
"""
    (ROOT / old_name).write_text(html, encoding="utf-8")


def chain_pages(pages: list[dict], module: str):
    for i, p in enumerate(pages):
        if i == 0:
            prev = p.get("prev_module", ("index.html", "← 返回", "研究首页"))
        else:
            prev = (pages[i - 1]["file"], "← 上一页", pages[i - 1]["title"])

        if i == len(pages) - 1:
            nxt = p.get("next_module", ("index.html", "返回首页 →", "研究首页"))
        else:
            nxt = (pages[i + 1]["file"], "下一页 →", pages[i + 1]["title"])

        render_page(
            module=module,
            page_id=p["id"],
            filename=p["file"],
            title=p["title"],
            desc=p["desc"],
            body=p["body"],
            prev=prev,
            nxt=nxt,
        )


def build_background():
    sections = extract_sections((ROOT / "background.html").read_text(encoding="utf-8"))
    defs = [
        ("motivation", "研究概览", ""),
    ]
    pages = []
    for pid, title, desc in defs:
        pages.append({
            "id": pid,
            "file": f"background-{pid}.html",
            "title": title,
            "desc": desc,
            "body": section_page(sections[pid], pid),
        })
    pages[0]["prev_module"] = ("index.html", "← 返回", "研究首页")
    pages[-1]["next_module"] = ("problems-answer.html", "下一模块 →", "问题论证")
    chain_pages(pages, "background")


def build_solutions():
    sections = extract_sections((ROOT / "solutions.html").read_text(encoding="utf-8"))
    defs = [
        ("architecture", "双轨交付架构", "同源双发——人类渲染页与机器消费层并行交付。"),
        ("format-priority", "格式优先级", "Markdown、源 HTML、渲染页的优先级建议。"),
        ("light-ia", "轻量 IA 方案", "模型所需的最小信息架构元数据。"),
        ("pipeline", "转换管道", "HTML → Markdown 转换管道设计。"),
        ("roadmap", "落地路线图", "三阶段改造落地路线。"),
        ("metadata", "元数据模板", "Front Matter 元数据模板与字段说明。"),
        ("kb-integration", "知识库集成", "知识库与大模型集成方案。"),
        ("ref-dialogs", "参考对话", "本章相关 Claude 探索对话链接。"),
    ]
    pages = []
    for pid, title, desc in defs:
        pages.append({
            "id": pid,
            "file": f"solutions-{pid}.html",
            "title": title,
            "desc": desc,
            "body": section_page(sections[pid], pid),
        })
    pages[0]["prev_module"] = ("problems-detail-ref-dialogs.html", "← 上一模块", "问题论证")
    pages[-1]["next_module"] = ("principles-general.html", "下一模块 →", "亲和原则")
    chain_pages(pages, "solutions")


def build_principles():
    sections = extract_sections((ROOT / "principles.html").read_text(encoding="utf-8"))
    defs = [
        ("general", "总原则", "文档大模型亲和改造的总原则与基本立场。"),
        ("heading", "标题", "H1–H6 标题组件的亲和规则。"),
        ("link", "链接", "站内/站外链接的文本化与冗余要求。"),
        ("image", "图片", "示意图 alt 与热区文本化规则。"),
        ("table", "表格", "数据表格的结构化与 caption 要求。"),
        ("code", "代码块", "代码块语言标注与行号分离。"),
        ("note", "注意提示", "注意/警告/提示的类型结构化。"),
        ("tab", "Tab 切换", "Tab 面板的全量文本输出。"),
        ("collapse", "折叠面板", "折叠内容的默认可抓取。"),
        ("tensor", "复杂内容：静态 Tensor", "静态 Tensor 编程内容的解读与转写。"),
        ("cheatsheet", "速查表", "九类组件规则速查。"),
        ("ref-dialogs", "参考对话", "本章相关 Claude 探索对话链接。"),
    ]
    pages = []
    for pid, title, desc in defs:
        pages.append({
            "id": pid,
            "file": f"principles-{pid}.html",
            "title": title,
            "desc": desc,
            "body": section_page(sections[pid], pid),
        })
    pages[0]["prev_module"] = ("solutions-ref-dialogs.html", "← 上一模块", "解决方案")
    pages[-1]["next_module"] = ("index.html", "返回首页 →", "研究首页")
    chain_pages(pages, "principles")


def build_problems():
    answer_sec = extract_sections((ROOT / "problems-answer.html").read_text(encoding="utf-8"))["answer-quality"]
    format_sec = extract_sections((ROOT / "problems-format.html").read_text(encoding="utf-8"))["page-format"]
    content_sec = extract_sections((ROOT / "problems-content.html").read_text(encoding="utf-8"))["content-acquire"]
    structure_sec = extract_sections((ROOT / "problems-structure.html").read_text(encoding="utf-8"))["structure"]
    detail_secs = extract_sections((ROOT / "problems-detail.html").read_text(encoding="utf-8"))

    format_intro = re.search(
        r"(<h2>页面形式</h2>\s*<p>.*?</p>)", format_sec, re.DOTALL
    ).group(1)

    format_parts = split_section_by_headings(
        format_sec,
        [
            ("h3", "format-md-vs-html"),
            ("h3", "format-md-suffix"),
            ("h3", "format-md-vs-html-url"),
            ("h4", "page-format-compare"),
        ],
    )

    content_intro = re.search(
        r"(<h2>内容获取</h2>\s*<p>.*?</p>)", content_sec, re.DOTALL
    ).group(1)

    content_parts = split_section_by_headings(
        content_sec,
        [
            ("h3", "content-image"),
            ("h3", "content-link"),
            ("h3", "content-table"),
            ("h3", "content-code"),
            ("h3", "content-note"),
            ("h3", "content-card"),
        ],
    )

    structure_intro = re.search(
        r"(<h2>结构感知</h2>\s*<p>.*?</p>)", structure_sec, re.DOTALL
    ).group(1)

    structure_parts = split_section_by_headings(
        structure_sec,
        [("h3", "structure-cross"), ("h3", "structure-single")],
    )

    detail_defs = [
        ("detail-format", "format", "格式与噪声", "Nuxt SPA 渲染页的信噪比与机器抓取噪声问题。"),
        ("detail-can-capture", "can-capture", "能抓取的内容", "源 HTML 端点下可较准确获取的内容类型。"),
        ("detail-cannot-capture", "cannot-capture", "不能抓取的内容", "热区、Tab、行号污染等难以准确抓取的内容。"),
        ("detail-endpoint", "endpoint", "端点对比", "渲染页与源 HTML 两个端点的抓取质量对比。"),
        ("detail-ia-problem", "ia-problem", "IA 理解问题", "模型理解文档信息架构的深度与噪声权衡。"),
        ("detail-diagnosis", "diagnosis", "四页诊断", "四页文档抓取完整度与优先改造项。"),
        ("detail-content-compare", "content-compare", "内容对比分析", "人类可见内容与模型抓取结果的系统性差异。"),
        ("detail-ref-dialogs", "ref-dialogs", "参考对话", "本章相关 Claude 探索对话链接。"),
    ]

    pages = []

    pages.append({
        "id": "answer",
        "file": "problems-answer.html",
        "title": "官方信源感知弱",
        "desc": "官方内容占比少、版本滞后——大模型难以稳定发现、抓取并引用昇腾社区权威信源。",
        "body": section_page(answer_sec, "answer"),
    })

    pages.append({
        "id": "format",
        "file": "problems-format.html",
        "title": "页面形式",
        "desc": "页面交付格式如何影响大模型抓取的成本、噪声与效率。",
        "body": intro_page(format_intro, "format"),
    })

    format_menu = [
        ("format-md-vs-html", "Markdown vs HTML", "纯 Markdown 与 HTML 渲染页在知识获取场景下的对比。"),
        ("format-md-suffix", ".md 后缀 ≠ Markdown", "社区 .md URL 与纯 Markdown 源文件的本质区别。"),
        ("format-md-vs-html-url", ".md vs .html 实测", "同一页面两种 URL 在昇腾社区实测下的差异。"),
        ("page-format-compare", "抓取对照详表", "「什么是 Ascend C」页面 .md / .html 抓取结果对照。"),
    ]
    for hid, title, desc in format_menu:
        htag = "h4" if hid == "page-format-compare" else "h3"
        ft, body = format_parts[hid]
        pages.append({
            "id": hid,
            "file": f"problems-{hid}.html",
            "title": title,
            "desc": desc,
            "body": heading_page(ft, body, hid, "h2"),
        })

    pages.append({
        "id": "content",
        "file": "problems-content.html",
        "title": "内容获取",
        "desc": "按组件类型审视大模型能否准确提取页面中的各类内容元素。",
        "body": intro_page(content_intro, "content"),
    })

    content_menu = [
        ("content-image", "图片图意", "信息型图片、热区与成长地图的抓取问题。"),
        ("content-link", "链接", "站内链接、占位符与导航污染。"),
        ("content-table", "表格", "标准数据表格与 highlighttable 误用。"),
        ("content-code", "代码块", "行号污染、语言标注与 Tab 隐藏。"),
        ("content-note", "注意提示", "note 正文可抓但类型语义缺失。"),
        ("content-card", "卡片", "Tab 切换与折叠面板的可见性差异。"),
    ]
    for hid, title, desc in content_menu:
        ht, body = content_parts[hid]
        pages.append({
            "id": hid,
            "file": f"problems-{hid}.html",
            "title": title,
            "desc": desc,
            "body": heading_page(ht, body, hid, "h2"),
        })

    pages.append({
        "id": "structure",
        "file": "problems-structure.html",
        "title": "结构感知",
        "desc": "跨文档与单文档结构感知——知识体系位置与页内逻辑结构。",
        "body": intro_page(structure_intro, "structure"),
    })

    for hid, title, desc in [
        ("structure-cross", "跨文档结构感知", "breadcrumb、版本消歧与章节间跳转。"),
        ("structure-single", "单文档结构感知", "标题层级、Tab 扁平化与切片边界。"),
    ]:
        ht, body = structure_parts[hid]
        pages.append({
            "id": hid,
            "file": f"problems-{hid}.html",
            "title": title,
            "desc": desc,
            "body": heading_page(ht, body, hid, "h2"),
        })

    for page_id, sec_id, title, desc in detail_defs:
        pages.append({
            "id": page_id,
            "file": f"problems-{page_id}.html",
            "title": title,
            "desc": desc,
            "body": section_page(detail_secs[sec_id], page_id),
        })

    pages[0]["prev_module"] = ("background-motivation.html", "← 上一模块", "研究概览")
    pages[-1]["next_module"] = ("solutions-architecture.html", "下一模块 →", "解决方案")
    chain_pages(pages, "problems")


def write_module_sidebar_js():
    nav = {
        "background": [],
        "problems": [
            {
                "group": None,
                "id": "answer",
                "href": "problems-answer.html",
                "label": "官方信源感知弱",
            },
            {"group": "问题维度", "id": "format", "href": "problems-format.html", "label": "页面形式"},
            {"group": None, "id": "format-md-vs-html", "href": "problems-format-md-vs-html.html", "label": "Markdown vs HTML"},
            {"group": None, "id": "format-md-suffix", "href": "problems-format-md-suffix.html", "label": ".md 后缀 ≠ Markdown"},
            {"group": None, "id": "format-md-vs-html-url", "href": "problems-format-md-vs-html-url.html", "label": ".md vs .html 实测"},
            {"group": None, "id": "page-format-compare", "href": "problems-page-format-compare.html", "label": "抓取对照详表"},
            {"group": None, "id": "content", "href": "problems-content.html", "label": "内容获取"},
            {"group": None, "id": "content-image", "href": "problems-content-image.html", "label": "图片图意"},
            {"group": None, "id": "content-link", "href": "problems-content-link.html", "label": "链接"},
            {"group": None, "id": "content-table", "href": "problems-content-table.html", "label": "表格"},
            {"group": None, "id": "content-code", "href": "problems-content-code.html", "label": "代码块"},
            {"group": None, "id": "content-note", "href": "problems-content-note.html", "label": "注意提示"},
            {"group": None, "id": "content-card", "href": "problems-content-card.html", "label": "卡片"},
            {"group": None, "id": "structure", "href": "problems-structure.html", "label": "结构感知"},
            {"group": None, "id": "structure-cross", "href": "problems-structure-cross.html", "label": "跨文档结构感知"},
            {"group": None, "id": "structure-single", "href": "problems-structure-single.html", "label": "单文档结构感知"},
            {"group": "实测详情", "id": "detail-format", "href": "problems-detail-format.html", "label": "格式与噪声"},
            {"group": None, "id": "detail-can-capture", "href": "problems-detail-can-capture.html", "label": "能抓取的内容"},
            {"group": None, "id": "detail-cannot-capture", "href": "problems-detail-cannot-capture.html", "label": "不能抓取的内容"},
            {"group": None, "id": "detail-endpoint", "href": "problems-detail-endpoint.html", "label": "端点对比"},
            {"group": None, "id": "detail-ia-problem", "href": "problems-detail-ia-problem.html", "label": "IA 理解问题"},
            {"group": None, "id": "detail-diagnosis", "href": "problems-detail-diagnosis.html", "label": "四页诊断"},
            {"group": None, "id": "detail-content-compare", "href": "problems-detail-content-compare.html", "label": "内容对比分析"},
            {"group": None, "id": "detail-ref-dialogs", "href": "problems-detail-ref-dialogs.html", "label": "参考对话"},
        ],
        "solutions": [
            {"group": None, "id": "architecture", "href": "solutions-architecture.html", "label": "双轨交付架构"},
            {"group": None, "id": "format-priority", "href": "solutions-format-priority.html", "label": "格式优先级"},
            {"group": None, "id": "light-ia", "href": "solutions-light-ia.html", "label": "轻量 IA 方案"},
            {"group": None, "id": "pipeline", "href": "solutions-pipeline.html", "label": "转换管道"},
            {"group": None, "id": "roadmap", "href": "solutions-roadmap.html", "label": "落地路线图"},
            {"group": None, "id": "metadata", "href": "solutions-metadata.html", "label": "元数据模板"},
            {"group": None, "id": "kb-integration", "href": "solutions-kb-integration.html", "label": "知识库集成"},
            {"group": None, "id": "ref-dialogs", "href": "solutions-ref-dialogs.html", "label": "参考对话"},
        ],
        "principles": [
            {"group": None, "id": "general", "href": "principles-general.html", "label": "总原则"},
            {"group": None, "id": "heading", "href": "principles-heading.html", "label": "标题"},
            {"group": None, "id": "link", "href": "principles-link.html", "label": "链接"},
            {"group": None, "id": "image", "href": "principles-image.html", "label": "图片"},
            {"group": None, "id": "table", "href": "principles-table.html", "label": "表格"},
            {"group": None, "id": "code", "href": "principles-code.html", "label": "代码块"},
            {"group": None, "id": "note", "href": "principles-note.html", "label": "注意提示"},
            {"group": None, "id": "tab", "href": "principles-tab.html", "label": "Tab 切换"},
            {"group": None, "id": "collapse", "href": "principles-collapse.html", "label": "折叠面板"},
            {"group": None, "id": "tensor", "href": "principles-tensor.html", "label": "复杂内容：静态 Tensor"},
            {"group": None, "id": "cheatsheet", "href": "principles-cheatsheet.html", "label": "速查表"},
            {"group": None, "id": "ref-dialogs", "href": "principles-ref-dialogs.html", "label": "参考对话"},
        ],
    }

    lines = [
        "/** 全站模块侧栏：一项一页，无锚点导航 */",
        "(function () {",
        "  var NAV = " + __import__("json").dumps(nav, ensure_ascii=False, indent=2) + ";",
        "",
        "  var module = document.body.getAttribute('data-module');",
        "  var page = document.body.getAttribute('data-page');",
        "  var items = NAV[module];",
        "  var aside = document.getElementById('module-sidebar');",
        "  if (!aside) return;",
        "  if (!items || items.length <= 1) {",
        "    aside.remove();",
        "    return;",
        "  }",
        "",
        "  var html = '<div class=\"sidebar-title\">本章导航</div><ul class=\"sidebar-nav\">';",
        "  var lastGroup = null;",
        "  items.forEach(function (item) {",
        "    if (item.group && item.group !== lastGroup) {",
        "      html += '<li class=\"nav-group-label\">' + item.group + '</li>';",
        "      lastGroup = item.group;",
        "    }",
        "    var active = item.id === page ? ' class=\"active\"' : '';",
        "    html += '<li><a href=\"' + item.href + '\"' + active + '>' + item.label + '</a></li>';",
        "    if (item.children && item.children.length) {",
        "      html += '<ul class=\"sub-nav\">';",
        "      item.children.forEach(function (child) {",
        "        var ext = child.external ? ' target=\"_blank\" rel=\"noopener\"' : '';",
        "        var childActive = child.id && child.id === page ? ' class=\"active\"' : '';",
        "        html += '<li><a href=\"' + child.href + '\"' + ext + childActive + '>— ' + child.label + '</a></li>';",
        "      });",
        "      html += '</ul>';",
        "    }",
        "  });",
        "  html += '</ul>';",
        "",
        "  aside.className = 'sidebar';",
        "  aside.innerHTML = html;",
        "})();",
        "",
    ]
    (ROOT / "assets/js/module-sidebar.js").write_text("\n".join(lines), encoding="utf-8")


def main():
    build_background()
    build_problems()
    build_solutions()
    build_principles()
    write_module_sidebar_js()

    redirect_page("background.html", "background-motivation.html")
    redirect_page("solutions.html", "solutions-architecture.html")
    redirect_page("principles.html", "principles-general.html")
    redirect_page("problems.html", "problems-answer.html")

    # remove obsolete files
    for f in [
        "assets/js/problems-sidebar.js",
        "assets/js/sidebar-scrollspy.js",
        "problems-detail.html",
    ]:
        p = ROOT / f
        if p.exists():
            p.unlink()

    print("Generated all pages.")


if __name__ == "__main__":
    main()
