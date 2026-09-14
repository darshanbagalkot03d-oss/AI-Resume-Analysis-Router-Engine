# 🚀 AI Resume Audit, Optimization & Benchmarking Engine

A CLI-driven AI Resume Audit and Evaluation Platform built with Python and the Google Gemini API SDK (google-genai).

---

## 🙋 My Role in This Project

I built this to learn — not to showcase raw coding output. My goals were to understand how modern resume-analysis systems actually work under the hood, get hands-on exposure to how a small SaaS-style product is structured end-to-end, and develop a real feel for prompt optimization.

What I did:

* Designed the evaluation logic — the Flaw A/B/C framework (keyword-stuffing detection, unanchored-metric validation, role-boundary mapping) and the Pydantic schemas that enforce it
* Designed the dual-branch execution model (ad-hoc single-file audits vs. automated batch benchmarking) and the routing logic between them
* Designed and iterated on the prompt architecture, including the Gatekeeper Agent pattern that turns unstructured user input into structured evaluation requests
* Defined the evaluation cases (case_1 through case_5) and what each one should measure
* Tested, evaluated, and refined the system's outputs against the synthetic test corpus

What AI tools did:

* Wrote the actual Python implementation (appv3.0.py, the corpus generator, the benchmark calculator) based on the design above

I'm sharing this openly because architecting a system, defining what "correct" output looks like, and directing an AI to implement and iterate on it is itself a skill worth being transparent about — not something to obscure.

This repository serves as an **architectural lab** built using AI-assisted engineering. The goal was to act as the **Product Architect**—designing system execution paths, defining Pydantic evaluation contracts, building synthetic data pipelines, and exploring production SaaS patterns.

### Key Conceptual Explorations:
* **LLM-Based Evaluation vs. Legacy ATS:** Moving past fragile keyword parsing to evaluate contextual skill proof and quantitative metric integrity (e.g., catching unanchored floating metrics and skill stuffing).
* **Prompt Optimization & Gatekeeper Agents:** Implementing low-temperature guardrail agents to compress and translate raw human queries into structured schemas before inference.
* **Zero-Token Analytics & Batch Testing:** Structuring headless testing workflows (`Branch B`) that execute multi-domain evaluation sweeps while logging data for local, zero-token cost benchmarking.
* **SaaS Architecture Fundamentals:** Designing modular backends capable of decoupling into REST APIs and web interfaces (Phase 2 Frontend / Phase 3 Database).

---

This repository currently houses the core backend evaluation engine (Phase 1), operating as a unified runtime that seamlessly handles both individual resume audits and large-scale automated benchmarking.

The system utilizes a dual-branch execution model driven by a single unified runner (appv3.0.py):

* **Branch A** (Ad-Hoc Single-File Router): An interactive audit engine for evaluating individual resumes against static prompts, specific job descriptions, or unstructured custom queries optimized by a dedicated Gatekeeper Agent.

* **Branch B** (Batch Automated Testing Harness): A headless pipeline (backend_system/generate_corpus.py → appv3.0.py → backend_system/compute_benchmarks.py) designed to stress-test system prompts against multi-domain synthetic edge-case corpora using strictly enforced Pydantic schemas and zero-token local analytics.

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SYSTEM ARCHITECTURE (EVOLVING)                          │
└─────────────────────────────────────────────────────────────────────────────────┘

      [PHASE 2: FRONTEND UI] ──────────────────────┐
    (Planned: React/Next.js)                       │
               │                                   ▼
               │                        [PHASE 1: BACKEND CORE]
               │                         (Active: CLI Engine)
               ▼                                   │
      [PHASE 3: DATABASE]                          ├─> [appv3.0.py Unified Runner]
     (Planned: State & Auth)                       ├─> [Branch A: Ad-Hoc Router]
                                                   ├─> [Branch B: Batch Evaluator]
                                                   └─> [Gatekeeper Agent]
                                                           │
                                                           ▼
                                                    [Gemini 3.6 API]
                                                 (Structured JSON Mode)
                                                           │
                                                           ▼
                                                [Local Data Interface]
                                          (benchmark_results.json & CLI stdout)
```
#### Phase 1 (Active): 
The core backend evaluation harness (appv3.0.py), featuring dynamic prompt routing, zero-token batch testing, and Pydantic-enforced structured outputs.

#### Phase 2 (Planned): 
A decoupled React/Next.js frontend UI to consume the benchmark JSON logs and provide a visual dashboard.

#### Phase 3 (Planned): 
Database integration for persistent user session state and authentication

---
## ✨ Key Features
* **Pydantic Structured Evaluation Schema:** Enforces strict, type-safe JSON output (CandidateEvaluationSchema) tracking Flaw A (Unbacked Skills), Flaw B (Unanchored Metrics), and Flaw C (Multi-Role Boundary Mapping).

* **Dual-Path Prompt Routing (Branch A):**

    * **Fast Lane:** Static system prompts (PROMPT_CASE_1 through 5) for talent audits, ATS job description alignment, architectural density, market benchmarking, and cover letter generation.

    * **Smart Lane:** A dedicated Gatekeeper Agent (temperature=0.1) that translates informal, unstructured user queries into Level-2  structured prompt schemas before inference.

* **Automated Batch Testing Harness (Branch B):**

    * **Synthetic Edge-Case Generation:** Automatically creates multi-domain test PDFs with embedded resume flaws (keyword stuffing, unanchored floating metrics).

    * **Headless Pipeline Processing:** Scans subdirectories, executes audits with exponential backoff rate-limit handling, and purges uploaded files from Gemini Cloud storage post-evaluation.

    * **Zero-Token Local Analytics:** Computes system-wide performance metrics, severity capture rates, and schema stability statistics locally without incurring additional API token costs.

* **Real-Time Token Auditing:** Pre-calculates estimated input tokens and logs final prompt, output, and cumulative token consumption post-inference.
---

## 📂 Project Structure

```text
├── config/
│   ├── __init__.py       # Config package exports
│   ├── jds.py            # Target job descriptions for ATS mapping
│   ├── menu.py           # CLI menu display logic & option metadata
│   ├── prompts.py        # Master system prompts (PROMPT_CASE_1..5) & Gatekeeper Schema
│   └── schemas.py        # Pydantic output schemas (CandidateEvaluationSchema, SkillProof, etc.)
├── backend_system/
│   ├── compute_benchmarks.py     # Local zero-token statistical benchmark calculator
│   ├── generate_corpus.py        # Synthetic test corpus generator & edge-case injector
│   ├── README.md                 # Granular CLI execution guide (Branch A vs. Branch B)
│   └── test_corpus/              # Multi-domain test corpus directory
├── legacy/               # Archived application version history
├── .env                  # Local environment configuration file (API keys)
├── .env.example          # Environment variable template
├── .gitignore            # Git untracked file exclusion rules
├── appv3.0.py            # Unified evaluation harness & main entry point
├── requirements.txt      # Project dependencies
└── README.md             # High-level system architecture documentation
```
---
## 🧰 Script Inventory & Role Descriptions

1. appv3.0.py (Unified Evaluation Harness)
* Role: Serves as the primary user-facing CLI application runner for both single-file ad-hoc evaluations and batch regression sweeps.

* Mechanism: Handles --file flag selection for Branch A single-file audits or executes automated directory sweeps across backend_system/test_corpus/ for Branch B. Routes requests through static prompt cases or the Gatekeeper Agent, uploads files via Gemini Files API, logs results atomically to benchmark_results.json, and executes cloud file cleanups post-evaluation.

2. backend_system/generate_corpus.py (Synthetic Test Data Generator)
* Role: Phase 1 of the testing pipeline—builds synthetic test datasets.

* Mechanism: Synthesizes realistic PDF resumes across 4 primary technical domains (AI/Data Science, Cloud/DevOps, Cybersecurity, Software/Embedded). Injects evaluation archetypes (flaw_a_keyword_stuffer, flaw_b_unanchored_metrics, production_control, domain_edge_case).

3. backend_system/compute_benchmarks.py (Zero-Token Analytics Dashboard)
* Role: Phase 3 of the testing pipeline—analyzes system performance.

* Mechanism: Reads benchmark_results.json locally without calling the Gemini API. Computes domain-wide score distributions, Metric Severity Capture Rates, and schema compliance metrics.

---

## 🎯 Evaluation Flaw Targets

| Flaw Target | Classification | Evaluation Logic | Penalty / System Action |
| --- | --- | --- | --- |
| **Flaw A** | Keyword Anti-Stuffing | Isolates skills listed in standalone technical sections that lack functional implementation proof within project descriptions. | Deducts points from `adjusted_technical_score` and flags skill in `skill_proofs`. |
| **Flaw B** | Quantitative Integrity | Scans metrics for required validation anchors: Resource Parameters, Timeline Scopes, and Scaling Bounds. | Classifies claim as "Unverified Metric" and deducts points from technical score. |
| **Flaw C** | Role Boundary Mapping | Evaluates candidate capabilities across overlapping adjacent domains without defaulting to generalist bias. | Calculates match percentage for all roles meeting $\ge 70\%$ threshold. |

---

## 🚀 Quickstart Guide
#### 1. Prerequisites
* Python 3.10 or higher installed.

* A valid Google Gemini API Key.

#### 2. Installation
Clone the repository and install dependencies:

```Bash
git clone [https://github.com/YOUR_USERNAME/AI-Resume-Analysis-Router-Engine.git](https://github.com/YOUR_USERNAME/AI-Resume-Analysis-Router-Engine.git)
cd AI-Resume-Analysis-Router-Engine
pip install -r requirements.txt
```

#### 3. Environment Configuration
Copy .env.example to .env and insert your API key:

```Bash
cp .env.example .env
Edit .env:

Code snippet
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
## 🖥️ Execution Workflows

For detailed CLI flags and custom query usage, refer to the Backend Documentation (backend_system/README.md).

#### Branch A: Single Resume Ad-Hoc Audit
Run an ad-hoc evaluation on a specific resume file:

```Bash
python appv3.0.py --file "backend_system/test_corpus/AI_DataScience/my_resume.pdf" --case case_1
```
#### Branch B: Multi-Domain Automated Benchmarking
Step 1: Generate or Populate Test Corpus
Place your target PDF resumes into subdirectories under backend_system/test_corpus/, or generate synthetic test profiles:

```Bash
python backend_system/generate_corpus.py
```
Step 2: Run the Batch Engine

```Bash
python appv3.0.py --case case_1
```
Step 3: Compute System Benchmarks

```Bash
python backend_system/compute_benchmarks.py
```

---

## 📊 System Execution Modes & Sample Outputs

The engine supports two primary execution flows depending on whether you are running large-scale system stress tests or evaluating individual resumes against specific job descriptions.

---

### 🛠️ 1. Developer Benchmarking Suite (Batch Mode)
*Designed for developers evaluating LLM flaw detection strength across synthetic test corpora.*

After running `generate_corpus.py` (which builds 48 synthetic test resumes containing injected anti-patterns) and processing them through the batch runner, executing `compute_benchmarks.py` generates aggregate accuracy metrics across the test suite:

```bash
============================================================
               SYSTEM BENCHMARK EVALUATION DASHBOARD
============================================================
Total Resumes Evaluated       : 48
Total Quantitative Claims     : 144
Unanchored Claims Caught      : 118
Unbacked Skills Flagged       : 86
------------------------------------------------------------
Metric Severity Capture Rate  : 81.9%
Hallucination / Schema Rate   : 0.00%
============================================================
```
---

🎯 2. Single-File Targeted Audit (User Mode)
Designed for end users or developers evaluating an individual resume against a specific custom job description.

Bypass the batch runner to trigger an immediate, single-file evaluation using the --file and --jd flags:

python appv3.0.py --file "my_resume.pdf" --case case_2 --jd "Seeking an AI Engineer experienced in fine-tuning LLMs, building RAG pipelines, deploying YOLO models, and orchestrating workflows using n8n."

Console Output & Token Audit:

```Bash
🚀 Running Single-File Audit on: my_resume.pdf
📝 Custom JD detected via --jd flag.
⚙️ [Gatekeeper Agent] Compressing and optimizing custom prompt instructions...
✅ Prompt optimization complete.
   [Token Audit] Est. Input Tokens: 1591

=============================== STRUCTURED REPORT (ATSEvaluationSchema) ====================================== 

🎯 Overall ATS Match Score : 82.5%

🔍 Quantitative Metric Audit Highlights:
 • Claim: 'achieving 70.04% precision, 63.81% recall, and mAP@50-95 of 44.47% (COCO standard)'
   Status: Unverified Metric (-15 pts) | Timeline: N/A | Scale: N/A
 • Claim: 'Benchmarked trained model at 30.6 FPS (32.6ms latency) on an NVIDIA T4 GPU at 768px resolution'
   Status: Unverified Metric (-15 pts) | Timeline: N/A | Scale: N/A

==============================================================================================================

[Token Audit] Final Output Tokens: 804
[Token Audit] Total Tokens Consumed: 3963
```

