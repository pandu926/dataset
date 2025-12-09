import json
import re

INPUT_FILE = "dataset_snk.json"
OUTPUT_FILE = "data/snk.json"

# ==========================================
# 1. Baca file mentah sebagai teks
# ==========================================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

# ==========================================
# 2. Hapus komentar // ...
# ==========================================
clean_text = re.sub(r'//.*', '', raw_text)

# ==========================================
# 3. Parse JSON setelah komentar dihapus
# ==========================================
try:
    data = json.loads(clean_text)
except json.JSONDecodeError as e:
    print("❌ JSON tidak valid:", e)
    exit(1)

# ==========================================
# 4. Ambil hanya Q dan A (hapus field type)
# ==========================================
clean_data = []
for item in data:
    if isinstance(item, dict) and "Q" in item and "A" in item:
        clean_data.append({
            "Q": item["Q"].strip(),
            "A": item["A"].strip()
        })

# ==========================================
# 5. Simpan hasil akhir ke file baru
# ==========================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, ensure_ascii=False, indent=2)

print(f"✅ Cleaning selesai! Hasil disimpan ke {OUTPUT_FILE}")
