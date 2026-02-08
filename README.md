# Autonomous Insurance Claims Processing Agent (FNOL)

Lightweight autonomous claims processing agent for FNOL (First Notice of Loss) PDFs.

It extracts key claim fields, detects missing mandatory data, routes the claim via deterministic rules, and generates a short reasoning explanation. Includes a Streamlit UI and deterministic routing demo tests.

## Features

- PDF FNOL ingestion (pdfplumber)
- Structured field extraction using Gemini (JSON)
- Missing mandatory field detection
- Deterministic rule-based routing
- AI-generated reasoning (Gemini)
- Final output in the required assessment JSON format
- Streamlit one-page UI + JSON download
- Deterministic routing tests (no LLM)

## Architecture (Lightweight Hexagonal / Ports & Adapters)

The system is structured using a minimal ports & adapters layout so the LLM can be swapped later (Gemini/OpenAI/local) without changing domain logic.

Ports:
- ports/llm_port.py
- ports/document_parser_port.py

Adapters:
- adapters/llm/gemini_adapter.py
- adapters/parser/pdf_parser_adapter.py
- adapters/ui/streamlit_ui.py

```
      ┌────────────────────┐
      │   Streamlit UI     │
      │  (adapters/)       │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Application UseCase│
      │ ProcessClaimUseCase│
      │ (application/)     │
      └─────────┬──────────┘
                │
                ├──────────────┐
                ▼              ▼
      ┌────────────────┐  ┌────────────────────┐
      │ Parser Port     │  │ LLM Port           │
      │ + PDF Adapter   │  │ + Gemini Adapter   │
      │ (ports/adapters)│  │ (ports/adapters)   │
      └─────────┬───────┘  └─────────┬──────────┘
                │                    │
                ▼                    ▼
      ┌──────────────────────────────────────────┐
      │ Domain (pure Python)                     │
      │ - ClaimFields model                      │
      │ - find_missing_fields()                  │
      │ - determine_route()                      │
      └──────────────────────────────────────────┘
```

### Folder structure

```
domain/
  models.py
  routing_rules.py

application/
  use_cases/
    process_claim.py

ports/
  llm_port.py
  document_parser_port.py

adapters/
  llm/
    gemini_adapter.py
  parser/
    pdf_parser_adapter.py
  ui/
    streamlit_ui.py

app/
  main.py

tests/
  test_routing.py

# Backwards-compatible entrypoints
main.py
app.py
tests_routing.py
```

## Output Format (assessment requirement)

```json
{
  "extractedFields": {},
  "missingFields": [],
  "recommendedRoute": "",
  "reasoning": ""
}
```

## Setup

### Install dependencies & activate venv

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Set Gemini API key

```bash
export GEMINI_API_KEY="YOUR_KEY"
```

## Run (CLI)

Backwards-compatible entrypoint:

```bash
source venv/bin/activate
python main.py
```

This prints the final JSON output.

## Run (UI)

Backwards-compatible Streamlit entrypoint:

```bash
source venv/bin/activate
streamlit run app.py
```

Upload an FNOL PDF, click **Process Claim**, then view results and download JSON.

## Run routing tests (deterministic demo)

These tests validate routing behavior for all routes without calling Gemini.

```bash
source venv/bin/activate
python -m tests.test_routing
```

## Notes

- Routing is deterministic (pure domain logic); LLM is used only for extraction + reasoning.
- This is an assessment-focused implementation (not production hardening like OCR, table extraction, PHI controls, etc.).
