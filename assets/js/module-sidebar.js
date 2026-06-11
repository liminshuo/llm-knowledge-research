/** 全站模块侧栏：一项一页，无锚点导航 */
(function () {
  var NAV = {
  "background": [],
  "problems": [
    {
      "group": "信源时效",
      "id": "timeliness",
      "href": "problems-timeliness.html",
      "label": "版本滞后"
    },
    {
      "group": "内容语义",
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
      "id": "content-link",
      "href": "problems-content-link.html",
      "label": "链接语义"
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
      "group": null,
      "id": "content-code",
      "href": "problems-content-code.html",
      "label": "代码语义"
    },
    {
      "group": null,
      "id": "content-table",
      "href": "problems-content-table.html",
      "label": "表格的结构语义"
    },
    {
      "group": null,
      "id": "content-note",
      "href": "problems-content-note.html",
      "label": "注意提示（Note）语义"
    },
    {
      "group": "信息架构与跨页语义",
      "id": "structure-metadata",
      "href": "problems-structure-metadata.html",
      "label": "页级元数据未结构化"
    },
    {
      "group": null,
      "id": "structure-cross",
      "href": "problems-structure-cross.html",
      "label": "跨页关系未结构化"
    },
    {
      "group": null,
      "id": "structure-single",
      "href": "problems-structure-single.html",
      "label": "单文档结构边界"
    },
    {
      "group": "格式交付与抓取入口",
      "id": "format",
      "href": "problems-format.html",
      "label": "双轨交付与载体"
    },
    {
      "group": null,
      "id": "structure-llms",
      "href": "problems-structure-llms.html",
      "label": "机器发现层缺失"
    }
  ],
  "principles": [
    {
      "group": null,
      "id": "general",
      "href": "principles-general.html",
      "label": "UI 亲和原则列表"
    },
    {
      "group": "信源时效",
      "id": "timeliness",
      "href": "principles-timeliness.html",
      "label": "版本外显"
    },
    {
      "group": "内容语义",
      "id": "image",
      "href": "principles-image.html",
      "label": "图片图意"
    },
    {
      "group": null,
      "id": "hotzone",
      "href": "principles-hotzone.html",
      "label": "图片热区"
    },
    {
      "group": null,
      "id": "link",
      "href": "principles-link.html",
      "label": "链接语义"
    },
    {
      "group": null,
      "id": "tab",
      "href": "principles-tab.html",
      "label": "隐藏语义 · Tab"
    },
    {
      "group": null,
      "id": "collapse",
      "href": "principles-collapse.html",
      "label": "隐藏语义 · 折叠"
    },
    {
      "group": null,
      "id": "code",
      "href": "principles-code.html",
      "label": "代码语义"
    },
    {
      "group": null,
      "id": "table",
      "href": "principles-table.html",
      "label": "表格的结构语义"
    },
    {
      "group": null,
      "id": "note",
      "href": "principles-note.html",
      "label": "注意提示（Note）语义"
    },
    {
      "group": "信息架构与跨页语义",
      "id": "structure-metadata",
      "href": "principles-structure-metadata.html",
      "label": "元数据字段规范"
    },
    {
      "group": null,
      "id": "structure-cross",
      "href": "principles-structure-cross.html",
      "label": "跨文档结构感知"
    },
    {
      "group": null,
      "id": "structure-single",
      "href": "principles-structure-single.html",
      "label": "单文档结构感知"
    },
    {
      "group": "格式交付与抓取入口",
      "id": "format",
      "href": "principles-format.html",
      "label": "双轨交付与载体"
    },
    {
      "group": null,
      "id": "structure-llms",
      "href": "principles-structure-llms.html",
      "label": "机器发现层"
    },
    {
      "group": "附录",
      "id": "cheatsheet",
      "href": "principles-cheatsheet.html",
      "label": "速查表"
    }
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
  html += "<ul class=\"sidebar-nav\">";
  var lastGroup = null;
  items.forEach(function (item) {
    if (item.group && item.group !== lastGroup) {
      html += "<li class=\"nav-group-label\">" + item.group + "</li>";
      lastGroup = item.group;
    }
    var active = item.id === page ? " class=\"active\"" : "";
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
  if (module !== "problems" && module !== "principles") return;
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
