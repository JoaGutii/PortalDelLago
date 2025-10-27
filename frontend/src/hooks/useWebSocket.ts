import { useEffect, useRef, useState } from 'react'

export default function useWebSocket(url: string) {
  const [messages, setMessages] = useState<any[]>([])
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const ws = new WebSocket(url)
    wsRef.current = ws
    ws.onmessage = (e) => {
      try { setMessages(prev => [...prev, JSON.parse(e.data)]) }
      catch { /* noop */ }
    }
    return () => { ws.close() }
  }, [url])

  return messages
}
