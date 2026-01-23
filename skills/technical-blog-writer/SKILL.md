---
name: technical-blog-writer
description: Write technical blog posts with deep research. Use for writing blog posts, technical articles, dev tutorials, how-to guides. Takes topics, researches thoroughly, produces polished posts with clear structure.
---

# Technical Blog Writer

## Overview

Research and write polished technical blog posts. Takes a topic, conducts deep research using web search and codebase exploration, then produces a well-structured article following technical writing best practices.

## The Process

**1. Clarify the Topic**
- Ask the user: "What topic should I write about? Who is the target audience (beginner/intermediate/advanced developers)?"
- Get any specific angle, constraints, or key points to cover
- Ask about desired length (short: 800-1200 words, medium: 1500-2500 words, long: 3000+ words)

**2. Deep Research**
- Use WebSearch to find current information, best practices, and expert perspectives
- If the topic relates to the current codebase, use Task agent with subagent_type=Explore to understand relevant code
- Gather 3-5 authoritative sources
- Note key insights, statistics, and quotable points

**3. Build an Outline**
- Present a structured outline to the user for approval:
  - Hook/Introduction (problem statement or compelling question)
  - Prerequisites (if tutorial-style)
  - Main sections (3-5 major points)
  - Conclusion with call-to-action
- Get feedback before writing

**4. Write the Draft**
- Follow the writing principles below
- Include code snippets where appropriate (with explanations)
- Add visual breaks (headers, lists, code blocks)
- Cite sources naturally in the text

**5. Review and Polish**
- Self-edit for clarity, conciseness, and flow
- Ensure no jargon without explanation
- Verify code snippets are accurate
- Suggest a compelling title and subtitle

**6. Save the Post**
- Write to `./<topic-slug>-blog-post.md` in root directory
- Include a "Sources" section at the end with links

## Writing Principles

**Know Your Audience**
- Define one target reader (not everyone)
- Declare prerequisites upfront
- Match technical depth to audience level

**Hook Early**
- First paragraph decides if reader stays
- Start with context, then state what they'll learn
- Make the value proposition clear

**Clarity Over Cleverness**
- Use simple, direct language
- One idea per paragraph
- Short sentences and paragraphs
- Active voice ("the function returns" not "is returned by")

**Structure for Scanning**
- Clear headings and subheadings
- Bullet points for lists of 3+ items
- Code blocks with syntax highlighting
- Bold key terms on first use

**Code Snippets**
- Explain what the code does before showing it
- Call out important lines
- Keep snippets focused (not entire files)
- Provide a working example repo link if applicable

**Avoid Time-Sensitive Traps**
- Don't reference specific version numbers unless essential
- Avoid phrases like "recently" or "this year"
- Focus on concepts that remain relevant

**End Strong**
- Summarize key takeaways
- Provide next steps or call-to-action
- Link to related resources

## Post Structure Template

```markdown
# [Compelling Title]

*[Subtitle that clarifies the value proposition]*

[Hook paragraph - problem, question, or surprising fact]

[Context paragraph - where this fits in the big picture]

[What you'll learn paragraph - concrete outcomes]

## Prerequisites

- [What reader should already know]
- [Tools or setup required]

## [Main Section 1]

[Content with explanations, code, examples]

## [Main Section 2]

[Continue building on previous section]

## [Main Section 3]

[Bring it together]

## Conclusion

[Key takeaways]
[Call to action - what should reader do next?]

---

*Sources:*
- [Source 1](url)
- [Source 2](url)
```

## Quality Checklist

Before delivering, verify:
- [ ] Title is specific and compelling
- [ ] Introduction hooks and promises value
- [ ] Prerequisites declared (if tutorial)
- [ ] Each section has clear purpose
- [ ] Code snippets are explained
- [ ] No unexplained jargon
- [ ] Conclusion has call-to-action
- [ ] Sources are cited
