from __future__ import annotations

import os
import json
from dataclasses import asdict
from typing import Any, Dict, Optional

from dotenv import load_dotenv

load_dotenv()

assert os.getenv("GEMINI_API_KEY") is not None, "GEMINI_API_KEY not loaded"

from ports.document_parser_port import DocumentParserPort
from ports.llm_port import LLMPort
from domain.models import ClaimFields
from domain.routing_rules import determine_route, find_missing_fields


class ProcessClaimUseCase:
    """
    Orchestrates the full pipeline:
    PDF -> text -> LLM extraction -> validation -> routing -> LLM reasoning -> final JSON dict.
    """

    def __init__(
        self,
        llm: LLMPort,
        parser: DocumentParserPort,
        extraction_prompt: str,
        reasoning_model: Optional[LLMPort] = None,
    ):
        self._llm = llm
        self._parser = parser
        self._extraction_prompt = extraction_prompt
        self._reasoning_llm = reasoning_model or llm

    def execute(self, pdf_path: str) -> Dict[str, Any]:
        text = self._parser.parse(pdf_path)

        claim = self._extract_fields(text)
        missing = find_missing_fields(claim)
        route = determine_route(claim, missing)
        reasoning = self._generate_reasoning(claim, route, missing)

        return {
            "extractedFields": claim.model_dump(),
            "missingFields": missing,
            "recommendedRoute": route,
            "reasoning": reasoning,
        }

    def _extract_fields(self, text: str) -> ClaimFields:
        hint = """
Key snippets (may appear in the document):
- POLICY NUMBER
- DATE OF LOSS
- LOCATION OF LOSS
- DESCRIPTION OF ACCIDENT
- NAME OF INSURED
- CONTACT
"""
        prompt = self._extraction_prompt + "\n" + hint + "\n" + text

        raw_output = self._llm.generate(prompt).strip()

        # remove markdown if present
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        data = json.loads(raw_output) if raw_output else {}
        data = self._normalize_llm_types(data)

        # Filter unknown keys (e.g., "expected" from demos) defensively
        allowed_keys = set(asdict(ClaimFields()).keys())
        filtered = {k: v for k, v in data.items() if k in allowed_keys}

        return ClaimFields(**filtered)

    def _generate_reasoning(
        self, claim: ClaimFields, route: str, missing_fields: list[str]
    ) -> str:
        data = claim.model_dump()

        prompt = f"""
You are an insurance claims assistant.

Explain in 1–2 sentences why this claim was routed.

Route: {route}

Missing fields: {missing_fields}

Extracted data:
{data}

Return only a short explanation sentence.
"""
        text = self._reasoning_llm.generate(prompt).strip()

        # Some models may wrap the response in quotes; normalize to a clean sentence.
        if (text.startswith('"') and text.endswith('"')) or (
            text.startswith("'") and text.endswith("'")
        ):
            text = text[1:-1].strip()

        return text

    @staticmethod
    def _normalize_llm_types(data: Any) -> Dict[str, Any]:
        if not isinstance(data, dict):
            return {}

        if "attachments" in data and isinstance(data["attachments"], list):
            data["attachments"] = ", ".join(str(x) for x in data["attachments"])

        if "third_parties" in data and isinstance(data["third_parties"], list):
            data["third_parties"] = ", ".join(str(x) for x in data["third_parties"])

        if "claimant_contact" in data and isinstance(data["claimant_contact"], dict):
            data["claimant_contact"] = json.dumps(data["claimant_contact"])

        return data
