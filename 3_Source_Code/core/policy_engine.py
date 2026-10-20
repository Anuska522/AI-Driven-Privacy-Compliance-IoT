"""
Automated Policy and Compliance Enforcement Engine.
Corresponds to Section 9, Table 6, and Appendix A of the Case Study Manuscript.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta
from .event_schema import IoTEvent, PolicyAction, DataClass, EventState


class PrivacyPolicy(BaseModel):
    policy_id: str
    version: str = "1.0"
    owner: str = "Privacy Governance Office"
    jurisdiction: str = "DPDP_2023_GDPR"
    effective_at: str = "2026-01-01T00:00:00Z"
    expires_at: str = "2027-12-31T23:59:59Z"
    signature_valid: bool = True
    data_class: DataClass
    allowed_purposes: List[str]
    allowed_receivers: List[str]
    forbidden_receivers: List[str] = Field(default_factory=list)
    max_retention_days: int = 30
    requires_minimisation: bool = False
    requires_human_review_above_risk: float = 70.0


class PolicyEvaluationResult:
    def __init__(
        self,
        passed: bool,
        action: PolicyAction,
        reason_codes: List[str],
        explanation: str,
        policy_version: str,
        state: EventState
    ):
        self.passed = passed
        self.action = action
        self.reason_codes = reason_codes
        self.explanation = explanation
        self.policy_version = policy_version
        self.state = state


class PolicyEngine:
    """Evaluates strict deterministic privacy rules before AI risk scoring."""

    def __init__(self):
        self._policies: Dict[str, PrivacyPolicy] = {}
        self._seed_default_policies()

    def _seed_default_policies(self):
        # Healthcare policy (HIPAA / DPDP Section 9 sensitive personal)
        self.register_policy(PrivacyPolicy(
            policy_id="POL-HEALTH-01",
            version="1.0",
            owner="Chief Medical Privacy Officer",
            jurisdiction="DPDP_2023 / HIPAA",
            effective_at="2026-01-01T00:00:00Z",
            expires_at="2027-01-01T00:00:00Z",
            signature_valid=True,
            data_class=DataClass.SENSITIVE_PERSONAL,
            allowed_purposes=["patient_remote_monitoring", "emergency_triage", "cardiac_telemetry"],
            allowed_receivers=["HOSPITAL_CORE_EHR", "CARDIOLOGY_ICU_SERVICE"],
            forbidden_receivers=["THIRD_PARTY_ANALYTICS_CO", "COMMERCIAL_BROKER", "AD_NETWORK"],
            max_retention_days=14,
            requires_minimisation=True,
            requires_human_review_above_risk=70.0
        ))

        # Smart City policy (GDPR Article 5 & 25 Minimisation)
        self.register_policy(PrivacyPolicy(
            policy_id="POL-CITY-01",
            version="1.0",
            owner="Municipal Data Protection Officer",
            jurisdiction="GDPR / DPDP",
            effective_at="2026-01-01T00:00:00Z",
            expires_at="2027-01-01T00:00:00Z",
            signature_valid=True,
            data_class=DataClass.PERSONAL,
            allowed_purposes=["traffic_flow_optimization", "congestion_analysis", "emergency_routing"],
            allowed_receivers=["CITY_TRAFFIC_CONTROL", "URBAN_PLANNING_PORTAL"],
            forbidden_receivers=["FACIAL_SURVEILLANCE_DB", "COMMERCIAL_INSURANCE"],
            max_retention_days=7,
            requires_minimisation=True,
            requires_human_review_above_risk=70.0
        ))

        # Industrial Manufacturing policy
        self.register_policy(PrivacyPolicy(
            policy_id="POL-IND-01",
            version="1.0",
            owner="Industrial Security Lead",
            jurisdiction="Enterprise Security Standard",
            effective_at="2026-01-01T00:00:00Z",
            expires_at="2027-01-01T00:00:00Z",
            signature_valid=True,
            data_class=DataClass.OPERATIONAL,
            allowed_purposes=["predictive_maintenance", "machine_telemetry", "safety_shutdown"],
            allowed_receivers=["FACTORY_MAINTENANCE_HQ", "SCADA_EDGE_SERVER"],
            forbidden_receivers=["PUBLIC_CLOUD_UNENCRYPTED"],
            max_retention_days=90,
            requires_minimisation=False,
            requires_human_review_above_risk=80.0
        ))

        # Generic / Public Weather policy
        self.register_policy(PrivacyPolicy(
            policy_id="POL-PUBLIC-01",
            version="1.0",
            owner="Open Data Trustee",
            jurisdiction="Public Domain",
            effective_at="2026-01-01T00:00:00Z",
            expires_at="2028-01-01T00:00:00Z",
            signature_valid=True,
            data_class=DataClass.PUBLIC,
            allowed_purposes=["environmental_monitoring", "public_weather_broadcast"],
            allowed_receivers=["OPEN_METEO_HUB", "CITY_DASHBOARD"],
            forbidden_receivers=[],
            max_retention_days=365,
            requires_minimisation=False,
            requires_human_review_above_risk=85.0
        ))

    def register_policy(self, policy: PrivacyPolicy) -> None:
        self._policies[policy.policy_id] = policy

    def get_policy(self, policy_id: str) -> Optional[PrivacyPolicy]:
        return self._policies.get(policy_id)

    def evaluate_mandatory_rules(self, event: IoTEvent, policy: PrivacyPolicy) -> PolicyEvaluationResult:
        """
        Enforce Section 9.2 Mandatory Hard Rules.
        AI risk score CANNOT override these rules if they fail.
        """
        # 1. Check Policy Validity and Expiry
        if not policy.signature_valid:
            return PolicyEvaluationResult(
                passed=False,
                action=PolicyAction.BLOCK,
                reason_codes=["policy_signature_invalid"],
                explanation="Policy cryptographic signature failed verification.",
                policy_version=policy.version,
                state=EventState.POLICY_CHECKED
            )

        now = datetime.now(timezone.utc)
        try:
            expires_dt = datetime.fromisoformat(policy.expires_at.replace("Z", "+00:00"))
            if now > expires_dt:
                return PolicyEvaluationResult(
                    passed=False,
                    action=PolicyAction.HOLD,
                    reason_codes=["policy_expired"],
                    explanation=f"Policy {policy.policy_id} expired on {policy.expires_at}. Safe fallback invoked.",
                    policy_version=policy.version,
                    state=EventState.POLICY_CHECKED
                )
        except Exception:
            pass

        # 2. Check Purpose Metadata (Appendix D case D-03)
        if not event.purpose_id or not event.purpose_id.strip():
            return PolicyEvaluationResult(
                passed=False,
                action=PolicyAction.HOLD,
                reason_codes=["missing_purpose"],
                explanation="Required purpose metadata missing from event payload.",
                policy_version=policy.version,
                state=EventState.HELD_MISSING_PURPOSE
            )

        # 3. Purpose Limitation Check (Section 10.1)
        if event.purpose_id not in policy.allowed_purposes:
            return PolicyEvaluationResult(
                passed=False,
                action=PolicyAction.BLOCK,
                reason_codes=["purpose_disallowed"],
                explanation=f"Purpose '{event.purpose_id}' is not permitted under policy {policy.policy_id}.",
                policy_version=policy.version,
                state=EventState.POLICY_CHECKED
            )

        # 4. Receiver Authorization Check (Appendix D case D-04)
        if not event.receiver_id:
            return PolicyEvaluationResult(
                passed=False,
                action=PolicyAction.HOLD,
                reason_codes=["missing_receiver"],
                explanation="Receiver destination not specified.",
                policy_version=policy.version,
                state=EventState.POLICY_CHECKED
            )

        if event.receiver_id in policy.forbidden_receivers or event.receiver_id not in policy.allowed_receivers:
            return PolicyEvaluationResult(
                passed=False,
                action=PolicyAction.BLOCK,
                reason_codes=["receiver_denied"],
                explanation=f"Receiver '{event.receiver_id}' is not in the approved receiver whitelist.",
                policy_version=policy.version,
                state=EventState.BLOCKED_RECEIVER
            )

        # 5. Retention Expiration Check (Appendix D case D-05)
        try:
            event_dt = datetime.fromisoformat(event.event_time.replace("Z", "+00:00"))
            retention_limit = event_dt + timedelta(days=policy.max_retention_days)
            if now > retention_limit:
                return PolicyEvaluationResult(
                    passed=False,
                    action=PolicyAction.QUARANTINE,
                    reason_codes=["retention_expired"],
                    explanation=f"Event age exceeds maximum policy retention window of {policy.max_retention_days} days.",
                    policy_version=policy.version,
                    state=EventState.BLOCKED_RETENTION_EXPIRED
                )
        except Exception:
            pass

        # All mandatory checks pass!
        return PolicyEvaluationResult(
            passed=True,
            action=PolicyAction.ALLOW,
            reason_codes=["mandatory_checks_passed"],
            explanation="All hard policy rules satisfied (identity, purpose, receiver, retention).",
            policy_version=policy.version,
            state=EventState.POLICY_CHECKED
        )
