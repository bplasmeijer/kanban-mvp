import React from 'react'
import { Droppable } from '@hello-pangea/dnd'
import TaskCard from './TaskCard'

export default function Column({ column, tasks }) {
    return (
        <div className="column">
            <h3>{column.name}</h3>
            <Droppable droppableId={column.id}>
                {(provided) => (
                    <div className="task-list" ref={provided.innerRef} {...provided.droppableProps}>
                        {tasks
                            .slice()
                            .sort((a, b) => a.order - b.order)
                            .map((t, idx) => (
                                <TaskCard key={t.id} task={t} index={idx} />
                            ))}
                        {provided.placeholder}
                    </div>
                )}
            </Droppable>
        </div>
    )
}
