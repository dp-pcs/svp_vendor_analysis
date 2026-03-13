# Scoring Validation Framework

## Purpose

This document defines specific, measurable criteria for self-assessment against the evaluation rubric provided in the assessment instructions. Each criterion includes:
- What "good" looks like
- Specific tests to validate our output
- Red flags that would indicate failure
- Evidence we need to collect

---

## Criterion 1: Claude Code CLI Usage for Department Categorization

**What they're evaluating:** Did you use Claude Code CLI (not claude.ai or other AI tools)?

### Validation Tests:
- [ ] All work performed in terminal using `claude` CLI
- [ ] No browser-based AI tools used
- [ ] Session logs/commands can be referenced
- [ ] README documents CLI usage explicitly

### Evidence to Collect:
- Terminal session context (this conversation)
- Screenshots of Claude Code CLI in action (optional)
- README section explaining CLI workflow

### Red Flags:
- ❌ Generic outputs that look copy-pasted from ChatGPT
- ❌ No explanation of CLI-specific workflow
- ❌ Outputs that don't reference file operations, tool usage

### Score Targets:
| Score | Description |
|-------|-------------|
| ✅ Pass | Clear evidence of CLI usage, documented workflow |
| ⚠️ Weak | CLI used but poorly documented |
| ❌ Fail | No evidence of CLI usage |

---

## Criterion 2: Vendor Description Quality

**What they're evaluating:** Are descriptions concise, accurate, and specific?

### Validation Tests:
- [ ] No descriptions contain generic phrases:
  - "business services provider"
  - "professional services"
  - "consulting services"
  - "technology company"
- [ ] Each description answers: "What specifically does this vendor do?"
- [ ] Descriptions are 5-15 words (concise)
- [ ] Unknown vendors marked clearly rather than guessed

### Quantitative Checks:
```
Total vendors: ~390
Generic descriptions allowed: 0
"Unknown/Unclear" acceptable: <5% (19 vendors max)
Average description length: 8-12 words
```

### Sample Quality Test (run on 20 random vendors):
- [ ] Can a reader understand what the vendor does without Googling?
- [ ] Is the description specific to that vendor (not interchangeable)?

### Red Flags:
- ❌ "Provides business solutions"
- ❌ "Technology and services company"
- ❌ "Professional consulting firm"
- ❌ Same description used for multiple vendors

### Score Targets:
| Score | Description |
|-------|-------------|
| ✅ Pass | 95%+ specific descriptions, 0 generic phrases |
| ⚠️ Weak | 80-95% specific, some generic phrases |
| ❌ Fail | <80% specific or multiple generic descriptions |

---

## Criterion 3: Recommendation Quality (Terminate/Consolidate/Optimize)

**What they're evaluating:** Are recommendations realistic and strategic? Risk factors identified?

### Validation Tests:
- [ ] Every vendor has exactly one recommendation
- [ ] Recommendations distributed logically (not all "Optimize")
- [ ] High-spend vendors have justified recommendations
- [ ] Consolidation recommendations grouped logically
- [ ] Risk factors documented for major recommendations

### Distribution Sanity Check:
```
Expected distribution (rough):
- Terminate: 5-15% (vendors with redundant/unnecessary services)
- Consolidate: 10-25% (overlapping vendors)
- Optimize: 60-80% (core vendors worth keeping but negotiating)
```

### Logic Validation:
- [ ] Consolidation targets share similar functions (e.g., 2 travel platforms)
- [ ] Termination targets have clear rationale
- [ ] Critical infrastructure not marked for termination
- [ ] Top 10 spenders have detailed justification

### Red Flags:
- ❌ 100% of vendors marked "Optimize" (lazy)
- ❌ Critical vendors (Salesforce, AWS) marked "Terminate"
- ❌ No consolidation groups identified
- ❌ Recommendations without strategic rationale

### Score Targets:
| Score | Description |
|-------|-------------|
| ✅ Pass | Logical distribution, grouped consolidations, risk factors noted |
| ⚠️ Weak | Recommendations present but poorly justified |
| ❌ Fail | Illogical recommendations, missing risk factors |

---

## Criterion 4: Top 3 Opportunities Quality

**What they're evaluating:** Specific, plausible, financially justified?

### Validation Tests:
- [ ] Each opportunity has clear title
- [ ] Each has detailed explanation (not just "consolidate vendors")
- [ ] Savings estimates include calculation methodology
- [ ] Savings are significant for a $1B business (>$100K each minimum)
- [ ] Total savings meaningful (targeting $500K-$1M+)

### Financial Justification Requirements:
```
For each opportunity:
- List affected vendors and their spend
- State savings percentage with rationale (e.g., "30% from consolidation based on industry benchmarks")
- Show calculation: Affected Spend × Savings % = Estimated Savings
- Note assumptions
```

### Plausibility Checks:
- [ ] Savings percentages are realistic (15-30% optimization, 30-50% consolidation)
- [ ] Not claiming 100% savings unless true termination
- [ ] Implementation is feasible (not "renegotiate all 400 contracts")

### Red Flags:
- ❌ Vague opportunities ("reduce vendor spend")
- ❌ No dollar amounts or calculations
- ❌ Unrealistic savings (80% cost reduction)
- ❌ Opportunities that don't connect to vendor data

### Score Targets:
| Score | Description |
|-------|-------------|
| ✅ Pass | 3 specific opportunities, clear math, $500K+ total savings |
| ⚠️ Weak | Opportunities identified but weak justification |
| ❌ Fail | Vague opportunities, no financial backing |

---

## Criterion 5: Methodology Documentation

**What they're evaluating:** Clear explanation of approach, tools, prompts, validation?

### Validation Tests:
- [ ] Describes overall approach (phases, strategy)
- [ ] Lists specific tools used (Claude Code CLI, specific commands)
- [ ] Includes actual prompts used (not just descriptions)
- [ ] Explains how work was validated
- [ ] Quality check process documented with evidence

### Required Sections:
```
1. Approach Overview
2. Tools Used (with specifics)
3. Prompts/Commands (actual examples)
4. Validation Process
5. Quality Check Evidence
```

### Red Flags:
- ❌ "I used AI to categorize vendors" (no specifics)
- ❌ No mention of validation process
- ❌ No example prompts
- ❌ Quality check claimed but no evidence

### Score Targets:
| Score | Description |
|-------|-------------|
| ✅ Pass | All 5 sections complete, specific details, evidence provided |
| ⚠️ Weak | Methodology present but lacking specifics |
| ❌ Fail | Missing sections, no validation evidence |

---

## Criterion 6: Quality Check Documentation

**What they're evaluating:** Did you QC and document what you looked for?

### Validation Tests:
- [ ] QC process clearly defined
- [ ] Specific checks listed (not just "reviewed for accuracy")
- [ ] Sample of vendors manually verified
- [ ] Errors found and corrected (shows rigor)
- [ ] Evidence provided (screenshots, logs, specific examples)

### QC Evidence Requirements:
```
Minimum evidence:
- 10% spot check of vendor classifications (39+ vendors)
- Web search verification for 10+ unknown vendors
- Math verification for all savings calculations
- Spell check on executive memo
- Cross-check with Agent 1 analysis
```

### Red Flags:
- ❌ "I reviewed the output for accuracy" (no specifics)
- ❌ Zero errors found (suggests no real QC)
- ❌ No evidence provided
- ❌ QC section is 1-2 sentences

### Score Targets:
| Score | Description |
|-------|-------------|
| ✅ Pass | Detailed QC process, specific checks, evidence of corrections |
| ⚠️ Weak | QC mentioned but lacking evidence |
| ❌ Fail | No QC documentation or fake QC claims |

---

## Criterion 7: Executive Memo Quality

**What they're evaluating:** Clear, succinct, error-free, significant savings for $1B business?

### Validation Tests:
- [ ] 1 page maximum (approximately 400-600 words)
- [ ] Professional tone appropriate for CEO/CFO
- [ ] Clear structure with headers
- [ ] No grammatical or spelling errors
- [ ] No mathematical errors
- [ ] Savings significant (>0.1% of $1B = $1M+ ideal)
- [ ] Includes timeline
- [ ] Includes implementation process
- [ ] Includes risks

### Required Elements:
```
1. Executive Summary (2-3 sentences)
2. Key Findings
3. Top Savings Opportunities with $ amounts
4. Total Potential Savings
5. Timeline (30/60/90 day or similar)
6. Implementation Process
7. Risks and Mitigation
```

### Significance Test:
```
For a $1B business:
- $100K savings = 0.01% (minimal impact)
- $500K savings = 0.05% (notable)
- $1M+ savings = 0.1%+ (significant, worth executive attention)

Target: $500K-$1M+ to "move the needle"
```

### Red Flags:
- ❌ Longer than 1 page
- ❌ Missing timeline, implementation, or risks
- ❌ Typos or grammar errors
- ❌ Math errors in savings totals
- ❌ Savings <$100K (not significant for $1B company)

### Score Targets:
| Score | Description |
|-------|-------------|
| ✅ Pass | All elements, error-free, $500K+ savings, professional tone |
| ⚠️ Weak | Elements present but errors or weak savings |
| ❌ Fail | Missing elements, errors, insignificant savings |

---

## Criterion 8: Project Organization

**What they're evaluating:** Well-organized folder with inputs, outputs, scripts, README?

### Validation Tests:
- [ ] Clear folder structure
- [ ] README explains project
- [ ] Inputs clearly separated from outputs
- [ ] Scripts documented if used
- [ ] File naming is consistent and clear
- [ ] No unnecessary files or clutter

### Required Structure:
```
✅ README.md - Project overview
✅ data/ - Input data files
✅ analysis/ - Working analysis files
✅ deliverables/ - Final outputs
✅ qa/ - Quality assurance documentation
✅ scripts/ - Any automation (if applicable)
```

### README Requirements:
```
1. Project overview
2. Folder structure explanation
3. How to navigate deliverables
4. Methodology summary
5. Tools used
```

### Red Flags:
- ❌ Flat folder with all files in root
- ❌ No README or minimal README
- ❌ Unclear file names (file1.csv, output.txt)
- ❌ Missing deliverables

### Score Targets:
| Score | Description |
|-------|-------------|
| ✅ Pass | Clear structure, comprehensive README, easy to navigate |
| ⚠️ Weak | Some organization but confusing or incomplete |
| ❌ Fail | No organization, no README |

---

## Pre-Submission Checklist

Run this checklist before final submission:

### Part 1: Vendor Analysis
- [ ] All ~390 vendors have Department assigned
- [ ] All vendors have specific 1-line description
- [ ] All vendors have Terminate/Consolidate/Optimize recommendation
- [ ] Zero generic descriptions ("business services provider")
- [ ] Consolidation groups are logical

### Part 2: Top 3 Opportunities
- [ ] 3 opportunities identified
- [ ] Each has title, explanation, and $ savings
- [ ] Calculations shown and verified
- [ ] Total savings > $500K

### Part 3: Methodology
- [ ] Approach explained
- [ ] Tools listed with specifics
- [ ] Prompts included
- [ ] Validation process documented
- [ ] QC evidence provided

### Part 4: Executive Memo
- [ ] ≤1 page
- [ ] Timeline included
- [ ] Implementation process included
- [ ] Risks included
- [ ] Spell-checked
- [ ] Math verified

### Project Organization
- [ ] Folder structure clear
- [ ] README complete
- [ ] All deliverables present
- [ ] Files clearly named

### Cross-Analysis (Phase 8)
- [ ] Compared with Agent 1 results
- [ ] Discrepancies documented
- [ ] Best insights synthesized

---

## Final Score Card

Complete this after all work is done:

| Criterion | Self-Score | Evidence |
|-----------|------------|----------|
| 1. Claude Code CLI Usage | ⬜ | |
| 2. Description Quality | ⬜ | |
| 3. Recommendation Quality | ⬜ | |
| 4. Top 3 Opportunities | ⬜ | |
| 5. Methodology | ⬜ | |
| 6. Quality Check | ⬜ | |
| 7. Executive Memo | ⬜ | |
| 8. Project Organization | ⬜ | |

**Overall Assessment:** ⬜ Ready for Submission / ⬜ Needs Work
