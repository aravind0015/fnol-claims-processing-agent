from utils.schema import ClaimFields


FRAUD_KEYWORDS = ["fraud", "staged", "inconsistent", "suspicious"]


def determine_route(claim: ClaimFields, missing_fields: list[str]) -> str:
    data = claim.model_dump()

    # Rule 1: missing mandatory fields → manual review
    if missing_fields:
        return "manual_review"

    description = (data.get("description") or "").lower()
    claim_type = (data.get("claim_type") or "").lower()
    damage = data.get("estimated_damage")

    # Rule 2: fraud keywords → investigation
    for word in FRAUD_KEYWORDS:
        if word in description:
            return "investigation"

    # Rule 3: injury → specialist
    if "injury" in claim_type:
        return "specialist"

    # Rule 4: damage < 25k → fast-track
    if damage is not None and damage < 25000:
        return "fast_track"

    # Default
    return "standard"
