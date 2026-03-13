# Methodology

## Approach

This analysis was conducted entirely using the Claude Code CLI and the Anthropic API. The goal was to build a repeatable, auditable workflow — not a one-time manual review — so the same process can be applied to future acquisitions.

---

## Tools Used

- **Claude Code CLI** — Primary tool for script generation, execution, and iteration
- **Anthropic API (claude-sonnet-4-5)** — AI model used for vendor classification
- **Python 3** — Scripting, CSV processing, validation logic
- **Google Sheets API** — Data extraction and output publishing
- **Web Research** — Unknown vendor identification via web search for high-spend vendors
- **Git** — Version control for all scripts and outputs

---

## Process

### Step 1: Spec-First Planning
Before writing any code, a planning document (CLAUDE.md) was written to define the department taxonomy, recommendation criteria, and output format. This ensures the AI operates within bounded, consistent parameters.

### Step 2: Data Extraction + Config Review
All 386 vendors were exported from the source Google Sheet to a local CSV file. **Critically — the Config tab was reviewed first** to identify the exact 12 department categories defined by the assessment. This is a step both independent agents initially missed and had to correct.

### Step 3: Tiered Analysis Strategy
Vendors were prioritized by spend for appropriate research depth:

| Tier | Spend Range | Count | Approach |
|---|---|---|---|
| 1 | $100K+ | 13 | Deep research, web search, detailed classification |
| 2 | $25K–$100K | 27 | Detailed classification with verification |
| 3 | $5K–$25K | 56 | Pattern-based classification with spot checks |
| 4 | <$5K | 290 | Automated classification with validation |

### Step 4: AI Classification via Claude Code CLI
A Python script (`scripts/analyze_vendors.py`) was written and executed via Claude Code CLI. The script:
- Processes vendors in batches of 25
- Sends each batch to the Anthropic API with a structured prompt
- Validates JSON responses (field count, valid recommendation values, valid department names)
- **Merges by row position — never trusts the model to return input values accurately**
- Retries up to 3x with exponential backoff on failure
- Writes classified output preserving original vendor names

**Key lesson learned:** An early run had the model hallucinating plausible vendor names instead of returning the actual input names. The fix — merge by row position — was identified through cross-validation and applied before submission.

### Step 5: Multi-Agent Cross-Validation
Two independent Claude Code agent sessions (Agent 1 and Agent 2) classified the same 386 vendors without shared context. This multi-agent ensemble validation pattern catches errors that single-pass review misses.

After both sessions completed, outputs were compared vendor-by-vendor. The comparison identified:

| Error | Agent | Caught By | Resolution |
|---|---|---|---|
| Hallucinated vendor names | Agent 1 | Agent 2 | Fixed merge-by-position; full re-run |
| Incorrect vendor count (383 vs 386) | Agent 2 | Agent 1 | User provided authoritative CSV |
| Wrong department taxonomy | Agent 2 | Agent 1 | Agent 2 reclassified 218 vendors to Config taxonomy |

**Standard applied:** Neither AI output was accepted until verifiably correct. 100% accuracy was the only acceptable standard — "close enough" was explicitly rejected on both runs.

Disagreements on 293 vendors were reviewed and resolved through:
1. Web research on high-spend ambiguous vendors
2. User judgment calls on genuine toss-ups
3. Document `analysis/user_decisions.md` records all final calls with rationale

**Final user decision scorecard: Agent 1 correct on 7 of 11 disputed high-spend vendors; Agent 2 correct on 4.**

### Step 6: Automated Scoring Validation
A dedicated scoring script (`scripts/scoring_validation.py`) was written to evaluate output quality against six criteria mapped directly to the published evaluation rubric:

| Check | What It Tested |
|---|---|
| Department Accuracy | Valid values, distribution sanity, spot-check against known vendors |
| Description Quality | Length distribution, generic phrase detection, duplicate detection |
| Recommendation Quality | Valid values, spread, high-spend Terminate flag |
| Financial Defensibility | Total savings potential vs. $1B business materiality |
| Project Organization | Required file checklist |
| Description Specificity | Top-10 spend vendor depth, uniqueness ratio |

**Agent 1 final score: 98% (A) — Agent 2 score: 79% (C)**

The primary gap in Agent 2's score: 105 descriptions under 5 words, and duplicate descriptions ("Croatian business services" used 7x) indicating template reuse on the long tail.

### Step 7: Issue Remediation
All flagged issues were corrected before final submission:
- Cloudcrossing Bvba → Engineering (PDF Butler = Salesforce ISV)
- RSM UK → M&A (M&A advisory, dedicated Config category)
- Telefonica → G&A + Consolidate
- Aetna, Bupa, Cigna, Care Health, Agram Life → G&A (health insurance = G&A, not Support)
- Big Frontier → Professional Services
- Tmforum → Professional Services

### Step 8: Reusable Skill
A reusable `vendor-classifier` skill was created (`skills/vendor-classifier/SKILL.md`) so this workflow can be applied to future acquisition due diligence without rebuilding from scratch.

---

## Classification Prompt

```
You are analyzing vendor spend for an acquired company. For each vendor, provide:
- department: MUST be exactly one of these 12:
  Engineering, Facilities, G&A, Legal, M&A, Marketing, SaaS, Product,
  Professional Services, Sales, Support, Finance
- description: one tight specific sentence. Be concrete, not generic.
  Bad: "business services provider"
  Good: "Corporate travel booking and expense management platform."
- recommendation: exactly one of Terminate | Consolidate | Optimize

Criteria:
- Terminate: one-off purchase, food/local vendor, spend <$100, clearly redundant
- Consolidate: duplicates another vendor in this list doing the same function
- Optimize: core vendor, renegotiable or over-provisioned

IMPORTANT: Return results in EXACT same order as input. Use index to match.

Return JSON array ONLY:
[{"index": 1, "department": "...", "description": "...", "recommendation": "..."}]
```

---

## Quality Check Evidence

Quality was validated at four distinct levels:

**1. API response validation** — Every batch response was checked for JSON structure, field count, valid department names, and valid recommendation values before being written to output.

**2. Name integrity check** — Output vendor names were verified against source names by row position. Any mismatch flags a critical hallucination error.

**3. Automated scoring script** — `scoring_validation.py` produces a scored report mapped to 6 evaluation criteria (see `output/scoring_report.md`).

**4. Multi-agent cross-validation** — Two independent sessions compared; all divergences reviewed; final decisions documented in `analysis/user_decisions.md`.

**QA checklist for exec memo:**
- ✅ ≤1 page
- ✅ Timeline included
- ✅ Risk table included
- ✅ Savings math verified
- ✅ Grammar and spelling reviewed
- ✅ Savings material for $1B business (>$500K)

The QA process specifically looked for:
- Generic or copy-paste descriptions
- Invalid department assignments
- High-spend vendors incorrectly flagged for termination
- Duplicate descriptions indicating template reuse
- Savings estimates too small to be material for a $1B business
- Vendor names not matching source data

---

## Project Repository

All inputs, outputs, scripts, and documentation are version-controlled in Git. Key commits document each phase including error discovery and remediation.

```
vendor-analysis/
├── data/vendors.csv                      # Raw input (386 vendors)
├── output/vendors_analyzed.csv           # Final classified output
├── output/scoring_report.md             # Automated QA score: 98%
├── scripts/analyze_vendors.py           # Main classification script
├── scripts/scoring_validation.py        # Scoring framework
├── scripts/quality_check.py            # First-pass QA
├── skills/vendor-classifier/SKILL.md   # Reusable classification skill
├── analysis/cross_analysis.md          # Cross-validation report
├── analysis/user_decisions.md          # David Proctor's final calls
├── analysis/agent1_wins.md             # Agent 1 position paper
├── CLAUDE.md                           # Planning spec
└── README.md                           # Full methodology
```
