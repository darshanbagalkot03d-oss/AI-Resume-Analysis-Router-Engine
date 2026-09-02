# Updated version of app_v2.1 with Uncluttered (by moving the Prompts to another file within the working directory and imported the prompts during execution of code) and Complete code block.
# app.py
"""
Main Execution Engine & CLI Router for AI Resume Audit System.
Uses google-genai SDK with clean config imports and robust session handling.
"""

import os
import sys
from dotenv import load_dotenv
from google import genai

# Clean imports from local config package
from config import (
    PROMPT_CASE_1,
    PROMPT_CASE_2,
    PROMPT_CASE_3,
    PROMPT_CASE_4,
    PROMPT_CASE_5,
    GATEKEEPER_SYSTEM_PROMPT,
    MENU_OPTIONS,
    display_menu,
)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

# Initialize Gemini Client
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3.6-flash"
RESUME_PATH = "my_resume.pdf"


def get_job_description() -> str:
    """Collects multi-line Job Description input from user."""
    print("\n📝 Paste the Target Job Description (Type 'END' on a new line when finished):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def run_gatekeeper_agent(user_query: str) -> str:
    """
    Path B: Compiles unstructured user query into structured Level-2 prompt schema.
    Restores system_instruction and low temperature (0.1) for deterministic output.
    """
    print("\n⚙️ [Path B] Passing query through Gatekeeper Agent for prompt optimization...")
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"Compress and structure this prompt:\n\n{user_query}",
        config={
            "system_instruction": GATEKEEPER_SYSTEM_PROMPT,
            "temperature": 0.1,
        }
    )
    optimized_prompt = response.text.strip()
    print("✅ Prompt density optimized successfully.")
    return optimized_prompt


def execute_resume_audit(prompt: str, resume_file_ref):
    """
    Executes model inference against uploaded PDF resume reference.
    Includes token audit metrics and exception isolation.
    """
    print("\n🚀 Analyzing resume against compiled prompt schema...\n")
    print("-" * 80)
    
    try:
        # Pre-execution Token Audit Estimation
        input_tokens = client.models.count_tokens(
            model=MODEL_NAME,
            contents=[resume_file_ref, prompt]
        )
        print(f"[Token Audit] Est. Input Tokens: {input_tokens.total_tokens}")

        # Model Inference
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[resume_file_ref, prompt]
        )
        
        print("\n" + "=" * 50 + " REPORT OUTPUT " + "=" * 50 + "\n")
        print(response.text)
        print("\n" + "=" * 115)
        
        # Post-execution Token Audit Metadata
        if response.usage_metadata:
            print(f"[Token Audit] Final Prompt Tokens:   {response.usage_metadata.prompt_token_count}")
            print(f"[Token Audit] Final Output Tokens:   {response.usage_metadata.candidates_token_count}")
            print(f"[Token Audit] Total Tokens Consumed: {response.usage_metadata.total_token_count}")
        print("=" * 115 + "\n")

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        print("-" * 80)


def main():
    if not os.path.exists(RESUME_PATH):
        print(f"❌ Error: Resume file '{RESUME_PATH}' not found in current directory.")
        sys.exit(1)

    print(f"📄 Uploading '{RESUME_PATH}' to Gemini Files API...")
    uploaded_file = client.files.upload(file=RESUME_PATH)
    print(f"✅ Resume successfully stored in cloud context (ID: {uploaded_file.name})\n")

    try:
        while True:
            display_menu()
            choice = input("Enter your choice (1-7): ").strip()

            if choice not in [str(i) for i in range(1, 8)]:
                print("⚠️ Invalid choice. Please enter a number between 1 and 7.")
                continue

            choice_num = int(choice)

            if choice_num == 7:
                print("\n👋 Terminating session. Cleaning up cloud context...")
                break

            # Enclose execution iteration in try/except to prevent loop crash on API failures
            try:
                # Handle Job Description input for Options requiring JD
                target_jd = ""
                if MENU_OPTIONS[choice_num]["requires_jd"]:
                    target_jd = get_job_description()
                    if not target_jd:
                        print("⚠️ Job Description cannot be empty for this option.")
                        continue

                # Route to appropriate Prompt Schema
                if choice_num == 1:
                    final_prompt = PROMPT_CASE_1
                elif choice_num == 2:
                    final_prompt = PROMPT_CASE_2.format(target_jd=target_jd)
                elif choice_num == 3:
                    final_prompt = PROMPT_CASE_3
                elif choice_num == 4:
                    final_prompt = PROMPT_CASE_4
                elif choice_num == 5:
                    final_prompt = PROMPT_CASE_5.format(target_jd=target_jd)
                elif choice_num == 6:
                    raw_user_query = input("\n💬 Enter your custom question/instruction regarding the resume: ").strip()
                    if not raw_user_query:
                        print("⚠️ Custom prompt cannot be empty.")
                        continue
                    final_prompt = run_gatekeeper_agent(raw_user_query)

                # Execute model call
                execute_resume_audit(final_prompt, uploaded_file)

            except Exception as iteration_error:
                print(f"⚠️ Action failed: {iteration_error}. Returning to main menu...")

    finally:
        # Cleanup uploaded cloud file reference
        print(f"🧹 Deleting cloud file reference '{uploaded_file.name}'...")
        try:
            client.files.delete(name=uploaded_file.name)
            print("✅ Cleanup complete. Goodbye!")
        except Exception as cleanup_error:
            print(f"⚠️ File cleanup failed or file already removed: {cleanup_error}")


if __name__ == "__main__":
    main()