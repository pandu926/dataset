import json
import csv
from pathlib import Path

def csv_to_json(csv_file, json_file):
    """
    Convert CSV Q&A format to JSON.

    Input: CSV with columns Q,A
    Output: [{"Q": "...", "A": "..."}, ...]
    """
    print(f"Reading: {csv_file}")

    # Read CSV file
    data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'Q': row['Q'],
                'A': row['A']
            })

    print(f"Total entries: {len(data)}")

    # Write to JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {json_file}")

    # Show sample
    print(f"\nSample (first 3 rows):")
    for i, item in enumerate(data[:3], 1):
        print(f"\n{i}. Q: {item['Q'][:70]}...")
        print(f"   A: {item['A'][:70]}...")

if __name__ == "__main__":
    # File paths
    csv_file = Path("dataset_cleaned_filtered.csv")
    json_file = Path("dataset_cleaned_filtered.json")

    # Convert
    csv_to_json(csv_file, json_file)

    print("\n" + "="*80)
    print("CONVERSION COMPLETE")
    print("="*80)
