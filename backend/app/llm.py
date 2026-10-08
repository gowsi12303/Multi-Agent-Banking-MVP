import json
import math
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def detect_intent(user_message: str) -> dict:
    """
    Use Gemini to detect the banking intent
    from a natural-language user request.
    """

    prompt = f"""
You are an intent classification system for a simulated banking application.

Classify the user's message into exactly ONE of these intents:

- customer_info
- balance
- transactions
- risk_analysis
- loan_eligibility
- emi
- unknown

Rules:
- balance = account balance questions
- transactions = recent transaction/history questions
- risk_analysis = suspicious/fraud/risk transaction questions
- loan_eligibility = loan eligibility/qualification questions
- emi = EMI/monthly payment calculation questions
- customer_info = customer/profile/account-holder information
- unknown = anything unrelated or unclear

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.

JSON format:
{{
    "intent": "one_of_the_allowed_intents",
    "confidence": 0.0
}}

User message:
{user_message}
"""

    fallback = {"intent": "unknown", "confidence": 0.0}

    allowed_intents = {
        "customer_info",
        "balance",
        "transactions",
        "risk_analysis",
        "loan_eligibility",
        "emi",
        "unknown",
    }

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt,
        )

        text = getattr(response, "text", None)

        if not isinstance(text, str) or not text.strip():
            return dict(fallback)

        text = text.strip()

        # Strip surrounding markdown code fences (```json ... ```)
        if text.startswith("```"):
            text = text[3:]
            if text.lower().startswith("json"):
                text = text[4:]
            text = text.strip()
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        result = json.loads(text)

        if not isinstance(result, dict):
            return dict(fallback)

        intent = result.get("intent", "unknown")

        if not isinstance(intent, str) or intent not in allowed_intents:
            intent = "unknown"

        try:
            confidence = float(result.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0

        if not math.isfinite(confidence):
            confidence = 0.0

        confidence = max(0.0, min(confidence, 1.0))

        return {
            "intent": intent,
            "confidence": confidence,
        }

    except Exception:
        return dict(fallback)
