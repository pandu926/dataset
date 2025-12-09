import json
import csv
from pathlib import Path

def json_to_csv(json_file, csv_file):
    """
    Convert JSON Q&A format to CSV with Q and A headers.

    Input: [{"Q": "...", "A": "..."}, ...]
    Output: CSV with columns Q,A
    """
    print(f"Reading: {json_file}")

    # Read JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total entries: {len(data)}")

    # Write to CSV
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Q', 'A'])

        # Write header
        writer.writeheader()

        # Write data
        writer.writerows(data)

    print(f"Saved to: {csv_file}")

    # Show sample
    print(f"\nSample (first 3 rows):")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            if i > 3:
                break
            print(f"\n{i}. Q: {row['Q'][:70]}...")
            print(f"   A: {row['A'][:70]}...")

if __name__ == "__main__":
    # File paths
    json_file = Path("dataset_snk.json")
    csv_file = Path("data/alur.csv")

    # Convert
    json_to_csv(json_file, csv_file)

    print("\n" + "="*80)
    print("CONVERSION COMPLETE")
    print("="*80)
