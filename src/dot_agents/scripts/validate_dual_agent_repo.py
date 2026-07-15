#!/usr/bin/env python3
"""Validate that this chezmoi source supports both Claude and Codex."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
SHARED = SRC / "dot_agents"
CLAUDE = SRC / "dot_claude"
CODEX = SRC / "dot_codex"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def require(path: Path) -> None:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_required_paths() -> None:
    for path in [
        ROOT / "CLAUDE.md",
        ROOT / "AGENTS.md",
        SHARED / "skills",
        SHARED / "knowledge",
        SHARED / "scripts",
        CLAUDE / "CLAUDE.md",
        CLAUDE / "settings.json.tmpl",
        CLAUDE / "symlink_skills",
        CLAUDE / "symlink_knowledge",
        CLAUDE / "symlink_scripts",
        CODEX / "AGENTS.md",
        CODEX / "private_config.toml",
        CODEX / "hooks.json.tmpl",
    ]:
        require(path)


def validate_symlink_sources() -> None:
    expected = {
        CLAUDE / "symlink_skills": "../.agents/skills",
        CLAUDE / "symlink_knowledge": "../.agents/knowledge",
        CLAUDE / "symlink_scripts": "../.agents/scripts",
    }
    for path, target in expected.items():
        actual = read(path).strip()
        if actual != target:
            fail(f"{path.relative_to(ROOT)} points to {actual!r}, expected {target!r}")


def validate_skill_frontmatter() -> None:
    for skill in sorted((SHARED / "skills").iterdir()):
        if not skill.is_dir():
            continue
        skill_md = skill / "SKILL.md"
        require(skill_md)
        text = read(skill_md)
        if not text.startswith("---\n"):
            fail(f"{skill_md.relative_to(ROOT)} missing YAML frontmatter")
        if not re.search(r"^name:\s*.+$", text, re.M):
            fail(f"{skill_md.relative_to(ROOT)} missing name")
        if not re.search(r"^description:\s*.+$", text, re.M):
            fail(f"{skill_md.relative_to(ROOT)} missing description")


def validate_command_skill_parity() -> None:
    commands = {path.stem for path in (CLAUDE / "commands").glob("*.md")}
    skills = {path.name for path in (SHARED / "skills").iterdir() if path.is_dir()}
    missing = sorted(commands - skills)
    if missing:
        fail(
            "Claude commands without matching shared Codex-visible skills: "
            + ", ".join(missing)
        )


def validate_no_stale_shared_paths() -> None:
    stale_patterns = [
        "~/.claude/knowledge",
        "~/.claude/scripts",
        "src/dot_claude/knowledge",
        "src/dot_claude/scripts",
    ]
    for path in sorted(SHARED.rglob("*")):
        if not path.is_file():
            continue
        if path == Path(__file__).resolve():
            continue
        try:
            text = read(path)
        except UnicodeDecodeError:
            continue
        for pattern in stale_patterns:
            if pattern in text:
                fail(f"{path.relative_to(ROOT)} contains stale shared path {pattern}")


def validate_root_instruction_contract() -> None:
    marker = "## Dual-Agent Contract"
    sections: dict[str, str] = {}
    for path in [ROOT / "CLAUDE.md", ROOT / "AGENTS.md"]:
        text = read(path)
        if marker not in text:
            fail(f"{path.name} missing {marker}")
        after_marker = text.split(marker, 1)[1]
        section_body = after_marker.split("\n## ", 1)[0].strip()
        sections[path.name] = section_body
    if sections["CLAUDE.md"] != sections["AGENTS.md"]:
        fail("CLAUDE.md and AGENTS.md Dual-Agent Contract sections differ")


def validate_global_instruction_parity() -> None:
    claude_path = CLAUDE / "CLAUDE.md"
    codex_path = CODEX / "AGENTS.md"
    if read(claude_path) != read(codex_path):
        fail(
            f"{claude_path.relative_to(ROOT)} and {codex_path.relative_to(ROOT)} "
            "must be byte-identical"
        )


def main() -> int:
    validate_required_paths()
    validate_symlink_sources()
    validate_skill_frontmatter()
    validate_command_skill_parity()
    validate_no_stale_shared_paths()
    validate_root_instruction_contract()
    validate_global_instruction_parity()
    print("dual-agent repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
