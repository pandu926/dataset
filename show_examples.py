#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Baca file variasi
with open('/root/dataset/dataset_biaya_variasi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Tampilkan 3 contoh pertama
print('='*80)
print('CONTOH OUTPUT VARIASI PERTANYAAN')
print('='*80)
print()

variation_types = ['FORMAL', 'CASUAL', 'TYPO', 'SINGKAT', 'PANJANG']

for idx, item in enumerate(data[:3], 1):
    print('='*80)
    print(f'CONTOH {idx}')
    print('='*80)
    print(f'PERTANYAAN ASLI:')
    print(f'  "{item["original_Q"]}"')
    print()
    print(f'VARIASI YANG DIHASILKAN:')
    print()

    for var_idx, variation in enumerate(item['variations'], 1):
        var_type = variation_types[var_idx-1]
        print(f'{var_idx}. VARIASI {var_type}:')
        print(f'   Q: "{variation["Q"]}"')
        print(f'   A: "{variation["A"]}"')
        print()

    print()
