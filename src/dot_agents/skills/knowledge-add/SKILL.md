---
name: knowledge-add
description: Add a new entry to the shared code or writing knowledge base, regenerate MOCs, and validate the corpus. Use when the user wants to teach the agent a new reusable rule, heuristic, law, workflow, or writing principle.
---

# Knowledge Add

Add a new entry to a domain-scoped knowledge base under
`~/.agents/knowledge/<domain>/`. Domains:

- `code`: software-engineering laws, language rules, workflow guides.
- `write`: prose craft, tone, voice, composition, and format rules.

The first argument must be the domain: `code` or `write`. If missing or invalid,
ask which KB the entry belongs to.

Let `<DOMAIN>` be the parsed domain and `<KB>` be
`~/.agents/knowledge/<DOMAIN>`.

## Schema

```yaml
---
slug: <kebab-case-slug>
categories: [<cat1>, <cat2>]
priority: 1
description: <one sentence>
applies_when:
  - <2-4 task-context phrases>
related: [<other-slugs>]
source: <url>
---
```

## Flow

1. Read `<KB>/index.md` to see existing categories and style.
2. Inspect 2-3 adjacent leaves in the likely category to match voice and density.
3. Synthesize the entry:
   - Choose a kebab-case slug and confirm `<KB>/<slug>.md` does not exist.
   - Choose 1-3 categories from the domain's existing category set.
   - Assign honest priority; default to 3 if unsure.
   - Write `description` as an applicability-forward sentence.
   - Write 2-4 `applies_when` phrases.
   - Populate `related` with same-domain slugs or `[]`.
4. Show the draft before writing.
5. On approval, write `<KB>/<slug>.md`.
6. Run `python3 ~/.agents/scripts/gen_mocs.py --knowledge-dir <KB>`.
7. Run `python3 ~/.agents/scripts/validate_kb.py --knowledge-dir <KB>`.
8. Fix any validation errors.
9. Ask about contribution scope. Steps 5-6 only wrote to `~/.agents/` on this
   machine; the chezmoi source of truth is the `dotagents` repo, and nothing
   reaches other machines until it lands there. Ask whether the entry is:
   - Universal (default) — belongs on every machine → contribute it back.
   - Machine-specific — only relevant here (e.g. work-laptop specifics) →
     leave it in `~/.agents/` only and skip to step 10.

   If universal, sync into the chezmoi source and push. Touched files are the new
   leaf plus every regenerated MOC (`index.md` always; each mapped category MOC —
   check `git status` if unsure):
   ```bash
   CFG=--config=$HOME/.config/chezmoi/dotagents.toml
   chezmoi $CFG add ~/.agents/knowledge/<DOMAIN>/<slug>.md
   chezmoi $CFG re-add ~/.agents/knowledge/<DOMAIN>/index.md ~/.agents/knowledge/<DOMAIN>/<touched-category-MOCs>
   REPO=$(git -C "$(chezmoi $CFG source-path)" rev-parse --show-toplevel)
   git -C "$REPO" add src/dot_agents/knowledge/<DOMAIN>/
   git -C "$REPO" commit -m "Add <slug> knowledge leaf (<DOMAIN>)"
   git -C "$REPO" push
   ```
   Use `re-add` (not `apply`) so the regenerated MOCs flow home → source, not the
   reverse.
10. Report the final file path, touched MOCs, and the contribution scope chosen
    (universal + pushed, or machine-local).

## Rules

- Never overwrite an existing file silently.
- Never invent categories without asking; adding a category requires updating
  `~/.agents/scripts/gen_mocs.py` and validator expectations.
- Never cross domains.
- Keep leaves dense: usually 150-300 words.
