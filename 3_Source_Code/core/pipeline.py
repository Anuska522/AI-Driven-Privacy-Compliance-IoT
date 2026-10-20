"""
End-to-End Privacy Compliance Pipeline.
Direct implementation of Appendix B: FUNCTION process_event(event).
"""

import time
from typing import Dict, Any, Optional, Tuple
from .event_schema import IoTEvent, EventState, PolicyAction, DataClass
from .device_registry import DeviceRegistry
from .policy_engine import PolicyEngine, PrivacyPolicy
from .risk_engine import RiskEngine, RiskAssessment
from .edge_controls import EdgePrivacyControls
from .audit_logger import AuditLogger, AuditRecord


class PipelineResponse:
    def __init__(
        self,
        event: IoTEvent,
        action: PolicyAction,
        action_result: str,
        explanation: str,
        risk_assessment: Optional[RiskAssessment],
        audit_record: Optional[AuditRecord],
        latency_ms: float
    ):
        self.event = event
        self.action = action
        self.action_result = action_result
        self.explanation = explanation
        self.risk_assessment = risk_assessment
        self.audit_record = audit_record
        self.latency_ms = latency_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event.event_id,
            "device_id": self.event.device_id,
            "action": str(self.action),
            "action_result": self.action_result,
            "explanation": self.explanation,
            "state": str(self.event.state),
            "risk_score": self.risk_assessment.score if self.risk_assessment else None,
            "risk_band": self.risk_assessment.risk_band if self.risk_assessment else None,
            "reasons": self.event.reason_codes,
            "latency_ms": round(self.latency_ms, 3),
            "audit_hash": self.audit_record.current_hash if self.audit_record else None,
            "payload_after_minimisation": self.event.payload
        }


class PrivacyCompliancePipeline:
    """Executes the 10-step reference compliance pipeline from Appendix B."""

    def __init__(
        self,
        device_registry: Optional[DeviceRegistry] = None,
        policy_engine: Optional[PolicyEngine] = None,
        audit_logger: Optional[AuditLogger] = None
    ):
        self.device_registry = device_registry or DeviceRegistry()
        self.policy_engine = policy_engine or PolicyEngine()
        self.audit_logger = audit_logger or AuditLogger()
        self.review_queue: list[Dict[str, Any]] = []

    def process_event(
        self,
        event: IoTEvent,
        policy_id: Optional[str] = None,
        simulate_policy_outage: bool = False,
        simulate_model_outage: bool = False
    ) -> PipelineResponse:
        t_start = time.perf_counter()

        # Step 1: Verify Schema
        if not event.event_id or not event.device_id:
            event.state = EventState.REJECTED_INVALID_SCHEMA
            event.action = PolicyAction.REJECT
            event.reason_codes.append("invalid_schema")
            expl = "Event rejected: missing required event_id or device_id."
            rec = self.audit_logger.record_decision(
                event_id=event.event_id or "UNKNOWN",
                device_id=event.device_id or "UNKNOWN",
                data_class=str(event.data_class),
                purpose_id=event.purpose_id,
                receiver_id=event.receiver_id,
                policy_version="N/A",
                model_version="N/A",
                risk_score=None,
                reason_codes=event.reason_codes,
                action=PolicyAction.REJECT,
                action_result="CONFIRMED_REJECTED"
            )
            lat = (time.perf_counter() - t_start) * 1000.0
            return PipelineResponse(event, PolicyAction.REJECT, "CONFIRMED_REJECTED", expl, None, rec, lat)

        # Step 2: Verify Device Identity & Revocation Status
        device_rec = self.device_registry.get_device(event.device_id)
        if device_rec is None:
            event.state = EventState.REJECTED_INVALID_DEVICE
            event.action = PolicyAction.REJECT
            event.reason_codes.append("unknown_device")
            expl = f"Device '{event.device_id}' is not onboarded in the trusted registry."
            rec = self.audit_logger.record_decision(
                event_id=event.event_id,
                device_id=event.device_id,
                data_class=str(event.data_class),
                purpose_id=event.purpose_id,
                receiver_id=event.receiver_id,
                policy_version=event.policy_version or "1.0",
                model_version="N/A",
                risk_score=None,
                reason_codes=event.reason_codes,
                action=PolicyAction.REJECT,
                action_result="CONFIRMED_REJECTED"
            )
            lat = (time.perf_counter() - t_start) * 1000.0
            return PipelineResponse(event, PolicyAction.REJECT, "CONFIRMED_REJECTED", expl, None, rec, lat)

        if device_rec.status != "ACTIVE":
            event.state = EventState.REJECTED_INVALID_DEVICE
            event.action = PolicyAction.REJECT
            reason = "revoked_device" if device_rec.status == "REVOKED" else "inactive_device"
            event.reason_codes.append(reason)
            expl = f"Device '{event.device_id}' status is {device_rec.status}. Rejection enforced."
            rec = self.audit_logger.record_decision(
                event_id=event.event_id,
                device_id=event.device_id,
                data_class=str(event.data_class),
                purpose_id=event.purpose_id,
                receiver_id=event.receiver_id,
                policy_version=event.policy_version or "1.0",
                model_version="N/A",
                risk_score=None,
                reason_codes=event.reason_codes,
                action=PolicyAction.REJECT,
                action_result="CONFIRMED_REJECTED"
            )
            lat = (time.perf_counter() - t_start) * 1000.0
            return PipelineResponse(event, PolicyAction.REJECT, "CONFIRMED_REJECTED", expl, None, rec, lat)

        # Step 3: Load Current Signed Policy / Safe Fallback
        resolved_pol_id = policy_id
        if not resolved_pol_id:
            # Map policy by device type / data class
            if event.data_class == DataClass.SENSITIVE_PERSONAL or "health" in device_rec.device_type:
                resolved_pol_id = "POL-HEALTH-01"
            elif event.data_class == DataClass.PERSONAL or "traffic" in device_rec.device_type or "camera" in device_rec.device_type:
                resolved_pol_id = "POL-CITY-01"
            elif event.data_class == DataClass.OPERATIONAL:
                resolved_pol_id = "POL-IND-01"
            else:
                resolved_pol_id = "POL-PUBLIC-01"

        policy = self.policy_engine.get_policy(resolved_pol_id)

        if simulate_policy_outage or policy is None:
            # Outage safe fallback (Section 5.4, Appendix D cases D-08, D-09)
            event.action = PolicyAction.HOLD
            event.reason_codes.append("policy_service_offline_fallback")
            expl = "Policy authority unavailable. Fail-safe holding applied."
            rec = self.audit_logger.record_decision(
                event_id=event.event_id,
                device_id=event.device_id,
                data_class=str(event.data_class),
                purpose_id=event.purpose_id,
                receiver_id=event.receiver_id,
                policy_version="FALLBACK",
                model_version="N/A",
                risk_score=None,
                reason_codes=event.reason_codes,
                action=PolicyAction.HOLD,
                action_result="CONFIRMED_HELD"
            )
            lat = (time.perf_counter() - t_start) * 1000.0
            return PipelineResponse(event, PolicyAction.HOLD, "CONFIRMED_HELD", expl, None, rec, lat)

        # Step 4: Classify Data Context
        if event.data_class == DataClass.UNKNOWN:
            event.reason_codes.append("unclassified_data_context")

        # Step 5: Verify Purpose, Receiver, and Retention (Mandatory Rules)
        eval_result = self.policy_engine.evaluate_mandatory_rules(event, policy)
        if not eval_result.passed:
            event.state = eval_result.state
            event.action = eval_result.action
            event.reason_codes.extend(eval_result.reason_codes)
            rec = self.audit_logger.record_decision(
                event_id=event.event_id,
                device_id=event.device_id,
                data_class=str(event.data_class),
                purpose_id=event.purpose_id,
                receiver_id=event.receiver_id,
                policy_version=policy.version,
                model_version="N/A",
                risk_score=None,
                reason_codes=event.reason_codes,
                action=eval_result.action,
                action_result=f"CONFIRMED_{eval_result.action.upper()}"
            )
            lat = (time.perf_counter() - t_start) * 1000.0
            return PipelineResponse(
                event,
                eval_result.action,
                f"CONFIRMED_{eval_result.action.upper()}",
                eval_result.explanation,
                None,
                rec,
                lat
            )

        # Step 6: Edge Minimisation & Safe Transformation (Appendix D case D-12)
        if policy.requires_minimisation:
            event = EdgePrivacyControls.apply_minimisation(event)
            event.reason_codes.append("edge_minimisation_applied")

        # Step 7: Compute AI-Powered Privacy Risk Score
        risk_assessment = None
        if not simulate_model_outage:
            risk_assessment = RiskEngine.evaluate(event)
            event.risk_score = risk_assessment.score
            event.reason_codes.extend(risk_assessment.reasons)
            event.state = EventState.RISK_REVIEWED
        else:
            event.reason_codes.append("ai_model_unavailable_fallback")

        # Step 8: Final Action Selection & Human Review Queue
        final_action = PolicyAction.ALLOW
        action_result = "CONFIRMED_ALLOWED"
        explanation = "Event verified and cleared for dispatch."

        if risk_assessment and risk_assessment.requires_human_review:
            final_action = PolicyAction.REVIEW
            action_result = "HELD_FOR_HUMAN_REVIEW"
            explanation = f"Flagged for human review: score {risk_assessment.score} exceeds threshold."
            event.state = EventState.REVIEW_REQUIRED
            self.review_queue.append({
                "event_id": event.event_id,
                "score": risk_assessment.score,
                "reasons": event.reason_codes,
                "time": event.event_time
            })
        else:
            event.state = EventState.ACTIONED

        event.action = final_action
        event.action_status = action_result

        # Step 9: Save Minimal Cryptographic Tamper-Evident Audit Record
        audit_record = self.audit_logger.record_decision(
            event_id=event.event_id,
            device_id=event.device_id,
            data_class=str(event.data_class),
            purpose_id=event.purpose_id,
            receiver_id=event.receiver_id,
            policy_version=policy.version,
            model_version=event.model_version or "v1",
            risk_score=risk_assessment.score if risk_assessment else None,
            reason_codes=event.reason_codes,
            action=final_action,
            action_result=action_result
        )

        event.state = EventState.LOGGED
        lat = (time.perf_counter() - t_start) * 1000.0

        # Step 10: Return Final State and Explanation
        return PipelineResponse(
            event=event,
            action=final_action,
            action_result=action_result,
            explanation=explanation,
            risk_assessment=risk_assessment,
            audit_record=audit_record,
            latency_ms=lat
        )
