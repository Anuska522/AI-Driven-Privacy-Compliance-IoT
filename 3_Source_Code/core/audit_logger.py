"""
Auditability and Cryptographic Tamper-Evident Logging Layer.
Corresponds to Section 11.2 and Section 11.7 of the Case Study Manuscript.
"""

import hashlib
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from .event_schema import PolicyAction


class AuditRecord(BaseModel):
    entry_id: int
    event_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    device_id: str
    data_class: str
    purpose_id: Optional[str] = None
    receiver_id: Optional[str] = None
    policy_version: str
    model_version: str
    risk_score: Optional[float] = None
    reason_codes: List[str] = Field(default_factory=list)
    action: PolicyAction
    action_result: str  # "CONFIRMED_BLOCKED", "CONFIRMED_ALLOWED", "HELD_PENDING_REVIEW"
    reviewer_id: Optional[str] = None
    prev_hash: str
    current_hash: str


class AuditLogger:
    """Maintains an append-only, SHA-256 hash-chained immutable audit ledger."""

    def __init__(self):
        self._entries: List[AuditRecord] = []
        self._latest_hash: str = "GENESIS_HASH_00000000000000000000000000000000"

    def compute_hash(self, prev_hash: str, payload_data: Dict[str, Any]) -> str:
        serialized = json.dumps(payload_data, sort_keys=True)
        combined = f"{prev_hash}|{serialized}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def record_decision(
        self,
        event_id: str,
        device_id: str,
        data_class: str,
        purpose_id: Optional[str],
        receiver_id: Optional[str],
        policy_version: str,
        model_version: str,
        risk_score: Optional[float],
        reason_codes: List[str],
        action: PolicyAction,
        action_result: str,
        reviewer_id: Optional[str] = None
    ) -> AuditRecord:
        """Appends a new decision record to the tamper-evident chain."""
        entry_id = len(self._entries) + 1
        timestamp = datetime.now(timezone.utc).isoformat()

        content = {
            "entry_id": entry_id,
            "event_id": event_id,
            "timestamp": timestamp,
            "device_id": device_id,
            "data_class": data_class,
            "purpose_id": purpose_id,
            "receiver_id": receiver_id,
            "policy_version": policy_version,
            "model_version": model_version,
            "risk_score": risk_score,
            "reason_codes": reason_codes,
            "action": str(action),
            "action_result": action_result,
            "reviewer_id": reviewer_id
        }

        current_hash = self.compute_hash(self._latest_hash, content)

        record = AuditRecord(
            entry_id=entry_id,
            event_id=event_id,
            timestamp=timestamp,
            device_id=device_id,
            data_class=data_class,
            purpose_id=purpose_id,
            receiver_id=receiver_id,
            policy_version=policy_version,
            model_version=model_version,
            risk_score=risk_score,
            reason_codes=reason_codes,
            action=action,
            action_result=action_result,
            reviewer_id=reviewer_id,
            prev_hash=self._latest_hash,
            current_hash=current_hash
        )

        self._entries.append(record)
        self._latest_hash = current_hash
        return record

    def verify_chain_integrity(self) -> bool:
        """Verifies cryptographic hash consistency across the entire audit log."""
        expected_prev = "GENESIS_HASH_00000000000000000000000000000000"
        for rec in self._entries:
            if rec.prev_hash != expected_prev:
                return False
            content = {
                "entry_id": rec.entry_id,
                "event_id": rec.event_id,
                "timestamp": rec.timestamp,
                "device_id": rec.device_id,
                "data_class": rec.data_class,
                "purpose_id": rec.purpose_id,
                "receiver_id": rec.receiver_id,
                "policy_version": rec.policy_version,
                "model_version": rec.model_version,
                "risk_score": rec.risk_score,
                "reason_codes": rec.reason_codes,
                "action": str(rec.action),
                "action_result": rec.action_result,
                "reviewer_id": rec.reviewer_id
            }
            computed = self.compute_hash(expected_prev, content)
            if computed != rec.current_hash:
                return False
            expected_prev = rec.current_hash
        return True

    def get_all_records(self) -> List[AuditRecord]:
        return list(self._entries)

    def get_latest_record(self) -> Optional[AuditRecord]:
        return self._entries[-1] if self._entries else None
