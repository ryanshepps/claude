#!/usr/bin/env python3
"""Regenerate category MOCs and index.md from leaf frontmatter.

Domain auto-detected from `--knowledge-dir` basename: must be `code` or `write`.
Each domain has its own CATEGORY_META, GROUP_ORDER, and TENSIONS.

Default knowledge dir is `../knowledge/code` relative to this script. Override
with `--knowledge-dir <path>` when running outside the standard layout.
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


CategoryMeta = dict[str, tuple[str, str, str]]
Tensions = dict[str, list[str]]
GroupOrder = list[tuple[str, list[str], str]]


class DomainCfg(TypedDict):
    meta: CategoryMeta
    tensions: Tensions
    group_order: GroupOrder


# ---------------------------------------------------------------------------
# Per-domain configuration
# ---------------------------------------------------------------------------

CODE_CATEGORY_META: CategoryMeta = {
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

CODE_CATEGORY_TENSIONS: Tensions = {
    "quality": [
        "**Boy-scout rule** vs **surgical changes** — opportunistic cleanup improves code health, but uninvited refactors bloat diff scope. Apply boy-scout for trivial single-line fixes adjacent to your task; stay surgical when reviewers need a tight, focused diff.",
    ],
}

CODE_GROUP_ORDER: GroupOrder = [
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


WRITE_CATEGORY_META: CategoryMeta = {
    "tone": (
        "Tone",
        "Voice, register, persona, and brand consistency rules.",
        "How a piece sounds — voice, register, persona. Use when matching a brand, calibrating formality, or checking that drafts read like the author intends.",
    ),
    "structure": (
        "Structure",
        "Composition: openings, transitions, evidence, narrative arc.",
        "How a piece is built — openings that earn attention, transitions that carry weight, evidence that lands. Use when outlining, drafting long-form, or fixing a piece that wanders.",
    ),
    "format": (
        "Format",
        "Genre rules per surface: blog, email, PR comment, slack, doc.",
        "Surface-specific rules — what works in a blog post fails in an email. Use when picking conventions for the channel: length, headers, salutations, sign-offs.",
    ),
}

WRITE_CATEGORY_TENSIONS: Tensions = {}

WRITE_GROUP_ORDER: GroupOrder = [
    (
        "Composition",
        ["tone", "structure", "format"],
        "Craft rules grouped by the dimension they shape: how it sounds, how it's built, where it lives.",
    ),
]


DOMAIN_CONFIG: dict[str, DomainCfg] = {
    "code": DomainCfg(
        meta=CODE_CATEGORY_META,
        tensions=CODE_CATEGORY_TENSIONS,
        group_order=CODE_GROUP_ORDER,
    ),
    "write": DomainCfg(
        meta=WRITE_CATEGORY_META,
        tensions=WRITE_CATEGORY_TENSIONS,
        group_order=WRITE_GROUP_ORDER,
    ),
}


# ---------------------------------------------------------------------------
# Parsing + rendering
# ---------------------------------------------------------------------------


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


def render_moc(cat: str, leaves: list[Leaf], meta: CategoryMeta, tensions: Tensions) -> str:
    title, desc, orientation = meta.get(cat, (cat.capitalize(), f"{cat} entries", ""))
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
    cat_tensions = tensions.get(cat, [])
    if cat_tensions:
        lines.extend(["## Tensions", ""])
        for t in cat_tensions:
            lines.append(f"- {t}")
        lines.append("")
    return "\n".join(lines)


def plural(count: int, singular: str, many: str) -> str:
    return singular if count == 1 else many


def render_index(groups: dict[str, list[Leaf]], meta: CategoryMeta, group_order: GroupOrder, domain: str) -> str:
    total = len({leaf["slug"] for leaves in groups.values() for leaf in leaves})
    domain_blurb = {
        "code": "Software-engineering laws, language rules, and cross-cutting craft guides. Leaves declare priority (1=foundational, 5=niche), applies_when (task contexts), and categories (list).",
        "write": "Prose craft: tone, structure, format. Leaves declare priority (1=foundational, 5=niche), applies_when (writing contexts), and categories (list).",
    }.get(domain, "Knowledge base.")
    lines = [
        "---",
        "description: Entry point to the knowledge base. Start here to discover territories.",
        "type: moc",
        "---",
        "",
        f"# Knowledge Base — {domain}",
        "",
        f"{total} entries. {domain_blurb}",
        "",
    ]
    for group_title, cats, group_orient in group_order:
        lines.append(f"## {group_title}")
        lines.append("")
        if group_orient:
            lines.extend([group_orient, ""])
        for cat in cats:
            if cat not in groups:
                continue
            count = len(groups[cat])
            _, cdesc, _ = meta.get(cat, (cat.capitalize(), "", ""))
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


def regenerate(knowledge_dir: pathlib.Path, domain: str) -> None:
    cfg = DOMAIN_CONFIG[domain]
    meta = cfg["meta"]
    tensions = cfg["tensions"]
    group_order = cfg["group_order"]
    reserved = {"index", *meta.keys()}
    leaves: list[Leaf] = []
    for path in sorted(knowledge_dir.glob("*.md")):
        if path.stem in reserved:
            continue
        leaf = parse_frontmatter(path)
        if leaf is None:
            print(f"WARN: no frontmatter in {path.name}", file=sys.stderr)
            continue
        leaves.append(leaf)
    print(f"[{domain}] Parsed {len(leaves)} leaves")
    groups = group_by_category(leaves)
    for cat, cat_leaves in groups.items():
        (knowledge_dir / f"{cat}.md").write_text(render_moc(cat, cat_leaves, meta, tensions))
    (knowledge_dir / "index.md").write_text(render_index(groups, meta, group_order, domain))
    print(f"[{domain}] Wrote {len(groups)} category MOCs + index.md")


def detect_domain(knowledge_dir: pathlib.Path) -> str:
    name = knowledge_dir.name
    if name not in DOMAIN_CONFIG:
        print(
            f"FAIL: knowledge-dir basename must be one of {sorted(DOMAIN_CONFIG)}; got '{name}' from {knowledge_dir}",
            file=sys.stderr,
        )
        sys.exit(1)
    return name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_kb = pathlib.Path(__file__).resolve().parent.parent / "knowledge" / "code"
    parser.add_argument("--knowledge-dir", type=pathlib.Path, default=default_kb)
    args = parser.parse_args()
    kb = args.knowledge_dir.resolve()
    if not kb.is_dir():
        print(f"FAIL: knowledge dir not found: {kb}", file=sys.stderr)
        return 1
    domain = detect_domain(kb)
    regenerate(kb, domain)
    return 0


if __name__ == "__main__":
    sys.exit(main())
