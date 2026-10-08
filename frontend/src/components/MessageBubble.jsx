import ResultView from './ResultView'

export default function MessageBubble({ message }) {
  if (message.role === 'user') {
    return (
      <div className="msg msg-user">
        <div className="bubble bubble-user">{message.text}</div>
      </div>
    )
  }

  return (
    <div className="msg msg-ai">
      <span className="avatar" aria-hidden="true">AI</span>
      <div className="bubble bubble-ai">
        {message.loading && (
          <div className="typing" role="status" aria-label="Agents are working">
            <span /><span /><span />
          </div>
        )}
        {message.error && <div className="notice notice-bad">{message.error}</div>}
        {message.response && <ResultView response={message.response} />}
      </div>
    </div>
  )
}
