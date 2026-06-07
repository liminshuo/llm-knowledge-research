#!/usr/bin/env python3
"""为亲和原则页中所有含 UI 层面的原则补充可视化渲染示例。"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def demo(n: int, title: str, bad: str, good: str) -> str:
    return f"""      <div class="ui-demo" id="ui-demo-{n}">
        <div class="ui-demo-head"><span class="ui-demo-num">{n}</span><span>{title}</span></div>
        <div class="compare-grid">
          <div class="compare-col machine"><h4>❌ 当前渲染</h4><div class="render-frame">{bad}</div></div>
          <div class="compare-col human"><h4>✅ 亲和渲染</h4><div class="render-frame">{good}</div></div>
        </div>
      </div>"""


def ui_section(items: list[str]) -> str:
    body = "\n".join(items)
    return f"""      <div class="ui-render-examples">
        <h3>UI 渲染示例</h3>
        <p>以下对照仅展示含 <span class="badge badge-scope-ui">UI</span> 调整层面的原则在用户可见页面上的差异。</p>
{body}
      </div>"""


def none_section() -> str:
    return """      <div class="ui-render-examples">
        <h3>UI 渲染示例</h3>
        <p class="ui-render-none">本篇原则的调整层面均为 <span class="badge badge-scope-src">源码</span> 或 <span class="badge badge-scope-pipe">管道</span>，无单独 UI 渲染改造项。</p>
      </div>"""


DEMOS: dict[str, list[str] | None] = {
    "principles-timeliness.html": [
        demo(
            1,
            "文章头部展示版本徽章",
            '<div class="rf-h1">算子开发入门</div><p class="rf-muted">（页头无版本信息，版本仅存在于 URL 参数）</p>',
            '<span class="rf-badge">CANN 8.0.RC1</span><span class="rf-badge">Ascend C</span><div class="rf-h1">算子开发入门</div>',
        ),
        demo(
            2,
            "弃用章节顶部横幅",
            '<div class="rf-h1">旧版 API 说明</div><p>本文介绍已下线的接口…</p>',
            '<div class="rf-banner">⚠ 本文档已废弃（CANN 8.0 起）· <a href="#">见 CANN 9.0 替代文档</a></div><div class="rf-h1">旧版 API 说明</div>',
        ),
    ],
    "principles-image.html": [
        demo(
            2,
            "图片下方附内容转写",
            '<div class="rf-img-placeholder">zh-cn_image_0280001505.png</div>',
            '<div class="rf-img-placeholder">架构示意图</div><p class="rf-caption"><strong>图1</strong> Ascend C 编译流程</p><div class="rf-transcript"><strong>图片内容转写：</strong>左侧为源码目录，箭头指向 bisheng 编译器，输出至 kernel 目录。</div>',
        ),
        demo(
            3,
            "装饰图标移除，信息由文本承载",
            '<p><span class="rf-note-icon">📄</span> 查看详细说明</p>',
            '<p><strong>查看详细说明</strong>（安装与环境配置章节）</p>',
        ),
    ],
    "principles-hotzone.html": [
        demo(
            1,
            "热区图片下方完整链接列表",
            '<div class="rf-img-placeholder">成长地图（仅图片热区可点）</div>',
            '<div class="rf-img-placeholder">成长地图</div><nav><ul class="rf-nav-links"><li><a href="#">环境准备</a></li><li><a href="#">算子开发</a></li><li><a href="#">算子调试</a></li><li><a href="#">性能优化</a></li></ul></nav>',
        ),
        demo(
            2,
            "热区链接使用描述性锚文本",
            '<ul class="rf-nav-links"><li><a href="#">区域1</a></li><li><a href="#">点击这里</a></li></ul>',
            '<ul class="rf-nav-links"><li><a href="#">环境准备与 CANN 安装</a></li><li><a href="#">首个 Ascend C 算子样例</a></li></ul>',
        ),
    ],
    "principles-link.html": [
        demo(
            1,
            "链接锚文本描述目标",
            '<p>完整样例请参考 <a class="rf-link-bad" href="#">LINK</a></p>',
            '<p>完整样例请参考 <a class="rf-link-good" href="#">HelloWorld 完整样例（GitCode）</a></p>',
        ),
        demo(
            2,
            "站外链接标注来源",
            '<p><a class="rf-link-bad" href="#">示例仓库</a></p>',
            '<p><a class="rf-link-good" href="#">示例仓库</a><span class="rf-ext">↗ gitcode.com</span></p>',
        ),
        demo(
            4,
            "链接附上下文说明",
            '<p><a class="rf-link-bad" href="#">详情</a></p>',
            '<p>环境变量配置步骤见 <a class="rf-link-good" href="#">安装后环境变量设置</a>（需 root 权限）。</p>',
        ),
    ],
    "principles-tab.html": [
        demo(
            2,
            "Tab 标签有明确文本",
            '<div class="rf-tabs"><span class="rf-tab rf-tab--active">Tab1</span><span class="rf-tab">Tab2</span></div><div class="rf-tab-panel">编译步骤…</div>',
            '<div class="rf-tabs"><span class="rf-tab rf-tab--active">bisheng 编译</span><span class="rf-tab">CMake 编译</span></div><div class="rf-tab-panel">bisheng 编译步骤…</div>',
        ),
        demo(
            4,
            "非激活 Tab 正文仍在 DOM 可见",
            '<div class="rf-tabs"><span class="rf-tab rf-tab--active">bisheng</span><span class="rf-tab">CMake</span></div><div class="rf-tab-panel">bisheng 内容</div><div class="rf-tab-panel rf-tab-panel--hidden">CMake 内容（display:none）</div>',
            '<div class="rf-tab-panels--good"><div class="rf-tab-panel"><div class="rf-tab-panel-label">bisheng 编译</div>bisheng 编译步骤…</div><div class="rf-tab-panel"><div class="rf-tab-panel-label">CMake 编译</div>CMake 编译步骤…</div></div>',
        ),
    ],
    "principles-collapse.html": [
        demo(
            2,
            "折叠标题有语义文本",
            '<div class="rf-collapse-empty">▸ <em>（空 div，无标题文本）</em></div><p class="rf-muted">正文被折叠…</p>',
            '<details open><summary>高级配置参数说明</summary><p>参数 A 用于控制 tiling 策略…</p></details>',
        ),
        demo(
            3,
            "折叠正文不用 display:none 移除",
            '<details><summary>参数说明</summary><p class="rf-muted">（折叠时正文 display:none，抓取为空）</p></details>',
            '<details open><summary>参数说明</summary><p>参数 A：控制 tiling…<br>参数 B：控制内存复用…</p></details>',
        ),
    ],
    "principles-code.html": [
        demo(
            2,
            "行号与代码分离（CSS 渲染）",
            '<table class="rf-code-table"><tr><td class="rf-ln">1</td><td><code>int main() {</code></td></tr><tr><td class="rf-ln">2</td><td><code>  return 0;</code></td></tr></table>',
            '<div class="rf-code-head">main.cpp · C++</div><pre class="rf-code">int main() {\n  return 0;\n}</pre><p class="rf-muted">行号由 CSS 伪元素渲染，不进 code 文本</p>',
        ),
        demo(
            3,
            "弃用 highlighttable 布局",
            '<table class="rf-code-table"><tr><td class="rf-ln">1</td><td>#include &lt;acl/acl.h&gt;</td></tr><tr><td class="rf-ln">2</td><td>int Init() { … }</td></tr></table>',
            '<pre class="rf-code">#include &lt;acl/acl.h&gt;\nint Init() { … }</pre>',
        ),
        demo(
            4,
            "代码块上方标注文件名与场景",
            '<pre class="rf-code">kernel_add.cpp</pre>',
            '<div class="rf-code-head">kernel_add.cpp · Ascend C · 矢量算子示例</div><pre class="rf-code">// kernel 实现…</pre>',
        ),
    ],
    "principles-table.html": [
        demo(
            1,
            "表格上方可见表题",
            '<table class="rf-table"><tr class="rf-fake-th"><td>类型</td><td>说明</td></tr><tr><td>Vector</td><td>逐元素</td></tr></table>',
            '<table class="rf-table"><caption>表1 编程模型分类</caption><tr><th>类型</th><th>说明</th></tr><tr><td>Vector</td><td>逐元素</td></tr></table>',
        ),
        demo(
            2,
            "表头使用 th 而非样式伪装",
            '<table class="rf-table"><tr><td class="rf-fake-th">类型</td><td class="rf-fake-th">说明</td></tr><tr><td>Vector</td><td>逐元素</td></tr></table>',
            '<table class="rf-table"><tr><th>类型</th><th>说明</th></tr><tr><td>Vector</td><td>逐元素</td></tr></table>',
        ),
        demo(
            3,
            "单元格内不嵌套大段代码",
            '<table class="rf-table"><tr><th>参数</th><th>示例</th></tr><tr><td>dtype</td><td><pre class="rf-code" style="font-size:9px">float16\nfloat32\n…</pre></td></tr></table>',
            '<p class="rf-muted">表1 参数说明</p><table class="rf-table"><tr><th>参数</th><th>说明</th></tr><tr><td>dtype</td><td>支持 float16 / float32</td></tr></table><pre class="rf-code">// 完整示例见下方代码块</pre>',
        ),
    ],
    "principles-note.html": [
        demo(
            2,
            "Note 正文完整展开",
            '<div class="rf-note rf-note--bad"><span class="rf-note-icon">ℹ️</span><span>安装后需设置环境变量 <em>（悬停才显示全文…）</em></span></div>',
            '<div class="rf-note rf-note--good"><div><span class="rf-note-label">注意：</span>安装 CANN 后，需执行 <code>source set_env.sh</code> 设置环境变量，否则无法调用算子 API。</div></div>',
        ),
        demo(
            3,
            "移除图标，类型用文本前缀",
            '<div class="rf-note rf-note--bad"><span class="rf-note-icon">⚠️</span><span>请勿在生产环境直接调试</span></div>',
            '<div class="rf-note rf-note--good"><div><span class="rf-note-label">警告：</span>请勿在生产环境直接调试，可能导致服务中断。</div></div>',
        ),
    ],
    "principles-format.html": [
        demo(
            4,
            "页脚提供机器可读版本入口",
            '<div class="rf-footer-bar">© 昇腾社区 · 上一篇 · 下一篇</div>',
            '<div class="rf-footer-bar"><a href="#">⎘ 机器可读版本（source HTML）</a> · © 昇腾社区 · 上一篇 · 下一篇</div>',
        ),
    ],
    "principles-structure-llms.html": None,
    "principles-structure-metadata.html": [
        demo(
            1,
            "有且仅有一个 H1",
            '<div class="rf-h1">算子开发</div><div class="rf-h1" style="font-size:15px">算子开发入门</div>',
            '<div class="rf-h1">算子开发入门</div><div class="rf-h2">环境准备</div>',
        ),
        demo(
            2,
            "标题层级连续",
            '<div class="rf-h1">算子开发入门</div><div class="rf-h3">（跳级 H3，无 H2）</div><p>正文…</p>',
            '<div class="rf-h1">算子开发入门</div><div class="rf-h2">环境准备</div><div class="rf-h3">安装 CANN</div>',
        ),
        demo(
            3,
            "标题文本自解释",
            '<div class="rf-h2">概述</div><div class="rf-h2">说明</div>',
            '<div class="rf-h2">Ascend C 算子工程结构</div><div class="rf-h2">编译与部署流程</div>',
        ),
        demo(
            5,
            "文章头部摘要块（60–120 字）",
            '<div class="rf-h1">算子开发入门</div><p>正文直接开始…</p>',
            '<div class="rf-h1">算子开发入门</div><p class="rf-summary">本文介绍 Ascend C 算子开发的基本流程与工程结构，面向已完成环境安装、希望编写首个自定义算子的开发者。（78 字）</p>',
        ),
        demo(
            6,
            "头部版本 / 产品徽章",
            '<div class="rf-h1">算子开发入门</div>',
            '<span class="rf-badge">CANN 9.0.0</span><span class="rf-badge">Ascend C</span><span class="rf-badge">算子开发</span><div class="rf-h1">算子开发入门</div>',
        ),
        demo(
            7,
            "面包屑文本路径可见",
            '<p class="rf-muted">（无面包屑，仅靠侧栏定位）</p>',
            '<nav class="rf-breadcrumb">文档中心 / Ascend C / 算子开发 / 算子开发入门</nav><div class="rf-h1">算子开发入门</div>',
        ),
        demo(
            10,
            "适用芯片标签在渲染页展示",
            '<div class="rf-h1">Add 算子 API</div><p>支持 Atlas 训练系列产品。</p>',
            '<span class="rf-badge">Atlas A2</span><span class="rf-badge">Atlas 200I</span><div class="rf-h1">Add 算子 API</div>',
        ),
    ],
}

SKIP = {"principles-general.html"}

STRIP = re.compile(
    r"\s*<div class=\"(?:principle-guide|ui-render-examples)[^\"]*\">.*?</div>\s*(?=</section>)",
    re.DOTALL,
)

STRIP2 = re.compile(
    r"(</table>)\s*<div class=\"(?:principle-guide|compare-grid|ui-render-examples).*?(?=</section>)",
    re.DOTALL,
)


def patch(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = STRIP2.sub(r"\1\n" + block + "\n", text, count=1)
    if "ui-render-examples" not in text and "</table>" in text:
        text = text.replace("</table>\n", f"</table>\n{block}\n", 1)
    path.write_text(text, encoding="utf-8")
    print(f"  {path.name}")


def main() -> None:
    for name, items in DEMOS.items():
        if name in SKIP:
            continue
        path = ROOT / name
        if not path.exists():
            continue
        if items is None:
            patch(path, none_section())
        else:
            patch(path, ui_section(items))
    print("done")


if __name__ == "__main__":
    main()
