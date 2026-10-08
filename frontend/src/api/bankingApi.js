import {
  DEFAULT_EMI,
  DEFAULT_LOAN_AMOUNT,
  DEMO_CONTEXT,
} from '../data/demoContext'

// Pull optional numbers out of free text; fall back to demo defaults.
function extractParams(message) {
  const amount = message
    .replace(/,/g, '')
    .match(/\b\d{4,}(?:\.\d+)?\b/)
  const rate = message.match(/(\d+(?:\.\d+)?)\s*%/)
  const years = message.match(/(\d+)\s*(?:years?|yrs?)\b/i)
  const value = amount ? Number(amount[0]) : null

  return {
    loan_amount: value ?? DEFAULT_LOAN_AMOUNT,
    principal: value ?? DEFAULT_EMI.principal,
    annual_interest_rate: rate ? Number(rate[1]) : DEFAULT_EMI.annual_interest_rate,
    tenure_years: years ? Number(years[1]) : DEFAULT_EMI.tenure_years,
  }
}

export async function sendChat(message) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, ...DEMO_CONTEXT, ...extractParams(message) }),
  })

  if (!response.ok) {
    throw new Error(`Backend returned ${response.status} ${response.statusText}`)
  }
  return response.json()
}

export async function checkHealth() {
  try {
    const response = await fetch('/health')
    return response.ok
  } catch {
    return false
  }
}
