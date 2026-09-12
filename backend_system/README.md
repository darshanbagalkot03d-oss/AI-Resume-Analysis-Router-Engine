# AI Candidate Evaluation & Benchmarking Engine (`appv3.0.py`)

Welcome to the backend documentation for the **AI Candidate Evaluation Engine**. This production-grade CLI system leverages Google's Gemini models with strict Pydantic schema enforcement, multi-key rotation, 429 rate-limit backoffs, and pre-flight token auditing to evaluate technical resumes across multiple domains.

Whether you are a **developer/tester** running multi-domain regression benchmarks or an **individual user** testing your own resume against real-world Job Descriptions, this system provides two flexible execution branches.

---

## ⚙️ Backend Execution Routing

The core engine (`appv3.0.py`) operates on a dual-branch execution model. It automatically routes your requests based on the flags you pass via the CLI, splitting traffic between targeted single-file audits and headless batch processing.

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      BACKEND EXECUTION ROUTING (appv3.0.py)                     │
└─────────────────────────────────────────────────────────────────────────────────┘

                                 [appv3.0.py]
                                      │
            ┌─────────────────────────┴────────────────────────┐
            ▼                                                  ▼
  [BRANCH A: Single-File Mode]                       [BRANCH B: Batch Mode]
       (Passes --file flag)                             (No --file flag)
            │                                                  │
            ├─(Opt 1a: Pre-Config Domain)                      ▼
            │     └─> Static Prompt Routing             [Corpus Scanner]
            │                                       (Iterates test_corpus/)
            ├─(Opt 1b: Custom JD)                              │
            │     └─> [Gatekeeper Agent]                       ▼
            │         (Optimizes/Structures JD)         [State Manager]
            │                                      (Checks Case/Domain/File
            ├─(Opt 1c: Custom Query)                to prevent double billing)
            │     └─> [Gatekeeper Agent]                       │
            │         (Structures Query)                       ▼
            │                                            [Gemini API]
            ▼                                        (Rate Limit & Backoff)
       [Gemini API]                                            │
            │                                                  ▼
            ▼                                      [benchmark_results.json]
 [Terminal Diagnostics (stdout)]                     (Atomic JSON Logging)
 (Score, Token Usage, Gap Flags)                               │
                                                               ▼
                                                    [compute_benchmarks.py]
                                                    (Zero-Token Dashboards)
```
---

## 📁 Backend Folder Structure

To keep documentation clean and separated from the main project overview, this guide lives in the `backend_system/` subfolder:

```text
├── backend_system/          # Dedicated Backend Suite
│   ├── compute_benchmarks.py# Post-run benchmark metrics & analytics
│   ├── generate_corpus.py   # Synthetic test corpus generator
│   └── README.md            # Backend developer guide (this file)
└── test_corpus/             # Multi-domain test corpus directory
    ├── AI_DataScience/      # 👈 Place your AI/ML/Data resumes here
    ├── Cloud_DevOps/        # 👈 Place your Cloud/Infrastructure resumes here
    ├── Cybersecurity/       # 👈 Place your InfoSec/SOC resumes here
    └── Software_Embedded/   # 👈 Place your Software/IoT resumes here
```
---

## ⚙️ Prerequisites & Environment Setup
Before executing any evaluation branch, clone the repository, install dependencies, and configure your Gemini API credentials.

1. Clone the Repository
```Bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

2. Install Required Dependencies
Ensure you have Python 3.10+ installed. Install all required dependencies:

```Bash
pip install -r requirements.txt
```
(Core packages required: google-genai, pydantic, python-dotenv)

3. Configure Gemini API Credentials (.env)
Create a .env file in the root directory. To enable automated failover and quota resilience, you can provide multiple API keys:

```
# Single Key (Basic Setup)
GEMINI_API_KEY=your_primary_gemini_api_key_here

# Multi-Key Rotation Pool (Recommended for Batch Runs)
GEMINI_API_KEY_1=your_primary_gemini_api_key_here
GEMINI_API_KEY_2=your_backup_gemini_api_key_here
```
--- 

## 🎯 Core Evaluation Cases
The system provides 5 standardized prompt evaluation cases. Each case enforces its own dynamic Pydantic schema contract:

In `appv3.0.py`, numerical prompt cases range from **`case_1`** to **`case_5`**. The custom query feature (which was Option 6 in the interactive `appv2.3.py` menu) is executed using the **`--custom`** CLI flag, where instructions are compressed by the Gatekeeper Agent.

Here is the updated complete table including all 6 evaluation capabilities:

| Mode / Identifier | Focus Objective | Primary Output Schema | Key Metrics / Audits |
| --- | --- | --- | --- |
| **`case_1`** | **Baseline Talent Audit** | `CandidateEvaluationSchema` | Unanchored claims, skill stuffing flags, technical score (0–100) |
| **`case_2`** | **ATS & JD Optimization** | `ATSEvaluationSchema` | Overall ATS match score (%), missing critical tech skills, keyword alignment |
| **`case_3`** | **Principal Architect Audit** | `ArchitectEvaluationSchema` | System design depth, architectural claims verification |
| **`case_4`** | **CTO Career Strategy** | `CTOStrategyEvaluationSchema` | Executive gap matrix, scaling & leadership risk flags |
| **`case_5`** | **Technical Cover Letter** | `CoverLetterEvaluationSchema` | Zero-hallucination custom cover letter synthesis retaining candidate metrics |
| **`--custom`** *(Custom Query)* | **Gatekeeper Custom Audit** | Dynamic (`CandidateEvaluationSchema`) | Compressed custom instruction evaluation, targeted skill integrity & metric checks |

---

### 🚀 Execution Guide: Choosing Your Branch
You can run appv3.0.py in two distinct operational modes:

### Branch A: Single-File / Ad-Hoc Target Mode (--file)
Designed for individual candidates, recruiters, or developers who want to audit a single resume PDF and receive rich terminal diagnostic reports.

#### Option 1a: Pre-Configured Domain Mapping
Evaluate a resume against a target domain using pre-configured job descriptions (AI_DataScience, Cloud_DevOps, Cyber, or Software_Embedded):

```Bash
python appv3.0.py --file "test_corpus/test_corpus/AI_DataScience/my_resume.pdf" --case case_2 --domain AI_DataScience
```

#### Option 1b: Custom Job Description for case 2 (--jd)
Inject a raw Job Description directly from a job posting.

> Note on Prompt Optimization: Any raw, user-provided text passed via --jd is automatically routed through the Gatekeeper Agent, which compresses and structures the JD before running the evaluation.

```Bash
python appv3.0.py --file "test_corpus/test_corpus/AI_DataScience/my_resume.pdf" --case case_2 --jd "Looking for a Senior Cyber Security Engineer with experience in Cloud Sentinel, IAM, penetration testing, and Zero-Trust architecture."
```

#### Option 1c: Custom Ad-Hoc Query (--custom)
Ask specific questions or provide custom evaluation instructions for a resume. This query will be optimized by the Gatekeeper Agent:

```Bash
python appv3.0.py --file "+test_corpus/AI_DataScience/my_resume.pdf" --custom "Evaluate if this candidate has hands-on experience in PyTorch, YOLO model deployment, and n8n workflow automation."
```

---

### Branch B: Batch Corpus Engine (Automated Testing)
Designed for developers and researchers performing corpus-wide regression benchmarking, or users looking to test cross-domain fitness.

##### Developer Use Case: Full Corpus Regression Testing
Evaluates every resume across all subdirectories inside backend_system/test_corpus/ using a specific prompt case. Handles rate limits, API key rotation, and atomic logging automatically:

```Bash
python appv3.0.py --case case_1
```

##### User Use Case 2a: Test Fitness for a Specific Domain
1. Place your resume PDF into the specific domain folder (e.g., backend_system/test_corpus/Cloud_DevOps/my_resume.pdf).

2. Run the batch engine for that case:

```Bash
python appv3.0.py --case case_2
```

##### User Use Case 2b: Test Cross-Domain Fitness (Multi-Domain Fit)
1. Place a copy of your resume in multiple domain subfolders inside backend_system/test_corpus/ (e.g., place my_resume.pdf in both backend_system/test_corpus/AI_DataScience/ and backend_system/test_corpus/Cloud_DevOps/).

2. Run the batch engine:

```Bash
python appv3.0.py --case case_1
```

> Tip: Inspect benchmark_results.json to compare how your profile scores across different technical domains.

---

## 🛠️ Utility Scripts (backend_system/)
1. generate_corpus.py: Generates synthetic, multi-domain benchmark PDF resumes for testing pipeline execution under high volume.

2. compute_benchmarks.py: Analyzes generated benchmark_results.json logs, computing domain-wide score distributions, token usage metrics, and error rates.

---

## 📊 Outputs & State Management
* Single-File Mode (Branch A): Outputs a formatted diagnostic report directly to standard output (stdout), including token usage, score breakdowns, and unanchored skill flags.

* Batch Mode (Branch B): Appends outputs atomically to benchmark_results.json. The engine tracks {case}/{domain}/{filename} composite keys to prevent duplicate billing and allow resuming interrupted runs seamlessly.