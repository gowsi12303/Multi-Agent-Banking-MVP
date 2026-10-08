from backend.app.banking_data import (
    CUSTOMERS,
    ACCOUNTS,
    TRANSACTIONS,
    CREDIT_PROFILES,
)


def get_customer(customer_id: str):
    return CUSTOMERS.get(customer_id)


def get_account(account_id: str):
    return ACCOUNTS.get(account_id)


def get_balance(account_id: str):
    account = ACCOUNTS.get(account_id)

    if not account:
        return None

    return {
        "account_id": account_id,
        "balance": account["balance"],
        "currency": account["currency"],
        "status": account["status"],
    }


def get_transactions(account_id: str):
    return [
        transaction
        for transaction in TRANSACTIONS.values()
        if transaction["account_id"] == account_id
    ]


def get_transaction(transaction_id: str):
    return TRANSACTIONS.get(transaction_id)


def get_credit_profile(customer_id: str):
    return CREDIT_PROFILES.get(customer_id)