"""
Dataset Generator and Exporter.
Populates the 4_Datasets/ directory with comprehensive synthetic IoT streams,
device catalogs, and policy rules matching Appendix C and Appendix D.
"""

import json
import csv
import os
import sys

# Ensure core can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.device_registry import DeviceRegistry
from core.policy_engine import PolicyEngine


def populate_datasets():
    datasets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "4_Datasets"))
    os.makedirs(datasets_dir, exist_ok=True)

    # 1. Devices Catalog
    dev_reg = DeviceRegistry()
    devices_data = [dev.model_dump() for dev in dev_reg._devices.values()]
    dev_path = os.path.join(datasets_dir, "iot_devices_catalog.json")
    with open(dev_path, "w", encoding="utf-8") as f:
        json.dump(devices_data, f, indent=2)
    print(f"[+] Created {dev_path}")

    # 2. Privacy Policies
    pol_engine = PolicyEngine()
    policies_data = [pol.model_dump() for pol in pol_engine._policies.values()]
    pol_path = os.path.join(datasets_dir, "privacy_policies_rules.json")
    with open(pol_path, "w", encoding="utf-8") as f:
        json.dump(policies_data, f, indent=2)
    print(f"[+] Created {pol_path}")

    # 3. Test Cases D-01 through D-12
    test_cases_d = [
        {
            "test_id": "D-01",
            "name": "Valid device and approved receiver",
            "device_id": "DEV-HEALTH-001",
            "data_class": "sensitive_personal",
            "purpose_id": "patient_remote_monitoring",
            "receiver_id": "HOSPITAL_CORE_EHR",
            "expected_action": "allow",
            "expected_status": "CONFIRMED_ALLOWED",
            "description": "Standard authorized tele-health stream passing all checks."
        },
        {
            "test_id": "D-02",
            "name": "Revoked device identity",
            "device_id": "DEV-REVOKED-999",
            "data_class": "sensitive_personal",
            "purpose_id": "patient_remote_monitoring",
            "receiver_id": "HOSPITAL_CORE_EHR",
            "expected_action": "reject",
            "expected_status": "CONFIRMED_REJECTED",
            "description": "Compromised device certificate detected; rejected at perimeter."
        },
        {
            "test_id": "D-03",
            "name": "Missing declared purpose",
            "device_id": "DEV-HEALTH-001",
            "data_class": "sensitive_personal",
            "purpose_id": None,
            "receiver_id": "HOSPITAL_CORE_EHR",
            "expected_action": "hold",
            "expected_status": "CONFIRMED_HELD",
            "description": "Missing purpose metadata holds the transfer for review."
        },
        {
            "test_id": "D-04",
            "name": "Unapproved third-party destination",
            "device_id": "DEV-HEALTH-001",
            "data_class": "sensitive_personal",
            "purpose_id": "patient_remote_monitoring",
            "receiver_id": "THIRD_PARTY_ANALYTICS_CO",
            "expected_action": "block",
            "expected_status": "CONFIRMED_BLOCKED",
            "description": "Receiver not on whitelist violates purpose limitation; blocked."
        },
        {
            "test_id": "D-05",
            "name": "Expired retention limit",
            "device_id": "DEV-HEALTH-001",
            "data_class": "sensitive_personal",
            "purpose_id": "patient_remote_monitoring",
            "receiver_id": "HOSPITAL_CORE_EHR",
            "event_time": "2026-08-01T00:00:00Z",
            "expected_action": "quarantine",
            "expected_status": "CONFIRMED_QUARANTINE",
            "description": "Stale historical record exceeds 14-day healthcare retention window."
        },
        {
            "test_id": "D-06",
            "name": "Unusual high-frequency data burst",
            "device_id": "DEV-CITY-042",
            "data_class": "personal",
            "purpose_id": "traffic_flow_optimization",
            "receiver_id": "CITY_TRAFFIC_CONTROL",
            "payload": {"burst_rate_hz": 75},
            "expected_action": "review",
            "expected_status": "HELD_FOR_HUMAN_REVIEW",
            "description": "Abnormal burst rate triggers high likelihood score, routing to human reviewer."
        },
        {
            "test_id": "D-07",
            "name": "AI Model service timeout / outage",
            "device_id": "DEV-IND-881",
            "data_class": "operational",
            "purpose_id": "predictive_maintenance",
            "receiver_id": "FACTORY_MAINTENANCE_HQ",
            "simulate_model_outage": True,
            "expected_action": "allow",
            "expected_status": "CONFIRMED_ALLOWED",
            "description": "Mandatory rules pass independently even when AI risk scorer is offline."
        },
        {
            "test_id": "D-08",
            "name": "Policy server offline with valid signed local cache",
            "device_id": "DEV-IND-881",
            "data_class": "operational",
            "purpose_id": "predictive_maintenance",
            "receiver_id": "FACTORY_MAINTENANCE_HQ",
            "expected_action": "allow",
            "expected_status": "CONFIRMED_ALLOWED",
            "description": "Edge node executes locally cached signed policy version during disconnection."
        },
        {
            "test_id": "D-09",
            "name": "Policy server offline with expired local policy",
            "device_id": "DEV-HEALTH-001",
            "data_class": "sensitive_personal",
            "simulate_policy_outage": True,
            "expected_action": "hold",
            "expected_status": "CONFIRMED_HELD",
            "description": "Fail-closed principle halts sensitive egress when no valid policy can be verified."
        },
        {
            "test_id": "D-11",
            "name": "Malformed schema missing required identifiers",
            "device_id": "",
            "event_id": "",
            "data_class": "unknown",
            "expected_action": "reject",
            "expected_status": "CONFIRMED_REJECTED",
            "description": "Perimeter drops unidentifiable frame before internal queue processing."
        },
        {
            "test_id": "D-12",
            "name": "Successful edge minimisation and transformation",
            "device_id": "DEV-CITY-042",
            "data_class": "personal",
            "purpose_id": "traffic_flow_optimization",
            "receiver_id": "CITY_TRAFFIC_CONTROL",
            "payload": {"raw_image_frame": "<bytes>", "detected_objects_count": 22, "latitude": 13.082711, "longitude": 80.270722},
            "expected_action": "allow",
            "expected_status": "CONFIRMED_ALLOWED",
            "description": "Edge node strips 4K camera frames, retains aggregate count, and rounds GPS to 2 decimal places."
        }
    ]

    test_path = os.path.join(datasets_dir, "test_cases_d01_to_d12.json")
    with open(test_path, "w", encoding="utf-8") as f:
        json.dump(test_cases_d, f, indent=2)
    print(f"[+] Created {test_path}")

    # 4. Export synthetic_iot_events_1000.json to CSV
    events_json = os.path.join(datasets_dir, "synthetic_iot_events_1000.json")
    if os.path.exists(events_json):
        with open(events_json, "r", encoding="utf-8") as f:
            events = json.load(f)

        csv_path = os.path.join(datasets_dir, "synthetic_iot_events_1000.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "event_id", "device_id", "event_type", "data_class",
                "purpose_id", "receiver_id", "retention_class",
                "policy_version", "model_version", "ground_truth", "payload_summary"
            ])
            for e in events:
                writer.writerow([
                    e["event_id"],
                    e["device_id"],
                    e["event_type"],
                    e["data_class"],
                    e.get("purpose_id", ""),
                    e.get("receiver_id", ""),
                    e.get("retention_class", ""),
                    e.get("policy_version", ""),
                    e.get("model_version", ""),
                    e.get("ground_truth", ""),
                    json.dumps(e.get("payload", {}))
                ])
        print(f"[+] Created {csv_path}")

    # 5. README for Datasets matching Data Availability statement
    readme_path = os.path.join(datasets_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""# Supplementary Datasets: AI-Driven Privacy Compliance

**Author**: Anuska Saha (Reg. No.: 23BCE0167)  
**Course**: BCSE318L - Data Privacy  
**Faculty**: Dr M Rajasekhara Babu  
**Institution**: School of Computer Science and Engineering, Vellore Institute of Technology (VIT)

---

## Data Availability Statement
> All synthetic data generated and analyzed during this study are included in this published supplementary dataset archive. No private, field, or empirical patient records were collected or disclosed. All experimental data adhere to privacy-by-design principles, de-identification, and reproducible synthetic generation protocols.

---

## Dataset Inventory

| File Name | Format | Records | Description |
|---|---|---|---|
| `synthetic_iot_events_1000.json` | JSON | 1,000 | Multi-domain synthetic IoT event stream with ground truth labels. |
| `synthetic_iot_events_1000.csv` | CSV | 1,000 | Flat tabular representation of the 1,000 event benchmark stream. |
| `test_cases_d01_to_d12.json` | JSON | 11 | Complete test vectors verifying Appendix D compliance cases. |
| `iot_devices_catalog.json` | JSON | 6 | Trusted device registry containing active, revoked, and legacy devices. |
| `privacy_policies_rules.json` | JSON | 4 | Formal machine-readable compliance policies (Healthcare, City, Factory, Public). |

---

## Field Dictionary (Appendix C Specification)
- `event_id`: Unique persistent identifier for the sensor transaction.
- `device_id`: Hardware reference linked to onboarding certificate.
- `event_type`: Categorization (`sensor_telemetry`, `biometric_stream`, `traffic_count`).
- `data_class`: Sensitivity hierarchy (`public`, `operational`, `personal`, `sensitive_personal`).
- `purpose_id`: Approved processing intention (e.g. `patient_remote_monitoring`).
- `receiver_id`: Target destination service identifier.
- `retention_class`: Governed maximum retention window.
- `payload`: Sensor metrics (subject to edge data minimisation and precision reduction).
""")
    print(f"[+] Created {readme_path}")


if __name__ == "__main__":
    populate_datasets()
