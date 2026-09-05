# 🚀 AI Resume Audit, Optimization & Benchmarking Engine

An enterprise-grade, CLI-driven AI Resume Audit and Evaluation Platform built with Python and the **Google Gemini API SDK (`google-genai`)**. 

The repository operates on a **dual-capability architecture**:
1. **Interactive Real-Time Evaluator (`appv2.3.py`):** Single-document interactive audit router supporting standard static prompts (Fast Lane) and dynamic query optimization via a dedicated Gatekeeper Agent (Smart Lane).
2. **Automated Multi-Domain Benchmarking Harness (`generate_corpus.py` → `batch_runner.py` → `compute_benchmarks.py`):** Headless, batch-processing engine that stress-tests system prompts against synthetic edge-case corpora using structured Pydantic schemas.

---

## 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   SYSTEM ARCHITECTURE                                  │
└────────────────────────────────────────────────────────────────────────────────────────┘

    [MODE 1: INTERACTIVE RUNTIME ENGINE]                [MODE 2: AUTOMATED BENCHMARK HARNESS]
                 (appv2.3.py)                                 (Testing Pipeline)
                      │                                               │
           ┌──────────┴──────────┐                          ┌─────────┴─────────┐
           ▼                     ▼                          ▼                   ▼
    [PATH A: FAST LANE]   [PATH B: SMART LANE]       [generate_corpus.py]  [test_corpus/*.pdf]
     Static System         Unstructured User          Generates Edge Case   Multi-Domain Synthetic
     Prompts (1-5)         Query + Gatekeeper         Flaw-Injected PDFs    Resumes (4 Domains)
           │                     │                          │                   │
           └──────────┬──────────┘                          └─────────┬─────────┘
                      ▼                                               ▼
            [Gemini 2.5 Flash]                                [batch_runner.py]
         (Files API + Multimodal)                          Headless Batch Processor
                      │                                    (Pydantic Schema Audit)
                      ▼                                               │
           [Interactive Console                                       ▼
             Executive Report]                           [benchmark_results.json]
                                                           Structured Output Log
                                                                      │
                                                                      ▼
                                                          [compute_benchmarks.py]
                                                          Zero-Token Analytics &
                                                           Dashboard Dashboard
```

---
## ✨ Key Features

### Pydantic Structured Evaluation Schema: 
Enforces strict, type-safe JSON output (CandidateEvaluationSchema) tracking Flaw A (Unbacked Skills), Flaw B (Unanchored Metrics), and Flaw C (Multi-Role Boundary Mapping).

### Dual-Path Prompt Routing (Interactive Mode):

Path A (Fast Lane): Static system prompts (PROMPT_CASE_1 through 5) for talent audits, ATS job description alignment, architectural density, market benchmarking, and cover letter generation.

Path B (Smart Lane): A dedicated Gatekeeper Agent (temperature=0.1) that translates informal, unstructured user queries into Level-2 structured prompt schemas before inference.

### Automated Batch Testing Harness:

Synthetic Edge-Case Generation: Automatically creates multi-domain test PDFs with embedded resume flaws (keyword stuffing, unanchored floating metrics).

Headless Pipeline Processing: Scans subdirectories, executes audits with exponential backoff rate-limit handling, and purges uploaded files from Gemini Cloud storage post-evaluation.

Zero-Token Local Analytics: Computes system-wide performance metrics, severity capture rates, and schema stability statistics locally without incurring additional API token costs.

Real-Time Token Auditing: Pre-calculates estimated input tokens and logs final prompt, output, and cumulative token consumption post-inference.
---

## 📂 Project Structure

```text
├── config/
│   ├── __init__.py       # Config package exports
│   ├── menu.py           # CLI menu display logic & option metadata
│   ├── prompts.py        # Master system prompts (PROMPT_CASE_1..5) & Gatekeeper Schema
│   └── schemas.py        # Pydantic output schemas (CandidateEvaluationSchema, SkillProof, etc.)
├── legacy/               # Archived application version history
│   ├── app_v0.py         # Initial baseline prototype script
│   ├── app_v1.py         # Version 1 implementation
│   ├── app_v1.1.py       # Version 1.1 iteration
│   ├── app_v1.2.py       # Version 1.2 iteration
│   ├── app_v1.3.py       # Version 1.3 iteration
│   ├── app_v2.py         # Version 2 architecture refactor
│   ├── app_v2.1.py       # Version 2.1 iteration
│   ├── app_v2.2.py       # Version 2.2 iteration
│   └── README.md         # Legacy folder documentation
├── test_corpus/              # Multi-domain synthetic PDF test corpus directory
│   ├── AI_DataScience/       # Synthetic resumes for AI/ML/Data roles
│   ├── Cloud_DevOps/         # Synthetic resumes for Cloud/Infrastructure roles
│   ├── Cybersecurity/        # Synthetic resumes for InfoSec/SOC roles
│   └── Software_Embedded/    # Synthetic resumes for Software/IoT roles
├── .env                      # Local environment configuration file (API keys)
├── .env.example              # Environment variable template
├── .gitignore                # Git untracked file exclusion rules
├── appv2.3.py                # Main interactive runtime application entry point
├── batch_runner.py           # Automated headless batch evaluation harness
├── compute_benchmarks.py     # Local zero-token statistical benchmark calculator
├── generate_corpus.py        # Synthetic test corpus generator & edge-case injector
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```
---

## 🧰 Script Inventory & Role Descriptions

### 1. appv2.3.py (Main Interactive Application Runner)
Role: Serves as the primary user-facing CLI application runner.

#### Mechanism: Handles interactive file path selection (my_resume.pdf), manages the CLI menu system, routes requests through Path A (Static Prompts) or Path B (Gatekeeper Agent), uploads PDFs via Gemini Files API, prints structured terminal reports, and executes automatic cloud file cleanups on exit.

### 2. generate_corpus.py (Synthetic Test Data Generator)
Role: Phase 1 of the automated testing pipeline—builds synthetic test dataset.

#### Mechanism: Synthesizes realistic PDF resumes across 4 primary technical domains (AI/Data Science, Cloud/DevOps, Cybersecurity, Software/Embedded). Injects specific evaluation archetypes into documents:

flaw_a_keyword_stuffer: Isolated skills listed without project execution.

flaw_b_unanchored_metrics: Floating stats lacking timeline, resource, or scale bounds.

production_control: Validated, highly anchored engineering profiles.

domain_edge_case: Low-level technical implementations without vendor buzzwords.

### 3. batch_runner.py (Headless Evaluation Harness)
Role: Phase 2 of the automated testing pipeline—executes large-scale batch inference.

#### Mechanism: Recursively scans test_corpus/, uploads each PDF to the Gemini Files API, attaches PROMPT_CASE_1, and requests structured output enforced by CandidateEvaluationSchema. Includes exponential backoff (evaluate_with_retry) for API rate limits (429), updates benchmark_results.json, and deletes cloud file handles immediately after processing.

### 4. compute_benchmarks.py (Zero-Token Analytics Dashboard)
Role: Phase 3 of the automated testing pipeline—analyzes system performance.

#### Mechanism: Reads benchmark_results.json locally without calling the Gemini API. Aggregates data and displays the System Benchmark Evaluation Dashboard, calculating:

Metric Severity Capture Rate: Percentage of floating metrics successfully caught (Flaw B).

Unbacked Skills Flagged Count: Total unanchored skills isolated by project audit (Flaw A).

Hallucination / Schema Exception Rate: Compliance metric checking Pydantic validation failures.

---

## 🎯 Evaluation Flaw Targets

| Flaw Target | Classification | Evaluation Logic | Penalty / System Action |
| --- | --- | --- | --- |
| **Flaw A** | Keyword Anti-Stuffing | Isolates skills listed in standalone technical sections that lack functional implementation proof within project descriptions. | Deducts points from `adjusted_technical_score` and flags skill in `skill_proofs`. |
| **Flaw B** | Quantitative Integrity | Scans metrics for required validation anchors: Resource Parameters, Timeline Scopes, and Scaling Bounds. | Classifies claim as "Unverified Metric" and deducts points from technical score. |
| **Flaw C** | Role Boundary Mapping | Evaluates candidate capabilities across overlapping adjacent domains without defaulting to generalist bias. | Calculates match percentage for all roles meeting $\ge 70\%$ threshold. |

## 🚀 Quickstart Guide
#### 1. Prerequisites
Python 3.10 or higher installed.

A valid Google Gemini API Key.

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

### Mode 1: Interactive Single Resume Evaluation
Place your resume named my_resume.pdf in the root directory and run:

```Bash
python appv2.3.py
```
Select choices 1-5 for Path A static analysis, or choice 6 to submit custom unstructured queries to the Gatekeeper Agent.

### Mode 2: Multi-Domain Automated Benchmarking Pipeline
Step 1: Generate the Synthetic Test Corpus

```Bash
python generate_corpus.py
```
Creates synthetic resume PDFs inside test_corpus/ across all 4 target domains.

Step 2: Run the Headless Batch Auditor
```Bash
python batch_runner.py
```

Evaluates all PDFs sequentially against PROMPT_CASE_1 using CandidateEvaluationSchema and outputs results to benchmark_results.json.

Step 3: Compute System Benchmarks

```Bash
python compute_benchmarks.py
```

Calculates local dashboard statistics, Flaw A/B capture rates, and schema validation compliance rates.

---

## 📊 Sample Benchmark Dashboard Output

Plaintext

```Bash
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

