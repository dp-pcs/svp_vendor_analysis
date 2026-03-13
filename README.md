# Vendor Analysis Assessment — David Proctor

## Overview
This project analyzes ~386 vendors for an acquired company, acting as VP of Operations. For each vendor it assigns a department, a one-line description, and a strategic recommendation (Terminate / Consolidate / Optimize). The analysis was performed entirely using the **Claude Code CLI** with the **Anthropic API**.

**Google Sheet (view-only):**
https://docs.google.com/spreadsheets/d/1I9_S_uhLqcFSHvz3RbvwDR_Y1gc5CzHalUVLJqf8Pn8

---

## Project Structure

```
vendor-analysis/
├── data/
│   └── vendors.csv                  # Raw vendor data exported from Google Sheets (386 vendors)
├── output/
│   ├── vendors_analyzed.csv         # Classified output: department + description + recommendation
│   └── scoring_report.md            # Automated QA scoring report
├── scripts/
│   ├── analyze_vendors.py           # Main classification script (Anthropic API, batched)
│   ├── quality_check.py             # First-pass QA script
│   └── scoring_validation.py        # Scoring framework mapped to evaluation criteria
├── skills/
│   └── vendor-classifier/
│       └── SKILL.md                 # Reusable Claude Code skill for vendor classification
├── CLAUDE.md                        # Planning spec written before any code was run
└── README.md                        # This file
```

---

## How It Was Done

### Phase 1 — Planning (CLAUDE.md)
Before writing any code, a planning spec (`CLAUDE.md`) was written in Claude Code to define:
- The department taxonomy (11 categories)
- Recommendation criteria (Terminate / Consolidate / Optimize with specific thresholds)
- Output format and quality expectations

This mirrors professional spec-first engineering practice and ensures the AI has clear, bounded instructions before execution.

### Phase 2 — Data Extraction
All 386 vendors were exported from Google Sheets to `data/vendors.csv` using the Google Sheets API. Vendors were already sorted by annual spend (descending), which was preserved for prioritization.

### Phase 3 — AI Classification (Claude Code CLI)
`scripts/analyze_vendors.py` was written and executed via Claude Code CLI. It:
- Reads all vendors from CSV
- Sends batches of 25 vendors to the Anthropic API (`claude-sonnet-4-5`)
- Prompts for department, specific one-line description, and recommendation
- Validates each JSON response (correct field count, valid recommendation values)
- Retries up to 3x with exponential backoff on API errors
- Writes classified output to `output/vendors_analyzed.csv`

**Batch processing was used** to stay within API token limits and to allow partial recovery if a batch fails.

### Phase 4 — Multi-Agent Cross-Validation
Two independent Claude Code agent sessions classified the same 386 vendors **without shared context**. This is a **multi-agent ensemble validation** pattern:
- Agent 1 produced one set of classifications
- Agent 2 (a separate Claude Code instance with no shared context) produced an independent set
- Divergent classifications were identified and resolved using a reconciliation judgment pass

This approach catches classification errors that a single-pass review would miss, because two agents trained on the same data can still diverge on ambiguous vendors (e.g., a legal-tech SaaS that straddles Legal and Engineering).

### Phase 5 — Automated Scoring Validation
`scripts/scoring_validation.py` runs six programmatic checks mapped directly to the published evaluation criteria:

| Check | What it tests |
|---|---|
| Department Accuracy | Valid values, distribution sanity, spot-check against known vendors |
| Description Quality | Length, generic phrase detection, duplicate detection |
| Recommendation Quality | Valid values, spread distribution, high-spend Terminate flags |
| Financial Defensibility | Total savings potential, $1B business materiality threshold |
| Project Organization | Required file checklist |
| Description Specificity | Top-10 spend vendor depth, uniqueness ratio |

**Final score: 86% (B grade)** — see `output/scoring_report.md` for full detail.

### Phase 6 — Issue Remediation
Flagged issues from the scoring report were corrected:
- Generic descriptions rewritten (Verizon Wireless, Amazon Marketplace entries)
- Department corrections applied (DocuSign → Legal, AWS → Engineering)
- Re-scored after fixes

### Phase 7 — Reusable Skill
A reusable `vendor-classifier` skill was created in `skills/vendor-classifier/SKILL.md`. This skill can be applied to any acquisition due diligence engagement — not just this one. It documents the prompt structure, department taxonomy, batch approach, and validation steps so any Claude Code session can reproduce the full workflow from scratch.

---

## Prompts Used

### Classification Prompt (per batch of 25)
```
You are a VP of Operations analyzing vendors for an acquired company.
For each vendor, provide:
- department: one of [Engineering, IT/Infrastructure, G&A, Finance, Legal, Sales, Marketing, HR, Facilities, Support, Product]
- description: one tight, specific sentence. Be concrete. Bad: "business services provider". Good: "Corporate travel booking and expense management platform."
- recommendation: exactly Terminate | Consolidate | Optimize

Criteria:
- Terminate: redundant, one-off spend <$500, food/local/single-purchase, no clear business value
- Consolidate: same function as other vendors in this list
- Optimize: core vendor, valuable but likely over-provisioned or renegotiable

Return JSON array only: [{vendor_name, department, description, recommendation}]
```

---

## Quality Assurance

Quality was validated at three levels:
1. **Script-level**: JSON validation and field count checks on every API response
2. **Automated scoring**: `scoring_validation.py` produces a scored report against 6 criteria
3. **Multi-agent cross-validation**: Two independent Claude Code sessions compared, divergences resolved

The QA process specifically looked for:
- Generic or copy-paste descriptions
- Invalid department assignments
- High-spend vendors incorrectly marked Terminate
- Duplicate descriptions indicating template reuse
- Financial savings estimates that are too small to be meaningful for a $1B business

---

## Results Summary

| Metric | Value |
|---|---|
| Total vendors analyzed | 386 |
| Total annual spend | ~$7.9M |
| Optimize (cost reduction) | 180 vendors |
| Consolidate (eliminate duplicates) | 88 vendors |
| Terminate (eliminate entirely) | 118 vendors |
| Estimated total savings potential | ~$1.67M (21.3% of spend) |

---

## Tools Used
- **Claude Code CLI (Agent 1 + Agent 2)** — two independent sessions for classification and cross-validation
- **Anthropic API** (`claude-sonnet-4-5`) — vendor classification
- **Python 3** — scripting, CSV processing, validation
- **Google Sheets API** (via `gws` CLI) — data extraction and output upload
- **Git** — version control
