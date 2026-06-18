---
name: prose-style
description: "Proofread and edit Markdown prose against the user's personal style guide (Orwell + Economist influenced; opinionated about voice, sentence shape, and Markdown formatting). Use when the user asks to proof, edit, review, rewrite, tighten, or critique a Markdown file, section, or passage. Does not run automatically on pi's own writing — invoke explicitly via /skill:prose-style or by asking."
---

# prose-style

Apply this style guide to Markdown the user asks you to proofread, edit, or rewrite.

## Workflow

The user works under version control, so apply edits directly rather than producing a review-only report.

1. Confirm scope: a whole file, a specific section, or a pasted passage.
2. For a long file, work section by section using the `read-md` skill rather than loading the whole thing into context.
3. Apply edits with the `edit` tool, one `edits[]` entry per change. Preserve everything else untouched.
4. After applying, summarise what changed in a few lines: which rules drove the edits, and any judgement calls the user should review.

If the user explicitly asks for a review only ("flag issues, don't change anything"), produce a numbered list of violations with suggested rewrites instead, and stop.

## Scope rules

Do not rewrite:

- Fenced code blocks (```` ``` ```` or `~~~`).
- Inline code (`` `like this` ``).
- Block quotations (lines starting with `>`). These are usually someone else's words.
- YAML frontmatter, HTML blocks, or link/image URLs.
- Headings: exempt from the one-sentence-per-line rule, but still subject to the prose rules (no slogans, no abstract noun stacks).

## Prose rules

Use concrete, specific prose.
Follow Orwell's bias for short words, short sentences, active voice, and cutting any word that can be cut.
Follow Economist style: clarity before flair, precise verbs, plain English, no pomposity.

Flag and rewrite:

- Generic uplift and motivational filler.
- LinkedIn-style revelation arcs ("I used to think X. Then I learned Y. Now…").
- Abstract noun stacks ("the implementation of optimisation strategies" → "optimising").
- Slogan endings and tidy aphoristic closers.
- Over-balanced templates: "not just X, but Y", "the real challenge is…", "it's not about X — it's about Y".
- Overused em dashes, rule-of-three triads, and polished transitional connectives ("moreover", "ultimately", "in essence").
- **Lazy hedges only** — words like "perhaps", "arguably", "in many ways", "somewhat", "often" used to dodge commitment on a claim the writer should just make. Keep precise qualifiers that carry real information in technical writing: "typically", "by default", "in most production deployments", "unless X is set", "as of version N". The test: if removing the hedge would make the sentence inaccurate, keep it; if it would just make the sentence more direct, cut it.
- Sentences that could appear in any article on any topic. Prefer details that could only fit *this* topic.
- Uniform sentence shape. Vary length and structure deliberately.
- Passive voice when an active rewrite exists.

Prefer:

- Direct claims over hedged ones.
- Concrete nouns and specific verbs over abstract ones.
- Short sentences with the occasional longer one for rhythm.

## Markdown formatting rules

- **Nested lists over tables.** If the information is hierarchical or fewer than ~4 columns wide, use a nested bullet list. Keep tables for genuinely tabular comparisons where every row shares the same columns.
- **No `---` horizontal rules** as section dividers. Use a heading or paragraph spacing instead. (Frontmatter delimiters at the top of a file are fine.)
- **One sentence per line** (semantic line breaks), with a blank line between paragraphs. This keeps git diffs readable. Do not reflow sentences onto shared lines. A line break inside a paragraph carries no semantic weight in rendered Markdown — it is purely for diff hygiene.

## Output format if the user asks for review-only mode

```
1. <file>:<line> — "<offending phrase>"
   Rule: <which rule>
   Suggest: "<rewrite>"
```

Group by rule when there are many violations of the same kind.

## Notes

- This skill is opinionated. When in doubt, lean toward fewer words and more specificity.
- If a rewrite changes meaning or tone significantly, flag it in the post-edit summary so the user can revert via git.
