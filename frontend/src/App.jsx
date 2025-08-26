import React, { useEffect, useMemo, useState } from 'react'
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd'
import { fetchBoard, createTask, updateTask } from './api'

const COLUMN_ORDER = ['todo', 'inprogress', 'done']

function Column({ column, tasks }) {
  return (
    <div className="column">
      <h3>{column.name}</h3>
      <Droppable droppableId={column.id}>
        {(provided) => (
          <div className="task-list" ref={provided.innerRef} {...provided.droppableProps}>
            {tasks.sort((a, b) => a.order - b.order).map((t, idx) => (
              <Draggable draggableId={t.id} index={idx} key={t.id}>
                {(prov) => (
                  <div className="task" ref={prov.innerRef} {...prov.draggableProps} {...prov.dragHandleProps}>
                    <div className="task-title">{t.title}</div>
                    {t.description && <div className="task-desc">{t.description}</div>}
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  )
}

export default function App() {
  const [board, setBoard] = useState(null)
  const [newTitle, setNewTitle] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    fetchBoard().then(setBoard).catch(e => setError(e.message))
  }, [])

  const columnsById = useMemo(() => {
    if (!board) return {}
    const map = {}
    for (const c of board.columns) map[c.id] = c
    return map
  }, [board])

  async function onDragEnd(result) {
    if (!result.destination || !board) return
    const { source, destination, draggableId } = result

    const srcColId = source.droppableId
    const destColId = destination.droppableId
    const newOrder = destination.index

    // Optimistic UI update
    setBoard(prev => {
      const copy = { ...prev, tasks: prev.tasks.map(t => ({ ...t })) }
      const t = copy.tasks.find(t => t.id === draggableId)
      if (!t) return prev

      // Remove from source ordering
      const srcTasks = copy.tasks.filter(t => t.column_id === srcColId && t.id !== draggableId)
      srcTasks.sort((a, b) => a.order - b.order)
      srcTasks.forEach((t, i) => t.order = i)

      // Insert into dest ordering
      t.column_id = destColId
      const destTasks = copy.tasks.filter(x => x.column_id === destColId && x.id !== draggableId)
      destTasks.sort((a, b) => a.order - b.order)
      destTasks.splice(newOrder, 0, t)
      destTasks.forEach((x, i) => x.order = i)
      return copy
    })

    try {
      await updateTask(draggableId, { column_id: destColId, new_order: newOrder })
    } catch (e) {
      setError(String(e))
      // Refetch to correct
      fetchBoard().then(setBoard)
    }
  }

  async function onAddTask(e) {
    e.preventDefault()
    if (!newTitle.trim()) return
    try {
      const t = await createTask(newTitle.trim())
      setBoard(prev => ({ ...prev, tasks: [...prev.tasks, t] }))
      setNewTitle('')
    } catch (e) {
      setError(String(e))
    }
  }

  if (!board) return <div className="container">Loading… {error && <span className="error">{error}</span>}</div>

  const tasksByColumn = (colId) => board.tasks.filter(t => t.column_id === colId)

  return (
    <div className="container">
      <header>
        <h1>Kanban Board</h1>
        <form onSubmit={onAddTask} className="add-form">
          <input value={newTitle} onChange={e => setNewTitle(e.target.value)} placeholder="Add task to Todo" />
          <button>Add</button>
        </form>
        {error && <div className="error">{error}</div>}
      </header>
      <DragDropContext onDragEnd={onDragEnd}>
        <div className="board">
          {board.columns.sort((a, b) => a.position - b.position).map(col => (
            <Column key={col.id} column={col} tasks={tasksByColumn(col.id)} />
          ))}
        </div>
      </DragDropContext>
    </div>
  )
}
