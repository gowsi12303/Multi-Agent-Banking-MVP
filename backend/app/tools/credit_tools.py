from backend.app.tools.banking_tools import get_credit_profile


def check_loan_eligibility(customer_id: str, loan_amount: float):
    profile = get_credit_profile(customer_id)

    if not profile:
        return {
            "customer_id": customer_id,
            "eligible": False,
            "reason": "Credit profile not found",
        }

    reasons = []

    if profile["credit_score"] < 650:
        reasons.append("Credit score is below the minimum requirement")

    if profile["employment_status"] != "EMPLOYED":
        reasons.append("Customer employment status does not meet the requirement")

    if loan_amount > profile["monthly_income"] * 6:
        reasons.append("Requested loan amount is high compared with monthly income")

    eligible = len(reasons) == 0

    return {
        "customer_id": customer_id,
        "loan_amount": loan_amount,
        "eligible": eligible,
        "credit_score": profile["credit_score"],
        "monthly_income": profile["monthly_income"],
        "reasons": reasons,
    }


def calculate_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_years: int,
):
    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative")

    if tenure_years <= 0:
        raise ValueError("Tenure must be greater than zero")

    monthly_rate = annual_interest_rate / (12 * 100)
    months = tenure_years * 12

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return {
        "principal": principal,
        "annual_interest_rate": annual_interest_rate,
        "tenure_years": tenure_years,
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
    }