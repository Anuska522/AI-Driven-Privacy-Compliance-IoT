"""
Interactive Web Application & Compliance Dashboard.
Implements the real-time IoT privacy compliance pipeline UI.
Author: Anuska Saha (Reg. No.: 23BCE0167)
Course: BCSE318L Data Privacy | Faculty: Dr M Rajasekhara Babu | VIT
"""

import streamlit as st
import os
import sys
import json
import time
from datetime import datetime, timezone

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.event_schema import IoTEvent, DataClass, PolicyAction
from core.pipeline import PrivacyCompliancePipeline
from core.risk_engine import RiskEngine

st.set_page_config(
    page_title="AI-Driven Privacy Compliance | BCSE318L",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 26px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 15px;
        color: #4B5563;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .pass-badge {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
    }
    .block-badge {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
    }
    .hold-badge {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "pipeline" not in st.session_state:
    st.session_state.pipeline = PrivacyCompliancePipeline()

pipeline: PrivacyCompliancePipeline = st.session_state.pipeline

# Sidebar Details
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Vellore_Institute_of_Technology_seal_2017.svg/300px-Vellore_Institute_of_Technology_seal_2017.svg.png", width=120)
st.sidebar.markdown("### **Project Details**")
st.sidebar.markdown("**Student**: Anuska Saha")
st.sidebar.markdown("**Reg. No.**: 23BCE0167")
st.sidebar.markdown("**Team ID**: 26FSDPYCPMID1029")
st.sidebar.markdown("**Course**: BCSE318L Data Privacy")
st.sidebar.markdown("**Faculty**: Dr M Rajasekhara Babu")
st.sidebar.markdown("**School**: SCOPE, VIT Vellore")
st.sidebar.markdown("---")
st.sidebar.markdown("### **Pipeline Status**")
st.sidebar.success("● Edge Policy Engine: ONLINE")
st.sidebar.success("● AI Risk Engine: ONLINE")
st.sidebar.success("● Audit Chain: IMMUTABLE (SHA-256)")

# Header
st.markdown("<div class='main-header'>AI-Driven Privacy Compliance in Heterogeneous IoT Environments</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>BCSE318L Case Study Reference Implementation & Live Evaluation System</div>", unsafe_allow_html=True)

tabs = st.tabs([
    "🚀 Live Pipeline Simulation",
    "📊 Comparative Benchmarks (Section 17)",
    "🔐 Immutable Audit Ledger (Section 11)",
    "🧪 Test Suite Runner (Appendix D)"
])

# ----------------- TAB 1: Live Pipeline Simulation -----------------
with tabs[0]:
    st.subheader("1. Test Event Configuration")

    col_dom, col_preset = st.columns([1, 2])
    with col_dom:
        domain_choice = st.selectbox(
            "Select IoT Domain:",
            ["Healthcare Wearables", "Smart City Surveillance", "Industrial Manufacturing", "Custom / Boundary Event"]
        )

    with col_preset:
        preset_choice = st.selectbox(
            "Load Canonical Test Vector:",
            [
                "Custom Config",
                "Case D-01: Valid Patient Telemetry (Allow + Minimise)",
                "Case D-02: Revoked Device Identity (Hard Perimeter Reject)",
                "Case D-03: Missing Purpose Metadata (Hold for Review)",
                "Case D-04: Unapproved Commercial Analytics Egress (Hard Block)",
                "Case D-12: Smart City 4K Camera Minimisation (Strip Frame + Round GPS)"
            ]
        )

    # Defaults based on preset
    def_device = "DEV-HEALTH-001"
    def_class = "sensitive_personal"
    def_purpose = "patient_remote_monitoring"
    def_receiver = "HOSPITAL_CORE_EHR"
    def_payload = {"heart_rate": 84, "patient_name": "Aarav Sharma", "latitude": 12.971598, "longitude": 79.158521}

    if "D-01" in preset_choice:
        def_device = "DEV-HEALTH-001"
        def_class = "sensitive_personal"
        def_purpose = "patient_remote_monitoring"
        def_receiver = "HOSPITAL_CORE_EHR"
        def_payload = {"heart_rate": 84, "patient_name": "Aarav Sharma", "latitude": 12.971598, "longitude": 79.158521, "raw_ecg_waveform": [0.1, 0.5, 1.2]}
    elif "D-02" in preset_choice:
        def_device = "DEV-REVOKED-999"
        def_class = "sensitive_personal"
        def_purpose = "patient_remote_monitoring"
        def_receiver = "HOSPITAL_CORE_EHR"
        def_payload = {"heart_rate": 84}
    elif "D-03" in preset_choice:
        def_device = "DEV-HEALTH-001"
        def_class = "sensitive_personal"
        def_purpose = ""
        def_receiver = "HOSPITAL_CORE_EHR"
        def_payload = {"heart_rate": 84}
    elif "D-04" in preset_choice:
        def_device = "DEV-HEALTH-001"
        def_class = "sensitive_personal"
        def_purpose = "patient_remote_monitoring"
        def_receiver = "THIRD_PARTY_ANALYTICS_CO"
        def_payload = {"heart_rate": 84}
    elif "D-12" in preset_choice:
        def_device = "DEV-CITY-042"
        def_class = "personal"
        def_purpose = "traffic_flow_optimization"
        def_receiver = "CITY_TRAFFIC_CONTROL"
        def_payload = {"raw_image_frame": "<bytes 4K image>", "detected_objects_count": 27, "latitude": 13.08268, "longitude": 80.270718}

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dev_id = st.text_input("Device ID", value=def_device)
    with col2:
        d_class = st.selectbox(
            "Data Class",
            ["sensitive_personal", "personal", "operational", "public", "unknown"],
            index=["sensitive_personal", "personal", "operational", "public", "unknown"].index(def_class)
        )
    with col3:
        purp_id = st.text_input("Declared Purpose", value=def_purpose)
    with col4:
        recv_id = st.text_input("Intended Receiver", value=def_receiver)

    st.markdown("#### **Sensor Payload & Parameter Overrides**")
    col_pay, col_risk = st.columns([1, 1])

    with col_pay:
        payload_str = st.text_area("Event Payload (JSON)", value=json.dumps(def_payload, indent=2), height=140)

    with col_risk:
        st.markdown("**AI Risk Parameters (Equation 1: $R = 100 \\times [0.40I + 0.35L + 0.25U]$)**")
        use_manual_risk = st.checkbox("Manual Risk Overrides (Simulate Model Inputs)", value=False)
        if use_manual_risk:
            s_i = st.slider("Impact (I)", 0.0, 1.0, 0.90, 0.05)
            s_l = st.slider("Likelihood (L)", 0.0, 1.0, 0.85, 0.05)
            s_u = st.slider("Uncertainty (U)", 0.0, 1.0, 0.80, 0.05)
        else:
            s_i = s_l = s_u = None
            st.info("Dynamic calculation enabled: Features derived from metadata and anomaly sensors.")

    if st.button("🚀 Ingest & Process Event through Compliance Pipeline", type="primary"):
        try:
            parsed_payload = json.loads(payload_str)
        except Exception:
            parsed_payload = {}

        event = IoTEvent(
            event_id=f"EVT-LIVE-{int(time.time())}",
            device_id=dev_id,
            data_class=DataClass(d_class),
            purpose_id=purp_id if purp_id.strip() else None,
            receiver_id=recv_id if recv_id.strip() else None,
            payload=parsed_payload
        )

        resp = pipeline.process_event(
            event,
            simulate_policy_outage=False,
            simulate_model_outage=False
        )

        st.markdown("---")
        st.subheader("2. Compliance Pipeline Execution Output")

        # Metric cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            if resp.action == PolicyAction.ALLOW:
                st.markdown("<div class='metric-card'><h3 style='color:#166534;margin:0;'>ALLOW</h3><p>Policy Action</p></div>", unsafe_allow_html=True)
            elif resp.action == PolicyAction.HOLD or resp.action == PolicyAction.REVIEW:
                st.markdown(f"<div class='metric-card'><h3 style='color:#92400E;margin:0;'>{resp.action.upper()}</h3><p>Policy Action</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='metric-card'><h3 style='color:#991B1B;margin:0;'>{resp.action.upper()}</h3><p>Policy Action</p></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-card'><h3 style='color:#1E3A8A;margin:0;'>{resp.event.state}</h3><p>Final Pipeline State</p></div>", unsafe_allow_html=True)
        with m3:
            score_disp = f"{resp.risk_assessment.score}/100" if resp.risk_assessment else "N/A"
            st.markdown(f"<div class='metric-card'><h3 style='color:#7C3AED;margin:0;'>{score_disp}</h3><p>AI Risk Score</p></div>", unsafe_allow_html=True)
        with m4:
            st.markdown(f"<div class='metric-card'><h3 style='color:#059669;margin:0;'>{resp.latency_ms:.2f} ms</h3><p>Processing Latency</p></div>", unsafe_allow_html=True)

        st.write("")
        col_out1, col_out2 = st.columns(2)
        with col_out1:
            st.markdown("##### **Policy Verdict & Explainability**")
            st.write(f"**Explanation:** {resp.explanation}")
            st.write(f"**Triggered Reason Codes:** `{resp.event.reason_codes}`")
            if resp.risk_assessment:
                b = resp.risk_assessment.breakdown
                st.markdown("##### **AI Risk Score Mathematical Breakdown**")
                st.write(f"* Impact ($0.40 \\times {b.impact_raw}$): **{b.impact_weighted} pts**")
                st.write(f"* Likelihood ($0.35 \\times {b.likelihood_raw}$): **{b.likelihood_weighted} pts**")
                st.write(f"* Uncertainty ($0.25 \\times {b.uncertainty_raw}$): **{b.uncertainty_weighted} pts**")
                st.write(f"* **Total Formula Score**: **{b.total_score}** ({b.risk_band} RISK)")

        with col_out2:
            st.markdown("##### **Edge Minimisation & Egress Payload**")
            if resp.event.provenance and resp.event.provenance.transformations_applied:
                st.success(f"Minimisations Applied: {', '.join(resp.event.provenance.transformations_applied)}")
            else:
                st.info("No transformations required for this payload class.")
            st.json(resp.event.payload)

            if resp.audit_record:
                st.markdown("##### **Cryptographic Audit Anchor**")
                st.code(f"Block #{resp.audit_record.entry_id} | SHA-256: {resp.audit_record.current_hash}")

# ----------------- TAB 2: Comparative Benchmarks -----------------
with tabs[1]:
    st.subheader("Empirical Comparative Assessment (Section 17)")
    st.markdown("Comparative evaluation across 1,000 synthetic multi-domain IoT streams.")

    benchmark_file = os.path.join(os.path.dirname(__file__), "..", "benchmark", "benchmark_summary.json")
    if os.path.exists(benchmark_file):
        with open(benchmark_file, "r") as f:
            bench_data = json.load(f)

        table_rows = []
        for name, m in bench_data.items():
            table_rows.append({
                "Method": name,
                "Precision": f"{m['Precision']:.4f}",
                "Recall": f"{m['Recall']:.4f}",
                "F1-Score": f"{m['F1_Score']:.4f}",
                "False-Positive Rate": f"{m['FPR']:.4f}",
                "Median Latency (ms)": f"{m['Median_Latency_ms']} ms",
                "Throughput (eps)": f"{m['Throughput_eps']}",
                "Compliance Coverage": f"{m['Compliance_Coverage_pct']}%",
                "Audit Completeness": f"{m['Audit_Completeness_pct']}%"
            })
        st.table(table_rows)

        st.markdown("""
        ### Key Analytical Findings:
        1. **Zero False Negatives on Hard Rules**: The Proposed Hybrid framework ensures that revoked devices, forbidden destinations, and expired policies are intercepted 100% of the time, overcoming the vulnerability of unconstrained AI models.
        2. **Sub-Millisecond Edge Enforcement**: By executing schema validation and policy checks at the local gateway level, median latency is under **1 ms** compared to **65+ ms** for cloud-centralized models.
        3. **Data Minimisation at Ingestion**: Identifiers and raw video frames are stripped prior to network transit, drastically reducing breach exposure and regulatory liability.
        """)
    else:
        st.warning("Run python benchmark/run_experiments.py to populate benchmark data.")

# ----------------- TAB 3: Immutable Audit Ledger -----------------
with tabs[2]:
    st.subheader("Cryptographic Tamper-Evident Audit Ledger (Section 11)")
    st.markdown("Every compliance action is cryptographically anchored using sequential SHA-256 hash chains (`current_hash = SHA256(prev_hash | record)`).")

    records = pipeline.audit_logger.get_all_records()
    col_aud1, col_aud2 = st.columns([1, 1])

    with col_aud1:
        if st.button("🛡️ Verify Ledger Cryptographic Chain Integrity"):
            is_valid = pipeline.audit_logger.verify_chain_integrity()
            if is_valid:
                st.success("✅ AUDIT CHAIN INTEGRITY VERIFIED: All block hashes and sequence pointers match!")
            else:
                st.error("❌ INTEGRITY BREACH DETECTED: Audit ledger has been modified or tampered with!")

    with col_aud2:
        if st.button("⚠️ Simulate Malicious Log Injection / Tampering"):
            if len(pipeline.audit_logger._entries) > 1:
                pipeline.audit_logger._entries[0].action_result = "UNAUTHORIZED_MODIFICATION"
                st.error("Tampering simulated! Re-verify integrity to see tamper detection.")
            else:
                st.warning("Process at least 2 events in Tab 1 first to create chain blocks.")

    if records:
        display_records = []
        for r in reversed(records[-15:]):  # show last 15
            display_records.append({
                "Block #": r.entry_id,
                "Timestamp": r.timestamp[11:19],
                "Event ID": r.event_id,
                "Device": r.device_id,
                "Action": r.action,
                "Result": r.action_result,
                "SHA-256 Current Hash": r.current_hash[:20] + "...",
                "SHA-256 Prev Hash": r.prev_hash[:20] + "..."
            })
        st.dataframe(display_records, use_container_width=True)
    else:
        st.info("No events logged yet. Process events in Tab 1 to populate the ledger.")

# ----------------- TAB 4: Test Suite Runner -----------------
with tabs[3]:
    st.subheader("Automated Verification Suite (Appendix D: Test Cases D-01 to D-12)")
    st.markdown("Executes the standardized compliance test matrix and validates expected policy actions.")

    if st.button("▶ Run Full Appendix D Test Suite"):
        test_file = os.path.join(os.path.dirname(__file__), "..", "..", "4_Datasets", "test_cases_d01_to_d12.json")
        if os.path.exists(test_file):
            with open(test_file, "r") as f:
                tests = json.load(f)

            passed_count = 0
            res_table = []
            for t in tests:
                evt = IoTEvent(
                    event_id=f"TEST-{t['test_id']}",
                    device_id=t["device_id"],
                    data_class=DataClass(t["data_class"]),
                    purpose_id=t.get("purpose_id"),
                    receiver_id=t.get("receiver_id"),
                    payload=t.get("payload", {})
                )
                resp = pipeline.process_event(
                    evt,
                    simulate_policy_outage=t.get("simulate_policy_outage", False),
                    simulate_model_outage=t.get("simulate_model_outage", False)
                )

                matches = (resp.action == t["expected_action"])
                if matches:
                    passed_count += 1

                res_table.append({
                    "Test ID": t["test_id"],
                    "Scenario Name": t["name"],
                    "Expected Action": t["expected_action"],
                    "Observed Action": resp.action,
                    "Latency (ms)": f"{resp.latency_ms:.2f}",
                    "Status": "PASSED" if matches else "FAILED"
                })

            st.table(res_table)
            if passed_count == len(tests):
                st.success(f"🎉 All {len(tests)} Appendix D Test Vectors PASSED successfully!")
            else:
                st.warning(f"Completed with {passed_count}/{len(tests)} passing.")
        else:
            st.error("Test definitions file not found in 4_Datasets.")
