import { useState, useMemo } from 'react'
import { useExpenses, useAddExpense, useDeleteExpense } from '../api/hooks'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default function Expenses() {
  const { data: expenses } = useExpenses()
  const add = useAddExpense()
  const del = useDeleteExpense()
  const [form, setForm] = useState({ date: '', amount: '', category: '', note: '' })

  const categoryData = useMemo(() => {
    const m = new Map()
    for (const e of expenses || []) {
      const key = (e.category || 'Other').toString()
      m.set(key, (m.get(key) || 0) + Number(e.amount || 0))
    }
    const labels = [...m.keys()]
    const values = labels.map(l => m.get(l))
    return {
      labels,
      datasets: [{ label: 'Expenses by Category (₹)', data: values, backgroundColor: '#ef4444' }]
    }
  }, [expenses])

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
    <div className="grid gap-4 fade-in">
      <div className="card slide-up">
        <h2 className="text-lg font-semibold mb-3">Add Expense</h2>
        <form className="grid md:grid-cols-4 gap-3" onSubmit={(e)=>{e.preventDefault(); add.mutate({ ...form, amount: Number(form.amount) });}}>
          <input className="input" placeholder="Date (YYYY-MM-DD)" value={form.date} onChange={e=>setForm({...form, date:e.target.value})} />
          <input className="input" type="number" placeholder="Amount" value={form.amount} onChange={e=>setForm({...form, amount:e.target.value})} required />
          <input className="input" placeholder="Category" value={form.category} onChange={e=>setForm({...form, category:e.target.value})} required />
          <input className="input" placeholder="Note" value={form.note} onChange={e=>setForm({...form, note:e.target.value})} />
          <div className="md:col-span-4"><button className="btn" disabled={add.isPending}>Add</button></div>
        </form>
      </div>
      <div className="card slide-up">
        <h2 className="text-lg font-semibold mb-3">Expenses</h2>
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 dark:bg-gray-900"><tr className="text-left"><th className="p-2">Date</th><th className="p-2">Amount</th><th className="p-2">Category</th><th className="p-2">Note</th><th className="p-2">Actions</th></tr></thead>
          <tbody>
            {expenses?.map(e => (
              <tr key={e.id} className="border-t border-gray-100 dark:border-gray-800">
                <td className="p-2">{e.date}</td>
                <td className="p-2">₹{e.amount}</td>
                <td className="p-2">{e.category}</td>
                <td className="p-2">{e.note}</td>
                <td className="p-2"><button className="text-red-600" onClick={()=>del.mutate(e.id)}>Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="card slide-up">
        <h2 className="text-lg font-semibold mb-3">Category-wise Spend</h2>
        <Bar data={categoryData} options={chartOptions} />
      </div>
    </div>
  )
}
