"""
Script untuk test model dengan pertanyaan dari test_pmb.json
Membandingkan Baseline (Gemma-3-1B) vs Fine-tuned Model
Evaluasi dengan BERT Score saja (BATCH MODE - SIMPLE & FAST)
"""

import time
import json
import random
import numpy as np
from datetime import datetime
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from bert_score import score as bert_score

# Set seed
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)

# ============================================================================
# CONFIGURATION
# ============================================================================
BASE_MODEL_NAME = "google/gemma-3-1b-it"
FINETUNED_MODEL_PATH = "../outputs/gemma-pmb_merged_final"
TEST_DATA_PATH = "data/test_pmb.json"
OUTPUT_DIR = "../outputs"
BATCH_SIZE = 8  # Batch size

SYSTEM_PROMPT = """Anda adalah asisten virtual untuk Penerimaan Mahasiswa Baru (PMB) di Universitas Sains Al-Qur'an."""

# ============================================================================
# LOAD MODELS
# ============================================================================
print("="*80)
print("  LOADING BASELINE & FINE-TUNED MODELS")
print("="*80)

print(f"\n📂 Loading BASELINE model: {BASE_MODEL_NAME}")
tokenizer_base = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
model_base = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)
model_base.eval()
print(f"✅ Baseline model loaded!")

print(f"\n📂 Loading FINE-TUNED model: {FINETUNED_MODEL_PATH}")
tokenizer_ft = AutoTokenizer.from_pretrained(FINETUNED_MODEL_PATH)
model_ft = AutoModelForCausalLM.from_pretrained(
    FINETUNED_MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto"
)
model_ft.eval()
print(f"✅ Fine-tuned model loaded!")

# ============================================================================
# LOAD TEST DATA
# ============================================================================
print(f"\n📂 Loading test data: {TEST_DATA_PATH}")

def extract_qa_from_text(text):
    """Extract question dan answer dari format Gemma chat template"""
    try:
        # Extract user question
        if "<start_of_turn>user\n" in text and "<end_of_turn>" in text:
            user_start = text.find("<start_of_turn>user\n") + len("<start_of_turn>user\n")
            user_end = text.find("<end_of_turn>", user_start)
            question = text[user_start:user_end].strip()
        else:
            question = ""
        
        # Extract model answer (reference)
        if "<start_of_turn>model\n" in text:
            model_start = text.find("<start_of_turn>model\n") + len("<start_of_turn>model\n")
            model_end = text.find("<end_of_turn>", model_start)
            if model_end == -1:
                reference = text[model_start:].strip()
            else:
                reference = text[model_start:model_end].strip()
        else:
            reference = ""
        
        return question, reference
    
    except Exception as e:
        print(f"⚠️  Error extracting Q&A: {e}")
        return "", ""

try:
    with open(TEST_DATA_PATH, 'r', encoding='utf-8') as f:
        test_data_raw = json.load(f)
    
    test_data = []
    skipped = 0
    
    for idx, item in enumerate(test_data_raw, 1):
        text = item.get("text", "")
        if not text:
            skipped += 1
            continue
        
        question, reference = extract_qa_from_text(text)
        if not question or not reference:
            skipped += 1
            continue
        
        test_data.append({
            "question": question,
            "reference": reference
        })
    
    print(f"✅ Test data loaded: {len(test_data)} questions")
    print(f"⚠️  Skipped: {skipped}")
    
    if len(test_data) == 0:
        print("❌ ERROR: No valid test data!")
        exit(1)

except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)

print("="*80)

# ============================================================================
# BATCH INFERENCE FUNCTION - SIMPLE VERSION
# ============================================================================
def generate_answers_batch(model, tokenizer, questions, batch_size=8):
    """Generate answers in batches - SIMPLE & CLEAN"""
    all_answers = []
    total = len(questions)
    
    for i in range(0, total, batch_size):
        batch_q = questions[i:i+batch_size]
        print(f"   Processing {i+1}-{min(i+batch_size, total)}/{total}...", end='\r')
        
        # Build prompts
        prompts = [
            f"<start_of_turn>system\n{SYSTEM_PROMPT}<end_of_turn>\n"
            f"<start_of_turn>user\n{q}<end_of_turn>\n"
            f"<start_of_turn>model\n"
            for q in batch_q
        ]
        
        # Tokenize
        inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=2048).to(model.device)
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,  # Greedy
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode - SIMPLE METHOD (seperti script original)
        for output in outputs:
            full_response = tokenizer.decode(output, skip_special_tokens=True)
            
            # Extract response setelah "model\n" (simple split)
            if "<start_of_turn>model\n" in full_response:
                response = full_response.split("<start_of_turn>model\n")[-1].strip()
            else:
                response = full_response.strip()
            
            response = response.replace("<end_of_turn>", "").strip()
            all_answers.append(response)
    
    print()  # newline
    return all_answers

# ============================================================================
# MAIN EVALUATION
# ============================================================================
def main():
    print("\n" + "="*80)
    print("  BASELINE vs FINE-TUNED COMPARISON (BATCH MODE)")
    print("  BERT SCORE EVALUATION")
    print("="*80)
    print(f"📅 Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total questions: {len(test_data)}")
    print(f"🔢 Batch size: {BATCH_SIZE}")
    print(f"🤖 Baseline: {BASE_MODEL_NAME}")
    print(f"🤖 Fine-tuned: {FINETUNED_MODEL_PATH}")
    print("="*80)
    
    questions = [item['question'] for item in test_data]
    references = [item['reference'] for item in test_data]
    
    # Generate baseline answers
    print("\n🔵 Generating BASELINE answers...")
    start = time.time()
    baseline_answers = generate_answers_batch(model_base, tokenizer_base, questions, BATCH_SIZE)
    baseline_time = time.time() - start
    print(f"✅ Baseline done: {baseline_time:.2f}s ({len(questions)/baseline_time:.2f} q/s)")
    
    # Generate fine-tuned answers
    print("\n🟢 Generating FINE-TUNED answers...")
    start = time.time()
    finetuned_answers = generate_answers_batch(model_ft, tokenizer_ft, questions, BATCH_SIZE)
    finetuned_time = time.time() - start
    print(f"✅ Fine-tuned done: {finetuned_time:.2f}s ({len(questions)/finetuned_time:.2f} q/s)")
    
    # ========================================================================
    # CALCULATE BERT SCORES
    # ========================================================================
    print(f"\n{'='*80}")
    print("  CALCULATING BERT SCORES...")
    print(f"{'='*80}")
    
    # Baseline BERT Score
    print("\n🔵 Calculating BASELINE BERT scores...")
    P_base, R_base, F1_base = bert_score(baseline_answers, references, lang='id', verbose=False)
    
    # Fine-tuned BERT Score
    print("🟢 Calculating FINE-TUNED BERT scores...")
    P_ft, R_ft, F1_ft = bert_score(finetuned_answers, references, lang='id', verbose=False)
    
    # Build results
    results = []
    for i in range(len(test_data)):
        results.append({
            "index": i+1,
            "question": questions[i],
            "reference": references[i],
            "baseline_answer": baseline_answers[i],
            "finetuned_answer": finetuned_answers[i],
            "baseline_bert_p": P_base[i].item(),
            "baseline_bert_r": R_base[i].item(),
            "baseline_bert_f1": F1_base[i].item(),
            "finetuned_bert_p": P_ft[i].item(),
            "finetuned_bert_r": R_ft[i].item(),
            "finetuned_bert_f1": F1_ft[i].item(),
            "improvement": F1_ft[i].item() - F1_base[i].item()
        })
    
    # ========================================================================
    # SUMMARY STATISTICS
    # ========================================================================
    print(f"\n{'='*80}")
    print("  COMPARISON RESULTS")
    print(f"{'='*80}")
    
    avg_base_f1 = F1_base.mean().item()
    avg_base_p = P_base.mean().item()
    avg_base_r = R_base.mean().item()
    
    avg_ft_f1 = F1_ft.mean().item()
    avg_ft_p = P_ft.mean().item()
    avg_ft_r = R_ft.mean().item()
    
    improvement = avg_ft_f1 - avg_base_f1
    improvement_pct = (improvement / avg_base_f1) * 100 if avg_base_f1 > 0 else 0
    
    print(f"\n🔵 BASELINE (Gemma-3-1B-IT)")
    print(f"   BERT F1:        {avg_base_f1:.4f}")
    print(f"   BERT Precision: {avg_base_p:.4f}")
    print(f"   BERT Recall:    {avg_base_r:.4f}")
    print(f"   Time:           {baseline_time:.2f}s")
    
    print(f"\n🟢 FINE-TUNED")
    print(f"   BERT F1:        {avg_ft_f1:.4f}")
    print(f"   BERT Precision: {avg_ft_p:.4f}")
    print(f"   BERT Recall:    {avg_ft_r:.4f}")
    print(f"   Time:           {finetuned_time:.2f}s")
    
    print(f"\n📈 IMPROVEMENT")
    print(f"   Δ F1:           {improvement:+.4f} ({improvement_pct:+.2f}%)")
    print(f"   Δ Precision:    {avg_ft_p - avg_base_p:+.4f}")
    print(f"   Δ Recall:       {avg_ft_r - avg_base_r:+.4f}")
    
    # Count better/worse
    better = sum(1 for r in results if r['improvement'] > 0.01)
    worse = sum(1 for r in results if r['improvement'] < -0.01)
    print(f"\n📊 Per-question: Better={better} | Worse={worse} | Total={len(results)}")
    
    # ========================================================================
    # SAVE RESULTS
    # ========================================================================
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    output_file = f"{OUTPUT_DIR}/comparison_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "baseline_model": BASE_MODEL_NAME,
        "finetuned_model": FINETUNED_MODEL_PATH,
        "test_data": TEST_DATA_PATH,
        "total_questions": len(test_data),
        "batch_size": BATCH_SIZE,
        "baseline_metrics": {
            "avg_bert_f1": float(avg_base_f1),
            "avg_bert_precision": float(avg_base_p),
            "avg_bert_recall": float(avg_base_r),
            "time_seconds": baseline_time
        },
        "finetuned_metrics": {
            "avg_bert_f1": float(avg_ft_f1),
            "avg_bert_precision": float(avg_ft_p),
            "avg_bert_recall": float(avg_ft_r),
            "time_seconds": finetuned_time
        },
        "improvement": {
            "delta_f1": float(improvement),
            "delta_f1_percent": float(improvement_pct),
            "delta_precision": float(avg_ft_p - avg_base_p),
            "delta_recall": float(avg_ft_r - avg_base_r),
            "better_count": better,
            "worse_count": worse
        },
        "results": results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 Results saved: {output_file}")
    
    # Top 5 improvements
    print(f"\n{'='*80}")
    print("TOP 5 IMPROVEMENTS")
    print(f"{'='*80}")
    sorted_results = sorted(results, key=lambda x: x['improvement'], reverse=True)
    for i, r in enumerate(sorted_results[:5], 1):
        print(f"{i}. {r['improvement']:+.4f} | {r['question'][:60]}...")
    
    # Top 5 regressions
    print(f"\n{'='*80}")
    print("TOP 5 REGRESSIONS")
    print(f"{'='*80}")
    for i, r in enumerate(sorted_results[-5:], 1):
        print(f"{i}. {r['improvement']:+.4f} | {r['question'][:60]}...")
    
    print(f"\n{'='*80}")
    print("✅ EVALUATION COMPLETE!")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()