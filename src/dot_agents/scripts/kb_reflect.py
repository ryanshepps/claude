#!/usr/bin/env python3
"""Mine knowledge-base telemetry into curation candidates for review.

Reads three files under `<knowledge-dir>/.stats/` (override with `--stats-dir`):

- `fetches.jsonl`  — one `{ts, path, domain, session_id?, cwd?}` per KB Read.
- `gaps.jsonl`     — one `{ts, domain, note, task?, session_id?}` per recorded miss.
- `last_reviewed`  — ISO-8601 UTC watermark written by `--mark-reviewed`.

Emits a markdown report (or `--json`) of candidate edits, never mutating the
corpus. `/knowledge-reflect` presents it; the human approves each edit. The
deterministic signals here are proposals, not decisions — fetch counts are a
weak proxy, so priority and deletion calls stay with the reviewer.

`--mark-reviewed` writes the watermark to now and exits; run it after a review
so the SessionStart nudge resets.
"""
import argparse
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations

MIN_COFETCH_SESSIONS = 2
HOT_FETCH_MIN = 3
COLD_KEEP_PRIORITY = 2


class Leaf:
    def __init__(self, slug: str, priority: int, related: list[str], categories: list[str]):
        self.slug = slug
        self.priority = priority
        self.related = related
        self.categories = categories


def parse_leaf(path: pathlib.Path) -> Leaf | None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = m.group(1)
    if re.search(r"^type:\s*moc\s*$", fm, re.MULTILINE):
        return None

    def scalar(name: str) -> str:
        mm = re.search(rf"^{name}:\s*(.*)$", fm, re.MULTILINE)
        return mm.group(1).strip() if mm else ""

    def list_field(name: str) -> list[str]:
        inline = re.search(rf"^{name}:\s*\[(.*?)\]\s*$", fm, re.MULTILINE)
        if inline:
            raw = inline.group(1).strip()
            return [x.strip() for x in raw.split(",") if x.strip()] if raw else []
        block = re.search(rf"^{name}:\s*\n((?:  - .*\n?)+)", fm, re.MULTILINE)
        if block:
            return [ln.removeprefix("  - ").strip() for ln in block.group(1).splitlines() if ln.strip()]
        return []

    slug = scalar("slug") or path.stem
    priority_raw = scalar("priority")
    priority = int(priority_raw) if priority_raw.isdigit() else 3
    return Leaf(slug, priority, list_field("related"), list_field("categories"))


def load_leaves(knowledge_dir: pathlib.Path) -> dict[str, Leaf]:
    leaves: dict[str, Leaf] = {}
    for path in sorted(knowledge_dir.glob("*.md")):
        if path.stem == "index":
            continue
        leaf = parse_leaf(path)
        if leaf is not None:
            leaves[leaf.slug] = leaf
    return leaves


def read_jsonl(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def read_watermark(stats_dir: pathlib.Path) -> str:
    wm = stats_dir / "last_reviewed"
    if not wm.exists():
        return ""
    return wm.read_text(encoding="utf-8").strip()


def slug_of(path: str) -> str:
    return pathlib.PurePath(path).stem


def build_report(knowledge_dir: pathlib.Path, stats_dir: pathlib.Path, domain: str) -> dict:
    leaves = load_leaves(knowledge_dir)
    leaf_slugs = set(leaves)
    fetches = read_jsonl(stats_dir / "fetches.jsonl")
    gaps = read_jsonl(stats_dir / "gaps.jsonl")
    watermark = read_watermark(stats_dir)

    pending_gaps = [g for g in gaps if g.get("ts", "") > watermark]

    fetch_counts: Counter[str] = Counter()
    session_leaves: dict[str, set[str]] = defaultdict(set)
    for row in fetches:
        slug = slug_of(row.get("path", ""))
        if slug not in leaf_slugs:
            continue
        fetch_counts[slug] += 1
        sid = row.get("session_id", "")
        if sid:
            session_leaves[sid].add(slug)

    pair_sessions: Counter[tuple[str, str]] = Counter()
    for slugs in session_leaves.values():
        for a, b in combinations(sorted(slugs), 2):
            pair_sessions[(a, b)] += 1

    missing_links = []
    for (a, b), n in pair_sessions.most_common():
        if n < MIN_COFETCH_SESSIONS:
            continue
        if b in leaves[a].related or a in leaves[b].related:
            continue
        missing_links.append({"a": a, "b": b, "sessions": n})

    cold_demote = []
    cold_keep = []
    for slug, leaf in sorted(leaves.items(), key=lambda kv: (kv[1].priority, kv[0])):
        if fetch_counts.get(slug, 0) > 0:
            continue
        record = {"slug": slug, "priority": leaf.priority}
        if leaf.priority <= COLD_KEEP_PRIORITY:
            cold_keep.append(record)
        else:
            cold_demote.append(record)

    hot_low_priority = [
        {"slug": slug, "priority": leaves[slug].priority, "fetches": count}
        for slug, count in fetch_counts.most_common()
        if count >= HOT_FETCH_MIN and leaves[slug].priority >= 4
    ]

    return {
        "domain": domain,
        "knowledge_dir": str(knowledge_dir),
        "stats_dir": str(stats_dir),
        "watermark": watermark or "(never reviewed — all telemetry is pending)",
        "totals": {
            "leaves": len(leaves),
            "fetch_events": len(fetches),
            "sessions": len(session_leaves),
            "gap_events": len(gaps),
            "pending_gaps": len(pending_gaps),
        },
        "gap_candidates": pending_gaps,
        "missing_links": missing_links,
        "cold_demote": cold_demote,
        "cold_keep": cold_keep,
        "hot_low_priority": hot_low_priority,
    }


def cap_list(items: list[str], limit: int = 15) -> list[str]:
    if len(items) <= limit:
        return items
    return items[:limit] + [f"- …and {len(items) - limit} more"]


def render_markdown(report: dict) -> str:
    t = report["totals"]
    thin = t["fetch_events"] < 30
    lines = [
        f"# Knowledge Reflection — {report['domain']}",
        "",
        f"Knowledge dir: {report['knowledge_dir']}",
        f"Watermark: {report['watermark']}",
        f"Leaves: {t['leaves']} · Fetch events: {t['fetch_events']} · "
        f"Sessions: {t['sessions']} · Gaps: {t['gap_events']} "
        f"({t['pending_gaps']} pending)",
        "",
    ]

    lines += ["## New-leaf candidates (recorded gaps)", ""]
    if report["gap_candidates"]:
        for g in report["gap_candidates"]:
            task = f" — task: {g['task']}" if g.get("task") else ""
            lines.append(f"- {g.get('note', '(no note)')}{task}  ·  {g.get('ts', '')}")
    else:
        lines.append("- (none pending)")
    lines.append("")

    lines += ["## Missing `related:` links (co-fetched, not linked)", ""]
    if report["missing_links"]:
        for link in report["missing_links"]:
            lines.append(
                f"- `{link['a']}` ↔ `{link['b']}` — co-fetched in {link['sessions']} sessions"
            )
    else:
        lines.append("- (none — pairs need session_id on fetch events and ≥2 shared sessions)")
    lines.append("")

    lines += ["## Priority signals (hot but low-priority — weak proxy, you decide)", ""]
    if report["hot_low_priority"]:
        for h in report["hot_low_priority"]:
            lines.append(f"- `{h['slug']}` (p{h['priority']}) — fetched {h['fetches']}×; consider bump")
    else:
        lines.append("- (none)")
    lines.append("")

    lines += ["## Cold leaves — demote/delete candidates (p3-5, never fetched)", ""]
    if thin:
        lines.append(f"- (skipped — only {t['fetch_events']} fetch events; cold lists need a fuller log to mean anything)")
    elif report["cold_demote"]:
        lines += cap_list([f"- `{c['slug']}` (p{c['priority']})" for c in report["cold_demote"]])
    else:
        lines.append("- (none)")
    lines.append("")

    keep = report["cold_keep"]
    lines += ["## Cold but foundational — keep (p1-2, never fetched)", ""]
    if thin:
        lines.append(f"- (skipped — thin log; {len(keep)} p1-2 leaves currently unfetched)")
    elif keep:
        lines.append(f"{len(keep)} foundational leaves are cold. Cold ≠ useless — do not demote on fetch count:")
        lines += cap_list([f"- `{c['slug']}` (p{c['priority']})" for c in keep])
    else:
        lines.append("- (none)")
    lines.append("")

    return "\n".join(lines)


def detect_domain(knowledge_dir: pathlib.Path) -> str:
    name = knowledge_dir.name
    if name not in {"code", "write"}:
        print(f"FAIL: knowledge-dir basename must be 'code' or 'write'; got '{name}'", file=sys.stderr)
        sys.exit(1)
    return name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_kb = pathlib.Path(__file__).resolve().parent.parent / "knowledge" / "code"
    parser.add_argument("--knowledge-dir", type=pathlib.Path, default=default_kb)
    parser.add_argument("--stats-dir", type=pathlib.Path, default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--mark-reviewed", action="store_true")
    args = parser.parse_args()

    kb = args.knowledge_dir.resolve()
    if not kb.is_dir():
        print(f"FAIL: knowledge dir not found: {kb}", file=sys.stderr)
        return 1
    domain = detect_domain(kb)
    stats_dir = args.stats_dir.resolve() if args.stats_dir else kb / ".stats"

    if args.mark_reviewed:
        stats_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        (stats_dir / "last_reviewed").write_text(now + "\n", encoding="utf-8")
        print(f"[{domain}] watermark advanced → {now}")
        return 0

    report = build_report(kb, stats_dir, domain)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
