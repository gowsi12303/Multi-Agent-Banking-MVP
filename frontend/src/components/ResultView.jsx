import { useState } from 'react'

const money = (value, currency = 'INR') =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency }).format(value)

function Stat({ label, value, tone }) {
  return (
    <div className="stat">
      <span className="stat-label">{label}</span>
      <span className={`stat-value ${tone ? `tone-${tone}` : ''}`}>{value}</span>
    </div>
  )
}

function Balance({ data }) {
  return (
    <div className="result-card">
      <h3>Account balance</h3>
      <div className="balance-figure">{money(data.balance, data.currency)}</div>
      <div className="stat-row">
        <Stat label="Account" value={data.account_id} />
        <Stat label="Status" value={data.status} tone={data.status === 'ACTIVE' ? 'good' : 'warn'} />
      </div>
    </div>
  )
}

function Transactions({ data }) {
  if (!data.length) return <p className="muted">No transactions found for this account.</p>
  return (
    <div className="result-card">
      <h3>Recent transactions</h3>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Merchant</th>
              <th>Category</th>
              <th>Location</th>
              <th className="num">Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.map((t) => (
              <tr key={t.transaction_id}>
                <td>{t.transaction_id}</td>
                <td>{t.merchant}</td>
                <td>{t.category}</td>
                <td>{t.location}</td>
                <td className={`num ${t.transaction_type === 'CREDIT' ? 'tone-good' : 'tone-debit'}`}>
                  {t.transaction_type === 'CREDIT' ? '+' : '−'}
                  {money(t.amount)}
                </td>
                <td>
                  <span className={`pill ${t.status === 'COMPLETED' ? 'pill-good' : 'pill-warn'}`}>
                    {t.status.replace('_', ' ')}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function Risk({ data }) {
  const tone = { HIGH: 'bad', MEDIUM: 'warn', LOW: 'good' }[data.risk_level] ?? 'warn'
  const txn = data.transaction
  return (
    <div className="result-card">
      <h3>Transaction risk analysis</h3>
      <div className="stat-row">
        <Stat label="Transaction" value={data.transaction_id} />
        <Stat label="Risk level" value={data.risk_level} tone={tone} />
        <Stat label="Decision" value={data.status} tone={tone} />
      </div>
      <div className="meter" role="img" aria-label={`Risk score ${data.risk_score} of 100`}>
        <div className={`meter-fill meter-${tone}`} style={{ width: `${data.risk_score}%` }} />
      </div>
      <p className="meter-caption">Risk score {data.risk_score} / 100</p>
      {txn && (
        <p className="muted">
          {money(txn.amount)} {txn.transaction_type.toLowerCase()} · {txn.merchant} · {txn.location}
        </p>
      )}
      {data.reasons?.length > 0 && (
        <ul className="reason-list">
          {data.reasons.map((reason) => (
            <li key={reason}>{reason}</li>
          ))}
        </ul>
      )}
    </div>
  )
}

function Loan({ data }) {
  return (
    <div className="result-card">
      <h3>Loan eligibility</h3>
      <div className={`verdict ${data.eligible ? 'verdict-good' : 'verdict-bad'}`}>
        {data.eligible ? 'Eligible' : 'Not eligible'}
      </div>
      <div className="stat-row">
        {data.loan_amount != null && <Stat label="Requested" value={money(data.loan_amount)} />}
        {data.credit_score != null && <Stat label="Credit score" value={data.credit_score} />}
        {data.monthly_income != null && (
          <Stat label="Monthly income" value={money(data.monthly_income)} />
        )}
      </div>
      {data.reason && <p className="muted">{data.reason}</p>}
      {data.reasons?.length > 0 && (
        <ul className="reason-list">
          {data.reasons.map((reason) => (
            <li key={reason}>{reason}</li>
          ))}
        </ul>
      )}
    </div>
  )
}

function Emi({ data }) {
  return (
    <div className="result-card">
      <h3>EMI calculation</h3>
      <div className="balance-figure">
        {money(data.monthly_emi)} <small>/ month</small>
      </div>
      <div className="stat-row">
        <Stat label="Principal" value={money(data.principal)} />
        <Stat label="Rate" value={`${data.annual_interest_rate}% p.a.`} />
        <Stat label="Tenure" value={`${data.tenure_years} years`} />
        <Stat label="Total interest" value={money(data.total_interest)} />
        <Stat label="Total payment" value={money(data.total_payment)} />
      </div>
    </div>
  )
}

const VIEWS = {
  balance: Balance,
  transactions: Transactions,
  risk_analysis: Risk,
  loan_eligibility: Loan,
  emi: Emi,
}

export default function ResultView({ response }) {
  const [showRaw, setShowRaw] = useState(false)
  const intent = response.intent?.intent
  const result = response.routing?.result
  const View = VIEWS[intent]

  let body
  if (!result || result.status === 'ERROR' || result.status === 'NOT_FOUND') {
    body = (
      <div className="notice notice-warn">
        {result?.message ?? 'The request could not be completed.'}
      </div>
    )
  } else if (View && result.data != null) {
    body = <View data={result.data} />
  } else {
    body = <pre className="raw">{JSON.stringify(result.data ?? result, null, 2)}</pre>
  }

  return (
    <div className="result">
      {body}
      <button type="button" className="link-btn" onClick={() => setShowRaw((v) => !v)}>
        {showRaw ? 'Hide raw JSON' : 'Show raw JSON'}
      </button>
      {showRaw && <pre className="raw">{JSON.stringify(response, null, 2)}</pre>}
    </div>
  )
}
