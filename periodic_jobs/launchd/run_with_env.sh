#!/bin/bash
# run_with_env.sh — launchd 包装器：加载 .env，确保 opencode 后台服务可用（解析端口与凭证），再运行目标脚本。
# 用法：run_with_env.sh <relative-script> [args...]
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OPENCODE_BIN="${OPENCODE_BIN:-/opt/homebrew/bin/opencode}"
PYVENV="$REPO_ROOT/.venv/bin/python"

if [ -f "$REPO_ROOT/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "$REPO_ROOT/.env"
    set +a
fi

# opencode v2 自带后台服务（`opencode service`，由桌面端登录项托管，父进程 launchd）。
# systemctl 风格：start 幂等，永远返回当前监听 URL；凭证在 ~/.config/opencode/service.json。
ensure_opencode_service() {
    [ -x "$OPENCODE_BIN" ] || return 0
    local url
    url="$("$OPENCODE_BIN" service start 2>/dev/null | tail -1 || true)"
    if [ -z "$url" ]; then
        url="$("$OPENCODE_BIN" service status 2>/dev/null | tail -1 || true)"
    fi
    case "$url" in
        http*)
            export OPENCODE_BASE_URL="${url%/}/api"
            ;;
    esac
    local svc="$HOME/.config/opencode/service.json"
    if [ -r "$svc" ]; then
        export OPENCODE_PASSWORD="$("$PYVENV" -c 'import json,sys;print(json.load(open(sys.argv[1])).get("password",""))' "$svc")"
    fi
}
ensure_opencode_service || true

mkdir -p "$REPO_ROOT/logs"
cd "$REPO_ROOT"
exec "$PYVENV" "$@"
