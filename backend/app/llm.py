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
You are the intent classifier for a simulated banking assistant.

Your job is to understand the user's banking request and classify it
into exactly ONE intent.

Allowed intents:

1. customer_info
   Use ONLY when the user asks about:
   - customer identity
   - name
   - email
   - customer details
   - account holder information

   Examples:
   "Tell me my customer details"
   "What is my name?"
   "Show my profile information"
   "What email is registered?"

2. balance
   Use when the user asks about:
   - current account balance
   - available money
   - how much money is in the account

   Examples:
   "What is my balance?"
   "How much money do I have?"
   "How much is available in my account?"

3. transactions
   Use when the user asks about:
   - recent transactions
   - transaction history
   - previous transactions
   - account activity

   Examples:
   "Show my recent transactions"
   "What transactions did I make?"
   "Show my transaction history"

4. risk_analysis
   Use when the user asks about:
   - suspicious transactions
   - fraud
   - transaction risk
   - whether a transaction is safe
   - why a transaction was flagged

   Examples:
   "Is TXN1005 suspicious?"
   "Analyze TXN1005 for fraud"
   "Why was TXN1005 flagged?"
   "Is this transaction risky?"

5. credit_profile
   Use when the user asks specifically about:
   - credit score
   - credit profile
   - credit rating
   - credit history
   - monthly income or debt from their credit profile

   IMPORTANT:
   Questions about credit score or credit profile MUST be classified
   as credit_profile, NOT customer_info.

   Examples:
   "What is my credit score?"
   "Check my credit profile"
   "How good is my credit?"
   "Show my credit score"
   "What is my credit rating?"
   "Tell me my credit history"

6. loan_eligibility
   Use when the user asks:
   - whether they qualify for a loan
   - whether they are eligible for a loan
   - whether they can get a specific loan amount
   - loan qualification

   Examples:
   "Am I eligible for a loan?"
   "Can I get a loan of 500000?"
   "Do I qualify for a 5 lakh loan?"
   "Can I get a loan based on my income?"

7. emi
   Use when the user asks about:
   - EMI
   - monthly loan payment
   - loan repayment calculation
   - interest/payment calculation for a loan

   Examples:
   "Calculate EMI for 500000"
   "What will my monthly payment be?"
   "Calculate my loan EMI"
   "How much will I pay every month?"

8. unknown
   Use when:
   - the request is unrelated to banking
   - the request is unclear
   - the request cannot be mapped confidently to one of the above intents

IMPORTANT CLASSIFICATION RULES:

- Credit score/profile questions = credit_profile.
- Loan qualification questions = loan_eligibility.
- EMI/payment calculation questions = emi.
- Suspicious/fraud/risk questions = risk_analysis.
- Balance questions = balance.
- Transaction history questions = transactions.
- Name/email/customer identity questions = customer_info.
- Do NOT classify credit score questions as customer_info.
- Choose exactly ONE intent.
- Do not invent a new intent.

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
        "credit_profile",
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