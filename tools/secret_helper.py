"""Secrets helper — 敏感值的统一检索：环境变量优先，缺省回落 macOS 钥匙串。

钥匙串条目约定：service = CONTEXTINFRA_<NAME>，account = $USER。
写入方式（一次性）:
    security add-generic-password -a "$USER" -s CONTEXTINFRA_<NAME> -w '<值>' -U
"""
import os
import subprocess

PREFIX = "CONTEXTINFRA_"


def keychain_get(name: str) -> str:
    """从 macOS 钥匙串读取 CONTEXTINFRA_<name>；不存在返回空串。"""
    account = os.environ.get("USER", "")
    try:
        r = subprocess.run(
            ["security", "find-generic-password", "-a", account, "-s", f"{PREFIX}{name}", "-w"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return ""


def get_secret(name: str) -> str:
    """环境变量优先（供 run_with_env.sh 预注入），否则查钥匙串。"""
    value = os.environ.get(name, "")
    if value:
        return value
    return keychain_get(name)
