import csv
import json
import re
from pathlib import Path

def contains_biaya_keywords(text):
    """
    Check if text contains keywords related to biaya/cost.
    """
    text_lower = text.lower()

    # Keywords related to biaya
    biaya_keywords = [
        'biaya',
        'harga',
        'tarif',
        'rp',
        'rupiah',
        'bayar',
        'pembayaran',
        'uang',
        'gratis',
        'diskon',
        'cicilan',
        'tagihan',
        'lunas',
        'tunggakan',
        'ukt',
        'spp',
        'dpp',
        'kip-k',
        'kip kuliah',
        'beasiswa',
        'semester 1',
        'semester 2',
        'semester 3',
        'semester 4',
        'semester 5',
        'semester 6',
        'semester 7',
        'semester 8',
        'semester pertama',
        'semester kedua',
        'semester ketiga',
        'semester keempat',
        'semester kelima',
        'semester keenam',
        'semester ketujuh',
        'semester kedelapan',
        'smt 1',
        'smt 2',
        'smt 3',
        'smt 4',
        'smt 5',
        'smt 6',
        'smt 7',
        'smt 8',
        'seluruh semester',
        'total biaya',
        'biaya kuliah',
    ]

    # Check if any keyword exists in text
    for keyword in biaya_keywords:
        if keyword in text_lower:
            return True

    # Check for currency pattern (Rp followed by numbers)
    if re.search(r'rp\s*\d', text_lower):
        return True

    return False

def csv_to_json_remove_biaya(csv_file, output_json):
    """
    Convert CSV to JSON and remove biaya-related entries.

    Input: CSV with Q,A columns
    Output: JSON [{"Q": "...", "A": "..."}, ...]
    """
    print(f"Reading: {csv_file}")

    # Read CSV
    data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig to handle BOM
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    print(f"Total entries in CSV: {len(data)}")

    # Filter out biaya-related entries
    filtered_data = []
    removed_count = 0

    for row in data:
        q = row.get('Q', '')
        a = row.get('A', '')

        # Check both Q and A for biaya keywords
        if not contains_biaya_keywords(q) and not contains_biaya_keywords(a):
            filtered_data.append({
                "Q": q,
                "A": a
            })
        else:
            removed_count += 1

    print(f"Entries removed (biaya-related): {removed_count}")
    print(f"Entries remaining: {len(filtered_data)}")

    # Save to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_json}")

    # Show sample
    if len(filtered_data) > 0:
        print(f"\nSample (first 5 entries):")
        for i, item in enumerate(filtered_data[:5], 1):
            print(f"\n{i}. Q: {item['Q'][:70]}...")
            print(f"   A: {item['A'][:70]}...")

    return len(data), removed_count, len(filtered_data)

if __name__ == "__main__":
    # File paths
    csv_file = Path("dataset_cleaned (7).csv")
    output_json = Path("dataset_cleaned_no_biaya.json")

    # Convert and filter
    total, removed, remaining = csv_to_json_remove_biaya(csv_file, output_json)

    print("\n" + "="*80)
    print("CONVERSION & FILTERING COMPLETE")
    print("="*80)
    print(f"Original entries:  {total}")
    print(f"Removed (biaya):   {removed} ({removed/total*100:.1f}%)")
    print(f"Remaining:         {remaining} ({remaining/total*100:.1f}%)")
    print("="*80)
