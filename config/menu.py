# config/menu.py
"""
UI Menu Metadata and CLI display module.
Contains 3-line descriptions and route flags for each option.
"""

MENU_OPTIONS = {
    1: {
        "title": "Standalone Audit & Skill Gaps",
        "path": "PATH A: FAST LANE",
        "requires_jd": False,
        "bullets": [
            "Performs a deep-tech talent audit of your background across AI, CV, and IoT.",
            "Categorizes technical skills into structured matrices and highlights gaps.",
            "Ranks top job roles you are qualified for based on current resume evidence."
        ]
    },
    2: {
        "title": "Resume vs Job Description (JD) Match",
        "path": "PATH A: FAST LANE",
        "requires_jd": True,
        "bullets": [
            "Compares your resume directly against a target job description.",
            "Generates an ATS match percentage score and flags missing keywords.",
            "Rewrites weak resume bullet points into high-impact 'Action + Tool + Metric' format."
        ]
    },
    3: {
        "title": "Strict Non-Repeated Bullet Audit",
        "path": "PATH A: FAST LANE",
        "requires_jd": False,
        "bullets": [
            "Generates an ultra-concise executive summary with zero text duplication.",
            "Identifies critical backend, cloud, and edge infrastructure gaps.",
            "Provides high-priority action items to fix your portfolio immediately."
        ]
    },
    4: {
        "title": "Market Benchmark Strategy Roadmap",
        "path": "PATH A: FAST LANE",
        "requires_jd": False,
        "bullets": [
            "Benchmarks your skills against top 5% AI/ML engineering standards.",
            "Identifies system design, agentic architecture, and model deployment gaps.",
            "Delivers an actionable 60-day upskilling roadmap broken into 30-day phases."
        ]
    },
    5: {
        "title": "Tailored Cover Letter Generator",
        "path": "PATH A: FAST LANE",
        "requires_jd": True,
        "bullets": [
            "Extracts core requirements from a target Job Description.",
            "Writes a 250-350 word, cliché-free technical cover letter.",
            "Leverages 2 specific engineering projects from your resume with exact metrics."
        ]
    },
    6: {
        "title": "Custom Analysis / Chat with Resume",
        "path": "PATH B: SMART LANE",
        "requires_jd": False,
        "bullets": [
            "Accepts any informal question, instruction, or custom query about your resume.",
            "Routes query through the Gatekeeper Agent to auto-optimize token density.",
            "Returns precise, schema-driven answers for tailored analysis scenarios."
        ]
    },
    7: {
        "title": "Exit",
        "path": "SYSTEM",
        "requires_jd": False,
        "bullets": [
            "Terminates the session and cleans up active cloud resources.",
            "Flushes cached context from local runtime memory.",
            "Safely exits the CLI environment."
        ]
    }
}

def display_menu():
    """Prints the structured CLI menu with 3-line choice descriptions."""
    print("\n" + "=" * 80)
    print("                      AI RESUME ANALYSIS & ROUTER ENGINE                     ")
    print("=" * 80 + "\n")
    
    current_path = ""
    for opt_num, data in MENU_OPTIONS.items():
        if data["path"] != current_path and data["path"] != "SYSTEM":
            current_path = data["path"]
            print(f"--- {current_path} ---\n")
            
        print(f"[Choice {opt_num}] {data['title']}")
        for bullet in data["bullets"]:
            print(f"  • {bullet}")
        print()
        
    print("=" * 80)