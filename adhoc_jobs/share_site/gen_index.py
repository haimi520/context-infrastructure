#!/usr/bin/env python3
"""从 manifest.json 生成 site/index.html（仅列出 indexed: true 的文章）。"""
import html
import json
import sys
from pathlib import Path

def main():
    site_dir = Path(__file__).resolve().parent
    manifest = json.loads((site_dir / "manifest.json").read_text(encoding="utf-8"))
    articles = [a for a in manifest.get("articles", []) if a.get("indexed")]
    articles.sort(key=lambda a: a.get("date", ""), reverse=True)

    rows = "\n".join(
        f'<li><a href="{html.escape(a["slug"])}.html">{html.escape(a["title"])}</a>'
        f'<span class="date">{html.escape(a.get("date", ""))}</span></li>'
        for a in articles
    )
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Share Index</title>
<link rel="stylesheet" href="share_report.css">
</head>
<body>
<main>
<h1>分享索引</h1>
<ul class="index-list">
{rows}
</ul>
</main>
</body>
</html>
"""
    (site_dir / "site" / "index.html").write_text(page, encoding="utf-8")
    print(f"index.html generated ({len(articles)} indexed articles)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
