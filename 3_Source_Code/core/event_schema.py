"""
Event Schema and Data Dictionary implementation.
Corresponds to Appendix C and Section 6.2 of the Case Study Manuscript.
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone


class DataClass(str, Enum):
    PUBLIC = "public"
    OPERATIONAL = "operational"
    PERSONAL = "personal"
    SENSITIVE_PERSONAL = "sensitive_personal"
    UNKNOWN = "unknown"


class PolicyAction(str, Enum):
    ALLOW = "allow"
    MINIMISE = "minimise"
    TRANSFORM = "transform"
    BLOCK = "block"
    HOLD = "hold"
    REVIEW = "review"
    QUARANTINE = "quarantine"
    REJECT = "reject"


class EventState(str, Enum):
    RECEIVED = "RECEIVED"
    VALIDATED = "VALIDATED"
    CLASSIFIED = "CLASSIFIED"
    POLICY_CHECKED = "POLICY_CHECKED"
    RISK_REVIEWED = "RISK_REVIEWED"
    ACTIONED = "ACTIONED"
    LOGGED = "LOGGED"
    # Failure & intermediate states
    REJECTED_INVALID_SCHEMA = "REJECTED_INVALID_SCHEMA"
    REJECTED_INVALID_DEVICE = "REJECTED_INVALID_DEVICE"
    HELD_MISSING_PURPOSE = "HELD_MISSING_PURPOSE"
    BLOCKED_RECEIVER = "BLOCKED_RECEIVER"
    BLOCKED_RETENTION_EXPIRED = "BLOCKED_RETENTION_EXPIRED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ProvenanceRecord(BaseModel):
    original_source: str
    transformations_applied: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IoTEvent(BaseModel):
    event_id: str
    device_id: str
    event_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = "telemetry"
    data_class: DataClass = DataClass.UNKNOWN
    purpose_id: Optional[str] = None
    receiver_id: Optional[str] = None
    retention_class: Optional[str] = "30_days"
    policy_version: Optional[str] = "1.0"
    model_version: Optional[str] = "risk-eval-v1"
    risk_score: Optional[float] = None
    reason_codes: List[str] = Field(default_factory=list)
    action: Optional[PolicyAction] = None
    action_status: Optional[str] = "pending"
    reviewer_id: Optional[str] = None
    state: EventState = EventState.RECEIVED
    payload: Dict[str, Any] = Field(default_factory=dict)
    provenance: Optional[ProvenanceRecord] = None

    model_config = ConfigDict(use_enum_values=True)
