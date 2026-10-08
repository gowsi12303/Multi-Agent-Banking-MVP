from backend.app.llm import detect_intent

from backend.app.agents.customer_agent import customer_agent
from backend.app.agents.risk_agent import risk_agent
from backend.app.agents.credit_agent import credit_agent


def supervisor_agent(
    intent: str,
    **kwargs,
):
    """
    Supervisor/Orchestrator Agent.

    Routes requests to the appropriate
    specialized banking agent.
    """

    if intent in ["customer_info", "balance", "transactions"]:
        if intent == "customer_info":
            agent_args = {"customer_id": kwargs.get("customer_id")}
        else:
            agent_args = {"account_id": kwargs.get("account_id")}

        result = customer_agent(
            request_type=intent,
            **agent_args,
        )

        return {
            "supervisor": "supervisor_agent",
            "selected_agent": "customer_agent",
            "result": result,
        }

    if intent == "risk_analysis":
        result = risk_agent(
            kwargs.get("transaction_id"),
        )

        return {
            "supervisor": "supervisor_agent",
            "selected_agent": "risk_agent",
            "result": result,
        }

    if intent in ["loan_eligibility", "emi"]:
        if intent == "loan_eligibility":
            agent_args = {
                "customer_id": kwargs.get("customer_id"),
                "loan_amount": kwargs.get("loan_amount"),
            }
        else:
            agent_args = {
                "principal": kwargs.get("principal"),
                "annual_interest_rate": kwargs.get("annual_interest_rate"),
                "tenure_years": kwargs.get("tenure_years"),
            }

        result = credit_agent(
            request_type=intent,
            **agent_args,
        )

        return {
            "supervisor": "supervisor_agent",
            "selected_agent": "credit_agent",
            "result": result,
        }

    return {
        "supervisor": "supervisor_agent",
        "selected_agent": None,
        "result": {
            "status": "ERROR",
            "message": f"Unknown intent: {intent}",
        },
    }


def process_user_message(user_message: str, **kwargs):
    """
    Complete natural-language banking flow.

    User message
        ↓
    Intent detection
        ↓
    Supervisor
        ↓
    Specialized agent
    """

    intent_result = detect_intent(user_message)

    intent = intent_result["intent"]

    if intent == "unknown":
        return {
            "user_message": user_message,
            "intent": intent_result,
            "routing": {
                "supervisor": "supervisor_agent",
                "selected_agent": None,
                "result": {
                    "status": "ERROR",
                    "message": "I could not understand the banking request.",
                },
            },
        }

    result = supervisor_agent(
        intent,
        **kwargs,
    )

    return {
        "user_message": user_message,
        "intent": intent_result,
        "routing": result,
    }