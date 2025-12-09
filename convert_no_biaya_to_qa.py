import json
import csv
import re
from pathlib import Path

def extract_qa_from_text(text):
    """Extract Question and Answer from Gemma chat template format."""
    user_pattern = r'<start_of_turn>user\n(.*?)<end_of_turn>'
    user_match = re.search(user_pattern, text, re.DOTALL)

    model_pattern = r'<start_of_turn>model\n(.*?)<end_of_turn>'
    model_match = re.search(model_pattern, text, re.DOTALL)

    if user_match and model_match:
        question = user_match.group(1).strip()
        answer = model_match.group(1).strip()
        return question, answer

    return None, None

def convert_to_qa_formats(input_file, output_json, output_csv):
    """Convert filtered PMB data to Q&A JSON and CSV formats."""
    print(f"Reading: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total entries: {len(data)}")

    # Convert to Q&A format
    qa_data = []
    for item in data:
        text = item.get('text', '')
        question, answer = extract_qa_from_text(text)

        if question and answer:
            qa_data.append({
                "Q": question,
                "A": answer
            })

    print(f"Converted to Q&A: {len(qa_data)} entries")

    # Save JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(qa_data, f, ensure_ascii=False, indent=2)
    print(f"JSON saved: {output_json}")

    # Save CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Q', 'A'])
        writer.writeheader()
        writer.writerows(qa_data)
    print(f"CSV saved: {output_csv}")

    # Show sample
    print(f"\nSample (first 3):")
    for i, item in enumerate(qa_data[:3], 1):
        print(f"\n{i}. Q: {item['Q'][:70]}...")
        print(f"   A: {item['A'][:70]}...")

if __name__ == "__main__":
    input_file = Path("train_pmb_no_biaya.json")
    output_json = Path("train_pmb_no_biaya_qa.json")
    output_csv = Path("train_pmb_no_biaya_qa.csv")

    convert_to_qa_formats(input_file, output_json, output_csv)

    print("\n" + "="*80)
    print("CONVERSION COMPLETE")
    print("="*80)
