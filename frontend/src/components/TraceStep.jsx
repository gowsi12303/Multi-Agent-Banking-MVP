export default function TraceStep({ index, title, status, children }) {
  return (
    <li className={`trace-step trace-${status}`}>
      <span className="trace-index" aria-hidden="true">
        {status === 'done' ? '✓' : status === 'error' ? '!' : index}
      </span>
      <div className="trace-body">
        <h4>{title}</h4>
        <div className="trace-detail">{children}</div>
      </div>
    </li>
  )
}
