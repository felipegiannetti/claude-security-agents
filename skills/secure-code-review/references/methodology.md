# Review Methodology

The step-by-step process for reviewing code for security issues, independent of vulnerability category.

## 1. Establish Context First

Before reading a single line for vulnerabilities, know: what does this code do, who can reach it, and what does the architecture model say about the controls around it (authentication, authorization, framework protections)? Reviewing code without this context produces exactly the kind of pattern-matched, low-confidence findings this project exists to avoid — see CLAUDE.md's Core Design Principle.

## 2. Prioritize by Attack Surface, Not File Order

Use the attack surface map (`04_attack_surface_mapping`) to spend the most attention on high-risk entry points (unauthenticated, sensitive operation) — not a uniform line-by-line sweep. A low-risk internal admin tool with the same code pattern as a public API deserves less scrutiny per CLAUDE.md's evidence-driven, not checklist-driven, principle.

## 3. For Each Candidate Pattern, Ask in Order

1. Is there attacker-influenced data involved at all? If not, stop — this isn't a security issue.
2. Where exactly does that data enter (source), and where does it end up (sink)? See [source-sink-analysis.md](source-sink-analysis.md).
3. What happens to it in between? See [data-flow-analysis.md](data-flow-analysis.md).
4. What would make this *not* exploitable — validation, framework protection, authorization elsewhere? See [false-positive-analysis.md](false-positive-analysis.md).
5. Only after 1–4: is this a candidate finding, and with what confidence?

## 4. Correlate, Don't Just Confirm, Scanner Output

A scanner result narrows *where* to look; it does not replace steps 1–4. Treat every scanner hit as a hypothesis to test, per [security.md](../../../.claude/rules/security.md)'s Scanner Trust Policy.

## 5. Write Down What You Didn't Confirm

A candidate finding with an honestly incomplete `data_flow` and `confidence: LOW` is more useful than one that quietly assumed the missing piece. `security-verifier` and, optionally, `pentest-validator` exist specifically to close those gaps — don't pretend to have already closed them.

## 6. Stop When the Evidence Runs Out

Not every suspicious-looking pattern resolves into either a confirmed finding or a clean rejection during the first pass. `NEEDS_MORE_EVIDENCE` is a legitimate, useful outcome — see CLAUDE.md's Finding Lifecycle.
