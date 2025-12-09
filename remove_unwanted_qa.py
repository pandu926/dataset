import json

# Kata-kata yang harus dihilangkan dari jawaban
UNWANTED_KEYWORDS = ["maaf", "konteks", "topik", "Jika Anda ingin tahu", "terlalu umum"]

def should_remove(answer):
    """
    Cek apakah jawaban mengandung kata-kata yang tidak diinginkan
    """
    answer_lower = answer.lower()
    for keyword in UNWANTED_KEYWORDS:
        if keyword.lower() in answer_lower:
            return True
    return False

def filter_qa_dataset(input_file, output_file):
    """
    Filter dataset QA untuk menghapus entries dengan jawaban yang mengandung kata-kata tertentu
    """
    # Baca file JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total entries sebelum filter: {len(data)}")

    # Filter data
    filtered_data = []
    removed_count = 0

    for item in data:
        answer = item.get('A', '')
        if should_remove(answer):
            removed_count += 1
        else:
            filtered_data.append(item)

    print(f"Total entries dihapus: {removed_count}")
    print(f"Total entries setelah filter: {len(filtered_data)}")

    # Simpan hasil filter
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(f"\nHasil disimpan ke: {output_file}")

if __name__ == "__main__":
    input_file = "train_pmb_no_biaya_qa.json"
    output_file = "train_pmb_no_biaya_qa_cleaned.json"

    filter_qa_dataset(input_file, output_file)
