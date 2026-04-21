---
name: stacked-prs
description: Guide for creating and managing stacked pull requests using Graphite's gt CLI. Covers stacked diffs, gt create, gt submit, gt stack submit, gt stack sync, pull request workflow, PR review process, atomic commits, and branch dependencies. Use when working with stacks, multiple PRs, or Graphite workflow.
---

# Stacked Pull Requests with Graphite

## Purpose

This skill provides comprehensive guidance for creating and managing stacked pull requests (stacked diffs) using Graphite's `gt` CLI. It ensures PRs are atomic, logical, and easy to review by breaking large features into small, dependent changes.

## When to Use

Use this skill when:
- Creating stacked pull requests for a feature
- Breaking down large changes into reviewable chunks
- Managing dependencies between multiple PRs
- Submitting or syncing stacks with Graphite
- Following best practices for atomic commits and PR structure

## Core Principles

### 1. Atomic PRs
Each PR in a stack must be:
- **Atomic**: Represents a single, coherent change
- **Small**: Focused on one logical piece of functionality
- **Testable**: Passes CI independently
- **Reviewable**: Easy for reviewers to understand in isolation

### 2. Logical Dependencies
Structure stacks with clear dependency chains:
```
main → feature-step-1 → feature-step-2 → feature-step-3
```

Each branch builds on the previous one, creating a logical progression of changes.

## Workflow

### Step 1: Plan Your Stack Structure

**Before writing any code**, present the user with the structure of the stack you intend to submit and ask for confirmation before proceeding.

**Example:**
```
Stack Structure:
1. feature-add-user-model (main)
   - Add User model and database schema

2. feature-add-auth-endpoints (feature-add-user-model)
   - Add authentication endpoints that use User model

3. feature-add-auth-ui (feature-add-auth-endpoints)
   - Add UI components that call authentication endpoints
```

Ask: "Does this stack structure look good? Should I proceed with implementing these changes?"

### Step 2: Confirm Atomic and CI-Passing

**IMPORTANT**: The code in each PR of a stack must be:
- **Atomic**: Represents one logical change

Before committing any updates, confirm with the user that each PR will be atomic and pass CI.

### Step 3: Verify GitHub Actions Checks Pass Locally

**CRITICAL**: Before creating any commit with `gt create`, investigate and run the same checks that GitHub Actions will run on the PR.

**Process:**

1. **Find GitHub Actions workflows:**
   ```bash
   ls .github/workflows/
   ```

2. **Read workflow files to identify checks:**
   Look for jobs that run on `pull_request` events. Common checks include:
   - Linting/formatting
   - Type checking
   - Unit tests
   - Integration tests
   - Build/compilation
   - Security scans

3. **Extract the exact commands used in workflows:**
   Identify the `run:` commands in each job step.

4. **Run those commands locally:**
   Execute the same commands on your local machine to verify they pass.

5. After completing each step you MUST rerun the command to ensure the changes you made do not break any previous commands you ran.

**Example workflow analysis:**

```yaml
# .github/workflows/ci.yml
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

**Local verification:**
```bash
npm ci
npm run lint    # Must pass ✅
npm test        # Must pass ✅
npm run build   # Must pass ✅
```

**Quality Gate Rules:**
- ✅ All checks that run in GitHub Actions must pass locally
- ✅ If a workflow step fails locally, fix it before proceeding
- ✅ Only proceed to `gt create` once all checks pass

**Why this matters:**
- Prevents CI failures that block the entire stack
- Catches issues before they reach GitHub
- Saves time by avoiding failed PR checks
- Maintains code quality and reviewer confidence

### Step 3: Create Each Branch with gt

Use `gt create --no-interactive` instead of `git commit`:

```bash
# First PR in stack
gt create --no-interactive -m "Add User model and database schema"

# Second PR (automatically creates dependency on previous)
gt create --no-interactive -m "Add authentication endpoints"

# Third PR
gt create --no-interactive -m "Add authentication UI components"
```

**Why `gt create`?**
- Automatically creates a commit AND a branch
- Establishes proper branch dependencies
- Keeps stack structure organized

### Step 4: Submit Stack

Instead of `git push`, use `gt submit --no-interactive`:

```bash
gt submit --no-interactive
```

**What it does:**
- Submits the current branch and all downstack branches to Graphite
- Creates PRs if they don't exist
- Updates existing PRs if they do
- Non-interactive mode skips confirmation prompts

**Alternative - Submit Full Stack:**
```bash
gt stack submit --no-interactive
```
Submits all PRs in the entire stack at once.

### Step 5: Keep Stack in Sync

Use `gt stack sync --no-interactive` to keep your stack aligned with the base branch:

```bash
gt stack sync --no-interactive
```

**What it does:**
- Pulls latest changes from main/base branch
- Rebases your stack on top of latest
- Reduces merge conflicts
- Keeps PRs up to date

## Command Discovery

**IMPORTANT**: Instead of maintaining a static command reference, use `gt --help` to discover available commands dynamically:

```bash
# See all available gt commands
gt --help

# Get help for a specific command
gt create --help
gt submit --help
gt stack --help
```

### Essential Commands (Always use --no-interactive)

| Command | Purpose |
|---------|---------|
| `gt create --no-interactive` | Create commit + branch with automatic dependencies |
| `gt submit --no-interactive` | Submit current branch + downstack to Graphite |
| `gt stack submit --no-interactive` | Submit entire stack as PRs |
| `gt stack sync --no-interactive` | Sync stack with base branch |
| `gt branch create --no-interactive` | Create new branch with dependencies |
| `gt restack --no-interactive` | Reorganize stack structure |
| `gt log short` | Visualize stack dependencies |
| `gt stack` | View current stack structure |

**When in doubt**: Run `gt <command> --help` to see all available options and flags.

## Best Practices

### Do's ✅

- **Plan first**: Present stack structure before coding
- **Keep PRs small**: Each PR should be < 400 lines if possible
- **Atomic commits**: One logical change per PR
- **Pass CI**: Every PR must pass tests independently
- **Clear messages**: Use descriptive commit/PR titles
- **Use gt commands**: Prefer `gt create --no-interactive` over `git commit`
- **Sync regularly**: Run `gt stack sync --no-interactive` to stay current
- **Logical flow**: Each PR should build naturally on previous

### Don'ts ❌

- **Don't mix concerns**: Keep each PR focused on one thing
- **Don't skip CI**: Never submit PRs that fail tests
- **Don't use git push**: Use `gt submit --no-interactive` instead
- **Don't create giant PRs**: Break them into smaller chunks
- **Don't forget dependencies**: Ensure proper branch ordering
- **Don't commit without planning**: Get stack structure approved first

## Example Stack

Here's a real-world example of a well-structured stack:

```
Stack: Add User Authentication System

PR 1: feature-add-user-schema (→ main)
  - Add User table to database
  - Add Prisma schema definitions
  - Generate migrations
  Files: schema.prisma, migrations/

PR 2: feature-add-auth-service (→ feature-add-user-schema)
  - Add authentication service class
  - Add password hashing utilities
  - Add JWT token generation
  Files: src/services/auth.service.ts, src/utils/crypto.ts

PR 3: feature-add-auth-endpoints (→ feature-add-auth-service)
  - Add /login endpoint
  - Add /register endpoint
  - Add /logout endpoint
  Files: src/routes/auth.routes.ts, src/controllers/auth.controller.ts

PR 4: feature-add-auth-ui (→ feature-add-auth-endpoints)
  - Add login form component
  - Add registration form component
  - Add authentication context
  Files: src/components/LoginForm.tsx, src/components/RegisterForm.tsx
```

## Workflow Checklist

Before starting:
- [ ] Plan complete stack structure
- [ ] Present structure to user for approval
- [ ] Confirm each PR will be atomic
- [ ] Confirm each PR will pass CI
- [ ] Investigate `.github/workflows/` to identify CI checks

For each PR in stack:
- [ ] Make focused, logical changes
- [ ] Read GitHub Actions workflows for PR checks
- [ ] Extract commands from workflow `run:` steps
- [ ] Run all workflow commands locally
- [ ] Verify all checks pass (lint, test, build, etc.)
- [ ] Use `gt create --no-interactive -m "descriptive message"`
- [ ] Verify branch dependency is correct

After completing stack:
- [ ] Review full stack structure with `gt log short`
- [ ] Run `gt stack sync --no-interactive` to sync with base branch
- [ ] Use `gt submit --no-interactive` or `gt stack submit --no-interactive`
- [ ] Verify all PRs created successfully on GitHub

## Troubleshooting

### Stack structure incorrect
```bash
gt restack --no-interactive  # Reorganize stack
gt log short  # Visualize current structure
```

### Merge conflicts
```bash
gt stack sync --no-interactive  # Sync with base branch
# Resolve conflicts manually, then:
git add .
git rebase --continue
```

### Need to modify earlier PR in stack
```bash
# Check out the branch you want to modify
gt checkout feature-name

# Make changes
# ...

# Create amendment commit
gt create --no-interactive -m "Update feature-name"

# Restack dependent branches
gt restack --no-interactive
```

### PR dependencies wrong
```bash
# Use gt branch commands to restructure
gt branch checkout <branch-name>
gt branch rebase <new-parent-branch>
```

## Integration with CI/CD

Ensure your CI/CD pipeline:
- Runs tests on each PR independently
- Blocks merging if tests fail
- Supports stacked PR workflow (e.g., GitHub Actions with Graphite)
- Provides clear feedback on test failures

## Additional Resources

- Run `gt --help` for complete command reference
- [Graphite Documentation](https://graphite.dev/docs) - Official docs
- [Stacked Diffs Guide](https://graphite.com/guides/stacked-diffs) - Best practices

---

**Remember**: Always plan your stack structure first, confirm it's atomic and will pass CI, then execute. This prevents rework and ensures high-quality, reviewable PRs.
