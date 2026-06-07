#!/usr/bin/env python3
"""Batch-apply UI system conventions to top-level HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"assets", "scripts", "references", "docs"}

NAV_PATTERNS = (
    ('<a href="problems-answer.html">当前问题</a>', '<a href="problems-answer-search.html">当前问题</a>'),
    ('<a href="problems-answer.html" class="active">当前问题</a>', '<a href="problems-answer-search.html" class="active">当前问题</a>'),
)

DETAIL_NESTED = re.compile(
    r'<section class="section" id="detail-[^"]+">\s*<section class="section" id="[^"]+">',
    re.MULTILINE,
)

SECTION_H3_TITLES = {
    "general": "原则一览",
    "heading": "标题规则",
    "link": "链接规则",
    "image": "图片规则",
    "table": "表格规则",
    "code": "代码块规则",
    "note": "注意提示规则",
    "tab": "Tab 规则",
    "collapse": "折叠面板规则",
    "tensor": "Tensor 规则",
    "cheatsheet": "速查说明",
    "architecture": "架构说明",
    "format-priority": "优先级说明",
    "light-ia": "方案说明",
    "pipeline": "管道说明",
    "metadata": "模板说明",
    "kb-integration": "集成说明",
    "format": "格式说明",
    "structure": "结构说明",
    "efficiency-noise": "噪声说明",
    "efficiency-shell": "壳层说明",
    "format-endpoint": "端点对比",
    "structure-llms": "入口说明",
    "structure-metadata": "字段说明",
    "timeliness": "结论",
    "timeliness-disambiguation": "结论",
    "answer": "主题入口",
    "answer-generate": "结论",
}


def should_process(path: Path) -> bool:
    if path.name in {"ui-system.html"}:
        return True
    parts = path.relative_to(ROOT).parts
    return len(parts) == 1 and path.suffix == ".html"


def inject_site_meta_ui_link(content: str, filename: str) -> str:
    if 'href="ui-system.html">UI 规范</a>' in content:
        if filename == "ui-system.html":
            return content.replace(
                '<a href="ui-system.html">UI 规范</a>',
                '<a href="ui-system.html" class="is-active">UI 规范</a>',
                1,
            )
        return content

    return re.sub(r'\n  <div class="site-meta">.*?</div>', "", content, count=1)


def fix_nav(content: str, filename: str) -> str:
    if filename == "problems-answer.html":
        return content.replace(
            '<a href="problems-answer-search.html" class="active">当前问题</a>',
            '<a href="problems-answer.html" class="active">当前问题</a>',
        )
    for old, new in NAV_PATTERNS:
        content = content.replace(old, new)
    return content


def add_module_label_motivation(content: str) -> str:
    if 'background-motivation.html' not in str(content):
        return content
    marker = '<div class="page-header">\n      <h1>研究概览</h1>'
    replacement = (
        '<div class="page-header">\n'
        '      <div class="module-label">模块 01 · 研究概览</div>\n'
        '      <h1>研究概览</h1>'
    )
    return content.replace(marker, replacement, 1)


def unwrap_nested_sections(content: str) -> str:
    if not DETAIL_NESTED.search(content):
        return content

    content = re.sub(
        r'<section class="section" id="detail-[^"]+">\s*',
        '',
        content,
        count=1,
    )
    # Remove one trailing </section> before page-nav when duplicate exists
    content = re.sub(
        r'(</section>)\s*</section>\s*(<nav class="page-nav">)',
        r'\1\n\n    \2',
        content,
        count=1,
    )
    return content


def add_section_h3(content: str, path: Path) -> str:
    page_match = re.search(r'data-page="([^"]+)"', content)
    if not page_match:
        return content

    page_id = page_match.group(1)
    title = SECTION_H3_TITLES.get(page_id)
    if not title:
        return content

    section_match = re.search(
        r'(<section class="section" id="[^"]+">)\s*(?!<h[234])',
        content,
    )
    if not section_match:
        return content

    insert = f'{section_match.group(1)}\n      <h3>{title}</h3>\n      '
    return content.replace(section_match.group(0), insert, 1)


def align_generate_page(content: str, path: Path) -> str:
    if path.name != "problems-answer-generate.html":
        return content

    old_desc = (
        '      <p class="page-desc">分析大模型生成回答中，来源于「昇腾社区」官方的内容占比。</p>\n'
    )
    new_desc = (
        '      <p class="page-desc page-desc--split">\n'
        '        <span class="page-desc-line">生成阶段即大模型输出回答并标注溯源（段末 URL、脚注）的阶段。</span>\n'
        '        <span class="page-desc-line">本页只聚焦这一阶段：统计三模型回答中，来源于「昇腾社区」官方（<code>hiascend.com</code>）的内容占比。</span>\n'
        '      </p>\n'
    )
    content = content.replace(old_desc, new_desc)

    old_block = (
        '    <section class="section" id="answer-generate">\n'
        '      <h3>结论</h3>\n'
        '      <ol class="search-phase-conclusions-list">\n'
        '        <li>Claude 回答（<a href="references/官方信源感知弱/claudeai-回答.md">Pages 导出版</a>，<strong>17</strong> 单元）：昇腾社区 <strong>35%</strong>（6）、第三方 <strong>65%</strong>（11）；段末 <strong>100%</strong> 写出可核对 URL，但仅 <strong>35%</strong> 指向 <code>hiascend.com</code>——有链可溯、社区官方占比低，与「基于官方资料」prompt 落差最大。</li>\n'
        '        <li>DeepSeek 回答（<a href="references/官方信源感知弱/deepseek-回答.md">Pages 版</a>，<strong>23</strong> 单元）：昇腾社区 <strong>22%</strong>（5），华为开发者等官方渠道 <strong>39%</strong>（9）、华为云博客 <strong>30%</strong>（7）、模型内化 <strong>9%</strong>（2）；<strong>91%</strong> 段末含 URL，仅 <strong>35%</strong> 标注含 <code>hiascend.com</code>——华为系文档主导，昇腾社区维度三模型最低。</li>\n'
        '        <li>千问回答（<a href="references/官方信源感知弱/千问-回答.md">脚注版</a>，<strong>18</strong> 单元）：昇腾社区 <strong>67%</strong>（12）、第三方 <strong>28%</strong>（5）、模型内化 <strong>5%</strong>（1）；<strong>17</strong> 单元含 <code>[^1]–[^13]</code> 脚注，文末 <strong>7</strong> 条 <code>hiascend</code> 直链（含 <strong>5</strong> 条 <code>document/detail</code>）——三模型中唯一生成阶段官方过半，最接近 prompt 口径；Claude / DeepSeek / 千问均未引用 CANN 社区版 <strong>9.0.0（900）</strong> 文档。</li>\n'
        '      </ol>\n\n'
        '      <h3>论证</h3>\n'
    )
    new_block = (
        '      <div class="component-problem">\n'
        '        <div class="cp-label">核心结论</div>\n'
        '        <ul>\n'
        '          <li><strong>社区主信源识别失败</strong>：在「基于官方资料」约束下，三模型均未将 <code>hiascend.com</code> 昇腾社区稳定识别为 Ascend C 算子开发的首要权威来源；社区引用仅 <strong>22%–67%</strong>（Claude <strong>35%</strong> 最低），说明模型<strong>感知不到「何处才是本题所指的官方」</strong>，prompt 未能拉高社区文档的选材优先级。</li>\n'
        '          <li><strong>「官方」归类失准</strong>：Claude 以知乎 / CSDN 等教程站支撑正文（<strong>65%</strong>），DeepSeek 以华为开发者站与云博客充当「官方」主体（华为系 <strong>69%</strong>、社区 <strong>22%</strong>），千问虽社区占比最高（<strong>67%</strong>）仍混用第三方与旧版路径——三模型对官方边界的判定不一致，体现<strong>信源分类与权重分配能力弱</strong>，开发者无法据回答判断应以哪套文档为准。</li>\n'
        '          <li><strong>约束难以纠偏选材</strong>：同一 prompt、同一「官方资料」表述，三模型给出截然不同的溯源构成，且均未见 CANN 9.0.0（900）社区版；说明仅靠自然语言约束<strong>不足以让模型跟昇腾社区文档体系对齐</strong>，官方信源感知弱将直接导致回答权威性与产品文档脱节。</li>\n'
        '        </ul>\n'
        '      </div>\n'
        '    </div>\n\n'
        '    <section class="section" id="answer-generate">\n'
        '      <h3>论证</h3>\n'
    )

    if old_block in content:
        content = content.replace(
            '      <p class="page-desc page-desc--split">\n'
            '        <span class="page-desc-line">生成阶段即大模型输出回答并标注溯源（段末 URL、脚注）的阶段。</span>\n'
            '        <span class="page-desc-line">本页只聚焦这一阶段：统计三模型回答中，来源于「昇腾社区」官方（<code>hiascend.com</code>）的内容占比。</span>\n'
            '      </p>\n'
            '    </div>\n\n'
            '    <section class="section" id="answer-generate">\n'
            '      <h3>结论</h3>\n',
            '      <p class="page-desc page-desc--split">\n'
            '        <span class="page-desc-line">生成阶段即大模型输出回答并标注溯源（段末 URL、脚注）的阶段。</span>\n'
            '        <span class="page-desc-line">本页只聚焦这一阶段：统计三模型回答中，来源于「昇腾社区」官方（<code>hiascend.com</code>）的内容占比。</span>\n'
            '      </p>\n',
        )
        content = content.replace(old_block, new_block)

    return content


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    content = original

    if path.name != "ui-system.html" and '<body' in content:
        content = fix_nav(content, path.name)
        content = inject_site_meta_ui_link(content, path.name)
        content = add_module_label_motivation(content)
        content = unwrap_nested_sections(content)
        content = add_section_h3(content, path)
        content = align_generate_page(content, path)

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.glob("*.html")):
        if process_file(path):
            changed.append(path.name)

    print(f"Updated {len(changed)} files:")
    for name in changed:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
