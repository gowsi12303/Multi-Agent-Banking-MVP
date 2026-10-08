from backend.app.tools.banking_tools import get_credit_profile
from backend.app.tools.credit_tools import (
    check_loan_eligibility,
    calculate_emi,
)


def credit_agent(
    request_type: str,
    customer_id: str | None = None,
    loan_amount: float | None = None,
    principal: float | None = None,
    annual_interest_rate: float | None = None,
    tenure_years: int | None = None,
):
    """
    Credit/Loan Agent.

    Handles:
    - Credit profile / credit score
    - Loan eligibility
    - EMI calculation
    """

    if request_type == "credit_profile":
        if not customer_id:
            return {
                "agent": "credit_agent",
                "status": "ERROR",
                "message": "Customer ID is required",
            }

        result = get_credit_profile(customer_id)

        return {
            "agent": "credit_agent",
            "status": "SUCCESS",
            "data": result,
        }

    if request_type == "loan_eligibility":
        if not customer_id or loan_amount is None:
            return {
                "agent": "credit_agent",
                "status": "ERROR",
                "message": "Customer ID and loan amount are required",
            }

        result = check_loan_eligibility(
            customer_id,
            loan_amount,
        )

        return {
            "agent": "credit_agent",
            "status": "SUCCESS",
            "data": result,
        }

    if request_type == "emi":
        if (
            principal is None
            or annual_interest_rate is None
            or tenure_years is None
        ):
            return {
                "agent": "credit_agent",
                "status": "ERROR",
                "message": "Principal, interest rate and tenure are required",
            }

        try:
            result = calculate_emi(
                principal,
                annual_interest_rate,
                tenure_years,
            )

            return {
                "agent": "credit_agent",
                "status": "SUCCESS",
                "data": result,
            }

        except ValueError as error:
            return {
                "agent": "credit_agent",
                "status": "ERROR",
                "message": str(error),
            }

    return {
        "agent": "credit_agent",
        "status": "ERROR",
        "message": f"Unsupported request type: {request_type}",
    }