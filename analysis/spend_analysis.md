# Initial Spend Analysis

## Data Source

**Authoritative source:** User-provided CSV export from Google Sheets
**File:** `data/raw_vendors.csv`
**Verified row count:** 387 rows (1 header + **386 vendors**)

*Note: Initial WebFetch retrieved only 383 vendors. User's attention to detail caught the 3-vendor gap and provided the complete dataset.*

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Vendors | **386** |
| Total Annual Spend | $7,244,582 |
| Average Spend per Vendor | $18,769 |
| Median Spend | ~$2,000 |

## Spend Distribution by Tier

| Tier | Spend Range | Vendor Count | Total Spend | % of Total |
|------|-------------|--------------|-------------|------------|
| **Tier 1** | $100K+ | 13 | $5,110,208 | 70.5% |
| **Tier 2** | $25K - $100K | 27 | $1,125,067 | 15.5% |
| **Tier 3** | $5K - $25K | 56 | $612,847 | 8.5% |
| **Tier 4** | <$5K | 294 | $396,460 | 5.5% |

**Key Insight:** 13 vendors (3.3% of total) account for 70.5% of spend. These are the critical focus areas.

---

## Top 20 Vendors by Spend

| Rank | Vendor | Spend | % of Total |
|------|--------|-------|------------|
| 1 | Salesforce Uk Ltd-Uk | $3,117,226 | 43.0% |
| 2 | Navan (Tripactions Inc) | $357,984 | 4.9% |
| 3 | Bdo Llp | $343,081 | 4.7% |
| 4 | Tog Uk Properties Limited | $263,821 | 3.6% |
| 5 | Cloudcrossing Bvba | $208,675 | 2.9% |
| 6 | Zagrebtower D.O.O. | $183,754 | 2.5% |
| 7 | Innovent Spaces Private Limited | $147,348 | 2.0% |
| 8 | Weking D.O.O. | $144,093 | 2.0% |
| 9 | Jensten Insurance Brokers | $142,700 | 2.0% |
| 10 | Gpt Space & Co | $133,507 | 1.8% |
| 11 | Aetna Life And Casualty Ltd | $124,661 | 1.7% |
| 12 | Rsm Uk Corporate Finance Llp | $117,078 | 1.6% |
| 13 | Amazon Web Services Llc | $106,399 | 1.5% |
| 14 | Telefonica Global Services Gmbh | $89,880 | 1.2% |
| 15 | Hr Solution International Gmbh | $80,823 | 1.1% |
| 16 | 4I Advisory Services | $71,860 | 1.0% |
| 17 | Bisley Law Ltd | $67,414 | 0.9% |
| 18 | Infosys | $66,570 | 0.9% |
| 19 | Big Frontier Pty Ltd (Cult Of Monday) | $66,131 | 0.9% |
| 20 | Harmonic Group Limited | $65,418 | 0.9% |

---

## Initial Category Observations

### Software/SaaS (Estimated ~$3.5M)
- **CRM:** Salesforce ($3.1M) - MASSIVE, 43% of total spend
- **Cloud:** AWS ($106K + $5K = $111K), Google ($25K)
- **Productivity:** Microsoft ($10K), Slack ($2K), Trello ($7K), Atlassian ($224)
- **Marketing:** HubSpot ($32K), Semrush ($4K), Cognism ($27K), Uberflip ($26K)
- **HR Tech:** Peakon ($17K), Workato ($16K)
- **Dev Tools:** JetBrains ($4K), GitHub/npm ($4K), Figma ($460)
- **Finance:** Planful ($28K), Sage ($47K), Kimble ($53K)

### Professional Services (Estimated ~$800K)
- **Accounting/Audit:** BDO ($343K), Grant Thornton ($47K), RSM ($117K), PwC ($5K)
- **Legal:** Bisley Law ($67K), multiple law firms
- **Consulting:** Infosys ($67K), various advisory firms

### Real Estate/Facilities (Estimated ~$1M)
- **Office Space:** TOG UK ($264K), WeWork ($64K), Zagrebtower ($184K), Innovent ($147K), multiple coworking
- **Facilities:** CBRE ($8K), Jones Lang LaSalle ($16K)

### Insurance/Benefits (Estimated ~$400K)
- **Insurance:** Jensten ($143K), Aetna ($125K), Bupa ($23K + $12K), Cigna ($13K), Allianz ($6K + $1K)
- **Benefits:** Benefit Systems ($17K), various health insurers

### Travel & Entertainment (Estimated ~$500K)
- **Travel:** Navan/Tripactions ($358K + $58K = $416K), various hotels
- **Catering/Events:** Multiple restaurants, catering services

### Telecom (Estimated ~$120K)
- Telefonica ($90K + $6K), Hrvatski Telekom ($18K), T-Mobile ($3K), Vodafone ($4K)

---

## Immediate Consolidation Opportunities Identified

### 1. Travel Platforms (Potential: $50-100K savings)
- Navan (Tripactions Inc): $357,984
- Navan, Inc: $57,929
- **Total:** $415,913
- **Issue:** Same company, two entries - likely duplicate billing or regional split
- **Action:** Consolidate contracts, negotiate volume discount

### 2. Coworking/Office Space (Potential: $100-200K savings)
- TOG UK Properties: $263,821
- Zagrebtower: $183,754
- Innovent Spaces: $147,348
- Weking: $144,093
- GPT Space: $133,507
- WeWork Singapore: $64,373
- Common Desk: $3,842
- Work Easy Space: $14,913
- **Total:** $955,651
- **Issue:** 8+ coworking vendors across regions
- **Action:** Evaluate space needs, consolidate to fewer providers, negotiate enterprise deals

### 3. Professional Services/Accounting (Potential: $50-100K savings)
- BDO LLP: $343,081
- RSM UK: $117,078
- Grant Thornton: $46,539
- PwC: $4,879
- Crowe Horwath: $4,062
- **Total:** $515,639
- **Issue:** Multiple Big 4/mid-tier accounting firms
- **Action:** Consolidate to primary firm with volume discount

### 4. Insurance Brokers/Providers (Potential: $30-50K savings)
- Jensten: $142,700
- Aetna: $124,661
- Bupa (2 entries): $35,263
- Cigna: $13,249
- Allianz (2 entries): $7,070
- Care Health: $24,045
- **Total:** $346,988
- **Issue:** Multiple insurers across regions
- **Action:** Review coverage overlap, consolidate where possible

### 5. Cloud/Infrastructure (Potential: $15-30K savings)
- AWS (2 entries): $111,552
- Google Ireland: $24,798
- Microsoft: $9,822
- **Total:** $146,172
- **Issue:** Multi-cloud without clear strategy
- **Action:** Optimize cloud spend, review reserved instances

---

## Salesforce Deep Dive Required

**Salesforce UK: $3,117,226 (43% of total vendor spend)**

This is an outlier that requires immediate attention:
- Single vendor = 43% of all vendor spend
- For a company with $7.2M total vendor spend, this is disproportionate
- Likely includes multiple Salesforce products (Sales Cloud, Service Cloud, Marketing Cloud, etc.)

**Questions to investigate:**
1. License utilization - are all seats being used?
2. Product bundling - are we paying for unused modules?
3. Contract terms - when does it renew? What leverage do we have?
4. Alternatives - could some functions be handled by cheaper tools?

**Potential savings:** Even 10% optimization = $311K annually

---

## Department Distribution (Preliminary)

Based on vendor names and spend patterns:

| Department | Est. Spend | % of Total | Vendor Count |
|------------|------------|------------|--------------|
| Sales & Marketing | $3,400,000 | 47% | ~30 |
| Facilities/Real Estate | $1,000,000 | 14% | ~40 |
| Finance | $550,000 | 8% | ~25 |
| HR/People | $450,000 | 6% | ~35 |
| IT/Engineering | $350,000 | 5% | ~50 |
| Legal | $200,000 | 3% | ~20 |
| Travel & Entertainment | $500,000 | 7% | ~80 |
| G&A/Other | $800,000 | 11% | ~110 |

---

## Next Steps

1. **Phase 2:** Classify each vendor with department, description, and recommendation
2. **Priority focus:** Tier 1 vendors (13 vendors, 70% of spend)
3. **Research needed:** Unknown Croatian/regional vendors (D.O.O. = Croatian LLC)
4. **Consolidation mapping:** Group similar vendors for consolidation recommendations
