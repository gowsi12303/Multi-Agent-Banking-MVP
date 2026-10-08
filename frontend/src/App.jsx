import { useCallback, useEffect, useRef, useState } from 'react'
import { checkHealth, sendChat } from './api/bankingApi'
import ChatPanel from './components/ChatPanel'
import Header from './components/Header'
import TracePanel from './components/TracePanel'
import './styles/app.css'

export default function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [online, setOnline] = useState(null)
  const nextId = useRef(0)

  useEffect(() => {
    let cancelled = false
    const poll = async () => {
      const ok = await checkHealth()
      if (!cancelled) setOnline(ok)
    }
    poll()
    const timer = setInterval(poll, 15000)
    return () => {
      cancelled = true
      clearInterval(timer)
    }
  }, [])

  const handleSend = useCallback(async (text) => {
    const userId = nextId.current++
    const aiId = nextId.current++
    setMessages((prev) => [
      ...prev,
      { id: userId, role: 'user', text },
      { id: aiId, role: 'assistant', loading: true },
    ])
    setLoading(true)

    const update = (patch) =>
      setMessages((prev) =>
        prev.map((m) => (m.id === aiId ? { ...m, loading: false, ...patch } : m)),
      )

    try {
      update({ response: await sendChat(text) })
      setOnline(true)
    } catch (err) {
      const unreachable = err instanceof TypeError
      if (unreachable) setOnline(false)
      update({
        error: unreachable
          ? 'Cannot reach the backend. Make sure FastAPI is running on http://127.0.0.1:8000.'
          : err.message,
      })
    } finally {
      setLoading(false)
    }
  }, [])

  const latest = [...messages].reverse().find((m) => m.role === 'assistant')

  return (
    <div className="app">
      <Header online={online} />
      <main className="layout">
        <ChatPanel messages={messages} loading={loading} onSend={handleSend} />
        <TracePanel
          response={latest?.response}
          loading={latest?.loading}
          error={latest?.error}
        />
      </main>
      <footer className="footer">
        Demo project · all banking data is simulated · no real transactions
      </footer>
    </div>
  )
}
