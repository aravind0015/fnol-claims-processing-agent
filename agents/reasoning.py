from google import genai

from utils.schema import ClaimFields
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)



def generate_reasoning(claim: ClaimFields, route: str, missing_fields: list[str]) -> str:
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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0},
    )

    return response.text.strip()
