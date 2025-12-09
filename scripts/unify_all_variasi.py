#!/usr/bin/env python3
"""
Script untuk menggabungkan semua file variasi menjadi satu file flat
Format output: [{"Q": "...", "A": "..."}, ...]
"""

import json
import os

# File yang akan digabungkan
# Untuk biaya: hanya yang ada "clean" nya
FILES_TO_UNIFY = [
    "dataset-biaya_clean_variasi.json",
    "dataset-biaya2_clean_variasi.json",
    "dataset_umum_clean_variasi.json",
    "dataset-beasiswa_clean_variasi.json",
    "dataset_pofil_variasi.json",
    "dataset-podi_variasi.json",
    "dataset_oot_clean_variasi.json",
    "dataset_snk_variasi.json",
    "dataset-fasilitas_clean_variasi.json",
    "dataset-alur_variasi.json"
]

def main():
    base_dir = "/root/dataset"
    all_qa_pairs = []

    print("="*70)
    print("UNIFIKASI SEMUA FILE VARIASI")
    print("="*70)

    for filename in FILES_TO_UNIFY:
        filepath = os.path.join(base_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠️  File tidak ditemukan: {filename}")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract semua variasi
        count = 0
        for item in data:
            # Ambil semua 5 variasi
            for variation in item['variations']:
                all_qa_pairs.append({
                    "Q": variation['Q'],
                    "A": variation['A']
                })
                count += 1

        print(f"✓ {filename:45s} : {count:5d} pairs")

    # Save ke file output
    output_path = os.path.join(base_dir, "dataset_all_variasi_unified.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_qa_pairs, f, ensure_ascii=False, indent=2)

    print("="*70)
    print(f"✓ TOTAL Q&A PAIRS: {len(all_qa_pairs)}")
    print(f"✓ OUTPUT: {output_path}")
    print("="*70)

if __name__ == "__main__":
    main()
