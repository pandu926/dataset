#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Baca file variasi
with open('/root/dataset/dataset_biaya_variasi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*90)
print('CONTOH OUTPUT VARIASI PERTANYAAN - IMPROVED VERSION')
print('='*90)
print()

variation_types = ['FORMAL', 'CASUAL', 'TYPO', 'SINGKAT', 'PANJANG']

# Tampilkan 4 contoh untuk menunjukkan variasi
for idx, item in enumerate(data[:4], 1):
    print('='*90)
    print(f'CONTOH {idx}')
    print('='*90)
    print(f'PERTANYAAN ASLI:')
    print(f'  "{item["original_Q"]}"')
    print()
    print(f'5 VARIASI SEMANTIK:')
    print('-'*90)

    for var_idx, variation in enumerate(item['variations'], 1):
        var_type = variation_types[var_idx-1]
        print(f'\n{var_idx}. [{var_type}]')
        print(f'   Q: "{variation["Q"]}"')
        print(f'   A: "{variation["A"]}"')

    print()
    print()
