from backend.app.agents.credit_agent import credit_agent
from backend.app.agents.customer_agent import customer_agent
from backend.app.agents.risk_agent import risk_agent
from backend.app.agents.supervisor_agent import supervisor_agent


# --- customer agent ---
def test_customer_info_success():
    result = customer_agent(customer_id="CUST001", request_type="customer_info")
    assert result["status"] == "SUCCESS"
    assert result["data"]["customer_id"] == "CUST001"


def test_customer_errors():
    assert customer_agent(request_type="customer_info")["status"] == "ERROR"
    assert customer_agent(customer_id="NOPE", request_type="customer_info")["status"] == "NOT_FOUND"
    assert customer_agent(request_type="balance")["status"] == "ERROR"
    assert customer_agent(account_id="NOPE", request_type="balance")["status"] == "NOT_FOUND"
    assert customer_agent(request_type="transactions")["status"] == "ERROR"
    assert customer_agent(request_type="bogus")["status"] == "ERROR"


def test_customer_balance_and_transactions_success():
    balance = customer_agent(account_id="ACC001", request_type="balance")
    assert balance["status"] == "SUCCESS"
    assert balance["data"]["balance"] == 125000.50

    transactions = customer_agent(account_id="ACC001", request_type="transactions")
    assert transactions["status"] == "SUCCESS"
    assert len(transactions["data"]) >= 3


# --- risk agent ---
def test_risk_agent_paths():
    ok = risk_agent("TXN1005")
    assert ok["status"] == "SUCCESS"
    assert ok["data"]["risk_level"] == "HIGH"
    assert risk_agent("NOPE")["status"] == "NOT_FOUND"
    assert risk_agent(None)["status"] == "ERROR"


# --- credit agent ---
def test_credit_agent_loan():
    ok = credit_agent("loan_eligibility", customer_id="CUST001", loan_amount=500000)
    assert ok["status"] == "SUCCESS"
    assert ok["data"]["eligible"] is True
    assert credit_agent("loan_eligibility", customer_id="CUST001")["status"] == "ERROR"


def test_credit_agent_emi():
    ok = credit_agent("emi", principal=500000, annual_interest_rate=8.5, tenure_years=5)
    assert ok["status"] == "SUCCESS"
    assert ok["data"]["monthly_emi"] == 10258.27
    assert credit_agent("emi", principal=500000)["status"] == "ERROR"
    invalid = credit_agent("emi", principal=0, annual_interest_rate=8.5, tenure_years=5)
    assert invalid["status"] == "ERROR"


def test_credit_agent_unsupported_type():
    assert credit_agent("bogus")["status"] == "ERROR"


# --- supervisor ---
def test_supervisor_routing():
    cases = [
        ("balance", {"account_id": "ACC001"}, "customer_agent"),
        ("transactions", {"account_id": "ACC001"}, "customer_agent"),
        ("customer_info", {"customer_id": "CUST001"}, "customer_agent"),
        ("risk_analysis", {"transaction_id": "TXN1005"}, "risk_agent"),
        ("loan_eligibility", {"customer_id": "CUST001", "loan_amount": 500000}, "credit_agent"),
        (
            "emi",
            {"principal": 500000, "annual_interest_rate": 8.5, "tenure_years": 5},
            "credit_agent",
        ),
    ]
    for intent, params, expected_agent in cases:
        result = supervisor_agent(intent, **params)
        assert result["selected_agent"] == expected_agent, intent
        assert result["result"]["status"] == "SUCCESS", intent


def test_supervisor_ignores_irrelevant_params():
    # All request params are forwarded; each agent must get only what it accepts.
    everything = dict(
        customer_id="CUST001",
        account_id="ACC001",
        transaction_id="TXN1005",
        loan_amount=500000,
        principal=500000,
        annual_interest_rate=8.5,
        tenure_years=5,
    )
    for intent in ["balance", "customer_info", "risk_analysis", "loan_eligibility", "emi"]:
        assert supervisor_agent(intent, **everything)["result"]["status"] == "SUCCESS"


def test_supervisor_unknown_intent():
    result = supervisor_agent("bogus")
    assert result["selected_agent"] is None
    assert result["result"]["status"] == "ERROR"
