---
name: skill-developer
description: Create and manage Claude Code skills following Anthropic best practices. Use when creating new skills, structuring skill content, implementing progressive disclosure, writing YAML frontmatter, or applying the 500-line rule. Covers skill structure, naming conventions, reference files, and content organization.
---

# Skill Developer Guide

## Purpose

Comprehensive guide for creating and managing skills in Claude Code, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern.

## When to Use This Skill

Use when you're:
- Creating or adding new skills
- Structuring skill content and reference files
- Writing YAML frontmatter for skills
- Applying the 500-line rule and progressive disclosure
- Organizing skills by feature/domain

---

## Quick Start: Creating a New Skill

### Step 1: Create Skill File

**Location:** `.claude/skills/{skill-name}/SKILL.md`

**Template:**
```markdown
---
name: my-new-skill
description: Brief description including keywords that help Claude match this skill to relevant tasks. Mention topics, file types, and use cases. Be explicit about what this skill covers.
---

# My New Skill

## Purpose
What this skill helps with

## When to Use
Specific scenarios and conditions

## Key Information
The actual guidance, documentation, patterns, examples
```

### Step 2: Follow Best Practices

- **Name**: Lowercase, hyphens, gerund form (verb + -ing) preferred (e.g., "processing-pdfs")
- **Description**: Include all relevant keywords/phrases (max 1024 chars). This is how Claude matches skills to tasks.
- **Content**: Under 500 lines - use reference files for details
- **Examples**: Include real code examples
- **Structure**: Clear headings, lists, code blocks

### Step 3: Add Reference Files (If Needed)

If your skill content exceeds 500 lines, split into reference files:

```
.claude/skills/my-skill/
  SKILL.md           # Main file (under 500 lines)
  REFERENCE_A.md     # Detailed topic A
  REFERENCE_B.md     # Detailed topic B
```

Link from SKILL.md to reference files so Claude can follow them when needed.

### Step 4: Test with Real Scenarios

Before considering a skill complete:
- Test with 3+ real prompts that should activate the skill
- Verify the guidance is actionable and correct
- Iterate based on actual usage

---

## Skill Structure Best Practices

### The 500-Line Rule

Keep SKILL.md under 500 lines. This is critical for:
- Keeping context window usage manageable
- Forcing concise, actionable content
- Encouraging progressive disclosure

### Progressive Disclosure

Structure information in layers:
1. **SKILL.md** - Core guidance, most important patterns, quick reference
2. **Reference files** - Deep dives, complete examples, edge cases

### Description Field

The `description` in YAML frontmatter is how Claude decides whether a skill is relevant. Write it to maximize discoverability:

```yaml
# WRONG: Too vague
description: Helps with database stuff

# CORRECT: Specific keywords and use cases
description: Guide for Prisma database operations including schema design, migrations, query optimization, relation modeling, and error handling. Use when working with database models, writing queries, or modifying the Prisma schema.
```

### Naming Conventions

- Use lowercase with hyphens: `my-skill-name`
- Prefer gerund form: `processing-pdfs`, `managing-state`, `writing-tests`
- Be descriptive but concise

### Content Guidelines

**Do:**
- Lead with the most important information
- Use code examples from the actual codebase when possible
- Include "When to Use" and "When NOT to Use" sections
- Provide checklists for complex processes
- Keep guidance actionable

**Don't:**
- Repeat information available in other skills
- Include implementation details that change frequently
- Write walls of text without structure
- Add content "just in case" - only include what's needed

---

## Skill Types

### Guardrail Skills

**Purpose:** Enforce critical best practices that prevent errors

**Characteristics:**
- Prevent common mistakes (wrong column names, critical errors)
- Short, focused content
- Clear "do this, not that" guidance

**When to Use:**
- Mistakes that cause runtime errors
- Data integrity concerns
- Critical compatibility issues

### Domain Skills

**Purpose:** Provide comprehensive guidance for specific areas

**Characteristics:**
- Topic or domain-specific
- Comprehensive documentation
- May use reference files for depth

**When to Use:**
- Complex systems requiring deep knowledge
- Best practices documentation
- Architectural patterns
- How-to guides

---

## Testing Checklist

When creating a new skill, verify:

- [ ] Skill file created in `.claude/skills/{name}/SKILL.md`
- [ ] Proper frontmatter with name and description
- [ ] Description includes relevant keywords for discoverability
- [ ] Content is actionable and correct
- [ ] Real code examples included
- [ ] **SKILL.md under 500 lines**
- [ ] Reference files created if needed
- [ ] Table of contents added to reference files > 100 lines
- [ ] Tested with 3+ real scenarios

---

## Reference Files

### [ADVANCED.md](ADVANCED.md)
Future enhancement ideas:
- Skill dependencies
- Skill versioning
- Multi-language support

---

## Quick Reference Summary

### Create New Skill (4 Steps)

1. Create `.claude/skills/{name}/SKILL.md` with frontmatter
2. Write concise, actionable content
3. Add reference files if over 500 lines
4. Test with real scenarios

### Anthropic Best Practices

- **500-line rule**: Keep SKILL.md under 500 lines
- **Progressive disclosure**: Use reference files for details
- **Table of contents**: Add to reference files > 100 lines
- **One level deep**: Don't nest references deeply
- **Rich descriptions**: Include all relevant keywords (max 1024 chars)
- **Test first**: Build 3+ evaluations before extensive documentation
- **Gerund naming**: Prefer verb + -ing (e.g., "processing-pdfs")

---

## Related Files

**All Skills:**
- `.claude/skills/*/SKILL.md` - Skill content files
