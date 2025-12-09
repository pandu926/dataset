import json
import random
from pathlib import Path

def create_variations(question):
    """
    Create 3 variations of a question using different patterns.

    Variations:
    1. Original question
    2. More formal variation
    3. More casual/informal variation
    """
    variations = [question]  # Original is always included

    # Variation patterns
    q_lower = question.lower().strip()
    q_clean = question.strip()

    # Variation 2: Add polite prefix
    polite_prefixes = [
        "Bisakah dijelaskan ",
        "Mohon informasi terkait ",
        "Saya ingin mengetahui ",
        "Tolong jelaskan ",
        "Bisa bantu info tentang ",
    ]

    # Create variation 2 (formal)
    if q_lower.startswith(("apakah", "bagaimana", "apa ", "berapa", "kapan", "dimana", "mengapa", "siapa")):
        # Remove question word and add prefix
        words = q_clean.split(None, 1)
        if len(words) > 1:
            main_part = words[1]
            # Remove trailing question mark if exists
            if main_part.endswith("?"):
                main_part = main_part[:-1]
            variation_2 = random.choice(polite_prefixes) + main_part.lower()
            if not variation_2.endswith("?"):
                variation_2 += "?"
            # Capitalize first letter
            variation_2 = variation_2[0].upper() + variation_2[1:]
            variations.append(variation_2)
        else:
            variations.append(question)
    else:
        # Just add a polite prefix
        prefix = random.choice(["Permisi, saya ingin tanya ", "Maaf, bisa bantu info tentang ", "Halo, mohon info "])
        var2 = prefix + q_clean.lower()
        if not var2.endswith("?"):
            var2 += "?"
        variations.append(var2)

    # Create variation 3 (casual)
    casual_q = q_clean

    # Apply casual transformations
    casual_replacements = [
        ("Apakah", "Apa"),
        ("apakah", "apa"),
        ("Bagaimana", "Gimana"),
        ("bagaimana", "gimana"),
        ("Bisakah", "Bisa"),
        ("bisakah", "bisa"),
        ("Dapatkah", "Bisa"),
        ("dapatkah", "bisa"),
        ("saya", "saya"),  # Keep saya, don't change to aku for professionalism
    ]

    for old, new in casual_replacements:
        casual_q = casual_q.replace(old, new)

    # Add casual ending
    casual_endings = [" dong?", " ya?", " gak?", "?"]

    if casual_q.endswith("?"):
        casual_q = casual_q[:-1]  # Remove existing ?

    casual_q += random.choice(casual_endings)

    variations.append(casual_q)

    return variations[:3]  # Return exactly 3 variations

def create_dataset_variations(input_file, output_file):
    """
    Create 3 variations for each question in the dataset.

    Input: [{"Q": "...", "A": "..."}, ...]
    Output: [{"Q": "variation1", "A": "..."}, {"Q": "variation2", "A": "..."}, ...]
    """
    print(f"Reading: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Original entries: {len(data)}")

    # Create variations
    varied_data = []

    for i, item in enumerate(data, 1):
        question = item['Q']
        answer = item['A']

        # Create 3 variations
        variations = create_variations(question)

        # Add each variation with the same answer
        for var_q in variations:
            varied_data.append({
                "Q": var_q,
                "A": answer
            })

        if i % 100 == 0:
            print(f"  Processed {i}/{len(data)} entries...")

    print(f"\nTotal entries after variation: {len(varied_data)}")
    print(f"Multiplication factor: {len(varied_data) / len(data):.1f}x")

    # Save to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(varied_data, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_file}")

    # Show samples
    print(f"\nSample variations (first 2 original questions):")
    for i in range(min(6, len(varied_data))):
        print(f"\n{i+1}. Q: {varied_data[i]['Q']}")
        print(f"   A: {varied_data[i]['A'][:70]}...")

    return len(data), len(varied_data)

if __name__ == "__main__":
    # File paths
    input_file = Path("dataset_cleaned_filtered.json")
    output_file = Path("dataset_cleaned_filtered_3x.json")

    # Create variations
    original_count, varied_count = create_dataset_variations(input_file, output_file)

    print("\n" + "="*80)
    print("VARIATION CREATION COMPLETE")
    print("="*80)
    print(f"Original entries:  {original_count}")
    print(f"Varied entries:    {varied_count}")
    print(f"Multiplier:        {varied_count / original_count:.1f}x")
    print("="*80)
