import os
from dotenv import load_dotenv
from google import genai

# Load API keys securely
load_dotenv()

# Initialize Gemini Client
gemini_client = genai.Client()

# File Path
RESUME_PATH = r"path_to_your/my_resume.pdf"

# ==========================================
# PATH A: HIGH-DENSITY MASTER PROMPTS (Fast Lane)
# ==========================================

PROMPT_CASE_1 = """
Role: Senior AI Hiring Director & Deep-Tech Talent Auditor (GenAI, CV, Edge IoT).
Task: Audit attached resume. Output strictly in the schema below.

## 1. Executive Summary & Market Readiness
- Candidate Profile Identity: [1-2 sentences capturing core technical focus]
- Market Readiness Score: [Score 1-10]/10
- Primary Technical Differentiators: [3 key bullets]

## 2. Extracted Technical Skill Matrix
| Category | Extracted Stack / Tools / Competencies |
| :--- | :--- |
| **Languages & Runtimes** | [List] |
| **Frameworks & Libraries** | [List] |
| **Orchestration & Tools** | [List] |
| **Hardware & Edge IoT** | [List] |

## 3. Critical Limitations & Missing Market Skills
- Infrastructure / Deployment Gaps: [e.g., Docker, FastAPI, CI/CD]
- Framework & Vector DB Gaps: [e.g., LangChain, Pinecone, MCP]
- Project Representation Limitations: [Weak metrics/details]

## 4. Ranked Target Job Role Alignment
Categorize into Primary Fit (>=85%), Specialized Niche Fit (>=75%), and Stretch Fit (>=60%):
### Role 1: [Primary Target Role] — *Primary Fit*
- Match Score: [X]%
- Technical Rationale: [Evidence-backed rationale]
- Key Assets to Leverage: [Top 2 resume points]
### Role 2: [Specialized Niche Role] — *Niche Fit*
- Match Score: [X]%
- Technical Rationale: [Evidence-backed rationale]
- Key Assets to Leverage: [Top 2 resume points]
"""

PROMPT_CASE_2 = """
Role: Lead Technical Recruiter & ATS Optimization Specialist.
Task: Audit attached resume against Target JD. Compute ATS match, identify keyword/skill gaps, and rewrite 3 weak bullets using Action + Tool + Outcome format.

TARGET JD:
{target_jd}

## 1. ATS Compatibility Overview
- Overall ATS Match Score: [X]%
- Keyword Density Score: [High / Medium / Low]
- Summary Assessment: [2 sentences on alignment]

## 2. Missing Critical Keywords & Required Hard Skills
- Missing Required Technologies: [Skills present in JD but absent in resume]
- Missing Architectural / Workflow Keywords: [e.g., RAG, Microservices, ONNX]
- Formatting / Density Recommendations: [Skill section updates]

## 3. Detailed Experience Gap Analysis
- Strengths Aligned with JD: [Direct alignment points]
- Experience Gaps: [Shortfalls against JD requirements]

## 4. Targeted ATS Bullet Rewrites (Action + Tool + Outcome)
1. Original: [Original weak bullet]
   - ATS Rewritten: **[Action Verb] + [Specific Tool from JD] + [Quantified Metric]**
2. Original: [Original weak bullet]
   - ATS Rewritten: **[Action Verb] + [Specific Tool from JD] + [Quantified Metric]**
"""

PROMPT_CASE_3 = """
Role: Principal Software Architect.
Task: Hyper-concise resume audit. 
Constraints: ZERO duplication across sections. NO intro/outro conversational filler. Use sub-bullet hierarchy exclusively. No paragraphs.

## Core Technical Stack & Differentiators
* Primary Languages: [Unique list]
* Core Frameworks & Tools: [Unique list]
* Key Hardware / Edge Exposure: [Unique list]

## Technical Limitations & Infrastructure Gaps
* Backend & Cloud Deficits: [2 unique distinct gaps without repeating tools]
* Framework Gaps: [2 unique distinct missing tools required for modern production]

## Code & Portfolio Action Items
* Action Item 1: [Specific engineering update to make immediately]
* Action Item 2: [Specific engineering update to make immediately]
"""

PROMPT_CASE_4 = """
Role: CTO & Tech Career Strategist.
Task: Benchmark candidate against top 5% AI engineers and provide an actionable 60-day upskilling roadmap. Output strictly in the schema below.

## 1. Candidate vs. Top 5% Market Benchmark Matrix
| Benchmark Dimension | Top 5% Candidate Standard | Candidate Current Level | Gap Severity |
| :--- | :--- | :--- | :--- |
| Agentic Architecture | Custom Python agents, MCP, Tool Calling | [Candidate Level] | [High/Med/Low] |
| Model Deployment | Containerized microservices (FastAPI, Docker) | [Candidate Level] | [High/Med/Low] |
| Evaluation | Evals framework, HITL guardrails, metrics | [Candidate Level] | [High/Med/Low] |

## 2. Critical Architectural & System Design Gaps
- Production Infrastructure Gap: [Evaluation of hosting/serving limitations]
- Framework Depth Gap: [Evaluation of transition from low-code to code-native]

## 3. 60-Day Technical Upskilling & Portfolio Roadmap
### Phase 1: Days 1–30 (Infrastructure & Microservices)
- Goal: [Primary milestone]
- Tasks & Artifact: [Specific tools to build & GitHub deliverable]
### Phase 2: Days 31–60 (Advanced Agentic Architecture)
- Goal: [Primary milestone]
- Tasks & Artifact: [Specific tools to build & GitHub deliverable]
"""

PROMPT_CASE_5 = """
Role: Senior Engineering Copywriter.
Task: Write a tailored, evidence-backed technical cover letter (250-350 words) mapping the attached resume to the target JD.
Constraints: No clichés/fluff. Tone confident and precise. Feature 2 specific resume projects (with tools/metrics) that solve JD challenges.

TARGET JD:
{target_jd}

## 1. Executive Strategy Summary
- Target Role Title: [Extracted from JD]
- Core Overlap Focus: [Top 2 shared technologies]

## 2. Tailored Technical Cover Letter
[Candidate Full Name]
[Email] | [Phone] | [LinkedIn/GitHub]

Date: [Current Date]

To: Hiring Manager
Re: Application for [Job Title]

Dear Hiring Manager,

[Paragraph 1: High-impact technical hook connecting candidate domain experience to JD challenge.]

[Paragraph 2: Technical proof highlighting 2 specific engineering projects from the resume. Explicit tools/metrics.]

[Paragraph 3: Value Add. How the candidate's cross-disciplinary skills will add value.]

[Paragraph 4: Confident call to action requesting a technical discussion.]

Sincerely,
[Candidate Full Name]
"""

# ==========================================
# PATH B: THE GATEKEEPER AGENT (Smart Lane)
# ==========================================

def compress_prompt_via_gatekeeper(verbose_prompt: str) -> str:
    print("\n[Gatekeeper] Intercepting and optimizing custom prompt...")

    gatekeeper_sys_inst = """
    You are a Meta-Prompt Compiler and High-Density Schema Architect.
    Rewrite incoming user prompts into ultracompact, imperative, Level-2 schemas.
    STRICT COMPLIANCE RULES:
    1. NEVER answer the user's request. Output ONLY the optimized prompt schema.
    2. REMOVE all conversational fluff, polite greetings, and filler text.
    3. IF THE USER PROMPT LACKS STRUCTURE: Auto-generate a strict, high-density Markdown schema with bullet points/tables.
    """

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": gatekeeper_sys_inst,
            "temperature": 0.1, 
        },
        contents=f"Compress and structure this prompt:\n\n{verbose_prompt}"
    )
    
    print("[Gatekeeper] Compression complete! Prompt successfully compiled.")
    return response.text.strip()

# ==========================================
# CENTRAL EXECUTION ENGINE
# ==========================================

def execute_gemini_analysis(pdf_path, final_prompt, case_title, original_verbose_prompt=None):
    """Executes the analysis, handles the PDF, and outputs a token audit."""
    print(f"\n--- Running {case_title} (Gemini 2.5 Flash) ---")
    uploaded_file = None
    
    try:
        print("Uploading resume to Gemini Files API...")
        uploaded_file = gemini_client.files.upload(file=pdf_path)
        
        # Token Audit Generation
        if original_verbose_prompt:
            uncompressed_tokens = gemini_client.models.count_tokens(
                model="gemini-2.5-flash",
                contents=[uploaded_file, original_verbose_prompt]
            )
            print(f"[Token Audit] Est. Tokens if uncompressed: {uncompressed_tokens.total_tokens}")
            
        final_input_tokens = gemini_client.models.count_tokens(
            model="gemini-2.5-flash",
            contents=[uploaded_file, final_prompt]
        )
        print(f"[Token Audit] Actual Input Tokens executing: {final_input_tokens.total_tokens}")
        
        print("Analyzing document...")
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, final_prompt]
        )
        
        print("\n" + "="*50 + " REPORT OUTPUT " + "="*50 + "\n")
        print(response.text)
        print("\n" + "="*115)
        
        if response.usage_metadata:
            print(f"[Token Audit] Final Prompt Tokens:   {response.usage_metadata.prompt_token_count}")
            print(f"[Token Audit] Final Output Tokens:   {response.usage_metadata.candidates_token_count}")
            print(f"[Token Audit] Total Tokens Consumed: {response.usage_metadata.total_token_count}")
        print("="*115 + "\n")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if uploaded_file:
            print("Cleaning up: Deleting uploaded file from Gemini servers...")
            gemini_client.files.delete(name=uploaded_file.name)
            print("Cleanup complete.")

# ==========================================
# ROUTER UI
# ==========================================

def main():
    while True:
        print("==================================================")
        print("   AI RESUME ANALYSIS ROUTER & STRATEGY ENGINE    ")
        print("==================================================")
        print("--- PATH A: FAST LANE (High-Density Schemas) ---")
        print("1. Standalone Audit & Skill Gaps")
        print("2. Resume vs Job Description Match")
        print("3. Strict Non-Repeated Bullet Audit")
        print("4. Market Benchmark Strategy Roadmap")
        print("5. Tailored Cover Letter Generator")
        print("--- PATH B: SMART LANE (Dynamic Gatekeeper) ---")
        print("6. Custom Analysis / Chat with Resume")
        print("--------------------------------------------------")
        print("7. Exit")
        
        user_choice = input("\nEnter Choice (1-7): ").strip()

        if user_choice == "1":
            execute_gemini_analysis(RESUME_PATH, PROMPT_CASE_1, "Case 1: Standalone Audit")
            
        elif user_choice == "2":
            target_jd = input("\nPaste Target Job Description:\n")
            execute_gemini_analysis(RESUME_PATH, PROMPT_CASE_2.format(target_jd=target_jd), "Case 2: Resume vs JD Match")
            
        elif user_choice == "3":
            execute_gemini_analysis(RESUME_PATH, PROMPT_CASE_3, "Case 3: Strict Bullet Audit")
            
        elif user_choice == "4":
            execute_gemini_analysis(RESUME_PATH, PROMPT_CASE_4, "Case 4: Benchmark Strategy")

        elif user_choice == "5":
            target_jd = input("\nPaste Target Job Description for Cover Letter:\n")
            execute_gemini_analysis(RESUME_PATH, PROMPT_CASE_5.format(target_jd=target_jd), "Case 5: Cover Letter")
            
        elif user_choice == "6":
            custom_prompt = input("\nEnter your custom prompt/question for the resume:\n")
            print("\nRouting through Smart Lane...")
            optimized_prompt = compress_prompt_via_gatekeeper(custom_prompt)
            print(f"\n[Gatekeeper Result]:\n{optimized_prompt}\n")
            execute_gemini_analysis(RESUME_PATH, optimized_prompt, "Case 6: Custom Analysis", custom_prompt)
            
        elif user_choice == "7":
            print("\nExiting AI Resume Router. Have a great day!")
            break
        else:
            print("Invalid choice! Please select an option between 1 and 7.")

if __name__ == "__main__":
    main()