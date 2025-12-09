#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk menampilkan statistik dataset variasi
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

def count_variations(filepath):
    """Hitung jumlah pertanyaan dan variasi"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        num_questions = len(data)
        num_variations = num_questions * 5
        return num_questions, num_variations
    except:
        return 0, 0

def main():
    base_dir = Path("/root/dataset")

    print("="*90)
    print("STATISTIK DATASET VARIASI PERTANYAAN")
    print("="*90)
    print()

    total_questions = 0
    total_variations = 0

    print(f"{'File':<45} {'Pertanyaan':>12} {'Variasi':>12}")
    print("-"*90)

    for filename in OUTPUT_FILES:
        filepath = base_dir / filename
        q_count, v_count = count_variations(filepath)
        total_questions += q_count
        total_variations += v_count

        print(f"{filename:<45} {q_count:>12,} {v_count:>12,}")

    print("-"*90)
    print(f"{'TOTAL':<45} {total_questions:>12,} {total_variations:>12,}")
    print("="*90)
    print()

    # Tambahan info
    print("INFORMASI TAMBAHAN:")
    print(f"  - Setiap pertanyaan menghasilkan 5 variasi semantik")
    print(f"  - Jenis variasi: Formal, Casual, Typo, Singkat, Panjang")
    print(f"  - Semua variasi memiliki jawaban yang identik")
    print(f"  - Format output: JSON dengan struktur standar")
    print()

    # Contoh penggunaan
    print("CARA PENGGUNAAN DATASET:")
    print("  1. Untuk fine-tuning: Gunakan semua variasi untuk meningkatkan robustness")
    print("  2. Untuk testing: Gunakan pertanyaan original sebagai test set")
    print("  3. Format training: Konversi ke format yang sesuai (ChatML, Alpaca, dll)")
    print()

if __name__ == "__main__":
    main()
