import os
import sys
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from config import PROMPT_CASE_1
from config.schemas import CandidateEvaluationSchema

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ Error: GEMINI_API_KEY missing.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3.6-flash"
CORPUS_DIR = "test_corpus"
OUTPUT_FILE = "benchmark_results.json"


def load_existing_results():
    """Loads existing results and returns unique domain/filename composite keys."""
    if not os.path.exists(OUTPUT_FILE):
        return [], set()
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Create a composite key "domain/filename" to prevent collision across domain folders
            processed_keys = {f"{item['domain']}/{item['filename']}" for item in data if "filename" in item and "domain" in item}
            return data, processed_keys
    except (json.JSONDecodeError, KeyError):
        return [], set()


def append_single_result(record):
    """Appends a single record atomically to prevent data loss on crashes."""
    existing_data, _ = load_existing_results()
    existing_data.append(record)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2)


def evaluate_with_retry(client, uploaded_file, prompt, max_retries=5):
    """Executes model generation with exponential backoff for rate limits."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[uploaded_file, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=CandidateEvaluationSchema,
                    temperature=0.1
                )
            )
            return response
        except errors.APIError as e:
            if "429" in str(e) or "Quota" in str(e):
                wait_time = (attempt + 1) * 15
                print(f"   ⚠️ Rate limit hit. Pausing for {wait_time}s before retry ({attempt+1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise e
    raise RuntimeError("Failed execution after maximum retries due to persistent API limits.")


def run_batch_evaluation():
    if not os.path.exists(CORPUS_DIR):
        print(f"❌ Error: Directory '{CORPUS_DIR}' not found. Run generate_corpus.py first.")
        sys.exit(1)

    # Load existing progress
    _, processed_keys = load_existing_results()
    total_files = 0

    print("🚀 Starting Batch Evaluation Harness across Synthetic Corpus...\n")
    print(f"📁 Existing records found in {OUTPUT_FILE}: {len(processed_keys)}\n")

    for root, _, files in os.walk(CORPUS_DIR):
        for file in files:
            if file.endswith(".pdf"):
                total_files += 1
                domain = os.path.basename(root)
                file_key = f"{domain}/{file}"  # Unique composite key (e.g. "Cloud_DevOps/domain_edge_case_v1.pdf")
                
                # 1. Skip logic: Check unique composite key
                if file_key in processed_keys:
                    print(f"[{total_files}] Skipping completed: {file_key}")
                    continue
                
                pdf_path = os.path.join(root, file)
                
                print(f"[{total_files}] Processing ({domain}): {file}...")

                # 2. Upload file to Gemini API
                uploaded_file = client.files.upload(file=pdf_path)

                try:
                    # 3. Run evaluation with retry wrapper
                    response = evaluate_with_retry(client, uploaded_file, PROMPT_CASE_1)

                    # 4. Parse and log
                    eval_data: CandidateEvaluationSchema = response.parsed
                    eval_dict = eval_data.model_dump()
                    
                    record = {
                        "filename": file,
                        "domain": domain,
                        "archetype": file.split("_v")[0],
                        "evaluation": eval_dict,
                        "token_usage": {
                            "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                            "output_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0
                        }
                    }
                    
                    # 5. Save progressively
                    append_single_result(record)
                    processed_keys.add(file_key)
                    
                    print(f"   -> Score: {eval_data.adjusted_technical_score}/100 | Metrics Audited: {len(eval_data.metrics_audit)} | Roles Matched: {len(eval_data.evaluated_roles)}")

                except Exception as e:
                    print(f"   ❌ Execution failed for {file}: {e}")

                finally:
                    # 6. Clean up cloud file context immediately
                    client.files.delete(name=uploaded_file.name)
                
                # 7. Safe pacing
                time.sleep(3) 

    print(f"\n✅ Batch processing complete. Detailed metrics saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    run_batch_evaluation()