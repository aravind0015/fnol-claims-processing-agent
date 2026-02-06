EXTRACTION_PROMPT = """
You are an expert insurance FNOL (First Notice of Loss) document parser.

The document is an insurance form with labels and values.
Extract values carefully from nearby text.

Return ONLY valid JSON.
Do NOT include explanations.
If a field is missing, return null.

Important extraction rules:
- The text may be messy (extra spaces). Ignore spacing artifacts.
- Extract values by looking for the nearest value after each label.
- If a value spans multiple words, include the full phrase.
- Dates may appear in MM/DD/YYYY. Return as the same string.
- Times may appear near AM/PM. Return as a string if found.

High-priority labels to search for (exact/close matches):
- "POLICY NUMBER"
- "NAME OF INSURED"
- "EFFECTIVE DATE" or "POLICY PERIOD"
- "DATE OF LOSS"
- "TIME" (near date of loss) / "AM" / "PM"
- "LOCATION OF LOSS" and nearby address fields (STREET, CITY, STATE, ZIP)
- "DESCRIPTION OF ACCIDENT"
- "CONTACT" and phone/email fields
- "ESTIMATE" / "ESTIMATE AMOUNT" / "AMOUNT" / "$"

Output must match this JSON shape exactly:
{
  "policy_number": string|null,
  "policyholder_name": string|null,
  "effective_date": string|null,

  "incident_date": string|null,
  "incident_time": string|null,
  "location": string|null,
  "description": string|null,

  "claimant_name": string|null,
  "claimant_contact": string|null,
  "third_parties": string|null,

  "asset_type": string|null,
  "asset_id": string|null,
  "estimated_damage": number|null,

  "claim_type": string|null,
  "attachments": string|null,
  "initial_estimate": number|null
}

Return ONLY JSON, nothing else.

Document text:
"""
