"""
AI-Powered Privacy Risk Assessment Layer.
Corresponds to Section 8, Equations (1) & (2), and Table 11 of the Case Study Manuscript.
"""

from typing import Dict, Any, List
from pydantic import BaseModel
from .event_schema import IoTEvent, DataClass


class RiskBreakdown(BaseModel):
    impact_raw: float
    likelihood_raw: float
    uncertainty_raw: float
    impact_weighted: float
    likelihood_weighted: float
    uncertainty_weighted: float
    total_score: float
    risk_band: str  # "LOW", "MEDIUM", "HIGH"


class RiskAssessment(BaseModel):
    score: float
    risk_band: str
    reasons: List[str]
    breakdown: RiskBreakdown
    requires_human_review: bool


class RiskEngine:
    """
    Computes risk score according to Equation (1):
    R = 100 * (0.40 * I + 0.35 * L + 0.25 * U)
    """

    WEIGHT_IMPACT = 0.40
    WEIGHT_LIKELIHOOD = 0.35
    WEIGHT_UNCERTAINTY = 0.25

    HIGH_RISK_THRESHOLD = 70.0
    MEDIUM_RISK_THRESHOLD = 40.0

    @classmethod
    def normalize(cls, val: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Equation (2): Feature Min-Max Scaling."""
        if max_val == min_val:
            return 0.0
        clamped = max(min_val, min(max_val, val))
        return (clamped - min_val) / (max_val - min_val)

    @classmethod
    def compute_impact(cls, event: IoTEvent) -> float:
        """Derives Impact (I) based on data sensitivity and recipient risk."""
        base_impact = {
            DataClass.SENSITIVE_PERSONAL: 0.90,
            DataClass.PERSONAL: 0.60,
            DataClass.OPERATIONAL: 0.30,
            DataClass.PUBLIC: 0.10,
            DataClass.UNKNOWN: 0.70
        }.get(event.data_class, 0.50)

        # Elevation if sending to external third party
        if event.receiver_id and "THIRD_PARTY" in event.receiver_id.upper():
            base_impact = min(1.0, base_impact + 0.15)

        return cls.normalize(base_impact)

    @classmethod
    def compute_likelihood(cls, event: IoTEvent) -> float:
        """Derives Likelihood (L) based on anomalous behavior indicators."""
        likelihood = 0.20  # baseline normal expectation

        # Anomaly signal: high frequency or sudden batch burst
        if event.payload.get("burst_rate_hz", 0) > 50:
            likelihood += 0.35

        # Unknown receiver increases chance of unauthorized exfiltration
        if event.receiver_id and "UNKNOWN" in event.receiver_id.upper():
            likelihood += 0.40

        # Anomaly score flag
        if event.payload.get("anomaly_flag", False):
            likelihood += 0.30

        return cls.normalize(min(1.0, likelihood))

    @classmethod
    def compute_uncertainty(cls, event: IoTEvent) -> float:
        """Derives Uncertainty (U) based on missing metadata or unverified sources."""
        uncertainty = 0.10  # baseline verified state

        if not event.purpose_id:
            uncertainty += 0.50
        if not event.receiver_id:
            uncertainty += 0.30
        if event.data_class == DataClass.UNKNOWN:
            uncertainty += 0.40
        if not event.provenance:
            uncertainty += 0.15

        return cls.normalize(min(1.0, uncertainty))

    @classmethod
    def evaluate(
        cls,
        event: IoTEvent,
        override_i: float = None,
        override_l: float = None,
        override_u: float = None
    ) -> RiskAssessment:
        """Calculates R = 100 * (0.40*I + 0.35*L + 0.25*U)."""
        I = override_i if override_i is not None else cls.compute_impact(event)
        L = override_l if override_l is not None else cls.compute_likelihood(event)
        U = override_u if override_u is not None else cls.compute_uncertainty(event)

        i_w = round(cls.WEIGHT_IMPACT * I * 100, 2)
        l_w = round(cls.WEIGHT_LIKELIHOOD * L * 100, 2)
        u_w = round(cls.WEIGHT_UNCERTAINTY * U * 100, 2)

        raw_score = i_w + l_w + u_w
        total_score = round(raw_score, 2)

        reasons = []
        if total_score >= cls.HIGH_RISK_THRESHOLD:
            risk_band = "HIGH"
            reasons.append(f"High aggregate privacy risk score ({total_score}/100)")
        elif total_score >= cls.MEDIUM_RISK_THRESHOLD:
            risk_band = "MEDIUM"
            reasons.append(f"Moderate privacy risk score ({total_score}/100)")
        else:
            risk_band = "LOW"
            reasons.append(f"Low privacy risk score ({total_score}/100)")

        if U >= 0.50:
            reasons.append(f"Elevated uncertainty index (U={U:.2f}) due to incomplete metadata")
        if I >= 0.70:
            reasons.append(f"High sensitivity payload category ({event.data_class})")

        breakdown = RiskBreakdown(
            impact_raw=round(I, 3),
            likelihood_raw=round(L, 3),
            uncertainty_raw=round(U, 3),
            impact_weighted=i_w,
            likelihood_weighted=l_w,
            uncertainty_weighted=u_w,
            total_score=total_score,
            risk_band=risk_band
        )

        return RiskAssessment(
            score=total_score,
            risk_band=risk_band,
            reasons=reasons,
            breakdown=breakdown,
            requires_human_review=(total_score >= cls.HIGH_RISK_THRESHOLD)
        )
