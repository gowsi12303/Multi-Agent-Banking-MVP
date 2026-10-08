import TraceStep from './TraceStep'

const AGENT_LABELS = {
  customer_agent: 'Customer Agent',
  risk_agent: 'Risk / Fraud Agent',
  credit_agent: 'Credit / Loan Agent',
}

const TOOLS = {
  balance: 'get_balance',
  transactions: 'get_transactions',
  customer_info: 'get_customer',
  risk_analysis: 'analyze_transaction_risk',
  loan_eligibility: 'check_loan_eligibility',
  emi: 'calculate_emi',
}

export default function TracePanel({ response, loading, error }) {
  let content

  if (loading) {
    content = <p className="muted">Agents are processing your request…</p>
  } else if (error) {
    content = <div className="notice notice-bad">Pipeline did not complete.</div>
  } else if (!response) {
    content = (
      <p className="muted">
        Send a message to see how Gemini, the Supervisor and the specialised agents
        handle it.
      </p>
    )
  } else {
    const intent = response.intent ?? {}
    const routing = response.routing ?? {}
    const result = routing.result ?? {}
    const agent = routing.selected_agent
    const ok = result.status === 'SUCCESS'
    const confidence =
      typeof intent.confidence === 'number' ? `${Math.round(intent.confidence * 100)}%` : '—'
    const agentName = agent ? (AGENT_LABELS[agent] ?? agent) : null
    const agentStatus = agent ? (ok ? 'done' : 'error') : 'idle'

    content = (
      <ol className="trace">
        <TraceStep
          index={1}
          title="Gemini intent detection"
          status={intent.intent === 'unknown' ? 'error' : 'done'}
        >
          <div>Intent <code>{intent.intent ?? 'unknown'}</code></div>
          <div>Confidence <strong>{confidence}</strong></div>
        </TraceStep>
        <TraceStep index={2} title="Supervisor Agent" status={agent ? 'done' : 'error'}>
          <div>{routing.supervisor ?? 'supervisor_agent'}</div>
          <div>Routed to <strong>{agentName ?? 'no agent'}</strong></div>
        </TraceStep>
        <TraceStep index={3} title="Specialised agent" status={agentStatus}>
          <div>{agentName ?? 'Not executed'}</div>
          {result.status && <div>Status <code>{result.status}</code></div>}
        </TraceStep>
        <TraceStep index={4} title="Tool / result" status={agentStatus}>
          {TOOLS[intent.intent] && <div>Tool <code>{TOOLS[intent.intent]}()</code></div>}
          <div>{ok ? 'Returned simulated data' : (result.message ?? 'No result')}</div>
        </TraceStep>
      </ol>
    )
  }

  return (
    <aside className="panel trace-panel" aria-label="Agent trace">
      <div className="panel-head">
        <h2>Agent execution trace</h2>
        <p className="muted">Latest request</p>
      </div>
      {content}
    </aside>
  )
}
