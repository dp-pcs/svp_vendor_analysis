# Skill: Vendor Classifier

## Purpose
Analyze a vendor spend CSV for an acquired or audited company and produce a classified output with department assignments, one-line descriptions, and strategic recommendations. Designed to be reusable across acquisition due diligence engagements.

## When to use this skill
- You have a CSV of vendor names and annual spend
- You need to classify vendors by department, describe what they do, and recommend Terminate / Consolidate / Optimize
- You want a defensible, auditable output suitable for executive review

## Input
A CSV file with at minimum:
- Vendor Name column
- Annual spend column (USD or any currency)

Optional columns (will be preserved): Department, Description, Recommendation

## Output
- `output/vendors_analyzed.csv` — original data plus three new columns: Department, Description, Recommendation
- `output/scoring_report.md` — automated quality validation report

## Steps

### 1. Read and inspect the CSV
- Load the file, print column names and row count
- Identify the vendor name column and cost column
- Note the currency and any formatting (e.g. "$1,234" vs "1234.00")

### 2. Parse costs
- Strip currency symbols and commas
- Convert to float for sorting
- Sort vendors by spend descending before processing (highest spend = highest priority)

### 3. Classify in batches of 25
Use the Anthropic API (claude-3-5-haiku or claude-sonnet for better accuracy on ambiguous vendors) with this prompt structure:

```
You are a VP of Operations analyzing vendors for an acquired company.
For each vendor, provide:
- department: one of [Engineering, IT/Infrastructure, G&A, Finance, Legal, Sales, Marketing, HR, Facilities, Support, Product]
- description: one tight, specific sentence. Be concrete. Bad: "business services provider". Good: "Corporate travel booking and expense management platform."
- recommendation: exactly Terminate | Consolidate | Optimize

Criteria:
- Terminate: redundant, one-off spend <$500, food/local/single-purchase, no clear business value
- Consolidate: same function as other vendors in this list (multiple travel tools, multiple legal firms, overlapping SaaS)
- Optimize: core vendor, valuable but likely over-provisioned or renegotiable

Return JSON array only: [{vendor_name, department, description, recommendation}]
```

### 4. Validate each batch response
- Confirm JSON parses cleanly
- Confirm count matches input batch size
- Confirm recommendation is exactly one of the three valid values
- Retry up to 3x with exponential backoff on failure

### 5. Run scoring validation
After all vendors are classified, run `scripts/scoring_validation.py` to:
- Check department distribution
- Flag generic descriptions
- Verify recommendation spread
- Compute financial defensibility (total potential savings)
- Check project file organization

### 6. Fix flagged issues
- Re-classify any vendors where spot-check mismatches are found
- Rewrite any generic descriptions
- Confirm high-spend vendors ($50K+) are not marked Terminate without justification

## Department Reference

| Department | What belongs here |
|---|---|
| Engineering | Dev tools, cloud infra (AWS/GCP/Azure), CI/CD, APIs, monitoring |
| IT/Infrastructure | SaaS platforms, networking, security, hardware, collaboration tools |
| G&A | Admin, office management, general software, payroll, compliance |
| Finance | Accounting firms, audit, banking, payments, tax, ERP |
| Legal | Law firms, contract tools, IP, legal software |
| Sales | CRM, sales engagement, prospecting, commissions, sales ops |
| Marketing | Advertising, content, brand, SEO, events, PR |
| HR | Recruiting, benefits, training, wellness, HRIS |
| Facilities | Office space/rent, utilities, food, maintenance, physical security |
| Support | Customer support ticketing, helpdesk, chat tools |
| Product | Product analytics, UX research, design tools, roadmap tools |

## Recommendation Reference

| Recommendation | Use when |
|---|---|
| Terminate | Vendor is redundant, unused, or a one-time purchase with no recurring value |
| Consolidate | 2+ vendors in this list do the same job — pick one, eliminate the rest |
| Optimize | Vendor is valuable but contract can be renegotiated, usage right-sized, or tier reduced |

## Reuse notes
- This skill works on any vendor CSV regardless of industry
- For non-USD currencies, note the currency in your README and convert at current FX rates for savings estimates
- For lists >500 vendors, increase batch size to 30 or use haiku model to stay within rate limits
- Always run scoring_validation.py before submitting — it catches issues humans miss
