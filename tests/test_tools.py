import pytest

from backend.app.tools.banking_tools import (
    get_balance,
    get_credit_profile,
    get_customer,
    get_transaction,
    get_transactions,
)
from backend.app.tools.credit_tools import calculate_emi, check_loan_eligibility
from backend.app.tools.risk_tools import analyze_transaction_risk


# --- banking tools ---
def test_get_customer():
    assert get_customer("CUST001")["customer_id"] == "CUST001"
    assert get_customer("NOPE") is None


def test_get_balance():
    balance = get_balance("ACC001")
    assert balance["balance"] == 125000.50
    assert balance["currency"] == "INR"
    assert get_balance("NOPE") is None


def test_get_transactions():
    transactions = get_transactions("ACC001")
    assert {t["transaction_id"] for t in transactions} >= {"TXN1001", "TXN1005"}
    assert all(t["account_id"] == "ACC001" for t in transactions)
    assert get_transactions("NOPE") == []


def test_get_transaction():
    assert get_transaction("TXN1005")["amount"] == 95000.00
    assert get_transaction("NOPE") is None


def test_get_credit_profile():
    assert get_credit_profile("CUST001")["credit_score"] == 760
    assert get_credit_profile("NOPE") is None


# --- risk tool ---
def test_risk_high_for_txn1005():
    result = analyze_transaction_risk("TXN1005")
    assert result["risk_score"] == 100
    assert result["risk_level"] == "HIGH"
    assert result["status"] == "FLAGGED"
    assert result["reasons"]


def test_risk_low_for_normal_transaction():
    result = analyze_transaction_risk("TXN1001")
    assert result["risk_level"] == "LOW"
    assert result["status"] == "SAFE"


def test_risk_missing_transaction():
    result = analyze_transaction_risk("NOPE")
    assert result["status"] == "NOT_FOUND"
    assert result["risk_level"] == "UNKNOWN"


# --- credit tools ---
def test_loan_eligible():
    result = check_loan_eligibility("CUST001", 500000)
    assert result["eligible"] is True
    assert result["credit_score"] == 760


def test_loan_not_eligible_when_amount_too_high():
    result = check_loan_eligibility("CUST001", 85000 * 6 + 1)
    assert result["eligible"] is False
    assert result["reasons"]


def test_loan_missing_customer():
    result = check_loan_eligibility("NOPE", 100000)
    assert result["eligible"] is False
    assert result["reason"] == "Credit profile not found"


def test_emi_calculation():
    result = calculate_emi(500000, 8.5, 5)
    assert result["monthly_emi"] == 10258.27


def test_emi_zero_interest():
    assert calculate_emi(120000, 0, 1)["monthly_emi"] == 10000.0


@pytest.mark.parametrize(
    "args",
    [(0, 8.5, 5), (-1, 8.5, 5), (500000, -1, 5), (500000, 8.5, 0), (500000, 8.5, -2)],
)
def test_emi_invalid_inputs(args):
    with pytest.raises(ValueError):
        calculate_emi(*args)
