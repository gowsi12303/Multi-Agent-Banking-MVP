export default function Header({ online }) {
  const state = online === null ? 'checking' : online ? 'online' : 'offline'
  const label =
    online === null ? 'Checking backend…' : online ? 'Backend online' : 'Backend offline'

  return (
    <header className="header">
      <div className="brand">
        <span className="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 32 32" width="22" height="22">
            <path
              d="M16 6 5 12v2h22v-2L16 6Zm-8 10v7h3v-7H8Zm6.5 0v7h3v-7h-3Zm6.5 0v7h3v-7h-3ZM6 25v2h20v-2H6Z"
              fill="currentColor"
            />
          </svg>
        </span>
        <div>
          <h1>Banking AI</h1>
          <p>Multi-agent assistant</p>
        </div>
      </div>
      <div className="header-badges">
        <span className="badge badge-sim">Simulated data only</span>
        <span className={`status status-${state}`}>
          <span className="status-dot" />
          {label}
        </span>
      </div>
    </header>
  )
}
