# UI 系统规范

> 本研究站静态页的统一文字、间距与结构约定。实现文件：`assets/css/style.css`；示例页：`ui-system.html`。

---

## 1. 设计令牌

### 1.1 字体

| 用途 | 字体栈 |
|------|--------|
| 全局正文 | `-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif` |
| 等宽 / 代码 | `"SF Mono", "Fira Code", "Cascadia Code", monospace` |
| 页头描述 | `"PingFang SC"`（`.page-header .page-desc` 单独指定） |

### 1.2 颜色

| 令牌 | 色值 | 用途 |
|------|------|------|
| `--color-text` | `#1e293b` | 主标题、正文 |
| `--color-text-secondary` | `#64748b` | 辅助说明、导航未选中 |
| `--color-primary` | `#2563eb` | 链接、标签、激活态 |
| `--color-primary-dark` | `#1d4ed8` | 链接 hover |
| `--color-primary-light` | `#eff6ff` | h2 下划线、h3 左边线、信息框背景 |
| `--color-bg` | `#f8fafc` | 页面背景 |
| `--color-surface` | `#ffffff` | 卡片、侧栏、表格面 |
| `--color-border` | `#e2e8f0` | 分割线、边框 |
| 页头描述 | `rgba(0, 0, 0, 0.6)` | `.page-desc` |
| 区块小字说明 | `rgba(0, 0, 0, 0.6)` | `.section-heading-desc` |

### 1.3 圆角与阴影

| 令牌 | 值 |
|------|-----|
| `--radius` | `8px` |
| `--shadow` | `0 1px 3px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.04)` |

### 1.4 布局 · 正文最大宽度

| 令牌 | 值 | 说明 |
|------|-----|------|
| `--content-max-width` | `1280px` | 正文内容区最大宽度（不含左右 padding） |
| `--content-wide-pad-x` | `clamp(24px, 4vw, 48px)` | 水平内边距，随视口缩放 |

全站正文遵循同一原则：1920 视口下内容区宽 **1280px**；视口变窄时 `width: 100%` + `clamp` 边距自适应。

| 页面类型 | 实现 |
|----------|------|
| 无侧栏（首页、研究概览） | `<main class="main-content content-wide">`，整体居中；无 `#module-sidebar`、无 `body.inner-page` |
| 有侧栏（当前问题、亲和原则等） | `<main class="main-content">` 占满侧栏以外区域；其直接子块（`.page-header`、`.section`、`.content-tabs` 等）`max-width: calc(1280px + 2 × pad)`，左对齐 |

| 视口 | 行为 |
|------|------|
| 宽屏（如 1920） | 正文内容区最大 **1280px** |
| 中间分辨率 | 随可用宽度缩小，保留 `clamp` 水平边距 |
| ≤ 900px | 水平 padding **24px**；侧栏隐藏；首页模块卡片单列 |

---

## 2. 标题层级（H1–H4）

### H1 · 页面主标题

| 属性 | 值 |
|------|-----|
| 选择器 | `.page-header h1` |
| 字号 | **28px** |
| 字重 | **800** |
| 行高 | **1.3** |
| 颜色 | `#1e293b` |
| 下边距 | **10px** |

> 首页 Hero 例外：`32px / 700 / line-height 1.25`，仅用于 `index.html`。

### H2 · 章节标题

| 属性 | 值 |
|------|-----|
| 选择器 | `.section h2` |
| 字号 | **20px** |
| 字重 | **700** |
| 颜色 | `#1e293b` |
| 下边距 | **16px** |
| 内边距（底） | **10px** |
| 装饰 | 底边 `2px solid #eff6ff` |

### H3 · 小节标题

| 属性 | 值 |
|------|-----|
| 选择器 | `.section h3` |
| 字号 | **16px** |
| 字重 | **600** |
| 颜色 | `#1e293b` |
| 上边距 | **28px**（首个 **16px**） |
| 下边距 | **12px** |
| 装饰 | 左侧 `3px solid #eff6ff` |

用于「结论」「论证」「说明」等小节，不重复 H1 文案。

### H4 · 四级标题

| 属性 | 值 |
|------|-----|
| 选择器 | `.section h4` |
| 字号 | **15px** |
| 字重 | **600** |
| 颜色 | `#1e293b` |
| 上边距 | **20px** |
| 下边距 | **10px** |

**卡片内 H4**（`.answer-card-header h4`）：`14px / 700`。

---

## 3. 正文与说明

### 全局正文（`body`）

| 属性 | 值 |
|------|-----|
| 字号 | **15px** |
| 行高 | **1.7** |
| 颜色 | `#1e293b` |

### 页头描述（`.page-desc`）

| 属性 | 值 |
|------|-----|
| 字号 | **14px** |
| 行高 | **22px** |
| 颜色 | `rgba(0, 0, 0, 0.6)` |

**分行版**（`.page-desc--split` + `.page-desc-line`）：

| 属性 | 值 |
|------|-----|
| 单行高 | **20px** |
| 行间距 | **4px** |

### 章节正文（`.section p`）

| 属性 | 值 |
|------|-----|
| 字号 | **15px**（继承） |
| 行高 | **1.7** |
| 段落下边距 | **12px** |

### 模块标签（`.module-label`）

| 属性 | 值 |
|------|-----|
| 字号 | **12px** |
| 字重 | **600** |
| 字间距 | `0.06em` |
| 大小写 | uppercase |
| 颜色 | `#2563eb` |
| 下边距 | **8px** |

格式：`模块 NN · {模块名} · {可选子主题}`

### 组件内文字

| 组件 | 字号 | 行高 |
|------|------|------|
| `.component-problem` | 14px | 1.65 |
| `.info-box` | 14px | 继承 |
| `.data-table` | 13.5px | 继承 |
| `.key-points li` | 14px | 继承 |
| `.cp-label` | 11px / 700 / 主色 | — |

### 行内代码（`code`）

| 属性 | 值 |
|------|-----|
| 字号 | `0.9em` |
| 字体 | 等宽栈 |
| 背景 | `#f1f5f9` |
| 内边距 | `2px 6px` |
| 圆角 | `4px` |
| 颜色 | `#1e293b` |

---

## 4. 段落与区块间距

| 区块 | 间距 |
|------|------|
| `.page-header` 下边距 | 36px |
| `.page-header` 底内边距 | 24px |
| `.section` 下边距 | 48px |
| `.section p` 段间距 | 12px |
| `.section ul/ol` 下边距 | 16px；左缩进 20px |
| `.section li` 项间距 | 6px |
| `.component-problem` | margin 12px 0；padding 20px |
| `.info-box` / `.data-table` | margin 16px 0 |
| `.page-nav` | margin-top 60px；padding-top 24px |

---

## 5. 页面结构模板

### 5.1 标准内页

```html
<body class="inner-page" data-module="problems" data-page="example">
  <header class="site-header">…</header>
  <div class="page-wrapper">
    <aside id="module-sidebar"></aside>
    <main class="main-content">
      <div class="page-header">
        <div class="module-label">模块 02 · 当前问题 · 子主题</div>
        <h1>页面标题</h1>
        <p class="page-desc">一句话说明本页测什么。</p>
        <!-- 可选 -->
        <div class="component-problem">
          <div class="cp-label">核心结论</div>
          <ul>
            <li><strong>概括主题</strong>：现象与数据描述；对检索 / 生成 / 开发者的影响。</li>
          </ul>
        </div>
      </div>
      <section class="section" id="example">
        <h3>论证</h3>
        <p>…</p>
      </section>
      <nav class="page-nav">…</nav>
    </main>
  </div>
</body>
```

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

示例：`index.html`、`background-motivation.html`。有侧栏时勿加 `content-wide`；正文宽度由 `main` 内直接子块的选择器约束（见 §1.4）。

### 5.5 顶栏

- 全站「当前问题」入口：`problems-answer-search.html`

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
| `assets/css/style.css` | 全部样式实现 |
| `ui-system.html` | 规范可视化示例 |
| `assets/js/module-sidebar.js` | 侧栏导航 |
