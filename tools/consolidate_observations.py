#!/usr/bin/env python3
"""consolidate_observations.py — 把 OBSERVATIONS.md 里的 mined 历史条目压缩成主题级记忆。

设计:
    - 474 条 mined 条目按顺序分成 N 个 chunk，每个 chunk 交给一个 agent 做主题归并
    - 再做一次跨 chunk 的最终合并（去重 + 控制总条数）
    - 组装 OBSERVATIONS.md：preamble 与未挖掘的每日观察块原样保留，
      mined 条目替换为单个 "Date: <start> ~ <end>" 主题块
    - 全程只写 contexts/memory/.consolidate/ 下的中间文件和最终产物，替换前留 .bak

用法:
    periodic_jobs/launchd/run_with_env.sh tools/consolidate_observations.py [--chunks 4] [--target 50] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "periodic_jobs" / "ai_heartbeat" / "src" / "v0"))

from opencode_client import OpenCodeClient  # noqa: E402

OBS = REPO_ROOT / "contexts" / "memory" / "OBSERVATIONS.md"
WORK = REPO_ROOT / "contexts" / "memory" / ".consolidate"
DATE_RE = re.compile(r"^Date: (\d{4}-\d{2}-\d{2})\s*$")

CHUNK_PROMPT = """【任务】把一批历史会话记忆条目合并成主题级记忆。

【输入文件】{src}（每行一条，格式 `[日期] 🔴/🟡 ...`）

【要求】
1. 按主题归并：同一技术坑、同一模块、同一方法论归到一起；不同主题不要强行合并
2. 去重但保留全部硬信息：命令、报错原文、端口/版本号、文件路径、协议条款、因果链
3. 输出去掉重复后信息量最大的 {target} 条左右（不超过 {cap} 条）
4. 条目格式严格如下（单行）：
   🔴 High: [主题标签] 合并后的内容 (mined from dsh ×N, YYYY-MM-DD..YYYY-MM-DD)
   其中 N 是被合并的原始条目数，日期范围取被合并条目的最早/最晚日期
5. 只保留 🔴 与 🟡；不新增输入里没有的事实；合并后每条仍须能独立读懂
6. 写入文件 {dst}（仅限这个文件，不要修改仓库中任何其他文件）
7. 文件内容只有条目行，不要标题、不要解释、不要代码块围栏

【汇报】完成后回复一句：输出了多少条。
"""

MERGE_PROMPT = """【任务】把 {n} 个分块的主题记忆文件合并成最终版。

【输入文件】
{srcs}

【要求】
1. 跨分块去重：同一主题出现在多个分块时合成一条，合并其中的事实
2. 最终输出 {target} 条左右（40-60 条之间），按重要性排序：硬性约束/跨项目方法论在前
3. 保留具体事实：命令、报错原文、数字、路径、协议条款——这是记忆的价值所在
4. 条目格式严格如下（单行）：
   🔴 High: [主题标签] 内容 (mined from dsh ×N, YYYY-MM-DD..YYYY-MM-DD)
5. 只保留 🔴 与 🟡；不新增输入中没有的事实
6. 写入文件 {dst}（仅限这个文件，不要修改任何其他文件）
7. 文件内容只有条目行，无标题、无解释、无围栏

【汇报】完成后回复一句：最终多少条。
"""


def parse_observations(text: str) -> tuple[str, list[tuple[str, list[str]]]]:
    """返回 (preamble, [(date, entries), ...])；代码围栏内的示例块不计入。"""
    lines = text.splitlines()
    preamble: list[str] = []
    blocks: list[tuple[str, list[str]]] = []
    cur_date: str | None = None
    cur_entries: list[str] = []
    in_fence = False
    seen_first_date = False

    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
        m = None if in_fence else DATE_RE.match(line)
        if m:
            if not seen_first_date:
                seen_first_date = True
            else:
                blocks.append((cur_date or "", cur_entries))
            cur_date, cur_entries = m.group(1), []
        elif not seen_first_date:
            preamble.append(line)
        elif line.startswith(("🔴", "🟡", "🟢")):
            cur_entries.append(line)
        elif line.strip() and cur_entries:
            # 续行（极少见）：并入上一条
            cur_entries[-1] += " " + line.strip()
    if seen_first_date:
        blocks.append((cur_date or "", cur_entries))
    return "\n".join(preamble).rstrip() + "\n", blocks


def run_agent(client: OpenCodeClient, title: str, prompt: str) -> bool:
    for attempt in (1, 2):
        sid = client.create_session(title)
        if not sid:
            print(f"  [{attempt}] create_session failed")
            time.sleep(10)
            continue
        client.send_message(sid, prompt)
        ok = client.wait_for_session_complete(sid, poll_interval=15, max_wait=2400)
        client.delete_session(sid)
        if ok:
            return True
        print(f"  [{attempt}] session did not complete")
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", type=int, default=4)
    ap.add_argument("--target", type=int, default=50)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = OBS.read_text(encoding="utf-8")
    preamble, blocks = parse_observations(text)

    mined: list[tuple[str, str]] = []
    keep_blocks: list[tuple[str, list[str]]] = []
    for date, entries in blocks:
        rest = [e for e in entries if "(mined from" not in e]
        mined += [(date, e) for e in entries if "(mined from" in e]
        if rest:
            keep_blocks.append((date, rest))

    print(f"blocks={len(blocks)} keep={len(keep_blocks)} mined={len(mined)}")
    if not mined:
        print("no mined entries; nothing to do")
        return 0

    WORK.mkdir(parents=True, exist_ok=True)
    size = (len(mined) + args.chunks - 1) // args.chunks
    chunk_files: list[Path] = []
    for i in range(args.chunks):
        part = mined[i * size : (i + 1) * size]
        if not part:
            continue
        src = WORK / f"chunk{i + 1}.in.md"
        src.write_text("\n".join(f"[{d}] {e}" for d, e in part) + "\n", encoding="utf-8")
        chunk_files.append(src)
        print(f"chunk{i + 1}: {len(part)} entries, {src.stat().st_size // 1024}KB")
    if args.dry_run:
        return 0

    start_date, end_date = mined[0][0], mined[-1][0]
    start_date = min(d for d, _ in mined)
    end_date = max(d for d, _ in mined)

    client = OpenCodeClient()
    outs: list[Path] = []
    for idx, src in enumerate(chunk_files, 1):
        dst = WORK / f"chunk{idx}.out.md"
        if dst.exists():
            dst.unlink()
        prompt = CHUNK_PROMPT.format(
            src=src.relative_to(REPO_ROOT),
            dst=dst.relative_to(REPO_ROOT),
            target=max(12, args.target // len(chunk_files)),
            cap=max(20, args.target // len(chunk_files) + 8),
        )
        print(f"[chunk {idx}/{len(chunk_files)}] consolidating...")
        if not run_agent(client, f"Memory Consolidation - chunk {idx}/{len(chunk_files)}", prompt):
            print("chunk failed")
            return 1
        if not dst.exists() or not dst.read_text(encoding="utf-8").strip():
            print(f"chunk {idx} produced no output")
            return 1
        outs.append(dst)
        time.sleep(3)

    final = WORK / "final.out.md"
    if final.exists():
        final.unlink()
    prompt = MERGE_PROMPT.format(
        n=len(outs),
        srcs="\n".join(f"- {p.relative_to(REPO_ROOT)}" for p in outs),
        target=args.target,
        dst=final.relative_to(REPO_ROOT),
    )
    print("[final merge] ...")
    if not run_agent(client, "Memory Consolidation - final merge", prompt):
        print("final merge failed")
        return 1
    if not final.exists() or not final.read_text(encoding="utf-8").strip():
        print("final merge produced no output")
        return 1

    final_lines = [ln.strip() for ln in final.read_text(encoding="utf-8").splitlines() if ln.strip()]
    final_lines = [ln for ln in final_lines if ln.startswith(("🔴", "🟡", "🟢"))]
    print(f"final entries: {len(final_lines)}")

    out_parts = [preamble.rstrip(), ""]
    for date, entries in keep_blocks:
        out_parts += [f"Date: {date}", ""]
        out_parts += entries
        out_parts.append("")
    out_parts += [
        f"Date: {start_date} ~ {end_date}",
        "",
        f"<!-- 以下 {len(final_lines)} 条由 {len(mined)} 条历史会话记忆（dsh 194 个会话）归并压缩而来 -->",
        "",
    ]
    out_parts += final_lines
    out_parts.append("")
    new_text = "\n".join(out_parts)

    backup = OBS.with_suffix(".md.bak")
    shutil.copy2(OBS, backup)
    OBS.write_text(new_text, encoding="utf-8")
    print(f"written {OBS} ({len(text)} -> {len(new_text)} bytes); backup at {backup.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
