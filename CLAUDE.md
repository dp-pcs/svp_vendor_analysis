# Vendor Analysis Assessment — Claude Code Project

## Objective
Analyze ~386 vendors for an acquired company acting as VP of Operations. 
Classify each vendor by department, provide a one-line description, and assign a strategic recommendation (Terminate / Consolidate / Optimize).

## Files
- `data/vendors.csv` — Raw vendor data exported from Google Sheets (386 vendors, sorted by spend descending)
- `scripts/` — Processing scripts
- `output/` — Processed results

## Google Sheet
https://docs.google.com/spreadsheets/d/1I9_S_uhLqcFSHvz3RbvwDR_Y1gc5CzHalUVLJqf8Pn8

## Task
1. Read vendors.csv
2. For each vendor, classify:
   - Department: Engineering, G&A, Finance, Sales, Marketing, HR, Legal, IT/Infrastructure, Facilities, Support, Product
   - Description: One concise line describing what the vendor does
   - Recommendation: Terminate | Consolidate | Optimize
3. Write output to output/vendors_analyzed.csv
4. Process in batches of 30 vendors at a time using the Anthropic API

## Departments to use
- Engineering — Dev tools, cloud infra, CI/CD, monitoring, APIs
- IT/Infrastructure — Hardware, networking, security, SaaS platforms
- G&A — Admin, general office, HR software, payroll, compliance
- Finance — Accounting, audit, banking, payments, tax
- Legal — Legal firms, contracts, IP, compliance software
- Sales — CRM, sales tools, prospecting, commissions
- Marketing — Ads, content, brand, SEO, events
- HR — Recruiting, benefits, training, wellness
- Facilities — Office space, utilities, food, maintenance
- Support — Customer support tools, ticketing
- Product — Product analytics, UX research, design tools

## Recommendation criteria
- Terminate: Redundant, unused, or easily replaced with existing tools; very low spend with unclear value
- Consolidate: Multiple vendors doing the same thing (e.g., 3 travel tools, 2 CRMs)
- Optimize: Valuable vendor but likely over-provisioned, or could renegotiate contract terms
