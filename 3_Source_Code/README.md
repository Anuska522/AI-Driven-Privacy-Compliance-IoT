# AI-Driven Privacy Compliance in Heterogeneous IoT Environments

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/pytest-11%20passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-Academic%20Research-purple.svg)]()
[![Course](https://img.shields.io/badge/Course-BCSE318L%20Data%20Privacy-orange.svg)]()

> Reference implementation and evaluation framework accompanying the Case Study:  
> **"AI-Driven Privacy Compliance in Heterogeneous IoT Environments"**  
> **Author**: Anuska Saha (Reg. No.: 23BCE0167)  
> **Faculty Guide**: Dr M Rajasekhara Babu  
> **Institution**: School of Computer Science and Engineering, Vellore Institute of Technology (VIT), Vellore, India  

---

## 📌 Architecture Overview

This software implements the 10-step reference privacy compliance pipeline specified in **Appendix B** and **Figure 1** of the manuscript:

```
[IoT Sources] -> [Secure Gateway] -> [Edge Privacy Controls] -> [AI Risk Engine & Policy Engine] -> [Audit Ledger]
```

### Core Tenets:
1. **Deterministic Rule Supremacy**: Hard policy rules (revoked credentials, unapproved receivers, expired retention) fail-closed; AI risk scores cannot override mandatory prohibitions.
2. **Edge Data Minimisation**: Payload stripping, pseudonymization, and GPS coordinate rounding occur at the local gateway prior to network egress.
3. **AI Risk Quantification**: Dynamic risk ranking using Equation (1):  
   $$R = 100 \times (0.40 \cdot I + 0.35 \cdot L + 0.25 \cdot U)$$
4. **Cryptographic Tamper-Evident Auditability**: Append-only SHA-256 hash chains ensure verifiable decision provenance without storing raw sensitive payloads.

---

## 📁 Repository Structure

```
3_Source_Code/
├── core/
│   ├── __init__.py
│   ├── event_schema.py        # IoT event models & validation (Appendix C)
│   ├── device_registry.py     # Hardware onboarding & revocation (Section 6.1)
│   ├── policy_engine.py       # Mandatory rule enforcement (Section 9, Table 6)
│   ├── edge_controls.py       # Minimisation & GPS rounding (Section 10.1)
│   ├── risk_engine.py         # AI risk scoring & uncertainty (Section 8)
│   ├── audit_logger.py        # Immutable SHA-256 chained audit logs (Section 11)
│   └── pipeline.py            # FUNCTION process_event reference pipeline (App B)
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py       # Full test suite verifying Cases D-01 to D-12
├── benchmark/
│   ├── run_experiments.py     # 1,000-event comparative benchmark runner
│   ├── populate_datasets.py   # Dataset generation & JSON/CSV export
│   └── benchmark_summary.json # Empirical benchmark metrics
├── dashboard/
│   └── app.py                 # Interactive Streamlit Web Demonstration
├── run_demo.py                # Standalone CLI interactive test runner
└── requirements.txt
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed:
```bash
python --version
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Run Automated Unit & Acceptance Tests (Appendix D)
```bash
python -m pytest tests -v
```
*Expected Result: 11 tests passing (D-01 to D-12, Table 11 mathematical calculations, cryptographic chain verification).*

### 4. Run Terminal Demo
```bash
python run_demo.py
```

### 5. Launch Interactive Web Dashboard
```bash
streamlit run dashboard/app.py
```
Open your browser at `http://localhost:8501` to test custom events, adjust risk weights, inspect edge minimisations, and verify audit integrity.

### 6. Run Comparative Benchmark Experiments
```bash
python benchmark/run_experiments.py
```

---

## 📊 Summary of Benchmark Results

| Architecture | Precision | Recall | F1-Score | FPR | Median Latency | Compliance Coverage | Audit Completeness |
|---|---|---|---|---|---|---|---|
| **Rules-Only** | 1.0000 | 0.7033 | 0.8258 | 0.0000 | 0.66 ms | 100.0% | 85.0% |
| **Proposed Hybrid** | **1.0000** | **0.7480** | **0.8558** | **0.0000** | **0.05 ms** | **100.0%** | **100.0%** |
| **Centralized AI** | 0.7917 | 0.9268 | 0.8539 | 0.0796 | 65.08 ms | 88.0% | 90.0% |
| **Manual Review** | 0.8538 | 0.8780 | 0.8657 | 0.0491 | 400.62 ms | 92.0% | 70.0% |

---

## 📜 Citation & Academic Notice
This implementation is created for academic research in partial fulfillment of the course **BCSE318L Data Privacy** at **Vellore Institute of Technology (VIT)**.
