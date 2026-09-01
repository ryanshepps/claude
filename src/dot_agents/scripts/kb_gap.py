#!/usr/bin/env python3
"""Record a knowledge-base gap: a task where no existing leaf fit.

Appended to `~/.agents/knowledge/<domain>/.stats/gaps.jsonl`, one JSON object
per line. `/knowledge-reflect` reads these as new-leaf candidates and the
SessionStart nudge counts unreviewed ones to decide when to prompt.

Domain must be `code` or `write`. Override the stats root with `--stats-root`
(used by tests); default is `~/.agents/knowledge`.
"""
import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

DOMAINS = {"code", "write"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", required=True, choices=sorted(DOMAINS))
    parser.add_argument("--note", required=True, help="one line: what was missing")
    parser.add_argument("--task", default="", help="short task context")
    parser.add_argument("--session-id", default="")
    parser.add_argument(
        "--stats-root",
        type=pathlib.Path,
        default=pathlib.Path.home() / ".agents" / "knowledge",
    )
    args = parser.parse_args()

    note = args.note.strip()
    if not note:
        print("FAIL: --note must be non-empty", file=sys.stderr)
        return 1

    stats_dir = args.stats_root / args.domain / ".stats"
    stats_dir.mkdir(parents=True, exist_ok=True)
    log = stats_dir / "gaps.jsonl"

    event = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "domain": args.domain,
        "note": note,
        "task": args.task.strip(),
        "session_id": args.session_id.strip(),
    }
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"Recorded {args.domain} gap → {log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
