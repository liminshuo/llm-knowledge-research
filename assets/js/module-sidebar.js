/** 全站模块侧栏：一项一页，无锚点导航 */
(function () {
  var NAV = {
  "background": [],
  "problems": [
    {
      "group": "时效",
      "id": "timeliness",
      "href": "problems-timeliness.html",
      "label": "版本滞后"
    },
    {
      "group": "语义理解",
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
      "label": "隐藏的语义（Tab）"
    },
    {
      "group": null,
      "id": "content-collapse",
      "href": "problems-content-collapse.html",
      "label": "隐藏的语义（折叠面板）"
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
      "label": "表格与列表结构语义"
    },
    {
      "group": null,
      "id": "content-note",
      "href": "problems-content-note.html",
      "label": "注意提示（Note）类型语义"
    },
    {
      "group": "交付格式",
      "id": "format",
      "href": "problems-format.html",
      "label": "交付格式"
    },
    {
      "group": "信息结构",
      "id": "structure-llms",
      "href": "problems-structure-llms.html",
      "label": "llms.txt 与机器入口"
    },
    {
      "group": null,
      "id": "structure-metadata",
      "href": "problems-structure-metadata.html",
      "label": "元数据字段规范"
    }
  ],
  "principles": [
    {
      "group": null,
      "id": "general",
      "href": "principles-general.html",
      "label": "总原则"
    },
    {
      "group": "时效",
      "id": "timeliness",
      "href": "principles-timeliness.html",
      "label": "版本滞后"
    },
    {
      "group": "语义理解",
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
      "label": "隐藏的语义（Tab）"
    },
    {
      "group": null,
      "id": "collapse",
      "href": "principles-collapse.html",
      "label": "隐藏的语义（折叠面板）"
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
      "label": "表格与列表结构语义"
    },
    {
      "group": null,
      "id": "note",
      "href": "principles-note.html",
      "label": "注意提示（Note）类型语义"
    },
    {
      "group": "交付格式",
      "id": "format",
      "href": "principles-format.html",
      "label": "交付格式"
    },
    {
      "group": "信息结构",
      "id": "structure-llms",
      "href": "principles-structure-llms.html",
      "label": "llms.txt 与机器入口"
    },
    {
      "group": null,
      "id": "structure-metadata",
      "href": "principles-structure-metadata.html",
      "label": "元数据字段规范"
    },
    {
      "group": null,
      "id": "tensor",
      "href": "principles-tensor.html",
      "label": "复杂内容：静态 Tensor"
    },
    {
      "group": null,
      "id": "cheatsheet",
      "href": "principles-cheatsheet.html",
      "label": "速查表"
    },
    {
      "group": null,
      "id": "ref-dialogs",
      "href": "principles-ref-dialogs.html",
      "label": "参考对话"
    }
  ]
};

  var SIDEBAR_TITLES = {
    problems: "信源感知",
    principles: "亲和原则"
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

  var html = "<div class=\"sidebar-title\">" + (SIDEBAR_TITLES[module] || "导航") + "</div>";
  if (module === "problems") {
    html += "<ul class=\"sidebar-nav sidebar-phase-nav\">";
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
})();
