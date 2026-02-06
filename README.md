# Autonomous Insurance Claims Processing Agent

This project implements a lightweight AI agent that processes FNOL (First Notice of Loss) insurance documents.

It extracts key fields, detects missing data, routes the claim to the correct workflow, and provides reasoning for the decision.

## Features

- PDF FNOL document ingestion
- Structured field extraction using Gemini
- Missing field detection
- Rule-based routing
- AI-generated reasoning
- Streamlit UI for demo
- JSON output

## Architecture

The system is designed as a lightweight modular AI agent pipeline.

```
      ┌────────────────────┐
      │   Streamlit UI     │
      │ Upload FNOL PDF    │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │  PDF Parser        │
      │ (pdfplumber)       │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Text Cleaner       │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Extraction Agent   │
      │ Gemini API         │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Schema Validation  │
      │ Pydantic           │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Missing Field Check│
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Routing Engine     │
      │ Rule-based logic   │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Reasoning Agent    │
      │ Gemini API         │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Final JSON Output  │
      └────────────────────┘
```

### Flow Summary

1. User uploads FNOL PDF via Streamlit UI
2. PDF is parsed into raw text
3. Text is cleaned to be LLM-friendly
4. Gemini extracts structured fields (JSON)
5. Fields validated via Pydantic schema
6. Missing mandatory fields detected
7. Rule engine determines routing
8. Gemini generates explanation
9. Final JSON displayed + downloadable

### Design Principles

- Lightweight (assessment-focused)
- Deterministic routing logic
- LLM used only for extraction + reasoning
- Modular agent-based structure
- Easy to extend to production

## Tech Stack

- Python
- Gemini API
- Streamlit
- Pydantic
- pdfplumber

## How to Run

### Install

```bash
pip install -r requirements.txt
```

### Set API key

```bash
export GEMINI_API_KEY=your_key
```

### Run CLI

```bash
python main.py
```

### Run UI

```bash
streamlit run app.py
```

## Output Format

```json
{
  "extractedFields": {},
  "missingFields": [],
  "recommendedRoute": "",
  "reasoning": ""
}
```

## Notes

This is a lightweight technical assessment implementation and not a production system.
