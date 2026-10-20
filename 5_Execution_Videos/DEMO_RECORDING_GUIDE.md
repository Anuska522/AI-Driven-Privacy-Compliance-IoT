# Project Demonstration & Execution Video Guide

**Project Title**: AI-Driven Privacy Compliance in Heterogeneous IoT Environments  
**Course**: BCSE318L Data Privacy  
**Student**: Anuska Saha | **Registration No.**: 23BCE0167 | **Team ID**: 26FSDPYCPMID1029  
**Faculty Evaluator**: Dr M Rajasekhara Babu | SCOPE, VIT Vellore  

---

## 📹 Video Requirements Checklist
According to the Case Study Guidelines:
- [ ] Clear narration explaining the project, problem, and results.
- [ ] Live execution of the compliance pipeline and test cases.
- [ ] Demonstration of data minimisation, AI risk scoring, and tamper-evident audit logs.
- [ ] Save the recorded file (e.g., `Execution_Video_23BCE0167.mp4`) inside this `5_Execution_Videos/` folder.

---

## ⚡ How to Record on Windows (Fastest Method)
You can record your screen with high quality in 1 shortcut using Windows built-in screen recorder:
1. Open PowerShell / Command Prompt and your browser.
2. Press **`Win + Alt + R`** to start recording immediately (or press **`Win + G`** to open Xbox Game Bar and click Record).
3. Ensure your microphone is unmuted if you wish to narrate your demo.
4. When finished, press **`Win + Alt + R`** again to stop.
5. The video is saved to `C:\Users\Anuska saha\Videos\Captures`. Simply copy it into this `5_Execution_Videos/` folder!

---

## 🎙️ Suggested 3-Minute Video Script (Talk Track)

### 0:00 - 0:30 | Introduction
> *"Hello respected Dr. Rajasekhara Babu sir and evaluators. My name is Anuska Saha, registration number 23BCE0167, presenting my Data Privacy case study on 'AI-Driven Privacy Compliance in Heterogeneous IoT Environments'. Today I will demonstrate the working implementation of the 10-step compliance pipeline specified in Appendix B of my manuscript."*

### 0:30 - 1:15 | Part 1: Automated Unit & Acceptance Test Matrix (Appendix D)
*Run command in terminal:*
```bash
python -m pytest tests -v
```
> *"First, let us run our automated verification suite covering Test Cases D-01 through D-12 and the Table 11 mathematical risk formulas. Notice that all 11 test vectors pass with 100% precision. The pipeline validates device onboarding, drops revoked credentials before AI scoring, catches missing metadata, blocks unauthorized third-party receivers, and enforces retention limits."*

### 1:15 - 2:00 | Part 2: Terminal Execution & Data Minimisation Demo
*Run command in terminal:*
```bash
python run_demo.py
```
> *"Here in `run_demo.py`, we observe 5 canonical IoT scenarios across Healthcare, Smart Cities, and Industry:
> 1. In Scenario 1 (Wearable Telemetry), edge minimisation automatically pseudonymizes direct patient names, reduces high-frequency ECG microvolts into summary metrics, and truncates GPS coordinates from 6 decimals to 2 decimals (~1.1 km resolution).
> 2. In Scenario 2, a revoked device certificate is instantly rejected at perimeter with 0.1 ms latency.
> 3. In Scenario 5, smart city surveillance discards raw 4K camera frames while preserving aggregate vehicle counts for urban planning.
> 4. Notice that every single event is cryptographically linked into an immutable SHA-256 audit ledger, confirming zero tampering."*

### 2:00 - 2:45 | Part 3: Interactive Streamlit Dashboard Walkthrough
*Run command in terminal:*
```bash
streamlit run dashboard/app.py
```
> *(Show the web browser UI on screen)*
> *"Now let's open our interactive Web Compliance Dashboard:
> - On Tab 1, we can inspect live event ingestion, dynamically tune Equation 1 risk parameters (Impact, Likelihood, Uncertainty), and view real-time state transitions and explainability reason codes.
> - On Tab 2, we view the Comparative Benchmarks comparing Manual Review, Rules-Only, Central AI, and our Proposed Hybrid framework. Our hybrid model achieves 100% precision on mandatory rules with sub-millisecond edge latency.
> - On Tab 3, we can verify the cryptographic SHA-256 audit ledger. If we simulate a malicious attacker modifying an audit record, the system immediately flags an integrity breach."*

### 2:45 - 3:00 | Conclusion
> *"In conclusion, this framework bridges deterministic legal policy compliance with AI-driven uncertainty estimation while preserving user privacy at the edge. Thank you!"*
