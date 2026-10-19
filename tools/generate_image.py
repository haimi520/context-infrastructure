#!/usr/bin/env python3
"""图谱生成 CLI —— SiliconFlow 图像接口（Kolors 免费档起）。

用法:
    python3 tools/generate_image.py "prompt" -o out.png
    python3 tools/generate_image.py "prompt" --model Tongyi-MAI/Z-Image-Turbo --size 1024x1024

环境变量（仓库根 .env 自动加载）:
    SEMANTIC_EMBEDDING_API_KEY — 与语义搜索共用同一把 SiliconFlow key
    IMAGE_API_KEY              — 可选覆盖
    IMAGE_API_BASE             — 可选，默认 https://api.siliconflow.cn/v1
"""
import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path


def load_repo_env():
    import re
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"\'')
        if k and k not in os.environ:
            os.environ[k] = v


def main():
    parser = argparse.ArgumentParser(description="Generate an image via an OpenAI-compatible image endpoint")
    parser.add_argument("prompt", help="Image prompt")
    parser.add_argument("-o", "--output", default="generated_image.png")
    parser.add_argument("--model", default=os.environ.get("IMAGE_GENERATION_MODEL", "Kwai-Kolors/Kolors"))
    parser.add_argument("--size", default="1024x1024", help='e.g. 1024x1024 (use "adaptive" for some models)')
    parser.add_argument("--api-base", default=os.environ.get("IMAGE_API_BASE", "https://api.siliconflow.cn/v1"))
    args = parser.parse_args()

    load_repo_env()
    api_key = os.getenv("IMAGE_API_KEY") or os.getenv("SEMANTIC_EMBEDDING_API_KEY")
    if not api_key:
        print("Error: set SEMANTIC_EMBEDDING_API_KEY (or IMAGE_API_KEY) in .env")
        return 1

    payload = {"model": args.model, "prompt": args.prompt}
    if args.size and args.size != "adaptive":
        payload["image_size"] = args.size

    req = urllib.request.Request(
        f"{args.api_base.rstrip('/')}/images/generations",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())

    images = data.get("images") or []
    if not images:
        print(f"No images returned: {data}")
        return 1

    image_url = images[0].get("url")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(image_url, out)
    print(f"saved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
