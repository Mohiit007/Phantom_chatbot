import { useState } from 'react'
import { useAgentChat } from '../api/hooks'

export default function AgentChat() {
  const [message, setMessage] = useState('Plan wedding in Dec 2026 for 8L and how is market today?')
  const chat = useAgentChat()

  const renderMarketCard = (name, info) => {
    if (!info || typeof info !== 'object') return null
    const currency = info.currency || 'INR'
    const fmt = new Intl.NumberFormat('en-IN', { style: 'currency', currency, maximumFractionDigits: 0 })
    return (
      <div key={name} className="rounded-md border border-gray-100 dark:border-gray-800 p-3 bg-gray-50 dark:bg-gray-900 slide-up">
        <div className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">{name}</div>
        <div className="mt-1 flex items-baseline gap-2">
          <div className="text-xl font-semibold">{fmt.format(info.last_price ?? 0)}</div>
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-100 text-blue-700 dark:bg-red-900/40 dark:text-red-200">{info.symbol}</span>
        </div>
        <div className="text-xs text-gray-500 dark:text-gray-400">Currency: {currency}</div>
      </div>
    )
  }

  return (
    <div className="grid gap-4 fade-in">
      <div className="card">
        <h2 className="text-lg font-semibold mb-2">Ask Phantom Agent</h2>
        <form className="grid gap-3" onSubmit={(e)=>{e.preventDefault(); chat.mutate({ message })}}>
          <textarea className="input h-28" value={message} onChange={e=>setMessage(e.target.value)} />
          <button className="btn" disabled={chat.isPending}>Send</button>
        </form>
      </div>
      {chat.data && (
        <div className="grid md:grid-cols-2 gap-4">
          <div className="card">
            <h3 className="font-medium mb-2">Reply</h3>
            <p className="text-sm whitespace-pre-wrap">{chat.data.reply}</p>
          </div>
          {chat.data.plan && (
            <div className="card text-sm slide-up">
              <h3 className="font-medium mb-2">Plan</h3>
              <div>Event: <b>{chat.data.plan.event_name}</b></div>
              <div>Year: <b>{chat.data.plan.target_year}</b></div>
              <div>Future Cost: <b>₹{chat.data.plan.future_cost}</b></div>
              <div>Monthly Saving: <b>₹{chat.data.plan.monthly_saving_needed}</b></div>
            </div>
          )}
          {chat.data.market_summary && (
            <div className="card text-sm slide-up">
              <h3 className="font-medium mb-2">Market Summary</h3>
              {Array.isArray(chat.data.market_summary) || typeof chat.data.market_summary !== 'object' ? (
                <pre className="bg-gray-50 dark:bg-gray-800 dark:text-gray-100 border border-gray-100 dark:border-gray-800 p-2 rounded overflow-auto">{JSON.stringify(chat.data.market_summary, null, 2)}</pre>
              ) : (
                <div className="grid grid-cols-1 gap-3">
                  {Object.entries(chat.data.market_summary).map(([name, info]) => renderMarketCard(name, info))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
