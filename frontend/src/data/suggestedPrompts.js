import { DEFAULT_EMI, DEFAULT_LOAN_AMOUNT } from './demoContext'

export const SUGGESTED_PROMPTS = [
  {
    id: 'balance',
    label: 'Account balance',
    icon: '₹',
    message: 'What is my account balance?',
  },
  {
    id: 'transactions',
    label: 'Recent transactions',
    icon: '≡',
    message: 'Show my recent transactions',
  },
  {
    id: 'risk',
    label: 'Suspicious transaction',
    icon: '!',
    message: 'Is transaction TXN1005 suspicious?',
  },
  {
    id: 'loan',
    label: 'Loan eligibility',
    icon: '✓',
    message: `Am I eligible for a loan of ${DEFAULT_LOAN_AMOUNT}?`,
  },
  {
    id: 'emi',
    label: 'EMI calculation',
    icon: '%',
    message: `Calculate EMI for ${DEFAULT_EMI.principal} at ${DEFAULT_EMI.annual_interest_rate}% for ${DEFAULT_EMI.tenure_years} years`,
  },
]
