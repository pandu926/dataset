import json
import random
from pathlib import Path

# Set seed untuk reproducibility
random.seed(42)

# Baca dataset
print("Membaca dataset...")
with open('dataset_combined_all_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total data: {len(data)} samples")

# Shuffle data
random.shuffle(data)

# Hitung split
total = len(data)
train_size = int(total * 0.8)
eval_size = int(total * 0.15)
test_size = total - train_size - eval_size  # sisanya untuk test

print(f"Train: {train_size} samples (80%)")
print(f"Eval: {eval_size} samples (15%)")
print(f"Test: {test_size} samples ({test_size/total*100:.1f}%)")

# Split data
train_data = data[:train_size]
eval_data = data[train_size:train_size + eval_size]
test_data = data[train_size + eval_size:]

# Fungsi untuk konversi ke format Gemma (chat format)
def convert_to_gemma_format(item):
    """
    Konversi dari format Q&A ke format chat Gemma
    Format Gemma menggunakan messages dengan roles: system, user, assistant
    """
    return {
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah asisten informasi UNSIQ (Universitas Sains Al-Qur'an) yang membantu menjawab pertanyaan tentang biaya kuliah, program studi, dan informasi akademik."
            },
            {
                "role": "user",
                "content": item["Q"]
            },
            {
                "role": "assistant",
                "content": item["A"]
            }
        ]
    }

# Buat folder data
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)
print(f"\nFolder 'data' dibuat/sudah ada")

# Simpan sebagai JSONL (satu JSON per baris)
def save_jsonl(data, filename):
    filepath = data_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            gemma_item = convert_to_gemma_format(item)
            f.write(json.dumps(gemma_item, ensure_ascii=False) + '\n')
    print(f"Saved: {filepath} ({len(data)} samples)")

# Simpan semua split
print("\nMenyimpan dataset dalam format JSONL...")
save_jsonl(train_data, 'train.jsonl')
save_jsonl(eval_data, 'eval.jsonl')
save_jsonl(test_data, 'test.jsonl')

print("\n✓ Selesai!")
print(f"\nFile yang dihasilkan:")
print(f"  - data/train.jsonl ({train_size} samples)")
print(f"  - data/eval.jsonl ({eval_size} samples)")
print(f"  - data/test.jsonl ({test_size} samples)")

# Tampilkan contoh data
print("\n" + "="*60)
print("Contoh data format Gemma:")
print("="*60)
example = convert_to_gemma_format(train_data[0])
print(json.dumps(example, ensure_ascii=False, indent=2))
