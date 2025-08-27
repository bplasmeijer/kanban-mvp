import React, { Fragment } from 'react'

export default function Header({ newTitle, setNewTitle, onAddTask, error }) {
    return (
        <Fragment>
            <header>
                <h1>Kanban Board</h1>
                <form onSubmit={onAddTask} className="add-form">
                    <input value={newTitle} onChange={e => setNewTitle(e.target.value)} placeholder="Add task to Todo" />
                    <button>Add</button>
                </form>
                {error && <div className="error">{error}</div>}
            </header>
        </Fragment>
    )
}
