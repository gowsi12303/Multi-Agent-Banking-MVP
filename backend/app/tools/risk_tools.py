from backend.app.tools.banking_tools import get_transaction


def analyze_transaction_risk(transaction_id: str):
    transaction = get_transaction(transaction_id)

    if not transaction:
        return {
            "transaction_id": transaction_id,
            "status": "NOT_FOUND",
            "risk_score": 0,
            "risk_level": "UNKNOWN",
            "reasons": ["Transaction not found"],
        }

    risk_score = 0
    reasons = []

    amount = transaction["amount"]

    # Large transaction
    if amount >= 50000:
        risk_score += 40
        reasons.append("Transaction amount is unusually high")

    # International transaction
    if transaction["location"] == "International":
        risk_score += 30
        reasons.append("International transaction detected")

    # Unknown merchant/category
    if transaction["category"] == "Unknown":
        risk_score += 20
        reasons.append("Unknown transaction category")

    if transaction["merchant"].startswith("Unknown"):
        risk_score += 10
        reasons.append("Unknown merchant detected")

    # Keep score within 100
    risk_score = min(risk_score, 100)

    if risk_score >= 70:
        risk_level = "HIGH"
        status = "FLAGGED"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
        status = "REVIEW"
    else:
        risk_level = "LOW"
        status = "SAFE"

    return {
        "transaction_id": transaction_id,
        "status": status,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons,
        "transaction": transaction,
    }