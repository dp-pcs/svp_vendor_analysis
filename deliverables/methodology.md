# Methodology

## 1. Approach Overview

8-phase execution: Data Prep → Classification → Recommendations → Top 3 → QA → Executive Memo → Final Packaging → Cross-Analysis

Tiered analysis by spend:
- Tier 1 ($100K+, 13 vendors): Deep research, web search, detailed classification
- Tier 2 ($25K–$100K, 27 vendors): Detailed classification with verification
- Tier 3 ($5K–$25K, 56 vendors): Pattern-based classification with spot checks
- Tier 4 (<$5K, 290 vendors): Automated classification with validation

Config tab reviewed first to establish the exact 12-department taxonomy before any classification logic was written. Both agents initially missed this and had to reclassify mid-run — catching this early was a critical design decision.

---

## 2. Tools Used

- Claude Code CLI (Read, Write, Edit, WebFetch, WebSearch tools)
- Task tool — spawned 4 parallel subagents to classify vendors simultaneously
- Custom /cross-analyze skill — built to systematically compare both agent outputs
- Python 3 — CSV processing, batch API calls, validation scripts
- Web search — vendor research for unknown or ambiguous vendors
- Git — version control for all scripts and outputs

---

## 3. Prompts and Commands

Classification prompt: 12-department taxonomy enforced, specific one-line description required (never generic), Terminate/Consolidate/Optimize with explicit criteria, JSON array returned indexed by row position only.

Research prompt: Web search for Tier 1/2 unknown vendors. D.O.O. noted as Croatian LLC equivalent.

Consolidation analysis prompt: Group vendors by function, calculate combined spend per cluster, estimate savings at 30–50% for consolidation, 15–25% for optimization, 100% for termination.

---

## 4. Validation Process

- Data integrity: Caught vendor count discrepancy (383 vs. 386). Resolved by exporting authoritative CSV directly from source Google Sheet.
- Classification validation: Spot checks against known vendor mappings; invalid department name scan run against all 386 rows.
- Recommendation distribution check: Expected ranges — Optimize 60–80%, Consolidate 10–25%, Terminate 5–15%. Flagged any batch deviating significantly from expected distribution.
- Name integrity: Results merged by row position only. Model was never trusted to return input vendor names accurately. This caught a hallucination bug in Agent 1 where plausible-but-wrong vendor names appeared in output.

---

## 5. Quality Check Evidence

- Generic description scan: Searched for phrases like "business services provider," "professional services," "consulting services" — 0 matches in final output.
- Consolidation group verification: Navan duplicate confirmed ($358K + $58K = $416K combined). Workspace cluster verified across 6 countries ($861K, 11 vendors).
- High-spend vendor spot checks: Top 10 vendors manually verified for department accuracy and description specificity.
- Savings reasonableness benchmarks: License optimization 10–15% (industry standard 10–25%); consolidation 17–29% (industry standard 15–35%). Conservative estimates used throughout — easier to exceed than miss.

---

## 6. Dual-Track Analysis

Two independent Claude Code CLI sessions classified all 386 vendors with no shared context until both analyses were complete. Cross-validation identified three critical errors caught before submission:

| Error | Agent | Caught By | Resolution |
|---|---|---|---|
| Hallucinated vendor names in output | Agent 1 | Agent 2 | Fixed merge-by-row-position; full re-run |
| Wrong vendor count (383 vs. 386) | Agent 2 | Agent 1 | User exported authoritative CSV from sheet |
| Wrong department taxonomy (invented categories) | Agent 2 | Agent 1 | Agent 2 reclassified 218 vendors to Config taxonomy |

Disputed high-spend classifications resolved through web research and human judgment. Final scorecard: Agent 1 correct on 7 of 11 high-spend disputes; Agent 2 correct on 4. Total savings estimates converged within 2% — Agent 1: $1.844M (23.4%), Agent 2: $1.88M (24%). Two independent methodologies, same bottom line.

---

## 7. Key Decisions

- Department taxonomy: Used exactly the 12 departments from the Config tab. No invented categories. M&A was explicitly preserved as a standalone department — not rolled into Finance.
- Recommendation framework: Terminate = one-off, local, or clearly redundant spend. Consolidate = functional duplicate of another vendor in the list. Optimize = essential vendor with negotiation or right-sizing opportunity.
- Conservative savings methodology: All estimates deliberately conservative (low end of industry ranges). More credible to a C-level audience; easier to exceed projections than miss them. Accounts for implementation friction and lease penalties.
- Row-position merge: Model output was never used to identify vendor names — always merged back to source CSV by row index. Prevents hallucination from corrupting vendor identity in final output.
