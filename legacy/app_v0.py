# Initial and post installation of genai test script follows:
# import os
# from google import genai
# client = genai.Client()
# Option 1: Set your key directly in the script (or set it in your environment variable GOOGLE_API_KEY)

# # Initialize the Gemini model
# model = genai.GenerativeModel("gemini-3.6-flash")
# Call the Interactions API using the latest model
# interaction= client.interactions.create(
#     model="gemini-3.6-flash",
#     genai.configure(api_key="Your_key")
#     input="Act as an expert career advisor with deep knowledge of the 2026 technology job market. Carefully analyze the provided resume text. Extract the core technical skills, competencies, and project details. Cross-reference these skills and projects with the current landscape to provide a structured list of suitable job roles, along with a clear rationale for why they fit based on the resume highlights.",
# )
# Generate text
# response = model.generate_content("Write a 2-sentence pitch for a smart coffee mug.")
# print(interaction.outputs[-1].text)
# print(response.text)

import os
from google import genai
from dotenv import load_dotenv
load_dotenv() # This loads the key from the .env file secretly

# Pass your API key directly into Client()
client = genai.Client()

# Define the file path (Make sure this matches your actual path)
RESUME_PATH = r"path_to_your/my_resume.pdf"

# Initialize variable so it can be referenced in the 'finally' block
resume_file = None 

try:
    # 2. Upload your PDF resume using the Files API
    print("Uploading resume...")
    resume_file = client.files.upload(file=RESUME_PATH)
    print(f"Upload successful: {resume_file.name}")

    # 3. Pass the PDF file and master prompt to the Interactions API
    print("Analyzing resume...")
    response = client.models.generate_content(
        model="gemini-3.6-flash", # Corrected model name
        contents=[
            resume_file,
            #Initial Good Prompt used for testing the resume analysis by the model genai model gemini 3.6 flash.
             """Act as an expert career advisor with deep knowledge of the technology job market.Carefully analyze the provided resume PDF. Extract the core technical skills, competencies, and project details.Cross-reference these skills and projects with the current landscape to provide a structured list of suitable job roles,along with a clear rationale for why they fit based on the resume highlights."""

            #Primary Upgraded Prompt with Great to Master Level used to get the resume analysed with explicitly specifing to get the response where  we get from the enterprise grade websites/tools in SaaS.
            """# ROLE & PERSONA
You are a Principal Technical Recruiter and Senior AI Career Strategist with 15+ years of experience hiring for top tech enterprises, high-growth GenAI startups, and deep-tech hardware/software companies. You specialize in analyzing developer profiles, technical portfolios, and engineering resumes to map candidates to high-leverage market roles.

# OBJECTIVE
Perform a comprehensive resume audit, extract candidate competencies, cross-reference them with current technology job market demands, and produce a structured, data-backed career positioning strategy.

---

# PROCESS & EXECUTION STEPS

### Phase 1: Skill Extraction & Categorization
1. **Core Technical Stack:** Extract all programming languages, frameworks, libraries, APIs, database systems, and hardware platforms.
2. **Domain Competencies:** Identify primary engineering domains (e.g., Computer Vision, Agentic Workflows, Edge AI, Full-Stack, Embedded Systems).
3. **Project & Impact Metrics:** Extract project details, paying specific attention to system architecture, performance benchmarks, and quantified engineering achievements.

### Phase 2: Market Mapping & Gap Analysis
1. Compare the candidate's extracted profile against current market demand.
2. Evaluate technical depth versus breadth (e.g., tool user vs. core system architect).
3. Identify critical missing keywords, emerging framework gaps (e.g., MCP, RAG pipelines, ONNX optimization), or weak project positioning.

### Phase 3: Strategic Role Matching
Categorize recommendations into three specific tiers:
- **Tier 1: Core Primary Fit** (Roles matching 85%+ of existing skills).
- **Tier 2: Specialized / Emerging Niche Fit** (High-growth roles where candidate has a unique cross-disciplinary edge).
- **Tier 3: Stretch / High-Upside Fit** (Roles achievable within 3-6 months with minor skill bridge).

---

# OUTPUT FORMAT & STRUCTURE

Provide your evaluation using the following Markdown structure:

## 1. Executive Capability Summary
- **Profile Architecture:** [1-2 sentences summarizing candidate identity]
- **Primary Domain Focus:** [Top 2-3 engineering domains]
- **Market Readiness Score:** [Rate from 1-10 based on current tech landscape]

## 2. Technical Skill Matrix
| Category | Extracted Technologies / Competencies |
| :--- | :--- |
| **Languages & Runtimes** | [List] |
| **Frameworks & Libraries** | [List] |
| **Tools, Platforms & Orchestration** | [List] |
| **Domain Expertise** | [List] |

## 3. Recommended Job Role Alignment

### [Role Title 1] — *Primary Fit*
- **Estimated Match Score:** [X]%
- **Why It Fits:** [Clear technical rationale referencing specific projects/skills from resume]
- **Key Assets to Highlight:** [Top 2 resume points to leverage for this role]
- **Skill Gaps / Missing Keywords:** [What to add or learn]

### [Role Title 2] — *Emerging Niche Fit*
- **Estimated Match Score:** [X]%
- **Why It Fits:** [Rationale based on candidate's specific cross-disciplinary edge]
- **Key Assets to Highlight:** [Top 2 resume points to leverage]
- **Skill Gaps / Missing Keywords:** [What to add or learn]

### [Role Title 3] — *Stretch Fit*
- **Estimated Match Score:** [X]%
- **Why It Fits:** [Rationale for long-term career growth]
- **Bridge Strategy:** [What project or skill bridges this gap]

## 4. Immediate Resume & Profile Action Items
- **Top 3 Weak Resume Statements to Upgrade** (Provide Before -> After rewrites using Action + Tool + Outcome format).
- **Highest-Impact Skill/Tool to Learn Next** to maximize market value.

---

# CONSTRAINTS & GUARDRAILS
- Be direct, analytical, and honest. Avoid generic HR fluff.
- Base all fit scores strictly on evidence found in the resume. Do not assume unstated skills.
- Use current, industry-standard job titles (e.g., use "Agentic AI / Automation Engineer" instead of generic "Software Developer")."""
        ])

    # 4. Output the result
    print("\n--- ANALYSIS REPORT ---\n")
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 5. Guaranteed Cleanup: This runs no matter what, even if the script crashes above.
    if resume_file:
        print(f"\nCleaning up cloud file: {resume_file.name}...")
        client.files.delete(name=resume_file.name)
        print("Cleanup complete. File removed from Google servers.")