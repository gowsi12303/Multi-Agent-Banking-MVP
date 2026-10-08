CUSTOMERS = {
    "CUST001": {
        "customer_id": "CUST001",
        "name": "Arun Kumar",
        "email": "arun@example.com",
    },
    "CUST002": {
        "customer_id": "CUST002",
        "name": "Priya Sharma",
        "email": "priya@example.com",
    },
}


ACCOUNTS = {
    "ACC001": {
        "account_id": "ACC001",
        "customer_id": "CUST001",
        "account_type": "Savings",
        "balance": 125000.50,
        "currency": "INR",
        "status": "ACTIVE",
    },
    "ACC002": {
        "account_id": "ACC002",
        "customer_id": "CUST002",
        "account_type": "Savings",
        "balance": 78500.00,
        "currency": "INR",
        "status": "ACTIVE",
    },
}


TRANSACTIONS = {
    "TXN1001": {
        "transaction_id": "TXN1001",
        "account_id": "ACC001",
        "amount": 2500.00,
        "transaction_type": "DEBIT",
        "merchant": "Amazon",
        "category": "Shopping",
        "location": "Chennai",
        "status": "COMPLETED",
    },
    "TXN1002": {
        "transaction_id": "TXN1002",
        "account_id": "ACC001",
        "amount": 15000.00,
        "transaction_type": "CREDIT",
        "merchant": "Salary",
        "category": "Income",
        "location": "Chennai",
        "status": "COMPLETED",
    },
    "TXN1005": {
        "transaction_id": "TXN1005",
        "account_id": "ACC001",
        "amount": 95000.00,
        "transaction_type": "DEBIT",
        "merchant": "Unknown International Merchant",
        "category": "Unknown",
        "location": "International",
        "status": "PENDING_REVIEW",
    },
}


CREDIT_PROFILES = {
    "CUST001": {
        "customer_id": "CUST001",
        "credit_score": 760,
        "monthly_income": 85000,
        "employment_status": "EMPLOYED",
        "existing_debt": 15000,
    },
    "CUST002": {
        "customer_id": "CUST002",
        "credit_score": 680,
        "monthly_income": 55000,
        "employment_status": "EMPLOYED",
        "existing_debt": 12000,
    },
}