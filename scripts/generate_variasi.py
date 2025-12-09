#!/usr/bin/env python3
"""
Script untuk generate 5 variasi pertanyaan semantik dari dataset Q&A
Setiap variasi: formal, casual, typo, singkat, panjang
"""

import json
import os
import random
from typing import List, Dict

# File yang akan diproses (exclude dataset_biaya_flat)
FILES_TO_PROCESS = [
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

class QuestionVariator:
    """Generator variasi pertanyaan berkualitas tinggi"""

    # Mapping untuk variasi casual
    CASUAL_REPLACEMENTS = {
        "berapa": ["brp", "berapa", "brapa"],
        "bagaimana": ["gimana", "bagaimana", "gmn"],
        "apakah": ["apa", "apakah"],
        "biaya": ["biaya", "bayar", "ongkos"],
        "semester": ["semester", "smt", "smester"],
        "program studi": ["prodi", "jurusan", "program studi"],
        "universitas": ["univ", "kampus", "universitas"],
        "pendidikan": ["pendidikan", "pend", "didik"],
        "kuliah": ["kuliah", "perkuliahan"],
    }

    def create_typo(self, text: str) -> str:
        """Buat typo realistis pada teks"""
        words = text.split()
        if len(words) < 3:
            return text

        # Pilih 1-2 kata untuk diberi typo
        typo_count = random.randint(1, min(2, len(words)))
        indices = random.sample(range(len(words)), typo_count)

        for idx in indices:
            word = words[idx]
            if len(word) <= 3:
                continue

            # Jenis typo
            typo_type = random.choice(['missing_char', 'swap_char', 'double_char', 'missing_space'])

            if typo_type == 'missing_char' and len(word) > 4:
                pos = random.randint(1, len(word) - 2)
                word = word[:pos] + word[pos+1:]
            elif typo_type == 'swap_char' and len(word) > 3:
                pos = random.randint(0, len(word) - 2)
                word_list = list(word)
                word_list[pos], word_list[pos+1] = word_list[pos+1], word_list[pos]
                word = ''.join(word_list)
            elif typo_type == 'double_char':
                pos = random.randint(0, len(word) - 1)
                word = word[:pos] + word[pos] + word[pos:]

            words[idx] = word

        result = ' '.join(words)
        # Kadang hilangkan spasi
        if random.random() < 0.3:
            result = result.replace(' ', '', 1)

        return result

    def make_casual(self, question: str) -> str:
        """Ubah ke bahasa casual/santai"""
        result = question.lower()

        # Ganti kata formal ke casual
        for formal, casuals in self.CASUAL_REPLACEMENTS.items():
            if formal in result:
                result = result.replace(formal, random.choice(casuals))

        # Hapus tanda tanya kadang atau ganti
        if result.endswith('?'):
            if random.random() < 0.3:
                result = result[:-1]
        else:
            if random.random() < 0.5:
                result += ' ya'

        return result

    def make_formal(self, question: str) -> str:
        """Ubah ke bahasa formal/akademik"""
        # Template formal
        templates = [
            "Saya ingin mengetahui {}",
            "Mohon informasi mengenai {}",
            "Dapatkah Anda memberitahu {}",
            "Saya ingin bertanya tentang {}",
            "Bolehkah saya mengetahui {}"
        ]

        # Hilangkan tanda tanya
        base = question.rstrip('?').strip()

        if random.random() < 0.6:
            return random.choice(templates).format(base.lower())
        else:
            return question  # Pertahankan bentuk asli

    def make_short(self, question: str) -> str:
        """Buat versi singkat"""
        # Hapus kata-kata tidak esensial
        short = question
        remove_words = ['yang', 'untuk', 'dari', 'pada', 'di', 'ke', 'oleh']

        for word in remove_words:
            if random.random() < 0.4:
                short = short.replace(f' {word} ', ' ')

        # Singkatan
        short = short.replace('semester', 'smt')
        short = short.replace('program studi', 'prodi')
        short = short.replace('Pendidikan', 'Pend')

        return short.strip()

    def make_long(self, question: str) -> str:
        """Buat versi panjang/deskriptif"""
        base = question.rstrip('?').strip()

        templates = [
            f"Saya ingin bertanya, {base}?",
            f"Mohon bantuannya, {base}?",
            f"Boleh tanya, {base}?",
            f"Permisi, saya mau tanya {base}?",
            f"Maaf mengganggu, {base}?",
            f"Izin bertanya, {base}?",
        ]

        return random.choice(templates)

    def generate_variations(self, question: str, answer: str) -> List[Dict[str, str]]:
        """Generate 5 variasi pertanyaan dengan jawaban yang sama"""
        variations = []

        # Variasi 1: Formal
        variations.append({
            "Q": self.make_formal(question),
            "A": answer
        })

        # Variasi 2: Casual
        variations.append({
            "Q": self.make_casual(question),
            "A": answer
        })

        # Variasi 3: Typo
        variations.append({
            "Q": self.create_typo(question),
            "A": answer
        })

        # Variasi 4: Singkat
        variations.append({
            "Q": self.make_short(question),
            "A": answer
        })

        # Variasi 5: Panjang
        variations.append({
            "Q": self.make_long(question),
            "A": answer
        })

        return variations


def process_file(input_path: str, output_path: str):
    """Process satu file JSON"""
    print(f"Processing: {input_path}")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"  ⚠️  Skipped: Not a list format")
            return

        variator = QuestionVariator()
        results = []

        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                print(f"  ⚠️  Skipped item {idx}: Not a dict")
                continue

            # Support multiple formats
            question = None
            answer = None

            if 'Q' in item and 'A' in item:
                question = item['Q']
                answer = item['A']
            elif 'instruction' in item and 'response' in item:
                question = item['instruction']
                answer = item['response']
            else:
                print(f"  ⚠️  Skipped item {idx}: Invalid format (no Q/A or instruction/response)")
                continue

            variations = variator.generate_variations(question, answer)

            results.append({
                "original_Q": question,
                "original_A": answer,
                "variations": variations
            })

            # Progress indicator
            if (idx + 1) % 50 == 0:
                print(f"  Processed: {idx + 1}/{len(data)}")

        # Save output
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"  ✓ Saved: {output_path} ({len(results)} items)")

    except FileNotFoundError:
        print(f"  ✗ File not found: {input_path}")
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON decode error: {e}")
    except Exception as e:
        print(f"  ✗ Error: {e}")


def main():
    """Main function"""
    print("=" * 60)
    print("VARIASI PERTANYAAN GENERATOR")
    print("=" * 60)

    base_dir = "/root/dataset"
    processed_count = 0

    for filename in FILES_TO_PROCESS:
        input_path = os.path.join(base_dir, filename)

        # Buat nama output
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_without_ext}_variasi.json"
        output_path = os.path.join(base_dir, output_filename)

        process_file(input_path, output_path)
        processed_count += 1
        print()

    print("=" * 60)
    print(f"✓ SELESAI: {processed_count} file diproses")
    print("=" * 60)


if __name__ == "__main__":
    main()
