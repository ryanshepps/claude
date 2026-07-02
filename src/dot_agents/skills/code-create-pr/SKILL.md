---
name: code-create-pr
description: |
  Prepare implemented code for review and create a pull request. Use after
  code-implement-spec or code when the user asks to create a PR, ship a branch,
  push changes for review, open a pull request, or finish a feature branch.
  Discovers the default branch, syncs against its latest state, finds and runs
  the repository's local checks, commits with local conventions, pushes, and
  opens a concise issue-linked PR.
---

# Code Create PR

Create a review-ready PR from completed implementation work. This is the
portable release loop: sync base, verify locally, commit cleanly, push, and open
the PR with a concise project-focused body.

## Guardrails

- Do not create a PR from the default branch. If the current branch is the
  default branch, stop and create or ask for a feature branch name.
- Never include testing instructions, command transcripts, agent attribution, or
  checklist evidence in the PR body.
- Stage only intentional files. Inspect untracked files and unrelated local
  changes before staging.
- If checks fail because of this branch, fix them and rerun. If failures appear
  pre-existing, prove that against the latest default branch before proceeding.
- Do not invent release metadata. Only update version files, changelogs, or
  release notes when this repository already requires that for normal PRs.

## Workflow

### 1. Identify Platform And Base

1. Confirm the git root and current branch:
   - `git rev-parse --show-toplevel`
   - `git branch --show-current`
   - `git status --short`
2. Determine the default branch, preferring hosted metadata when available:
   - GitHub: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`
   - GitLab: `glab repo view --output json` if available
   - Git fallback: `git remote show origin` or
     `git symbolic-ref refs/remotes/origin/HEAD`
3. Fetch the latest default branch:
   - `git fetch origin <default-branch>`
4. Integrate the latest default branch into the feature branch before checks:
   - Prefer the repository's established branch-update convention if obvious.
   - Otherwise use a normal merge:
     `git merge --no-edit origin/<default-branch>`
   - If conflicts are non-trivial, stop and report the conflicted files.

Use the detected default branch as the PR base.

### 2. Discover Local Checks

Find the repository's own validation commands before running anything:

1. Read project instructions and common docs:
   - `AGENTS.md`, `CLAUDE.md`, `README*`, `CONTRIBUTING*`, `docs/*`
2. Inspect CI and task runners:
   - `.github/workflows/*`, `.gitlab-ci.yml`, `Makefile`, `Justfile`,
     `Taskfile.yml`, `mise.toml`, `.pre-commit-config.yaml`
3. Inspect language manifests and scripts:
   - Node: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`
   - Python: `pyproject.toml`, `tox.ini`, `noxfile.py`, `pytest.ini`
   - Rust: `Cargo.toml`
   - Go: `go.mod`
   - Java/Kotlin: `build.gradle*`, `pom.xml`, `gradlew`, `mvnw`
   - Ruby: `Gemfile`, `.rspec`, `Rakefile`
   - .NET: `*.sln`, `*.csproj`
4. Search command names and docs for general check language:
   - `test`, `tests`, `lint`, `format`, `fmt`, `prettier`, `typecheck`,
     `type-check`, `compile`, `build`, `check`, `verify`, `ci`

Select the broadest practical local commands that cover tests, linting,
formatting, type checking, compiling, and building. Prefer documented aggregate
commands such as `make test`, `make check`, `pnpm test`, `cargo test`,
`go test ./...`, `pytest`, `gradle test`, or `mvn test` over invented command
combinations.

### 3. Run Checks

Run all selected checks locally.

- Run independent checks in parallel when that is safe.
- If a formatter command writes changes, inspect and include only intentional
  formatting output, then rerun the affected checks.
- If a command needs dependencies or a service that is not available, try the
  repository's documented setup path. If it still cannot run, stop and report the
  exact blocker.
- After code changes made to fix check failures, rerun the relevant failed
  command and the broadest final validation command.

Do not proceed to commit and PR creation until local verification is green or a
pre-existing failure has been demonstrated against the latest default branch.

### 4. Commit Changes

1. Review the diff:
   - `git diff --stat`
   - `git diff`
   - `git status --short`
2. Review recent commit conventions:
   - `git log --oneline --decorate -n 30`
   - `git log origin/<default-branch> --oneline -n 30`
3. Infer message style from history:
   - Conventional commits: `feat(scope): ...`, `fix: ...`, `chore: ...`
   - Verb-first subjects: `Add ...`, `Fix ...`, `Update ...`
   - Repository-specific prefixes or ticket IDs
4. Stage only intentional files.
5. Create one or more logical commits. Small cohesive changes can be one commit;
   split unrelated or dependency-ordered changes into separate commits.

If there are no uncommitted changes because the implementation was already
committed, do not create an empty commit. Continue with the existing commits.

### 5. Prepare PR Metadata

Determine the PR title convention before creating the PR:

1. Inspect recent default-branch commits for squash-merge shape:
   - Recent commits ending in `(#123)` usually mirror squashed PR titles.
   - Merge commits like `Merge pull request #123...` mean PR titles may differ
     from commit subjects.
2. If `gh` is available, inspect recent merged PR titles:
   - `gh pr list --state merged --limit 20 --json title,number,mergeCommit`
3. Use the dominant convention:
   - If squashed PRs dominate, make the PR title match recent squashed PR
     titles.
   - If conventional commits dominate, use a conventional PR title.
   - If verb-first titles dominate, start with the same kind of verb.
4. Identify issue references:
   - Look in the branch name, commit messages, implementation plan, TODOs, and
     local issue tracker metadata.
   - GitHub issues: use `Closes #123` when this PR completes the issue, or
     `Refs #123` when it only relates.
   - Linear-style keys: use the repository's observed convention such as
     `Closes ABC-123`, `Fixes ABC-123`, or `Refs ABC-123`.
   - If an issue likely exists but the closing relationship is unclear, ask
     before using a closing keyword.

### 6. Push And Create The PR

1. Push the branch:
   - `git push -u origin <branch>` if no upstream exists.
   - `git push` if upstream is already configured.
2. Create or update the PR:
   - If an open PR already exists for this branch, update its title/body instead
     of creating a duplicate.
   - GitHub: `gh pr create --base <default-branch> --title "<title>" --body
     "<body>"`
   - GitLab: `glab mr create -b <default-branch> -t "<title>" -d "<body>"`
3. Keep the PR body short. Do not add section headings by default. Most PRs
   need only a sentence or a few bullets covering what changed and why,
   followed by the issue line:

   ```markdown
   - <what changed>
   - <why this change was needed>

   Closes <issue-id>
   ```

   Add a `## Summary` heading (and other headings) only when the body is long
   enough that a reader benefits from structure — for example a large change
   with several distinct parts that each need their own labeled section:

   ```markdown
   ## Summary
   <one or two sentences framing the change>

   ## <Area or component>
   - <what changed here and why>

   ## <Another area>
   - <what changed here and why>

   Closes <issue-id>
   ```

   Omit the issue line when no issue applies. Do not add a testing section.

### 7. Monitor PR Readiness

After the PR exists, verify that it is mergeable and that hosted CI passes when
the repository has CI configured.

1. Detect whether hosted CI exists:
   - Repository files: `.github/workflows/*`, `.gitlab-ci.yml`,
     `.circleci/config.yml`, `azure-pipelines.yml`, `buildkite.yml`,
     `.buildkite/*`, `.drone.yml`
   - Platform checks: GitHub status checks, GitLab pipelines, or the repository's
     documented PR checks.
2. Check PR mergeability:
   - GitHub: inspect `gh pr view --json mergeable,mergeStateStatus`
   - GitLab: inspect `glab mr view` merge status or equivalent JSON output when
     available.
3. If the PR has merge conflicts or is behind the base branch:
   - Fetch the latest base: `git fetch origin <default-branch>`
   - Integrate the base using the repository's established convention, otherwise
     `git merge --no-edit origin/<default-branch>`.
   - Resolve conflicts in the working tree. Prefer the implementation intent and
     current base-branch APIs; do not blindly choose one side.
   - Rerun the local checks affected by the conflict and the broadest final
     validation command.
   - Commit the conflict-resolution/update changes using the repository's commit
     convention and push the branch.
   - Re-check PR mergeability after the push.
4. If CI exists, wait for it:
   - GitHub: prefer `gh pr checks --watch` when available. If checks are still
     queued or pending, continue monitoring until they pass, fail, or time out.
   - GitLab: monitor the MR pipeline with `glab pipeline ci view`, `glab mr
     view`, or the repository's documented command.
5. If CI fails:
   - Inspect the failing job logs.
   - If the failure is caused by this branch, fix it, rerun local checks, commit,
     push, and monitor CI again.
   - If the failure is clearly pre-existing or infrastructure-related, capture
     the evidence and report it as an unresolved caveat instead of masking it in
     the PR body.
6. If no hosted CI exists, skip CI monitoring after local checks pass.

Do not change the PR body just to add CI or testing details.

### 8. After Creation

After the PR is created and readiness monitoring is complete, report:

- PR URL
- Base branch and feature branch
- Local checks that passed
- CI status when CI exists
- Any unresolved caveats, only if present

If the repository or agent environment has existing post-PR review skills or
checks, run them after the PR exists. When `code-review-pr` and
`code-production-readiness` are available, invoke both for the new PR unless the
user explicitly asked only to open the PR.
