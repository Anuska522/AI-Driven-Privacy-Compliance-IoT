"""
Edge Privacy Controls and Data Minimisation.
Corresponds to Section 10.1 and Appendix D case D-12 of the Case Study Manuscript.
"""

import hashlib
from typing import Dict, Any, Tuple
from .event_schema import IoTEvent, ProvenanceRecord


class EdgePrivacyControls:
    """Applies local edge transformations: pseudonymization, location rounding, and aggregation."""

    @staticmethod
    def pseudonymize_identifier(value: str) -> str:
        """Replace direct identifier with a keyed pseudo-hash."""
        salt = "bcse318l_edge_salt_2026"
        return "PSEUDO-" + hashlib.sha256(f"{salt}_{value}".encode()).hexdigest()[:12].upper()

    @staticmethod
    def reduce_location_precision(lat: float, lon: float, precision_decimals: int = 2) -> Tuple[float, float]:
        """
        Reduce GPS precision (Section 10.1).
        2 decimal places ~ 1.1 km resolution, preventing home/work route tracking.
        """
        return round(lat, precision_decimals), round(lon, precision_decimals)

    @classmethod
    def apply_minimisation(cls, event: IoTEvent) -> IoTEvent:
        """
        Apply context-specific data minimisation on the event payload.
        Ensures raw sensitive fields are stripped or generalised before egress.
        """
        payload = dict(event.payload)
        transformations = []

        # 1. Healthcare Biometric Minimisation
        if "patient_name" in payload:
            raw_name = payload.pop("patient_name")
            payload["patient_pseudo_id"] = cls.pseudonymize_identifier(raw_name)
            transformations.append("pseudonymized_patient_name")

        if "raw_ecg_waveform" in payload:
            # Strip raw high-frequency microvolt waveform, retain medical summary metric
            waveform = payload.pop("raw_ecg_waveform")
            if isinstance(waveform, list) and len(waveform) > 0:
                payload["avg_ecg_amplitude"] = round(sum(waveform) / len(waveform), 3)
            transformations.append("reduced_raw_ecg_to_summary")

        # 2. Smart City Traffic Camera Minimisation
        if "raw_image_frame" in payload:
            # Drop raw camera imagery, compute aggregate vehicle count
            payload.pop("raw_image_frame")
            payload["vehicle_count"] = payload.get("detected_objects_count", 1)
            transformations.append("discarded_raw_camera_frame_retained_count")

        if "latitude" in payload and "longitude" in payload:
            try:
                lat = float(payload["latitude"])
                lon = float(payload["longitude"])
                r_lat, r_lon = cls.reduce_location_precision(lat, lon, precision_decimals=2)
                payload["latitude"] = r_lat
                payload["longitude"] = r_lon
                transformations.append("reduced_gps_precision_2_decimals")
            except (ValueError, TypeError):
                pass

        # 3. Industrial Worker Badge Minimisation
        if "worker_id" in payload:
            worker = payload.pop("worker_id")
            payload["operator_shift_code"] = cls.pseudonymize_identifier(worker)
            transformations.append("suppressed_worker_badge_id")

        # Update event
        event.payload = payload
        if event.provenance is None:
            event.provenance = ProvenanceRecord(
                original_source=event.device_id,
                transformations_applied=transformations
            )
        else:
            event.provenance.transformations_applied.extend(transformations)

        return event
