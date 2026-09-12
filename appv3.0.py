import os
import sys
import json
import time
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from config.prompts import (
    PROMPT_CASE_1,
    PROMPT_CASE_2,
    PROMPT_CASE_3,
    PROMPT_CASE_4,
    PROMPT_CASE_5,
    GATEKEEPER_SYSTEM_PROMPT
)
from config.jds import DOMAIN_JD_MAP, DEFAULT_JD
from config.schemas import (
    CandidateEvaluationSchema,
    ATSEvaluationSchema,
    ArchitectEvaluationSchema,
    CTOStrategyEvaluationSchema,
    CoverLetterEvaluationSchema
)

load_dotenv()

# --- MULTI-KEY ROTATION POOL INITIALIZATION ---
API_KEYS = []
for k in ["GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY"]:
    val = os.getenv(k)
    if val and val not in API_KEYS:
        API_KEYS.append(val)

if not API_KEYS:
    print("❌ Error: No valid API keys (GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY) found in .env.")
    sys.exit(1)

current_key_index = 0
client = genai.Client(api_key=API_KEYS[current_key_index])


MODEL_NAME = "gemini-3.6-flash"
CORPUS_DIR = r"C:\Users\Admin\Desktop\Personal_Project\Exploring_the_Gemini_API_key\backend_system\test_corpus"
OUTPUT_FILE = r"C:\Users\Admin\Desktop\Personal_Project\Exploring_the_Gemini_API_key\backend_system\benchmark_results.json"

def rotate_client():
    """Hot-swaps API client to backup key on hard daily quota limits."""
    global current_key_index, client
    if current_key_index + 1 < len(API_KEYS):
        current_key_index += 1
        print(f"\n   🔄 Daily Quota Exhausted! Swapping to API Key #{current_key_index + 1}...\n")
        client = genai.Client(api_key=API_KEYS[current_key_index])
        return True
    return False

# Dynamic Case Registry mapping Prompt Cases to Schemas and JD Requirements
PROMPT_REGISTRY = {
    "case_1": {"prompt": PROMPT_CASE_1, "requires_jd": False, "schema": CandidateEvaluationSchema},
    "case_2": {"prompt": PROMPT_CASE_2, "requires_jd": True,  "schema": ATSEvaluationSchema},
    "case_3": {"prompt": PROMPT_CASE_3, "requires_jd": False, "schema": ArchitectEvaluationSchema},
    "case_4": {"prompt": PROMPT_CASE_4, "requires_jd": False, "schema": CTOStrategyEvaluationSchema},
    "case_5": {"prompt": PROMPT_CASE_5, "requires_jd": True,  "schema": CoverLetterEvaluationSchema},
}

# --- FEATURE 1: GATEKEEPER AGENT ---
def run_gatekeeper_agent(user_query: str) -> str:
    """Optimizes and compresses raw custom user prompts or user-provided JDs using the Gatekeeper System Prompt."""
    print("⚙️ [Gatekeeper Agent] Compressing and optimizing custom prompt instructions...")
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"Compress and structure this prompt:\n\n{user_query}",
        config={
            "system_instruction": GATEKEEPER_SYSTEM_PROMPT,
            "temperature": 0.1,
        }
    )
    optimized_prompt = response.text.strip()
    print("✅ Prompt optimization complete.")
    return optimized_prompt


# --- FEATURE 2: PRE-FLIGHT TOKEN AUDIT ---
def estimate_tokens(uploaded_file, prompt_text: str):
    """Calculates input token count before sending request to model."""
    try:
        input_tokens = client.models.count_tokens(
            model=MODEL_NAME,
            contents=[uploaded_file, prompt_text]
        )
        print(f"   [Token Audit] Est. Input Tokens: {input_tokens.total_tokens}")
    except Exception as e:
        print(f"   [Token Audit] Could not calculate tokens: {e}")


# --- FEATURE 3: RICH TERMINAL OUTPUT FORMATTER ---
def print_rich_console_summary(eval_data, schema_name: str):
    """Prints formatted diagnostic summaries to stdout for single-file runs with safe attribute access."""
    print("\n" + "=" * 45 + f" STRUCTURED REPORT ({schema_name}) " + "=" * 45 + "\n")

    # Generic Score Outputs
    if hasattr(eval_data, "adjusted_technical_score"):
        print(f"📊 Adjusted Technical Score : {eval_data.adjusted_technical_score} / 100")
    if hasattr(eval_data, "overall_ats_match_score"):
        print(f"🎯 Overall ATS Match Score : {eval_data.overall_ats_match_score}%")

    # Metrics Audit Output
    if hasattr(eval_data, "metrics_audit") and eval_data.metrics_audit:
        print("\n🔍 Quantitative Metric Audit Highlights:")
        for audit in eval_data.metrics_audit[:5]:  # Display top 5
            claim = getattr(audit, "original_claim", "N/A")
            status = getattr(audit, "validation_status", "N/A")
            timeline = getattr(audit, "has_timeline_scope", getattr(audit, "has_timeline", "N/A"))
            scale = getattr(audit, "has_scaling_bound", getattr(audit, "has_scale", "N/A"))
            print(f"  • Claim: '{claim}'")
            print(f"    Status: {status} | Timeline: {timeline} | Scale: {scale}")

    # Skill Proofs / Flaw A Check
    if hasattr(eval_data, "skill_proofs") and eval_data.skill_proofs:
        print("\n🛡️ Skill Integrity & Project Proof Audit:")
        for proof in eval_data.skill_proofs[:5]:
            skill_name = getattr(proof, "skill_name", "N/A")
            has_proof = getattr(proof, "has_project_proof", False)
            status = "✅ Project Verified" if has_proof else "⚠️ Unanchored Skill"
            print(f"  • Skill: {skill_name} | Status: {status}")

    # Capability / Gap Highlights
    if hasattr(eval_data, "missing_critical_technologies") and eval_data.missing_critical_technologies:
        print("\n⚠️ Missing Critical Technologies:")
        for tech in eval_data.missing_critical_technologies[:5]:
            print(f"  • {tech}")

    if hasattr(eval_data, "high_severity_strategic_gaps") and eval_data.high_severity_strategic_gaps:
        print("\n🚨 High Severity Strategic Gaps:")
        for gap in eval_data.high_severity_strategic_gaps[:5]:
            print(f"  • {gap}")

    print("\n" + "=" * 110 + "\n")


# --- ATOMIC LOGGING & STATE MANAGEMENT ---
def load_existing_results():
    """Loads existing benchmark logs to track completed composite keys."""
    if not os.path.exists(OUTPUT_FILE):
        return [], set()
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            processed_keys = {
                f"{item.get('prompt_case', 'case_1')}/{item['domain']}/{item['filename']}"
                for item in data if "filename" in item and "domain" in item
            }
            return data, processed_keys
    except (json.JSONDecodeError, KeyError):
        return [], set()


def append_single_result(record):
    """Appends single record atomically to prevent data corruption."""
    existing_data, _ = load_existing_results()
    existing_data.append(record)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2)


def rotate_client():
    """Hot-swaps API client to backup key on hard daily quota limits."""
    global current_key_index, client
    if current_key_index + 1 < len(API_KEYS):
        current_key_index += 1
        print(f"\n   🔄 Daily Quota Exhausted! Swapping to API Key #{current_key_index + 1}...\n")
        client = genai.Client(api_key=API_KEYS[current_key_index])
        return True
    return False


# --- RESILIENT EXECUTION CORE ---
def evaluate_file_with_fallback(pdf_path: str, prompt_text: str, response_schema):
    """Executes model generation with key rotation and 429 rate limit backoff."""
    global client
    
    uploaded_file = client.files.upload(file=pdf_path)
    estimate_tokens(uploaded_file, prompt_text)

    for attempt in range(5):
        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.1
            )
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[uploaded_file, prompt_text],
                config=config
            )
            
            client.files.delete(name=uploaded_file.name)
            return response

        except errors.APIError as e:
            error_msg = str(e).lower()

            try:
                client.files.delete(name=uploaded_file.name)
            except Exception:
                pass

            # Handle 429 RPM limit (Wait 45s)
            if "429" in error_msg and "quota" not in error_msg:
                print(f"   ⚠️ Per-minute rate limit (RPM) hit. Pausing 45s before retry ({attempt + 1}/5)...")
                time.sleep(45)
                uploaded_file = client.files.upload(file=pdf_path)

            # Handle Hard Daily Quota Limits (Rotate Key)
            elif "quota" in error_msg or "exhausted" in error_msg or "429" in error_msg:
                if rotate_client():
                    print("   Re-uploading file under new key context...")
                    uploaded_file = client.files.upload(file=pdf_path)
                else:
                    raise RuntimeError("STOP_QUOTA_EXHAUSTED: All provided API keys have hit daily limits.")
            else:
                raise e

    raise RuntimeError("Failed execution after maximum retries.")


# --- BRANCH A: SINGLE FILE / AD-HOC TARGET EXECUTION ---
def run_single_file_evaluation(file_path: str, selected_case: str, domain: str, custom_query: str, target_jd: str):
    if not os.path.exists(file_path):
        print(f"❌ Error: Specified file '{file_path}' does not exist.")
        sys.exit(1)

    print(f"🚀 Running Single-File Audit on: {file_path}")

    # Determine Prompt & Schema
    if custom_query:
        final_prompt = run_gatekeeper_agent(custom_query)
        target_schema = CandidateEvaluationSchema
        case_id = "custom_ad_hoc"
    else:
        case_config = PROMPT_REGISTRY[selected_case]
        raw_prompt = case_config["prompt"]
        target_schema = case_config["schema"]
        case_id = selected_case

        if case_config["requires_jd"]:
            # If user provided a raw custom JD string via --jd, optimize it with Gatekeeper Agent
            if target_jd:
                print("📝 Custom JD detected via --jd flag.")
                optimized_jd = run_gatekeeper_agent(f"Extract key criteria and technical requirements from this JD:\n\n{target_jd}")
                final_prompt = raw_prompt.format(target_jd=optimized_jd)
            else:
                # Fallback to pre-configured domain JD map
                jd_text = DOMAIN_JD_MAP.get(domain, DEFAULT_JD)
                final_prompt = raw_prompt.format(target_jd=jd_text)
        else:
            final_prompt = raw_prompt

    try:
        response = evaluate_file_with_fallback(file_path, final_prompt, target_schema)
        eval_data = response.parsed
        
        # Display rich terminal feedback
        print_rich_console_summary(eval_data, target_schema.__name__)

        if response.usage_metadata:
            print(f"[Token Audit] Final Output Tokens: {response.usage_metadata.candidates_token_count}")
            print(f"[Token Audit] Total Tokens Consumed: {response.usage_metadata.total_token_count}\n")

    except Exception as e:
        print(f"❌ Execution failed for {file_path}: {e}")


# --- BRANCH B: BATCH CORPUS EXECUTION ENGINE ---
def run_batch_evaluation(selected_case="case_1"):
    if selected_case not in PROMPT_REGISTRY:
        print(f"❌ Error: Invalid prompt case '{selected_case}'. Choose from: {list(PROMPT_REGISTRY.keys())}")
        sys.exit(1)

    case_config = PROMPT_REGISTRY[selected_case]
    raw_prompt = case_config["prompt"]
    target_schema = case_config["schema"]

    if not os.path.exists(CORPUS_DIR):
        print(f"❌ Error: Directory '{CORPUS_DIR}' not found.")
        sys.exit(1)

    _, processed_keys = load_existing_results()
    total_files = 0

    print(f"🚀 Starting Batch Evaluation Harness for [{selected_case.upper()}] (Active Key: #{current_key_index + 1})...\n")

    for root, _, files in os.walk(CORPUS_DIR):
        for file in files:
            if file.endswith(".pdf"):
                total_files += 1
                domain = os.path.basename(root)
                file_key = f"{selected_case}/{domain}/{file}"

                if file_key in processed_keys:
                    print(f"[{total_files}] Skipping completed: {file_key}")
                    continue

                pdf_path = os.path.join(root, file)
                print(f"[{total_files}] Processing ({domain}) with {selected_case}: {file}...")

                formatted_prompt = raw_prompt
                if case_config["requires_jd"]:
                    domain_jd = DOMAIN_JD_MAP.get(domain, DEFAULT_JD)
                    formatted_prompt = raw_prompt.format(target_jd=domain_jd)

                try:
                    response = evaluate_file_with_fallback(pdf_path, formatted_prompt, target_schema)
                    eval_data = response.parsed
                    eval_output = eval_data.model_dump()

                    summary_str = f"Evaluated under {target_schema.__name__}"
                    if hasattr(eval_data, 'adjusted_technical_score'):
                        summary_str += f" | Score: {eval_data.adjusted_technical_score}/100"
                    if hasattr(eval_data, 'overall_ats_match_score'):
                        summary_str += f" | ATS Score: {eval_data.overall_ats_match_score}%"

                    record = {
                        "prompt_case": selected_case,
                        "filename": file,
                        "domain": domain,
                        "archetype": file.split("_v")[0],
                        "evaluation": eval_output,
                        "token_usage": {
                            "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                            "output_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0
                        }
                    }

                    append_single_result(record)
                    processed_keys.add(file_key)
                    print(f"   -> Completed. {summary_str}")

                    time.sleep(4)

                except RuntimeError as re:
                    if "STOP_QUOTA_EXHAUSTED" in str(re):
                        print("\n🛑 All API keys have reached daily limits. Progress saved cleanly to benchmark_results.json.")
                        sys.exit(0)
                    else:
                        print(f"   ❌ Execution failed for {file}: {re}")

                except Exception as e:
                    print(f"   ❌ Execution failed for {file}: {e}")

    print(f"\n✅ Batch processing complete for {selected_case}. Results saved to '{OUTPUT_FILE}'")


# --- MAIN CLI ROUTER ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Resume Evaluation Engine (v3.0)")
    
    parser.add_argument(
        "--case",
        type=str,
        default="case_1",
        choices=["case_1", "case_2", "case_3", "case_4", "case_5"],
        help="Prompt case to execute (default: case_1)"
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to a single resume PDF file for ad-hoc audit."
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="AI_DS",
        help="Domain context for single-file audit (e.g., AI_DS, Cloud_DevOps, Cyber, Software_Embedded)."
    )
    parser.add_argument(
        "--custom",
        type=str,
        default=None,
        help="Custom query instruction. Triggers Gatekeeper Agent optimization."
    )
    parser.add_argument(
        "--jd",
        type=str,
        default=None,
        help="Custom Job Description text for single-file ATS/Cover Letter audits."
    )

    args = parser.parse_args()

    # Route based on arguments
    if args.file:
        run_single_file_evaluation(
            file_path=args.file,
            selected_case=args.case,
            domain=args.domain,
            custom_query=args.custom,
            target_jd=args.jd
        )
    else:
        run_batch_evaluation(selected_case=args.case)