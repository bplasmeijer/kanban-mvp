import React, { useEffect, useRef, useState } from 'react'
import { Draggable } from '@hello-pangea/dnd'
import { updateTask } from '../api'

export default function TaskCard({ task, index }) {
    const [editing, setEditing] = useState(false)
    const [value, setValue] = useState(task.title)
    const [saving, setSaving] = useState(false)
    const inputRef = useRef(null)

    useEffect(() => {
        if (editing && inputRef.current) {
            inputRef.current.focus()
            inputRef.current.select()
        }
    }, [editing])

    useEffect(() => {
        // keep in sync if parent changes title (e.g., after refetch)
        if (!editing) setValue(task.title)
    }, [task.title, editing])

    const startEdit = (e) => {
        e.stopPropagation()
        setValue(task.title)
        setEditing(true)
    }

    const cancelEdit = () => {
        setEditing(false)
        setValue(task.title)
    }

    const saveEdit = async () => {
        const next = value.trim()
        if (!next || next === task.title) {
            setEditing(false)
            setValue(task.title)
            return
        }
        try {
            setSaving(true)
            await updateTask(task.id, { title: next })
            // Optimistically reflect the change locally
            task.title = next
            setEditing(false)
        } catch (err) {
            console.error('Failed to update task title', err)
            // revert value to current title
            setValue(task.title)
            setEditing(false)
        } finally {
            setSaving(false)
        }
    }

    const onKeyDown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            void saveEdit()
        } else if (e.key === 'Escape') {
            e.preventDefault()
            cancelEdit()
        }
    }

    return (
        <Draggable draggableId={task.id} index={index}>
            {(prov) => (
                <div
                    className="task"
                    ref={prov.innerRef}
                    {...prov.draggableProps}
                    // Disable drag handle while editing to avoid interference
                    {...(editing ? {} : prov.dragHandleProps)}
                    onDoubleClick={startEdit}
                >
                    {editing ? (
                        <input
                            ref={inputRef}
                            className="task-title"
                            value={value}
                            onChange={(e) => setValue(e.target.value)}
                            onKeyDown={onKeyDown}
                            onBlur={cancelEdit}
                            disabled={saving}
                        />
                    ) : (
                        <div className="task-title">{value}</div>
                    )}
                    {task.description && !editing && <div className="task-desc">{task.description}</div>}
                </div>
            )}
        </Draggable>
    )
}
