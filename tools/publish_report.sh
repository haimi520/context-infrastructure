#!/bin/bash
# publish_report.sh — 把 Markdown 报告转成 HTML 并发布到 GitHub Pages 本地仓。
# 用法: publish_report.sh <input.md> <slug> [--title "标题"] [--indexed] [--push]
#
# 前置:
#   PAGES_REPO_DIR 指向 GitHub Pages 仓库的本地 clone（含 site/ 目录软链或直接以此为 site 根）
#   repo .env 的域名/账号无需配置；CSS 取自 tools/share_report.css
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# 加载仓库 .env（PAGES_REPO_DIR 等配置）
if [ -f "$REPO_ROOT/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "$REPO_ROOT/.env"
    set +a
fi

SITE_DIR="$REPO_ROOT/adhoc_jobs/share_site/site"
MANIFEST="$REPO_ROOT/adhoc_jobs/share_site/manifest.json"
CSS_SRC="$REPO_ROOT/tools/share_report.css"
PAGES_REPO_DIR="${PAGES_REPO_DIR:-}"

INPUT=""
SLUG=""
TITLE=""
INDEXED=0
DO_PUSH=0

while [ $# -gt 0 ]; do
    case "$1" in
        --title) TITLE="$2"; shift 2 ;;
        --indexed) INDEXED=1; shift ;;
        --push) DO_PUSH=1; shift ;;
        *) if [ -z "$INPUT" ]; then INPUT="$1"; else SLUG="$1"; fi; shift ;;
    esac
done

[ -n "$INPUT" ] && [ -n "$SLUG" ] || { echo "usage: publish_report.sh <input.md> <slug> [--title T] [--indexed] [--push]"; exit 2; }
[ -n "$TITLE" ] || TITLE=$(basename "$INPUT" .md)
DATE=$(date +%F)

mkdir -p "$SITE_DIR"
cp "$CSS_SRC" "$SITE_DIR/share_report.css" 2>/dev/null || true

# 1. 去掉首行 H1（pandoc metadata title 会再生成一个）
NO_H1="/tmp/${SLUG}_no_h1.md"
tail -n +2 "$INPUT" > "$NO_H1"

# 2. SEO meta 片段（境内访问无 GA4/TTS，跳过）
DESC=$(python3 -c "import sys; t=open(sys.argv[1],encoding='utf-8').read(400); print(' '.join(t.split())[:140])" "$INPUT")
SEO="/tmp/${SLUG}_seo.html"
cat > "$SEO" <<EOF
<meta name="description" content="$DESC">
<meta property="og:title" content="$TITLE">
<meta property="og:description" content="$DESC">
<meta property="og:type" content="article">
<meta property="article:published_time" content="$DATE">
EOF

# 3. pandoc 转换（cwd=site 目录，使 --css 相对名既可解析又能正确输出相对链接）
(
    cd "$SITE_DIR"
    pandoc "$NO_H1" \
        -o "${SLUG}.html" \
        --standalone \
        --embed-resources \
        --metadata title="$TITLE" \
        --css share_report.css \
        --include-in-header="$SEO"
)

# 4. manifest 增量（python 原子更新）
MANIFEST="$MANIFEST" PAGES_REPO_DIR="$PAGES_REPO_DIR" SLUG="$SLUG" TITLE="$TITLE" ARTICLE_DATE="$DATE" DESC="$DESC" INDEXED="$INDEXED" \
python3 - <<'PYEOF'
import json, os
from pathlib import Path
manifest_path = Path(os.environ["MANIFEST"])
data = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"articles": []}
articles = [a for a in data.get("articles", []) if a.get("slug") != os.environ["SLUG"]]
articles.append({
    "slug": os.environ["SLUG"],
    "title": os.environ["TITLE"],
    "date": os.environ["ARTICLE_DATE"],
    "description": os.environ["DESC"],
    "author": "hill",
    "indexed": os.environ["INDEXED"] == "1",
    "is_temporary": False,
})
manifest_path.write_text(json.dumps({"articles": articles}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"manifest updated: {len(articles)} articles")
PYEOF

# 5. 索引页（仅 indexed 条目）
python3 "$REPO_ROOT/adhoc_jobs/share_site/gen_index.py"

# 6. 发布到 GitHub Pages 本地仓
if [ "$DO_PUSH" = "1" ]; then
    [ -n "$PAGES_REPO_DIR" ] && [ -d "$PAGES_REPO_DIR/.git" ] || { echo "PAGES_REPO_DIR 未配置或不是 git 仓库"; exit 2; }
    cp -f "$SITE_DIR/${SLUG}.html" "$SITE_DIR/share_report.css" "$SITE_DIR/index.html" "$PAGES_REPO_DIR/" 2>/dev/null || true
    git -C "$PAGES_REPO_DIR" add -A
    git -C "$PAGES_REPO_DIR" commit -m "publish: $SLUG" || echo "nothing to commit"
    git -C "$PAGES_REPO_DIR" push
    echo "published."
else
    echo "local build done: $SITE_DIR/${SLUG}.html (未 push；加 --push 且配置 PAGES_REPO_DIR 后发布)"
fi
