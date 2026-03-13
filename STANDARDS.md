# Project Standards

## Non-Negotiable Requirements

### 1. 100% Data Accuracy

**There is no acceptable margin of error.**

- Every single vendor must be accounted for
- Every classification must be verified
- Every calculation must be checked
- "Close enough" is never acceptable

If data is incomplete, we stop and fix it before proceeding. We do not proceed with partial data and document the gap as acceptable.

### 2. No Guessing

- If a vendor is unknown, research it
- If research fails, mark it explicitly as "Unknown - requires manual verification"
- Never fabricate descriptions or classifications

### 3. Verify Before Proceeding

Before moving to the next phase:
- Confirm row counts match source data
- Spot-check calculations
- Validate assumptions

### 4. Interview Standard

This is an interview assessment. The evaluators are looking for:
- Precision
- Attention to detail
- Thoroughness
- Professional rigor

Anything less than 100% reflects poorly on the candidate. There are no shortcuts.

---

## Incident Log

### Data Accuracy Incident - Phase 1

**What happened:**
1. Claude (via WebFetch) retrieved vendor data and reported 390 vendors
2. User reviewed the source spreadsheet and identified **387 rows (386 vendors)**
3. Upon verification, Claude's saved data contained only **383 vendors** - a 3-vendor gap
4. Claude incorrectly suggested proceeding with 99.2% coverage, calling it "likely fine"
5. **User immediately rejected this**, stating: *"are you crazy? you think it's okay to be close to right?"*
6. User demanded 100% accuracy standards be documented
7. User provided authoritative local copy of the data

**Resolution:**
- User exported CSV directly from Google Sheets
- File saved to `data/raw_vendors.csv` (source of truth)
- This STANDARDS.md file created to enforce 100% accuracy going forward

**Lesson:**
For interview assessments (or any professional work), "close enough" is never acceptable. The user's attention to detail caught this error before it propagated through the entire analysis.

*Added after incorrectly suggesting 99.2% coverage was acceptable. It is not.*

---

### Cross-Validation Incident - Phase 8

**What happened:**
1. Agent 2 (this session) ran `/cross-analyze` to compare with Agent 1's output
2. Agent 1's vendor list contained **completely different vendors** (AWS, Slack, Zendesk, etc.)
3. The actual vendors were Croatian D.O.O. entities, UK firms, Australian providers
4. Agent 1's LLM script had **hallucinated vendor names** instead of using input data

**Agent 1's acknowledgment:**
> "No excuses — that's a fundamental data integrity failure. The script asked the model to return vendor names in the JSON output, and I didn't verify that what came back matched what went in."

**Why this matters:**
- Agent 1 caught Agent 2's missing vendor count (383 vs 386)
- Agent 2 caught Agent 1's hallucinated vendor names
- **Neither error would have been caught with a single-agent approach**

**Validation:**
The dual-track methodology worked exactly as designed. Independent analysis caught errors that would have gone undetected in a single-agent workflow.

**Lesson:**
For LLM-based data processing:
1. Never trust the model to return input values correctly
2. Merge by row position, not by model-generated identifiers
3. Cross-validate with independent analysis before submission

---

### Department Taxonomy Error - Phase 8

**What happened:**
1. Agent 2 used custom department categories (HR, IT, Operations, Travel & Entertainment, Sales & Marketing)
2. The Google Sheets Config tab defines **12 specific departments** that should be used
3. Agent 1 correctly followed the Config taxonomy; Agent 2 did not
4. This was discovered during cross-validation when comparing department classifications

**The 12 Valid Departments (from Config tab):**
1. Engineering
2. Facilities
3. G&A
4. Legal
5. M&A
6. Marketing
7. SaaS
8. Product
9. Professional Services
10. Sales
11. Support
12. Finance

**Agent 2's Invalid Departments:**
- HR → remapped to Support or Professional Services
- IT → remapped to SaaS or Engineering
- Operations → remapped to G&A
- Travel & Entertainment → remapped to G&A
- Sales & Marketing → split into Sales or Marketing

**Resolution:**
- All 386 vendors reclassified using the 12 valid departments
- 218 vendor department assignments corrected
- vendors_final.csv updated with correct taxonomy

**Lesson:**
Always check for defined taxonomies or schemas in source data before creating custom categories. The "(e.g., ...)" in instructions suggested examples, but the Config tab provided authoritative definitions.
