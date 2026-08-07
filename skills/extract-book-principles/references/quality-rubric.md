# Quality rubric

Score each dimension 0–2. Require no zero and at least 12/14 for an MVP marked `reviewing`. Require human source checks before `verified`.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Edition identity | Edition unknown | Partial bibliography | Edition, format, ISBN where present, and hash fixed |
| Scope | Scope implied | Scope stated broadly | Included chapters/sections and gaps explicit |
| Traceability | Missing/invalid references | Chapter-only references | Registered source plus section and stable format locator |
| Claim fidelity | Misattributed or copied excessively | Mostly faithful but vague | Concise paraphrase; exact type and source relationship clear |
| Type honesty | Types absent or misleading | Some ambiguity | `explicit`, `inferred`, `adapted`, `external` applied consistently |
| Action quality | Generic advice | Useful application | Specific application plus meaningful limitation or failure case |
| Dual-reader consistency | YAML/Markdown diverge | Manual agreement only | YAML is authoritative and Markdown is reproducibly generated |

## Review checks

For every principle:

1. Locate every referenced block in the registered edition.
2. Confirm the evidence supports the statement at its stated strength.
3. Downgrade `explicit` to `inferred` if the rule requires synthesis across passages.
4. Use `adapted` when adding an operational procedure not stated by the source.
5. Use `external` only with a separately registered source.
6. Remove decorative quotes and long excerpts; preserve only a necessary short quote.
7. Test whether the boundary prevents an obvious misuse.
8. Set confidence independently from review status. Confidence expresses evidential strength; review status expresses workflow maturity.

## Failure conditions

Reject the package when any source ID is unresolved, the edition is ambiguous, generated views are stale, a locator lacks a stable format coordinate, a copyrighted chapter is reproduced, or AI-created content is labeled `verified` without human checking.
