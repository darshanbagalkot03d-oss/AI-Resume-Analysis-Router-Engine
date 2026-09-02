# 🚀 AI Resume Analysis & Router Engine

A CLI-based Resume Optimization Engine built with Python and the **Google Gemini API SDK**. The system features a **hybrid dual-path architecture**: standard static prompt routing (Fast Lane) and dynamic unstructured prompt optimization via a dedicated Gatekeeper Agent (Smart Lane).

---

## 🏗️ System Architecture

```text
                ┌──────────────────────────────────────────────┐
                │               User Selection                 │
                └──────────────────────┬───────────────────────┘
                                       │
               ┌───────────────────────┴───────────────────────┐
               ▼                                               ▼
     [PATH A: FAST LANE]                             [PATH B: SMART LANE]
    Static Prompt Schemas                           Unstructured User Input
   (Choices 1–5: ATS, Cover                        (Choice 6: Custom Query)
    Letter, Skill Matrix)                                      │
               │                                               ▼
               │                                    [Gatekeeper Agent]
               │                                (Token Density & Prompt Ops)
               │                                               │
               └───────────────────────┬───────────────────────┘
                                       ▼
                          [Gemini 2.5 Flash Model]
                          (Payload: Resume PDF + Prompt)
                                       │
                                       ▼
                          [Structured Evaluation &
                             Token Usage Audit]
```

---

## ✨ Key Features

- **Dual-Path Prompt Routing:**
  - **Path A (Fast Lane):** Pre-engineered, high-density system prompts for immediate talent audits, ATS job description alignment, market benchmarking, and cover letter generation.
  - **Path B (Smart Lane):** A dedicated **Gatekeeper Agent** (`temperature=0.1`) that compresses conversational, unstructured user queries into Level-2 structured prompt schemas before final inference.
- **Gemini Files API Integration:** Directly uploads PDF resumes to Google's cloud storage context for multi-modal context processing, complete with automatic cloud cleanup upon exiting (`Choice 7`).
- **Real-Time Token Auditing:** Tracks estimated input tokens prior to execution and audits final prompt, candidate, and overall token consumption post-inference.
- **Fault-Tolerant CLI:** Includes multi-line input handling (`END` terminator) and graceful exception catching to maintain session continuity during transient 503 API rate limits.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **LLM SDK:** `google-genai`
- **Model:** `gemini-2.5-flash`
- **Environment Management:** `python-dotenv`

---

## 📂 Project Structure

```text
├── config/
│   ├── __init__.py       # Config package exports
│   ├── menu.py           # CLI menu display logic & option metadata
│   └── prompts.py        # Master system prompts & Gatekeeper schema
├── appv2.2.py            # Main CLI router, execution engine & cleanup handler
├── .env.example          # Environment variable template
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```
---

## 🚀 Quickstart Guide
1. Prerequisites
Python 3.10 or higher installed.

A valid Google Gemini API Key.

2. Installation
Clone the repository and install dependencies:

```Bash
git clone [https://github.com/YOUR_USERNAME/AI-Resume-Analysis-Router-Engine.git](https://github.com/YOUR_USERNAME/AI-Resume-Analysis-Router-Engine.git)
cd AI-Resume-Analysis-Router-Engine
pip install -r requirements.txt
```

3. Environment Configuration
Copy .env.example to .env and insert your API key:

```Bash
cp .env.example .env
Edit .env:

Code snippet
GEMINI_API_KEY=AIzaSy...
```

4. Running the Engine
Place your resume PDF in the root directory named my_resume.pdf and execute:

```Bash
python appv2.2.py
```

---

## 📊 Sample CLI Output

Plaintext

⚙️ [Path B] Passing query through Gatekeeper Agent for prompt optimization...
✅ Prompt density optimized successfully.

## 🚀 Analyzing resume against compiled prompt schema...

```Bash
[Token Audit] Est. Input Tokens: 1369

================================ REPORT OUTPUT ================================
                ... [Structured Executive Report Output] ...
================================================================================

[Token Audit] Final Prompt Tokens:   1329
[Token Audit] Final Output Tokens:   815
[Token Audit] Total Tokens Consumed: 3827

```

