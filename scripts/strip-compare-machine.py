#!/usr/bin/env python3
"""统一处理原则页对照示例：删除「❌ 当前渲染 / ✅ 亲和渲染」两个小标题，
删除红色（machine / 当前渲染）示例块，只保留绿色（human / 亲和渲染）示例。

仅作用于 principles-*.html。每个待删元素都在独立单行，按行删除即可。
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 待删除的整行（strip 后）特征
DROP_PATTERNS = [
    re.compile(r'^<h4 class="compare-label compare-label--machine">.*</h4>$'),
    re.compile(r'^<h4 class="compare-label compare-label--human">.*</h4>$'),
    re.compile(r'^<div class="compare-col machine">.*</div>$'),
]


def should_drop(line: str) -> bool:
    s = line.strip()
    return any(p.match(s) for p in DROP_PATTERNS)


def main():
    total_files = 0
    total_dropped = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "principles-*.html"))):
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        kept = [ln for ln in lines if not should_drop(ln)]
        dropped = len(lines) - len(kept)
        if dropped:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(kept)
            total_files += 1
            total_dropped += dropped
            print(f"{os.path.basename(path)}: -{dropped} 行")
    print(f"\n共处理 {total_files} 个文件，删除 {total_dropped} 行")


if __name__ == "__main__":
    main()
