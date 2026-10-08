from unittest.mock import patch

# supervisor_agent.py does `from backend.app.llm import detect_intent`, so the
# name to patch is the one bound in the supervisor module.
DETECT = "backend.app.agents.supervisor_agent.detect_intent"


def post_chat(client, intent, **body):
    with patch(DETECT, return_value={"intent": intent, "confidence": 0.9}) as mock:
        response = client.post("/api/chat", json={"message": "test message", **body})
    mock.assert_called_once_with("test message")
    return response


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_balance(client):
    body = post_chat(client, "balance", account_id="ACC001").json()
    assert body["intent"]["intent"] == "balance"
    assert body["routing"]["selected_agent"] == "customer_agent"
    assert body["routing"]["result"]["data"]["balance"] == 125000.50


def test_chat_transactions(client):
    body = post_chat(client, "transactions", account_id="ACC001").json()
    assert body["routing"]["selected_agent"] == "customer_agent"
    assert len(body["routing"]["result"]["data"]) >= 3


def test_chat_risk(client):
    body = post_chat(client, "risk_analysis", transaction_id="TXN1005").json()
    assert body["routing"]["selected_agent"] == "risk_agent"
    assert body["routing"]["result"]["data"]["risk_level"] == "HIGH"


def test_chat_loan(client):
    body = post_chat(client, "loan_eligibility", customer_id="CUST001", loan_amount=500000).json()
    assert body["routing"]["selected_agent"] == "credit_agent"
    assert body["routing"]["result"]["data"]["eligible"] is True


def test_chat_emi(client):
    body = post_chat(
        client, "emi", principal=500000, annual_interest_rate=8.5, tenure_years=5
    ).json()
    assert body["routing"]["selected_agent"] == "credit_agent"
    assert body["routing"]["result"]["data"]["monthly_emi"] == 10258.27


def test_chat_all_params_do_not_crash(client):
    response = post_chat(
        client,
        "balance",
        customer_id="CUST001",
        account_id="ACC001",
        transaction_id="TXN1005",
        loan_amount=500000,
        principal=500000,
        annual_interest_rate=8.5,
        tenure_years=5,
    )
    assert response.status_code == 200
    assert response.json()["routing"]["result"]["status"] == "SUCCESS"


def test_chat_unknown_intent(client):
    body = post_chat(client, "unknown").json()
    assert body["intent"] == {"intent": "unknown", "confidence": 0.9}
    assert body["routing"]["selected_agent"] is None
    assert body["routing"]["result"]["status"] == "ERROR"
    assert body["routing"]["result"]["message"] == "I could not understand the banking request."


def test_chat_requires_message(client):
    assert client.post("/api/chat", json={}).status_code == 422
