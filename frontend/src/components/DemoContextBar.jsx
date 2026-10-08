import { DEMO_CONTEXT } from '../data/demoContext'

const ITEMS = [
  ['Customer', DEMO_CONTEXT.customer_id],
  ['Account', DEMO_CONTEXT.account_id],
  ['Transaction', DEMO_CONTEXT.transaction_id],
]

export default function DemoContextBar() {
  return (
    <div className="context-bar" aria-label="Demo context">
      <span className="context-title">Demo context</span>
      {ITEMS.map(([label, value]) => (
        <span className="context-chip" key={label}>
          {label} <strong>{value}</strong>
        </span>
      ))}
    </div>
  )
}
