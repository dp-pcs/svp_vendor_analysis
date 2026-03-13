#!/usr/bin/env python3
"""
Quality check script for vendor analysis results.
"""

import csv
from collections import Counter


def main():
    csv_path = 'output/vendors_analyzed.csv'

    vendors = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}
            vendors.append(row)

    print(f"Total vendors analyzed: {len(vendors)}\n")

    # Count by department
    departments = Counter()
    for v in vendors:
        # Try both with and without trailing space
        dept = v.get('Department ', v.get('Department', ''))
        if dept:
            departments[dept] += 1

    print("VENDORS BY DEPARTMENT:")
    for dept, count in sorted(departments.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dept}: {count}")

    # Count by recommendation
    recommendations = Counter()
    for v in vendors:
        rec = v.get('Suggestions (Consolidate / Terminate / Optimize costs)', '')
        recommendations[rec] += 1

    print("\nVENDORS BY RECOMMENDATION:")
    for rec, count in sorted(recommendations.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rec}: {count}")

    # Check for generic descriptions
    print("\nGENERIC DESCRIPTIONS (< 5 words or contains generic phrases):")
    generic_phrases = [
        'business services', 'provides services', 'various services',
        'consulting', 'professional services', 'solutions provider'
    ]

    flagged = []
    for v in vendors:
        desc = v.get('1-line Description on what the Vendor does', '')
        word_count = len(desc.split())

        is_generic = False
        if word_count < 5:
            is_generic = True

        desc_lower = desc.lower()
        for phrase in generic_phrases:
            if phrase in desc_lower and len(desc_lower.replace(phrase, '').strip()) < 20:
                is_generic = True
                break

        if is_generic:
            flagged.append({
                'vendor': v.get('Vendor Name ', ''),
                'description': desc,
                'words': word_count
            })

    print(f"\nFound {len(flagged)} potentially generic descriptions:\n")
    for item in flagged[:20]:  # Show first 20
        print(f"  - {item['vendor']}")
        print(f"    Description: {item['description']}")
        print(f"    Word count: {item['words']}\n")

    if len(flagged) > 20:
        print(f"  ... and {len(flagged) - 20} more")


if __name__ == '__main__':
    main()
