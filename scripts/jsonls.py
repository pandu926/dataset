import json
import re

# ============================================================
# 1. LOAD DATA DARI FILE JSON
# ============================================================

input_file = "dataset_combined_all_variations.json"        # ganti sesuai file kamu
output_file = "pmb_dataset_gsm8k.jsonl"

with open(input_file, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)        # JSON berisi list objek [{'Q':..., 'A':...}, ...]

gsm8k_data = []

# ============================================================
# 2. KONVERSI KE FORMAT GSM8K
#    answer: [jawaban lengkap] #### [jawaban singkat]
# ============================================================

for item in raw_data:
    # Bisa pakai key 'Q' atau 'question'
    question = item.get("Q") or item.get("question")
    answer = item.get("A") or item.get("answer")

    if not question or not answer:
        continue  # skip kalau ada data rusak

    # Ambil nominal uang sebagai "jawaban singkat"
    numbers = re.findall(r'Rp[\d\.]+', answer)
    final_answer = numbers[0] if numbers else answer

    formatted_answer = f"{answer} #### {final_answer}"

    gsm8k_data.append({
        "question": question,
        "answer": formatted_answer
    })


# ============================================================
# 3. SIMPAN OUTPUT KE FILE JSONL
# ============================================================

with open(output_file, 'w', encoding='utf-8') as f:
    for entry in gsm8k_data:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")

print("✅ Berhasil convert!")
print(f"📦 Output disimpan di: {output_file}")
print(f"📊 Total data: {len(gsm8k_data)}")

print("\n🔍 Contoh data pertama:")
print(json.dumps(gsm8k_data[0], indent=2, ensure_ascii=False))
