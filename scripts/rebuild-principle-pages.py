#!/usr/bin/env python3
"""Rebuild all principle pages to match the standardized structure:
H2 (文档内容/设计UI/前端调整) → H3 调整建议 (ul.principle-suggestions) + H3 调整示例
"""
from pathlib import Path
import re

BASE = Path('/Users/melody/Desktop/大模型抓取')


def cell_to_items(html_text):
    """Parse table cell HTML with <strong>Title</strong>：<br>content into list items."""
    html_text = html_text.strip()
    if not html_text or html_text == '—':
        return []
    # Split on <strong> occurrences, keep the delimiter
    parts = re.split(r'(<strong>)', html_text)
    items = []
    buf = ''
    for p in parts:
        if p == '<strong>':
            if buf.strip():
                # Flush previous non-strong text as a single item
                text = re.sub(r'<br\s*/?>', '\n', buf).strip()
                if text and text != '—':
                    items.append(f'<li>{text}</li>')
            buf = '<strong>'
        else:
            buf += p
    if buf.strip():
        text = buf.strip()
        # Clean up trailing <br> fragments
        text = re.sub(r'<br\s*/?>\s*$', '', text).strip()
        text = re.sub(r'<br\s*/?>', ' ', text)
        if text and text != '—':
            items.append(f'<li>{text}</li>')
    return items


def items_from_table(raw_td_inner):
    """Parse inner HTML of a <td> cell into structured <li> items."""
    text = raw_td_inner.strip()
    if not text or text == '—':
        return []
    # Find all <strong>...</strong>：<br>content blocks
    items = []
    # Pattern: <strong>Title</strong>：\n?content_until_next_strong_or_end
    pattern = re.compile(
        r'<strong>(.*?)</strong>：\s*(?:<br\s*/?>)?\s*(.*?)(?=<strong>|$)',
        re.DOTALL | re.IGNORECASE
    )
    matches = list(pattern.finditer(text))
    if matches:
        for m in matches:
            title = m.group(1).strip()
            content = m.group(2).strip()
            # Clean trailing <br>
            content = re.sub(r'<br\s*/?>\s*$', '', content).strip()
            # Replace <br> within content with space
            content = re.sub(r'\s*<br\s*/?>\s*', ' ', content)
            items.append(f'<li><strong>{title}</strong>：{content}</li>')
    else:
        # No <strong> pattern — just use the raw text as a single item
        cleaned = re.sub(r'<br\s*/?>', ' ', text).strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        if cleaned and cleaned != '—':
            items.append(f'<li>{cleaned}</li>')
    return items


def wrap_section(sec_id, h2_title, suggestions_items, example_html, h3_sug_id, h3_ex_id):
    """Build a complete section block."""
    sug_li = '\n        '.join(suggestions_items)
    ex_block = example_html.strip() if example_html else '<p class="text-auxiliary">（示例待补充）</p>'
    return f'''    <section class="section" id="{sec_id}">
      <h2>{h2_title}</h2>

      <h3 id="{h3_sug_id}">调整建议</h3>
      <ul class="principle-suggestions">
        {sug_li}
      </ul>

      <h3 id="{h3_ex_id}">调整示例</h3>
      {ex_block}
    </section>'''


def read_page_header(html):
    """Extract the page-header div from existing HTML."""
    m = re.search(r'(<div class="page-header">.*?</div>)', html, re.DOTALL)
    return m.group(1) if m else ''


def read_section_examples(html, section_marker):
    """Extract example content (h4, ui-demo, pre, hr) after a section heading."""
    # Find the section by h2 id or class
    # section_marker: 'design', 'content-side', 'dev-side'
    pattern = re.compile(
        r'<h2[^>]+id="' + re.escape(section_marker) + r'"[^>]*>.*?</h2>(.*?)(?=<h2\b|</section>)',
        re.DOTALL | re.IGNORECASE
    )
    m = pattern.search(html)
    if not m:
        return ''
    chunk = m.group(1)
    # Remove old principle-deliverable blocks (replaced by new suggestion list)
    chunk = re.sub(r'<div[^>]+class="[^"]*principle-deliverable[^"]*"[^>]*>.*?</div>', '', chunk, flags=re.DOTALL)
    # Remove old H3 id="design-example" etc. heading (we'll add our own)
    chunk = re.sub(r'<h3[^>]+id="[^"]*-example"[^>]*>.*?</h3>', '', chunk, flags=re.DOTALL | re.IGNORECASE)
    # Remove old generic <h3>示例</h3>
    chunk = re.sub(r'<h3[^>]*>\s*示例\s*</h3>', '', chunk, flags=re.IGNORECASE)
    chunk = chunk.strip()
    return chunk


HEADER_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · 亲和原则 · 社区AI亲和分析</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="inner-page" data-module="principles" data-page="{data_page}">

<header class="site-header">
  <div class="site-logo">社区AI亲和分析</div>
  <nav class="site-nav">
    <a href="index.html">首页</a>
    <a href="background-motivation.html">研究概览</a>
    <a href="problems-answer-search.html">实测问题</a>
    <a href="principles-affinity-full.html" class="active">亲和原则</a>
  </nav>
</header>

<div class="page-wrapper">

  <aside id="module-sidebar"></aside>

  <main class="main-content">
'''

FOOTER_HTML = '''
  </main></div>

<footer class="site-footer">
  模块 03 · 亲和原则 · 社区AI亲和分析
</footer>

<script src="assets/js/site-config.js"></script>
<script src="assets/js/site-init.js"></script>
<script src="assets/js/module-sidebar.js"></script>
</body>
</html>'''


# ─── Cell data from principles-affinity-full.html ───────────────────────────
# Keyed by filename, contains: has_content, has_design, has_dev, content_td, design_td, dev_td

PRINCIPLE_DATA = {

'principles-timeliness.html': {
    'data_page': 'timeliness',
    'title': '版本外显',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': '<strong>每个文档页面必须在其元数据区域以结构化（机器可优先读）和自然语言（人类可读）两种形式，明确声明</strong>：产品/项目名称、文档对应的软件版本号（遵循SemVer）、该版本的发布日期、该版本的生命周期状态（如当前稳定版、维护中、已启用、EOS）、（可选）文档版本自身的版本号。所有版本差异必须使用表格进行条目化描述，禁止使用模糊散文。',
    'design_td': '<strong>版本元数据展示，不使用JS动态渲染</strong>：<br>在页面固定位置（参考 NV 放顶部导航栏或 H1 下方）展示产品名、版本号、发布日期、生命周期状态，位置全站统一。<br><strong>生命周期状态标签</strong>：<br>稳定版、维护中、已弃用、EOS 用不同颜色的标签组件区分，与失效状态原则的警告色保持一致的色彩语义体系，不能各自定义颜色。<br><strong>版本差异表格样式（可选）</strong>：<br>版本对比内容必须用表格呈现，表格列头（版本号、差异项、说明）样式清晰，设计上禁止用列表或段落替代表格来呈现版本差异。',
    'dev_td': '<strong>版本元数据结构化字段</strong>：<br>CMS 中为每个页面增加强制填写的结构化字段：product-name、software-version（SemVer 格式校验）、release-date、lifecycle-status，发布时校验必填，缺失则阻断。<br><strong>元数据机器可读输出</strong>：<br>版本信息同步写入页面 &lt;head&gt; 的 &lt;meta&gt; 标签和 JSON-LD，如 softwareVersion、datePublished、releaseNotes 字段，供大模型直接读取，不依赖解析页面正文。<br><strong>SemVer 格式校验</strong>：<br>CMS 在版本号字段录入时强制校验 SemVer 格式（X.Y.Z），拒绝模糊写法如"最新版"、"V2"。<br><strong>版本元数据在大纲接口中透传</strong>：<br>页面大纲接口返回结果中包含版本元数据字段，大模型消费接口时可直接获取版本上下文，无需进入页面解析。',
},

'principles-a2.html': {
    'data_page': 'a2',
    'title': '失效/弃用状态显化',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': '失效状态显性化：版本、上线、废弃、灰度、兼容边界明确写明，AI自动过滤失效内容；已废弃章节在页顶展示弃用提示，并链接代替文档。<br>a. <strong>功能/接口失效</strong>：任何已弃用、将下线、或对特定环境无效的功能、API端点、配置参数，必须在描述它的最靠近的标题下方使用显著的警告块进行标记。该警告必须说明：弃用/失效的时间点（或版本）、影响范围、以及代替方案（链接到新文档）。<br>b. <strong>文档失效</strong>：对于已停止维护的文档版本或章节，必须在页面顶部（H1上方）展示一个清晰的提示框，说明"此文档适用于已停止维护的[产品名]vX.Y"，并提供一个指向最新版本推荐文档的醒目链接。',
    'design_td': '<strong>警告块组件规范</strong>：<br>功能/接口失效的警告块需要有统一的视觉样式（颜色、图标、边框），与普通提示框、信息框明确区分，视觉权重足够高，用户不会忽略。<br><strong>页顶文档失效提示框</strong>：<br>位置固定在 H1 上方，样式与正文完全隔离（如全宽背景色条），包含失效说明文本和指向新文档的醒目链接，不能被页面其他内容淹没。',
    'dev_td': '<strong>失效状态元数据字段</strong>：<br>CMS 中为每个页面和内容块增加结构化字段，包括 status（active / deprecated / sunset）、deprecated-since（版本或时间）、replacement-url（替代文档链接），与内容分离管理，不依赖人工在正文中手写。<br><strong>失效内容的机器可读标注</strong>：<br>废弃警告块加 data-status="deprecated"、data-since="vX.Y"、data-replacement="url" 属性，大模型抓取时可直接识别该内容块的有效性，自动过滤或降权失效内容。<br><strong>页顶提示框自动渲染</strong>：<br>当页面 status 字段为 deprecated 时，由模板自动在 H1 上方注入提示框，不依赖内容侧手动添加，避免遗漏。<br><strong>失效内容在大纲接口中标注</strong>：<br>在大纲接口中为每个内容块带上 status 字段，供大模型在消费大纲时直接过滤失效章节，无需进入页面逐一判断。',
},

'principles-structure-metadata.html': {
    'data_page': 'structure-metadata',
    'title': '元数据丰富化',
    'has_content': True,
    'has_design': False,
    'has_dev': True,
    'content_td': '<strong>每个文档页面建议在 &lt;head&gt; 中包含丰富的结构化元数据，优先使用JSON-LD格式，至少嵌入</strong>：@type（TechArticle / HowTo / FAQPage）、headline、description（150–160字符）、inLanguage、datePublished、dateModified、keywords、author/publisher。',
    'dev_td': '<strong>JSON-LD 模板化输出</strong>：<br>在页面模板中统一注入 JSON-LD，字段从 CMS 结构化数据中动态读取，覆盖所有文档页面，不依赖人工逐页添加。<br><strong>必填字段完整性校验</strong>：<br>发布流程中检测 JSON-LD 是否包含所有必填字段（@type、headline、description、inLanguage、datePublished、dateModified、keywords、author/publisher），缺失字段则阻断发布。<br><strong>@type 按页面类型自动匹配</strong>：<br>文档类型（HowTo、TechArticle、FAQPage 等）在 CMS 中作为页面属性维护，JSON-LD 的 @type 由系统根据页面类型自动填入，不依赖人工判断。',
},

'principles-image.html': {
    'data_page': 'image',
    'title': '图片内容转译',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': '架构图、流程图、时序图、界面截图关键信息、核心结论采用文本介绍，图片做辅助展示。<br>a. <strong>替代文本</strong>：每一张图（&lt;img&gt;）必须提供非空的alt属性，简洁描述图片的内容和功能。<br>b. <strong>禁止"见上图/下图"</strong>：正文中禁止出现"见上图/下图"等仅依赖视觉位置进行引用的语句，图片引用必须将图片中的关键信息用文字复述一遍。<br>c. <strong>复杂图表转写</strong>：对于包含复杂逻辑的图表，必须在图片下方提供一个"图表内容转写"段落，用文字完整描述图表所表达的全部关键信息。<br>d. <strong>替代格式优先</strong>：对于流程图、时序图、架构图，优先使用Mermaid等文本可渲染的图表格式代替不可读的PNG/JPG图片。<br>e. <strong>装饰图片</strong>：纯装饰性的图标、分割线图片等，应使用CSS背景图或标记 alt=""（空字符串）。',
    'design_td': '<strong>图表格式规范</strong>：<br>所有流程图、时序图、架构图，在交付给研发时优先提供 Mermaid 源码，而不是导出 PNG/JPG；如果 Mermaid 表达不了，提供 SVG 源文件。<br><strong>图片排版预留 figcaption 位</strong>：<br>每张图片下方在设计稿中预留 figcaption 注释区域，作为内容转写的展示位，纳入排版规范，不能设计成没有这个位置的图文布局。<br><strong>复制链接按钮设计</strong>：<br>在 figcaption 段落旁设计"复制链接"按钮，以及点击后的 toast 轻提示样式（文案如"已复制链接"，持续约 2 秒后消失），需出现在每个 figcaption 区域。<br><strong>装饰性图片识别</strong>：<br>在设计交付标注中，明确标出哪些图片是装饰性的（图标、分割线等），告知研发这些元素标记 aria-hidden="true" 或使用 CSS 背景图实现。',
    'dev_td': '<strong>HTML 结构实现</strong>：<br>每张图片用 &lt;figure&gt; + &lt;figcaption&gt; 包裹，&lt;img&gt; 上填写 alt、title、data-llm-transcription 三个字段，每个 &lt;figure&gt; 需要有唯一 id 作为锚点。<br><strong>复制链接按钮功能</strong>：<br>figcaption 旁实现"复制链接"按钮，点击后将当前图片的锚点 URL 写入剪贴板，同时触发 toast 提示"已复制链接"，2秒后自动消失。<br><strong>Mermaid / SVG 渲染支持</strong>：<br>研发侧引入 Mermaid 渲染库，支持在文档内容中直接嵌入 Mermaid 代码块并渲染为可交互图表；SVG 图表直接内联到 HTML 中，而不是作为 &lt;img&gt; 引用，保证文本可提取。<br><strong>Chunk 切片管道</strong>：<br>将每张图片的 alt + figcaption 文字 + 图片前后的正文段落拼接为一个连续文本块，作为该图片的语义 chunk 供向量化索引使用；装饰性图片（aria-hidden="true"）跳过，不参与切片。',
},

'principles-hotzone.html': {
    'data_page': 'hotzone',
    'title': '图片热区转译',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': '<strong>对于包含可点击区域（ImageMap，即带有 &lt;map&gt; 和 &lt;area&gt; 标签的图片），图片下方必须提供一个完整的、无序列表样式的链接清单，清单中列出所有热区对应的跳转目标。每个清单项必须包含</strong>：热区所代表的描述性文字，以及完整的跳转URL；禁止在清单中使用"区域1"、"链接2"等无意义的描述。',
    'design_td': '<strong>热区语义文案交付</strong>：<br>设计交付时，针对每一个 &lt;area&gt; 热区，同步提供：a. 描述性文字（热区代表的阶段名、文档名或功能名，禁止用"区域1""链接2"等无意义文字）；b. alt 文案（填入 &lt;area alt&gt;，一句话描述跳转目标）；c. title 文案（补充热区的上下文说明）。<br><strong>热区链接清单设计</strong>：<br>在图片下方的 figcaption 区域内，预留热区链接清单的展示位，样式为无序列表，每项包含描述性文字和跳转目标，与 figcaption 图意转写并排或紧随其后。',
    'dev_td': '<strong>&lt;area&gt; 标签补全</strong>：<br>每个 &lt;area&gt; 必须填写 alt 和 title，href 必须为绝对 URL，禁止使用相对路径。<br><strong>&lt;nav&gt; 文本链接清单实现</strong>：<br>在每个带有 &lt;map&gt; 的图片下方，用 &lt;nav&gt; 包裹一个无序列表，覆盖全部热区目标，&lt;a&gt; 标签内必须有描述性锚文本，href 为绝对 URL，与 figcaption 图意转写组合展示。<br><strong>绝对 URL 转换</strong>：<br>构建管道中自动将 &lt;area href&gt; 和 &lt;nav&gt; 内 &lt;a href&gt; 的相对路径转换为绝对 URL，确保机器可直接引用和跳转。<br><strong>Chunk 切片管道</strong>：<br>针对热区图片额外提取 &lt;nav&gt; 内的链接清单文本，与 data-llm-transcription、figcaption、周围正文拼接为一个完整 chunk。',
},

'principles-table.html': {
    'data_page': 'table',
    'title': '表格语义化',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': '表格中的符号需要替换为文本。<br>a. <strong>符号替换</strong>：表格单元格中禁止使用仅靠形状表达含义的符号，如 ✅、❌、-、N/A 等，所有状态必须使用完整的文字表达，如"是/否"、"支持/不支持"。<br>b. <strong>结构化标题</strong>：表格必须使用 &lt;caption&gt; 标签提供表格标题/摘要，列名称必须使用 &lt;th&gt; 标签。<br>c. <strong>作用域</strong>：&lt;th&gt; 标签应尽可能指定 scope="col" 或 scope="row"。',
    'design_td': '<strong>符号替换规范</strong>：<br>建立表格内容写作规范，明确禁止使用仅靠形状表达含义的符号，所有状态必须用完整文字表达，纳入内容审核流程。<br><strong>表格标题文案交付</strong>：<br>每张表格交付时同步提供 &lt;caption&gt; 文案，格式为"表N 描述性标题"，如"表1 Ascend C Add算子设计规格"，禁止使用"表格1""数据表"等无意义文字。<br><strong>复杂表格结构标注</strong>：<br>复杂规格表（如含 I/O 子表、合并单元格、多级表头）在设计交付标注中明确：哪些单元格是表头（用 &lt;th&gt;），哪些是数据（用 &lt;td&gt;）；表头的作用域方向（scope="col" 或 scope="row"）；接口列表区域标注为独立列表结构，不拆成伪数据行。',
    'dev_td': '<strong>表格完整语义结构实现</strong>：<br>所有表格使用完整语义结构，&lt;caption&gt; 写入表格标题，&lt;thead&gt; 包裹 &lt;th&gt;，&lt;th&gt; 指定 scope，&lt;tbody&gt; 包裹数据行。<br><strong>复杂规格表 I/O 子表实现</strong>：<br>I/O 子表的 name / shape / data type / format 列必须使用 &lt;th&gt; 表头，禁止用样式伪装成表头的 &lt;td&gt;；行级表头使用 scope="row"。<br><strong>Chunk 切片管道追加规则</strong>：<br>&lt;caption&gt; 内容作为表格 chunk 的标题元数据；&lt;th scope="col"&gt; 内容作为列名前缀，拼接到每个数据单元格；接口列表（&lt;ul&gt;）与所属表格绑定为同一 chunk，不拆分；优先使用 Markdown 副本入库，HTML 表格作为降级来源。',
},

'principles-code.html': {
    'data_page': 'code',
    'title': '代码块语义化',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': '代码示例格式清晰，提供完整可运行示例和预期输出。<br>a. <strong>独立可运行</strong>：代码示例应尽可能自包含，用户可以复制后直接运行。<br>b. <strong>语言标注</strong>：每个代码块必须标注编程语言（如 python、cpp）。<br>c. <strong>注释清晰</strong>：关键行应包含注释，解释其作用。<br>d. <strong>预期输出</strong>：对于执行类代码，应在代码块后提供"预期输出"块。<br>e. <strong>格式分离</strong>：代码行号应由前端CSS或代码高亮库生成，严禁在代码文本中手动写入行号。<br>f. <strong>区块语义</strong>：代码块应使用 &lt;pre&gt;&lt;code&gt; 语义标签包裹。',
    'design_td': '<strong>定义代码块组件规范</strong>：<br>设计代码块组件，包含：a. 顶部元信息栏（文件名、语言类型、适用场景，如 hello_world.cu | C++ | 基础编译场景）；b. 代码区（行号由 CSS 渲染，不出现在可选中文本中）；c. 底部预期输出块（执行类代码必须配套，样式与代码块区分）；d. 右上角复制按钮。纳入设计系统组件库。<br><strong>预期输出块样式设计</strong>：<br>预期输出块与代码块视觉上明确区分，标题固定为"预期输出"，不使用"输出结果""运行结果"等变体，纳入格式规范。<br><strong>元信息文案交付</strong>：<br>内容交付时，每个代码块同步提供：文件名（如有）、语言类型、适用场景描述（一句话）、预期输出内容。',
    'dev_td': '<strong>&lt;pre&gt;&lt;code&gt; 语义结构实现</strong>：<br>所有代码块使用 &lt;pre&gt;&lt;code&gt; 包裹，&lt;code&gt; 上标注 language-xxx 类名，禁止使用 highlighttable 表格布局。<br><strong>行号 CSS 渲染，禁止写入文本节点</strong>：<br>行号通过 CSS counter 实现，不写入 &lt;code&gt; 文本内容，确保复制代码时不包含行号，切片管道拿到的是纯净代码文本。<br><strong>HTML 实体解码</strong>：<br>切片管道入模前，将代码文本中的 HTML 实体还原为可读字符。<br><strong>弃用 highlighttable 布局</strong>：<br>将现有使用 highlighttable 表格承载代码的结构全部迁移为 &lt;pre&gt;&lt;code&gt; 结构；构建管道中加入检测，发现 highlighttable class 时阻断发布。<br><strong>Chunk 切片管道追加规则</strong>：<br>提取 &lt;code class="language-xxx"&gt; 的语言类型作为 chunk 元数据；提取 .code-meta 内的文件名和场景描述，拼接到代码 chunk 头部；code-output 块与对应代码块绑定为同一 chunk，不拆分。',
},

'principles-link.html': {
    'data_page': 'link',
    'title': '链接语义化',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': '内容引用超链接采用描述性、可见文字显性标注跳转目标，实现AI可访问性和搜索索引性。<br>a. <strong>描述性锚文本</strong>：超链接的可点击文本必须能够在不依赖上下文的情况下，独立描述链接的目标内容或操作；禁止使用"点击这里"、"更多"、"链接"作为锚文本。<br>b. <strong>站外来源标注</strong>：对于指向其他域名的链接，应在锚文本旁添加显式标识，如[外部]或图标+目标域名。<br>c. <strong>内联上下文</strong>：链接应嵌入在具有上下文的句子中，而不是孤立地列出。<br>d. <strong>用途说明</strong>：对于下载链接、API参考链接等，可在链接后附带括号说明文件类型、大小或用途。',
    'design_td': '<strong>锚文本写作规范</strong>：<br>建立链接文案规范，纳入内容审核流程，同时覆盖正文链接和热区链接：a. 锚文本必须能独立描述跳转目标，脱离上下文也能理解；b. 禁止使用"点击这里""更多""链接""查看详情"作为锚文本；c. 下载链接、API 链接在锚文本后附带括号说明文件类型、大小、用途；d. 热区的 area alt / area title 文案同步提供，禁止使用"区域1""链接2"等无意义文字。',
    'dev_td': '<strong>描述性锚文本实现</strong>：<br>正文 &lt;a&gt; 标签内必须有描述性文字，href 为绝对 URL；下载链接和 API 链接在锚文本后附带 &lt;span&gt; 说明用途，不影响链接本身的语义。<br><strong>站外链接自动标识</strong>：<br>构建管道中检测 &lt;a href&gt; 是否跨域，跨域链接自动注入外部标识和 rel="noopener noreferrer" 属性，同时添加 data-external="true" 供切片管道识别。<br><strong>Chunk 切片管道追加规则</strong>：<br>提取每个 &lt;a&gt; 的锚文本 + href，拼接为"锚文本 → 绝对URL"格式，纳入所在段落的 chunk；站外链接在 chunk 中标注来源域名；裸 URL（无锚文本的 &lt;a&gt;）标记为低质量，降低索引权重。',
},

'principles-note.html': {
    'data_page': 'note',
    'title': '安全警示语义化',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': 'Note、注意、警告等安全警示提示正文在页面上完整展示，不折叠、不同tooltip藏字。<br>a. <strong>完整可见</strong>：所有安全警示内容必须完全在页面上展示，禁止使用折叠块、点击展开、鼠标悬停Tooltip、模态框等需要用户交互才能看到完整内容的方式。<br>b. <strong>文字前缀</strong>：警示信息必须使用文字前缀明确表示其类型，如"注意"、"警告"、"危险"；禁止仅使用图标来传递类型信息。<br>c. <strong>结构化</strong>：建议为不同类型的安全警示定义固定的CSS类。',
    'design_td': '<strong>警示块完整展示</strong>：<br>所有 Note/注意/警告内容必须直接渲染在页面上，禁止折叠、tooltip、模态框等交互形式，设计稿不出现任何需要点击才能看到警示内容的方案。<br><strong>文字前缀必须可见</strong>：<br>警示类型必须用文字（"注意："、"警告："、"危险："）标注，图标只能作为辅助装饰，不能作为唯一的类型标识。<br><strong>不同警示级别的视觉区分</strong>：<br>Note、注意、警告、危险用不同颜色的容器组件区分，颜色语义全站统一（如黄色=注意、红色=危险），与失效状态、生命周期状态的色彩体系保持一致。',
    'dev_td': '<strong>data-admonition-type 属性标注</strong>：<br>每个警示块容器加 data-admonition-type="note|warning|tip|danger"，大模型可直接识别警示级别，不依赖解析图标或颜色。<br><strong>文字前缀写入 DOM</strong>：<br>警示类型文字（"注意："、"警告："）必须作为真实文本节点输出到 HTML，禁止通过 CSS 伪元素 ::before 或图片生成，确保爬虫和大模型能直接读取。<br><strong>嵌套层级保留</strong>：<br>步骤列表 &lt;ol&gt;&lt;li&gt; 内嵌的警示块，DOM 结构中必须保持嵌套关系，禁止渲染时扁平化输出，确保大模型能识别"这条警告属于第几步"。',
},

'principles-tab.html': {
    'data_page': 'tab',
    'title': '隐藏语义：Tab/折叠全量展开',
    'has_content': True,
    'has_design': True,
    'has_dev': True,
    'content_td': '避免折叠、隐藏或采用交互形式内容。<br>a. <strong>避免交互内容</strong>：核心文档内容应该以静态HTML/Markdown的形式存在；应避免使用依赖JavaScript才能显示内容的交互式组件（Tab标签页、折叠/手风琴块、轮播图、动态加载）。<br>b. <strong>Tab全量可见</strong>：如果必须使用Tab页签页，则必须提供一种无需点击即可访问所有Tab内容的方法。<br>c. <strong>折叠默认展开</strong>：如果必须使用折叠组件（如&lt;details&gt;），其open属性必须默认为true；关键步骤和说明禁止放在折叠区内。<br>d. <strong>折叠标题可读</strong>：折叠组件的标题（&lt;summary&gt;）必须包含有语义的文本。',
    'design_td': '<strong>避免隐藏</strong>：<br>如果必须用 Tab，设计上需要提供"展开全部"或页面内所有 Tab 内容垂直排列的备用布局，不能仅依赖点击切换，确保所有内容无交互即可看到。<br><strong>折叠组件默认展开</strong>：<br>折叠块的设计默认状态为展开，折叠是用户主动收起的操作，而非默认隐藏内容的手段。<br><strong>禁止核心内容进折叠</strong>：<br>设计规范中明确，关键步骤、警示信息、验证区块禁止放入折叠组件，折叠只用于附录、扩展说明等非核心内容。',
    'dev_td': '<strong>禁止 display:none 隐藏内容</strong>：<br>非激活 Tab 面板和折叠内容禁止用 display:none 或 visibility:hidden 隐藏，改用不影响 DOM 可读性的方式处理视觉层叠，确保爬虫遍历到所有内容节点。<br><strong>&lt;details&gt; 强制 open 属性</strong>：<br>所有折叠组件在 SSR 输出时默认带 open 属性，用户可手动收起，但初始 HTML 中内容必须完整存在。<br><strong>&lt;summary&gt; 必须含语义文本</strong>：<br>折叠标题禁止只放图标或空节点，文本内容必须能独立描述折叠区的主题。<br><strong>Tab 面板全量输出到 HTML</strong>：<br>所有 Tab 面板内容在 SSR 首屏 HTML 中完整输出，不依赖 JS 动态注入非激活面板内容，确保爬虫一次抓取即可获得所有面板文本。',
},

'principles-format.html': {
    'data_page': 'format',
    'title': '双轨交付',
    'has_content': False,
    'has_design': False,
    'has_dev': True,
    'dev_td': '<strong>Markdown 源文件对外可访问</strong>：<br>/doc_center/source/ 路径下的 Markdown 文件必须可直接访问和下载，不做鉴权拦截，配合 robots.txt 放行和 llms.txt 索引。<br><strong>两轨内容一致性校验</strong>：<br>构建流程中对比 Markdown 源文件与生成的 HTML 内容，检测是否存在渲染层单独修改导致的内容不一致，不一致则阻断发布。<br><strong>Markdown 文件元数据同步</strong>：<br>Markdown 文件头部的 frontmatter（版本号、日期、状态等）与 HTML 页面 &lt;head&gt; 中的 meta 和 JSON-LD 字段保持自动同步，由构建管道统一处理，不依赖人工双向维护。<br><strong>HTML 源码优化</strong>：<br>不使用 .md 的渲染页面，采用 .html 渲染页面，需尽量在前端输出，不通过服务端动态渲染。',
},

}  # end PRINCIPLE_DATA


# ─── Example content extracted from existing pages ───────────────────────────
# We keep the existing demo HTML as-is under H3 "调整示例"

EXISTING_EXAMPLES = {

'principles-timeliness.html': {
    'content': '''<div class="principle-example">
        <h4>1. 版本元数据在 Frontmatter 中声明</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无版本声明</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram"># 算子开发入门

本文介绍 Ascend C 算子开发基本流程…</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整版本 Frontmatter</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">---
product: CANN
version: "9.0.0"
release_date: "2026-06-01"
lifecycle_status: stable   # stable | rc | beta | deprecated
---

# 算子开发入门

本文介绍 Ascend C 算子开发基本流程…</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 版本元数据展示</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无版本信息</h4>
          <div class="compare-col machine">
            <div class="render-frame">
              <div class="rf-h1">算子开发入门</div>
              <p class="rf-muted">页面无任何版本标注</p>
            </div>
          </div>
          <h4 class="compare-label compare-label--human">After · 版本徽章 + 生命周期标签</h4>
          <div class="compare-col human">
            <div class="render-frame"><span class="rf-badge">CANN 9.0.0</span><span class="rf-badge">稳定版</span><div class="rf-h1">算子开发入门</div></div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. 元数据写入 &lt;head&gt;</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 缺失版本元数据</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;head&gt;
  &lt;title&gt;算子开发入门&lt;/title&gt;
  &lt;!-- 无版本信息 --&gt;
&lt;/head&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整结构化元数据</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;meta name="version" content="9.0.0"&gt;
&lt;meta name="release_date" content="2026-06-01"&gt;
&lt;meta name="lifecycle_status" content="stable"&gt;
&lt;link rel="canonical" href="https://…/900/operator_dev.html"&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-a2.html': {
    'content': '''<div class="principle-example">
        <h4>1. 失效状态与替代链接在文档中声明</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无失效说明</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">---
version: "8.0.0"
---

# 旧版 API 说明

本文描述 CANN 8.0 的算子接口…</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 失效状态 + 替代方案</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">---
version: "8.0.0"
lifecycle_status: deprecated
deprecated_since: "9.0.0"
replaced_by: https://…/900/operator_dev.html
---

> **警告**：本文档适用于已停止维护的 CANN 8.0，
> 请参阅 [CANN 9.0 替代文档](https://…/900/)。

# 旧版 API 说明

本文描述 CANN 8.0 的算子接口…</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 文档顶部失效横幅</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无失效提示</h4>
          <div class="compare-col machine">
            <div class="render-frame">
              <div class="rf-h1">旧版 API 说明</div>
              <p class="rf-muted">用户无法判断文档是否已弃用</p>
            </div>
          </div>
          <h4 class="compare-label compare-label--human">After · 显著失效横幅</h4>
          <div class="compare-col human">
            <div class="render-frame"><div class="rf-banner">⚠ 本文档已废弃（CANN 8.0 起）· <a href="#">见 CANN 9.0 替代文档</a></div><div class="rf-h1">旧版 API 说明</div></div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. 机器可读的失效状态标注</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无结构化状态</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;link rel="canonical" href="…"&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整失效元数据</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;link rel="canonical" href="https://…/900/operator_dev.html"&gt;
&lt;meta name="lifecycle_status" content="deprecated"&gt;
&lt;div data-status="deprecated" data-since="8.0"
     data-replacement="https://…/900/"&gt;…&lt;/div&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-structure-metadata.html': {
    'content': '''<div class="principle-example">
        <h4>1. Frontmatter 中补充完整元数据字段</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 仅标题与版本</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">---
title: 算子开发入门
version: "9.0.0"
---</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整结构化元数据</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">---
title: 算子开发入门
description: "面向已完成环境安装的开发者，介绍
  Ascend C 算子开发基本流程与工程结构。（78字）"
version: "9.0.0"
date_published: "2026-01-01"
date_modified: "2026-06-01"
in_language: zh-CN
keywords: [Ascend C, 算子开发, CANN, 入门]
author: 昇腾文档团队
schema_type: TechArticle
---</pre>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. JSON-LD 结构化元数据</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无 JSON-LD</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;head&gt;
  &lt;title&gt;算子开发入门&lt;/title&gt;
&lt;/head&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整 JSON-LD</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;script type="application/ld+json"&gt;
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "算子开发入门",
  "description": "面向已完成环境安装的开发者介绍 Ascend C 算子开发基本流程（150字以内）",
  "inLanguage": "zh-CN",
  "datePublished": "2026-01-01",
  "dateModified": "2026-06-01",
  "version": "9.0.0"
}
&lt;/script&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-image.html': {
    'content': '''<div class="principle-example">
        <h4>1. 图片 alt 文本与内容转写段落</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无 alt 与转写</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">如图所示，Ascend C API 层次如下：

![](api-arch.png)</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · alt + 内容转写段落</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">Ascend C API 自下而上分为五层：语言扩展层 C API、
基础 API、高阶 API、算子模板库、Python 前端。

![Ascend C 多层级 API 体系架构图](api-arch.svg)

*图1 Ascend C API 自下而上分为五层：语言扩展层
C API、基础 API、高阶 API、算子模板库、Python 前端。*</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 图片格式规范（Mermaid 优先）</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · PNG 图片</h4>
          <div class="compare-col machine">
            <div class="render-frame"><div class="rf-img-placeholder">流程图（PNG）</div><p class="rf-muted">爬虫无法解析图中文字</p></div>
          </div>
          <h4 class="compare-label compare-label--human">After · Mermaid 文本图表</h4>
          <div class="compare-col human">
            <div class="render-frame"><pre class="rf-code">graph LR; A[源码] --&gt; B[bisheng] --&gt; C[kernel]</pre><p class="rf-caption"><strong>图2</strong> Ascend C 编译流程（Mermaid）</p></div>
          </div>
        </div>
      </div>

      <div class="principle-example">
        <h4>2. 图片排版预留正文转译位置</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无 figcaption 位</h4>
          <div class="compare-col machine">
            <div class="render-frame">
              <div class="rf-img-placeholder">API 层级架构图</div>
              <p class="rf-muted">图片下方无任何说明区域</p>
            </div>
          </div>
          <h4 class="compare-label compare-label--human">After · 图片 + figcaption 转译区</h4>
          <div class="compare-col human">
            <div class="render-frame">
              <div class="rf-img-placeholder">API 层级架构图</div>
              <p class="rf-caption"><strong>图1</strong> Ascend C 多层级 API 体系</p>
              <div class="rf-transcript"><strong>图片内容转写：</strong>Ascend C API 自下而上分为五层：1. 语言扩展层 C API；2. 基础 API；3. 高阶 API；4. 算子模板库；5. Python 前端。</div>
            </div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. figure + figcaption 语义结构</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 裸 &lt;img&gt;</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;img src="api-arch.png"&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整语义结构</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;figure id="fig-api-arch"&gt;
  &lt;img src="api-arch.svg"
       alt="Ascend C 多层级 API 体系架构图"
       data-llm-transcription="API 自下而上分为五层：…"&gt;
  &lt;figcaption&gt;图1 Ascend C API 自下而上分为五层：
  语言扩展层 C API、基础 API、高阶 API、
  算子模板库、Python 前端。&lt;/figcaption&gt;
&lt;/figure&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-hotzone.html': {
    'content': '''<div class="principle-example">
        <h4>1. 热区图片下方补充文本链接清单</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 仅热区，无链接清单</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">![成长地图](roadmap.png)
<!-- 热区跳转仅靠坐标，文本中无链接可读 --></pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 图片 + 完整链接清单</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">![成长地图——含四个阶段热区](roadmap.png)

**成长地图导航：**

- [环境准备与 CANN 安装](https://…/install.html)
- [首个 Ascend C 算子样例](https://…/helloworld.html)
- [算子调试与性能分析](https://…/debug.html)
- [性能优化最佳实践](https://…/optimize.html)</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 描述性热区文案</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无意义热区文案</h4>
          <div class="compare-col machine">
            <div class="render-frame"><ul class="rf-nav-links"><li><a href="#">区域1</a></li><li><a href="#">链接2</a></li></ul></div>
          </div>
          <h4 class="compare-label compare-label--human">After · 描述性锚文本</h4>
          <div class="compare-col human">
            <div class="render-frame"><ul class="rf-nav-links"><li><a href="#">环境准备与 CANN 安装</a></li><li><a href="#">首个 Ascend C 算子样例</a></li></ul></div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. &lt;area&gt; + &lt;nav&gt; 链接清单实现</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 仅坐标热区</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;area shape="rect" coords="0,0,120,40"
      href="/install"&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整语义实现</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;area shape="rect" coords="0,0,120,40"
      href="https://…/install.html"
      alt="环境准备与 CANN 安装"&gt;
&lt;nav aria-label="成长地图"&gt;
  &lt;ul&gt;
    &lt;li&gt;&lt;a href="https://…/install.html"&gt;
      环境准备与 CANN 安装&lt;/a&gt;&lt;/li&gt;
  &lt;/ul&gt;
&lt;/nav&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-table.html': {
    'content': '''<div class="principle-example">
        <h4>1. 符号替换为文字 + 补充表格标题</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 符号 + 无标题</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">| 功能    | 支持 |
|---------|------|
| Add 算子 | ✅  |
| Sub 算子 | ❌  |</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 文字状态 + 描述性标题</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">**表1 算子支持情况**

| 功能     | 支持状态 |
|----------|----------|
| Add 算子 | 支持     |
| Sub 算子 | 不支持   |</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 表格标题与符号替换规范</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 符号 + 无标题</h4>
          <div class="compare-col machine">
            <div class="render-frame"><table class="rf-table"><tr><th>name</th><th>shape</th><th>支持</th></tr><tr><td>x</td><td>(8,2048)</td><td>✅</td></tr></table></div>
          </div>
          <h4 class="compare-label compare-label--human">After · 含 caption 与文字状态</h4>
          <div class="compare-col human">
            <div class="render-frame"><table class="rf-table"><caption>表1 Ascend C Add算子设计规格</caption><tr><th scope="col">name</th><th scope="col">shape</th><th scope="col">支持状态</th></tr><tr><td>x</td><td>(8,2048)</td><td>支持</td></tr></table></div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. 完整语义 HTML 表格</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无语义表格</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;table&gt;
  &lt;tr&gt;&lt;td&gt;name&lt;/td&gt;&lt;td&gt;shape&lt;/td&gt;&lt;/tr&gt;
  &lt;tr&gt;&lt;td&gt;x&lt;/td&gt;&lt;td&gt;(8,2048)&lt;/td&gt;&lt;/tr&gt;
&lt;/table&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整语义结构</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;table&gt;
  &lt;caption&gt;表1 Ascend C Add算子设计规格&lt;/caption&gt;
  &lt;thead&gt;
    &lt;tr&gt;&lt;th scope="col"&gt;name&lt;/th&gt;
        &lt;th scope="col"&gt;shape&lt;/th&gt;&lt;/tr&gt;
  &lt;/thead&gt;
  &lt;tbody&gt;
    &lt;tr&gt;&lt;td&gt;x&lt;/td&gt;&lt;td&gt;(8, 2048)&lt;/td&gt;&lt;/tr&gt;
  &lt;/tbody&gt;
&lt;/table&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-code.html': {
    'content': '''<div class="principle-example">
        <h4>1. 语言标注 + 预期输出块</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无语言标注，无预期输出</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">```
__aicore__ inline void Add(...) {
    Add(z, x, y, TILE_LENGTH);
}
```</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 语言 + 注释 + 预期输出</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">```cpp
// kernel_add.cpp · Ascend C · 矢量加法算子示例
__aicore__ inline void Add(
    const LocalTensor&lt;float&gt; &amp;z,
    const LocalTensor&lt;float&gt; &amp;x,
    const LocalTensor&lt;float&gt; &amp;y) {
    Add(z, x, y, TILE_LENGTH); // 执行向量加法
}
```

**预期输出：**

```
[INFO] kernel Add executed successfully.
```</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 代码块组件规范</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无元信息 / 无复制按钮</h4>
          <div class="compare-col machine">
            <div class="render-frame"><pre class="rf-code">#include &lt;acl/acl.h&gt;
int Init() { … }</pre></div>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整代码块组件</h4>
          <div class="compare-col human">
            <div class="render-frame"><div class="rf-code-head">kernel_add.cpp · Ascend C · 矢量算子示例</div><pre class="rf-code">// kernel 实现…</pre></div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. &lt;pre&gt;&lt;code&gt; 语义结构替代 highlighttable</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · highlighttable 布局</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;table class="highlighttable"&gt;
  &lt;tr&gt;&lt;td class="linenos"&gt;1&lt;/td&gt;
      &lt;td class="code"&gt;…&lt;/td&gt;&lt;/tr&gt;
&lt;/table&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 纯净 &lt;pre&gt;&lt;code&gt;</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;pre&gt;&lt;code class="language-cpp"&gt;
__aicore__ inline void Add(
  const LocalTensor&lt;float&gt; &amp;z,
  const LocalTensor&lt;float&gt; &amp;x,
  const LocalTensor&lt;float&gt; &amp;y) {
    Add(z, x, y, TILE_LENGTH);
}
&lt;/code&gt;&lt;/pre&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-link.html': {
    'content': '''<div class="principle-example">
        <h4>1. 描述性锚文本</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无意义锚文本</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">完整样例请参考[点击这里](https://gitcode.com/…)。</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 描述性锚文本</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">完整样例请参考
[HelloWorld 完整样例（GitCode）](https://gitcode.com/…)。</pre>
          </div>
        </div>
      </div>

      <div class="principle-example">
        <h4>2. 站外链接标注来源 + 下载链接说明用途</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无来源 / 无用途说明</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">- [示例仓库](https://gitcode.com/…)
- [下载](https://…/toolkit.run)</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 来源 + 用途标注</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">- [示例仓库（↗ gitcode.com）](https://gitcode.com/…)
- [CANN Toolkit 离线包（Linux x86_64，约 3 GB）](https://…/toolkit.run)</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 锚文本规范对比</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 模糊锚文本</h4>
          <div class="compare-col machine">
            <div class="render-frame"><p>更多信息 <a href="#">查看详情</a></p></div>
          </div>
          <h4 class="compare-label compare-label--human">After · 自解释锚文本</h4>
          <div class="compare-col human">
            <div class="render-frame"><p>环境变量配置步骤见 <a class="rf-link-good" href="#">安装后环境变量设置</a>（需 root 权限）。</p></div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. &lt;a&gt; 标签完整属性</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 裸链接</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;a href="/helloworld"&gt;点击这里&lt;/a&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 完整语义链接</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;a href="https://gitcode.com/…/helloworld"
   title="HelloWorld 完整样例（C++ · GitCode）"
   rel="nofollow noopener" target="_blank"&gt;
  HelloWorld 完整样例（GitCode）
&lt;/a&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-note.html': {
    'content': '''<div class="principle-example">
        <h4>1. 完整警示正文 + 文字前缀</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 折叠 / 仅图标，无文字前缀</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">安装 CANN 后需进行环境配置。
<!-- 警示内容被折叠或藏在 tooltip 中 --></pre>
          </div>
          <h4 class="compare-label compare-label--human">After · blockquote 展开 + 文字前缀</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">安装 CANN 后需进行环境配置。

> **注意**：安装 CANN 后，需执行
> `source ${INSTALL_DIR}/set_env.sh`
> 设置环境变量，否则无法调用算子 API。</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 警示级别视觉区分</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 所有警示同样式</h4>
          <div class="compare-col machine">
            <div class="render-frame"><div class="rf-note"><span>注意：</span>...</div><div class="rf-note"><span>警告：</span>...</div></div>
          </div>
          <h4 class="compare-label compare-label--human">After · 颜色区分级别</h4>
          <div class="compare-col human">
            <div class="render-frame"><div class="rf-note rf-note--info"><span class="rf-note-label">注意：</span>安装 CANN 后需设置环境变量。</div><div class="rf-note rf-note--good"><span class="rf-note-label">警告：</span>升级前请备份 /usr/local/Ascend。</div></div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. data-admonition-type 标注</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无语义属性</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;div class="note"&gt;
  ⚠ 升级前请备份…
&lt;/div&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 语义化警示标注</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;div class="admonition"
     data-admonition-type="warning"&gt;
  &lt;span class="admonition-label"&gt;警告：&lt;/span&gt;
  升级前请备份 /usr/local/Ascend。
&lt;/div&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-tab.html': {
    'content': '''<div class="principle-example">
        <h4>1. 避免 Tab 隐藏内容，改用标题区分</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · Tab 结构，仅一个面板可读</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram"><!-- 在线安装 Tab（激活） -->
在线安装步骤：wget … ./toolkit.run --install

<!-- 离线安装 Tab（隐藏，爬虫不可见） --></pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 平铺结构，所有内容可读</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">### 在线安装（x86_64 · CANN 9.0.0）

```bash
wget … ./Ascend-cann-toolkit_9.0.0_linux-x86_64.run
./Ascend-cann-toolkit_9.0.0_linux-x86_64.run --install
```

### 离线安装（x86_64 · CANN 9.0.0）

```bash
./Ascend-cann-toolkit_9.0.0_linux-x86_64.run --install --offline
```</pre>
          </div>
        </div>
      </div>''',
    'design': '''<div class="principle-example">
        <h4>1. 折叠组件默认展开</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 默认收起</h4>
          <div class="compare-col machine">
            <div class="render-frame"><details><summary>离线安装步骤</summary>./toolkit.run --offline</details><p class="rf-muted">默认折叠，爬虫抓取时内容不可见</p></div>
          </div>
          <h4 class="compare-label compare-label--human">After · 默认展开</h4>
          <div class="compare-col human">
            <div class="render-frame"><details open><summary>离线安装步骤</summary>./toolkit.run --offline</details></div>
          </div>
        </div>
      </div>''',
    'dev': '''<div class="principle-example">
        <h4>1. &lt;details open&gt; 与 Tab 全量输出</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 非激活面板 display:none</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;div class="tab-panel hidden"&gt;
  离线安装步骤…
&lt;/div&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · SSR 全量输出 + details open</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;!-- source 端点全量输出所有面板 --&gt;
&lt;div class="tab-panel"&gt;离线安装步骤…&lt;/div&gt;

&lt;!-- 折叠默认展开 --&gt;
&lt;details open&gt;
  &lt;summary&gt;离线安装步骤&lt;/summary&gt;
  ./toolkit.run --install --offline
&lt;/details&gt;</pre>
          </div>
        </div>
      </div>''',
},

'principles-format.html': {
    'dev': '''<div class="principle-example">
        <h4>1. 同源双发链路</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 仅 HTML 渲染页</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">/document/detail/…/operator_dev.html
← 唯一入口，带导航/样式，不适合机器直读</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 同源双轨</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">/doc_center/source/…/operator_dev.html
        │
        ├──► 人类：/document/detail/…    渲染页（带导航/样式）
        └──► 机器：/.../operator_dev.md  管道导出 Markdown</pre>
          </div>
        </div>
      </div>

      <div class="principle-example">
        <h4>2. 机器可读入口与 Markdown frontmatter</h4>
        <div class="compare-grid compare-grid--stack compare-grid--no-mid-divider">
          <h4 class="compare-label compare-label--machine">Before · 无 Markdown 源</h4>
          <div class="compare-col machine">
            <pre class="arch-diagram">&lt;footer&gt;
  &lt;!-- 无机器可读入口 --&gt;
&lt;/footer&gt;</pre>
          </div>
          <h4 class="compare-label compare-label--human">After · 页脚入口 + frontmatter 同步</h4>
          <div class="compare-col human">
            <pre class="arch-diagram">&lt;footer class="doc-footer"&gt;
  &lt;a href="/doc_center/source/…/operator_dev.html"&gt;
    机器可读版本（source HTML）
  &lt;/a&gt;
&lt;/footer&gt;

---
source_url: /doc_center/source/…/operator_dev.html
render_url: /document/detail/…/operator_dev.html
---</pre>
          </div>
        </div>
      </div>''',
},

}  # end EXISTING_EXAMPLES


def build_suggestions_ul(td_html):
    items = items_from_table(td_html)
    if not items:
        return '<ul class="principle-suggestions"><li>（待补充）</li></ul>'
    joined = '\n        '.join(items)
    return f'<ul class="principle-suggestions">\n        {joined}\n      </ul>'


def build_section(sec_id, h2_title, h3_sug_id, h3_ex_id, suggestions_html, example_html):
    ex = example_html.strip() if example_html else '<p class="text-auxiliary">（示例待补充）</p>'
    return f'''
    <section class="section" id="{sec_id}">
      <h2>{h2_title}</h2>

      <h3 id="{h3_sug_id}">调整建议</h3>
      {suggestions_html}

      <h3 id="{h3_ex_id}">调整示例</h3>
      {ex}
    </section>'''


for fname, data in PRINCIPLE_DATA.items():
    fpath = BASE / fname
    existing = EXISTING_EXAMPLES.get(fname, {})

    sections = []

    if data.get('has_design'):
        sug = build_suggestions_ul(data.get('design_td', ''))
        ex = existing.get('design', '')
        sections.append(build_section(
            'design-ui', '设计UI调整',
            'design-suggestions', 'design-example',
            sug, ex
        ))

    if data.get('has_content'):
        sug = build_suggestions_ul(data.get('content_td', ''))
        ex = existing.get('content', '')
        sections.append(build_section(
            'content-adjust', '文档内容调整',
            'content-suggestions', 'content-example',
            sug, ex
        ))

    if data.get('has_dev'):
        sug = build_suggestions_ul(data.get('dev_td', ''))
        ex = existing.get('dev', '')
        sections.append(build_section(
            'frontend-adjust', '前端调整',
            'frontend-suggestions', 'frontend-example',
            sug, ex
        ))

    # Read existing page-header
    old_html = fpath.read_text(encoding='utf-8')
    page_header = read_page_header(old_html)

    body = HEADER_HTML.format(
        title=data['title'],
        data_page=data['data_page']
    )
    body += '\n' + page_header + '\n'
    body += '\n'.join(sections)
    body += '\n' + FOOTER_HTML

    fpath.write_text(body, encoding='utf-8')
    print(f'✓ {fname}')

print('\nDone — rebuilt', len(PRINCIPLE_DATA), 'pages.')
