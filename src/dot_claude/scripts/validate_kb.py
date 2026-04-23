#!/usr/bin/env python3
"""Static validation of the knowledge/ structure.

Default knowledge dir is `../knowledge` relative to this script. Override with
`--knowledge-dir <path>` when running outside the standard layout.

Exits 0 on pass, 1 on any errors. Warnings do not fail the run.
"""
import argparse
import pathlib
import re
import sys
from typing import TypedDict


class Entry(TypedDict):
    path: pathlib.Path
    slug: str
    categories: list[str]
    priority: int
    description: str
    applies_when: list[str]
    related: list[str]
    is_moc: bool


CATEGORY_MOCS = {
    "architecture", "design", "teams", "planning", "quality", "scale", "decisions",
    "python", "rust", "java", "elixir", "frontend",
    "testing", "prs", "style", "communication",
    "ux",
}


def parse_file(path: pathlib.Path) -> Entry | None:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = m.group(1)

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
            return [line.removeprefix("  - ").strip() for line in block.group(1).splitlines() if line.strip()]
        return []

    is_moc = scalar("type") == "moc"
    priority_raw = scalar("priority")
    priority = int(priority_raw) if priority_raw.isdigit() else 0
    return Entry(
        path=path,
        slug=scalar("slug"),
        categories=list_field("categories"),
        priority=priority,
        description=scalar("description"),
        applies_when=list_field("applies_when"),
        related=list_field("related"),
        is_moc=is_moc,
    )


def extract_wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", text)


def validate(knowledge_dir: pathlib.Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    files = sorted(knowledge_dir.glob("*.md"))
    if not files:
        print(f"FAIL: no files in {knowledge_dir}", file=sys.stderr)
        return 1

    entries: dict[str, Entry] = {}
    for path in files:
        parsed = parse_file(path)
        if parsed is None:
            errors.append(f"{path.name}: no frontmatter")
            continue
        stem = path.stem
        if stem != "index" and stem not in CATEGORY_MOCS and parsed["slug"] != stem:
            errors.append(f"{path.name}: slug '{parsed['slug']}' does not match filename stem '{stem}'")
        entries[stem] = parsed

    if "index" not in entries:
        errors.append("index.md: missing top-level MOC")

    for cat in CATEGORY_MOCS:
        if cat not in entries:
            errors.append(f"{cat}.md: category MOC missing")

    declared_categories: set[str] = set()
    for stem, entry in entries.items():
        if entry["is_moc"]:
            continue
        declared_categories.update(entry["categories"])
        for cat in entry["categories"]:
            if cat not in CATEGORY_MOCS:
                errors.append(f"{stem}.md: declares unknown category '{cat}'")
        for rel in entry["related"]:
            if rel not in entries:
                warnings.append(f"{stem}.md: related '[[{rel}]]' has no matching file")
        if entry["priority"] < 1 or entry["priority"] > 5:
            errors.append(f"{stem}.md: priority {entry['priority']} out of range 1-5")
        if not entry["description"]:
            errors.append(f"{stem}.md: empty description")
        if not entry["applies_when"]:
            warnings.append(f"{stem}.md: empty applies_when")

    extra_cats = CATEGORY_MOCS - declared_categories
    if extra_cats:
        warnings.append(f"MOCs with no leaves declaring them: {sorted(extra_cats)}")

    for stem, entry in entries.items():
        if not entry["is_moc"]:
            continue
        text = entry["path"].read_text()
        for target in extract_wikilinks(text):
            if target not in entries:
                errors.append(f"{stem}.md: wiki-link '[[{target}]]' has no matching file")

    total_leaves = sum(1 for e in entries.values() if not e["is_moc"])
    total_mocs = sum(1 for e in entries.values() if e["is_moc"])
    print(f"Parsed {len(entries)} files ({total_leaves} leaves, {total_mocs} MOCs)")

    if warnings:
        print(f"\n{len(warnings)} WARNINGS:")
        for w in warnings:
            print(f"  WARN: {w}")

    if errors:
        print(f"\n{len(errors)} ERRORS:", file=sys.stderr)
        for e in errors:
            print(f"  FAIL: {e}", file=sys.stderr)
        return 1

    print("\nOK: all checks passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_kb = pathlib.Path(__file__).resolve().parent.parent / "knowledge"
    parser.add_argument("--knowledge-dir", type=pathlib.Path, default=default_kb)
    args = parser.parse_args()
    kb = args.knowledge_dir.resolve()
    if not kb.is_dir():
        print(f"FAIL: knowledge dir not found: {kb}", file=sys.stderr)
        return 1
    return validate(kb)


if __name__ == "__main__":
    sys.exit(main())
