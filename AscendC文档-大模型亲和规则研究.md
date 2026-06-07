# Ascend C 文档大模型亲和规则研究

> **研究角色**：UI 设计师  
> **研究背景**：以鲲鹏社区 Ascend C 算子开发文档为切入点，审视「给人看的文档」如何改造为「给大模型看、能准确抓取并调用」的文档体系。  
> **文档版本**：CANN 社区版 9.0.0  
> **研究日期**：2026-06-05

---

## 参考对话与延伸阅读

以下是与 Claude 的研究对话，作为本报告的观点来源与后续探索入口。对话内容需在 Claude 页面中查看；本报告将围绕其中的核心观点展开。

| 主题 | 对话链接 | 关联模块 | 探索方向 |
|------|----------|----------|----------|
| Ascend-C 文档内容对比分析 | [打开对话](https://claude.ai/share/3f2d4c30-6210-4259-9a9b-de7943cf6fff) | 当前问题 | 人类可见内容 vs 模型抓取结果的逐项对比 |
| 读取 Ascend C 文档内容 | [打开对话](https://claude.ai/share/d11287e8-ffd5-41f0-9b1d-b2d76b20a84c) | 研究背景 | 大模型如何读取社区文档、抓取路径与端点选择 |
| 知识库与大模型的集成方案 | [打开对话](https://claude.ai/share/272104cc-2681-453e-9cbd-5ac25f16e999) | 解决方案 | RAG 入库、切片策略、Agent 调用与元数据设计 |
| Ascend C 是什么 | [打开对话](https://claude.ai/share/4091dd7f-2949-4197-ace5-ed546d108fb4) | 研究背景 | Ascend C 定义、API 层级、适用场景与设备 |
| Ascend C 语言学习指南 | [打开对话](https://claude.ai/share/ea0e9a83-f5d6-448a-a53b-59d30392d83f) | 研究背景 / 亲和原则 | 学习路径、成长地图、文档 IA 与阅读顺序 |
| 静态 Tensor 编程内容解读 | [打开对话](https://claude.ai/share/6290a369-81d8-4064-b473-d9151e1ccd89) | 亲和原则 | 复杂技术内容的结构化表达与模型理解 |

### 对话与研究报告的映射关系

```
参考对话                          本报告模块
─────────────────────────────────────────────────
读取 Ascend C 文档内容      →    研究背景 · 研究方法
Ascend C 是什么             →    研究背景 · 概念上下文
Ascend C 语言学习指南       →    研究背景 · 信息架构
Ascend-C 文档内容对比分析   →    当前问题 · 抓取诊断
知识库与大模型集成方案      →    解决方案 · 双轨架构
静态 Tensor 编程内容解读    →    亲和原则 · 复杂内容组件
```

> **说明**：Claude 分享页需登录且在浏览器中打开，无法被自动化工具直接抓取正文。请将导出内容粘贴至 [`references/claude-conversations/`](./references/claude-conversations/) 目录下对应文件，Agent 可自动解析并更新 HTML 站点。详见 [`references/README.md`](./references/README.md)。

---

## 研究范围

| 序号 | 页面 | URL | 备注 |
|------|------|-----|------|
| 1 | 什么是 Ascend C | [atlas_ascendc_map_10_0002.html](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/Ascendcopdevg/atlas_ascendc_map_10_0002.html) | 含图片热区导航图 |
| 2 | 环境准备 | [atlas_ascendc_map_10_0003.html](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/Ascendcopdevg/atlas_ascendc_map_10_0003.html) | 含注意提示、代码块 |
| 3 | HelloWorld | [atlas_ascendc_map_10_0005.html](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/Ascendcopdevg/atlas_ascendc_map_10_0005.html) | 用户提供链接有误（原链接与环境准备重复），正确页面为 `0005` |
| 4 | 编程模型概述 | [atlas_ascendc_10_10062.html](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/Ascendcopdevg/atlas_ascendc_10_10062.html) | 含表格、跨页链接 |

**研究方法**：对页面进行「模拟大模型抓取」——使用 HTTP 静态抓取（等同 RAG 爬虫 / 网页 Reader），对比用户可见内容与抓取结果；同时分析源 HTML（`/doc_center/source/` 端点）与前端渲染页（`/document/detail/` 端点）的差异。

---

## 一、页面呈现的最优形式：MD 还是 HTML？

### 结论：**双轨交付，MD 为主、HTML 为辅**

| 维度 | Markdown (.md) | HTML (.html) | 评判 |
|------|----------------|--------------|------|
| 语义纯度 | 标题层级、列表、代码块、表格均为显式文本标记，噪声低 | 含大量布局 class、Vue 指令、样式、导航壳层，信噪比低 | MD 胜 |
| 大模型训练/推理成本 | Token 效率高，结构可预测 | 同内容 Token 消耗约为 MD 的 2–4 倍 | MD 胜 |
| 人类阅读体验 | 纯文本，缺乏品牌视觉、交互组件 | 支持 Tab、折叠、图片热区、侧边导航 | HTML 胜 |
| 可抓取稳定性 | 静态文件，不依赖 JS 渲染 | 当前站点为 Nuxt SPA，部分内容依赖客户端 hydration | MD 胜 |
| 与现有体系兼容 | 需从现有 HTML 源转换 | 已是内容生产源头（`/doc_center/source/`） | HTML 现势 |

### 推荐架构

```
内容生产（HTML 源）
    │
    ├──► 人类阅读层：品牌化 HTML + 交互 UI（现有 document/detail 站点）
    │
    └──► 模型消费层：MD / 结构化 JSON（llms.txt、sitemap、API）
              │
              └──► RAG 向量库 / Agent Tool Calling
```

### 为什么不是「只保留一种格式」

1. **只给 MD**：开发者失去图片热区导航、Tab 切换等高效浏览体验；UI 设计师的品牌与信息层次难以表达。
2. **只给 HTML**：大模型抓取时混入 22 万字符页面中的导航菜单（282 个 `o-link`）、Cookie 横幅、`display:none` 隐藏层，严重污染上下文。
3. **最优解**：**同源双发（Single Source, Dual Output）**——从 `/doc_center/source/` 的干净 HTML 自动管道转换为 MD，并附带结构化元数据。

### 格式优先级建议

| 场景 | 推荐格式 |
|------|----------|
| RAG 知识库入库 | MD + YAML Front Matter |
| Agent 实时 Tool Calling | JSON API（含 `title`、`breadcrumb`、`content_md`、`links[]`、`code_blocks[]`） |
| 人类在线阅读 | 现有 HTML 站点 |
| 发现与索引 | `llms.txt` + `llms-full.txt`（行业新兴惯例） |

---

## 二、大模型回答侧问题

在实际使用中，开发者通过主流大模型咨询昇腾 / Ascend C 问题时，还面临两类与「回答质量」直接相关的痛点：

| 问题 | 表现 | 可能原因 |
|------|------|----------|
| **官方内容占比少** | 大模型回答中，来自昇腾社区官方的内容少 | 社区文档机器可读性弱；未进入主流 RAG/索引；第三方教程更易被收录 |
| **版本不是最新** | 回答的信息不是最新版本的 | 训练数据截止早；文档缺乏 version 元数据；多版本并存未消歧 |

**与亲和改造的关联**：

1. 提供机器友好源、`llms.txt`、结构化 MD 出口 → 提升官方内容被收录与引用率
2. 每篇文档标注 `version: CANN社区版 9.0.0` → RAG 检索时优先最新版
3. 回答附带 `source_url` / `doc_id` → 用户可溯源至官方正文核验

---

## 三、模型能抓取到什么 / 不能抓取到什么

### 3.1 能较好抓取的内容 ✅

基于四页实测，通过静态 HTTP 抓取（或访问 `/doc_center/source/` 源 HTML），模型**可以较准确获取**：

| 内容类型 | 抓取质量 | 实测示例 |
|----------|----------|----------|
| 页面标题（`<title>` / `<h1>`） | 高 | 「什么是 Ascend C」「环境准备」「HelloWorld」「编程模型概述」 |
| 段落正文 | 高 | Ascend C 定义、AI Core 说明等 |
| 有序/无序列表 | 高 | API 层级列表、环境准备步骤 |
| 加粗/强调语义 | 中高 | `<strong>` 包裹的「驱动固件」「CANN 软件包」 |
| 代码块主体 | 中高 | `hello_world.asc` 完整代码、cmake 安装命令 |
| 数据表格 | 高 | 「表1 编程模型分类」三行四列结构完整 |
| 站内相对链接 | 中高 | `atlas_ascendc_10_10063.html` 等可解析为完整 URL |
| 站外绝对链接 | 高 | Ascend C 主页、PyAsc、CANN 软件安装 |
| 注意提示正文 | 中高 | `<div class="note">` 内 `notebody` 文本（如 set_env.sh 说明） |
| 面包屑/父子主题 | 中 | 「父主题：入门教程」「父主题：编程模型」 |
| 上下篇导航 | 中 | 什么是 Ascend C → 下一篇「环境准备」 |
| Topic 锚点 ID | 高 | `ZH-CN_TOPIC_0000002562272921` 可用于精确定位 |

### 3.2 不能或难以准确抓取的内容 ❌

| 内容类型 | 问题描述 | 实测影响 |
|----------|----------|----------|
| **图片热区（Image Map）** | `<img usemap>` + `<area href>` 链接藏在坐标里，无文字 | 「成长地图」「快速入门」导航图：模型只见 PNG 文件名，**丢失 28 个跳转关系** |
| **无 alt 的示意图** | `<img class="eddx">` 无替代文本 | API 层级架构图、成长路径图：**语义为零** |
| **Tab 切换的隐藏面板** | 前端 `tab-hover .more-tab-item{display:none}`，非激活 Tab 可能不可见 | 若渲染层做 Tab 折叠，模型可能**只抓到第一个 Tab** |
| **JS 动态渲染内容** | Nuxt `v-if` 条件渲染（161 处）、`window.__NUXT__` payload 为空 | 纯静态爬虫可能拿到不完整 SSR 片段 |
| **装饰性图标** | `note_3.0-zh-cn.png` 仅作视觉标识 | 模型抓到无意义图片路径，**不知道这是「注意」类型** |
| **行号列污染代码** | `highlighttable` 将行号与代码混为表格 | 代码块出现 `1 2 3...31` 行号前缀，**干扰代码复用** |
| **站点全局导航** | 每页 282 个 `o-link`、完整社区菜单 JSON | 污染上下文，**稀释正文语义密度** |
| **Cookie / 广告 / 页脚** | 法务声明、营销链接 | 无关 Token 占用 |
| **占位符链接** | 「完整样例请参考 LINK」| 链接文本未解析，**模型无法追溯样例仓库** |
| **折叠面板未展开内容** | 若 UI 默认折叠 | 正文被截断 |
| **表格内嵌代码** | 代码被拆入 `<table>` 单元格 | Markdown 转换后结构破碎 |

### 3.3 抓取质量对比：两个端点

| 端点 | 路径模式 | 页面大小 | 适合模型？ |
|------|----------|----------|------------|
| 渲染页 | `/document/detail/.../*.html` | ~224 KB | ❌ 噪声大 |
| 源 HTML | `/doc_center/source/.../*.html` | 4–11 KB | ✅ 推荐作为抓取入口 |

> **设计建议**：在文档站点增加显式的「模型友好源」入口，或在 `robots.txt` / `llms.txt` 中声明 `/doc_center/source/` 为机器可读canonical 源。

---

## 四、模型是否需要理解整个文档信息架构？

### 结论：**需要「轻量 IA」，不需要「全站 IA」**

### 4.1 需要的架构信息（精准上下文）

模型在回答「如何编译 HelloWorld」「SIMD 和 SIMT 区别」等问题时，需要以下**页面级**元数据：

```yaml
# 每篇文档应提供的 IA 元数据
doc_id: atlas_ascendc_map_10_0005
title: HelloWorld
breadcrumb: [Ascend C算子开发, 入门教程, 基于SIMD编程, 快速入门, HelloWorld]
parent_topic: 快速入门
prev_topic: { title: 环境准备, url: ...0003.html }
next_topic: { title: ..., url: ... }
version: CANN社区版 9.0.0
product: Ascend C算子开发
keywords: [核函数, bisheng, CMake, dav-2201]
applicable_devices: [Atlas A2, Atlas A3, Atlas 350]
```

**作用**：
- 消歧（「环境准备」在入门教程 vs 软件安装文档中均有）
- 支持多跳推理（从 HelloWorld → 环境准备 → CANN 安装）
- 版本锁定（避免 8.5 与 9.0 内容混淆）

### 4.2 不需要的架构信息（噪声）

| 不需要 | 原因 |
|--------|------|
| 全站 282 项导航菜单 | 与当前问题无关，占用上下文窗口 |
| 社区活动、营销链接 | 非技术语义 |
| 所有产品线的文档树 | 模型应按需检索，而非一次性灌入 |
| 页面 CSS/布局结构 | 对理解内容无帮助 |

### 4.3 IA 理解深度分级

```
Level 0 — 单页正文        → 能回答「这段说了什么」
Level 1 — 页面元数据      → 能回答「这篇文档在知识体系中的位置」  ← 推荐最低标准
Level 2 — 章节子树        → 能回答「入门教程完整路径」
Level 3 — 全站文档树      → 仅索引服务需要，不应灌入模型上下文
```

### 4.4 对四页的具体 IA 关系

```
Ascend C算子开发
└── 入门教程
    ├── 什么是 Ascend C        ← 0002（概念 + 导航图）
    ├── 环境准备               ← 0003
    └── 基于SIMD编程
        └── 快速入门
            └── HelloWorld     ← 0005
└── 编程模型
    └── 编程模型概述           ← 10062
```

**设计建议**：在每页顶部输出机器可读的 breadcrumb JSON-LD，而非仅渲染可视面包屑。

---

## 五、各组件的 UI 与代码层调整方案

### 5.1 总原则

| 原则 | 说明 |
|------|------|
| **语义先行** | 所有信息必须有文本表达，不能仅依赖视觉或坐标 |
| **扁平交付** | 隐藏/折叠/Tab 内容在机器可读层全部展开 |
| **双通道一致** | 人类看到的 ≈ 模型读到的（信息不丢失，允许呈现形式不同） |
| **元数据外显** | 类型、级别、适用设备等用结构化字段表达 |
| **源页瘦身** | 机器源剥离导航壳、脚本、样式 |

---

## 六、各组件大模型亲和规则

---

### 组件 1：标题（H1–H6）

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| H-01 | 每页有且仅有一个 H1，与 `<title>` 语义一致 | 必须 |
| H-02 | 标题层级连续，不跳级（H1→H2→H3） | 必须 |
| H-03 | 标题文本应自解释，避免「概述」「说明」等孤立词 | 建议 |
| H-04 | 保留 `id` 锚点，格式稳定：`ZH-CN_TOPIC_{id}` | 必须 |

#### 说明

模型依赖标题建立文档结构和 chunk 边界。当前四页 H1 均清晰（如「编程模型概述」），符合规则。标题跳级会导致 RAG 切片时层级关系错乱。

#### 代码示例

```html
<!-- ✅ 亲和 -->
<h1 class="topictitle1" id="ZH-CN_TOPIC_0000002531522172">编程模型概述</h1>

<!-- ❌ 不亲和 -->
<div class="title-style-level1">编程模型概述</div>
```

#### MD 输出

```markdown
# 编程模型概述
```

---

### 组件 2：段落与列表

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| P-01 | 列表项中嵌套注意提示时，提示正文须在 `<li>` 内完整展开 | 必须 |
| P-02 | 有序列表表达步骤序列，无序列表表达并列项 | 必须 |
| P-03 | 列表项首词加粗时，加粗文本作为该条目的「标签」 | 建议 |
| P-04 | 避免空段落 `<p></p>` 作为间距手段 | 建议 |

#### 说明

环境准备页将「安装 CANN」步骤与注意提示嵌套在 `<ol><li>` 内，源 HTML 结构良好，模型可完整抓取步骤与注意事项的从属关系。

#### 代码示例

```html
<!-- ✅ 亲和：注意提示嵌套在步骤内 -->
<li><strong>安装CANN软件包</strong>
  <div class="note" data-type="note">
    <div class="notebody">...source ${INSTALL_DIR}/set_env.sh...</div>
  </div>
</li>
```

---

### 组件 3：链接

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| L-01 | 链接文本必须是描述性的，禁止「点击这里」「LINK」 | 必须 |
| L-02 | 站外链接保留完整 `href`，标注 `external: true` | 必须 |
| L-03 | 站内链接在机器层转换为绝对 URL | 必须 |
| L-04 | 图片热区 `<area>` 必须冗余为文本链接列表 | 必须 |
| L-05 | 链接附带 `title` 或上下文说明其目标内容 | 建议 |

#### 说明

HelloWorld 页出现「完整样例请参考 LINK」——`LINK` 对模型无意义。成长地图页有 28 个 `<area href>` 热区，模型完全无法感知。

#### 代码示例

```html
<!-- ❌ 当前 -->
<a href="https://gitcode.com/...">LINK</a>

<!-- ✅ 改造 -->
<a href="https://gitcode.com/cann/ascendc-samples/tree/master/hello_world"
   data-link-purpose="完整样例代码仓库">
  hello_world 完整样例（GitCode 仓库）
</a>

<!-- ✅ 图片热区冗余文本化 -->
<nav aria-label="成长地图导航">
  <ul>
    <li><a href="atlas_ascendc_map_10_0003.html">环境准备</a></li>
    <li><a href="atlas_ascendc_10_10063.html">AI Core SIMD编程</a></li>
    <!-- ...其余 26 项 -->
  </ul>
</nav>
```

#### MD 输出

```markdown
- [环境准备](./atlas_ascendc_map_10_0003.html)
- [AI Core SIMD编程](./atlas_ascendc_10_10063.html)
```

---

### 组件 4：图片

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| IMG-01 | 所有信息型图片必须有 `alt` 文本，描述图中传达的知识 | 必须 |
| IMG-02 | 复杂图表须附「图片内容转写」（Image Caption + Text Transcription） | 必须 |
| IMG-03 | 图片热区 `<map>` 须配 `IMG-04` 文本导航冗余 | 必须 |
| IMG-04 | 装饰性图标（如 note 图标）用 `aria-hidden="true"` 标记，信息由文本承载 | 必须 |
| IMG-05 | 图片提供可访问的 SVG 或 Mermaid 替代源 | 建议 |

#### 说明

「什么是 Ascend C」页含 5 张 `usemap` 热区图 + 1 张 API 层级图，是**本次研究最大的抓取盲区**。模型只能看到 `zh-cn_image_0000002531512958.png`，无法理解成长路径。

#### 代码示例

```html
<!-- ❌ 当前 -->
<img class="eddx" src="figure/zh-cn_image_0000002531512958.png">

<!-- ✅ 改造 -->
<figure id="ascend-c-api-layers">
  <img src="figure/zh-cn_image_0000002531512958.png"
       alt="Ascend C API 层级：语言扩展层C API、基础API、高阶API、算子模板库、Python前端">
  <figcaption>图1 Ascend C 多层级 API 体系</figcaption>
</figure>

<!-- 机器阅读专用转写 -->
<div data-llm-transcription="true" hidden>
  Ascend C API 自下而上分为五层：
  1. 语言扩展层 C API — 指针编程，芯片级能力
  2. 基础 API — Tensor 级 C++ 类库
  3. 高阶 API — 卷积、矩阵等公共算法
  4. 算子模板库 — Tiling 模板
  5. Python 前端 — PyAsc
</div>
```

---

### 组件 5：表格

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| TBL-01 | 表格必须有 `<caption>` 或前置标题（如「表1」） | 必须 |
| TBL-02 | 表头 `<th>` 明确，不依赖视觉样式表达表头 | 必须 |
| TBL-03 | 不在表格单元格内嵌套代码块；代码应独立于表外 | 必须 |
| TBL-04 | 机器层额外输出 Markdown 表格或 JSON 数组 | 建议 |
| TBL-05 | 保持列语义简单，避免跨行跨列合并 | 建议 |

#### 说明

「编程模型概述」页的「表1 编程模型分类」结构清晰，是四页中**表格亲和度最高**的示例。HelloWorld 页将代码行号与代码混为 `highlighttable`，属于表格滥用。

#### 代码示例

```html
<!-- ✅ 亲和 -->
<div class="tablenoborder">
  <table>
    <caption><b>表1 </b>编程模型分类</caption>
    <thead>
      <tr><th>编程模型</th><th>计算空间</th><th>特点</th></tr>
    </thead>
    <tbody>...</tbody>
  </table>
</div>
```

#### MD 输出

```markdown
| 编程模型 | 计算空间 | 特点 |
|----------|----------|------|
| SIMD编程 | AI Core | 适合矩阵计算、连续计算的矢量算子及融合算子场景... |
| SIMT编程 | AI Core | 适用于离散访问场景、复杂分支控制场景 |
| AI CPU编程 | AI CPU | 作为AI Core计算的补充 |
```

---

### 组件 6：代码块

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| CODE-01 | 代码须置于 `<pre><code class="language-xxx">` 中，标注语言 | 必须 |
| CODE-02 | 行号与代码分离：行号用 CSS 伪元素或独立列，不写入 `code` 文本 | 必须 |
| CODE-03 | 不使用 `highlighttable` 将代码拆为表格单元格 | 必须 |
| CODE-04 | 每段代码标注：文件名、语言、适用场景（如 bisheng / CMake） | 建议 |
| CODE-05 | 命令行代码与源代码分开标记 `class="language-bash"` / `language-cpp` | 建议 |
| CODE-06 | HTML 实体须解码（`&quot;` → `"`）后再入模型层 | 必须 |

#### 说明

HelloWorld 页代码块内容完整可获取，但行号污染和表格化拆分是主要问题。环境准备页的 cmake 安装命令结构简洁，亲和度较好。

#### 代码示例

```html
<!-- ❌ 当前：行号与代码混在 table 中 -->
<div class="highlight">
  <table class="highlighttable">
    <tr><td class="linenos"><pre>1\n2\n3</pre></td>
        <td class="code"><pre>// code...</pre></td></tr>
  </table>
</div>

<!-- ✅ 改造 -->
<div class="code-block" data-filename="hello_world.asc" data-language="asc">
  <pre><code class="language-cpp">// Host侧应用程序需要包含的头文件
#include "acl/acl.h"
...</code></pre>
</div>
```

#### MD 输出

````markdown
```cpp
// 文件：hello_world.asc
#include "acl/acl.h"
...
```
````

---

### 组件 7：注意 / 警告 / 提示（Note）

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| NOTE-01 | 提示类型用 `data-admonition-type` 标注：`note` / `warning` / `caution` / `tip` | 必须 |
| NOTE-02 | 提示正文在 `notebody` 中完整展开，不依赖图标传达类型 | 必须 |
| NOTE-03 | 图标图片 `aria-hidden="true"`，类型用文本前缀表达 | 必须 |
| NOTE-04 | 机器层转换为 MD 引用块，前缀为类型标签 | 必须 |
| NOTE-05 | 不在注意提示内再嵌套折叠 | 建议 |

#### 说明

当前 `<div class="note">` 结构已有 `notebody`，正文可抓取，但模型不知道这是「注意」还是「警告」（图标路径无文本语义）。

#### 代码示例

```html
<!-- ❌ 当前 -->
<div class="note">
  <img src="public_sys-resources/note_3.0-zh-cn.png">
  <span class="notetitle"> </span>
  <div class="notebody">安装CANN软件后...</div>
</div>

<!-- ✅ 改造 -->
<aside class="admonition note" data-admonition-type="note" role="note">
  <p class="admonition-title">注意</p>
  <p>安装CANN软件后，使用CANN运行用户进行编译、运行时...</p>
</aside>
```

#### MD 输出

```markdown
> **注意**
> 安装CANN软件后，使用CANN运行用户进行编译、运行时，需要以CANN运行用户登录环境，执行 `source ${INSTALL_DIR}/set_env.sh` 命令设置环境变量。
```

---

### 组件 8：Tab 切换

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| TAB-01 | 所有 Tab 面板内容在源 HTML 中完整存在，不依赖 JS 懒加载 | 必须 |
| TAB-02 | 每个 Tab 有明确的文本标签（如「使用 bisheng」「使用 CMake」） | 必须 |
| TAB-03 | 机器层输出时**全部展开**，用 H3 标注各 Tab 标题 | 必须 |
| TAB-04 | 禁止使用 `display:none` 在源 HTML 中隐藏非默认 Tab | 必须 |
| TAB-05 | UI 层可用 Tab 交互，但 `/doc_center/source/` 层必须扁平 | 必须 |

#### 说明

HelloWorld 页「bisheng 编译」与「CMake 编译」在源 HTML 中为同级 `<li>` 顺序排列——**源层已较亲和**。风险在于 `/document/detail/` 渲染层可能将其变为 Tab UI 并隐藏非激活项。

#### 代码示例

```html
<!-- ✅ 源 HTML 层：顺序展开 -->
<h3 id="compile-bisheng">使用 bisheng 命令行进行编译</h3>
<pre class="language-bash">bisheng hello_world.asc --npu-arch=dav-2201 -o demo</pre>

<h3 id="compile-cmake">使用 CMake 进行编译</h3>
<pre class="language-cmake">cmake_minimum_required(VERSION 3.16)...</pre>
```

#### MD 输出

```markdown
### 使用 bisheng 命令行进行编译
\`\`\`bash
bisheng hello_world.asc --npu-arch=dav-2201 -o demo
\`\`\`

### 使用 CMake 进行编译
\`\`\`cmake
cmake_minimum_required(VERSION 3.16)
...
\`\`\`
```

---

### 组件 9：折叠面板

#### 规则

| 编号 | 规则 | 级别 |
|------|------|------|
| COLL-01 | 默认状态在机器层为「展开」 | 必须 |
| COLL-02 | 折叠标题使用 `<h3>` 或 `<summary>`，不用空 `<div>` | 必须 |
| COLL-03 | 不用 `display:none` / `visibility:hidden` 隐藏正文 | 必须 |
| COLL-04 | 若使用 `<details>`，添加 `open` 属性作为源 HTML 默认态 | 建议 |
| COLL-05 | 提供 `data-llm-expanded="true"` 标记供爬虫识别 | 建议 |

#### 说明

当前四页未大量使用折叠面板，但全站存在 `collapse` / `accordion` 模式。折叠是模型抓取的头号敌人——**用户看得到 ≠ 模型读得到**。

#### 代码示例

```html
<!-- ❌ 不亲和 -->
<div class="collapse">
  <div class="collapse-header">高级配置</div>
  <div class="collapse-body" style="display:none">...</div>
</div>

<!-- ✅ 源层展开 -->
<h3>高级配置</h3>
<p>配置内容...</p>

<!-- ✅ 人类 UI 层可用 details，但默认 open -->
<details open>
  <summary>高级配置</summary>
  <p>配置内容...</p>
</details>
```

---

## 七、四页抓取诊断摘要

| 页面 | 抓取完整度 | 主要丢失项 | 优先改造项 |
|------|------------|------------|------------|
| 什么是 Ascend C | ★★☆☆☆ | 成长地图热区、API 层级图 | IMG-02/03/04、L-04 |
| 环境准备 | ★★★★☆ | 注意图标语义 | NOTE-01/03 |
| HelloWorld | ★★★☆☆ | 行号污染、LINK 占位符 | CODE-02/03、L-01 |
| 编程模型概述 | ★★★★★ | 基本完整 | 保持现状，作标杆 |

---

## 八、落地路线图

### Phase 1：快速修复（不改 UI 视觉）

- [ ] 为所有信息型图片补充 `alt` 与 `data-llm-transcription`
- [ ] 图片热区 `<map>` 冗余文本链接列表
- [ ] 修复「LINK」类无意义链接文本
- [ ] 在 `llms.txt` 中声明 `/doc_center/source/` 为机器可读源
- [ ] 代码块行号与代码分离

### Phase 2：管道建设

- [ ] 建立 HTML → MD 自动转换管道（含 Front Matter 元数据）
- [ ] 每页输出 JSON-LD breadcrumb
- [ ] 注意提示统一为 `admonition` 语义标签
- [ ] Tab / 折叠在源层扁平展开

### Phase 3：体验统一

- [ ] 人类 UI 与机器源双轨发布纳入 CI/CD
- [ ] RAG 切片策略按 H2/H3 边界 + 元数据过滤
- [ ] 建立抓取质量回归测试（对比可见内容与 MD 输出）

---

## 九、附录

### A. 机器可读文档头（Front Matter 模板）

```yaml
---
doc_id: atlas_ascendc_map_10_0005
title: HelloWorld
product: Ascend C算子开发
version: CANN社区版 9.0.0
language: zh-CN
breadcrumb:
  - Ascend C算子开发
  - 入门教程
  - 基于SIMD编程
  - 快速入门
  - HelloWorld
parent: 快速入门
prev: { id: atlas_ascendc_map_10_0003, title: 环境准备 }
keywords: [HelloWorld, 核函数, bisheng, CMake, dav-2201]
applicable_devices:
  - Atlas 350 加速卡
  - Atlas A2 训练系列产品
  - Atlas A3 训练系列产品
source_url: https://www.hiascend.com/doc_center/source/zh/.../atlas_ascendc_map_10_0005.html
human_url: https://www.hiascend.com/document/detail/zh/.../atlas_ascendc_map_10_0005.html
last_updated: 2026-06-05
---
```

### B. 组件规则速查表

| 组件 | 核心规则（一句话） |
|------|-------------------|
| 标题 | 一个 H1，层级连续，有锚点 ID |
| 段落/列表 | 列表即结构，不嵌空段落 |
| 链接 | 描述性文本，热区须文本冗余 |
| 图片 | alt + 转写，热区变链接列表 |
| 表格 | 有 caption，不嵌代码 |
| 代码块 | 标注语言，行号与代码分离 |
| 注意提示 | 类型文本化，MD 引用块输出 |
| Tab | 源层全展开，标签作 H3 |
| 折叠面板 | 机器层默认展开 |

### C. 参考端点

| 用途 | URL 模式 |
|------|----------|
| 人类阅读 | `https://www.hiascend.com/document/detail/zh/.../*.html` |
| 机器抓取（推荐） | `https://www.hiascend.com/doc_center/source/zh/.../*.html` |
| 面包屑 API | `/ascendgateway/ascendservice/doc/single/page/breadcrumbs?route=...` |

---

*本报告基于 CANN 社区版 9.0.0 Ascend C 算子开发文档四页的实测抓取分析，供 UI 设计与文档工程团队参考。*
