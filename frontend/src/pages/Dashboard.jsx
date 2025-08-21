import { useMarketSummary, useAdvice } from '../api/hooks'
import { Line, Doughnut, Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, BarElement, Title, Tooltip, Legend)

const inr = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 })

export default function Dashboard() {
  const { data: market, isLoading: marketLoading, isError: marketError, error: marketErr } = useMarketSummary()
  const { data: advice, isLoading: adviceLoading, isError: adviceError, error: adviceErr } = useAdvice()

  const labels = ['Equity', 'Debt', 'Cash']
  const alloc = advice?.suggested_allocation || { equity: 0.4, debt: 0.4, cash: 0.2 }
  const lineData = {
    labels,
    datasets: [
      {
        label: 'Allocation %',
        data: [alloc.equity * 100, alloc.debt * 100, alloc.cash * 100],
        borderColor: '#4f46e5',
        backgroundColor: 'rgba(79,70,229,0.2)'
      }
    ]
  }

  const doughnutData = {
    labels,
    datasets: [
      {
        label: 'Allocation %',
        data: [alloc.equity * 100, alloc.debt * 100, alloc.cash * 100],
        backgroundColor: ['#4f46e5', '#06b6d4', '#f59e0b'],
        borderColor: ['#312e81', '#0e7490', '#92400e']
      }
    ]
  }

  const inc = advice?.monthly_income_total || 0
  const exp = advice?.monthly_expense_total || 0
  const sav = advice?.monthly_savings || 0
  const barData = {
    labels: ['Income', 'Expenses', 'Savings'],
    datasets: [
      {
        label: 'Amount (₹)',
        data: [inc, exp, sav],
        backgroundColor: ['#22c55e', '#ef4444', '#3b82f6']
      }
    ]
  }

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

  // External tooltip for fade/scale effect
  const externalTooltip = (context) => {
    const { chart, tooltip } = context
    let el = chart.canvas.parentNode.querySelector('.chartjs-tooltip')
    if (!el) {
      el = document.createElement('div')
      el.className = 'chartjs-tooltip'
      chart.canvas.parentNode.appendChild(el)
    }
    if (tooltip.opacity === 0) {
      el.style.opacity = 0
      el.style.transform = 'scale(0.96)'
      return
    }
    if (tooltip.body) {
      const bodyLines = tooltip.body.map(b => b.lines).flat()
      const title = (tooltip.title || []).join(' — ')
      el.innerHTML = `<div><strong>${title}</strong></div><div>${bodyLines.join('<br/>')}</div>`
    }
    const { offsetLeft: positionX, offsetTop: positionY } = chart.canvas
    el.style.opacity = 1
    el.style.transform = 'scale(1)'
    el.style.left = positionX + tooltip.caretX + 12 + 'px'
    el.style.top = positionY + tooltip.caretY + 12 + 'px'
  }

  const chartOptions = { animation: { duration: 300 }, plugins: { tooltip: { enabled: false, external: externalTooltip } } }

  return (
    <div className="grid md:grid-cols-2 gap-4 fade-in">
      <div className="card">
        <h2 className="text-lg font-semibold mb-2">Market Summary</h2>
        {marketLoading && <div className="text-sm text-gray-500">Loading market summary...</div>}
        {marketError && <div className="text-sm bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-200 border border-red-200 dark:border-red-900/50 p-2 rounded">{String(marketErr?.message || 'Failed to load market data')}</div>}
        {!marketLoading && !marketError && (
          Array.isArray(market) || typeof market !== 'object' ? (
            <pre className="text-sm bg-gray-50 dark:bg-gray-800 dark:text-gray-100 border border-gray-100 dark:border-gray-800 p-2 rounded overflow-auto">{JSON.stringify(market, null, 2)}</pre>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {Object.entries(market).map(([name, info]) => renderMarketCard(name, info))}
            </div>
          )
        )}
      </div>
      <div className="card">
        <h2 className="text-lg font-semibold mb-2">Advice</h2>
        {adviceLoading && <div className="text-sm text-gray-500">Calculating advice...</div>}
        {adviceError && <div className="text-sm bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-200 border border-red-200 dark:border-red-900/50 p-2 rounded">{String(adviceErr?.message || 'Failed to load advice')}</div>}
        {advice ? (
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>Monthly Income: <b>{inr.format(advice.monthly_income_total)}</b></div>
            <div>Monthly Expense: <b>{inr.format(advice.monthly_expense_total)}</b></div>
            <div>Savings: <b>{inr.format(advice.monthly_savings)}</b></div>
            <div>Savings Rate: <b>{advice.savings_rate_percent}%</b></div>
            <div>Tax Bracket: <b>{advice.tax_bracket}</b></div>
            <div>Est. Annual Tax: <b>{inr.format(advice.estimated_annual_tax)}</b></div>
          </div>
        ) : (
          <div className="text-sm text-gray-500">Add some income and expenses to see advice.</div>
        )}
      </div>
      <div className="card">
        <h2 className="text-lg font-semibold mb-2">Suggested Allocation (Line)</h2>
        <Line data={lineData} options={chartOptions} />
      </div>
      <div className="card">
        <h2 className="text-lg font-semibold mb-2">Suggested Allocation (Doughnut)</h2>
        <Doughnut data={doughnutData} options={chartOptions} />
      </div>
      <div className="card md:col-span-2">
        <h2 className="text-lg font-semibold mb-2">Income vs Expenses vs Savings</h2>
        <Bar data={barData} options={chartOptions} />
      </div>
    </div>
  )
}
