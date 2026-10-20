"""
Interactive Demonstration and Test Runner.
Executes the AI-Driven Privacy Compliance Pipeline across canonical IoT events.
Author: Anuska Saha (Reg. No.: 23BCE0167)
"""

import os
import sys
import time
import json
from datetime import datetime, timezone

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from core.event_schema import IoTEvent, DataClass, PolicyAction
from core.pipeline import PrivacyCompliancePipeline
from core.risk_engine import RiskEngine


def print_banner():
    print("=" * 80)
    print("   AI-DRIVEN PRIVACY COMPLIANCE IN HETEROGENEOUS IoT ENVIRONMENTS")
    print("   BCSE318L Data Privacy - Vellore Institute of Technology (VIT)")
    print("   Student: Anuska Saha | Reg No: 23BCE0167 | Team ID: 26FSDPYCPMID1029")
    print("   Course Faculty: Dr M Rajasekhara Babu")
    print("=" * 80)


def demo_pipeline_execution():
    pipeline = PrivacyCompliancePipeline()

    test_scenarios = [
        {
            "title": "Scenario 1: Authorized Smart Healthcare Telemetry (Case D-01)",
            "event": IoTEvent(
                event_id="EVT-HEALTH-001",
                device_id="DEV-HEALTH-001",
                data_class=DataClass.SENSITIVE_PERSONAL,
                purpose_id="patient_remote_monitoring",
                receiver_id="HOSPITAL_CORE_EHR",
                payload={
                    "heart_rate": 82,
                    "patient_name": "Aarav Sharma",
                    "latitude": 12.971598,
                    "longitude": 79.158521,
                    "raw_ecg_waveform": [0.12, 0.45, 1.25, -0.32, 0.05]
                }
            )
        },
        {
            "title": "Scenario 2: Malicious / Revoked IoT Device Ingestion (Case D-02)",
            "event": IoTEvent(
                event_id="EVT-REVOKED-002",
                device_id="DEV-REVOKED-999",
                data_class=DataClass.SENSITIVE_PERSONAL,
                purpose_id="patient_remote_monitoring",
                receiver_id="HOSPITAL_CORE_EHR"
            )
        },
        {
            "title": "Scenario 3: Missing Purpose Metadata (Case D-03)",
            "event": IoTEvent(
                event_id="EVT-NOPURP-003",
                device_id="DEV-HEALTH-001",
                data_class=DataClass.SENSITIVE_PERSONAL,
                purpose_id="",  # Missing purpose!
                receiver_id="HOSPITAL_CORE_EHR"
            )
        },
        {
            "title": "Scenario 4: Unapproved Commercial Analytics Egress (Case D-04)",
            "event": IoTEvent(
                event_id="EVT-ILLEGAL-004",
                device_id="DEV-HEALTH-001",
                data_class=DataClass.SENSITIVE_PERSONAL,
                purpose_id="patient_remote_monitoring",
                receiver_id="THIRD_PARTY_ANALYTICS_CO"  # Explicitly forbidden!
            )
        },
        {
            "title": "Scenario 5: Smart City Traffic Camera Data Minimisation (Case D-12)",
            "event": IoTEvent(
                event_id="EVT-CITY-005",
                device_id="DEV-CITY-042",
                data_class=DataClass.PERSONAL,
                purpose_id="traffic_flow_optimization",
                receiver_id="CITY_TRAFFIC_CONTROL",
                payload={
                    "raw_image_frame": "<BASE64_4K_SURVEILLANCE_IMAGE_DATA>",
                    "detected_objects_count": 34,
                    "latitude": 13.082680,
                    "longitude": 80.270718
                }
            )
        }
    ]

    for idx, sc in enumerate(test_scenarios, 1):
        print(f"\n[>>>] {sc['title']}")
        evt = sc["event"]
        print(f"      Device: {evt.device_id} | Class: {evt.data_class} | Purpose: {evt.purpose_id} | Receiver: {evt.receiver_id}")
        
        # Show raw payload before minimisation
        if evt.payload:
            print(f"      Raw Payload Ingested: {json.dumps(evt.payload)}")

        # Execute reference compliance pipeline (Appendix B)
        resp = pipeline.process_event(evt)

        # Print decision
        action_symbol = "[PASS] ALLOWED" if resp.action == PolicyAction.ALLOW else f"[BLOCKED] {resp.action.upper()}"
        print(f"      [RESULT] ==> {action_symbol}")
        print(f"      Execution State: {resp.event.state}")
        print(f"      Explanation: {resp.explanation}")

        if resp.risk_assessment:
            b = resp.risk_assessment.breakdown
            print(f"      AI Risk Score: {resp.risk_assessment.score}/100 [{resp.risk_assessment.risk_band} RISK]")
            print(f"        -> Formula: 100 * (0.40 * {b.impact_raw} + 0.35 * {b.likelihood_raw} + 0.25 * {b.uncertainty_raw})")
            print(f"        -> Breakdown: Impact={b.impact_weighted} pts, Likelihood={b.likelihood_weighted} pts, Uncertainty={b.uncertainty_weighted} pts")

        if resp.event.provenance and resp.event.provenance.transformations_applied:
            print(f"      Edge Minimisation Applied:")
            for t in resp.event.provenance.transformations_applied:
                print(f"        * {t}")
            print(f"      Clean Payload Egress: {json.dumps(resp.event.payload)}")

        if resp.audit_record:
            print(f"      Immutable Audit Hash: {resp.audit_record.current_hash[:24]}...")
        print(f"      Pipeline Latency: {resp.latency_ms:.3f} ms")
        time.sleep(0.05)

    print("\n" + "=" * 80)
    print(" [OK] Cryptographic Tamper-Evidence Verification:")
    is_valid = pipeline.audit_logger.verify_chain_integrity()
    print(f"     Audit Ledger Integrity: {'VALID (Zero Tampering Detected)' if is_valid else 'TAMPERED'}")
    print(f"     Total Audited Blocks: {len(pipeline.audit_logger.get_all_records())}")
    print("=" * 80)


def main():
    print_banner()
    demo_pipeline_execution()
    print("\nDemo execution complete. For comprehensive benchmarks run: python benchmark/run_experiments.py")
    print("To launch the interactive Web Dashboard run: streamlit run dashboard/app.py\n")


if __name__ == "__main__":
    main()
