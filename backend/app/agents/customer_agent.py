from backend.app.tools.banking_tools import (
    get_customer,
    get_balance,
    get_transactions,
)


def customer_agent(
    customer_id: str | None = None,
    account_id: str | None = None,
    request_type: str = "customer_info",
):
    """
    Customer/Banking Agent.

    Handles:
    - Customer information
    - Account balance
    - Recent transactions
    """

    if request_type == "customer_info":
        if not customer_id:
            return {
                "agent": "customer_agent",
                "status": "ERROR",
                "message": "Customer ID is required",
            }

        customer = get_customer(customer_id)

        if not customer:
            return {
                "agent": "customer_agent",
                "status": "NOT_FOUND",
                "message": "Customer not found",
            }

        return {
            "agent": "customer_agent",
            "status": "SUCCESS",
            "data": customer,
        }

    if request_type == "balance":
        if not account_id:
            return {
                "agent": "customer_agent",
                "status": "ERROR",
                "message": "Account ID is required",
            }

        balance = get_balance(account_id)

        if not balance:
            return {
                "agent": "customer_agent",
                "status": "NOT_FOUND",
                "message": "Account not found",
            }

        return {
            "agent": "customer_agent",
            "status": "SUCCESS",
            "data": balance,
        }

    if request_type == "transactions":
        if not account_id:
            return {
                "agent": "customer_agent",
                "status": "ERROR",
                "message": "Account ID is required",
            }

        transactions = get_transactions(account_id)

        return {
            "agent": "customer_agent",
            "status": "SUCCESS",
            "data": transactions,
        }

    return {
        "agent": "customer_agent",
        "status": "ERROR",
        "message": f"Unsupported request type: {request_type}",
    }