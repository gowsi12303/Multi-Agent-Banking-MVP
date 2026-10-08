from backend.app.tools.risk_tools import analyze_transaction_risk


def risk_agent(transaction_id: str):
    """
    Risk/Fraud Agent.

    Analyzes a transaction and determines:
    - Risk score
    - Risk level
    - Fraud indicators
    """

    if not transaction_id:
        return {
            "agent": "risk_agent",
            "status": "ERROR",
            "message": "Transaction ID is required",
        }

    result = analyze_transaction_risk(transaction_id)

    if result["status"] == "NOT_FOUND":
        return {
            "agent": "risk_agent",
            "status": "NOT_FOUND",
            "data": result,
        }

    return {
        "agent": "risk_agent",
        "status": "SUCCESS",
        "data": result,
    }