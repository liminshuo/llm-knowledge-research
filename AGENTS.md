# Agent 指南 · 大模型知识获取研究站

静态站点（HTML + CSS + 少量 JS）。**改样式优先读小文件，不要通读整站 CSS。**

## CSS 结构

入口仍为各页 `<link href="assets/css/style.css">`；`style.css` 仅 `@import` 子模块。

| 文件 | 内容 |
|------|------|
| `assets/css/tokens.css` | `:root` 设计令牌（色、字级、间距、布局宽度） |
| `assets/css/base.css` | Reset、`body`、链接、行内 `code` / `pre` |
| `assets/css/layout.css` | 顶栏、侧栏、TOC、`main` 栅格、首页 Hero/模块卡、Footer、响应式 |
| `assets/css/page.css` | `.page-header`、`.section` / H2–H4、`.test-prompt-card`、Tab、`.page-nav` |
| `assets/css/components/summary-card.css` | `.summary-card` |
| `assets/css/components/surface-card.css` | `.surface-card`、`.component-problem`、`.list-badge-led`、章节列表间距 |
| `assets/css/components/content-widgets.css` | `.info-box`、`.data-table`、`.arch-diagram`、占位块等 |
| `assets/css/components/badges.css` | 状态 / 优先级 / scope 标签 |
| `assets/css/components/misc.css` | 参考卡、要点列表、对比块等 |
| `assets/css/components/ui-demo.css` | 亲和原则页 UI 渲染示例 |
| `assets/css/components/answer-card.css` | `.answer-card-*`、`.source-breakdown`、来源图例条 |
| `assets/css/components/drawers.css` | 预览抽屉、回答抽屉、`.source-type-defs`、检索 URL 列表 |
| `assets/css/components/ui-system-page.css` | `ui-system.html` 专用 |

完整单文件备份：`assets/css/style.monolith.css`。若需重新拆分：`python3 scripts/split-css.py`。

**视觉规范文档**：`docs/ui-system.md`（与 `ui-system.html` 对照）。

## 按任务读哪些文件

### 检索阶段（问题实测 + 解决方案）

- 页面：`problems-answer-search.html`
- 样式：`assets/css/components/answer-card.css`、`assets/css/components/surface-card.css`、`assets/css/page.css`（`.test-prompt-card`）
- 抽屉模板：同页底部 `<template data-drawer-template="…">`
- 脚本：`assets/js/answer-drawer.js`

### 生成阶段

- 页面：`problems-answer-generate.html`
- 样式：同上 + `components/drawers.css`

### 侧栏 / 导航

- `assets/js/module-sidebar.js`（`NAV.problems` / `NAV.principles` 数据 + 渲染）

### 亲和原则某一维度

- 页面：`principles-*.html`（机器发现层：`principles-structure-llms.html`，已入侧栏）
- 样式：`components/ui-demo.css`、`components/badges.css`、`components/content-widgets.css`

### 改颜色 / 间距 / 新组件

1. 先查 `docs/ui-system.md` 是否已有约定  
2. 改 `tokens.css` 或对应 `components/*.css`  
3. 更新 `docs/ui-system.md` 与（若需要）`ui-system.html` 示例  

## 提问建议（省 token）

在 Cursor 里 `@` 具体文件，例如：

```
@problems-answer-search.html @assets/css/components/answer-card.css
```

避免只写「改卡片样式」而不带文件——Agent 容易扫 `style.monolith.css` 或全站 HTML。

## 模块与页面对照

| 顶栏模块 | 典型页面 | `data-module` |
|----------|----------|---------------|
| 研究概览 | `background-motivation.html` | —（无侧栏或 `content-wide`） |
| 问题论证 | `problems-*.html` | `problems` |
| 亲和原则 | `principles-*.html` | `principles` |

## 约定

- 内页结构（**问题论证**与**亲和原则**共用）：`page-header` 仅含 H1（或 `page-header-top`）；`.page-desc`、`.component-problem` 放在 header **底部分割线下方**，再接 `.section` 正文  
- 各页「解决方案」H2 统一 `id="solution"`，跨页链接用 `#solution`（如 `problems-format.html#solution`）  
- 批量规范化：`python3 scripts/normalize-page-header.py`（默认 `problems-*.html` + `principles-*.html`）  
- 卡片容器：浅灰底 + `#F0F0F0` 描边用 `.surface-card`（见 `docs/ui-system.md` §5.1.1）  
- 已合并页用根目录 **redirect stub**（`<meta refresh>` + canonical），勿在侧栏保留入口；旧 `problems-detail-*`、`problems-format-md-*` 等已重定向  
- **勿批量运行** `scripts/split-all-pages.py`、`enrich-principles-pages.py`、`add-ui-render-demos.py`（NAV / 示例落后于 `module-sidebar.js`）  
- 仅当用户明确要求时再 `git commit` / 部署  

## 发布（GitHub Pages）

线上：<https://liminshuo.github.io/llm-knowledge-research/>

**推荐：从 `main` 分支根目录发布**（仓库 Settings → Pages → Build and deployment → Branch 选 `main` / `/ (root)` → Save）。改完后：

```bash
git push origin main
```

无需再 `git push origin main:gh-pages`。确认站点正常后，可删除远程 `gh-pages` 分支（可选）。

本地预览：`python3 -m http.server 8080`，打开 `http://localhost:8080/`。
