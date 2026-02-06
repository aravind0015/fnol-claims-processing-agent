import json

from agents.extractor import extract_fields_from_text
from agents.reasoning import generate_reasoning
from agents.router import determine_route
from agents.validator import find_missing_fields
from utils.pdf_parser import clean_text, extract_text_from_pdf


def process_claim(pdf_path: str) -> dict:
    raw = extract_text_from_pdf(pdf_path)
    cleaned = clean_text(raw)

    claim = extract_fields_from_text(cleaned)
    missing = find_missing_fields(claim)
    route = determine_route(claim, missing)
    reasoning = generate_reasoning(claim, route, missing)

    result = {
        "extractedFields": claim.model_dump(),
        "missingFields": missing,
        "recommendedRoute": route,
        "reasoning": reasoning,
    }

    return result


def main():
    result = process_claim("samples/fnol.pdf")

    print("\n--- FINAL OUTPUT JSON ---\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
