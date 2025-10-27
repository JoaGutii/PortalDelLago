import { useEffect, useState } from 'react'
import { login } from './auth'
import { api } from './api'
import useWebSocket from './hooks/useWebSocket'

type Incident = { id:number; title:string; description:string; status:string; room:string }
type Task = { id:number; title:string; detail:string; priority:string; done:boolean }
type LostFound = { id:number; description:string; location:string; state:string }

export default function App() {
  const [user, setUser] = useState<any>(null)
  const [form, setForm] = useState({ username:'', password:'' })
  const wsMsgs = useWebSocket((import.meta.env.VITE_API_BASE || 'http://localhost:8000').replace(/^http/, 'ws') + '/ws/notifications/') + location.host.replace(':5173', ':8000') + '/ws/notifications/')

  async function doLogin(e:any) {
    e.preventDefault()
    try {
      const u = await login(form.username, form.password)
      setUser(u)
      loadAll()
    } catch { alert('Error de login') }
  }

  async function loadAll() {
    const [inc, tasks, lf] = await Promise.all([
      api.get('/api/incidents/'),
      api.get('/api/tasks/'),
      api.get('/api/lostfound/'),
    ])
    setIncidents(inc.data)
    setTasks(tasks.data)
    setLostFound(lf.data)
  }

  // data
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [lostFound, setLostFound] = useState<LostFound[]>([])

  useEffect(() => {
    // reload on websocket events
    if (wsMsgs.length) loadAll()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [wsMsgs])

  if (!user) {
    return (
      <div className="min-h-screen grid place-items-center">
        <form onSubmit={doLogin} className="card w-full max-w-sm space-y-4">
          <h1 className="text-2xl font-bold">Portal del Lago</h1>
          <input className="w-full border rounded px-3 py-2" placeholder="Usuario" value={form.username} onChange={e=>setForm(v=>({...v, username:e.target.value}))} />
          <input type="password" className="w-full border rounded px-3 py-2" placeholder="Contraseña" value={form.password} onChange={e=>setForm(v=>({...v, password:e.target.value}))} />
          <button className="btn border-gray-300">Ingresar</button>
          <p className="text-sm text-gray-500">Usuarios demo: superadmin / recepcion / mucama / mantenimiento — Contraseña: probar la que configures</p>
        </form>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Bienvenido, {user.username}</h1>
        <button className="btn" onClick={()=>{localStorage.clear(); location.reload()}}>Salir</button>
      </header>

      <section className="grid md:grid-cols-3 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-3">Incidentes</h2>
          <CreateIncident onCreated={loadAll}/>
          <ul className="mt-3 space-y-2">
            {incidents.map(i => (
              <li key={i.id} className="border rounded p-2">
                <div className="font-medium">{i.title} <span className="text-xs bg-gray-100 rounded px-1">{i.status}</span></div>
                <div className="text-sm text-gray-600">{i.description}</div>
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h2 className="font-semibold mb-3">Tareas</h2>
          <CreateTask onCreated={loadAll}/>
          <ul className="mt-3 space-y-2">
            {tasks.map(t => (
              <li key={t.id} className="border rounded p-2 flex items-center justify-between">
                <div>
                  <div className="font-medium">{t.title}</div>
                  <div className="text-sm text-gray-600">{t.detail}</div>
                </div>
                <span className="text-xs bg-gray-100 rounded px-2">{t.priority}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h2 className="font-semibold mb-3">Objetos Perdidos</h2>
          <CreateLostFound onCreated={loadAll}/>
          <ul className="mt-3 space-y-2">
            {lostFound.map(l => (
              <li key={l.id} className="border rounded p-2">
                <div className="font-medium">{l.description}</div>
                <div className="text-sm text-gray-600">{l.location} — {l.state}</div>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="card">
        <h2 className="font-semibold mb-3">Eventos (Realtime)</h2>
        <div className="text-sm max-h-48 overflow-auto space-y-1">
          {wsMsgs.map((m, idx) => <pre key={idx} className="bg-gray-50 p-2 rounded">{JSON.stringify(m)}</pre>)}
        </div>
      </section>
    </div>
  )
}

function CreateIncident({ onCreated }: { onCreated: ()=>void }) {
  const [f, setF] = useState({ title:'', description:'', room:'' })
  async function submit(e:any) {
    e.preventDefault()
    await api.post('/api/incidents/', f)
    setF({ title:'', description:'', room:'' })
    onCreated()
  }
  return (
    <form onSubmit={submit} className="space-y-2">
      <input className="w-full border rounded px-3 py-2" placeholder="Título" value={f.title} onChange={e=>setF(v=>({...v, title:e.target.value}))} />
      <textarea className="w-full border rounded px-3 py-2" placeholder="Descripción" value={f.description} onChange={e=>setF(v=>({...v, description:e.target.value}))} />
      <input className="w-full border rounded px-3 py-2" placeholder="Habitación" value={f.room} onChange={e=>setF(v=>({...v, room:e.target.value}))} />
      <button className="btn border-gray-300">Crear</button>
    </form>
  )
}

function CreateTask({ onCreated }: { onCreated: ()=>void }) {
  const [f, setF] = useState({ title:'', detail:'', priority:'MEDIUM' })
  async function submit(e:any) {
    e.preventDefault()
    await api.post('/api/tasks/', f)
    setF({ title:'', detail:'', priority:'MEDIUM' })
    onCreated()
  }
  return (
    <form onSubmit={submit} className="space-y-2">
      <input className="w-full border rounded px-3 py-2" placeholder="Título" value={f.title} onChange={e=>setF(v=>({...v, title:e.target.value}))} />
      <textarea className="w-full border rounded px-3 py-2" placeholder="Detalle" value={f.detail} onChange={e=>setF(v=>({...v, detail:e.target.value}))} />
      <select className="w-full border rounded px-3 py-2" value={f.priority} onChange={e=>setF(v=>({...v, priority:e.target.value}))}>
        <option value="HIGH">Alta</option>
        <option value="MEDIUM">Media</option>
        <option value="LOW">Baja</option>
      </select>
      <button className="btn border-gray-300">Crear</button>
    </form>
  )
}

function CreateLostFound({ onCreated }: { onCreated: ()=>void }) {
  const [f, setF] = useState({ description:'', location:'', date_found: new Date().toISOString().slice(0,10) })
  async function submit(e:any) {
    e.preventDefault()
    await api.post('/api/lostfound/', f)
    setF({ description:'', location:'', date_found:new Date().toISOString().slice(0,10) })
    onCreated()
  }
  return (
    <form onSubmit={submit} className="space-y-2">
      <input className="w-full border rounded px-3 py-2" placeholder="Descripción" value={f.description} onChange={e=>setF(v=>({...v, description:e.target.value}))} />
      <input className="w-full border rounded px-3 py-2" placeholder="Ubicación" value={f.location} onChange={e=>setF(v=>({...v, location:e.target.value}))} />
      <input type="date" className="w-full border rounded px-3 py-2" value={f.date_found} onChange={e=>setF(v=>({...v, date_found:e.target.value}))} />
      <button className="btn border-gray-300">Crear</button>
    </form>
  )
}
