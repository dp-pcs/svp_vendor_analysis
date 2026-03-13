# Vendor Analysis Assessment - Execution Plan

## Understanding Confirmation

### What I Need to Deliver:

**Part 1: Vendor Data Analysis (~400 vendors)**
- [ ] Department assignment (Engineering, G&A, Finance, Support, Sales, Marketing, HR, Legal, Facilities, IT, etc.)
- [ ] One-line description (specific, not generic like "business services provider")
- [ ] Strategic recommendation: Terminate | Consolidate | Optimize

**Part 2: Top 3 Strategic Opportunities**
- [ ] Summary title (e.g., "CRM Tool Consolidation")
- [ ] Brief explanation of the opportunity
- [ ] Estimated annual savings in USD (must be significant for a $1B business)

**Part 3: Methodology Documentation**
- [ ] How I approached the task
- [ ] Which tools I used (Claude Code CLI specifics)
- [ ] Prompts I created
- [ ] Quality check process with evidence

**Part 4: Executive Memo (1 page)**
- [ ] Audience: CEO and CFO
- [ ] Clear findings and savings opportunities
- [ ] Realistic timeline
- [ ] Implementation process
- [ ] Risks to the plan

### Evaluation Criteria I Must Meet:

1. ✅ Use Claude Code CLI (not claude.ai or other AI tools)
2. ✅ Accurate department categorization
3. ✅ Concise, specific vendor descriptions
4. ✅ Realistic, strategic recommendations with risk factors
5. ✅ Specific, plausible, financially justified top 3 opportunities
6. ✅ Clear methodology explanation
7. ✅ Documented quality check with evidence
8. ✅ Error-free executive memo with significant savings
9. ✅ Well-organized project folder with README

---

## Execution Plan

### Phase 1: Data Preparation & Initial Analysis
**Objective:** Organize raw data and understand vendor landscape

**Tasks:**
1. Export vendor data to local CSV file for processing
2. Calculate total spend and spend distribution
3. Identify vendor categories by name pattern analysis
4. Create initial department mapping logic

**Outputs:**
- `data/raw_vendors.csv` - Original data
- `data/spend_analysis.md` - Initial spend breakdown

---

### Phase 2: Vendor Classification & Research
**Objective:** Accurately classify each vendor

**Approach:**
1. **Batch processing by spend tier:**
   - Tier 1: $100K+ (13 vendors) - Manual deep research
   - Tier 2: $25K-$100K (25 vendors) - Detailed classification
   - Tier 3: $5K-$25K (50 vendors) - Pattern-based classification
   - Tier 4: <$5K (300+ vendors) - Automated classification with spot checks

2. **Department Categories:**
   - Engineering/IT - Software, cloud services, dev tools
   - Sales & Marketing - CRM, marketing automation, lead gen
   - G&A (General & Administrative) - Office, facilities, admin
   - Finance - Accounting, audit, banking
   - HR/People - Benefits, recruiting, training
   - Legal - Law firms, compliance
   - Support/Operations - Customer service tools
   - Facilities - Office space, supplies
   - Travel & Entertainment - Travel, food, events

3. **Research Methods:**
   - Web search for unknown vendors
   - Pattern recognition for similar vendor types
   - Cross-reference with known software/service categories

**Outputs:**
- `data/vendors_classified.csv` - All vendors with departments and descriptions
- `analysis/classification_log.md` - Notes on classification decisions

---

### Phase 3: Strategic Recommendations
**Objective:** Assign Terminate/Consolidate/Optimize to each vendor

**Framework:**
1. **Terminate candidates:**
   - Duplicate functionality with another vendor
   - Low strategic value relative to cost
   - One-time services no longer needed
   - Outdated or superseded solutions

2. **Consolidate candidates:**
   - Multiple vendors serving same function (e.g., 2 CRM tools)
   - Overlapping regional vendors that could be unified
   - Similar SaaS tools that could be reduced

3. **Optimize candidates:**
   - Essential vendors with room for negotiation
   - Underutilized licenses
   - Expensive tiers that could be downgraded

**Outputs:**
- `data/vendors_with_recommendations.csv` - Final vendor analysis
- `analysis/consolidation_opportunities.md` - Grouped consolidation targets

---

### Phase 4: Top 3 Opportunities Identification
**Objective:** Identify highest-impact savings opportunities

**Methodology:**
1. Analyze consolidation groups by total spend
2. Identify negotiation opportunities for top vendors
3. Calculate realistic savings percentages:
   - Consolidation: 30-50% of duplicate vendor spend
   - Optimization: 15-25% through negotiation/right-sizing
   - Termination: 100% of terminated vendor spend

4. Rank by total annual savings potential

**Output:**
- `deliverables/top_3_opportunities.md`

---

### Phase 5: Quality Assurance
**Objective:** Validate accuracy and catch errors

**QA Checks:**
1. **Spot check 10% of classifications** - Verify department assignments
2. **Cross-reference vendor names** - Web search to confirm descriptions
3. **Validate savings calculations** - Math check on all figures
4. **Peer review recommendations** - Ensure they're realistic
5. **Document all QA steps** - Evidence for methodology section
6. **Run Scoring Validation Framework** - Self-assess against all 8 evaluation criteria

**Scoring Validation Framework:** `qa/scoring_validation.md`
- Maps directly to the 8 evaluation criteria from the assessment
- Defines specific, measurable tests for each criterion
- Includes red flags to avoid
- Pre-submission checklist
- Final scorecard for self-assessment

**Output:**
- `qa/quality_check_log.md` - Detailed QA evidence
- `qa/scoring_validation.md` - Self-assessment against rubric (completed)

---

### Phase 6: Executive Memo
**Objective:** Write compelling C-level summary

**Structure:**
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Top 3 Savings Opportunities with $ amounts
4. Total Potential Savings
5. Implementation Timeline (30/60/90 day)
6. Implementation Process
7. Risks and Mitigation

**Output:**
- `deliverables/executive_memo.md`

---

### Phase 7: Final Deliverables & Documentation
**Objective:** Package everything professionally

**Tasks:**
1. Create final spreadsheet with all tabs
2. Write comprehensive README
3. Organize project folder structure
4. Final review of all deliverables

**Final Folder Structure:**
```
SVP_myversion/
├── README.md                    # Project overview and instructions
├── instructions.md              # Original assessment instructions
├── PLAN.md                      # This execution plan
├── .env                         # Spreadsheet source
├── data/
│   ├── raw_vendors.csv          # Original data
│   ├── vendors_classified.csv   # With departments/descriptions
│   └── vendors_final.csv        # With recommendations
├── analysis/
│   ├── spend_analysis.md        # Initial analysis
│   ├── classification_log.md    # Classification decisions
│   └── consolidation_opportunities.md
├── qa/
│   └── quality_check_log.md     # QA evidence
├── deliverables/
│   ├── top_3_opportunities.md   # Part 2
│   ├── methodology.md           # Part 3
│   └── executive_memo.md        # Part 4
└── scripts/
    └── vendor_classifier.py     # Any automation scripts used
```

---

## Timeline

| Phase | Tasks |
|-------|-------|
| Phase 1 | Data prep, initial analysis |
| Phase 2 | Vendor classification |
| Phase 3 | Strategic recommendations |
| Phase 4 | Top 3 opportunities |
| Phase 5 | Quality assurance |
| Phase 6 | Executive memo |
| Phase 7 | Final packaging |
| Phase 8 | Cross-analysis with Agent 1, synthesis |

---

## Key Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Misclassifying obscure vendors | Web research for unknowns, conservative categorization |
| Unrealistic savings estimates | Use industry-standard ranges (15-30% for optimization) |
| Missing consolidation opportunities | Group vendors by function, not just name |
| Generic descriptions | Research each vendor, avoid boilerplate language |
| Math errors in savings | Double-check all calculations |

---

---

## Phase 8: Cross-Analysis with Agent 1

**Context:** A parallel independent analysis is being conducted by Agent 1 subagents at `~/Documents/GitHub/vendor-analysis`. This dual-track approach provides:

1. **Independent validation** - Neither system sees the other's work until completion
2. **Error detection** - Discrepancies highlight areas needing deeper review
3. **Perspective diversity** - Different classification logic may surface unique insights
4. **Stronger deliverable** - Final synthesis incorporates best elements from both

### Custom Skill: `/cross-analyze`

A custom Claude Code skill has been created for this phase:
- **Location:** `~/.claude/skills/cross-analyze/SKILL.md`
- **Trigger:** Type `/cross-analyze` in either Claude Code session
- **Purpose:** Systematically compare both vendor analyses

**What the skill does:**
1. Loads both vendor analysis CSVs
2. Matches vendors across datasets
3. Compares department assignments (calculates agreement rate)
4. Compares recommendations (Terminate/Consolidate/Optimize)
5. Flags high-spend discrepancies for review
6. Generates structured comparison report
7. Recommends which analysis to favor for each discrepancy

### Process:

**IMPORTANT: Do NOT run `/cross-analyze` until BOTH analyses are complete!**

1. ✅ Complete Phases 1-7 independently (no peeking at Agent 1's work)
2. ✅ Verify Agent 1 has also completed their analysis
3. 🔄 Run `/cross-analyze` to compare outputs
4. 📝 Review discrepancies, especially high-spend vendors
5. 🔀 Have Agent 1 also run `/cross-analyze` from their session
6. ✨ Synthesize final deliverable with strongest insights from both

**Outputs:**
- `analysis/cross_analysis.md` - Comparison report from the skill
- `analysis/discrepancy_resolution.md` - Manual decisions on conflicts

**Updated Folder Structure:**
```
SVP_myversion/
├── README.md                    # Project overview and instructions
├── instructions.md              # Original assessment instructions
├── PLAN.md                      # This execution plan
├── .env                         # Spreadsheet source
├── data/
│   ├── raw_vendors.csv          # Original data
│   ├── vendors_classified.csv   # With departments/descriptions
│   └── vendors_final.csv        # With recommendations
├── analysis/
│   ├── spend_analysis.md        # Initial analysis
│   ├── classification_log.md    # Classification decisions
│   ├── consolidation_opportunities.md
│   ├── cross_analysis.md        # Comparison with Agent 1
│   └── discrepancy_resolution.md
├── qa/
│   └── quality_check_log.md     # QA evidence
├── deliverables/
│   ├── top_3_opportunities.md   # Part 2
│   ├── methodology.md           # Part 3
│   └── executive_memo.md        # Part 4
└── scripts/
    └── vendor_classifier.py     # Any automation scripts used
```

---

## Success Criteria

- [ ] All 390+ vendors have department, description, and recommendation
- [ ] Descriptions are specific (no "business services provider")
- [ ] Top 3 opportunities total significant savings (targeting $500K+ annual)
- [ ] Methodology clearly explains Claude Code CLI usage
- [ ] QA log shows systematic quality checking
- [ ] Executive memo is professional, error-free, actionable
- [ ] README clearly explains the project
- [ ] Cross-analysis with Agent 1 completed and documented
- [ ] Final synthesis incorporates best insights from both analyses
