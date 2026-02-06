import json

from google import genai

from utils.prompts import EXTRACTION_PROMPT
from utils.schema import ClaimFields

client = genai.Client(api_key="AIzaSyD89VsYBxvkc359HRUk-kkoaAWWlpSJtcg")


def extract_fields_from_text(text: str) -> ClaimFields:
    # Give the model a bit more local context to latch onto form labels by
    # emphasizing key snippets.
    hint = """
Key snippets (may appear in the document):
- POLICY NUMBER
- DATE OF LOSS
- LOCATION OF LOSS
- DESCRIPTION OF ACCIDENT
- NAME OF INSURED
- CONTACT
"""
    prompt = EXTRACTION_PROMPT + "\n" + hint + "\n" + text

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0,
            "response_mime_type": "application/json",
        },
    )

    raw_output = response.text.strip()
    print("\n--- RAW GEMINI OUTPUT ---\n")
    print(raw_output)

    # remove markdown if present
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        print("\n⚠️ JSON parse failed. Raw output:\n")
        print(raw_output)
        raise

    # Normalize a few common "close enough" types from the LLM to match our schema
    # (keeping schema strict while still being resilient to minor variations).
    if isinstance(data, dict):
        if "attachments" in data and isinstance(data["attachments"], list):
            data["attachments"] = ", ".join(str(x) for x in data["attachments"])

        if "third_parties" in data and isinstance(data["third_parties"], list):
            data["third_parties"] = ", ".join(str(x) for x in data["third_parties"])

        if "claimant_contact" in data and isinstance(data["claimant_contact"], dict):
            data["claimant_contact"] = json.dumps(data["claimant_contact"])

    claim = ClaimFields(**data)
    return claim
