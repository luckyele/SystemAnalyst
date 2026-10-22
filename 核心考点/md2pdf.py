# -*- coding: utf-8 -*-
"""把《核心考点》目录下的 Markdown 章节渲染成与既有章节同风格的 A4 PDF。

用法：python md2pdf.py [章节名关键字]
      不带参数时转换目录内全部 .md 章节。
依赖：pip install markdown weasyprint
"""
import os
import sys

import markdown
from weasyprint import HTML, CSS

BASE = os.path.dirname(os.path.abspath(__file__))

CSS_TEXT = """
@page {
  size: A4;
  margin: 44pt 42pt 42pt 42pt;
}
body {
  font-family: "Noto Sans CJK SC", "Source Han Sans SC", sans-serif;
  font-size: 11.2pt;
  line-height: 1.66;
  color: #000;
  margin: 0;
  text-align: justify;
}
h1 { font-size: 11.2pt; font-weight: 700; margin: 0 0 8pt 0; line-height: 1.6; }
h2 { font-size: 12.6pt; font-weight: 700; margin: 13pt 0 6pt 0; line-height: 1.6; }
h3 { font-size: 11.2pt; font-weight: 700; margin: 10pt 0 4pt 0; line-height: 1.6; }
p { margin: 0 0 5pt 0; }
ul, ol { margin: 0 0 5pt 0; padding-left: 20pt; }
li { margin: 0; }
li > ul, li > ol { margin: 0; }
strong { font-weight: 700; }
blockquote {
  margin: 6pt 0 0 0;
  padding: 2pt 0 2pt 10pt;
  border-left: 3pt solid #d0d7de;
  color: #444;
  font-size: 9.8pt;
}
blockquote p { margin: 0 0 3pt 0; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 4pt 0 8pt 0;
  font-size: 9.8pt;
  line-height: 1.6;
}
th, td {
  border: 0.6pt solid #b9c0c8;
  padding: 3pt 6pt;
  text-align: left;
  vertical-align: top;
}
th { background: #f2f4f7; font-weight: 700; }
h1, h2, h3, h4, h5, h6 { bookmark-level: none; }
"""


def convert(md_path: str) -> str:
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    title = os.path.splitext(os.path.basename(md_path))[0]
    body = markdown.markdown(text, extensions=["tables", "sane_lists"], output_format="html5")
    html = (
        f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
        f"<title>{title}</title><style>{CSS_TEXT}</style></head><body>{body}</body></html>"
    )
    out_path = os.path.splitext(md_path)[0] + ".pdf"
    HTML(string=html, base_url=BASE).write_pdf(out_path, stylesheets=[CSS(string=CSS_TEXT)])
    return out_path


def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else ""
    for name in sorted(os.listdir(BASE)):
        if not name.endswith(".md") or keyword not in name:
            continue
        print("已生成:", convert(os.path.join(BASE, name)))


if __name__ == "__main__":
    main()
