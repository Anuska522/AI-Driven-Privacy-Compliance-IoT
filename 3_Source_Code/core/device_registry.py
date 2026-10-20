"""
IoT Device Onboarding and Status Registry.
Corresponds to Section 6.1 and Section 13.2 of the Case Study Manuscript.
"""

from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class DeviceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    RETIRED = "RETIRED"
    SUSPENDED = "SUSPENDED"


class DeviceRecord(BaseModel):
    device_id: str
    device_type: str  # e.g., "wearable", "traffic_camera", "factory_vibration", "smart_meter"
    model: str
    owner: str
    firmware_version: str
    supported_data_classes: list[str] = Field(default_factory=list)
    status: DeviceStatus = DeviceStatus.ACTIVE
    registered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_verified_at: Optional[str] = None
    revocation_reason: Optional[str] = None


class DeviceRegistry:
    """Manages verified device identities and revocation status."""

    def __init__(self):
        self._devices: Dict[str, DeviceRecord] = {}
        self._seed_default_devices()

    def _seed_default_devices(self):
        """Pre-populate canonical test devices reflecting the case study."""
        defaults = [
            DeviceRecord(
                device_id="DEV-HEALTH-001",
                device_type="wearable_biometric",
                model="CardioPulse-X2",
                owner="City Hospital Cardiology Dept",
                firmware_version="v2.4.1",
                supported_data_classes=["sensitive_personal", "personal"],
                status=DeviceStatus.ACTIVE
            ),
            DeviceRecord(
                device_id="DEV-CITY-042",
                device_type="traffic_camera",
                model="VisionFlow-4K",
                owner="Municipal Transport Authority",
                firmware_version="v1.8.0",
                supported_data_classes=["public", "personal"],
                status=DeviceStatus.ACTIVE
            ),
            DeviceRecord(
                device_id="DEV-IND-881",
                device_type="vibration_sensor",
                model="VibraSense-Pro",
                owner="Apex Precision Manufacturing",
                firmware_version="v3.1.2",
                supported_data_classes=["operational"],
                status=DeviceStatus.ACTIVE
            ),
            DeviceRecord(
                device_id="DEV-ENERGY-303",
                device_type="smart_meter",
                model="GridWatts-500",
                owner="State Power Distribution",
                firmware_version="v2.0.4",
                supported_data_classes=["operational", "personal"],
                status=DeviceStatus.ACTIVE
            ),
            DeviceRecord(
                device_id="DEV-LOG-512",
                device_type="gps_tracker",
                model="FleetTrack-G8",
                owner="TransGlobal Logistics",
                firmware_version="v1.2.0",
                supported_data_classes=["personal", "operational"],
                status=DeviceStatus.ACTIVE
            ),
            DeviceRecord(
                device_id="DEV-REVOKED-999",
                device_type="wearable_biometric",
                model="OldPulse-V1",
                owner="Compromised Clinic Node",
                firmware_version="v0.9.8-unsupported",
                supported_data_classes=["sensitive_personal"],
                status=DeviceStatus.REVOKED,
                revocation_reason="Compromised private key detected in audit trace"
            ),
        ]
        for dev in defaults:
            self._devices[dev.device_id] = dev

    def register_device(self, record: DeviceRecord) -> None:
        self._devices[record.device_id] = record

    def revoke_device(self, device_id: str, reason: str = "Administrative revocation") -> bool:
        if device_id in self._devices:
            self._devices[device_id].status = DeviceStatus.REVOKED
            self._devices[device_id].revocation_reason = reason
            return True
        return False

    def get_device(self, device_id: str) -> Optional[DeviceRecord]:
        return self._devices.get(device_id)

    def is_active(self, device_id: str) -> bool:
        dev = self.get_device(device_id)
        return dev is not None and dev.status == DeviceStatus.ACTIVE

    def is_revoked(self, device_id: str) -> bool:
        dev = self.get_device(device_id)
        return dev is not None and dev.status == DeviceStatus.REVOKED
