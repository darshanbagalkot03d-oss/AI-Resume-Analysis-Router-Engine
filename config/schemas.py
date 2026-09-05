# config/schemas.py
from pydantic import BaseModel, Field
from typing import List

class MetricAudit(BaseModel):
    original_claim: str = Field(description="The numerical or statistical claim made in the resume.")
    has_resource_params: bool = Field(description="True if hardware, dataset size, or environment context is present.")
    has_timeline_scope: bool = Field(description="True if a time bound or duration is specified.")
    has_scaling_bound: bool = Field(description="True if load limits or constraints are specified.")
    validation_status: str = Field(description="Mark as 'Verified' or 'Unverified Metric'")

class RoleMatch(BaseModel):
    role_name: str = Field(description="Title of the technical role matched against candidate's skills.")
    match_score: float = Field(description="Percentage score from 0 to 100 based on tool/skill proof.")
    reasoning: str = Field(description="Brief justification for the role match.")

class SkillProof(BaseModel):
    skill_name: str = Field(description="The extracted tool or framework.")
    has_project_proof: bool = Field(description="True if tied to an active project narrative; False if found only in a static skill list.")
    evidence_snippet: str = Field(description="Short quote or reference showing project context.")

class CandidateEvaluationSchema(BaseModel):
    metrics_audit: List[MetricAudit] = Field(description="Audit of all quantitative claims found.")
    skill_proofs: List[SkillProof] = Field(description="Audit of skills vs project context proof (Flaw A).")
    evaluated_roles: List[RoleMatch] = Field(description="All roles where the candidate meets a minimum skill threshold.")
    adjusted_technical_score: int = Field(description="Formulated final score after metric penalty deductions.")