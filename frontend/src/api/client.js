import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({
  baseURL,
})

// Initialize Authorization header from saved token
try {
  const token = localStorage.getItem('token')
  if (token) api.defaults.headers.common.Authorization = `Bearer ${token}`
} catch {}

// Listen to auth changes
if (typeof window !== 'undefined') {
  window.addEventListener('auth-changed', () => {
    try {
      const token = localStorage.getItem('token')
      if (token) api.defaults.headers.common.Authorization = `Bearer ${token}`
      else delete api.defaults.headers.common.Authorization
    } catch {}
  })
}

export const get = (url, config) => api.get(url, config).then(r => r.data)
export const post = (url, data, config) => api.post(url, data, config).then(r => r.data)
export const del = (url, config) => api.delete(url, config).then(r => r.data)
