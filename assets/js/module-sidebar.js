/** 全站模块侧栏：一项一页，无锚点导航 */
(function () {
  var NAV = {
  "background": [],
  "problems": [
    {
      "group": "A. 可发现性",
      "id": "timeliness",
      "href": "problems-timeliness.html",
      "label": "版本滞后"
    },
    {
      "group": null,
      "id": "structure-metadata",
      "href": "problems-structure-metadata.html",
      "label": "页级元数据未结构化"
    },
    {
      "group": null,
      "id": "structure-llms",
      "href": "problems-structure-llms.html",
      "label": "机器发现层缺失"
    },
    {
      "group": "B. 可解析性",
      "id": "format",
      "href": "problems-format.html",
      "label": "双轨交付与载体"
    },
    {
      "group": null,
      "id": "content-tab",
      "href": "problems-content-tab.html",
      "label": "隐藏语义 · Tab"
    },
    {
      "group": null,
      "id": "content-collapse",
      "href": "problems-content-collapse.html",
      "label": "隐藏语义 · 折叠"
    },
    {
      "group": "C. 可切分性",
      "id": "structure-single",
      "href": "problems-structure-single.html",
      "label": "单文档结构边界"
    },
    {
      "group": "E. 非文本元素语义转译",
      "id": "content-image",
      "href": "problems-content-image.html",
      "label": "图片图意"
    },
    {
      "group": null,
      "id": "content-hotzone",
      "href": "problems-content-hotzone.html",
      "label": "图片热区"
    },
    {
      "group": null,
      "id": "content-table",
      "href": "problems-content-table.html",
      "label": "表格的结构语义"
    },
    {
      "group": null,
      "id": "content-code",
      "href": "problems-content-code.html",
      "label": "代码语义"
    },
    {
      "group": null,
      "id": "content-link",
      "href": "problems-content-link.html",
      "label": "链接语义"
    },
    {
      "group": null,
      "id": "content-note",
      "href": "problems-content-note.html",
      "label": "注意提示（Note）语义"
    },
    {
      "group": "F. 可溯源性与可信度",
      "id": "structure-cross",
      "href": "problems-structure-cross.html",
      "label": "跨页关系未结构化"
    }
  ],
  "principles": [
    { "group": "A. 可发现性", "id": "a1", "href": "principles-timeliness.html", "label": "版本号外显", "pageIds": ["timeliness"] },
    { "group": null, "id": "a2", "href": "principles-a2.html", "label": "失效/弃用状态显化" },
    { "group": null, "id": "a3", "href": "principles-a3.html", "label": "更新日期标准化" },
    { "group": null, "id": "a4", "href": "principles-structure-metadata.html", "label": "元数据丰富化", "pageIds": ["structure-metadata"] },
    { "group": null, "id": "a5", "href": "principles-structure-llms.html", "label": "llms.txt / sitemap 部署", "pageIds": ["structure-llms"] },
    { "group": "B. 可解析性", "id": "b1", "href": "principles-b1.html", "label": "降噪纯净" },
    { "group": null, "id": "b2", "href": "principles-b2.html", "label": "SSR直出（服务端渲染）" },
    { "group": null, "id": "b3", "href": "principles-tab.html", "label": "Tab/折叠/手风琴全量展开", "pageIds": ["tab", "collapse"] },
    { "group": null, "id": "b4", "href": "principles-b4.html", "label": "Tooltip/悬浮卡片文字前置" },
    { "group": null, "id": "b5", "href": "principles-format.html", "label": "Markdown双轨交付", "pageIds": ["format"] },
    { "group": "C. 可切分性", "id": "c1", "href": "principles-c1.html", "label": "标题层级固定" },
    { "group": null, "id": "c2", "href": "principles-structure-cross.html", "label": "段落锚点稳定可引用", "pageIds": ["structure-cross"] },
    { "group": null, "id": "c3", "href": "principles-structure-single.html", "label": "单文档结构感知", "pageIds": ["structure-single"] },
    { "group": "D. 可理解性", "id": "d1", "href": "principles-d1.html", "label": "结论前置" },
    { "group": null, "id": "d2", "href": "principles-d2.html", "label": "内容自包含" },
    { "group": null, "id": "d3", "href": "principles-d3.html", "label": "术语一致性" },
    { "group": null, "id": "d4", "href": "principles-d4.html", "label": "消除模糊指代" },
    { "group": null, "id": "d5", "href": "principles-d5.html", "label": "明确边界" },
    { "group": null, "id": "d6", "href": "principles-d6.html", "label": "短句优先" },
    { "group": "E. 非文本元素语义转译", "id": "e1", "href": "principles-image.html", "label": "图片内容转译", "pageIds": ["image"] },
    { "group": null, "id": "e2", "href": "principles-hotzone.html", "label": "图片热区转译", "pageIds": ["hotzone"] },
    { "group": null, "id": "e3", "href": "principles-table.html", "label": "表格语义化", "pageIds": ["table"] },
    { "group": null, "id": "e4", "href": "principles-code.html", "label": "代码块语义化", "pageIds": ["code"] },
    { "group": null, "id": "e5", "href": "principles-link.html", "label": "链接语义化", "pageIds": ["link"] },
    { "group": null, "id": "e6", "href": "principles-e6.html", "label": "步骤列表化" },
    { "group": null, "id": "e7", "href": "principles-e7.html", "label": "验证区块" },
    { "group": null, "id": "e8", "href": "principles-note.html", "label": "安全警示语义化", "pageIds": ["note"] },
    { "group": null, "id": "e9", "href": "principles-e9.html", "label": "FAQ结构化" },
    { "group": "F. 可溯源性与可信度", "id": "f1", "href": "principles-f1.html", "label": "chunk级来源携带" },
    { "group": null, "id": "f2", "href": "principles-f2.html", "label": "来源类型标注" },
    { "group": null, "id": "f3", "href": "principles-f3.html", "label": "重大变更记录" },
    { "group": null, "id": "f4", "href": "principles-f4.html", "label": "跨文档命名统一" },
    { "group": "附录", "id": "cheatsheet", "href": "principles-cheatsheet.html", "label": "速查表", "pageIds": ["cheatsheet"] }
  ]
};

  var module = document.body.getAttribute("data-module");
  var page = document.body.getAttribute("data-page");
  var items = NAV[module];
  var aside = document.getElementById("module-sidebar");
  if (!aside) return;
  if (!items || items.length <= 1) {
    aside.remove();
    return;
  }

  var html = "";
  if (module === "problems") {
    html += "<ul class=\"sidebar-nav sidebar-phase-nav\">";
    html += "<li class=\"nav-group-label\">链路观测</li>";
    html += "<li><a href=\"problems-answer-search.html\"" + (page === "answer-search" ? " class=\"active\"" : "") + ">检索阶段</a></li>";
    html += "<li><a href=\"problems-answer-generate.html\"" + (page === "answer-generate" ? " class=\"active\"" : "") + ">生成阶段</a></li>";
    html += "</ul>";
  }
  if (module === "principles") {
    html += "<ul class=\"sidebar-nav sidebar-phase-nav sidebar-module-title\">";
    html += "<li class=\"nav-group-label\">亲和原则</li>";
    html += "<li><a href=\"principles-affinity.html\"" + (page === "affinity" ? " class=\"active\"" : "") + ">亲和性原则</a></li>";
    html += "</ul>";
  }
  function navItemActive(item) {
    if (item.pageIds && item.pageIds.indexOf(page) !== -1) return true;
    return item.id === page;
  }

  html += "<ul class=\"sidebar-nav\">";
  var lastGroup = null;
  items.forEach(function (item) {
    if (item.group && item.group !== lastGroup) {
      html += "<li class=\"nav-group-label\">" + item.group + "</li>";
      lastGroup = item.group;
    }
    var active = navItemActive(item) ? " class=\"active\"" : "";
    html += "<li><a href=\"" + item.href + "\"" + active + ">" + item.label + "</a></li>";
  });
  html += "</ul>";

  aside.className = "sidebar";
  aside.innerHTML = html;
  initPageToc();
})();

/** 文档页右侧锚点目录（h2 / h3） */
function initPageToc() {
  var module = document.body.getAttribute("data-module");
  var page = document.body.getAttribute("data-page");
  if (module !== "problems" && module !== "principles") return;
  if (page === "affinity") return;
  if (!document.getElementById("module-sidebar")) return;

  var main = document.querySelector(".main-content");
  if (!main) return;

  var headings = main.querySelectorAll("h2, h3");
  if (!headings.length) return;

  var used = {};
  function slugify(text) {
    var base = (text || "")
      .trim()
      .toLowerCase()
      .replace(/[^\w\u4e00-\u9fff]+/g, "-")
      .replace(/^-+|-+$/g, "");
    if (!base) base = "section";
    var slug = base;
    var n = 2;
    while (used[slug]) {
      slug = base + "-" + n++;
    }
    used[slug] = true;
    return slug;
  }

  var items = [];
  headings.forEach(function (el) {
    if (el.closest(".preview-drawer")) return;
    var text = el.textContent.replace(/\s+/g, " ").trim();
    if (!text) return;
    if (!el.id) el.id = slugify(text);
    items.push({ el: el, id: el.id, text: text, level: el.tagName === "H3" ? 3 : 2 });
  });
  if (!items.length) return;

  var aside = document.createElement("aside");
  aside.id = "page-toc";
  aside.className = "page-toc";
  aside.setAttribute("aria-label", "本篇目录");

  var html = "<div class=\"page-toc-title\">本篇目录</div><nav class=\"page-toc-nav\"><ul>";
  items.forEach(function (item) {
    var cls = item.level === 3 ? " class=\"toc-h3\"" : "";
    html += "<li><a href=\"#" + item.id + "\"" + cls + " data-toc-link>" + item.text + "</a></li>";
  });
  html += "</ul></nav>";
  aside.innerHTML = html;

  var wrapper = document.querySelector(".page-wrapper");
  var drawer = wrapper && wrapper.querySelector(".preview-drawer");
  if (drawer) wrapper.insertBefore(aside, drawer);
  else if (wrapper) wrapper.appendChild(aside);

  var links = aside.querySelectorAll("[data-toc-link]");
  function setActive(id) {
    links.forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("href") === "#" + id);
    });
  }

  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        var visible = entries
          .filter(function (e) { return e.isIntersecting; })
          .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
        if (visible.length) setActive(visible[0].target.id);
      },
      { rootMargin: "-80px 0px -60% 0px", threshold: 0 }
    );
    items.forEach(function (item) { observer.observe(item.el); });
  } else if (items[0]) {
    setActive(items[0].id);
  }
}
