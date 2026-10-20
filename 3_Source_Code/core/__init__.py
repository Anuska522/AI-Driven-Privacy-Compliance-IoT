"""
Core package for AI-Driven Privacy Compliance in Heterogeneous IoT Environments.
Implements the architecture specified in BCSE318L Data Privacy Case Study.
Author: Anuska Saha (Reg No: 23BCE0167)
"""

from .event_schema import IoTEvent, EventState, DataClass, PolicyAction
from .device_registry import DeviceRegistry, DeviceStatus
from .policy_engine import PolicyEngine, PrivacyPolicy
from .risk_engine import RiskEngine, RiskAssessment
from .edge_controls import EdgePrivacyControls
from .audit_logger import AuditLogger, AuditRecord
from .pipeline import PrivacyCompliancePipeline

__all__ = [
    "IoTEvent",
    "EventState",
    "DataClass",
    "PolicyAction",
    "DeviceRegistry",
    "DeviceStatus",
    "PolicyEngine",
    "PrivacyPolicy",
    "RiskEngine",
    "RiskAssessment",
    "EdgePrivacyControls",
    "AuditLogger",
    "AuditRecord",
    "PrivacyCompliancePipeline"
]
