import { useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useSignup } from '../api/hooks'
import { api } from '../api/client'

export default function Signup() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { mutate, isPending, error } = useSignup()

  const onSubmit = (e) => {
    e.preventDefault()
    if (!email || !password) return
    mutate(
      { name, email, password },
      {
        onSuccess: (data) => {
          const token = data?.access_token || data?.token
          if (token) {
            try { localStorage.setItem('token', token) } catch {}
            api.defaults.headers.common.Authorization = `Bearer ${token}`
            window.dispatchEvent(new Event('auth-changed'))
            navigate('/')
          } else {
            navigate('/login')
          }
        },
      }
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 pt-2 sm:pt-4">
      <div className="max-w-md w-full card mt-0">
        <h2 className="text-2xl font-semibold mb-4">Create account</h2>
        <form onSubmit={onSubmit} className="space-y-4">
          <div>
            <label className="label">Name (optional)</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input"
            />
          </div>
          <div>
            <label className="label">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input"
              required
            />
          </div>
          <div>
            <label className="label">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input"
              required
            />
          </div>
          {error && (
            <div className="text-sm text-red-600 dark:text-red-400">
              {error.message || 'Signup failed'}
            </div>
          )}
          <button
            type="submit"
            disabled={isPending}
            className="btn w-full"
          >
            {isPending ? 'Creating…' : 'Create account'}
          </button>
        </form>
        <p className="mt-6 text-sm text-center">
          Already have an account?{' '}
          <NavLink to="/login" className="text-blue-600 dark:text-blue-400 hover:underline">
            Login
          </NavLink>
        </p>
      </div>
    </div>
  )
}
