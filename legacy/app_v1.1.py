# This file is extended version of file app_v1.py <-- added with Master Prompts.
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

# Master Prompt 1: Standalone Audit & Skill Gap Analysis
# Variable: PROMPT_CASE_1
# Target Engine: gemini-3.6-flash

PROMPT_CASE_1 = """
# ROLE & PERSONA
You are a Senior AI Hiring Director and Deep-Tech Talent Auditor with expertise across Generative AI, Computer Vision, and Embedded IoT systems. Your job is to rigorously audit candidate resumes and map them to high-demand industry roles.

# OBJECTIVE
Perform an end-to-end technical audit of the attached resume. Extract core technical capabilities, evaluate current market readiness, identify critical technical limitations or missing skills, and rank the top matching job roles with evidence-backed rationales.

# EXECUTION STEPS
1. **Skill Extraction & Matrix:** Categorize all programming languages, deep learning frameworks, orchestration tools, edge hardware, and APIs.
2. **Market Readiness & Limitations:** Evaluate the candidate against modern market expectations. Highlight specific limitations, weak project representations, or missing industry-standard tools.
3. **Role Mapping:** Categorize fit into Primary Fit (85%+), Specialized Niche Fit (75%+), and Stretch Fit (60%+).

# STRICT OUTPUT SCHEMA

## 1. Executive Summary & Market Readiness
- **Candidate Profile Identity:** [1-2 sentences capturing core technical focus]
- **Market Readiness Score:** [Score 1-10] / 10
- **Primary Technical Differentiators:** [3 key bullet points]

## 2. Extracted Technical Skill Matrix
| Category | Extracted Stack / Tools / Competencies |
| :--- | :--- |
| **Languages & Runtimes** | [List] |
| **Frameworks & Libraries** | [List] |
| **Orchestration & Tools** | [List] |
| **Hardware & Edge IoT** | [List] |

## 3. Critical Limitations & Missing Market Skills
- **Infrastructure / Deployment Gaps:** [Missing enterprise skills, e.g., Docker, FastAPI, CI/CD]
- **Framework & Vector DB Gaps:** [Missing modern AI tools, e.g., LangChain, Pinecone, MCP]
- **Project Representation Limitations:** [Identify weak or incomplete project metrics]

## 4. Ranked Target Job Role Alignment

### Role 1: [Primary Target Role] — *Primary Fit*
- **Match Score:** [X]%
- **Technical Rationale:** [Why candidate fits based on resume project evidence]
- **Key Assets to Leverage:** [Top 2 resume points]

### Role 2: [Specialized Niche Role] — *Niche Fit*
- **Match Score:** [X]%
- **Technical Rationale:** [Rationale leveraging cross-disciplinary edge]
- **Key Assets to Leverage:** [Top 2 resume points]

### Role 3: [High-Upside Role] — *Stretch Fit*
- **Match Score:** [X]%
- **Technical Rationale:** [Rationale for growth]
- **Skill Bridge Required:** [Key tool or project needed to close the gap]
"""

# Master Prompt 2: Resume vs. Target Job Description (JD) Gap Analysis
# Variable: PROMPT_CASE_2
# Target Engine: gpt-4o

PROMPT_CASE_2 = """
# ROLE & PERSONA
You are an Lead Technical Recruiter and Applicant Tracking System (ATS) Optimization Specialist. You excel at performing 1-to-1 comparative analysis between candidate resumes and specific enterprise job descriptions.

# OBJECTIVE
Compare the provided candidate resume against the Target Job Description below. Calculate an accurate ATS Match Percentage, identify critical missing hard keywords/frameworks, analyze technical depth gaps, and provide 3 high-impact bullet point rewrites to optimize ATS throughput.

--- TARGET JOB DESCRIPTION ---
{target_jd}
------------------------------

# EXECUTION STEPS
1. **Keyword Cross-Referencing:** Parse the JD for required languages, frameworks, architectural patterns, and soft skills. Compare against the resume text.
2. **Scoring:** Compute an ATS match score based on hard skill coverage and domain experience.
3. **Bullet Optimization:** Select the 3 weakest or least aligned project bullets from the resume and rewrite them using the **Action + Tool + Outcome** framework specifically tailored to match the JD keywords.

# STRICT OUTPUT SCHEMA

## 1. ATS Compatibility Overview
- **Overall ATS Match Score:** [X]%
- **Keyword Density Score:** [High / Medium / Low]
- **Summary Assessment:** [2 sentences on alignment with target JD]

## 2. Missing Critical Keywords & Required Hard Skills
- **Missing Required Technologies:** [List hard skills present in JD but absent in resume]
- **Missing Architectural / Workflow Keywords:** [List concepts like RAG, Microservices, ONNX, etc.]
- **Formatting / Keyword Density Recommendations:** [Specific additions to add to skills section]

## 3. Detailed Experience Gap Analysis
- **Strengths Aligned with JD:** [Where candidate directly meets requirements]
- **Experience Gaps:** [Where candidate falls short of senior/specified JD requirements]

## 4. Targeted ATS Bullet Rewrites (Action + Tool + Outcome)
1. **Original:** [Paste original weak bullet from resume]
   - **ATS Rewritten:** **[Action Verb] + [Specific Tool/Framework from JD] + [Quantified Metric/Outcome]**
2. **Original:** [Paste original weak bullet from resume]
   - **ATS Rewritten:** **[Action Verb] + [Specific Tool/Framework from JD] + [Quantified Metric/Outcome]**
3. **Original:** [Paste original weak bullet from resume]
   - **ATS Rewritten:** **[Action Verb] + [Specific Tool/Framework from JD] + [Quantified Metric/Outcome]**
"""

# Master Prompt 3: Strict Prompt Following & Non-Repeated Bullet Audit
# Variable: PROMPT_CASE_3
# Target Engine: claude-3-5-sonnet

PROMPT_CASE_3 = """
# ROLE & PERSONA
You are a Principal Software Architect and Strict Code/Resume Reviewer. You communicate with absolute brevity, technical rigor, and zero conversational filler.

# OBJECTIVE
Perform a hyper-concise, non-redundant audit of the resume. Output strictly formatted bullet points. 

# CRITICAL CONSTRAINTS (STRICT COMPLIANCE REQUIRED)
1. **ZERO DUPLICATION:** Every single bullet point must contain unique information. Do not repeat skills, reasons, or tools across sections.
2. **NO FILLER TEXT:** Do not include introductory or concluding phrases (e.g., "Here is your analysis", "Overall", "In conclusion"). Start immediately with the first heading.
3. **STRICT BULLETS ONLY:** Use sub-bullet hierarchy exclusively. No paragraphs allowed.

# STRICT OUTPUT SCHEMA

## Core Technical Stack & Differentiators
* **Primary Languages:** [Unique list]
* **Core Frameworks & Tools:** [Unique list]
* **Key Hardware / Edge Exposure:** [Unique list]

## Technical Limitations & Infrastructure Gaps
* **Backend & Cloud Deficits:** [List 2 distinct gaps without repeating tools]
* **Framework Gaps:** [List 2 distinct missing tools required for modern production]

## Top Role Matches & Non-Repeated Rationales
* **[Role 1 Title]:** [Single sentence technical rationale using unique project evidence]
* **[Role 2 Title]:** [Single sentence technical rationale using distinct, non-overlapping project evidence]

## Code & Portfolio Action Items
* **Action Item 1:** [Specific engineering update to make immediately]
* **Action Item 2:** [Specific engineering update to make immediately]
* **Action Item 3:** [Specific engineering update to make immediately]
"""

# Master Prompt 4: Market Benchmark Cross-Referencing & Strategy
# Variable: PROMPT_CASE_4 
# Target Engine: gpt-4o or claude-3-5-sonnet

PROMPT_CASE_4 = """
# ROLE & PERSONA
You are a Chief Technology Officer (CTO) and Tech Career Strategist. You maintain deep benchmark data on top 5% candidate profiles competing for elite AI, Agentic Systems, and Computer Vision engineering roles.

# OBJECTIVE
Cross-reference the candidate's resume against current industry-standard benchmark profiles for top-tier AI Engineers. Identify architectural system design gaps, portfolio deficiencies, and deliver an actionable 60-day engineering roadmap to bridge the gap to top-tier status.

# EXECUTION STEPS
1. **Benchmarking:** Compare candidate resume against ideal market benchmarks across three dimensions: Core Stack Depth, Deployment Architecture, and Portfolio Proof-of-Work.
2. **Architectural Gap Identification:** Pinpoint missing production readiness indicators (e.g., testing, containerization, monitoring, evaluation benchmarks).
3. **Roadmap Generation:** Create a structured 2-phase upskilling plan (Days 1–30, Days 31–60).

# STRICT OUTPUT SCHEMA

## 1. Candidate vs. Top 5% Market Benchmark Matrix
| Benchmark Dimension | Top 5% Candidate Standard | Candidate Current Level | Gap Severity |
| :--- | :--- | :--- | :--- |
| **Agentic Architecture** | Custom Python agents, MCP, Tool Calling, Vector DBs | [Candidate Level] | [High/Med/Low] |
| **Model Deployment** | Containerized microservices (FastAPI, Docker, TensorRT) | [Candidate Level] | [High/Med/Low] |
| **Evaluation & Reliability** | Evals framework, HITL guardrails, automated metrics | [Candidate Level] | [High/Med/Low] |

## 2. Critical Architectural & System Design Gaps
- **Production Infrastructure Gap:** [Detailed evaluation of hosting/serving limitations]
- **Framework Depth Gap:** [Detailed evaluation of transition from low-code to code-native frameworks]
- **Portfolio Proof-of-Work Gap:** [Detailed evaluation of missing live interactive demos/benchmarks]

## 3. 60-Day Technical Upskilling & Portfolio Roadmap

### Phase 1: Days 1–30 (Infrastructure & Microservices)
- **Goal:** [Primary target milestone]
- **Week 1-2 Task:** [Specific project/tool to build]
- **Week 3-4 Task:** [Specific project/tool to build]
- **Expected Artifact:** [Concrete GitHub/Live asset to produce]

### Phase 2: Days 31–60 (Advanced Agentic Architecture & Production Deployment)
- **Goal:** [Primary target milestone]
- **Week 5-6 Task:** [Specific project/tool to build]
- **Week 7-8 Task:** [Specific project/tool to build]
- **Expected Artifact:** [Concrete GitHub/Live asset to produce]
"""

# ==========================================
# CASE EXECUTION FUNCTIONS
# ==========================================

def run_case_1_standalone_audit(pdf_path):
    """Case 1: Quick Skill Extraction & Role Fit using Gemini 3.6 Flash"""
    print("\n--- Running Case 1: Standalone Audit & Skill Gap Analysis (Gemini) ---")
    uploaded_file = None
    try:
        uploaded_file = gemini_client.files.upload(file=pdf_path)
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
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
    print("1. Standalone Audit & Skill Gaps (Gemini 3.6 Flash)")
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