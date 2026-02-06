from typing import List

from utils.schema import ClaimFields


MANDATORY_FIELDS = [
    "policy_number",
    "incident_date",
    "location",
    "description",
    "claim_type",
]


def find_missing_fields(claim: ClaimFields) -> List[str]:
    missing = []

    data = claim.model_dump()

    for field in MANDATORY_FIELDS:
        value = data.get(field)
        if value is None or value == "":
            missing.append(field)

    return missing
