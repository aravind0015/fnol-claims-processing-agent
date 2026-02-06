from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class ClaimFields:
    """
    Domain model for extracted FNOL claim fields.

    Kept dependency-free (no Pydantic) to ensure the domain layer stays pure.
    """

    policy_number: Optional[str] = None
    policyholder_name: Optional[str] = None
    effective_date: Optional[str] = None
    incident_date: Optional[str] = None
    incident_time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    claimant_name: Optional[str] = None
    claimant_contact: Optional[str] = None
    third_parties: Optional[str] = None
    asset_type: Optional[str] = None
    asset_id: Optional[str] = None
    estimated_damage: Optional[float] = None
    claim_type: Optional[str] = None
    attachments: Optional[str] = None
    initial_estimate: Optional[float] = None

    def model_dump(self) -> Dict[str, Any]:
        # Provide a familiar API for the rest of the codebase.
        return asdict(self)


@dataclass(frozen=True)
class RoutingDecision:
    recommended_route: str
    missing_fields: list[str]
    reasoning: str

    def model_dump(self) -> Dict[str, Any]:
        return asdict(self)
