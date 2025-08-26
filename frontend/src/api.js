const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function fetchBoard() {
  const r = await fetch(`${API_BASE}/board`)
  if (!r.ok) throw new Error('Failed to fetch board')
  return r.json()
}

export async function createTask(title, description) {
  const r = await fetch(`${API_BASE}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description })
  })
  if (!r.ok) throw new Error('Failed to create task')
  return r.json()
}

export async function updateTask(taskId, body) {
  const r = await fetch(`${API_BASE}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!r.ok) throw new Error('Failed to update task')
  return r.json()
}

export async function deleteTask(taskId) {
  const r = await fetch(`${API_BASE}/tasks/${taskId}`, { method: 'DELETE' })
  if (!r.ok) throw new Error('Failed to delete task')
}
