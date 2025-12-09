#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk Generate Variasi Pertanyaan Dataset Q&A - VERSION IMPROVED
Menghasilkan 5 variasi semantik berkualitas tinggi untuk setiap pertanyaan
"""

import json
import os
import random
import re
from pathlib import Path

# Daftar file input
INPUT_FILES = [
    "dataset_biaya.json",
    "dataset-biaya2_clean.json",
    "dataset_umum_clean.json",
    "dataset-beasiswa_clean.json",
    "dataset_pofil.json",
    "dataset-podi.json",
    "dataset_oot_clean.json",
    "dataset-biaya_clean.json",
    "dataset_snk.json",
    "dataset-fasilitas_clean.json",
    "dataset-alur.json"
]

# Mapping kata untuk variasi casual
CASUAL_MAP = {
    'berapa': 'brp',
    'bagaimana': 'gmn',
    'kenapa': 'knp',
    'semester': 'smt',
    'program studi': 'prodi',
    'universitas': 'univ',
    'pendaftaran': 'daftar',
    'biaya': 'harga',
    'untuk': 'buat',
}

# Typo patterns yang realistis
TYPO_PATTERNS = [
    ('berapa', 'berapaa'),
    ('berapa', 'brapa'),
    ('biaya', 'biya'),
    ('semester', 'semster'),
    ('kuliah', 'kulah'),
    ('pendidikan', 'pendidkan'),
    ('untuk', 'untk'),
    ('bagaimana', 'bgaimana'),
    ('total', 'totl'),
    ('apakah', 'apkah'),
    ('seluruh', 'sluruh'),
    ('pertama', 'prtama'),
]

def apply_random_typo(text):
    """Terapkan typo yang realistis"""
    text_lower = text.lower()
    applicable_typos = [(orig, typo) for orig, typo in TYPO_PATTERNS if orig in text_lower]

    if applicable_typos:
        # Pilih 1 typo saja untuk realistis
        original, typo = random.choice(applicable_typos)
        # Case-insensitive replacement
        pattern = re.compile(re.escape(original), re.IGNORECASE)
        text = pattern.sub(typo, text, count=1)

    return text

def create_formal_variation(question):
    """Variasi 1: Formal/Akademik"""
    q_lower = question.lower().strip('?').strip()

    formal_templates = [
        f"Mohon informasi mengenai {q_lower}.",
        f"Saya ingin mengetahui {q_lower}.",
        f"Dapatkah dijelaskan {q_lower}?",
        f"Saya memerlukan keterangan tentang {q_lower}.",
        f"Bisakah diberikan informasi terkait {q_lower}?",
    ]

    # Pilih template yang paling cocok
    if question.lower().startswith('berapa'):
        q_modified = q_lower.replace('berapa ', '')
        return f"Mohon informasi mengenai {q_modified}."
    elif question.lower().startswith('apa'):
        q_modified = q_lower.replace('apa ', '')
        return f"Saya ingin mengetahui {q_modified}."
    elif question.lower().startswith('apakah'):
        return f"Dapatkah dijelaskan {q_lower}?"

    return random.choice(formal_templates)

def create_casual_variation(question):
    """Variasi 2: Casual/Santai dengan singkatan"""
    q = question.lower().strip('?').strip()

    # Apply casual mappings
    for formal, casual in CASUAL_MAP.items():
        if formal in q:
            q = q.replace(formal, casual)

    # Casual endings
    casual_endings = ['dong', 'ya', 'kak', 'min', 'nih', 'gan']
    ending = random.choice(casual_endings)

    # Hapus kata formal
    q = q.replace('mohon ', '').replace('tolong ', '').replace('saya ', '')

    return f"{q} {ending}?"

def create_typo_variation(question):
    """Variasi 3: Dengan typo realistis"""
    return apply_random_typo(question)

def create_short_variation(question):
    """Variasi 4: Versi singkat/padat"""
    q = question.strip('?').strip()

    # Hapus kata tidak esensial
    remove_words = ['mohon', 'tolong', 'bisa', 'dapatkah', 'saya ingin', 'bagaimana']
    for word in remove_words:
        q = re.sub(r'\b' + word + r'\b', '', q, flags=re.IGNORECASE)

    # Simplifikasi awalan pertanyaan
    q = re.sub(r'^apakah\s+', '', q, flags=re.IGNORECASE)
    q = re.sub(r'^berapa\s+', '', q, flags=re.IGNORECASE)
    q = re.sub(r'^apa\s+', '', q, flags=re.IGNORECASE)

    # Clean up multiple spaces
    q = re.sub(r'\s+', ' ', q).strip()

    return f"{q}?"

def create_long_variation(question):
    """Variasi 5: Versi panjang/deskriptif"""
    q_lower = question.lower().strip('?').strip()

    long_templates = [
        f"Selamat siang, saya ingin bertanya secara detail mengenai {q_lower}. Mohon penjelasannya.",
        f"Saya sedang mencari informasi lengkap tentang {q_lower}, bisakah dijelaskan?",
        f"Mohon bantuannya untuk menjelaskan secara rinci mengenai {q_lower} untuk keperluan pendaftaran saya.",
        f"Sebagai calon mahasiswa, saya perlu memahami lebih lanjut tentang {q_lower}. Terima kasih sebelumnya.",
        f"Untuk kelengkapan data saya, mohon dijelaskan dengan detail mengenai {q_lower}. Terima kasih.",
        f"Permisi, saya ingin menanyakan informasi yang cukup spesifik tentang {q_lower}. Mohon dibantu.",
    ]

    return random.choice(long_templates)

def generate_variations(question, answer):
    """
    Generate 5 variasi pertanyaan dengan jawaban yang sama
    """
    variations = []

    # Variasi 1: Formal/Akademik
    variations.append({
        "Q": create_formal_variation(question),
        "A": answer
    })

    # Variasi 2: Casual/Santai
    variations.append({
        "Q": create_casual_variation(question),
        "A": answer
    })

    # Variasi 3: Dengan typo
    variations.append({
        "Q": create_typo_variation(question),
        "A": answer
    })

    # Variasi 4: Singkat/padat
    variations.append({
        "Q": create_short_variation(question),
        "A": answer
    })

    # Variasi 5: Panjang/deskriptif
    variations.append({
        "Q": create_long_variation(question),
        "A": answer
    })

    return variations

def process_file(input_path, output_path):
    """Proses satu file JSON dan generate variasi"""
    print(f"📁 Memproses: {input_path}")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        results = []

        # Handle dua format
        for idx, item in enumerate(data):
            if "Q" in item and "A" in item:
                question = item["Q"]
                answer = item["A"]
            elif "instruction" in item and "response" in item:
                question = item["instruction"]
                answer = item["response"]
            else:
                print(f"⚠️  Item {idx} tidak memiliki format yang dikenali, dilewati")
                continue

            # Generate 5 variasi
            variations = generate_variations(question, answer)

            results.append({
                "original_Q": question,
                "variations": variations
            })

            # Progress indicator
            if (idx + 1) % 50 == 0:
                print(f"  ✓ Diproses {idx + 1} pertanyaan...")

        # Simpan hasil
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"✅ Selesai! Output: {output_path} ({len(results)} pertanyaan, {len(results)*5} variasi)\n")
        return True

    except FileNotFoundError:
        print(f"❌ File tidak ditemukan: {input_path}\n")
        return False
    except json.JSONDecodeError:
        print(f"❌ Error parsing JSON: {input_path}\n")
        return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def main():
    """Main function"""
    print("="*70)
    print("🚀 GENERATOR VARIASI PERTANYAAN DATASET Q&A - IMPROVED VERSION")
    print("="*70)
    print()

    # Set working directory
    base_dir = Path("/root/dataset")
    os.chdir(base_dir)

    success_count = 0
    failed_files = []

    for filename in INPUT_FILES:
        input_path = base_dir / filename

        # Buat nama output
        name_without_ext = filename.replace('.json', '')
        output_filename = f"{name_without_ext}_variasi.json"
        output_path = base_dir / output_filename

        # Proses file
        if process_file(input_path, output_path):
            success_count += 1
        else:
            failed_files.append(filename)

    # Summary
    print("="*70)
    print("📊 RINGKASAN")
    print("="*70)
    print(f"Total file diproses: {len(INPUT_FILES)}")
    print(f"Berhasil: {success_count}")
    print(f"Gagal: {len(failed_files)}")

    if failed_files:
        print("\n❌ File yang gagal:")
        for f in failed_files:
            print(f"  - {f}")

    print("\n✅ Semua file output tersimpan di: /root/dataset/")
    print("="*70)

if __name__ == "__main__":
    main()
