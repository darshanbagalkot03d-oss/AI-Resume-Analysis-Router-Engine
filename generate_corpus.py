import os
import sys
from dotenv import load_dotenv
from fpdf import FPDF
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ Error: GEMINI_API_KEY missing in .env file.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3-flash-preview"

DOMAINS = {
    "AI_DataScience": "Artificial Intelligence, MLOps, Computer Vision, & Data Engineering",
    "Cloud_DevOps": "Cloud Architecture, DevOps, Site Reliability (SRE), & Infrastructure",
    "Cybersecurity": "SOC Operations, Penetration Testing, IAM, & Security Governance",
    "Software_Embedded": "Embedded Systems, RTOS, C/C++, Full-Stack, & System Architecture"
}

ARCHETYPES = [
    {
        "id": "flaw_a_keyword_stuffer",
        "description": "Dense keyword stuffer. Has a massive list of 30+ tools/frameworks in a 'Skills' block, but zero project bullets or functional execution context."
    },
    {
        "id": "flaw_b_unanchored_metrics",
        "description": "Notebook prototyper or unanchored claimer. Claims '95% accuracy' or '40% latency reduction', but completely lacks hardware parameters, dataset scale, execution duration, or baseline bounds."
    },
    {
        "id": "production_control",
        "description": "High-rigor production engineer. Includes fully anchored metrics with hardware limits (e.g., Raspberry Pi 4B, 8GB RAM, batch size 16), timeline scopes, scaling bounds, and CI/CD container deployment."
    },
    {
        "id": "domain_edge_case",
        "description": "Niche domain specialist (e.g., RTOS/register-level SPI developer for Embedded, or zero-day exploit chain specialist for Pen Testing). Uses deep technical methodology rather than popular vendor tool listings."
    }
]


class ResumePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def save_text_to_pdf(text: str, output_path: str):
    """Converts raw text into a clean PDF document."""
    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    
    # Sanitize unicode characters for standard FPDF core fonts
    sanitized_text = text.encode("latin-1", "replace").decode("latin-1")
    
    for line in sanitized_text.split("\n"):
        pdf.multi_cell(0, 5, txt=line)
        pdf.ln(1)
        
    pdf.output(output_path)


def generate_synthetic_resumes(count_per_archetype: int = 3):
    """
    Generates synthetic resume PDFs across all domains and archetypes.
    Default: 4 domains x 4 archetypes x 3 variations = 48 synthetic test resumes.
    """
    print("🚀 Starting Synthetic Resume Corpus Generation...\n")
    
    base_dir = "test_corpus"
    os.makedirs(base_dir, exist_ok=True)

    for domain_key, domain_label in DOMAINS.items():
        domain_path = os.path.join(base_dir, domain_key)
        os.makedirs(domain_path, exist_ok=True)
        
        print(f"📁 Processing Domain: {domain_key}")

        for archetype in ARCHETYPES:
            for i in range(1, count_per_archetype + 1):
                file_id = f"{archetype['id']}_v{i}"
                pdf_filename = f"{file_id}.pdf"
                pdf_path = os.path.join(domain_path, pdf_filename)

                if os.path.exists(pdf_path):
                    print(f"  • Skipping existing: {pdf_filename}")
                    continue

                prompt = f"""
Generate a realistic, professional, single-page resume text for a candidate in the domain: '{domain_label}'.

STRICT DESIGN INSTRUCTION:
Create this resume specifically to match the following evaluation test archetype:
Archetype Goal: {archetype['description']}

FORMAT REQUIREMENT:
- Include Candidate Name, Contact Info, Skills, Professional Experience, and Projects.
- Return ONLY the raw resume text. Do not include markdown meta-commentary, code blocks, or preamble.
"""

                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt,
                        config={"temperature": 0.7}
                    )
                    
                    resume_text = response.text.strip()
                    save_text_to_pdf(resume_text, pdf_path)
                    print(f"  ✅ Generated: {pdf_filename}")

                except Exception as e:
                    print(f"  ❌ Failed generating {pdf_filename}: {e}")

    print(f"\n🎉 Corpus generation complete! All files saved to './{base_dir}/'")


if __name__ == "__main__":
    # Adjust count_per_archetype (e.g., 5 = 80 resumes, 7 = 112 resumes)
    generate_synthetic_resumes(count_per_archetype=3)