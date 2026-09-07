"""
FastAPI Application Entry Point
Goated Tech - Smart India Hackathon 2026 (Problem Statement 26154)
National Technical Research Organisation (NTRO)
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json

from .models import TransformationRequest, TransformationResponse
from .pipeline import execute_transformation_pipeline
from .blockchain import ledger

app = FastAPI(
    title="NTRO GenAI Content Transformation Platform",
    description="Secure Blockchain-Backed Source-Grounded Multimodal Transformation Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "ONLINE",
        "service": "NTRO Content Transformation Engine",
        "team": "Goated Tech",
        "ps_id": "26154",
        "blockchain_height": len(ledger.chain),
        "consensus": "Proof-of-Authority (PoA)"
    }

@app.post("/api/transform", response_model=TransformationResponse)
def transform_content(payload: TransformationRequest):
    try:
        result = execute_transformation_pipeline(payload.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blockchain/ledger")
def get_blockchain_ledger():
    return {
        "total_blocks": len(ledger.chain),
        "chain": [b.to_dict() for b in ledger.chain]
    }

@app.post("/api/blockchain/verify")
def verify_artefact_integrity(data: dict):
    content = data.get("content", "")
    claimed_hash = data.get("claimed_hash")
    if not content and not claimed_hash:
        raise HTTPException(status_code=400, detail="Must provide either content or claimed_hash")
    return ledger.verify_artefact(content, claimed_hash)
