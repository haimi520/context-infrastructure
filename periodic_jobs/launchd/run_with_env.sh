#!/bin/bash
# run_with_env.sh — launchd 包装器：加载仓库根目录 .env 后执行用户脚本。
# 用法：run_with_env.sh <relative-script> [args...]
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if [ -f "$REPO_ROOT/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "$REPO_ROOT/.env"
    set +a
fi

mkdir -p "$REPO_ROOT/logs"
cd "$REPO_ROOT"
exec "$REPO_ROOT/.venv/bin/python" "$@"
