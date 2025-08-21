import { useState } from 'react'
import { usePlanner, useParseAndPlan } from '../api/hooks'

export default function Planner() {
  const [planForm, setPlanForm] = useState({ event_name: '', today_cost: '', target_year: '', inflation_override_pct: '' })
  const [text, setText] = useState('Plan wedding in Dec 2026 for ₹800000')
  const plan = usePlanner()
  const parsePlan = useParseAndPlan()

  return (
    <div className="grid md:grid-cols-2 gap-4 fade-in">
      <div className="card slide-up">
        <h2 className="text-lg font-semibold mb-2">Plan Event</h2>
        <form className="grid gap-3" onSubmit={(e)=>{e.preventDefault(); plan.mutate({ ...planForm, today_cost: Number(planForm.today_cost), target_year: Number(planForm.target_year), inflation_override_pct: planForm.inflation_override_pct? Number(planForm.inflation_override_pct): undefined })}}>
          <input className="input" placeholder="Event Name" value={planForm.event_name} onChange={e=>setPlanForm({...planForm, event_name:e.target.value})} required />
          <input className="input" type="number" placeholder="Today Cost (₹)" value={planForm.today_cost} onChange={e=>setPlanForm({...planForm, today_cost:e.target.value})} required />
          <input className="input" type="number" placeholder="Target Year" value={planForm.target_year} onChange={e=>setPlanForm({...planForm, target_year:e.target.value})} required />
          <input className="input" type="number" placeholder="Inflation Override % (optional)" value={planForm.inflation_override_pct} onChange={e=>setPlanForm({...planForm, inflation_override_pct:e.target.value})} />
          <button className="btn" disabled={plan.isPending}>Create Plan</button>
        </form>
        {plan.data && <PlanCard title="Plan Result" p={plan.data} />}
      </div>
      <div className="card slide-up">
        <h2 className="text-lg font-semibold mb-2">Parse & Plan</h2>
        <form className="grid gap-3" onSubmit={(e)=>{e.preventDefault(); parsePlan.mutate({ text, inflation_override_pct: undefined })}}>
          <textarea className="input h-28" value={text} onChange={e=>setText(e.target.value)} />
          <button className="btn" disabled={parsePlan.isPending}>Parse & Plan</button>
        </form>
        {parsePlan.data && <PlanCard title="Parsed Plan" p={parsePlan.data} />}
      </div>
    </div>
  )
}

function PlanCard({ title, p }) {
  return (
    <div className="mt-4 border rounded-md p-3 text-sm bg-gray-50 dark:bg-gray-900 dark:text-gray-100 border-gray-200 dark:border-gray-800 slide-up">
      <div className="font-medium mb-1">{title}</div>
      <div>Event: <b>{p.event_name}</b></div>
      <div>Year: <b>{p.target_year}</b></div>
      <div>Today: <b>₹{p.today_cost}</b></div>
      <div>Inflation Used: <b>{p.inflation_percent_used}%</b></div>
      <div>Years: <b>{p.years_to_goal}</b></div>
      <div>Future Cost: <b>₹{p.future_cost}</b></div>
      <div>Monthly Saving: <b>₹{p.monthly_saving_needed}</b></div>
      {p.recommendation && <div>Note: {p.recommendation}</div>}
    </div>
  )
}
