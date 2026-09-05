# config/menu.py
"""
UI Menu Metadata and CLI display module updated for Metric Auditing and Multi-Role Mapping.
"""

MENU_OPTIONS = {
    1: {
        "title": "Standalone Audit, Metric Validation & Multi-Role Mapping",
        "path": "PATH A: FAST LANE",
        "requires_jd": False,
        "bullets": [
            "Performs a deep-tech talent audit across all IT domains with strict metric validation.",
            "Audits quantitative claims for resource parameters, timeline scopes, and scaling bounds.",
            "Generates a Multi-Domain Capability Matrix mapping you to all roles where you meet >=70% fit."
        ]
    },
    2: {
        "title": "Resume vs Job Description (JD) Match & Multi-Pipeline Fit",
        "path": "PATH A: FAST LANE",
        "requires_jd": True,
        "bullets": [
            "Compares your resume directly against a target job description across domains.",
            "Calculates ATS match score, audits metric claims, and flags missing keywords.",
            "Rewrites weak resume bullets into high-impact 'Action + Tool + Scaled Metric' format."
        ]
    },
    3: {
        "title": "Strict Non-Repeated Bullet Audit & Metric Integrity",
        "path": "PATH A: FAST LANE",
        "requires_jd": False,
        "bullets": [
            "Generates an ultra-concise executive summary with zero text duplication.",
            "Flags unanchored metrics lacking environment, timeline, or scaling parameters.",
            "Provides high-priority action items to harden your portfolio immediately."
        ]
    },
    4: {
        "title": "Market Benchmark Strategy & Multi-Domain Roadmap",
        "path": "PATH A: FAST LANE",
        "requires_jd": False,
        "bullets": [
            "Benchmarks your skills against top 5% engineering standards across fields.",
            "Evaluates architectural depth, metric rigor, and multi-domain readiness.",
            "Delivers an actionable 60-day upskilling roadmap broken into 30-day phases."
        ]
    },
    5: {
        "title": "Tailored Cover Letter Generator (Metric-Backed)",
        "path": "PATH A: FAST LANE",
        "requires_jd": True,
        "bullets": [
            "Extracts core requirements from a target Job Description.",
            "Writes a 250-350 word, cliché-free technical cover letter.",
            "Leverages 2 specific resume projects featuring verified tools and scale metrics."
        ]
    },
    6: {
        "title": "Custom Analysis / Chat with Resume (Gatekeeper Agent)",
        "path": "PATH B: SMART LANE",
        "requires_jd": False,
        "bullets": [
            "Accepts any informal question, instruction, or custom query about your resume.",
            "Routes query through the Gatekeeper Agent to auto-optimize token density.",
            "Forces strict metric validation and multi-role parsing rules on custom queries."
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
    """Prints the structured CLI menu with updated choice descriptions."""
    print("\n" + "=" * 80)
    print("           AI RESUME ANALYSIS & ROUTER ENGINE (METRIC & ROLE OPTIMIZED)       ")
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