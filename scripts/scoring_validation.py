#!/usr/bin/env python3
"""
Scoring & Validation Framework
Maps directly to the published evaluation criteria for the Vendor Analysis Assessment.

Evaluation criteria (from assessment instructions):
1. Department accuracy — vendors categorized appropriately
2. Description quality — concise, accurate, specific (not "business services provider")
3. Recommendation quality — realistic, strategic, with risk awareness
4. Top 3 opportunities — specific, plausible, financially justified
5. Methodology clarity — tools used, prompts documented
6. Quality check evidence — documented what QA looked for
7. Executive memo quality — formatted, grammatically correct, savings move the needle for $1B business
8. Project organization — inputs, outputs, scripts, README

Scoring: each criterion scored 0-10. Total /80. Report card printed to output/scoring_report.md
"""

import csv
import json
import re
import os
from collections import Counter
from typing import List, Dict, Tuple

# ─── LOAD DATA ───────────────────────────────────────────────────────────────

def load_vendors(path: str) -> List[Dict]:
    with open(path, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    # Normalize keys
    normalized = []
    for r in rows:
        normalized.append({k.strip(): v.strip() for k, v in r.items()})
    return normalized

def parse_cost(cost_str: str) -> float:
    """Parse '$1,234,567' to float."""
    try:
        return float(re.sub(r'[^\d.]', '', cost_str))
    except:
        return 0.0

# ─── CRITERION 1: DEPARTMENT ACCURACY ────────────────────────────────────────

VALID_DEPARTMENTS = {
    "Engineering", "IT/Infrastructure", "G&A", "Finance", "Legal",
    "Sales", "Marketing", "HR", "Facilities", "Support", "Product"
}

KNOWN_MAPPINGS = {
    # High-confidence vendor→department spot checks
    "salesforce": "Sales",
    "navan": "G&A",
    "bdo": "Finance",
    "github": "Engineering",
    "aws": "Engineering",
    "google": "Engineering",
    "workday": "HR",
    "zendesk": "Support",
    "hubspot": "Marketing",
    "slack": "IT/Infrastructure",
    "zoom": "IT/Infrastructure",
    "docusign": "Legal",
}

def score_departments(vendors: List[Dict]) -> Tuple[float, List[str]]:
    issues = []
    dept_key = next((k for k in vendors[0] if 'department' in k.lower()), None)
    if not dept_key:
        return 0, ["Could not find Department column"]

    depts = [v[dept_key] for v in vendors]
    dept_counts = Counter(depts)

    # Check 1: All values are valid department names
    invalid = [d for d in set(depts) if d not in VALID_DEPARTMENTS]
    if invalid:
        issues.append(f"Invalid department values: {invalid}")

    # Check 2: Distribution sanity — no single dept > 40% of total
    for dept, count in dept_counts.most_common(3):
        pct = count / len(vendors) * 100
        if pct > 40:
            issues.append(f"WARNING: {dept} is {pct:.0f}% of all vendors — likely over-assigned")

    # Check 3: Minimum coverage — at least 7 distinct departments used
    if len(dept_counts) < 7:
        issues.append(f"Only {len(dept_counts)} departments used — insufficient coverage")

    # Check 4: Spot-check known vendors
    name_key = next((k for k in vendors[0] if 'vendor' in k.lower()), None)
    mismatches = []
    for v in vendors:
        name_lower = v.get(name_key, '').lower()
        assigned = v[dept_key]
        for keyword, expected in KNOWN_MAPPINGS.items():
            if keyword in name_lower and assigned != expected:
                mismatches.append(f"{v[name_key]}: assigned '{assigned}', expected '{expected}'")
    if mismatches:
        issues.append(f"Spot-check mismatches ({len(mismatches)}): {mismatches[:5]}")

    # Score
    score = 10
    score -= len(invalid) * 2
    score -= len(mismatches) * 0.5
    if len(dept_counts) < 7: score -= 3
    score = max(0, min(10, score))

    return score, issues

# ─── CRITERION 2: DESCRIPTION QUALITY ────────────────────────────────────────

GENERIC_PHRASES = [
    "business services", "provides services", "various services",
    "service provider", "technology company", "software company",
    "consulting firm", "professional services", "it services",
    "technology services", "business solutions"
]

def score_descriptions(vendors: List[Dict]) -> Tuple[float, List[str]]:
    issues = []
    desc_key = next((k for k in vendors[0] if 'description' in k.lower() or '1-line' in k.lower()), None)
    if not desc_key:
        return 0, ["Could not find Description column"]

    descs = [v[desc_key] for v in vendors]
    name_key = next((k for k in vendors[0] if 'vendor' in k.lower()), None)

    # Check 1: Length — under 4 words is too short, over 25 is too long
    too_short = [(vendors[i][name_key], descs[i]) for i, d in enumerate(descs) if len(d.split()) < 5]
    too_long  = [(vendors[i][name_key], descs[i]) for i, d in enumerate(descs) if len(d.split()) > 25]
    if too_short:
        issues.append(f"Too short (<5 words): {len(too_short)} vendors — {too_short[:3]}")
    if too_long:
        issues.append(f"Too long (>25 words): {len(too_long)} vendors — {[x[0] for x in too_long[:3]]}")

    # Check 2: Generic phrase detection
    generic_hits = []
    for v, d in zip(vendors, descs):
        for phrase in GENERIC_PHRASES:
            if phrase in d.lower():
                generic_hits.append((v[name_key], d))
                break
    if generic_hits:
        issues.append(f"Generic descriptions ({len(generic_hits)}): {[x[0] for x in generic_hits[:5]]}")

    # Check 3: Duplicate descriptions (copy-paste indicator)
    desc_counts = Counter(descs)
    duplicates = [(d, c) for d, c in desc_counts.most_common() if c > 3]
    if duplicates:
        issues.append(f"Duplicate descriptions (>3 uses): {duplicates[:3]}")

    # Check 4: Average word count
    avg_words = sum(len(d.split()) for d in descs) / len(descs)
    if avg_words < 7:
        issues.append(f"Average description length is only {avg_words:.1f} words — may be too terse")

    score = 10
    score -= len(too_short) * 0.1
    score -= len(generic_hits) * 0.5
    score -= len(duplicates) * 1
    if avg_words < 7: score -= 2
    score = max(0, min(10, score))

    return score, issues

# ─── CRITERION 3: RECOMMENDATION QUALITY ─────────────────────────────────────

def score_recommendations(vendors: List[Dict]) -> Tuple[float, List[str]]:
    issues = []
    rec_key = next((k for k in vendors[0] if 'suggest' in k.lower() or 'recommendation' in k.lower()), None)
    cost_key = next((k for k in vendors[0] if 'cost' in k.lower()), None)
    name_key = next((k for k in vendors[0] if 'vendor' in k.lower()), None)

    if not rec_key:
        return 0, ["Could not find Recommendation column"]

    recs = [v[rec_key] for v in vendors]
    rec_counts = Counter(recs)
    total = len(vendors)

    # Check 1: Valid values only
    valid_recs = {"Terminate", "Consolidate", "Optimize"}
    invalid = [r for r in set(recs) if r not in valid_recs]
    if invalid:
        issues.append(f"Invalid recommendation values: {invalid}")

    # Check 2: Distribution — each category should be 15-60% of total
    for rec, count in rec_counts.items():
        pct = count / total * 100
        if pct < 10:
            issues.append(f"WARNING: {rec} is only {pct:.0f}% — may be under-used")
        if pct > 65:
            issues.append(f"WARNING: {rec} is {pct:.0f}% — likely over-used, lacks differentiation")

    # Check 3: High-spend vendors should not be Terminate
    if cost_key:
        high_spend_terminates = [
            v for v in vendors
            if v[rec_key] == 'Terminate' and parse_cost(v.get(cost_key, '0')) > 50000
        ]
        if high_spend_terminates:
            issues.append(f"High-spend vendors marked Terminate (>$50K): "
                         f"{[(v[name_key], v.get(cost_key,'')) for v in high_spend_terminates[:5]]}")

    # Check 4: Very low spend (<$100) should mostly be Terminate
    if cost_key:
        tiny_spend_keep = [
            v for v in vendors
            if parse_cost(v.get(cost_key, '0')) < 100 and v[rec_key] != 'Terminate'
        ]
        if tiny_spend_keep:
            issues.append(f"Vendors with <$100 spend NOT marked Terminate: "
                         f"{[v[name_key] for v in tiny_spend_keep[:5]]}")

    score = 10
    score -= len(invalid) * 2
    score -= len([r for r,c in rec_counts.items() if c/total > 0.65]) * 2
    score -= min(3, len(high_spend_terminates) * 0.5) if cost_key else 0
    score = max(0, min(10, score))

    return score, issues

# ─── CRITERION 4: FINANCIAL DEFENSIBILITY ────────────────────────────────────

def score_financial_defensibility(vendors: List[Dict]) -> Tuple[float, List[str]]:
    """
    Checks that the data supports financially defensible Top 3 opportunities.
    Computes total spend, identifies consolidation clusters, terminate savings.
    """
    issues = []
    cost_key = next((k for k in vendors[0] if 'cost' in k.lower()), None)
    rec_key = next((k for k in vendors[0] if 'suggest' in k.lower() or 'recommendation' in k.lower()), None)
    dept_key = next((k for k in vendors[0] if 'department' in k.lower()), None)

    if not cost_key:
        return 5, ["No cost column found — financial checks skipped"]

    costs = [parse_cost(v.get(cost_key, '0')) for v in vendors]
    total_spend = sum(costs)

    # Terminate savings
    terminate_savings = sum(
        parse_cost(v.get(cost_key, '0'))
        for v in vendors
        if v.get(rec_key, '') == 'Terminate'
    )

    # Consolidate savings (assume 30% savings on consolidated vendor spend)
    consolidate_spend = sum(
        parse_cost(v.get(cost_key, '0'))
        for v in vendors
        if v.get(rec_key, '') == 'Consolidate'
    )
    consolidate_savings_estimate = consolidate_spend * 0.30

    # Optimize savings (assume 20% savings)
    optimize_spend = sum(
        parse_cost(v.get(cost_key, '0'))
        for v in vendors
        if v.get(rec_key, '') == 'Optimize'
    )
    optimize_savings_estimate = optimize_spend * 0.20

    total_potential_savings = terminate_savings + consolidate_savings_estimate + optimize_savings_estimate
    savings_pct = (total_potential_savings / total_spend * 100) if total_spend > 0 else 0

    # For a $1B business, savings should be meaningful (>$500K min to "move the needle")
    if total_potential_savings < 500_000:
        issues.append(f"Total potential savings ${total_potential_savings:,.0f} may not move the needle for a $1B business")

    issues.append(f"FINANCIAL SUMMARY:")
    issues.append(f"  Total vendor spend: ${total_spend:,.0f}")
    issues.append(f"  Terminate savings: ${terminate_savings:,.0f}")
    issues.append(f"  Consolidate savings (est. 30%): ${consolidate_savings_estimate:,.0f}")
    issues.append(f"  Optimize savings (est. 20%): ${optimize_savings_estimate:,.0f}")
    issues.append(f"  Total potential savings: ${total_potential_savings:,.0f} ({savings_pct:.1f}% of spend)")

    score = 10 if total_potential_savings > 1_000_000 else (7 if total_potential_savings > 500_000 else 4)

    return score, issues

# ─── CRITERION 5: PROJECT ORGANIZATION ───────────────────────────────────────

def score_project_organization(base_path: str) -> Tuple[float, List[str]]:
    issues = []
    required_files = {
        "README.md": "Project documentation",
        "data/vendors.csv": "Raw input data",
        "output/vendors_analyzed.csv": "Classified vendor output",
        "scripts/analyze_vendors.py": "Main analysis script",
        "CLAUDE.md": "Claude Code spec/planning document",
    }
    optional_files = {
        "scripts/quality_check.py": "Quality check script",
        "scripts/scoring_validation.py": "Scoring validation (this file)",
        "output/scoring_report.md": "Scoring report",
    }

    score = 10
    for path, desc in required_files.items():
        full_path = os.path.join(base_path, path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            issues.append(f"✅ {path} ({size:,} bytes) — {desc}")
        else:
            issues.append(f"❌ MISSING: {path} — {desc}")
            score -= 2

    for path, desc in optional_files.items():
        full_path = os.path.join(base_path, path)
        status = "✅" if os.path.exists(full_path) else "⬜"
        issues.append(f"{status} {path} — {desc}")

    return max(0, score), issues

# ─── CRITERION 6: DESCRIPTION SPECIFICITY DEEP CHECK ─────────────────────────

def score_specificity(vendors: List[Dict]) -> Tuple[float, List[str]]:
    """Checks that descriptions are specific to the vendor, not just the category."""
    issues = []
    desc_key = next((k for k in vendors[0] if 'description' in k.lower() or '1-line' in k.lower()), None)
    name_key = next((k for k in vendors[0] if 'vendor' in k.lower()), None)

    if not desc_key:
        return 0, ["No description column found"]

    # Check that top-10 spend vendors have specific, detailed descriptions
    cost_key = next((k for k in vendors[0] if 'cost' in k.lower()), None)
    if cost_key:
        sorted_vendors = sorted(vendors, key=lambda v: parse_cost(v.get(cost_key, '0')), reverse=True)
        top10 = sorted_vendors[:10]
        vague_top = [(v[name_key], v[desc_key]) for v in top10 if len(v[desc_key].split()) < 8]
        if vague_top:
            issues.append(f"Top-10 spend vendors with short descriptions (<8 words): {vague_top}")
        else:
            issues.append(f"✅ All top-10 spend vendors have substantive descriptions")

    # Check uniqueness ratio — descriptions should mostly be unique
    descs = [v[desc_key] for v in vendors]
    unique_ratio = len(set(descs)) / len(descs)
    issues.append(f"Description uniqueness: {unique_ratio:.1%} ({len(set(descs))}/{len(descs)} unique)")
    if unique_ratio < 0.85:
        issues.append("WARNING: <85% unique descriptions — possible template reuse")

    score = 10 if unique_ratio > 0.90 else (7 if unique_ratio > 0.80 else 4)
    if vague_top if cost_key else False:
        score -= 2

    return max(0, min(10, score)), issues

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vendors_path = os.path.join(base_path, 'output', 'vendors_analyzed.csv')

    print("=" * 60)
    print("VENDOR ANALYSIS — SCORING VALIDATION REPORT")
    print("=" * 60)

    if not os.path.exists(vendors_path):
        print(f"ERROR: {vendors_path} not found. Run analyze_vendors.py first.")
        return

    vendors = load_vendors(vendors_path)
    print(f"Loaded {len(vendors)} vendors\n")

    results = {}
    total_score = 0
    max_score = 0

    criteria = [
        ("1. Department Accuracy",       lambda: score_departments(vendors)),
        ("2. Description Quality",        lambda: score_descriptions(vendors)),
        ("3. Recommendation Quality",     lambda: score_recommendations(vendors)),
        ("4. Financial Defensibility",    lambda: score_financial_defensibility(vendors)),
        ("5. Project Organization",       lambda: score_project_organization(base_path)),
        ("6. Description Specificity",    lambda: score_specificity(vendors)),
    ]

    report_lines = ["# Scoring Validation Report\n",
                    f"**Vendors analyzed:** {len(vendors)}\n",
                    f"**Output file:** {vendors_path}\n\n",
                    "---\n"]

    for name, fn in criteria:
        score, issues = fn()
        results[name] = (score, issues)
        total_score += score
        max_score += 10

        status = "✅" if score >= 8 else ("⚠️" if score >= 6 else "❌")
        print(f"{status} {name}: {score:.1f}/10")
        for issue in issues:
            print(f"   {issue}")
        print()

        report_lines.append(f"## {name}: {score:.1f}/10 {status}\n")
        for issue in issues:
            report_lines.append(f"- {issue}\n")
        report_lines.append("\n")

    # Overall
    overall_pct = total_score / max_score * 100
    grade = "A" if overall_pct >= 90 else ("B" if overall_pct >= 80 else ("C" if overall_pct >= 70 else "D"))

    summary = f"\n{'='*60}\nOVERALL SCORE: {total_score:.1f}/{max_score} ({overall_pct:.0f}%) — Grade: {grade}\n{'='*60}\n"
    print(summary)

    report_lines.append("---\n")
    report_lines.append(f"## Overall Score\n**{total_score:.1f}/{max_score} ({overall_pct:.0f}%) — Grade: {grade}**\n")

    # Write report
    report_path = os.path.join(base_path, 'output', 'scoring_report.md')
    with open(report_path, 'w') as f:
        f.writelines(report_lines)
    print(f"Full report written to: {report_path}")


if __name__ == '__main__':
    main()
