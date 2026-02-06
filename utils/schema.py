from typing import Optional

from pydantic import BaseModel, Field


class ClaimFields(BaseModel):
    # Policy
    policy_number: Optional[str] = Field(default=None)
    policyholder_name: Optional[str] = Field(default=None)
    effective_date: Optional[str] = Field(default=None)

    # Incident
    incident_date: Optional[str] = Field(default=None)
    incident_time: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    # Parties
    claimant_name: Optional[str] = Field(default=None)
    claimant_contact: Optional[str] = Field(default=None)
    third_parties: Optional[str] = Field(default=None)

    # Asset
    asset_type: Optional[str] = Field(default=None)
    asset_id: Optional[str] = Field(default=None)
    estimated_damage: Optional[float] = Field(default=None)

    # Claim metadata
    claim_type: Optional[str] = Field(default=None)
    attachments: Optional[str] = Field(default=None)
    initial_estimate: Optional[float] = Field(default=None)
