import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { get, post, del } from './client'

export const useMarketSummary = () => useQuery({ queryKey: ['market'], queryFn: () => get('/market/summary'), refetchInterval: 60_000 })
export const useAdvice = () => useQuery({ queryKey: ['advice'], queryFn: () => get('/advice'), refetchInterval: 30_000 })

export const useGoals = () => useQuery({ queryKey: ['goals'], queryFn: () => get('/goals/') })
export const useCreateGoal = () => {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (data) => post('/goals/', data), onSuccess: () => qc.invalidateQueries({ queryKey: ['goals'] }) })
}
export const useDeleteGoal = () => {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (id) => del(`/goals/${id}`), onSuccess: () => qc.invalidateQueries({ queryKey: ['goals'] }) })
}

export const useExpenses = () => useQuery({ queryKey: ['expenses'], queryFn: () => get('/expenses') })
export const useAddExpense = () => {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (data) => post('/expenses', data), onSuccess: () => qc.invalidateQueries({ queryKey: ['expenses','advice'] }) })
}
export const useDeleteExpense = () => {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (id) => del(`/expenses/${id}`), onSuccess: () => qc.invalidateQueries({ queryKey: ['expenses','advice'] }) })
}

export const useIncome = () => useQuery({ queryKey: ['income'], queryFn: () => get('/income') })
export const useAddIncome = () => {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (data) => post('/income', data), onSuccess: () => qc.invalidateQueries({ queryKey: ['income','advice'] }) })
}
export const useDeleteIncome = () => {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (id) => del(`/income/${id}`), onSuccess: () => qc.invalidateQueries({ queryKey: ['income','advice'] }) })
}

export const usePlanner = () => {
  return useMutation({ mutationFn: (data) => post('/planner/', data) })
}
export const useParseAndPlan = () => {
  return useMutation({ mutationFn: (data) => post('/planner/parse-and-plan', data) })
}
export const useNlpParse = () => {
  return useMutation({ mutationFn: (data) => post('/nlp/parse', data) })
}
export const useAgentChat = () => {
  return useMutation({ mutationFn: (data) => post('/agent/chat', data) })
}

// Auth
export const useLogin = () => {
  return useMutation({ mutationFn: (data) => post('/auth/login', data) })
}
export const useSignup = () => {
  return useMutation({ mutationFn: (data) => post('/auth/register', data) })
}
