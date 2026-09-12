# config/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field


# =====================================================================
# SHARED SUB-MODELS (Used across multiple schemas)
# =====================================================================

class MetricAuditItem(BaseModel):
    original_claim: str = Field(description="The exact numerical claim extracted from the resume.")
    resource_parameters_present: bool = Field(description="Whether compute, memory, budget, or team resource parameters are specified.")
    timeline_scope_present: bool = Field(description="Whether a specific timeframe or duration is specified.")
    scaling_bounds_present: bool = Field(description="Whether initial vs final scale metrics are specified.")
    validation_status: str = Field(description="'Verified Metric' or 'Unverified Metric (-15 pts)'")
    penalty_note: Optional[str] = Field(default="", description="Reason for penalty if unverified.")


class SkillProof(BaseModel):
    skill_name: str = Field(description="The tool, framework, or skill evaluated.")
    category: str = Field(description="e.g., Languages, Frameworks, Cloud, Hardware")
    is_anchored_in_project: bool = Field(description="True if proven within an active project description; False if keyword-stuffed.")
    project_context: Optional[str] = Field(default=None, description="Description of functional application if anchored.")


class EvaluatedRoleMatch(BaseModel):
    domain_category: str = Field(description="Target technical domain.")
    matched_role_title: str = Field(description="Specific job title.")
    match_score_percentage: float = Field(description="Match score percentage (0 to 100).")
    evidence_rationale: str = Field(description="Resume proof supporting the match score.")


# =====================================================================
# PROMPT CASE 1: Baseline Talent Audit Schema
# =====================================================================

class CandidateEvaluationSchema(BaseModel):
    candidate_profile_identity: str = Field(description="1-2 sentences capturing core technical focus.")
    market_readiness_score: float = Field(description="Overall market readiness score from 1.0 to 10.0.")
    primary_technical_differentiators: List[str] = Field(description="Top 3 key technical strengths.")
    skill_proofs: List[SkillProof] = Field(description="Verification status for extracted tools/frameworks.")
    metrics_audit: List[MetricAuditItem] = Field(description="Flaw B audit for all quantitative claims.")
    evaluated_roles: List[EvaluatedRoleMatch] = Field(description="Flaw C mapping for roles with >=70% match.")
    missing_market_skills: List[str] = Field(description="Missing tools/skills needed for market alignment.")
    adjusted_technical_score: int = Field(description="Final score out of 100 after applying Flaw A & B penalties.")


# =====================================================================
# PROMPT CASE 2: ATS Optimization & JD Match Schema
# =====================================================================

class BulletRewrite(BaseModel):
    original_bullet: str = Field(description="Original weak or unanchored resume bullet.")
    ats_rewritten_bullet: str = Field(description="Rewritten bullet in Action + Tool + Quantified Outcome format.")


class ATSEvaluationSchema(BaseModel):
    overall_ats_match_score: float = Field(description="ATS match score percentage (0 to 100).")
    keyword_density_score: str = Field(description="High, Medium, or Low.")
    summary_assessment: str = Field(description="2 sentences summarizing alignment with Target JD.")
    metrics_audit: List[MetricAuditItem] = Field(description="Flaw B audit for quantitative claims.")
    missing_required_technologies: List[str] = Field(description="Skills present in Target JD but missing from resume.")
    missing_architectural_keywords: List[str] = Field(description="Missing domain workflows or architectural concepts.")
    formatting_recommendations: List[str] = Field(description="Updates required to improve ATS parsing.")
    bullet_rewrites: List[BulletRewrite] = Field(description="Top 3 weak bullets rewritten for ATS alignment.")


# =====================================================================
# PROMPT CASE 3: Principal Software Architect Schema
# =====================================================================

class ArchitectEvaluationSchema(BaseModel):
    primary_languages: List[str] = Field(description="Unique list of core programming languages.")
    core_frameworks_tools: List[str] = Field(description="Unique list of verified frameworks and tools.")
    hardware_edge_exposure: List[str] = Field(description="Unique list of hardware/edge devices or zero if none.")
    unanchored_claims_flagged: List[str] = Field(description="Quantitative claims lacking resource, timeline, or scale bounds.")
    adjusted_technical_score: int = Field(description="Score out of 100 after metric penalties.")
    qualified_technical_roles: List[str] = Field(description="All roles across IT domains meeting >=70% match.")
    code_portfolio_action_items: List[str] = Field(description="Immediate engineering updates to execute.")


# =====================================================================
# PROMPT CASE 4: CTO & Tech Career Strategist Schema
# =====================================================================

class BenchmarkDimension(BaseModel):
    dimension_name: str = Field(description="e.g., Agentic Architecture, Model Deployment, Evaluation Frameworks")
    top_5_percent_standard: str = Field(description="Industry standard for top performers.")
    candidate_current_level: str = Field(description="Current observed proficiency level of candidate.")
    gap_severity: str = Field(description="High, Medium, or Low.")


class CTOStrategyEvaluationSchema(BaseModel):
    benchmark_matrix: List[BenchmarkDimension] = Field(description="Comparison against top 5% candidate standard.")
    primary_domain_fits: List[str] = Field(description="Roles meeting high proficiency thresholds.")
    adjacent_domain_fits: List[str] = Field(description="Roles meeting secondary qualification thresholds.")
    phase_1_30_day_milestone: str = Field(description="Primary focus for Days 1-30.")
    phase_1_tasks_deliverable: List[str] = Field(description="Specific tools to build and GitHub deliverable.")
    phase_2_60_day_milestone: str = Field(description="Secondary focus for Days 31-60.")
    phase_2_tasks_deliverable: List[str] = Field(description="Specific system architecture to deploy.")


# =====================================================================
# PROMPT CASE 5: Senior Engineering Copywriter Schema
# =====================================================================

class CoverLetterEvaluationSchema(BaseModel):
    candidate_full_name: str = Field(description="Candidate's full name.")
    target_role_title: str = Field(description="Target position title from JD.")
    verified_metrics_used: List[str] = Field(description="Only verified metrics with resource/scale bounds used in letter.")
    projects_highlighted: List[str] = Field(description="Top 2 active projects featured in the letter.")
    cover_letter_text: str = Field(description="Full 250-350 word evidence-backed technical cover letter.")