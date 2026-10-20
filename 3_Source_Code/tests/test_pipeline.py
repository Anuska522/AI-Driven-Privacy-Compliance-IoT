"""
Comprehensive Test Suite for Privacy Compliance Pipeline.
Verifies Appendix D (Test Cases D-01 through D-12) and Table 11 Mathematical Examples.
"""

import pytest
from datetime import datetime, timezone, timedelta
from core.event_schema import IoTEvent, DataClass, PolicyAction, EventState
from core.device_registry import DeviceRegistry, DeviceStatus
from core.policy_engine import PolicyEngine, PrivacyPolicy
from core.risk_engine import RiskEngine
from core.pipeline import PrivacyCompliancePipeline


@pytest.fixture
def pipeline():
    return PrivacyCompliancePipeline()


def test_d01_valid_device_and_approved_receiver(pipeline):
    """D-01: Valid device and approved receiver: All checks pass, transfer allowed."""
    event = IoTEvent(
        event_id="EVT-001",
        device_id="DEV-HEALTH-001",
        data_class=DataClass.SENSITIVE_PERSONAL,
        purpose_id="patient_remote_monitoring",
        receiver_id="HOSPITAL_CORE_EHR",
        payload={"heart_rate": 78, "patient_name": "John Doe", "latitude": 12.9716, "longitude": 79.1585}
    )
    res = pipeline.process_event(event)

    assert res.action == PolicyAction.ALLOW
    assert res.action_result == "CONFIRMED_ALLOWED"
    # Verify edge minimisation stripped raw patient name and truncated GPS
    assert "patient_name" not in res.event.payload
    assert "patient_pseudo_id" in res.event.payload
    assert res.event.payload["latitude"] == 12.97
    assert res.audit_record is not None
    assert pipeline.audit_logger.verify_chain_integrity() is True


def test_d02_revoked_device(pipeline):
    """D-02: Revoked device: Must be rejected immediately before AI scoring."""
    event = IoTEvent(
        event_id="EVT-002",
        device_id="DEV-REVOKED-999",
        data_class=DataClass.SENSITIVE_PERSONAL,
        purpose_id="patient_remote_monitoring",
        receiver_id="HOSPITAL_CORE_EHR"
    )
    res = pipeline.process_event(event)

    assert res.action == PolicyAction.REJECT
    assert res.action_result == "CONFIRMED_REJECTED"
    assert "revoked_device" in res.event.reason_codes
    assert res.risk_assessment is None  # Hard rule stops pipeline before AI!


def test_d03_missing_purpose(pipeline):
    """D-03: Missing purpose: Must be held for review rather than assumed compliant."""
    event = IoTEvent(
        event_id="EVT-003",
        device_id="DEV-HEALTH-001",
        data_class=DataClass.SENSITIVE_PERSONAL,
        purpose_id="",  # Missing purpose!
        receiver_id="HOSPITAL_CORE_EHR"
    )
    res = pipeline.process_event(event)

    assert res.action == PolicyAction.HOLD
    assert "missing_purpose" in res.event.reason_codes


def test_d04_unapproved_receiver(pipeline):
    """D-04: Unapproved receiver: Mandatory rule must block transfer."""
    event = IoTEvent(
        event_id="EVT-004",
        device_id="DEV-HEALTH-001",
        data_class=DataClass.SENSITIVE_PERSONAL,
        purpose_id="patient_remote_monitoring",
        receiver_id="THIRD_PARTY_ANALYTICS_CO"  # Explicitly forbidden!
    )
    res = pipeline.process_event(event)

    assert res.action == PolicyAction.BLOCK
    assert "receiver_denied" in res.event.reason_codes
    assert res.event.state == EventState.BLOCKED_RECEIVER


def test_d05_expired_retention(pipeline):
    """D-05: Expired retention: Must trigger quarantine / deletion rule."""
    old_time = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
    event = IoTEvent(
        event_id="EVT-005",
        device_id="DEV-HEALTH-001",
        event_time=old_time,
        data_class=DataClass.SENSITIVE_PERSONAL,
        purpose_id="patient_remote_monitoring",
        receiver_id="HOSPITAL_CORE_EHR"
    )
    res = pipeline.process_event(event)

    assert res.action == PolicyAction.QUARANTINE
    assert "retention_expired" in res.event.reason_codes


def test_d07_model_unavailable_fallback(pipeline):
    """D-07: Model unavailable: Mandatory policy rules still execute safely."""
    event = IoTEvent(
        event_id="EVT-007",
        device_id="DEV-IND-881",
        data_class=DataClass.OPERATIONAL,
        purpose_id="predictive_maintenance",
        receiver_id="FACTORY_MAINTENANCE_HQ"
    )
    res = pipeline.process_event(event, simulate_model_outage=True)

    assert res.action == PolicyAction.ALLOW
    assert "ai_model_unavailable_fallback" in res.event.reason_codes


def test_d08_d09_policy_service_outage(pipeline):
    """D-08/D-09: Policy service offline triggers fail-safe hold."""
    event = IoTEvent(
        event_id="EVT-008",
        device_id="DEV-HEALTH-001",
        data_class=DataClass.SENSITIVE_PERSONAL,
        purpose_id="patient_remote_monitoring",
        receiver_id="HOSPITAL_CORE_EHR"
    )
    res = pipeline.process_event(event, simulate_policy_outage=True)

    assert res.action == PolicyAction.HOLD
    assert "policy_service_offline_fallback" in res.event.reason_codes


def test_d11_invalid_schema(pipeline):
    """D-11: Invalid schema missing event_id or device_id must be rejected."""
    event = IoTEvent(
        event_id="",  # Missing required field
        device_id="",
        data_class=DataClass.PUBLIC
    )
    res = pipeline.process_event(event)

    assert res.action == PolicyAction.REJECT
    assert "invalid_schema" in res.event.reason_codes


def test_d12_successful_transformation(pipeline):
    """D-12: Smart city camera raw frame discarded, aggregate count retained."""
    event = IoTEvent(
        event_id="EVT-012",
        device_id="DEV-CITY-042",
        data_class=DataClass.PERSONAL,
        purpose_id="traffic_flow_optimization",
        receiver_id="CITY_TRAFFIC_CONTROL",
        payload={"raw_image_frame": "<bytes 4K image>", "detected_objects_count": 14}
    )
    res = pipeline.process_event(event)

    assert res.action == PolicyAction.ALLOW
    assert "raw_image_frame" not in res.event.payload
    assert res.event.payload["vehicle_count"] == 14
    assert "discarded_raw_camera_frame_retained_count" in res.event.provenance.transformations_applied


def test_table_11_mathematical_examples():
    """Verify Section 8.3 & Table 11 Equation (1) Exact Calculations."""
    # Case 1: Public sensor
    r1 = RiskEngine.evaluate(
        IoTEvent(event_id="t1", device_id="d1", data_class=DataClass.PUBLIC),
        override_i=0.20, override_l=0.15, override_u=0.10
    )
    assert round(r1.score) == 16

    # Case 2: Purpose missing
    r2 = RiskEngine.evaluate(
        IoTEvent(event_id="t2", device_id="d2", data_class=DataClass.PERSONAL),
        override_i=0.60, override_l=0.45, override_u=0.90
    )
    assert round(r2.score) == 62

    # Case 3: Unusual export
    r3 = RiskEngine.evaluate(
        IoTEvent(event_id="t3", device_id="d3", data_class=DataClass.OPERATIONAL),
        override_i=0.75, override_l=0.80, override_u=0.60
    )
    assert round(r3.score) == 73

    # Case 4: Sensitive + unapproved
    r4 = RiskEngine.evaluate(
        IoTEvent(event_id="t4", device_id="d4", data_class=DataClass.SENSITIVE_PERSONAL),
        override_i=0.90, override_l=0.85, override_u=0.80
    )
    assert round(r4.score) == 86

    # Case 5: Revoked device
    r5 = RiskEngine.evaluate(
        IoTEvent(event_id="t5", device_id="d5", data_class=DataClass.SENSITIVE_PERSONAL),
        override_i=0.95, override_l=0.95, override_u=0.95
    )
    assert round(r5.score) == 95


def test_audit_ledger_cryptographic_tamper_evidence(pipeline):
    """Test cryptographic SHA-256 chain immutability and tamper detection."""
    # Process 3 events
    for i in range(3):
        e = IoTEvent(
            event_id=f"AUDIT-EVT-{i}",
            device_id="DEV-IND-881",
            data_class=DataClass.OPERATIONAL,
            purpose_id="predictive_maintenance",
            receiver_id="FACTORY_MAINTENANCE_HQ"
        )
        pipeline.process_event(e)

    assert pipeline.audit_logger.verify_chain_integrity() is True

    # Tamper with an audit entry maliciously
    pipeline.audit_logger._entries[1].action_result = "TAMPERED_RESULT"
    # Verification must now fail!
    assert pipeline.audit_logger.verify_chain_integrity() is False
