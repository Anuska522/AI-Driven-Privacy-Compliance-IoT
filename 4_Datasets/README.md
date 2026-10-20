# Supplementary Datasets: AI-Driven Privacy Compliance

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
