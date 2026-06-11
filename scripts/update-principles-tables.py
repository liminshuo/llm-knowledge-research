#!/usr/bin/env python3
"""Sync principles dimension tables with principles-general.html catalog."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

THEAD = """        <thead>
          <tr><th>编号</th><th>UI 改造项</th><th>渲染页呈现要求</th><th>级别</th></tr>
        </thead>"""

# Single source of truth: (file, dimension label, rows)
# Each row: (anchor_id, ui_item, render_requirement, level)
DIMENSIONS: list[tuple[str, str, list[tuple[str, str, str, str]]]] = [
    (
        "principles-timeliness.html",
        "版本外显",
        [
            ("ver-01", "版本徽章", "文章头部（H1 上方或旁侧）展示「CANN 9.0.0」「Ascend C」等版本与产品徽章", "must"),
            ("ver-02", "弃用横幅", "已废弃章节在页顶展示弃用提示，并链接替代文档", "must"),
        ],
    ),
    (
        "principles-image.html",
        "图片图意",
        [
            ("img-ui-label", "可读图片标签", "信息型图片以描述性标签呈现（如「API 层级架构图」），禁止仅显示无意义文件名", "must"),
            ("img-02", "图片内容转写", "复杂图表下方附可见「图片内容转写」段落；成长地图等路径图可用正文有序列表等价呈现节点与关系", "must"),
            ("img-06", "可见图注", "图片下方展示「图1 · …」等图号与图意说明", "should"),
            ("img-ui-mermaid", "Mermaid 呈现", "流程 / 架构类图以 Mermaid 可编辑图替代不可读 PNG", "should"),
            ("img-04", "装饰图标移除", "纯装饰图标从正文移除，信息改由相邻文本承载", "must"),
        ],
    ),
    (
        "principles-hotzone.html",
        "图片热区",
        [
            ("img-03", "热区文本链接列表", "带热区的图片下方展示完整链接列表，覆盖全部热区跳转目标", "must"),
            ("l-04", "描述性热区锚文本", "每个热区链接使用描述性锚文本，禁止「区域1」「点击这里」", "must"),
        ],
    ),
    (
        "principles-link.html",
        "链接语义",
        [
            ("l-01", "描述性锚文本", "链接可见文字描述跳转目标，禁止 LINK 等占位符", "must"),
            ("l-02", "站外来源标注", "站外链接旁附完整域名或来源标识（如 ↗ gitcode.com）", "must"),
            ("l-05", "上下文链接", "链接置于有上下文的句子中，或附用途说明，避免孤立「详情」", "should"),
        ],
    ),
    (
        "principles-tab.html",
        "隐藏语义 · Tab",
        [
            ("tab-02", "Tab 标签可读", "Tab 标签展示场景化文本（如「在线安装 · x86_64 · CANN 9.0.0」），禁止 Tab1/Tab2", "must"),
            ("tab-ui-expand", "Tab 面板全量可见", "各 Tab 面板正文在页面上全量可见，纵向排列或切换时不隐藏非激活项正文", "must"),
        ],
    ),
    (
        "principles-collapse.html",
        "隐藏语义 · 折叠",
        [
            ("coll-02", "折叠标题可读", "折叠区展示有语义的标题文本（如「高级配置参数说明」），禁止空标题占位", "must"),
            ("coll-ui-open", "折叠默认展开", "折叠面板初始展开，步骤与说明在页面上直接可读", "must"),
        ],
    ),
    (
        "principles-code.html",
        "代码语义",
        [
            ("code-02", "行号与代码分离", "行号由样式渲染，代码区不出现表格行号列", "must"),
            ("code-03", "代码块 pre 呈现", "代码块以 <code>pre</code> 区域呈现，不用 highlighttable 表格承载", "must"),
            ("code-04", "代码场景标注", "代码块上方可见文件名、语言与适用场景（如 kernel_add.cpp · Ascend C）", "should"),
        ],
    ),
    (
        "principles-table.html",
        "表格的结构语义",
        [
            ("tbl-01", "可见表题", "表格上方展示「表1 · …」等可见表题", "must"),
            ("tbl-02", "表头语义化", "表头行与数据行视觉区分——表头加粗或使用 TH 样式", "must"),
            ("tbl-03", "代码独立于表格外", "大段代码放在表格外独立代码块，不在单元格内嵌套多行代码", "must"),
        ],
    ),
    (
        "principles-note.html",
        "注意提示（Note）语义",
        [
            ("note-02", "Note 正文展开", "提示正文在页面上完整展示，不折叠、不用 Tooltip 藏字", "must"),
            ("note-03", "类型文本前缀", "移除装饰图标；以「注意：」「警告：」等文字前缀标识类型", "must"),
        ],
    ),
    (
        "principles-structure-metadata.html",
        "元数据字段规范",
        [
            ("h-01", "单一 H1", "渲染页有且仅有一个 H1，与页面主题一致", "must"),
            ("h-02", "标题层级连续", "标题层级连续（H1→H2→H3），大纲结构在页面上清晰可读", "must"),
            ("h-03", "标题文本自解释", "H2/H3 标题文本自解释，避免孤立「概述」「说明」", "should"),
            ("mdm-summary", "文章摘要块", "页头展示 60–120 字摘要，概括主题与适用读者", "must"),
            ("mdm-version", "版本 / 产品徽章", "页头展示 version、product 等版本与产品标识徽章", "must"),
            ("mdm-breadcrumb", "可见面包屑", "页头展示完整 breadcrumb 文本路径", "must"),
            ("mdm-tags", "适用设备标签", "适用芯片 / 算子类别在页头以标签展示", "should"),
        ],
    ),
    (
        "principles-structure-cross.html",
        "跨文档结构感知",
        [
            ("cross-01", "可见面包屑", "展示完整 breadcrumb 路径，消歧同名章节（如两处「环境准备」）", "must"),
            ("cross-02", "上下篇导航", "页脚或文首展示「上一篇 / 下一篇」，锚文本描述目标章节", "must"),
        ],
    ),
    (
        "principles-structure-single.html",
        "单文档结构感知",
        [
            ("single-01", "版式间距规范", "用 CSS 间距控制版式，禁止用空段落 / 空行堆叠作间距", "must"),
            ("single-03", "列表表达步骤", "步骤与层级以有序 / 无序列表呈现，不用多个独立段落模拟列表", "must"),
        ],
    ),
    (
        "principles-format.html",
        "双轨交付与载体",
        [
            ("fmt-link", "机器可读入口", "页脚或工具栏提供「机器可读版本」可见链接，指向 source 或 Markdown 入口", "should"),
        ],
    ),
]

# Sidebar dimensions with no render-page UI rules (catalog omits these; see problems pages)
NO_UI_DIMENSIONS: list[tuple[str, str, str, str, str | None]] = []


# 0-based ui-demo index per rule (when not sequential)
DEMO_INDEX_OVERRIDES: dict[str, dict[str, int]] = {
    "principles-image.html": {
        "img-ui-label": 0,
        "img-02": 1,
        "img-06": 0,
        "img-ui-mermaid": 2,
        "img-04": 3,
    },
}


def demo_index(fname: str, anchor_id: str, anchor_ids: list[str], demo_count: int) -> int:
    if demo_count == 0:
        return 0
    if fname in DEMO_INDEX_OVERRIDES and anchor_id in DEMO_INDEX_OVERRIDES[fname]:
        return DEMO_INDEX_OVERRIDES[fname][anchor_id]
    return min(anchor_ids.index(anchor_id), demo_count - 1)


def link_fragments(fname: str, anchor_ids: list[str]) -> dict[str, str]:
    """Each rule anchor maps to the primary id on its target ui-demo."""
    path = ROOT / fname
    text = path.read_text(encoding="utf-8")
    demo_count = len(re.findall(r'<div class="ui-demo ui-demo--plain"', text))
    if demo_count == 0:
        return {aid: aid for aid in anchor_ids}

    groups: dict[int, list[str]] = defaultdict(list)
    for aid in anchor_ids:
        groups[demo_index(fname, aid, anchor_ids, demo_count)].append(aid)

    primary = {idx: aids[0] for idx, aids in groups.items()}
    return {
        aid: primary[demo_index(fname, aid, anchor_ids, demo_count)]
        for aid in anchor_ids
    }


def anchor_principle_demos(fname: str, anchor_ids: list[str]) -> dict[str, str]:
    path = ROOT / fname
    text = path.read_text(encoding="utf-8")

    for aid in anchor_ids:
        text = re.sub(rf'(<tr)\s+id="{re.escape(aid)}"', r"\1", text)

    demo_count = len(re.findall(r'<div class="ui-demo ui-demo--plain"', text))
    fragments = link_fragments(fname, anchor_ids)

    if demo_count == 0:
        path.write_text(text, encoding="utf-8")
        return fragments

    groups: dict[int, list[str]] = defaultdict(list)
    for aid in anchor_ids:
        groups[demo_index(fname, aid, anchor_ids, demo_count)].append(aid)
    primary_by_idx = {idx: aids[0] for idx, aids in groups.items()}

    text = re.sub(
        r'(<div class="ui-demo ui-demo--plain") id="[^"]*"',
        r"\1",
        text,
    )

    n = [0]

    def add_demo_id(match: re.Match[str]) -> str:
        idx = n[0]
        n[0] += 1
        if idx in primary_by_idx:
            return f'{match.group(1)} id="{primary_by_idx[idx]}"'
        return match.group(1)

    text = re.sub(r'(<div class="ui-demo ui-demo--plain")', add_demo_id, text)
    path.write_text(text, encoding="utf-8")
    return fragments


def badge(level: str) -> str:
    if level == "must":
        return '<span class="badge badge-must">必须</span>'
    return '<span class="badge badge-should">建议</span>'


def rows_html(rows: list[tuple[str, str, str, str]]) -> str:
    lines = ["        <tbody>"]
    for i, (_row_id, name, desc, level) in enumerate(rows, 1):
        lines.append(
            f"          <tr><td>{i}</td><td>{name}</td><td>{desc}</td><td>{badge(level)}</td></tr>"
        )
    lines.append("        </tbody>")
    return "\n".join(lines)


def replace_table(path: Path, rows: list[tuple[str, str, str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    start = text.index('      <table class="data-table">')
    end = text.index("      </table>", start) + len("      </table>")
    new_table = f'      <table class="data-table">\n{THEAD}\n{rows_html(rows)}\n      </table>'
    path.write_text(text[:start] + new_table + text[end:], encoding="utf-8")
    print(f"updated {path.name}")


def catalog_entries() -> list[tuple[str, str, list[tuple[str, str, str, str]] | None]]:
    """Ordered catalog: (href, label, rows) or (href, label, None) for no-UI dimensions."""
    by_file = {fname: (label, rows) for fname, label, rows in DIMENSIONS}
    order = [fname for fname, _, _ in DIMENSIONS]
    entries: list[tuple[str, str, list | None]] = []

    for fname in order:
        label, rows = by_file[fname]
        entries.append((fname, label, rows))
        for no_ui in NO_UI_DIMENSIONS:
            if no_ui[4] == fname:
                entries.append((no_ui[0], no_ui[1], None))

    return entries


def catalog_tbody(link_map: dict[str, dict[str, str]]) -> str:
    lines = ["        <tbody>"]
    for href, label, rows in catalog_entries():
        if rows is None:
            no_ui = next(n for n in NO_UI_DIMENSIONS if n[0] == href)
            _, _, problems_href, problems_label, _ = no_ui
            lines.append("          <tr>")
            lines.append(f"            <td>{label}</td>")
            lines.append(
                f'            <td colspan="2">无渲染页 UI 改造项 → 见 <a href="{problems_href}">{problems_label}</a></td>'
            )
            lines.append("          </tr>")
            continue

        span = len(rows)
        fragments = link_map.get(href, {})
        for j, (anchor_id, name, desc, _level) in enumerate(rows):
            dim_cell = f'<td rowspan="{span}">{label}</td>' if j == 0 else ""
            fragment = fragments.get(anchor_id, anchor_id)
            lines.append("          <tr>")
            if dim_cell:
                lines.append(f"            {dim_cell}")
            lines.append(f'            <td><a href="{href}#{fragment}">{name}</a></td>')
            lines.append(f"            <td>{desc}</td>")
            lines.append("          </tr>")

    lines.append("        </tbody>")
    return "\n".join(lines)


def update_catalog(link_map: dict[str, dict[str, str]]) -> None:
    path = ROOT / "principles-general.html"
    text = path.read_text(encoding="utf-8")
    thead = """        <thead>
          <tr><th>维度</th><th>UI 改造项</th><th>渲染页呈现要求</th></tr>
        </thead>"""
    start = text.index('      <table class="data-table">')
    end = text.index("      </table>", start) + len("      </table>")
    new_table = f'      <table class="data-table">\n{thead}\n{catalog_tbody(link_map)}\n      </table>'
    path.write_text(text[:start] + new_table + text[end:], encoding="utf-8")
    print("updated principles-general.html")


def verify(link_map: dict[str, dict[str, str]]) -> None:
    errors: list[str] = []
    for fname, _label, rows in DIMENSIONS:
        path = ROOT / fname
        if not path.exists():
            errors.append(f"missing file: {fname}")
            continue
        text = path.read_text(encoding="utf-8")
        fragments = link_map.get(fname, {})
        for row_id, name, _desc, _level in rows:
            fragment = fragments.get(row_id, row_id)
            if f'id="{fragment}"' not in text:
                errors.append(f"{fname}: missing demo anchor {fragment} ({name})")

    if errors:
        raise SystemExit("verify failed:\n" + "\n".join(errors))
    print(f"verified {len(DIMENSIONS)} dimension pages, {sum(len(r) for _, _, r in DIMENSIONS)} rules")


def main() -> None:
    link_map: dict[str, dict[str, str]] = {}
    for fname, _, rows in DIMENSIONS:
        anchor_ids = [r[0] for r in rows]
        replace_table(ROOT / fname, rows)
        link_map[fname] = anchor_principle_demos(fname, anchor_ids)
    update_catalog(link_map)
    verify(link_map)


if __name__ == "__main__":
    main()
