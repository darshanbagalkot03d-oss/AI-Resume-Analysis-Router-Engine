# 🏛️ Legacy Codebase & Architectural Evolution History

This directory contains all historical iterations, experimental prototypes, and incremental refactors developed during the evolution of the **AI Resume Analysis Router Engine**. 

These files document the step-by-step transition from a basic single-run script into a production-grade, dual-pipeline engine.

---

## 📁 Directory Structure

```text
legacy/
├── app_v0.py       <-- v0.1 Pre-Alpha: Early API connectivity & upload tests
├── app_v1.py       <-- Version 1.0: Monolithic Single-Run Prototype
├── app_v1.1.py     <-- Version 1.1: Multimodal PDF parsing & Level-1 prompts
├── app_v1.2.py     <-- Version 2.0: Multi-Model Provider Router CLI
├── app_v1.3.py     <-- Version 2.1: Expanded routing & formatted schemas
├── app_v2.py       <-- Version 3.0: Centralized Gemini Engine helper
├── app_v2.1.py     <-- Version 3.5: Session Persistence (while True) & Token Auditing
├── app_v2.2.py     <-- Version 4.0: Decoupled Architecture & Gatekeeper Agent
└── README.md       <-- Archive documentation & version history
```

## 📂 File-to-Version Mapping Quick Reference

| File Name in `legacy/` | Architecture Version | Architectural Milestone |
| :--- | :--- | :--- |
| **`app_v0.py`** | **v0.1 Pre-Alpha** | Early API connectivity verification & PDF payload upload tests. |
| **`app_v1.py`** | **Version 1** | Monolithic Single-Run Prototype (`gemini-3.6-flash` Files API). |
| **`v1.1.py`** | **Version 1.1** | Multimodal PDF parsing refinement & Level-1 verbose prompt engineering. |
| **`v1.2.py`** | **Version 2.0** | Multi-Model Provider Router (CLI routing across Gemini, OpenAI, Claude). |
| **`v1.3.py`** | **Version 2.1** | Expanded routing cases & standardized matrix/table formatting rules. |
| **`v2.py`** | **Version 3.0** | Centralized Gemini Engine & Lifecycle Manager (`execute_gemini_analysis`). |
| **`v2.1.py`** | **Version 3.5** | Session Persistence (`while True` loop) & Pre/Post Token Auditing. |
| **`appv2.2.py`** | **Version 4.0** | Decoupled Architecture (`config.py`) & System-Instruction Gatekeeper Agent. |
| *`../app.py` (Root)* | **Version 5.0** | Production Dual-Pipeline System (Path A Fast-Lane / Path B Smart-Lane). |

---

## 🛠️ Detailed Version Evolution Breakdown

### Milestone 1: Monolithic Single-Run Prototype (`app_v0.py`, `app_v1.py`, `v1.1.py`)

#### Architecture & Core Script Features
* **Single-Execution Workflow:** Non-interactive scripts executing a single resume audit pass per run.
* **Direct File Management:** Uses `google.genai` SDK's Files API (`client.files.upload()`) to pass PDF files directly into the context window of `gemini-3.6-flash`.
* **Guaranteed Resource Cleanup:** Implemented strict `try...finally` blocks to ensure uploaded cloud files are deleted via `client.files.delete()`.

#### Functions & Execution Logic
* **Inline Scripting:** Monolithic procedural code with environment variable setup using `python-dotenv`.
* **Model Context Call:** Direct invocation of `client.models.generate_content()` passing both file references and text instructions.

#### Prompt Engineering Strategy (Level-1 Verbose Master Prompt)
* **Style:** High-context, narrative-heavy master prompts.
* **Structure:** Multi-section framework including `# ROLE & PERSONA`, `# OBJECTIVE`, `# PROCESS & EXECUTION STEPS`, `# OUTPUT FORMAT`, and `# CONSTRAINTS`.
* **Characteristics:** High token footprint (~420 tokens) due to detailed roleplay setup, explicit execution instructions, and repeated output formatting rules.

---

### Milestone 2: Multi-Model Provider Router (`v1.2.py`, `v1.3.py`)

#### Architecture & Core Script Features
* **Multi-Provider Integration:** Expanded model routing beyond Google to include `openai.OpenAI` and `anthropic.Anthropic`.
* **CLI Command Router:** Implemented an interactive terminal menu using `if/else` control structures to route tasks based on user input.
* **Cross-Model Task Matching:** Distributed workloads to specific model strengths:
  * **Gemini 2.5 Flash:** Multimodal standalone resume parsing and speed.
  * **GPT-4o:** Complex Job Description (JD) matching and market cross-referencing.
  * **Claude 3.5 Sonnet:** Strict adherence to non-repetition constraints and formatting rules.

#### Functions Developed
* `run_case_1_standalone_audit(pdf_path)`: Gemini-powered skill extraction and audit.
* `run_case_2_jd_comparison(pdf_path, target_jd)`: OpenAI-powered comparative ATS match scoring.
* `run_case_3_strict_bullet_audit(pdf_text)`: Claude-powered strict non-repeated bullet audit.
* `run_case_4_benchmark_cross_reference(pdf_text)`: GPT-4o-powered CTO-level candidate benchmarking.

#### Prompt Engineering Strategy
* **Style:** Vendor-customized Level-1 Master Prompts (`PROMPT_CASE_1` to `PROMPT_CASE_4`).
* **Structure:** Formatted Markdown schemas tailored to force specific output structures (e.g., skill matrices, strict sub-bullet hierarchies).

---

### Milestone 3: Centralized Engine with Token Metrics (`v2.py`, `v2.1.py`)

#### Architecture & Core Script Features
* **SDK Standardization:** Consolidated all analysis cases back to the official `google.genai` SDK (`gemini-2.5-flash` / `gemini-3.6-flash`) for lower latency and cost.
* **Centralized Lifecycle Engine:** Refactored repetitive code into a unified helper function (`execute_gemini_analysis`) managing upload, execution, token auditing, and cloud deletion.
* **Token Observability:** Introduced pre-execution token estimation (`client.models.count_tokens()`) and post-execution usage analysis (`response.usage_metadata`).
* **Session Persistence:** Wrapped choice routing in an interactive `while True` CLI menu loop.

#### Functions Developed
* `execute_gemini_analysis(pdf_path, prompt_text, case_title)`: Unified wrapper for document upload, API execution, token tracking, and resource deletion.
* Expanded CLI cases including Option 5 (`Tailored Cover Letter Generator`).

---

### Milestone 4: Modular Enterprise Architecture (`appv2.2.py`)

#### Architecture & Core Script Features
* **Codebase Decoupling:** Separated prompt definitions, system instructions, and menu items into an external `config/` package.
* **Session Safety:** Wrapped individual menu iterations in localized `try/except` blocks to prevent API errors or bad inputs from crashing the loop.
* **Multi-Line Input Collector:** Enhanced JD collection to parse multi-line text input until a termination signal (`END`) is entered.

#### Functions Developed
* `get_job_description()`: Captures raw multi-line string inputs for target job descriptions.
* `run_gatekeeper_agent(user_query)`: Intercepts raw, unstructured user questions and processes them through a dedicated compiler agent.
* `execute_resume_audit(prompt, resume_file_ref)`: Executes analysis directly against persistent cloud file references.

#### Prompt Engineering Strategy (The Gatekeeper Agent)
* **Style:** System-Instruction-driven meta-prompting (`GATEKEEPER_SYSTEM_PROMPT`).
* **Function:** Operates at a low temperature (`0.1`) to convert unstructured user queries into Level-2 structured prompt schemas before sending them to the primary processing model.

### Milestone 5: Dual-Pipeline Architecture (Current Root `app.py`)
The culmination of the project's evolution, implementing intelligent routing to drastically reduce token consumption while handling both strict formatting and open-ended queries.

```text
                  ┌─────────────────────────────────────────┐
                  │          USER INPUT SELECTION           │
                  └────────────────────┬────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────┐                             ┌───────────────────────┐
│        PATH A         │                             │        PATH B         │
│      (Fast Lane)      │                             │     (Smart Lane)      │
├───────────────────────┤                             ├───────────────────────┤
│ Standard Menu (1-5)   │                             │ Custom Query (Option 6)│
│ Pre-Compiled          │                             │ Unstructured Inputs   │
│ High-Density Prompts  │                             │ User Raw Text/Prompts │
└───────────┬───────────┘                             └───────────┬───────────┘
            │                                                     │
            │                                                     ▼
            │                                         ┌───────────────────────┐
            │                                         │   GATEKEEPER AGENT    │
            │                                         │ (gemini-2.5-flash)    │
            │                                         │ System Inst. | T=0.1  │
            │                                         └───────────┬───────────┘
            │                                                     │
            │                                                     │ (Level-2 Schema)
            └──────────────────────────┬──────────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │       GEMINI 2.5/3.6 FLASH ENGINE       │
                  │   (Document + High-Density Prompt)    │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │     TOKEN AUDIT & REPORT OUTPUT         │
                  └─────────────────────────────────────────┘
```

---

## 📊 Comparative Evolution Matrix

| Version File | Engine / SDK | Architecture Pattern | Token Efficiency | Prompt Engineering Paradigm |
| :--- | :--- | :--- | :--- | :--- |
| **`app_v0.py` / `app_v1.py`** | `google.genai` (`gemini-3.6-flash`) | Monolithic Script | Baseline (Low) | Level-1 Verbose Master Prompt |
| **`v1.2.py` / `v1.3.py`** | Multi-SDK (`genai`, `openai`, `anthropic`) | Provider Router CLI | Low | Vendor-Specific Master Prompts |
| **`v2.py` / `v2.1.py`** | `google.genai` (`gemini-2.5-flash`) | Centralized Processing Helper | Moderate | Schema-Driven Prompts + Token Tracking |
| **`appv2.2.py`** | `google.genai` + `config/` package | Decoupled Modular App | High | Hybrid Prompts + Gatekeeper Agent |
| **`app.py` (Current Root)** | `google.genai` (`gemini-2.5-flash`) | Dual-Pipeline (Path A/B) | Maximum (~60% Avg Savings) | Level-2 High-Density Prompts |

---

## 📉 Token Optimization Metrics Across Versions

| Analysis Case | Level 1 Prompt (Verbose) | Level 2 Prompt (High-Density) | Token Reduction | Key Optimization Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Case 1: Standalone Audit** | ~420 tokens | ~140 tokens | **~66% drop** | Removed execution steps; merged task with Markdown schema anchors. |
| **Case 2: Resume vs JD Match** | ~450 tokens | ~150 tokens | **~67% drop** | Stripped preamble; preserved *Action + Tool + Outcome* rules. |
| **Case 3: Strict Bullet Audit** | ~240 tokens | ~120 tokens | **~50% drop** | Consolidated constraints; enforced strict sub-bullet output. |
| **Case 4: Benchmark Strategy** | ~350 tokens | ~170 tokens | **~50% drop** | Removed duplicated execution steps; relied on table structure. |
| **Case 5: Cover Letter Gen.** | ~310 tokens | ~150 tokens | **~51% drop** | Condensed rule blocks; simplified section directives. |

---

## ⚠️ Usage Note

The scripts in this directory are **archival reference copies** documenting architectural progress. 

To run the latest production version featuring the **Dual-Pipeline (Path A / Path B)** architecture and **Level-2 High-Density Prompts**, run the main entry point from the root directory:

```bash
python app.py