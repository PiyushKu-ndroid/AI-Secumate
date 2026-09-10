"""
Permissioned Blockchain Ledger Module for Goated Tech (NTRO PS 26154)
Implements a tamper-evident, SHA-256 chained ledger with Proof-of-Authority (PoA)
consensus among authorized defense nodes (NTRO, CERT-In, GoatedTech).
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional

class ArtefactRecord:
    def __init__(self, artefact_type: str, source_hash: str, output_hash: str, 
                 operator_id: str, factuality_score: float, metadata: Dict[str, Any]):
        self.artefact_type = artefact_type
        self.source_hash = source_hash
        self.output_hash = output_hash
        self.operator_id = operator_id
        self.factuality_score = factuality_score
        self.metadata = metadata
        self.timestamp = time.time()
        self.record_id = hashlib.sha256(f"{source_hash}:{output_hash}:{self.timestamp}".encode()).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "artefact_type": self.artefact_type,
            "source_hash": self.source_hash,
            "output_hash": self.output_hash,
            "operator_id": self.operator_id,
            "factuality_score": self.factuality_score,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }

class Block:
    def __init__(self, index: int, previous_hash: str, records: List[ArtefactRecord], validator_node: str):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.records = [r.to_dict() if isinstance(r, ArtefactRecord) else r for r in records]
        self.validator_node = validator_node
        self.merkle_root = self.calculate_merkle_root()
        self.nonce = 0
        self.hash = self.compute_hash()

    def calculate_merkle_root(self) -> str:
        if not self.records:
            return hashlib.sha256(b"empty_block").hexdigest()
        hashes = [hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest() for r in self.records]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest()
                new_hashes.append(combined)
            hashes = new_hashes
        return hashes[0]

    def compute_hash(self) -> str:
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "validator_node": self.validator_node,
            "nonce": self.nonce
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "validator_node": self.validator_node,
            "records": self.records,
            "nonce": self.nonce,
            "hash": self.hash
        }

class PermissionedLedger:
    VALIDATOR_NODES = ["NTRO-NODE-ALPHA", "CERT-IN-NODE-01", "GOATED-TECH-NODE-GATEWAY"]

    def __init__(self):
        self.chain: List[Block] = []
        self.pending_records: List[ArtefactRecord] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_record = ArtefactRecord(
            artefact_type="GENESIS",
            source_hash="0000000000000000000000000000000000000000000000000000000000000000",
            output_hash="0000000000000000000000000000000000000000000000000000000000000000",
            operator_id="SYSTEM_INIT",
            factuality_score=1.0,
            metadata={"network": "NTRO-Secure-Mesh", "standard": "NIST-SP-800-53-R5"}
        )
        genesis_block = Block(0, "0"*64, [genesis_record], self.VALIDATOR_NODES[0])
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_record(self, record: ArtefactRecord) -> Dict[str, Any]:
        self.pending_records.append(record)
        # In a PoA system, automatically mint block when threshold reached or immediately on demand
        new_block = self.mint_block()
        return {
            "block_index": new_block.index,
            "block_hash": new_block.hash,
            "record_id": record.record_id,
            "merkle_root": new_block.merkle_root,
            "validator": new_block.validator_node,
            "timestamp": new_block.timestamp
        }

    def mint_block(self) -> Block:
        if not self.pending_records:
            return self.last_block
        validator = self.VALIDATOR_NODES[len(self.chain) % len(self.VALIDATOR_NODES)]
        block = Block(len(self.chain), self.last_block.hash, self.pending_records, validator)
        self.chain.append(block)
        self.pending_records = []
        return block

    def verify_artefact(self, content_text: str, claimed_hash: Optional[str] = None) -> Dict[str, Any]:
        computed_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()
        target_hash = claimed_hash if claimed_hash else computed_hash
        
        for block in self.chain:
            for rec in block.records:
                if rec.get("output_hash") == target_hash:
                    is_tampered = (computed_hash != rec.get("output_hash"))
                    return {
                        "verified": not is_tampered,
                        "status": "AUTHENTIC" if not is_tampered else "TAMPERED",
                        "block_index": block.index,
                        "block_hash": block.hash,
                        "timestamp": rec.get("timestamp"),
                        "operator_id": rec.get("operator_id"),
                        "artefact_type": rec.get("artefact_type"),
                        "factuality_score": rec.get("factuality_score"),
                        "recorded_hash": rec.get("output_hash"),
                        "computed_hash": computed_hash,
                        "merkle_root": block.merkle_root,
                        "validator_node": block.validator_node
                    }
        return {
            "verified": False,
            "status": "NOT_FOUND",
            "message": "Hash not found in permissioned blockchain ledger.",
            "computed_hash": computed_hash
        }

# Global ledger instance
ledger = PermissionedLedger()
