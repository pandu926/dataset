#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk konversi dataset variasi ke format flat (siap fine-tuning)
Output: Format standar Q&A seperti input original
"""

import json
from pathlib import Path

OUTPUT_FILES = [
    "dataset_biaya_variasi.json",
    "dataset-biaya2_clean_variasi.json",
    "dataset_umum_clean_variasi.json",
    "dataset-beasiswa_clean_variasi.json",
    "dataset_pofil_variasi.json",
    "dataset-podi_variasi.json",
    "dataset_oot_clean_variasi.json",
    "dataset-biaya_clean_variasi.json",
    "dataset_snk_variasi.json",
    "dataset-fasilitas_clean_variasi.json",
    "dataset-alur_variasi.json"
]

def convert_to_flat(input_file, output_file):
    """Konversi format variasi ke flat Q&A"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    flat_data = []

    for item in data:
        # Tambahkan pertanyaan original
        # flat_data.append({
        #     "Q": item["original_Q"],
        #     "A": item["variations"][0]["A"]  # Ambil jawaban dari variasi pertama
        # })

        # Tambahkan semua variasi
        for variation in item["variations"]:
            flat_data.append({
                "Q": variation["Q"],
                "A": variation["A"]
            })

    # Simpan
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(flat_data, f, ensure_ascii=False, indent=2)

    return len(flat_data)

def main():
    base_dir = Path("/root/dataset")

    print("="*90)
    print("KONVERSI DATASET KE FORMAT FLAT (SIAP FINE-TUNING)")
    print("="*90)
    print()

    all_data = []
    total_entries = 0

    for filename in OUTPUT_FILES:
        input_path = base_dir / filename

        # Nama output
        flat_filename = filename.replace('_variasi.json', '_flat.json')
        output_path = base_dir / flat_filename

        # Konversi
        count = convert_to_flat(input_path, output_path)
        total_entries += count

        # Juga tambahkan ke combined dataset
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)

        print(f"✓ {filename:<45} → {count:>6} entries")

    # Simpan combined dataset
    combined_path = base_dir / "dataset_combined_all_variations.json"
    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("-"*90)
    print(f"✓ {'COMBINED DATASET':<45} → {len(all_data):>6} entries")
    print("="*90)
    print()

    print(f"✅ File combined tersimpan di: {combined_path}")
    print(f"✅ Total {total_entries:,} pasangan Q&A siap untuk fine-tuning")
    print()

    # Info ukuran file
    file_size = combined_path.stat().st_size / (1024 * 1024)  # MB
    print(f"📊 Ukuran file combined: {file_size:.2f} MB")
    print()

if __name__ == "__main__":
    main()
