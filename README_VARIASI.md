# Dataset Variasi Pertanyaan Q&A

## Deskripsi
Script ini menghasilkan 5 variasi semantik untuk setiap pertanyaan dalam dataset Q&A, dengan jawaban yang identik. Tujuannya adalah meningkatkan kualitas fine-tuning model dengan data yang lebih beragam dan realistis.

## Struktur Output
Setiap file output memiliki format:
```json
[
  {
    "original_Q": "Pertanyaan asli",
    "variations": [
      {"Q": "Variasi 1 - Formal", "A": "Jawaban sama persis"},
      {"Q": "Variasi 2 - Casual", "A": "Jawaban sama persis"},
      {"Q": "Variasi 3 - Typo", "A": "Jawaban sama persis"},
      {"Q": "Variasi 4 - Singkat", "A": "Jawaban sama persis"},
      {"Q": "Variasi 5 - Panjang", "A": "Jawaban sama persis"}
    ]
  }
]
```

## Jenis Variasi

### 1. FORMAL/AKADEMIK
- Menggunakan bahasa baku dan sopan
- Struktur kalimat lengkap dan teratur
- Contoh: "Mohon informasi mengenai biaya semester pertama PAI S1."

### 2. CASUAL/SANTAI
- Bahasa sehari-hari dengan singkatan
- Penggunaan partikel casual: dong, ya, min, kak, nih
- Singkatan umum: brp, smt, prodi, gmn
- Contoh: "harga smt satu pai s1 min?"

### 3. TYPO REALISTIS
- Simulasi kesalahan ketik yang umum terjadi
- Huruf hilang: "biaya" → "biya"
- Huruf tertukar: "semester" → "semster"
- Pengetikan ganda: "berapa" → "berapaa"
- Contoh: "Biaya semster satu PAI S1?"

### 4. SINGKAT/PADAT
- Menghilangkan kata-kata tidak esensial
- Langsung ke inti pertanyaan
- Efisien untuk token
- Contoh: "Biaya semester satu PAI S1?"

### 5. PANJANG/DESKRIPTIF
- Konteks lengkap dengan sapaan
- Penjelasan latar belakang
- Lebih natural dan formal
- Contoh: "Permisi, saya ingin menanyakan informasi yang cukup spesifik tentang biaya semester satu pai s1. Mohon dibantu."

## File yang Diproses

| File Input | Jumlah Q | Total Variasi | Output File |
|-----------|----------|---------------|-------------|
| dataset_biaya.json | 300 | 1500 | dataset_biaya_variasi.json |
| dataset-biaya2_clean.json | 144 | 720 | dataset-biaya2_clean_variasi.json |
| dataset_umum_clean.json | 50 | 250 | dataset_umum_clean_variasi.json |
| dataset-beasiswa_clean.json | 120 | 600 | dataset-beasiswa_clean_variasi.json |
| dataset_pofil.json | 30 | 150 | dataset_pofil_variasi.json |
| dataset-podi.json | 80 | 400 | dataset-podi_variasi.json |
| dataset_oot_clean.json | 65 | 325 | dataset_oot_clean_variasi.json |
| dataset-biaya_clean.json | 110 | 550 | dataset-biaya_clean_variasi.json |
| dataset_snk.json | 108 | 540 | dataset_snk_variasi.json |
| dataset-fasilitas_clean.json | 40 | 200 | dataset-fasilitas_clean_variasi.json |
| dataset-alur.json | 24 | 120 | dataset-alur_variasi.json |
| **TOTAL** | **1071** | **5355** | **11 files** |

## Cara Penggunaan

### 1. Menjalankan Script
```bash
python3 generate_variations_improved.py
```

### 2. Melihat Contoh Output
```bash
python3 show_improved_examples.py
```

### 3. Melihat Statistik
```bash
python3 show_statistics.py
```

## Keunggulan Dataset

1. **Variasi Semantik Tinggi**: Setiap pertanyaan memiliki 5 cara berbeda untuk mengajukan pertanyaan yang sama
2. **Realistis**: Typo dan gaya bahasa mencerminkan pola pengguna nyata
3. **Konsistensi Jawaban**: Semua variasi memiliki jawaban yang identik persis
4. **Bahasa Indonesia Autentik**: Menggunakan pola bahasa Indonesia yang natural
5. **Efisien Token**: Variasi singkat membantu optimasi penggunaan token

## Catatan Implementasi

- Script menggunakan random selection untuk variasi yang lebih natural
- Typo hanya diterapkan 1x per pertanyaan untuk menjaga realistis
- Casual variation menggunakan mapping yang konsisten
- Format JSON output valid dan siap untuk fine-tuning

## Lisensi
Dataset ini dibuat untuk keperluan fine-tuning model AI chatbot kampus UNSIQ.

---
Generated: 2025-12-05
Script Version: Improved v1.0
