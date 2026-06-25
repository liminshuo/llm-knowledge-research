#!/usr/bin/env python3
"""从 亲和原则汇总.xlsx 生成 principles-affinity.html 表格 tbody。"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XLSX = Path.home() / "Downloads" / "亲和原则汇总.xlsx"
HTML = ROOT / "principles-affinity.html"
TBODY_SNIPPET = ROOT / "scripts" / "_affinity_tbody.html"
TASK_RE = re.compile(r"^([A-F]\d+)\.\s*(.+)$")


def split_task(task: str):
    s = str(task).strip()
    m = TASK_RE.match(s)
    if m:
        return m.group(1), m.group(2)
    return "—", s


def fmt_cell(text):
    if text is None:
        return "—"
    s = str(text).strip()
    if not s:
        return "—"
    return "<br>".join(html.escape(line.strip()) for line in s.split("\n") if line.strip())


PROBLEMS_SOURCE = {
    "A5", "A1", "A2", "A4", "B2", "B3", "B4", "B5", "C3",
    "E1", "E2", "E3", "E4", "E5", "E6", "E8", "F4",
}


def fmt_source_cell(code: str, source=None) -> str:
    if source is not None and str(source).strip():
        label = html.escape(str(source).strip())
        kind = "problems" if label == "问题论证" else "content"
        return f'            <td class="col-source"><span class="affinity-source affinity-source--{kind}">{label}</span></td>'
    if code in PROBLEMS_SOURCE:
        return '            <td class="col-source"><span class="affinity-source affinity-source--problems">问题论证</span></td>'
    return '            <td class="col-source"><span class="affinity-source affinity-source--content">内容侧输入</span></td>'

    import openpyxl

    ws = openpyxl.load_workbook(xlsx, data_only=True).active
    rows = []
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 8)]
        if any(vals):
            rows.append(vals)

    lines = []
    i = 0
    while i < len(rows):
        group = rows[i][0]
        j = i + 1
        while j < len(rows) and rows[j][0] == group:
            j += 1
        span = j - i
        for k in range(span):
            domain, task, priority, design, content, dev, source = (
                list(rows[i + k]) + [None] * 7
            )[:7]
            parts = ["          <tr>"]
            if k == 0:
                parts.append(
                    f'            <td class="col-dim" rowspan="{span}">{html.escape(str(domain))}</td>'
                )
            code, name = split_task(task)
            parts.extend(
                [
                    f'            <td class="col-id">{html.escape(code)}</td>',
                    f"            <td>{html.escape(name)}</td>",
                    f"            <td>{fmt_cell(design)}</td>",
                    f"            <td>{fmt_cell(content)}</td>",
                    f"            <td>{fmt_cell(dev)}</td>",
                    fmt_source_cell(code, source),
                    "          </tr>",
                ]
            )
            lines.append("\n".join(parts))
        i = j
    return "\n".join(lines)


def patch_html(tbody: str) -> None:
    text = HTML.read_text(encoding="utf-8")
    text = re.sub(r"<tbody>.*?</tbody>", "<tbody>\n" + tbody + "\n        </tbody>", text, count=1, flags=re.S)
    HTML.write_text(text, encoding="utf-8")


def main() -> None:
    xlsx = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_XLSX
    if not xlsx.is_file():
        sys.exit(f"找不到 Excel：{xlsx}")
    tbody = build_tbody(xlsx)
    TBODY_SNIPPET.write_text(tbody, encoding="utf-8")
    patch_html(tbody)
    print(f"已更新 {HTML}（{tbody.count('<tr>')} 行）")


if __name__ == "__main__":
    main()
