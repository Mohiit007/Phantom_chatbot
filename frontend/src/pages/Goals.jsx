import { useGoals, useCreateGoal } from '../api/hooks'
import { useState } from 'react'

export default function Goals() {
  const { data: goals } = useGoals()
  const createGoal = useCreateGoal()
  const [form, setForm] = useState({ event_name: '', today_cost: '', target_year: '' })

  return (
    <div className="grid gap-4 fade-in">
      <div className="card slide-up">
        <h2 className="text-lg font-semibold mb-3">Create Goal</h2>
        <form className="grid md:grid-cols-3 gap-3" onSubmit={(e)=>{e.preventDefault(); createGoal.mutate({ ...form, today_cost: Number(form.today_cost), target_year: Number(form.target_year) });}}>
          <div>
            <label className="label">Event Name</label>
            <input className="input" value={form.event_name} onChange={e=>setForm({...form, event_name:e.target.value})} required />
          </div>
          <div>
            <label className="label">Today Cost (₹)</label>
            <input className="input" type="number" value={form.today_cost} onChange={e=>setForm({...form, today_cost:e.target.value})} required />
          </div>
          <div>
            <label className="label">Target Year</label>
            <input className="input" type="number" value={form.target_year} onChange={e=>setForm({...form, target_year:e.target.value})} required />
          </div>
          <div className="md:col-span-3">
            <button className="btn" disabled={createGoal.isPending}>Create</button>
          </div>
        </form>
      </div>
      <div className="card slide-up">
        <h2 className="text-lg font-semibold mb-3">Goals</h2>
        <div className="overflow-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-50 dark:bg-gray-900"><tr className="text-left"><th className="p-2">Event</th><th className="p-2">Year</th><th className="p-2">Today Cost</th><th className="p-2">Future Cost</th><th className="p-2">Monthly Saving</th></tr></thead>
            <tbody>
              {goals?.map(g=> (
                <tr key={g.id} className="border-t border-gray-100 dark:border-gray-800">
                  <td className="p-2">{g.event_name}</td>
                  <td className="p-2">{g.target_year}</td>
                  <td className="p-2">₹{g.today_cost}</td>
                  <td className="p-2">₹{g.calculation?.future_cost ?? '-'}</td>
                  <td className="p-2">₹{g.calculation?.monthly_saving ?? '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
