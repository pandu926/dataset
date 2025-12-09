import csv

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

def filter_qa_csv(input_file, output_file):
    """
    Filter dataset QA CSV untuk menghapus entries dengan jawaban yang mengandung kata-kata tertentu
    """
    # Baca file CSV
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        data = list(reader)

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
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        if filtered_data:
            fieldnames = ['Q', 'A']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_data)

    print(f"\nHasil disimpan ke: {output_file}")

if __name__ == "__main__":
    input_file = "dataset_cleaned (7).csv"
    output_file = "dataset_cleaned_filtered.csv"

    filter_qa_csv(input_file, output_file)
