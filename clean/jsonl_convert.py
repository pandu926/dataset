import json
import re
import uuid

INPUT_FILE = "clean/snk.json"       # file asal
OUTPUT_FILE = "data/snk_v2.jsonl"    # hasil JSONL

# ================================
# 1. Baca raw file & hapus komentar // ...
# ================================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

clean = re.sub(r'//.*', '', raw)  # hapus komentar

# ================================
# 2. Parse JSON
# ================================
data = json.loads(clean)

# ================================
# 3. Fungsi hitung kata
# ================================
def count_words(text):
    return len(text.split())

# ================================
# 4. Konversi ke format JSONL ChatML
# ================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for i, item in enumerate(data, start=1):

        q = item["Q"].strip()
        a = item["A"].strip()
      

        obj = {
            "messages": [
                {"role": "user", "content": q},
                {"role": "assistant", "content": a}
            ],
            "metadata": {
                "id": f"entry_{i}",
                "format_type": "original",
                "q_tokens": count_words(q),
                "a_tokens": count_words(a),
                "category": "syarat_n_ketentuan",
                "verified": False
            }
        }

        out.write(json.dumps(obj, ensure_ascii=False) + "\n")

print("✅ Konversi selesai. Hasil disimpan di:", OUTPUT_FILE)
