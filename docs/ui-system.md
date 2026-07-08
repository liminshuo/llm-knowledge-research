# UI 系统规范

> 本研究站静态页的统一文字、间距与结构约定。CSS 入口为 `assets/css/style.css`（`@import` 子模块，见 `AGENTS.md`）；示例页：`ui-system.html`。

---

## 1. 设计令牌

### 1.1 字体

| 用途 | 字体栈 |
|------|--------|
| 全局正文 | `"PingFang SC", sans-serif` |
| 等宽 / 代码 | `"SF Mono", "Fira Code", "Cascadia Code", monospace` |

### 1.2 颜色

| 令牌 | 色值 | 用途 |
|------|------|------|
| `--color-text` | `#191919` | 主标题、正文 |
| `--color-text-secondary` | `#595959` | 辅助说明、导航未选中 |
| `--color-primary` | `#1476FF` | 链接、标签、激活态 |
| `--color-primary-dark` | `#1476FF` | 链接 hover |
| `--color-primary-light` | `#F5F5F5` | 信息框背景、导航激活底 |
| `--color-bg` | `#F5F5F5` | 页面背景 |
| `--color-surface` | `#ffffff` | 卡片、侧栏、表格面 |
| `--color-border` | `#e2e8f0` | 分割线、边框 |
| `--color-card-border` | `#F0F0F0` | `.surface-card` 描边 |
| `--color-code-bg` | `#f1f5f9` | 行内 `code` 背景 |
| `--color-code-text` | `#1e293b` | 行内 `code` 文字 |
| `--color-desc` | `rgba(0, 0, 0, 0.6)` | `.page-desc`、`.section-heading-desc` |
| `--color-primary-tint` | `rgba(20, 118, 255, 0.1)` | 主色浅底（标签、检索徽章等） |
| `--color-primary-tint-strong` | `rgba(20, 118, 255, 0.25)` | 主色描边 / hover 强调 |
| `--color-primary-subtle` | `rgba(20, 118, 255, 0.06)` | 导航激活底、侧栏选中 |
| `--color-primary-block-bg` | `rgba(20, 118, 255, 0.07)` | 第三方信源区块底 |
| `--color-success` | `#16a34a` | 成功 / 官方语义色 |
| `--color-success-bg` | `rgba(22, 163, 74, 0.08)` | 成功浅底（信息框、标签） |
| `--color-success-border` | `rgba(22, 163, 74, 0.25)` | 成功描边 |
| `--color-success-tint` | `rgba(22, 163, 74, 0.12)` | 成功徽章底 |
| `--color-warning` | `#d97706` | 警告 / 可选语义色 |
| `--color-warning-bg` | `rgba(217, 119, 6, 0.08)` | 警告浅底 |
| `--color-warning-border` | `rgba(217, 119, 6, 0.28)` | 警告描边 |
| `--color-warning-tint` | `rgba(217, 119, 6, 0.12)` | 警告徽章底 |
| `--color-danger` | `#dc2626` | 危险 / 必要语义色 |
| `--color-danger-bg` | `rgba(220, 38, 38, 0.08)` | 危险浅底 |
| `--color-danger-border` | `rgba(220, 38, 38, 0.25)` | 危险描边 |
| `--color-accent` | `#7c3aed` | 辅助强调色 |
| `--color-accent-tint` | `rgba(124, 58, 237, 0.12)` | 辅助色徽章底 |
| `--color-accent-block-bg` | `rgba(124, 58, 237, 0.07)` | 辅助色区块底 |
| `--color-principle-empirical` | `#1a56db` | 实测锚点原则文字 / 顶条 |
| `--color-principle-empirical-bg` | `#e8f0fe` | 实测锚点浅底 |
| `--color-principle-empirical-border` | `#bfcffd` | 实测锚点描边 |
| `--color-principle-generalize` | `#6d28d9` | 根因泛化原则文字 / 顶条 |
| `--color-principle-generalize-bg` | `#f5f3ff` | 根因泛化浅底 |
| `--color-principle-generalize-border` | `#ddd6fe` | 根因泛化描边 |
| `--color-principle-standard` | `#047857` | 行业标准原则文字 / 顶条 |
| `--color-principle-standard-bg` | `#ecfdf5` | 行业标准浅底 |
| `--color-principle-standard-border` | `#6ee7b7` | 行业标准描边 |
| `--color-neutral-bg` | `rgba(89, 89, 89, 0.08)` | 未知 / 中性区块底 |
| `--color-neutral-tint` | `rgba(89, 89, 89, 0.12)` | 未知 / 中性徽章底 |
| `--color-overlay` | `rgba(30, 41, 59, 0.45)` | 抽屉遮罩（基于 `--color-code-text`） |
| `--color-panel-shadow` | `rgba(30, 41, 59, 0.08)` | 侧栏面板阴影 |
| `--color-panel-shadow-strong` | `rgba(30, 41, 59, 0.12)` | 抽屉面板阴影 |

语义色浅底统一为 **8% / 12% / 25–28%** 三档透明度（底 / 徽章 / 描边），主色基于 `#1476FF`（`rgb(20, 118, 255)`）。

### 1.3 圆角与阴影

| 令牌 | 值 |
|------|-----|
| `--radius` | `8px` |
| `--shadow` | `0 1px 3px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.04)` |

### 1.4 布局 · 正文最大宽度

| 令牌 | 值 | 说明 |
|------|-----|------|
| `--content-max-width` | `1000px` | 正文内容区最大宽度（不含左右 padding） |
| `--content-wide-pad-x` | `clamp(24px, 4vw, 48px)` | 无侧栏页 / main 右内边距，随视口缩放 |
| `--content-main-pad-left-max` | `200px` | 有侧栏内页：正文距 `main.main-content` 左缘最大 padding |
| `--content-main-pad-left` | `clamp(24px, 10.4167vw, 200px)` | 有侧栏内页：`main` 左 padding；1920 视口为 **200px**（`200 ÷ 1920 ≈ 10.4167vw`），更窄视口等比缩小，下限 **24px** |
| `--content-main-pad-top-max` | `48px` | 内页 `main.main-content` 上内边距最大值（H1 距 `main` 顶缘） |
| `--content-main-pad-top` | `clamp(32px, 2.5vw, 48px)` | 正文距 `main` 顶缘；1920 视口为 **48px**（`48 ÷ 1920 = 2.5vw`），更窄视口等比缩小，下限 **32px** |
| `--sidebar-width-max` | `248px` | 模块侧栏（`#module-sidebar`）最大宽度 |
| `--sidebar-width` | `clamp(200px, 12.9167vw, 248px)` | 侧栏实际宽度：1920 视口为 **248px**，更窄视口按 `12.9167vw` 缩小，下限 **200px** |
| `--toc-width` | `200px` | 右侧本篇目录（`#page-toc`）宽度 |
| `--content-offset-left` | `calc(var(--sidebar-width) + var(--content-main-pad-left))` | 无侧栏页 `main` 左 padding：模拟侧栏占位，使 1000px 正文与有侧栏内页**左缘对齐**（1920 下 **448px** = 248 + 200） |

全站正文遵循同一原则：1920 视口下内容区宽 **1000px**；视口变窄时 `width: 100%` + `clamp` 边距自适应。模块侧栏在 1920 视口下为 **248px**（`248 ÷ 1920 ≈ 12.9167vw`），作为最大宽度，随分辨率等比收窄。

| 页面类型 | 实现 |
|----------|------|
| 无侧栏（首页、研究概览） | `<main class="main-content content-wide">`：白底满宽；`padding-left: var(--content-offset-left)`；子块 `max-width: 1000px`——与有侧栏页正文**同一水平起点** |
| 有侧栏（问题论证、亲和原则等） | 左 `#module-sidebar`（248px @1920）+ 中 `main`（`padding-left: 200px` @1920）+ 右 `#page-toc`；正文子块 `max-width: 1000px` |

| 视口 | 行为 |
|------|------|
| 宽屏（如 1920） | 正文左缘距视口 **448px**（侧栏 248 + main 左 pad 200）；宽 **1000px**；`main` 上 padding **48px**（H1 顶对齐） |
| 中间分辨率 | 侧栏与 `main` 左 padding 随 `vw` 缩小；正文最大仍 **1000px** |
| ≤ 1280px | 隐藏右侧本篇目录（`#page-toc`） |
| ≤ 900px | `main` 水平 padding **24px**；侧栏隐藏；首页模块卡片单列 |

---

## 2. 标题层级（H1–H4）

### H1 · 页面主标题

| 属性 | 值 |
|------|-----|
| 选择器 | `.page-header h1` |
| 字号 | **32px** |
| 字重 | **800** |
| 行高 | **48** |
| 颜色 | `#191919` |
| 下边距 | **32px**（至 `.page-desc`） |

> 首页 Hero 例外：`32px / 700 / line-height 1.25`，仅用于 `index.html`。

### H2 · 章节标题

| 属性 | 值 |
|------|-----|
| 选择器 | `.section h2` |
| 字号 | **24px** |
| 字重 | **700** |
| 行高 | **36** |
| 颜色 | `#191919` |
| 文字与底边线间距 | **24px**（`padding-bottom`） |
| 上边距 | **32px**|
| 下边距 | **16px**（边框线以下至下一元素） |
| 装饰 | 底边 `2px solid #f0f0f0` |

### H3 · 小节标题

| 属性 | 值 |
|------|-----|
| 选择器 | `.section h3` |
| 字号 | **18px** |
| 字重 | **700** |
| 行高 | **28px** |
| 字体 | **PingFang SC**（`--font`） |
| 颜色 | `#191919` |
| 上边距 | **32px**|
| 下边距 | **16px** |

用于「结论」「论证」「说明」等小节，不重复 H1 文案。

### H4 · 四级标题

| 属性 | 值 |
|------|-----|
| 选择器 | `.section h4` |
| 字号 | **14px** |
| 字重 | **700** |
| 颜色 | `#191919` |
| 上边距 | **24px** |
| 下边距 | **16px** |

**卡片内 H4**（`.answer-card-header h4`）：`14px / 700`。

---

## 3. 正文与说明

### 全局正文（`body`）

| 属性 | 值 |
|------|-----|
| 字号 | **14px** |
| 行高 | **22** |
| 颜色 | `#595959` |

### 页头描述（`.page-desc`）

| 属性 | 值 |
|------|-----|
| 字号 | **14px** |
| 行高 | **22px** |
| 颜色 | `rgba(0, 0, 0, 0.6)`（`--color-desc`） |

**分行版**（`.page-desc--split` + `.page-desc-line`）：

| 属性 | 值 |
|------|-----|
| 单行高 | **20px** |
| 行间距 | **4px** |

### 章节正文（`.section p`）

| 属性 | 值 |
|------|-----|
| 字号 | **14px**（继承） |
| 行高 | **22** |
| 段落下边距 | **12px** |

### 章节引导（`.section-heading-desc`）

| 属性 | 值 |
|------|-----|
| 字号 | **14px** |
| 行高 | **22px** |
| 颜色 | `rgba(0, 0, 0, 0.6)`（`--color-desc`） |
| 下边距 | **16px** |

用于章节内表格/列表前的说明，勿用 inline `style`。

### 辅助文字（`.text-auxiliary`）

| 属性 | 值 |
|------|-----|
| 字号 | **12px**（`--text-auxiliary`） |
| 行高 | **20px**（`--text-auxiliary-lh`） |
| 颜色 | `#595959`（`--color-text-secondary`） |
| 段落下边距 | **12px**（`--space-p`） |

用于语义维度等小节后、措施列表下的**实测举例 / 延伸阅读**（如「当前以抓取 … 为例，具体实测见 …」），层级低于 `.section p` 正文，勿与论证段落混用。

```html
<ul class="list-badge-led">…</ul>
<p class="text-auxiliary">当前以抓取 … 为例。具体实测见 <a href="…">问题论证 · …</a>。</p>
```

### 摘要卡片（`.summary-card`）

用于章节内一句式摘要（如「核心命题」），标签与正文合为**一个 `<p>` 正文单元**。

| 属性 | 值 |
|------|-----|
| 背景 | `#ffffff` |
| 圆角 | `8px`（`--radius`） |
| 描边 | 无 |
| 内边距 | `16px 0 24px`（左右 0） |
| 外边距 | **上 24px / 下 24px**（`margin: 24px 0`） |
| 字号 | 14px，行高 22px |

```html
<div class="summary-card">
  <p>
    <span class="cp-label">核心命题</span>
    RAG / 知识库尽量完整收录昇腾官方文档的<strong>文档语义</strong>。
  </p>
</div>
```

示例：`background-motivation.html` · 研究目标章节。

### 组件内文字

| 组件 | 字号 | 行高 |
|------|------|------|
| `.summary-card` | 14px | 22px |
| `.component-problem` | 14px | 1.65 |
| `.info-box` | 14px | 继承 |
| `.data-table` | 13.5px | 继承 |
| `.key-points li` | 14px | 继承 |
| `.cp-label` | 11px / 700 / 主色 | — |

### 代码文案（行内 `code`）

段落、列表、`list-badge-led` 中的字段名与标签片段（如 `` `alt` ``、`` `<img>` ``）统一使用**代码文案**样式，全站高度一致（**20px** = 2 + 16 + 2）。

| 令牌 / 属性 | 值 |
|------|-----|
| `--code-copy-size` | `13px` |
| `--code-copy-lh` | `16px`（固定行高，不继承正文 22px） |
| `--code-copy-pad-y` / `--code-copy-pad-x` | `2px` / `6px` |
| `--code-copy-radius` | `4px` |
| 字体 | 等宽栈（`--font-mono`） |
| 背景 / 字色 | `--color-code-bg` / `--color-code-text` |

| 选择器 | 说明 |
|------|------|
| `code` | 默认代码文案 |
| `pre` | 多行代码块容器（独立 padding） |
| `pre code` | 块内 `code` 重置为透明底、无 padding，避免双重包裹 |

### 文案解释（`.copy-explain`）

正文中的缩写或术语，用**虚线下划线**标示；悬停或键盘聚焦时浮层展示完整释义（`data-tip` 承载说明文字）。

| 属性 | 值 |
|------|-----|
| 下划线 | `1px dashed`，色 `--color-text-secondary` |
| 浮层字号 / 行高 | 12px / 1.5 |
| 浮层最大宽 | 300px |
| 浮层背景 | `--color-text`，白字 |

| 选择器 | 说明 |
|------|------|
| `.copy-explain` | 文案解释触发词 |
| `data-tip` | 浮层正文（纯 CSS `::after` 渲染） |
| `tabindex="0"` | 建议加上，支持键盘聚焦显示 |

```html
<span class="copy-explain" tabindex="0" data-tip="Retrieval-Augmented Generation (检索增强生成)：…">RAG</span>
```

### 标签（两套样式）

| 类型 | 类名 | 用途 | 视觉 |
|------|------|------|------|
| **状态标签** | `badge badge-status badge-bad` 等 | 页头 H1 后、小节标题旁入库状态、表格评级 | 12px、左右 padding 10px、**描边** |
| **优先级标签** | `badge badge-priority badge-must` 等 | `list-badge-led` 内「必要 / 可选」 | 11px、**固定宽 40px** 居中、无描边 |

`list-badge-led > li` 用 **左缩进 + badge 绝对定位**（`padding-left: 48px`），正文与行内 `code` 保持**同一文本流**自然换行；勿用 flex 横排（会把文字与 `code` 拆成多个 flex 项，窄屏下出现「拼接式」断行）。

色阶 modifier 共用：`badge-bad` / `badge-should` / `badge-ok`（状态）；`badge-must` / `badge-should`（优先级）。背景与描边分别使用 `--color-danger-bg` / `--color-danger-border` 等语义透明度令牌。未写 `badge-status` 时，`.section h3 > .badge` 与 `.list-badge-led .badge` 仍按上下文自动套用对应样式。

```html
<h3>1. 图片语义 <span class="badge badge-status badge-bad">语义完全丢失</span></h3>
<ul class="list-badge-led">
  <li><span class="badge badge-priority badge-must">必要</span><code>alt</code>：…</li>
</ul>
```

### 原则来源标签（`.principle-tag`）

研究概览推导链 / 行业标准 / 理论映射表中的原则名称用彩色标签展示；可加 `href` 链到全量原则页锚点。

| 属性 | 值 |
|------|-----|
| 高度 | **24px**（`inline-flex` + `padding: 0 8px`） |
| 字号 / 字重 | 12px / **400**（不加粗） |
| 圆角 | 4px |
| 描边悬停 | `border-style: dashed`（链接触发） |

| Modifier | 用途 | 色（令牌） |
|----------|------|------------|
| `principle-tag--empirical` | 实测锚点原则 | `--color-principle-empirical*` |
| `principle-tag--generalize` | 根因泛化原则 | `--color-principle-generalize*` |
| `principle-tag--standard` | 行业标准原则 | `--color-principle-standard*` |
| `principle-tag--pending` | 待定 / 未归类 | 中性虚线描边 |

```html
<a class="principle-tag principle-tag--generalize" href="principles-affinity-full.html#principle-full-29">#3 多语言锚点</a>
```

---

## 4. 段落与区块间距

| 区块 | 间距 |
|------|------|
| `body.inner-page .main-content` 上内边距 | `clamp(32px, 2.5vw, 48px)`（1920 下 **48px**，H1 距 `main` 顶缘） |
| `.page-header` 下边距 | 36px |
| `.page-header` 底内边距 | 24px |
| `.section` 下边距 | 48px |
| `.section p` 段间距 | 12px |
| `.section ul/ol` 下边距 | 16px；左缩进 20px |
| `.section li` 项间距 | 6px |
| `.summary-card` | margin **24px 0**；padding **16px 0 24px**（左右 0） |
| `.component-problem` | margin 12px 0；padding **20px 0**（左右 0） |
| `.info-box` / `.data-table` | margin 16px 0 |
| `.page-nav` | margin-top 60px；padding-top 24px |

---

## 5. 页面结构模板

### 5.1 标准内页

`page-header` **仅含 H1**（或 `page-header-top` + 预览按钮）；`.page-desc`、`.component-problem` 放在 header **底部分割线下方**，再接 `.section` 正文（与 `AGENTS.md`、各 `problems-*.html` 一致）。

各页「解决方案」章节 H2 统一 `id="solution"`，供跨页链接 `#solution` 跳转。

```html
<body class="inner-page" data-module="problems" data-page="example">
  <header class="site-header">…</header>
  <div class="page-wrapper">
    <aside id="module-sidebar"></aside>
    <main class="main-content">
      <!-- #page-toc 由 module-sidebar.js 注入 -->
      <div class="page-header">
        <div class="page-header-top">
          <h1>页面标题 <span class="badge badge-status badge-should">入库状态</span></h1>
          <button type="button" class="preview-drawer-trigger">查看测试页面</button>
        </div>
      </div>
      <p class="page-desc">一句话说明本页测什么。</p>
      <div class="component-problem">
        <div class="cp-label">核心问题</div>
        <ul><li>…</li></ul>
      </div>
      <section class="section" id="example-problem">…</section>
      <section class="section" id="example-solution">
        <h2 id="solution">解决方案</h2>
        …
      </section>
    </main>
  </div>
</body>
```

### 5.1.1 卡片容器（`.surface-card`）

浅灰底 + `#F0F0F0`（`--color-card-border`）描边的内容块；用于论证单元、对比区等。样式见 `assets/css/components/surface-card.css`。

### 5.2 语义组件页（含预览抽屉）

在 `page-header` 内使用 `page-header-top` 包裹 H1 与预览按钮；`component-problem` 的 `cp-label` 为 **核心问题**。

### 5.3 页头描述两行

```html
<p class="page-desc page-desc--split">
  <span class="page-desc-line">第一行：定义或背景。</span>
  <span class="page-desc-line">第二行：本页聚焦点。</span>
</p>
```

### 5.4 无侧栏宽版页（首页、研究概览）

```html
<body>
  <header class="site-header">…</header>
  <div class="page-wrapper">
    <main class="main-content content-wide">
      <!-- 首页：hero、module-grid；研究概览：page-header、section -->
    </main>
  </div>
</body>
```

示例：`index.html`、`background-motivation.html` 使用 `content-wide`（`padding-left: var(--content-offset-left)`，正文与有侧栏内页左缘对齐）。有侧栏模块内页勿加 `content-wide`（见 §1.4）。

### 5.5 顶栏

- 全站「问题论证」入口：`problems-answer-search.html`

---

## 6. 禁止项

- 不在 `.page-header` 上使用 inline `style`
- 不在正文中用 `<br>` 代替段落间距（`page-desc--split` 除外）
- 不嵌套重复 `<section class="section">`
- 不用 H1 在 `.section` 内重复页面标题

---

## 7. 文件索引

| 文件 | 职责 |
|------|------|
| `assets/css/style.css` | CSS 入口（`@import` 子模块，见 `AGENTS.md`） |
| `ui-system.html` | 规范可视化示例 |
| `assets/js/module-sidebar.js` | 模块侧栏 + 右侧本篇目录 |
