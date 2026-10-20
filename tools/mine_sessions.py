#!/usr/bin/env python3
"""mine_sessions.py — 从 contexts/ai_sessions 历史会话批量提取记忆条目到 OBSERVATIONS.md。

用法:
    .venv/bin/python tools/mine_sessions.py --source dsh --batch 15 [--limit 30] [--dry-run]

设计:
    - 复用 opencode_client（与 observer 同一条服务通道，模型走 OPENCODE_MODEL）
    - 每批 N 个会话文件喂给 agent，只提取 🔴/🟡，带 mined from 来源
    - agent 直接 append 写 OBSERVATIONS.md（与 observer 相同的持久化模式）
    - 幂等：批内提示 agent 检查已提取来源；state 记录已处理批次
"""
import argparse
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "periodic_jobs" / "ai_heartbeat" / "src" / "v0"))

from opencode_client import OpenCodeClient  # noqa: E402

PROMPT_TEMPLATE = """
【目标】：从历史 AI 会话归档中提取有长期价值的记忆，直接追加写入 contexts/memory/OBSERVATIONS.md。

【本次批次会话文件】（均为相对仓库根的路径）：
{files}

【提取标准】（沿用 periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md 的分级定义，先读它）：
- 🔴 High：跨项目通用的经验教训、硬性约束、方法论——这是重点
- 🟡 Medium：关键技术决策、架构变更及背景
- 🟢 Low：任务流水——一律忽略，不写入

【硬性要求】：
1. 逐个阅读上述会话文件（每个是一段完整人机会话，frontmatter 有来源项目路径）
2. 提取时按会话自身的日期归档：若 OBSERVATIONS.md 已有该日期的 `Date: YYYY-MM-DD` 块，
   在该块末尾追加条目；没有则新建日期块。绝不新建重复的日期行。
3. 每条末尾必须标注来源：`(mined from <该会话文件的相对路径>)`
4. 幂等：写入前先 grep OBSERVATIONS.md 中是否已有相同来源标注，有则跳过该来源
5. 只做 append，不修改既有行，不动 rules/ 下任何文件
6. 语言风格与现有条目一致（简体中文，紧凑，事实优先）

【汇报】：完成后回复简短 Walkthrough（提取了几条、分布哪些日期、跳过了哪些）。
"""


def main():
    parser = argparse.ArgumentParser(description="Mine historical AI sessions into OBSERVATIONS.md")
    parser.add_argument("--source", default="dsh", choices=["dsh", "hermes", "opencode", "codex", "claude_code"])
    parser.add_argument("--batch", type=int, default=15)
    parser.add_argument("--limit", type=int, default=0, help="0 = all pending files")
    parser.add_argument("--state-file", default=str(REPO_ROOT / "contexts" / "memory" / ".mining_state.json"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    import json
    state_path = Path(args.state_file)
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    processed = set(state.get(args.source, []))

    source_dir = REPO_ROOT / "contexts" / "ai_sessions" / args.source
    files = sorted(source_dir.glob("*.md"))
    pending = [f for f in files if str(f.relative_to(REPO_ROOT)) not in processed]
    if args.limit:
        pending = pending[: args.limit]
    print(f"source={args.source} total={len(files)} processed={len(processed)} pending={len(pending)}")
    if args.dry_run:
        for f in pending:
            print("  would mine:", f.name)
        return 0
    if not pending:
        print("nothing to mine")
        return 0

    client = OpenCodeClient()
    batches = [pending[i : i + args.batch] for i in range(0, len(pending), args.batch)]
    for idx, batch in enumerate(batches, 1):
        rel_paths = "\n".join(str(f.relative_to(REPO_ROOT)) for f in batch)
        prompt = PROMPT_TEMPLATE.format(files=rel_paths)
        title = f"Heartbeat Mining L1.5 - {args.source} batch {idx}/{len(batches)}"
        print(f"[batch {idx}/{len(batches)}] {len(batch)} files -> {title}")
        session_id = client.create_session(title)
        if not session_id:
            print("  create_session failed, abort")
            return 1
        client.send_message(session_id, prompt)
        ok = client.wait_for_session_complete(session_id, poll_interval=15, max_wait=3600)
        client.delete_session(session_id)
        if ok:
            processed.update(str(f.relative_to(REPO_ROOT)) for f in batch)
            state[args.source] = sorted(processed)
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
            print(f"  batch {idx} done (state saved)")
        else:
            print(f"  batch {idx} incomplete; state not advanced")
            return 1
        time.sleep(5)
    print("mining complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
