from fastapi import FastAPI
from pydantic import BaseModel

from backend.app.agents.supervisor_agent import process_user_message


app = FastAPI(
    title="Multi-Agent Banking MVP",
    description="Simulated Banking Architecture with Multi-Agent AI",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str
    customer_id: str | None = None
    account_id: str | None = None
    transaction_id: str | None = None
    loan_amount: float | None = None
    principal: float | None = None
    annual_interest_rate: float | None = None
    tenure_years: int | None = None


@app.get("/")
def root():
    return {
        "message": "Multi-Agent Banking MVP is running",
        "status": "healthy",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/api/chat")
def chat(request: ChatRequest):
    return process_user_message(
        request.message,
        customer_id=request.customer_id,
        account_id=request.account_id,
        transaction_id=request.transaction_id,
        loan_amount=request.loan_amount,
        principal=request.principal,
        annual_interest_rate=request.annual_interest_rate,
        tenure_years=request.tenure_years,
    )
