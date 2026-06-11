#!/usr/bin/env python3
"""为亲和原则页注入：原则概要、原则描述、调整层面（UI / 源码 / 管道）。

DEPRECATED — 示例内容（如编程模型表）可能落后于现行 pages；勿批量重跑。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCOPE = {
    "ui": '<span class="badge badge-scope-ui">UI</span>',
    "src": '<span class="badge badge-scope-src">源码</span>',
    "pipe": '<span class="badge badge-scope-pipe">管道</span>',
}


def scopes(*keys: str) -> str:
    return " ".join(SCOPE[k] for k in keys)


def level_badge(level: str) -> str:
    if level == "must":
        return '<span class="badge badge-must">必须</span>'
    return '<span class="badge badge-should">建议</span>'


def rules_table(rules: list[dict]) -> str:
    rows = []
    for n, r in enumerate(rules, 1):
        rows.append(
            f'          <tr id="{r["anchor"]}"><td>{n}</td>'
            f'<td>{r["desc"]}</td>'
            f'<td>{level_badge(r["level"])}</td>'
            f'<td class="scope-cell">{scopes(*r["scope"])}</td></tr>'
        )
    body = "\n".join(rows)
    return f"""      <table class="data-table">
        <thead>
          <tr><th>编号</th><th>原则描述</th><th>级别</th><th>调整层面</th></tr>
        </thead>
        <tbody>
{body}
        </tbody>
      </table>"""


def block(brief: str, rules: list[dict], guide: str, section_id: str, section_title: str = "亲和原则") -> str:
    return f"""    <section class="section" id="{section_id}">
      <h3>{section_title}</h3>
{rules_table(rules)}
{guide}
    </section>"""


PAGES: dict[str, dict] = {
    "principles-timeliness.html": {
        "desc": "版本、弃用状态须在渲染页头部可见，并写入结构化字段供检索过滤。",
        "problem": "problems-timeliness.html",
        "section_id": "timeliness",
        "brief": "大模型选型依赖文档版本。版本号与弃用提示不能只藏在 URL 或后台字段——须在<strong>文章头部渲染区</strong>用徽章、横幅直观呈现，同时在源码与管道中同步 <code>version</code> / <code>deprecated_since</code>。",
        "rules": [
            {"anchor": "ver-01", "id": "VER-01", "desc": "文章头部（H1 下方）展示版本徽章，如「CANN 8.0.RC1」", "level": "must", "scope": ("ui", "src")},
            {"anchor": "ver-02", "id": "VER-02", "desc": "已废弃章节在渲染页顶部显示弃用横幅，并链接替代文档", "level": "must", "scope": ("ui", "src")},
            {"anchor": "ver-03", "id": "VER-03", "desc": "Front Matter 与 JSON-LD 写入 <code>version</code>、<code>deprecated_since</code>", "level": "must", "scope": ("src", "pipe")},
            {"anchor": "ver-04", "id": "VER-04", "desc": "机器层导出须携带版本字段，供 RAG 按版本过滤", "level": "must", "scope": ("pipe",)},
        ],
        "guide": """      <div class="principle-guide info-box">
        <div class="box-title">落地指引 · 文章头部</div>
        <div class="article-header-mock">
          <div class="mock-meta">
            <span class="mock-tag">CANN 8.0.RC1</span>
            <span class="mock-tag">Ascend C</span>
            <span class="mock-tag" style="background:#fef2f2;color:#b91c1c;">已废弃 · 见 CANN 9.0 替代</span>
          </div>
          <strong style="font-size:18px;">算子开发入门</strong>
        </div>
        <p style="margin:12px 0 0;font-size:13px;color:var(--color-text-secondary);">版本与弃用状态放在用户首屏可见区域，而非仅存在于页脚或接口返回值。</p>
      </div>""",
    },
    "principles-image.html": {
        "desc": "信息型图片的图意须用可见转写或替代文本表达，不能只留 PNG 文件名。",
        "problem": "problems-content-image.html",
        "section_id": "image",
        "brief": "模型读不到像素里的箭头与标注。示意图、架构图须在<strong>渲染页</strong>提供可见的 figcaption / 转写段落，同时在<strong>源码</strong>写入 alt；复杂图另附 Mermaid 或 SVG 文本源。",
        "rules": [
            {"anchor": "img-01", "id": "IMG-01", "desc": "信息型图片在源码中写有意义 <code>alt</code>（描述图意，非文件名）", "level": "must", "scope": ("src",)},
            {"anchor": "img-02", "id": "IMG-02", "desc": "复杂图表在渲染页图片下方附「图片内容转写」段落（逐步描述节点与关系）", "level": "must", "scope": ("ui", "src")},
            {"anchor": "img-04", "id": "IMG-04", "desc": "纯装饰图标从渲染页移除或 <code>aria-hidden</code>，信息改由相邻文本承载", "level": "must", "scope": ("ui", "src")},
            {"anchor": "img-05", "id": "IMG-05", "desc": "架构类图片另提供 Mermaid / SVG 可编辑源，便于机器层直接读取", "level": "should", "scope": ("src", "pipe")},
        ],
        "guide": """      <div class="compare-grid principle-guide">
        <div class="compare-col machine">
          <h4>❌ 不亲和</h4>
          渲染页仅一张图，源码 <code>&lt;img src="figure/zh-cn_image_...png"&gt;</code>，模型只得文件名
        </div>
        <div class="compare-col human">
          <h4>✅ 亲和</h4>
          图下可见转写 + 源码 alt + 可选 Mermaid；热区另见 <a href="principles-hotzone.html">图片热区</a>
        </div>
      </div>""",
    },
    "principles-hotzone.html": {
        "desc": "热区坐标对模型不可读，须在渲染页提供等价的文本链接列表。",
        "problem": "problems-content-hotzone.html",
        "section_id": "hotzone",
        "brief": "图片热区（<code>usemap</code>）只在视觉上可点，模型无法解析坐标。须在<strong>渲染页</strong>图片旁或下方列出完整文本导航，并在<strong>源码</strong>用 <code>&lt;nav&gt;</code> 与每个 <code>&lt;area&gt;</code> 一一对应。",
        "rules": [
            {"anchor": "img-03", "id": "IMG-03", "desc": "带热区的图片下方渲染完整链接列表（<code>&lt;nav aria-label&gt;</code>），覆盖全部热区目标", "level": "must", "scope": ("ui", "src")},
            {"anchor": "l-04", "id": "L-04", "desc": "每个热区目标须有描述性锚文本链接，禁止「区域1」「点击这里」", "level": "must", "scope": ("ui", "src")},
        ],
        "guide": """      <div class="compare-grid principle-guide">
        <div class="compare-col machine"><h4>❌ 不亲和</h4><code>&lt;img usemap="#map"&gt;</code>，模型只见 PNG</div>
        <div class="compare-col human"><h4>✅ 亲和</h4>图下 28 条文本链接 + <code>aria-label="成长地图"</code></div>
      </div>""",
    },
    "principles-link.html": {
        "desc": "链接目标须由锚文本自解释，禁止无意义占位符。",
        "problem": "problems-content-link.html",
        "section_id": "link",
        "brief": "「LINK」「点击这里」在渲染页与源码中对模型均为黑盒。锚文本须在<strong>可见页面</strong>直接说明目标，站外链保留完整 URL；站内链在管道层转为绝对地址。",
        "rules": [
            {"anchor": "l-01", "id": "L-01", "desc": "渲染页链接文字描述目标，如「HelloWorld 完整样例（GitCode）」", "level": "must", "scope": ("ui", "src")},
            {"anchor": "l-02", "id": "L-02", "desc": "站外链接在渲染页标注 external 或图标旁附完整域名", "level": "must", "scope": ("ui", "src")},
            {"anchor": "l-03", "id": "L-03", "desc": "机器层将站内相对链转为绝对 URL", "level": "must", "scope": ("pipe",)},
            {"anchor": "l-05", "id": "L-05", "desc": "必要时用 <code>title</code> 或前后句补充链接用途", "level": "should", "scope": ("ui", "src")},
        ],
        "guide": """      <div class="principle-guide info-box danger">
        <div class="box-title">违规示例</div>
        「完整样例请参考 <strong>LINK</strong>」—— 渲染页与源码均无目标语义，模型无法追溯 GitCode 仓库。
      </div>""",
    },
    "principles-tab.html": {
        "desc": "Tab 隐藏的面板须在源码完整存在，渲染层不得用 CSS 藏掉非激活项。",
        "problem": "problems-content-tab.html",
        "section_id": "tab",
        "brief": "用户切换 Tab 才看到的内容，模型默认抓不到。所有面板须在<strong>源码</strong>并列存在；<strong>渲染页</strong>可用样式区分激活态，但禁止 <code>display:none</code> 移除非默认 Tab 的 DOM 文本。",
        "rules": [
            {"anchor": "tab-01", "id": "TAB-01", "desc": "所有 Tab 面板内容在源 HTML 中完整输出，不依赖 JS 懒加载正文", "level": "must", "scope": ("src",)},
            {"anchor": "tab-02", "id": "TAB-02", "desc": "每个 Tab 标签在渲染页有明确文本（如「bisheng 编译」「CMake 编译」）", "level": "must", "scope": ("ui", "src")},
            {"anchor": "tab-03", "id": "TAB-03", "desc": "机器层将全部 Tab 展开，以 H3 标注各面板标题", "level": "must", "scope": ("pipe",)},
            {"anchor": "tab-04", "id": "TAB-04", "desc": "渲染组件禁止用 <code>display:none</code> / <code>visibility:hidden</code> 隐藏非激活面板正文", "level": "must", "scope": ("ui", "src")},
        ],
        "guide": """      <div class="principle-guide info-box">
        <div class="box-title">落地指引</div>
        源 HTML 中 bisheng / CMake 已同级排列则源层亲和；风险在 Nuxt Tab 组件渲染时折叠非激活项——改组件或 SSR 时全量输出。
      </div>""",
    },
    "principles-collapse.html": {
        "desc": "折叠面板正文须在渲染页默认可读，标题须有文本语义。",
        "problem": "problems-content-collapse.html",
        "section_id": "collapse",
        "brief": "折叠是「用户看得到 ≠ 模型读得到」的典型场景。<strong>渲染页</strong>应用 <code>details open</code> 或默认展开样式；<strong>源码</strong>标题用 <code>summary</code> / H3，禁止空 div 作标题。",
        "rules": [
            {"anchor": "coll-01", "id": "COLL-01", "desc": "机器层导出时默认展开全部折叠块", "level": "must", "scope": ("pipe",)},
            {"anchor": "coll-02", "id": "COLL-02", "desc": "折叠标题在渲染页可见且有语义（<code>&lt;summary&gt;</code> 或 H3 文本）", "level": "must", "scope": ("ui", "src")},
            {"anchor": "coll-03", "id": "COLL-03", "desc": "禁止用 CSS 将折叠正文从 DOM 流中隐藏（display:none）", "level": "must", "scope": ("ui", "src")},
            {"anchor": "coll-04", "id": "COLL-04", "desc": "源码中 <code>&lt;details&gt;</code> 建议加 <code>open</code> 属性", "level": "should", "scope": ("src",)},
        ],
        "guide": """      <div class="principle-guide info-box warning">
        <div class="box-title">核心原则</div>
        若折叠仅为节省屏效，机器源应始终输出展开态；渲染页可用视觉折叠，但抓取源不可丢字。
      </div>""",
    },
    "principles-code.html": {
        "desc": "代码块须纯净可复制，行号与语法高亮不得污染正文。",
        "problem": "problems-content-code.html",
        "section_id": "code",
        "brief": "highlighttable 把行号写进 DOM 文本，模型会复述「1 2 3…」污染代码。<strong>渲染页</strong>行号用 CSS 伪元素；<strong>源码</strong>用 <code>pre &gt; code.language-xxx</code>；实体解码在管道完成。",
        "rules": [
            {"anchor": "code-01", "id": "CODE-01", "desc": "源码使用 <code>pre &gt; code</code> 并标注 <code>language-xxx</code>", "level": "must", "scope": ("src",)},
            {"anchor": "code-02", "id": "CODE-02", "desc": "渲染页行号与代码分离，行号不写入 <code>code</code> 文本节点", "level": "must", "scope": ("ui", "src")},
            {"anchor": "code-03", "id": "CODE-03", "desc": "弃用 highlighttable 表格布局渲染代码块", "level": "must", "scope": ("ui", "src")},
            {"anchor": "code-04", "id": "CODE-04", "desc": "代码块上方在渲染页标注文件名、语言、适用场景", "level": "should", "scope": ("ui", "src")},
            {"anchor": "code-06", "id": "CODE-06", "desc": "管道入模前解码 <code>&amp;lt;</code> 等 HTML 实体", "level": "must", "scope": ("pipe",)},
        ],
        "guide": """      <div class="compare-grid principle-guide">
        <div class="compare-col machine"><h4>❌ highlighttable</h4>行号与代码混为表格，模型输出污染</div>
        <div class="compare-col human"><h4>✅ pre + code</h4>渲染页 CSS 行号，源码纯净代码</div>
      </div>""",
    },
    "principles-table.html": {
        "desc": "表格语义靠 caption 与 th，不能仅靠加粗样式。",
        "problem": "problems-content-table.html",
        "section_id": "table",
        "brief": "无边题表格在渲染页是「一堆格子」。须在<strong>渲染页</strong>显示表题（caption 或前置 H4），<strong>源码</strong>用 <code>th</code> 标表头；单元格内不嵌套代码块。",
        "rules": [
            {"anchor": "tbl-01", "id": "TBL-01", "desc": "渲染页表格上方可见表题，如「表1 编程模型分类」", "level": "must", "scope": ("ui", "src")},
            {"anchor": "tbl-02", "id": "TBL-02", "desc": "表头用 <code>th</code> 而非样式伪装的 <code>td</code>", "level": "must", "scope": ("ui", "src")},
            {"anchor": "tbl-03", "id": "TBL-03", "desc": "不在单元格内嵌套多行代码块，大段代码放表格外", "level": "must", "scope": ("ui", "src")},
            {"anchor": "tbl-04", "id": "TBL-04", "desc": "机器层额外输出 Markdown 表格副本", "level": "should", "scope": ("pipe",)},
        ],
        "guide": """      <div class="principle-guide info-box success">
        <div class="box-title">标杆</div>
        「编程模型概述」页「表1 编程模型分类」—— 渲染页表题 + 结构清晰，亲和度最高。
      </div>""",
    },
    "principles-note.html": {
        "desc": "注意/警告/提示用文本表达类型；装饰图标对模型无意义，应从渲染页与源码同时移除。",
        "problem": "problems-content-note.html",
        "section_id": "note",
        "brief": "Note 组件的图标（⚠️ 💡）在渲染页好看，但对大模型是噪声——图标不携带可检索语义。类型须用<strong>可见文本前缀</strong>（「注意：」「警告：」）表达，图标从<strong>UI 与源码</strong>同时去掉；正文默认在渲染页完整展开。",
        "rules": [
            {"anchor": "note-01", "id": "NOTE-01", "desc": "源码用 <code>data-admonition-type</code> 标注 note / warning / tip / danger", "level": "must", "scope": ("src",)},
            {"anchor": "note-02", "id": "NOTE-02", "desc": "渲染页 Note 正文完整展开，不折叠、不 Tooltip 藏字", "level": "must", "scope": ("ui", "src")},
            {"anchor": "note-03", "id": "NOTE-03", "desc": "移除 Note 装饰图标；类型改用文本前缀「注意：」「警告：」显示在渲染页", "level": "must", "scope": ("ui", "src")},
            {"anchor": "note-04", "id": "NOTE-04", "desc": "机器层转为 Markdown 引用块（<code>&gt; **注意**</code>）", "level": "must", "scope": ("pipe",)},
        ],
        "guide": """      <div class="principle-guide">
        <h4>渲染页目标样式</h4>
        <div class="arch-diagram">&gt; **注意**
&gt; 安装 CANN 软件后，需要执行 `source ${INSTALL_DIR}/set_env.sh` 设置环境变量。</div>
        <p style="margin-top:12px;font-size:13px;color:var(--color-text-secondary);">左侧无图标，类型由加粗文本承担；源码同步删除 <code>&lt;img&gt;</code> / icon font 节点。</p>
      </div>""",
    },
    "principles-format.html": {
        "desc": "人类渲染页与机器源双轨交付；渲染页可声明机器入口。",
        "problem": "problems-format.html",
        "section_id": "format",
        "brief": "交付格式主要是<strong>管道与站点</strong>决策：机器源剥离导航壳、<code>.md</code> 须为真 Markdown。少量<strong>UI</strong>改动：在文章页脚提供「查看机器源」链接，让用户与爬虫发现低噪声入口。",
        "rules": [
            {"anchor": "fmt-dual", "id": "FMT-01", "desc": "每篇文档提供渲染页 + 机器源（<code>/doc_center/source/</code> 或纯 MD）双轨", "level": "must", "scope": ("pipe",)},
            {"anchor": "fmt-md", "id": "FMT-02", "desc": "<code>.md</code> URL 返回真实 Markdown，非 SPA 壳层", "level": "must", "scope": ("pipe",)},
            {"anchor": "fmt-strip", "id": "FMT-03", "desc": "机器源剥离全站导航、页头页脚、脚本与样式", "level": "must", "scope": ("pipe",)},
            {"anchor": "fmt-link", "id": "FMT-04", "desc": "渲染页页脚或工具栏提供「机器可读版本」链接", "level": "should", "scope": ("ui",)},
            {"anchor": "fmt-priority", "id": "FMT-05", "desc": "sitemap / robots 优先声明机器源 URL", "level": "must", "scope": ("pipe",)},
        ],
        "guide": """      <div class="principle-guide info-box">
        <div class="box-title">落地指引</div>
        双轨架构与转换管道见 <a href="problems-format.html#solution">问题论证 · 解决方案</a>；UI 侧仅需在渲染页增加可发现的机器源入口。
      </div>""",
    },
    "principles-structure-llms.html": {
        "desc": "机器发现层靠站点配置，单篇文档 UI 改动极少。",
        "problem": "problems-structure-llms.html",
        "section_id": "structure-llms",
        "brief": "llms.txt、sitemap、robots 决定爬虫能否找到机器源——属<strong>管道 / 站点运维</strong>。可选在全局模板 <code>&lt;head&gt;</code> 增加 <code>link rel</code> 发现链接，单篇文章渲染页通常无需改动。",
        "rules": [
            {"anchor": "llms-01", "id": "LLMS-01", "desc": "站点根路径部署 <code>llms.txt</code>，列出文档索引与机器源基址", "level": "must", "scope": ("pipe",)},
            {"anchor": "llms-02", "id": "LLMS-02", "desc": "<code>robots.txt</code> 不得禁止 <code>/doc_center/source/</code>", "level": "must", "scope": ("pipe",)},
            {"anchor": "llms-03", "id": "LLMS-03", "desc": "sitemap 优先收录机器源 URL", "level": "must", "scope": ("pipe",)},
            {"anchor": "llms-04", "id": "LLMS-04", "desc": "全局模板可选 <code>link rel=\"llms\"</code> 指向站点索引", "level": "should", "scope": ("src",)},
        ],
        "guide": """      <div class="principle-guide info-box">
        <div class="box-title">实测结论</div>
        Ascend 文档站 <code>llms.txt</code> 404、sitemap 100% 渲染页——需站点级改造，非单篇 UI 写作能弥补。
      </div>""",
    },
    "principles-structure-metadata.html": {
        "desc": "版本、产品、适用设备、摘要等须在文章头部可视化呈现，并同步元数据。",
        "problem": "problems-structure-metadata.html",
        "section_id": "metadata",
        "section_title": "元数据与文章头部",
        "brief": "模型选型靠元数据，但元数据必须<strong>在渲染页头部可见</strong>才有写作约束力。每篇文章顶部应呈现：版本徽章、产品标签、适用芯片、<strong>60–120 字摘要</strong>、面包屑；同时在源码写 Front Matter，管道输出 JSON-LD。",
        "rules": [
            {"anchor": "h-01", "id": "H-01", "desc": "渲染页有且仅有一个 H1，与浏览器 title 语义一致", "level": "must", "scope": ("ui", "src")},
            {"anchor": "h-02", "id": "H-02", "desc": "标题层级连续（H1→H2→H3），渲染页大纲结构清晰", "level": "must", "scope": ("ui", "src")},
            {"anchor": "h-03", "id": "H-03", "desc": "H2/H3 文本自解释，避免孤立「概述」「说明」", "level": "should", "scope": ("ui", "src")},
            {"anchor": "h-04", "id": "H-04", "desc": "保留稳定锚点 ID（<code>ZH-CN_TOPIC_xxx</code>）", "level": "must", "scope": ("src",)},
            {"anchor": "mdm-summary", "id": "MDM-07", "desc": "文章头部渲染摘要块，<strong>60–120 字</strong>，概括本文解决的问题与适用读者", "level": "must", "scope": ("ui", "src")},
            {"anchor": "mdm-version", "id": "MDM-01", "desc": "头部展示 version / product / doc_type 徽章，源码 Front Matter 同步", "level": "must", "scope": ("ui", "src", "pipe")},
            {"anchor": "mdm-breadcrumb", "id": "MDM-02", "desc": "渲染页面包屑 <code>&lt;nav aria-label=\"breadcrumb\"&gt;</code> 文本路径可见", "level": "must", "scope": ("ui", "src")},
            {"anchor": "mdm-jsonld", "id": "MDM-03", "desc": "管道输出 JSON-LD TechArticle，字段与可见头部一致", "level": "must", "scope": ("pipe", "src")},
            {"anchor": "mdm-canonical", "id": "MDM-04", "desc": "<code>canonical</code> 指向稳定文档 ID，避免同题异版", "level": "must", "scope": ("pipe", "src")},
            {"anchor": "mdm-tags", "id": "MDM-05", "desc": "适用芯片 / 算子类别在渲染页以标签展示，非仅后台字段", "level": "should", "scope": ("ui", "src")},
            {"anchor": "mdm-sync", "id": "MDM-06", "desc": "渲染页可见元数据与入库字段一致，避免「页面有据、入库无情」", "level": "must", "scope": ("pipe",)},
        ],
        "guide": """      <div class="principle-guide">
        <h4>落地指引 · 文章头部信息块</h4>
        <div class="article-header-mock">
          <nav style="font-size:12px;color:var(--color-text-secondary);margin-bottom:10px;">文档中心 / Ascend C / 算子开发 / 算子开发入门</nav>
          <div class="mock-meta">
            <span class="mock-tag">CANN 9.0.0</span>
            <span class="mock-tag">Ascend C</span>
            <span class="mock-tag">算子开发 · 入门</span>
            <span class="mock-tag">Atlas A2</span>
          </div>
          <strong style="font-size:20px;display:block;margin-bottom:8px;">算子开发入门</strong>
          <p class="mock-summary">本文介绍 Ascend C 算子开发的基本流程与工程结构，面向已完成环境安装、希望编写首个自定义算子的开发者。阅读约 15 分钟。（摘要 60–120 字）</p>
        </div>
        <p style="margin-top:12px;font-size:13px;color:var(--color-text-secondary);">摘要字数可在写作规范中定义为 60–120 字；版本与适用设备标签须与 Front Matter 字段一一对应。</p>
      </div>""",
        "extra_section": """    <section class="section" id="heading-rules">
      <h3>标题层级（并入本篇）</h3>
      <p class="page-desc" style="margin:-8px 0 16px;">标题规则已并入上表 H-01 ~ H-04；原独立「标题」页见 <a href="principles-structure-metadata.html#h-01">H-01</a>。</p>
    </section>""",
    },
}


def problem_label_for(data: dict) -> str:
    if data.get("problem_label"):
        return data["problem_label"]
    problem_path = ROOT / data["problem"]
    if problem_path.exists():
        match = re.search(r"<h1>([^<]+)</h1>", problem_path.read_text(encoding="utf-8"))
        if match:
            return match.group(1)
    return data["problem"]


def patch_file(path: Path, data: dict) -> None:
    text = path.read_text(encoding="utf-8")
    problem_label = problem_label_for(data)

    new_desc = (
        f'      <p class="page-desc">对应 <a href="{data["problem"]}">问题论证 · {problem_label}</a>。{data["desc"]}</p>'
    )
    text = re.sub(
        r"      <p class=\"page-desc\">.*?</p>",
        new_desc,
        text,
        count=1,
        flags=re.DOTALL,
    )

    content = block(
        data["brief"],
        data["rules"],
        data["guide"],
        data["section_id"],
        data.get("section_title", "亲和原则"),
    )
    if data.get("extra_section"):
        content += "\n\n" + data["extra_section"]

    text = re.sub(
        r"    <section class=\"section\".*?</section>",
        content,
        text,
        count=1,
        flags=re.DOTALL,
    )

    path.write_text(text, encoding="utf-8")
    print(f"  updated {path.name}")


def main() -> None:
    for name, data in PAGES.items():
        patch_file(ROOT / name, data)
    print("done")


if __name__ == "__main__":
    main()
