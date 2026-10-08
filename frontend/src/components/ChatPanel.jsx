import { useEffect, useRef, useState } from 'react'
import DemoContextBar from './DemoContextBar'
import MessageBubble from './MessageBubble'
import SuggestedPrompts from './SuggestedPrompts'

export default function ChatPanel({ messages, loading, onSend }) {
  const [draft, setDraft] = useState('')
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages])

  const submit = (event) => {
    event.preventDefault()
    const text = draft.trim()
    if (!text || loading) return
    setDraft('')
    onSend(text)
  }

  return (
    <section className="panel chat" aria-label="Chat">
      <div className="panel-head">
        <h2>Ask Banking AI</h2>
        <DemoContextBar />
      </div>

      <div className="messages" aria-live="polite">
        {messages.length === 0 && (
          <div className="empty">
            <h3>How can I help today?</h3>
            <p>
              Ask a banking question in natural language, or try a suggested prompt.
              Every answer comes from simulated data.
            </p>
          </div>
        )}
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        <div ref={endRef} />
      </div>

      <div className="composer">
        <SuggestedPrompts onSelect={onSend} disabled={loading} />
        <form onSubmit={submit} className="composer-form">
          <input
            type="text"
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            placeholder="e.g. Is transaction TXN1005 suspicious?"
            aria-label="Message"
            disabled={loading}
          />
          <button type="submit" disabled={loading || !draft.trim()}>
            {loading ? 'Working…' : 'Send'}
          </button>
        </form>
      </div>
    </section>
  )
}
