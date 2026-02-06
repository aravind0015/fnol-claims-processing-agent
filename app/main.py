from __future__ import annotations

import json
import os
from typing import Any, Dict

from application.use_cases.process_claim import ProcessClaimUseCase
from infrastructure.llm.gemini_adapter import GeminiLLM
from infrastructure.parsing.pdf_parser_adapter import PdfParserAdapter

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
""".strip()


def build_use_case() -> ProcessClaimUseCase:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Export it first: export GEMINI_API_KEY=..."
        )

    llm = GeminiLLM(api_key=api_key)
    parser = PdfParserAdapter()
    return ProcessClaimUseCase(llm=llm, parser=parser, extraction_prompt=EXTRACTION_PROMPT)


def process_claim(pdf_path: str) -> Dict[str, Any]:
    """
    Backwards-compatible function used by Streamlit UI.
    """
    use_case = build_use_case()
    return use_case.execute(pdf_path)


def main() -> None:
    result = process_claim("samples/fnol.pdf")
    print("\n--- FINAL OUTPUT JSON ---\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
