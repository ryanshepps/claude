#!/usr/bin/env python3
"""Regenerate category MOCs and index.md from leaf frontmatter.

Default knowledge dir is `../knowledge` relative to this script. Override with
`--knowledge-dir <path>` when running outside the standard layout.
"""
import argparse
import pathlib
import re
import sys
from collections import defaultdict
from typing import TypedDict


class Leaf(TypedDict):
    slug: str
    categories: list[str]
    priority: int
    description: str


CATEGORY_META: dict[str, tuple[str, str, str]] = {
    "architecture": (
        "Architecture",
        "Laws governing system structure, coupling, service boundaries.",
        "How components couple, where boundaries fall, and why organizational shape leaks into design. Reach for these when scoping services, drawing boundaries, or diagnosing coupling.",
    ),
    "design": (
        "Design",
        "Code patterns: DRY, KISS, YAGNI, SOLID, abstractions, coupling.",
        "Code-level patterns for what to abstract, what to leave concrete, and when copying beats unifying. Use when shaping a module, naming the duplication threshold, or pruning premature abstractions.",
    ),
    "teams": (
        "Teams",
        "Organizational dynamics, communication, team sizing, coordination.",
        "How org dynamics shape software outcomes — sizing, communication overhead, coordination cost. Use when planning team shape, splitting work, or diagnosing throughput drops.",
    ),
    "planning": (
        "Planning",
        "Estimation, timelines, optimization decisions, scoping.",
        "Estimation, sequencing, and scoping heuristics. Use when sizing work, picking what to optimize, or cutting scope under time pressure.",
    ),
    "quality": (
        "Quality",
        "Testing, technical debt, code health, resilience.",
        "Testing strategy, debt, resilience, and code-health practices. Use when writing tests, weighing rewrites, or judging whether code can survive in production.",
    ),
    "scale": (
        "Scale",
        "Performance, concurrency, parallelization limits, network effects.",
        "Limits on parallelization, network effects, and where adding hardware stops paying. Use when optimizing throughput or sizing concurrent systems.",
    ),
    "decisions": (
        "Decisions",
        "Cognitive biases, heuristics, mental models for reasoning.",
        "Cognitive biases, heuristics, and reasoning models. Use when stuck, choosing between options, or sanity-checking your own confidence.",
    ),
    "languages": (
        "Languages",
        "Per-language coding rules and style guides.",
        "One leaf per language with idioms, error handling, and testing conventions. Fetch the leaf matching the language you're writing.",
    ),
    "testing": ("Testing", "Test writing principles and patterns.", ""),
    "prs": ("PRs", "Pull request workflow and review process.", ""),
    "style": ("Style", "Universal coding style rules.", ""),
    "communication": ("Communication", "How to converse with users about code.", ""),
    "ux": (
        "UX",
        "User experience laws: perception, cognition, decision-making, interaction patterns.",
        "Perception, cognition, and interaction laws governing how users experience interfaces. Use when designing flows, hierarchies, or surfaces users touch.",
    ),
}

CATEGORY_TENSIONS: dict[str, list[str]] = {
    "quality": [
        "**Boy-scout rule** vs **surgical changes** — opportunistic cleanup improves code health, but uninvited refactors bloat diff scope. Apply boy-scout for trivial single-line fixes adjacent to your task; stay surgical when reviewers need a tight, focused diff.",
    ],
}

GROUP_ORDER: list[tuple[str, list[str], str]] = [
    (
        "Task territories (software engineering laws)",
        ["architecture", "design", "teams", "planning", "quality", "scale", "decisions"],
        "Engineering laws grouped by the kind of decision they inform.",
    ),
    (
        "UX & Design",
        ["ux"],
        "User-facing perception and interaction laws.",
    ),
    (
        "Languages",
        ["languages"],
        "Per-language style and idiom rules. Fetch when writing code in that language.",
    ),
    (
        "Cross-cutting",
        ["testing", "prs", "style", "communication"],
        "Process and craft rules that apply regardless of language or layer.",
    ),
]


def parse_frontmatter(path: pathlib.Path) -> Leaf | None:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = m.group(1)

    def field(name: str) -> str:
        mm = re.search(rf"^{name}:\s*(.*)$", fm, re.MULTILINE)
        return mm.group(1).strip() if mm else ""

    cats_raw = field("categories")
    cats = [c.strip() for c in cats_raw.strip("[]").split(",") if c.strip()]
    priority_raw = field("priority")
    priority = int(priority_raw) if priority_raw.isdigit() else 3
    return Leaf(
        slug=field("slug"),
        categories=cats,
        priority=priority,
        description=field("description"),
    )


def group_by_category(leaves: list[Leaf]) -> dict[str, list[Leaf]]:
    groups: dict[str, list[Leaf]] = defaultdict(list)
    for leaf in leaves:
        for cat in leaf["categories"]:
            groups[cat].append(leaf)
    for cat in groups:
        groups[cat].sort(key=lambda x: (x["priority"], x["slug"]))
    return groups


def render_moc(cat: str, leaves: list[Leaf]) -> str:
    title, desc, orientation = CATEGORY_META.get(cat, (cat.capitalize(), f"{cat} entries", ""))
    lines = [
        "---",
        f"description: {desc}",
        "type: moc",
        "---",
        "",
        f"# {title}",
        "",
    ]
    if orientation:
        lines.extend([orientation, ""])
    lines.extend(["## Entries (by priority)", ""])
    for leaf in leaves:
        lines.append(f"- [[{leaf['slug']}]] (p{leaf['priority']}) — {leaf['description']}")
    lines.append("")
    tensions = CATEGORY_TENSIONS.get(cat, [])
    if tensions:
        lines.extend(["## Tensions", ""])
        for t in tensions:
            lines.append(f"- {t}")
        lines.append("")
    return "\n".join(lines)


def plural(count: int, singular: str, many: str) -> str:
    return singular if count == 1 else many


def render_index(groups: dict[str, list[Leaf]]) -> str:
    total = len({leaf["slug"] for leaves in groups.values() for leaf in leaves})
    lines = [
        "---",
        "description: Entry point to the knowledge base. Start here to discover territories.",
        "type: moc",
        "---",
        "",
        "# Knowledge Base",
        "",
        f"{total} entries across three axes: task-related laws, language-specific rules, cross-cutting guides. Leaves declare priority (1=foundational, 5=niche), applies_when (task contexts), and categories (list).",
        "",
    ]
    for group_title, cats, group_orient in GROUP_ORDER:
        lines.append(f"## {group_title}")
        lines.append("")
        if group_orient:
            lines.extend([group_orient, ""])
        for cat in cats:
            if cat not in groups:
                continue
            count = len(groups[cat])
            _, cdesc, _ = CATEGORY_META.get(cat, (cat.capitalize(), "", ""))
            noun = plural(count, "entry", "entries")
            lines.append(f"- [[{cat}]] — {cdesc} ({count} {noun})")
        lines.append("")
    lines.extend([
        "## How to Use",
        "",
        "1. Pick 1-2 categories relevant to the current subtask",
        "2. Read those category MOCs — each lists leaves with descriptions and priority",
        "3. Pick 3-7 leaves by description + applies_when match",
        "4. Read leaf files fully",
        "5. Re-fetch as task shape shifts — knowledge is cheap to re-read",
        "",
    ])
    return "\n".join(lines)


def regenerate(knowledge_dir: pathlib.Path) -> None:
    reserved = {"index", *CATEGORY_META.keys()}
    leaves: list[Leaf] = []
    for path in sorted(knowledge_dir.glob("*.md")):
        if path.stem in reserved:
            continue
        leaf = parse_frontmatter(path)
        if leaf is None:
            print(f"WARN: no frontmatter in {path.name}", file=sys.stderr)
            continue
        leaves.append(leaf)
    print(f"Parsed {len(leaves)} leaves")
    groups = group_by_category(leaves)
    for cat, cat_leaves in groups.items():
        (knowledge_dir / f"{cat}.md").write_text(render_moc(cat, cat_leaves))
    (knowledge_dir / "index.md").write_text(render_index(groups))
    print(f"Wrote {len(groups)} category MOCs + index.md")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_kb = pathlib.Path(__file__).resolve().parent.parent / "knowledge"
    parser.add_argument("--knowledge-dir", type=pathlib.Path, default=default_kb)
    args = parser.parse_args()
    kb = args.knowledge_dir.resolve()
    if not kb.is_dir():
        print(f"FAIL: knowledge dir not found: {kb}", file=sys.stderr)
        return 1
    regenerate(kb)
    return 0


if __name__ == "__main__":
    sys.exit(main())
