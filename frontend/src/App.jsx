import { Routes, Route, NavLink } from 'react-router-dom'
import { LineChart, Wallet, Target, Bot, Moon, Sun } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Goals from './pages/Goals'
import Planner from './pages/Planner'
import Expenses from './pages/Expenses'
import Income from './pages/Income'
import AgentChat from './pages/AgentChat'
import { useEffect, useState, useRef } from 'react'
import Login from './pages/Login'
import Signup from './pages/Signup'

const NavItem = ({ to, icon: Icon, label }) => (
  <NavLink to={to} className={({ isActive }) => `px-3 py-2 rounded-md transition-colors ${isActive ? 'bg-blue-50 text-blue-700 dark:bg-red-900/40 dark:text-red-300' : 'hover:bg-blue-50 dark:hover:bg-red-900/30'}`}>
    <span className="inline-flex items-center gap-2"><Icon size={18} /> {label}</span>
  </NavLink>
)

function ThemeToggle() {
  const [theme, setTheme] = useState(() => {
    try { return localStorage.getItem('theme') || 'light' } catch { return 'light' }
  })
  useEffect(() => {
    const isHorror = theme === 'horror'
    document.documentElement.classList.toggle('dark', isHorror)
    try { localStorage.setItem('theme', theme) } catch {}
  }, [theme])

  const handleToggle = () => {
    const root = document.documentElement
    // Temporarily disable transitions/animations to avoid flicker
    root.classList.add('no-transitions')
    setTheme(t => t === 'horror' ? 'light' : 'horror')
    // Remove the class on the next frame after DOM updates
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        root.classList.remove('no-transitions')
      })
    })
  }

  return (
    <button className="btn-ghost" onClick={handleToggle} title="Toggle theme">
      {theme === 'horror' ? (<><Sun size={16} /> Light</>) : (<><Moon size={16} className="accent-blood" /> Horror</>)}
    </button>
  )
}

export default function App() {
  const [authed, setAuthed] = useState(() => {
    try { return !!localStorage.getItem('token') } catch { return false }
  })

  useEffect(() => {
    const handler = () => {
      try { setAuthed(!!localStorage.getItem('token')) } catch { setAuthed(false) }
    }
    window.addEventListener('auth-changed', handler)
    return () => window.removeEventListener('auth-changed', handler)
  }, [])

  const [reduced, setReduced] = useState(false)
  useEffect(() => {
    const mqReduced = window.matchMedia('(prefers-reduced-motion: reduce)')
    const mqCoarse = window.matchMedia('(pointer: coarse)')
    const update = () => setReduced(mqReduced.matches || mqCoarse.matches)
    update()
    mqReduced.addEventListener?.('change', update)
    mqCoarse.addEventListener?.('change', update)
    return () => {
      mqReduced.removeEventListener?.('change', update)
      mqCoarse.removeEventListener?.('change', update)
    }
  }, [])

  // Fade-in on load and when switching to dark
  const ghostsRef = useRef(null)
  useEffect(() => {
    const root = document.documentElement
    const apply = () => {
      if (!ghostsRef.current) return
      if (root.classList.contains('dark')) ghostsRef.current.classList.add('ghosts-ready')
      else ghostsRef.current.classList.remove('ghosts-ready')
    }
    // Initial pass after mount
    requestAnimationFrame(apply)
    // Observe theme class changes
    const obs = new MutationObserver(apply)
    obs.observe(root, { attributes: true, attributeFilter: ['class'] })
    return () => obs.disconnect()
  }, [])

  const handleLogout = () => {
    try { localStorage.removeItem('token') } catch {}
    window.dispatchEvent(new Event('auth-changed'))
  }

  return (
    <div className="min-h-screen">
      <div ref={ghostsRef} className={`ghosts-container ${reduced ? 'ghosts--reduced' : ''}`} aria-hidden="true">
        <div className="stars stars-1" />
        <div className="stars stars-2" />
        <div className="stars stars-3" />
        <div className="stars stars-4" />
        <img id="ghost1" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost2" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost3" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost4" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost5" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost6" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost7" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost8" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost9" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost10" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost11" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost12" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost13" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost14" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost15" className="ghost" src="/ghost.png" alt="" />
        <img id="ghost16" className="ghost" src="/ghost.png" alt="" />
      </div>
      <header className="sticky top-0 z-50 bg-white dark:bg-black border-b border-gray-100 dark:border-red-900/40">
        <div className="max-w-6xl mx-auto flex items-center justify-between p-2">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-semibold brand-title">
              <span className="brand-phantom">Phantom</span>
              <span className="brand-finance">Finance</span>
            </h1>
          </div>
          <nav className="flex items-center gap-2 text-sm">
            <NavItem to="/" icon={LineChart} label="Dashboard" />
            <NavItem to="/goals" icon={Target} label="Goals" />
            <NavItem to="/planner" icon={Target} label="Planner" />
            <NavItem to="/expenses" icon={Wallet} label="Expenses" />
            <NavItem to="/income" icon={Wallet} label="Income" />
            <NavItem to="/agent" icon={Bot} label="Agent" />
            {authed ? (
              <button onClick={handleLogout} className="px-3 py-2 rounded-md hover:bg-blue-50 dark:hover:bg-red-900/30">Logout</button>
            ) : (
              <>
                <NavLink to="/login" className="px-3 py-2 rounded-md hover:bg-blue-50 dark:hover:bg-red-900/30">Login</NavLink>
                <NavLink to="/signup" className="px-3 py-2 rounded-md hover:bg-blue-50 dark:hover:bg-red-900/30">Signup</NavLink>
              </>
            )}
            <ThemeToggle />
          </nav>
        </div>
      </header>
      <main className="relative max-w-6xl mx-auto p-4 pt-4 sm:pt-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/goals" element={<Goals />} />
          <Route path="/planner" element={<Planner />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/income" element={<Income />} />
          <Route path="/agent" element={<AgentChat />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </main>
    </div>
  )
}
