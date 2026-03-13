#!/usr/bin/env python3
"""
Vendor Analysis Script
Reads vendors.csv and uses Claude API to classify each vendor by department,
description, and recommendation (Terminate/Consolidate/Optimize).
"""

import csv
import json
import os
import sys
import time
from typing import List, Dict, Any
import anthropic


DEPARTMENTS = [
    "Engineering", "IT/Infrastructure", "G&A", "Finance", "Legal",
    "Sales", "Marketing", "HR", "Facilities", "Support", "Product"
]

BATCH_SIZE = 25
MODEL = "claude-sonnet-4-5"


def read_vendors(csv_path: str) -> List[Dict[str, str]]:
    """Read vendors from CSV file."""
    vendors = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Strip whitespace from column names
            row = {k.strip(): v.strip() for k, v in row.items()}
            vendors.append({
                'vendor_name': row.get('Vendor Name ', ''),
                'cost': row.get('Last 12 months Cost (USD)', '')
            })
    return vendors


def create_analysis_prompt(vendors: List[Dict[str, str]]) -> str:
    """Create the prompt for Claude to analyze vendors."""

    vendor_list = []
    for i, v in enumerate(vendors, 1):
        vendor_list.append(f"{i}. {v['vendor_name']} (Annual spend: {v['cost']})")

    vendor_text = "\n".join(vendor_list)

    prompt = f"""You are a VP of Operations analyzing vendors for an acquired company. For each vendor below, provide:

1. **department**: Choose exactly one from: {', '.join(DEPARTMENTS)}
2. **description**: One tight, specific sentence describing what the vendor does. Be concrete (e.g., "Corporate travel booking and expense management platform" not "business services").
3. **recommendation**: Exactly one of: Terminate | Consolidate | Optimize

Recommendation criteria:
- **Terminate**: Clearly redundant, one-off spend <$500, clearly unused (food vendors, single purchases, obscure local services, duplicate tools)
- **Consolidate**: Same function as other vendors you see in the list (multiple office spaces, travel tools, legal firms, insurance providers)
- **Optimize**: Core vendor that's valuable but likely over-provisioned or has renegotiable contract terms (major SaaS platforms, large annual contracts)

VENDORS TO ANALYZE:
{vendor_text}

Return a JSON array with this exact structure:
[
  {{
    "vendor_name": "Exact vendor name from list",
    "department": "Department",
    "description": "Specific one-line description",
    "recommendation": "Terminate|Consolidate|Optimize"
  }},
  ...
]

Return ONLY the JSON array, no other text."""

    return prompt


def analyze_batch(client: anthropic.Anthropic, vendors: List[Dict[str, str]],
                  batch_num: int, total_batches: int) -> List[Dict[str, str]]:
    """Analyze a batch of vendors using Claude API."""

    print(f"Processing batch {batch_num}/{total_batches} ({len(vendors)} vendors)...")

    prompt = create_analysis_prompt(vendors)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = message.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])

            # Parse JSON
            results = json.loads(response_text)

            # Validate results
            if not isinstance(results, list):
                raise ValueError("Response is not a JSON array")

            if len(results) != len(vendors):
                print(f"  Warning: Expected {len(vendors)} results, got {len(results)}")

            # Validate each result has required fields
            for result in results:
                if not all(k in result for k in ['vendor_name', 'department', 'description', 'recommendation']):
                    raise ValueError(f"Missing required fields in result: {result}")

                if result['recommendation'] not in ['Terminate', 'Consolidate', 'Optimize']:
                    print(f"  Warning: Invalid recommendation '{result['recommendation']}' for {result['vendor_name']}")
                    # Fix it
                    if 'terminate' in result['recommendation'].lower():
                        result['recommendation'] = 'Terminate'
                    elif 'consolidate' in result['recommendation'].lower():
                        result['recommendation'] = 'Consolidate'
                    else:
                        result['recommendation'] = 'Optimize'

            print(f"  ✓ Batch {batch_num} complete")
            return results

        except json.JSONDecodeError as e:
            print(f"  ✗ JSON decode error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"  Failed to parse response after {max_retries} attempts")
                print(f"  Response: {response_text[:500]}")
                raise

        except Exception as e:
            print(f"  ✗ Error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise


def write_results(output_path: str, results: List[Dict[str, str]]):
    """Write results to CSV."""

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Vendor Name ', 'Department ', 'Last 12 months Cost (USD)',
                     '1-line Description on what the Vendor does',
                     'Suggestions (Consolidate / Terminate / Optimize costs)']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow({
                'Vendor Name ': result['vendor_name'],
                'Department ': result['department'],
                'Last 12 months Cost (USD)': result['cost'],
                '1-line Description on what the Vendor does': result['description'],
                'Suggestions (Consolidate / Terminate / Optimize costs)': result['recommendation']
            })


def main():
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)

    # Read vendors
    csv_path = 'data/vendors.csv'
    print(f"Reading vendors from {csv_path}...")
    vendors = read_vendors(csv_path)
    print(f"Found {len(vendors)} vendors")

    # Process in batches
    all_results = []
    total_batches = (len(vendors) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(vendors), BATCH_SIZE):
        batch = vendors[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1

        try:
            results = analyze_batch(client, batch, batch_num, total_batches)

            # Merge cost back into results
            for j, result in enumerate(results):
                result['cost'] = batch[j]['cost']

            all_results.extend(results)

            # Small delay between batches to be nice to the API
            if i + BATCH_SIZE < len(vendors):
                time.sleep(1)

        except Exception as e:
            print(f"Fatal error processing batch {batch_num}: {e}")
            print("Partial results will be saved.")
            break

    # Write results
    output_path = 'output/vendors_analyzed.csv'
    print(f"\nWriting {len(all_results)} results to {output_path}...")
    write_results(output_path, all_results)

    print(f"✓ Complete! Processed {len(all_results)}/{len(vendors)} vendors")

    if len(all_results) < len(vendors):
        print(f"Warning: Only {len(all_results)} vendors were processed successfully")
        sys.exit(1)


if __name__ == '__main__':
    main()
