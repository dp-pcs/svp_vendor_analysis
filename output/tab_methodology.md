# Methodology

## Approach

This analysis was conducted entirely using the Claude Code CLI and the Anthropic API. The goal was to build a repeatable, auditable workflow — not a one-time manual review — so that the same process can be applied to future acquisitions.

## Tools Used

- **Claude Code CLI** — Primary tool for script generation, execution, and iteration
- **Anthropic API (claude-sonnet-4-5)** — AI model used for vendor classification
- **Python 3** — Scripting, CSV processing, validation logic
- **Google Sheets API** — Data extraction and output publishing
- **Git** — Version control for all scripts and outputs

## Process

### Step 1: Spec-First Planning
Before writing any code, a planning document (CLAUDE.md) was written to define the department taxonomy, recommendation criteria, and output format. This ensures the AI operates within bounded, consistent parameters rather than making unconstrained judgment calls.

### Step 2: Data Extraction
All 386 vendors were exported from the source Google Sheet to a local CSV file via the Google Sheets API. Vendors were already sorted by annual spend (descending), which was preserved to ensure high-spend vendors received the most scrutiny.

### Step 3: AI Classification via Claude Code CLI
A Python script (analyze_vendors.py) was written and executed via Claude Code CLI. The script:
- Processes vendors in batches of 25
- Sends each batch to the Anthropic API with a structured prompt
- Validates the JSON response (field count, valid recommendation values)
- Retries failed batches up to 3 times with exponential backoff
- Writes classified output to CSV

### Classification Prompt
The prompt instructed the model to assign each vendor:
- **Department** (one of 11 defined categories: Engineering, IT/Infrastructure, G&A, Finance, Legal, Sales, Marketing, HR, Facilities, Support, Product)
- **Description** — one tight, specific sentence (explicit instruction: not "business services provider")
- **Recommendation** — exactly one of: Terminate | Consolidate | Optimize

Recommendation criteria provided in the prompt:
- **Terminate**: Redundant, one-off spend <$500, food/local/single-purchase vendors
- **Consolidate**: Same function as another vendor in the list
- **Optimize**: Core vendor, valuable but likely over-provisioned or renegotiable

### Step 4: Multi-Agent Cross-Validation
Two independent Claude Code agent sessions (Agent 1 and Agent 2) classified the same 386 vendors without shared context. This multi-agent ensemble validation pattern catches classification errors that single-pass review misses — two agents trained on the same data can still diverge on ambiguous vendors (e.g., a legal-tech SaaS that could reasonably fall under Legal or Engineering).

After both sessions completed, outputs were compared vendor-by-vendor. Divergences were reviewed and resolved using a third-pass judgment call documented in the Cross-Validation tab.

### Step 5: Automated Scoring Validation
A dedicated scoring script (scoring_validation.py) was written to evaluate output quality against six criteria mapped directly to the published evaluation rubric:

| Check | What it tested |
|---|---|
| Department Accuracy | Valid values, distribution sanity, spot-check against known vendors |
| Description Quality | Length distribution, generic phrase detection, duplicate detection |
| Recommendation Quality | Valid values, spread, high-spend Terminate flag |
| Financial Defensibility | Total savings potential vs. $1B business materiality |
| Project Organization | Required file checklist |
| Description Specificity | Top-10 spend vendor depth, uniqueness ratio |

**Score after remediation: 93% (A grade)**

### Step 6: Issue Remediation
Flagged issues from the scoring report were corrected:
- Generic descriptions rewritten (Verizon Wireless, Amazon Marketplace entries)
- Department corrections applied (DocuSign → Legal, AWS → Engineering)
- Re-scored to confirm improvement

### Step 7: Reusable Skill Creation
A reusable vendor-classifier skill (skills/vendor-classifier/SKILL.md) was created so this workflow can be applied to any future acquisition without rebuilding from scratch.

## Quality Check Evidence

Quality was validated at three distinct levels:

1. **API response validation** — Every batch response was checked for correct JSON structure, field count, and valid recommendation values before being written to output
2. **Automated scoring script** — scoring_validation.py produces a scored report (output/scoring_report.md) with specific pass/fail checks
3. **Multi-agent cross-validation** — Two independent sessions compared; divergences documented in the Cross-Validation tab

The QA process specifically looked for:
- Generic or copy-paste descriptions
- Invalid or unlikely department assignments
- High-spend vendors incorrectly flagged for termination
- Duplicate descriptions indicating template reuse
- Savings estimates too small to be material for a $1B business

### Errors Found and Remediated

The cross-validation process identified real errors in both agent outputs — errors that would have compromised the submission if not caught:

**Agent 1 (critical):** The classification script asked the model to return vendor names in its JSON response. The model hallucinated plausible vendor names (e.g., returning "Amazon Web Services" for a vendor named "Salesforce Uk Ltd-Uk") instead of echoing the original input. All 386 classifications were applied to the wrong vendor names. The fix: merge results by row position only, never trust the model to return input values accurately. Corrected and re-run to 100%.

**Agent 2:** Initial run returned an incorrect vendor count (92% coverage). "Close enough" was explicitly rejected. 100% coverage was the only acceptable standard. Re-run until complete.

**Standard applied:** Neither AI output was accepted until it was verifiably correct. This is the appropriate standard for any data product going to senior leadership — a CFO looking at vendor spend recommendations needs to trust that the data is accurate, not approximately accurate.

## Project Repository

All inputs, outputs, scripts, and documentation are version-controlled in the project GitHub repository. Structure:

- data/ — Raw input CSV
- output/ — Classified vendors CSV, scoring report
- scripts/ — analyze_vendors.py, quality_check.py, scoring_validation.py
- skills/vendor-classifier/ — Reusable classification skill
- CLAUDE.md — Planning spec
- README.md — Full methodology documentation
