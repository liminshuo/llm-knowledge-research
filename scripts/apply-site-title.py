#!/usr/bin/env python3
"""将全站网站标题统一为 SITE_CONFIG.title，并注入 site-config / site-init 脚本。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_TITLE = '社区AI亲和分析'
OLD_NAMES = (
    'Ascend C 文档大模型亲和规则研究',
    'Ascend C 文档大模型知识获取研究',
    '大模型知识获取研究',
)
SITE_SCRIPTS = (
    '<script src="assets/js/site-config.js"></script>\n'
    '<script src="assets/js/site-init.js"></script>\n'
)


def apply(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text

    for old in OLD_NAMES:
        text = text.replace(old, SITE_TITLE)

    if 'site-config.js' not in text and 'class="site-header"' in text:
        if '<script ' in text:
            text = text.replace('<script ', SITE_SCRIPTS + '<script ', 1)
        else:
            text = text.replace('</body>', SITE_SCRIPTS + '</body>', 1)

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.glob('*.html')):
        if apply(path):
            changed.append(path.name)
    print(f'Updated {len(changed)} files')
    for name in changed:
        print(f'  {name}')


if __name__ == '__main__':
    main()
