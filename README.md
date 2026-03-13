# Vendor Analysis Assessment — David Proctor

Analysis of 386 vendors across $7.9M in annual spend for a post-acquisition due diligence scenario.

## Google Sheet
[Vendor Analysis Assessment](https://docs.google.com/spreadsheets/d/1I9_S_uhLqcFSHvz3RbvwDR_Y1gc5CzHalUVLJqf8Pn8)

Tabs: Vendor Analysis Assessment | Session A - Agent 1 | Session B - Agent 2 | Cross-Validation | Top 3 Opportunities | Methodology | CEO/CFO Recommendations

## Executive Memo (Google Doc)
[Vendor Spend Analysis — Executive Memo](https://docs.google.com/document/d/1SO3Y3U0C9d3oC4lSzAv3G771mzyZR4v59ShXf2S8pJ4/edit)

## Key Results
- **386 vendors** analyzed | **$7,887,359** total annual spend
- **$1,853,331** in addressable savings (23.4%)
- Optimize: 190 vendors | Consolidate: 49 | Terminate: 147
- QA score: **98% (A)** — validated via automated scoring script

## Top 3 Opportunities
1. **Salesforce Renegotiation** — $312K–$623K (40% of total spend, post-acq leverage window)
2. **Global Workspace Consolidation** — $150K–$261K (11 vendors, 6 countries, fragmented procurement)
3. **Travel, Benefits & Telecom** — $150K–$224K (Navan duplicate + 5 health carriers + 3 telecom carriers)

## Project Structure

```
vendor-analysis/
├── PLAN.md                          # 8-phase execution plan
├── CLAUDE.md                        # Classification spec and taxonomy
├── STANDARDS.md                     # Quality standards
├── data/
│   └── vendors.csv                  # Source data (386 vendors)
├── output/
│   └── vendors_final.csv            # Final classified output
├── deliverables/
│   ├── top_3_opportunities.md       # Part 2: Top 3 opportunities
│   ├── methodology.md               # Part 3: Methodology documentation
│   └── executive_memo.md            # Part 4: CEO/CFO memo
├── analysis/
│   ├── spend_analysis.md            # Initial spend breakdown
│   ├── consolidation_opportunities.md  # Grouped consolidation targets
│   ├── cross_analysis.md            # Cross-validation report
│   ├── cross_validation.csv         # Agent 1 vs Agent 2 comparison
│   ├── user_decisions.md            # Final human judgment calls
│   └── cross-validation/            # Agent debate artifacts
├── qa/
│   ├── scoring_validation.md        # Pre-built scoring framework
│   ├── scoring_report.md            # Final QA score: 98% (A)
│   └── quality_check_log.md         # QA evidence log
├── scripts/
│   ├── analyze_vendors.py           # Main classification script
│   ├── quality_check.py             # First-pass QA
│   └── scoring_validation.py        # Automated scoring (run against either agent)
└── skills/
    └── vendor-classifier/SKILL.md   # Reusable classification skill
```

## Methodology Summary

Two independent Claude Code CLI sessions classified all 386 vendors with no shared context until cross-validation. Tiered analysis by spend (deep research for $100K+ vendors, automated for <$5K). Custom `/cross-analyze` skill built to compare outputs. Three critical errors caught before submission through cross-validation. Final disputed classifications resolved via web research; documented in `analysis/user_decisions.md`.

**Agent 1: 7 wins | Agent 2: 4 wins** on disputed high-spend vendor calls.
**Both agents converged within 2% on total savings** ($1.844M vs $1.88M) — independent validation of the methodology.

See `deliverables/methodology.md` for full detail.
