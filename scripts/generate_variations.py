#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk Generate Variasi Pertanyaan Dataset Q&A
Menghasilkan 5 variasi semantik untuk setiap pertanyaan dengan jawaban yang identik
"""

import json
import os
import random
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

def generate_typo(text):
    """Generate realistic typo untuk simulasi kesalahan manusia"""
    typo_rules = [
        # Hilangkan huruf vokal
        ('berapa', 'brapa'),
        ('biaya', 'biya'),
        ('semester', 'semster'),
        ('kuliah', 'kulah'),
        ('pendidikan', 'pendidkan'),
        # Tukar huruf berdekatan
        ('untuk', 'untk'),
        ('bagaimana', 'bgaimana'),
        ('berapa', 'berapaa'),
        # Hilangkan spasi
        ('berapa biaya', 'berapabiaya'),
        ('apa itu', 'apaitu'),
    ]

    result = text
    # Random apply 1-2 typo rules
    num_typos = random.randint(1, 2)
    selected_typos = random.sample(typo_rules, min(num_typos, len(typo_rules)))

    for original, typo in selected_typos:
        if original.lower() in result.lower():
            result = result.replace(original, typo)
            break

    return result

def generate_variations(question, answer):
    """
    Generate 5 variasi pertanyaan dengan jawaban yang sama
    Variasi: formal, casual, typo, singkat, panjang
    """
    variations = []

    # Variasi 1: Formal/Akademik
    formal = create_formal_version(question)
    variations.append({"Q": formal, "A": answer})

    # Variasi 2: Casual/Santai
    casual = create_casual_version(question)
    variations.append({"Q": casual, "A": answer})

    # Variasi 3: Dengan typo ringan
    typo_version = generate_typo(question)
    variations.append({"Q": typo_version, "A": answer})

    # Variasi 4: Versi singkat/padat
    short = create_short_version(question)
    variations.append({"Q": short, "A": answer})

    # Variasi 5: Versi panjang/deskriptif
    long_version = create_long_version(question)
    variations.append({"Q": long_version, "A": answer})

    return variations

def create_formal_version(question):
    """Buat versi formal/akademik"""
    # Template formal
    if "berapa" in question.lower():
        return f"Mohon informasi mengenai {question.lower().replace('berapa ', '')}."
    elif "apa" in question.lower():
        return f"Saya ingin menanyakan {question.lower().replace('apa ', '')}."
    elif "?" in question:
        return f"Dapatkah Anda menjelaskan {question.replace('?', '')}?"
    return f"Saya memerlukan informasi tentang: {question}"

def create_casual_version(question):
    """Buat versi casual/santai dengan singkatan"""
    casual_words = {
        'berapa': 'brp',
        'bagaimana': 'gmn',
        'kenapa': 'knp',
        'kuliah': 'kuliah',
        'semester': 'smt',
        'program': 'prodi',
        'universitas': 'univ',
        'pendaftaran': 'daftar',
    }

    result = question.lower()
    # Apply beberapa singkatan casual
    for formal, casual in casual_words.items():
        if formal in result and random.random() > 0.5:
            result = result.replace(formal, casual)

    # Tambahkan kata casual di awal
    casual_starters = ['dong', 'nih', 'ya', 'kak', 'min']
    starter = random.choice(casual_starters)

    # Hilangkan tanda tanya formal, ganti dengan casual
    result = result.replace('?', f' {starter}?')

    return result.capitalize()

def create_short_version(question):
    """Buat versi singkat/padat"""
    # Hilangkan kata-kata tidak esensial
    words_to_remove = [
        'mohon', 'tolong', 'bisa', 'dapat', 'ingin', 'mau',
        'saya', 'kami', 'kita', 'untuk', 'tentang'
    ]

    result = question
    for word in words_to_remove:
        result = result.replace(f"{word} ", "")
        result = result.replace(f" {word}", "")

    # Simplifikasi struktur
    result = result.replace("Apakah ", "")
    result = result.replace("Berapa ", "")

    return result.strip()

def create_long_version(question):
    """Buat versi panjang/deskriptif"""
    # Template panjang dengan konteks
    long_templates = [
        f"Saya sedang mencari informasi detail mengenai {question.lower().replace('?', '')}, bisakah dijelaskan?",
        f"Mohon penjelasan lengkap tentang {question.lower().replace('?', '')} untuk keperluan saya?",
        f"Selamat pagi/siang/sore, saya ingin bertanya secara rinci mengenai {question.lower().replace('?', '')}?",
        f"Sebagai calon mahasiswa, saya perlu memahami lebih lanjut tentang {question.lower().replace('?', '')}. Terima kasih.",
        f"Untuk kelengkapan informasi saya, mohon dijelaskan dengan detail mengenai {question.lower().replace('?', '')}?"
    ]

    return random.choice(long_templates)

def process_file(input_path, output_path):
    """Proses satu file JSON dan generate variasi"""
    print(f"📁 Memproses: {input_path}")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        results = []

        # Handle dua format: {"Q": ..., "A": ...} atau {"instruction": ..., "response": ...}
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

            # Progress indicator setiap 50 item
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
    print("🚀 GENERATOR VARIASI PERTANYAAN DATASET Q&A")
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
