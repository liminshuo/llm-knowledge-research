#!/usr/bin/env python3
"""Merge 改进路径 scenario tables into h4 measure paragraphs; add action verbs to titles."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

SCENARIO_TABLE = re.compile(
    r'<table class="data-table">\s*'
    r'<thead>\s*<tr><th>场景</th><th>建议</th><th>优先级</th></tr>\s*</thead>\s*'
    r'<tbody>(.*?)</tbody>\s*</table>',
    re.S,
)

ROW_RE = re.compile(
    r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>.*?</td>\s*</tr>',
    re.S,
)

MEASURE_H4 = re.compile(
    r'(<h4>)(\d+\.\s*)(.*?)(</h4>)',
    re.S,
)

VERB_RULES = [
    ("元数据与溯源", "补充"),
    ("元数据", "补充"),
    ("Front Matter", "补充"),
    ("chunk 级", "细化"),
    ("检索池", "承接"),
    ("信源标注", "规范"),
    ("信源", "规范"),
    ("robots.txt", "调整"),
    ("部署 llms", "部署"),
    ("llms.txt", "部署"),
    ("sitemap", "完善"),
    ("canonical", "完善"),
    ("转换管道", "建设"),
    ("知识库集成", "强化"),
    ("版本与元数据", "强化"),
    ("内容侧", "推进"),
    ("图意文本化", "推进"),
    ("链接文本化", "规范"),
    ("热区文本化", "推进"),
    ("代码规范化", "规范"),
    ("Tab 全量", "推进"),
    ("折叠默认", "推进"),
    ("提示类型", "推进"),
    ("表格与列表", "规范"),
    ("双轨交付", "落实"),
    ("架构侧", "落实"),
    ("与双轨", "衔接"),
    ("与转换管道", "衔接"),
    ("与语义", "明确"),
    ("边界", "明确"),
]


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text).strip()


def add_verb(title):
    plain = strip_tags(title)
    for key, verb in VERB_RULES:
        if key in plain:
            if plain.startswith(verb):
                return title
            return title.replace(plain, f"{verb}{plain}", 1)
    if re.match(r"^(补充|落实|推进|规范|部署|调整|完善|建设|强化|衔接|明确|承接)", plain):
        return title
    return title.replace(plain, f"落实{plain}", 1)


def parse_scenario_rows(table_inner):
    rows = []
    for scene, suggestion in ROW_RE.findall(table_inner):
        rows.append((strip_tags(scene), strip_tags(suggestion)))
    return rows


def remove_scenario_table(html):
    return SCENARIO_TABLE.sub("", html).rstrip()


def split_rows(rows, n_measures):
    if not rows or n_measures == 0:
        return [[] for _ in range(n_measures)]
    if len(rows) == n_measures:
        return [[r] for r in rows]
    chunks = [[] for _ in range(n_measures)]
    for i, row in enumerate(rows):
        chunks[min(i * n_measures // len(rows), n_measures - 1)].append(row)
    return chunks


def scenario_prefix(row_groups):
    parts = []
    for scene, suggestion in row_groups:
        parts.append(f"针对<strong>{scene}</strong>：{suggestion}")
    return "；".join(parts) + "。"


def integrate_first_paragraph(block, prefix_text):
    if not prefix_text:
        return block
    match = re.search(r"(<p[^>]*>)(.*?)(</p>)", block, re.S)
    if not match:
        return f"<p>{prefix_text}</p>\n{block}"
    open_tag, body, close_tag = match.group(1), match.group(2).strip(), match.group(3)
    if body.startswith("针对<strong>"):
        return block
    return block.replace(
        match.group(0),
        f"{open_tag}{prefix_text}{body}{close_tag}",
        1,
    )


def process_measures_inner(inner):
    table = SCENARIO_TABLE.search(inner)
    if not table:
        inner = MEASURE_H4.sub(
            lambda m: f"{m.group(1)}{m.group(2)}{add_verb(m.group(3))}{m.group(4)}",
            inner,
        )
        return inner

    rows = parse_scenario_rows(table.group(1))
    inner_wo = remove_scenario_table(inner)

    h4_matches = list(MEASURE_H4.finditer(inner_wo))
    if not h4_matches:
        return inner_wo

    row_groups = split_rows(rows, len(h4_matches))
    out = []
    last = 0
    for i, m in enumerate(h4_matches):
        out.append(inner_wo[last : m.start()])
        title = add_verb(m.group(3))
        out.append(f"{m.group(1)}{m.group(2)}{title}{m.group(4)}")
        seg_start = m.end()
        seg_end = h4_matches[i + 1].start() if i + 1 < len(h4_matches) else len(inner_wo)
        segment = inner_wo[seg_start:seg_end]
        prefix = scenario_prefix(row_groups[i]) if row_groups[i] else ""
        out.append(integrate_first_paragraph(segment, prefix))
        last = seg_end
    out.append(inner_wo[last:])
    return "".join(out)


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


def transform_file(path):
    html = path.read_text(encoding="utf-8")
    if "<h3>改进措施</h3>" not in html:
        return False

    units = list(iter_content_units(html))
    changed = False
    for start, end, outer in units:
        inner = inner_html(outer)
        if "<h3>改进措施</h3>" not in inner:
            continue
        new_inner = process_measures_inner(inner)
        if new_inner != inner:
            html = html[:start] + rebuild_content_unit(outer, new_inner) + html[end:]
            changed = True
        break

    if changed:
        path.write_text(html, encoding="utf-8")
    return changed


def iter_content_units(html):
    pos = 0
    while True:
        block = find_div_block(html, "content-unit", pos)
        if not block:
            break
        yield block
        pos = block[1]


# Hand-tuned replacements for complex pages
CUSTOM = {
    "problems-answer-generate.html": """        <h3>改进措施</h3>
        <h4>1. 承接检索池治理</h4>
        <p>针对<strong>900 未进入生成溯源</strong>：生成质量上限由检索池决定——先落实 <a href="problems-answer-search.html#answer-search-root-cause">检索阶段 · 根因分析</a>（llms.txt、双轨交付、版本 过滤）；检索默认 900 + 生成阶段 version 过滤。</p>
        <h4>2. 补充元数据与溯源 <span class="badge badge-priority badge-must">P0</span></h4>
        <p>针对<strong>脚注仅裸 URL</strong>：chunk 附带 <code>version</code>、<code>doc_id</code>、<code>source_url</code>，生成时默认过滤 900 社区版，脚注回链稳定；输出 <code>doc_id</code> + 人类层/机器层双 URL。详见 <a href="principles-structure-metadata.html">亲和原则 · 元数据字段规范</a>。</p>
        <h4>3. 规范信源标注 <span class="badge badge-priority badge-should">P1</span></h4>
        <p>针对<strong>社区主信源识别失败</strong>：区分昇腾社区官方 / 华为系渠道 / 第三方教程，优先召回 <code>hiascend.com</code> 机器层 chunk，避免 CSDN 教程在「基于官方资料」prompt 下被标为官方。</p>""",
}


def apply_custom(path):
    if path.name not in CUSTOM:
        return False
    html = path.read_text(encoding="utf-8")
    units = list(iter_content_units(html))
    for start, end, outer in units:
        inner = inner_html(outer)
        if "<h3>改进措施</h3>" not in inner:
            continue
        new_inner = CUSTOM[path.name]
        html = html[:start] + rebuild_content_unit(outer, new_inner) + html[end:]
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    paths = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else sorted(ROOT.glob("problems-*.html"))
    for path in paths:
        if path.name == "problems-answer-search.html":
            continue
        if apply_custom(path):
            print("custom", path.name)
            continue
        if transform_file(path):
            print("updated", path.name)


if __name__ == "__main__":
    main()
