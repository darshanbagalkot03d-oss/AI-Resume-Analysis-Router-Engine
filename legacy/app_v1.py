import os
import sys
from dotenv import load_dotenv

# Load API keys securely from .env file
load_dotenv()

# Client Initializations
from google import genai
import openai
import anthropic

gemini_client = genai.Client()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Paths
RESUME_PATH = r"path_to_your/my_resume.pdf"

# ==========================================
# PROMPT TEMPLATES FOR SPECIFIC CASES
# ==========================================

PROMPT_CASE_1 = """
Act as a Senior AI Recruiter. Analyze the provided resume:
1. Extract and list key technical skills.
2. Identify major limitations, disadvantages, and missing market skills.
3. Assign top 3 best-suited job roles with clear technical rationales based on existing strengths.
"""

PROMPT_CASE_2 = """
Act as an ATS Optimization Expert. Compare the attached resume against the following Job Description (JD):
--- JOB DESCRIPTION ---
{target_jd}
-----------------------
1. Calculate Match Score (0-100%).
2. Highlight missing critical keywords/skills required by the JD.
3. List 3 specific resume bullet points to rewrite for maximum ATS alignment.
"""

PROMPT_CASE_3 = """
Act as a Principal Engineer. Perform a strict, concise audit of the resume.
CRITICAL CONSTRAINTS:
- Use STRICT bullet points only.
- ZERO duplicate or overlapping reasons.
- No introductory filler text.
- Highlight: Core Technical Stack, Hardware/Software Gaps, and Top 2 High-Demand Roles.
"""

PROMPT_CASE_4 = """
Act as a Deep-Tech Career Strategist. Cross-reference the candidate's resume against current industry standard benchmark resumes for AI/Edge Engineers.
1. Compare candidate's project depth vs top-tier candidate profiles.
2. Identify architectural gaps (e.g., missing Docker, FastAPI, TensorRT, or Vector DB exposure).
3. Provide a step-by-step 60-day roadmap to reach top 5% candidate alignment.
"""

# ==========================================
# CASE EXECUTION FUNCTIONS
# ==========================================

def run_case_1_standalone_audit(pdf_path):
    """Case 1: Quick Skill Extraction & Role Fit using Gemini 2.5 Flash"""
    print("\n--- Running Case 1: Standalone Audit & Skill Gap Analysis (Gemini) ---")
    uploaded_file = None
    try:
        uploaded_file = gemini_client.files.upload(file=pdf_path)
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, PROMPT_CASE_1]
        )
        print(response.text)
    finally:
        if uploaded_file:
            gemini_client.files.delete(name=uploaded_file.name)

def run_case_2_jd_comparison(pdf_path, target_jd):
    """Case 2: Resume vs JD Match using GPT-4o"""
    print("\n--- Running Case 2: Resume vs. Job Description Matching (GPT-4o) ---")
    # For GPT-4o / Claude text extraction, pass resume text or PDF file via API
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an ATS resume optimization engine."},
            {"role": "user", "content": f"{PROMPT_CASE_2.format(target_jd=target_jd)}\n\n[Resume File Provided: {pdf_path}]"}
        ]
    )
    print(response.choices[0].message.content)

def run_case_3_strict_bullet_audit(pdf_text):
    """Case 3: Strict Prompt Following & Non-Repeated Bullets using Claude 3.5 Sonnet"""
    print("\n--- Running Case 3: Strict Non-Repeated Bullet Audit (Claude 3.5 Sonnet) ---")
    response = claude_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        system="Follow constraints with 100% precision. Never repeat points.",
        messages=[
            {"role": "user", "content": f"{PROMPT_CASE_3}\n\nResume Content:\n{pdf_text}"}
        ]
    )
    print(response.content[0].text)

def run_case_4_benchmark_cross_reference(pdf_text):
    """Case 4: Cross-Reference against Top Market Benchmark Resumes using GPT-4o"""
    print("\n--- Running Case 4: Market Benchmark Cross-Referencing (GPT-4o) ---")
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a tech talent benchmarking strategist."},
            {"role": "user", "content": f"{PROMPT_CASE_4}\n\nCandidate Resume Data:\n{pdf_text}"}
        ]
    )
    print(response.choices[0].message.content)

# ==========================================
# MAIN EXECUTION ROUTER (IF-ELSE CONTROL)
# ==========================================

def main():
    print("==========================================")
    print("   AI RESUME ANALYSIS ROUTER & STRATEGY   ")
    print("==========================================")
    print("Select Analysis Mode:")
    print("1. Standalone Audit & Skill Gaps (Gemini 2.5 Flash)")
    print("2. Resume vs Job Description Match (GPT-4o)")
    print("3. Strict Non-Repeated Bullet Audit (Claude 3.5 Sonnet)")
    print("4. Market Benchmark Cross-Referencing (GPT-4o)")
    
    user_choice = input("\nEnter Choice (1-4): ").strip()

    # Route request based on user requirement
    if user_choice == "1":
        run_case_1_standalone_audit(RESUME_PATH)
        
    elif user_choice == "2":
        target_jd = input("\nPaste the Target Job Description:\n")
        if not target_jd.strip():
            print("Job description required for Case 2.")
            return
        run_case_2_jd_comparison(RESUME_PATH, target_jd)
        
    elif user_choice == "3":
        # Note: Extract text locally or pass file directly based on SDK
        resume_text_sample = "Extract text from PDF here..." 
        run_case_3_strict_bullet_audit(resume_text_sample)
        
    elif user_choice == "4":
        resume_text_sample = "Extract text from PDF here..."
        run_case_4_benchmark_cross_reference(resume_text_sample)
        
    else:
        print("Invalid choice! Please select a option between 1 and 4.")

if __name__ == "__main__":
    main()