---
name: brainstorming
description: Use when creating or developing, before writing code or implementation plans - refines rough ideas into fully-formed designs through collaborative questioning, alternative exploration, incremental validation, and engineering review handoff. Don't use during clear 'mechanical' processes
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.
After the design is validated, write a design doc that is ready for
`code-plan-eng-review`.

## Knowledge Base

Brainstorming is decision-heavy work — scope, alternatives, stop conditions. Use the **code knowledge base** at `~/.agents/knowledge/code/` to ground reasoning, following the same protocol as the `code` skill.

Entry points:
1. Read `~/.agents/knowledge/code/index.md` to discover territories.
2. Pick the MOCs that match the current brainstorm. Decide case by case; don't anchor on a default set.
3. Pick leaves by description + `applies_when`. Prefer priority 1 unless the task needs niche entries. Follow `related:` fields when adjacent leaves strengthen the reasoning.
4. Re-fetch as the brainstorm shape shifts — different phases (understanding, alternatives, design) often need different leaves.

Read each knowledge file via the `Read` tool — the PostToolUse hook auto-logs the fetch to `~/.agents/knowledge/code/.stats/fetches.jsonl`. Don't bypass with `cat`/`grep`; the stats only increment on `Read`.

If you traverse the KB during a brainstorm and no leaf covers the decision at hand, record the gap so `knowledge-reflect` can turn it into a new-leaf candidate — same convention as the `code` skill:

```bash
python3 ~/.agents/scripts/kb_gap.py --domain code --note "<what was missing, one line>" --task "<short brainstorm context>"
```

Record only genuine misses on substantive decisions, not when an adequate leaf exists.

### Audit trail (MANDATORY)

Before every Read of a knowledge file, emit one line with the `KB:` prefix stating WHAT and WHY in terms of THIS brainstorm. Same convention as the `code` skill.

Format:
- `KB: index.md — discovering territories`
- `KB: <moc>.md — <reason this MOC fits the current brainstorm>`
- `KB: <leaf>.md (pN) — <how it applies to this brainstorm decision>`

Rules:
- One line per Read, immediately before the tool call.
- Always include the priority tag for leaf files (not MOCs).
- Reason in terms of the current brainstorm, not the general topic of the entry.
- Only narrate Reads under `~/.agents/knowledge/code/` — not source code, project files, or design drafts.

## The Process

**Understanding the idea:**
- Check out the current project state first (files, docs, recent commits)
- Hit the KB before asking probing questions: read `index.md`, then pull whichever MOCs and leaves fit the task
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Re-fetch from the KB if the alternatives reach into new territories
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why — cite the leaves that shaped it by slug

**Presenting the design:**
- Once you believe you understand what you're building, present the tradeoffs of the design. Skip anything that is unambiguous and invariable.
- Break each tradeoff into 100-200 words. 
- Your job is to let the user guide the design by understanding the tradeoffs they will be making.
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Documentation:**
- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Do not commit the design doc or any generated plan files unless the user
  explicitly asks for a commit.
- Include an `## Engineering Review Handoff` section in the design doc. It
  should contain:
  - Questions for `code-plan-eng-review`
  - Known tradeoffs and alternatives rejected during brainstorming
  - Files, modules, commands, schemas, routes, or jobs likely to change
  - Existing code or flows that should be reused
  - Not-in-scope boundaries accepted during brainstorming
  - Expected validation commands and manual checks
  - Risk areas for architecture, tests, performance, failure modes, security,
    and rollout
- Treat this handoff as the input to engineering review; do not defer it to
  `code-generate-spec`.
- Use elements-of-style:writing-clearly-and-concisely skill if available

**Implementation (if continuing):**
- Ask: "Ready to run `code-plan-eng-review`?"

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
- **Ground reasoning in the KB** - Pull at least one leaf early; cite by slug when it shapes a recommendation so the user can audit the reasoning
