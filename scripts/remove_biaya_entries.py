import json
import re
from pathlib import Path

def contains_biaya_keywords(text):
    """
    Check if text contains keywords related to biaya/cost.

    Keywords: biaya, harga, tarif, Rp, rupiah, bayar, pembayaran, uang, gratis, diskon, cicilan, semester 1-8, dll
    """
    # Lowercase for case-insensitive matching
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
    ]

    # Check if any keyword exists in text
    for keyword in biaya_keywords:
        if keyword in text_lower:
            return True

    # Check for currency pattern (Rp followed by numbers)
    if re.search(r'rp\s*\d', text_lower):
        return True

    return False

def remove_biaya_entries(input_file, output_file):
    """
    Remove all entries related to biaya from train_pmb_augmented.json
    """
    print(f"Reading: {input_file}")

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total entries before filtering: {len(data)}")

    # Filter out biaya-related entries
    filtered_data = []
    removed_count = 0

    for item in data:
        text = item.get('text', '')

        if not contains_biaya_keywords(text):
            filtered_data.append(item)
        else:
            removed_count += 1

    print(f"Entries removed (biaya-related): {removed_count}")
    print(f"Entries remaining: {len(filtered_data)}")

    # Save filtered data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_file}")

    # Show sample of remaining data
    if len(filtered_data) > 0:
        print(f"\nSample of remaining entries (first 3):")
        for i, item in enumerate(filtered_data[:3], 1):
            text_preview = item['text'].replace('\n', ' ')[:100]
            print(f"\n{i}. {text_preview}...")

    return len(data), removed_count, len(filtered_data)

if __name__ == "__main__":
    # File paths
    input_file = Path("train_pmb_augmented.json")
    output_file = Path("train_pmb_no_biaya.json")

    # Remove biaya entries
    total, removed, remaining = remove_biaya_entries(input_file, output_file)

    print("\n" + "="*80)
    print("FILTERING COMPLETE")
    print("="*80)
    print(f"Original entries:  {total}")
    print(f"Removed (biaya):   {removed} ({removed/total*100:.1f}%)")
    print(f"Remaining:         {remaining} ({remaining/total*100:.1f}%)")
    print("="*80)
