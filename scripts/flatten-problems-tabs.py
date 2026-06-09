#!/usr/bin/env python3
"""Remove content-tabs; stack 问题实测/解决方案 as H2; merge 改进路径 into 改进措施."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

MERGE_H2 = ("改进路径", "全站落地路线图")
CN_NUM = {
    "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
}


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


def rebuild_content_unit(outer, new_inner):
    open_tag = outer[: outer.find(">") + 1]
    indent_match = re.match(r"^(\s*)", inner_html(outer) or " ")
    close_indent = indent_match.group(1) if indent_match else ""
    return f"{open_tag}\n{new_inner}\n{close_indent}</div>"


def iter_content_units(html):
    pos = 0
    while True:
        block = find_div_block(html, "content-unit", pos)
        if not block:
            break
        yield block
        pos = block[1]


def h2_title(inner):
    m = re.search(r"<h2>([^<]+)</h2>", inner)
    return m.group(1).strip() if m else None


def merge_path_into_measures(solution_inner):
    units = list(iter_content_units(solution_inner))
    if not units:
        return solution_inner

    measures_idx = None
    merge_indices = []
    for i, (_, _, outer) in enumerate(units):
        title = h2_title(inner_html(outer))
        if title == "改进措施":
            measures_idx = i
        elif title in MERGE_H2:
            merge_indices.append(i)

    if measures_idx is None or not merge_indices:
        return solution_inner

    new_measures_inner = inner_html(units[measures_idx][2]).rstrip()
    extras = []
    for i in merge_indices:
        body = inner_html(units[i][2])
        body = re.sub(r"^\s*<h2>[^<]+</h2>\s*", "", body, count=1, flags=re.S).strip()
        if body:
            extras.append(body)
    if extras:
        extras = [demote_headings(body, min_level=3) for body in extras]
        new_measures_inner += "\n\n" + "\n\n".join(extras)

    out = solution_inner
    for i in sorted(merge_indices, reverse=True):
        start, end, _ = units[i]
        out = out[:start] + out[end:]
    ms, me, mouter = units[measures_idx]
    out = out[:ms] + rebuild_content_unit(mouter, new_measures_inner) + out[me:]
    return out


def demote_headings(html, min_level=2):
    for level in range(5, min_level - 1, -1):
        new = level + 1
        html = re.sub(rf"</h{level}>", f"</h{new}>", html)
        html = re.sub(rf"<h{level}(\s[^>]*)?>", rf"<h{new}\1>", html)
    return html


def demote_problem_headings(html):
    return demote_headings(html, min_level=2)


def demote_solution_headings(html):
    html = re.sub(r"<h2(\s[^>]*)?>", r"<h3\1>", html)
    html = re.sub(r"</h2>", "</h3>", html)

    def h4_repl(match):
        tag = match.group(0)
        if "badge-priority" in tag or re.search(r"<h4>\d+\.", tag):
            return tag
        return tag.replace("<h4", "<h5", 1).replace("</h4>", "</h5>", 1)

    html = re.sub(r"<h5(\s[^>]*)?>", r"<h6\1>", html)
    html = re.sub(r"</h5>", "</h6>", html)
    html = re.sub(r"<h4(\s[^>]*)?>.*?</h4>", h4_repl, html, flags=re.S)
    return html


def convert_measure_text(text):
    text = text.strip()
    pri_match = re.search(r"(?:（|\()(P0|P1)(?:[^）)]*)?(?:）|\))\s*$", text)
    pri = pri_match.group(1) if pri_match else None
    core = re.sub(r"(?:（|\()(P0|P1)(?:[^）)]*)?(?:）|\))\s*$", "", text).strip()
    num_match = re.match(r"([一二三四五六七八九十]+)、(.+)", core)
    if not num_match:
        return None
    num = CN_NUM.get(num_match.group(1), num_match.group(1))
    title = num_match.group(2).strip()
    if pri:
        badge = "badge-must" if pri == "P0" else "badge-should"
        return (
            f'<h4>{num}. {title} '
            f'<span class="badge badge-priority {badge}">{pri}</span></h4>'
        )
    return f"<h4>{num}. {title}</h4>"


def convert_measures_headings(html):
    units = list(iter_content_units(html))
    for start, end, outer in units:
        inner = inner_html(outer)
        if h2_title(inner) != "改进措施":
            continue

        def repl(m):
            converted = convert_measure_text(m.group(1))
            return converted if converted else m.group(0)

        new_inner = re.sub(
            r"<h3>((?:[一二三四五六七八九十]+、)[^<]*)</h3>",
            repl,
            inner,
        )
        if new_inner != inner:
            html = html[:start] + rebuild_content_unit(outer, new_inner) + html[end:]
        break
    return html


def fix_answer_card_headers(html):
    return re.sub(
        r'(<div class="answer-card-header">\s*)<h5>(.*?)</h5>',
        r"\1<h4>\2</h4>",
        html,
        flags=re.S,
    )


def fix_measures_orphan_h3(html):
    units = list(iter_content_units(html))
    for start, end, outer in units:
        inner = inner_html(outer)
        if not re.search(r"<h3>改进措施</h3>", inner):
            continue

        def repl(match):
            title = re.sub(r"<[^>]+>", "", match.group(1)).strip()
            if title == "改进措施":
                return match.group(0)
            return f"<h4>{match.group(1).strip()}</h4>"

        new_inner = re.sub(r"<h3>((?:[^<]|<(?!/h3>))*)</h3>", repl, inner)
        if new_inner != inner:
            html = html[:start] + rebuild_content_unit(outer, new_inner) + html[end:]
        break
    return html


def post_fix(html):
    html = fix_answer_card_headers(html)
    html = fix_measures_orphan_h3(html)
    return html

    units = list(iter_content_units(html))
    for start, end, outer in units:
        inner = inner_html(outer)
        if ">测试问题</h3>" not in inner and ">测试问题</h2>" not in inner:
            continue
        if "test-prompt-card" in inner:
            continue
        m = re.match(r"^(\s*)<h3>测试问题</h3>\s*(.*)$", inner, re.S)
        if not m:
            m = re.match(r"^(\s*)<h2>测试问题</h2>\s*(.*)$", inner, re.S)
        if not m:
            continue
        indent, body = m.group(1), m.group(2).strip()
        lines = [line.strip() for line in body.split("\n") if line.strip()]
        body_html = "\n".join(f"{indent}  {line}" for line in lines)
        new_inner = (
            f"{indent}<h3>测试问题</h3>\n"
            f'{indent}<div class="test-prompt-card">\n'
            f"{body_html}\n"
            f"{indent}</div>"
        )
        return html[:start] + rebuild_content_unit(outer, new_inner) + html[end:]
    return html


def add_surface_card(html):
    return re.sub(
        r'<div class="source-type-defs">',
        '<div class="source-type-defs surface-card">',
        html,
    )


def clean_section_tag(open_tag):
    tag = re.sub(r'\s+class="[^"]*"', "", open_tag)
    tag = re.sub(r'\s+role="tabpanel"', "", tag)
    tag = re.sub(r'\s+data-tab-panel="[^"]*"', "", tag)
    tag = tag.replace(" hidden", "").replace(' hidden="hidden"', "")
    tag = re.sub(r'\s+is-active', "", tag)
    if 'class="' not in tag:
        tag = tag.replace("<section", '<section class="section"', 1)
    elif 'class="section' not in tag:
        tag = tag.replace('class="', 'class="section ', 1)
    return tag


def extract_panel(html, panel):
    pattern = rf'(<section\b[^>]*\bdata-tab-panel="{panel}"[^>]*>)(.*?)(</section>)'
    m = re.search(pattern, html, re.S)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


def section_id(open_tag):
    m = re.search(r'\bid="([^"]+)"', open_tag)
    return m.group(1) if m else None


def find_section_bounds(html, open_tag):
    sid = section_id(open_tag)
    if not sid:
        return None
    start_m = re.search(rf"<section\b[^>]*\bid=\"{re.escape(sid)}\"[^>]*>", html)
    if not start_m:
        return None
    start = start_m.start()
    depth = 0
    i = start
    while i < len(html):
        sec_open = html.find("<section", i)
        sec_close = html.find("</section>", i)
        if sec_close == -1:
            return None
        if sec_open != -1 and sec_open < sec_close:
            depth += 1
            i = sec_open + 8
            continue
        if depth == 0:
            end = sec_close + len("</section>")
            return start, end, html[start:end]
        depth -= 1
        i = sec_close + len("</section>")
    return None


def find_content_tabs_bounds(html):
    tabs_start = html.find('<div class="content-tabs"')
    if tabs_start == -1:
        return None
    after = html[tabs_start:]
    end_m = re.match(r"(?s).*?</section>\s*</div>\s*</div>", after)
    if not end_m:
        return None
    return tabs_start, tabs_start + end_m.end()


def flatten_already_done(html):
    return "data-content-tabs" not in html and ">问题实测</h2>" in html


def transform(html):
    if "data-content-tabs" not in html:
        return html, False

    problem = extract_panel(html, "problem")
    solution = extract_panel(html, "solution")
    if not problem or not solution:
        return html, False

    bounds = find_content_tabs_bounds(html)
    if not bounds:
        return html, False

    prob_open, prob_inner, prob_close = problem
    sol_open, sol_inner, sol_close = solution

    sol_inner = merge_path_into_measures(sol_inner)
    sol_inner = convert_measures_headings(sol_inner)
    prob_inner = demote_problem_headings(prob_inner)
    sol_inner = demote_solution_headings(sol_inner)
    prob_inner = wrap_test_prompt(prob_inner)
    prob_inner = add_surface_card(prob_inner)

    prob_section = (
        f"{clean_section_tag(prob_open)}\n      <h2>问题实测</h2>\n{prob_inner}    {prob_close}"
    )
    sol_section = (
        f"{clean_section_tag(sol_open)}\n      <h2>解决方案</h2>\n{sol_inner}    {sol_close}"
    )

    t_start, t_end = bounds
    new_html = html[:t_start] + prob_section + "\n\n    " + sol_section + "\n\n" + html[t_end:]
    new_html = re.sub(r'\n<script src="assets/js/content-tabs.js"></script>', "", new_html)
    return new_html, True


def merge_path_in_flat_page(html):
    """Merge 改进路径 into 改进措施 on already-flattened pages (e.g. answer-search)."""
    sol = re.search(
        r'(<section\b[^>]*id="[^"]*-solution"[^>]*>)(.*?)(</section>)',
        html,
        re.S,
    )
    if not sol:
        return html
    open_tag, inner, close = sol.group(1), sol.group(2), sol.group(3)
    new_inner = merge_path_into_measures_flat(inner)
    if new_inner == inner:
        return html
    return html[: sol.start()] + open_tag + new_inner + close + html[sol.end() :]


def merge_path_into_measures_flat(solution_inner):
    units = list(iter_content_units(solution_inner))
    measures_idx = None
    merge_indices = []
    for i, (_, _, outer) in enumerate(units):
        inner = inner_html(outer)
        if re.search(r"<h3>改进措施</h3>", inner):
            measures_idx = i
        elif re.search(r"<h3>(?:改进路径|全站落地路线图)</h3>", inner):
            merge_indices.append(i)

    if measures_idx is None or not merge_indices:
        return solution_inner

    new_measures_inner = inner_html(units[measures_idx][2]).rstrip()
    extras = []
    for i in merge_indices:
        body = inner_html(units[i][2])
        body = re.sub(r"^\s*<h3>[^<]+</h3>\s*", "", body, count=1, flags=re.S).strip()
        if body:
            extras.append(body)
    if extras:
        extras = [demote_headings(body, min_level=3) for body in extras]
        new_measures_inner += "\n\n" + "\n\n".join(extras)

    out = solution_inner
    for i in sorted(merge_indices, reverse=True):
        start, end, _ = units[i]
        out = out[:start] + out[end:]

    ms, me, mouter = units[measures_idx]
    out = out[:ms] + rebuild_content_unit(mouter, new_measures_inner) + out[me:]
    return out


def normalize_page_header(html):
    block = find_div_block(html, "page-header")
    if not block:
        return html
    start, end, outer = block
    inner = inner_html(outer).strip()
    if "page-desc" not in inner and "component-problem" not in inner:
        return html
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
        return html
    header_inner = work.strip()
    new_header = f'<div class="page-header">\n      {header_inner}\n    </div>'
    moved_block = "\n\n    ".join(moved)
    return html[:start] + new_header + "\n\n    " + moved_block + html[end:]


def main():
    paths = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else sorted(ROOT.glob("problems-*.html"))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        original = text
        if "data-content-tabs" in text:
            text = normalize_page_header(text)
            new_text, ok = transform(text)
        else:
            new_text, ok = text, False
        if path.name == "problems-answer-search.html":
            new_text = merge_path_in_flat_page(new_text)
        new_text = post_fix(new_text)
        if ok or new_text != original:
            path.write_text(new_text, encoding="utf-8")
            print("updated", path.name)


if __name__ == "__main__":
    main()
