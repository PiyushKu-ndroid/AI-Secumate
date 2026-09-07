"""
Pydantic Data Models & Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class TransformationRequest(BaseModel):
    source_type: str = Field("text", description="text | pdf | audio | video | web")
    source_content: str = Field(..., description="Raw text or parsed input string")
    source_url: Optional[str] = None
    target_audience: str = Field("Executive Leadership", description="Executive, Technical SecOps, Policy, General")
    tone: str = Field("Authoritative & Urgent", description="Tone of the deliverable")
    language: str = Field("English", description="Target language")
    detail_level: str = Field("Balanced", description="Executive Brief | Balanced | Deep Technical")
    communication_objective: str = Field("Threat Mitigation", description="Objective of communication")
    content_style: str = Field("NTRO Official", description="Style preset")
    selected_outputs: List[str] = Field(..., description="List of desired formats: video, linkedin, twitter, advisory, infographic, executive_summary, presentation")
    operator_id: str = Field("OP-NTRO-704", description="Authenticated operator ID for RBAC")

class ArtefactOutput(BaseModel):
    artefact_type: str
    title: str
    content: Any
    sha256_hash: str
    factuality_score: float
    grounded_citations: List[str]
    blockchain_tx: Dict[str, Any]

class TransformationResponse(BaseModel):
    job_id: str
    source_hash: str
    execution_time_ms: float
    fact_extraction: Dict[str, Any]
    artefacts: Dict[str, ArtefactOutput]
