import json
import re
from pathlib import Path

def extract_qa_from_text(text):
    """
    Extract Question and Answer from Gemma chat template format.

    Format in text:
    <start_of_turn>user\n{question}<end_of_turn>\n<start_of_turn>model\n{answer}<end_of_turn>
    """
    # Extract user question
    user_pattern = r'<start_of_turn>user\n(.*?)<end_of_turn>'
    user_match = re.search(user_pattern, text, re.DOTALL)

    # Extract model answer
    model_pattern = r'<start_of_turn>model\n(.*?)<end_of_turn>'
    model_match = re.search(model_pattern, text, re.DOTALL)

    if user_match and model_match:
        question = user_match.group(1).strip()
        answer = model_match.group(1).strip()
        return question, answer

    return None, None

def convert_pmb_to_qa(input_file, output_file):
    """
    Convert train_pmb_augmented.json to dataset_combined_all_variations.json format.

    Input format:  [{"text": "<start_of_turn>user\n...<end_of_turn>..."}, ...]
    Output format: [{"Q": "...", "A": "..."}, ...]
    """
    print(f"Reading: {input_file}")

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total entries in input: {len(data)}")

    # Convert to Q&A format
    qa_data = []
    skipped = 0

    for i, item in enumerate(data):
        text = item.get('text', '')
        question, answer = extract_qa_from_text(text)

        if question and answer:
            qa_data.append({
                "Q": question,
                "A": answer
            })
        else:
            skipped += 1
            if skipped <= 5:  # Show first 5 skipped entries
                print(f"  WARNING: Skipped entry {i+1}: Could not extract Q&A")

    print(f"\nSuccessfully converted: {len(qa_data)} entries")
    print(f"Skipped: {skipped} entries")

    # Save to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(qa_data, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_file}")

    # Show sample
    print(f"\nSample output (first 3 entries):")
    for i, item in enumerate(qa_data[:3], 1):
        print(f"\n{i}. Q: {item['Q'][:80]}...")
        print(f"   A: {item['A'][:80]}...")

if __name__ == "__main__":
    # File paths
    input_file = Path("train_pmb_augmented.json")
    output_file = Path("train_pmb_qa_format.json")

    # Convert
    convert_pmb_to_qa(input_file, output_file)

    print("\n" + "="*80)
    print("CONVERSION COMPLETE")
    print("="*80)
