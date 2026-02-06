from domain.models import ClaimFields
from domain.routing_rules import determine_route, find_missing_fields


def run_test(name, claim_data):
    expected = claim_data.pop("expected", None)

    claim = ClaimFields(**claim_data)
    missing = find_missing_fields(claim)
    route = determine_route(claim, missing)

    print("\n==============================")
    print(name)
    print("Expected route:", expected)
    print("Actual route:  ", route)


# 1️⃣ Missing fields → manual_review
run_test(
    "Missing fields test",
    {
        "claim_type": "auto",
        "expected": "manual_review",
    },
)

# 2️⃣ Fast-track (<25k)
run_test(
    "Fast-track test",
    {
        "policy_number": "P1",
        "incident_date": "2024-01-01",
        "location": "NY",
        "description": "Minor accident",
        "claim_type": "auto",
        "estimated_damage": 10000,
        "expected": "fast_track",
    },
)

# 3️⃣ Investigation (fraud word)
run_test(
    "Fraud keyword test",
    {
        "policy_number": "P2",
        "incident_date": "2024-01-01",
        "location": "NY",
        "description": "This looks like a staged accident",
        "claim_type": "auto",
        "estimated_damage": 50000,
        "expected": "investigation",
    },
)

# 4️⃣ Specialist (injury)
run_test(
    "Injury claim test",
    {
        "policy_number": "P3",
        "incident_date": "2024-01-01",
        "location": "NY",
        "description": "Person injured in crash",
        "claim_type": "injury",
        "estimated_damage": 50000,
        "expected": "specialist",
    },
)

# 5️⃣ Standard route
run_test(
    "Standard route test",
    {
        "policy_number": "P4",
        "incident_date": "2024-01-01",
        "location": "NY",
        "description": "Vehicle damage",
        "claim_type": "auto",
        "estimated_damage": 40000,
        "expected": "standard",
    },
)
