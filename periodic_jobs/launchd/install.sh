#!/bin/bash
# install.sh — 把本目录的 launchd agent 安装到 ~/Library/LaunchAgents 并加载。
# 用法：./install.sh            安装全部并加载
#       ./install.sh uninstall 反安装
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LAUNCHD_DIR="$REPO_ROOT/periodic_jobs/launchd"
LABELS=(
    com.contextinfra.opencode-server
    com.contextinfra.heartbeat-observer
    com.contextinfra.heartbeat-reflector
)
GID="$(id -u)"

if [ "${1:-}" = "uninstall" ]; then
    for label in "${LABELS[@]}"; do
        launchctl bootout "gui/$GID/$label" 2>/dev/null || true
        rm -f "$HOME/Library/LaunchAgents/$label.plist"
    done
    echo "uninstalled."
    exit 0
fi

for label in "${LABELS[@]}"; do
    launchctl bootout "gui/$GID/$label" 2>/dev/null || true
    sleep 1
    cp "$LAUNCHD_DIR/$label.plist" "$HOME/Library/LaunchAgents/$label.plist"
    launchctl bootstrap "gui/$GID" "$HOME/Library/LaunchAgents/$label.plist"
done

# server 立即启动（KeepAlive 模式）；observer/reflector 只注册日程，不手动触发
launchctl kickstart -k "gui/$GID/com.contextinfra.opencode-server"
echo "installed. server should be listening on 127.0.0.1:4096."
