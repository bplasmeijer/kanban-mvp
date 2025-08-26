# Kanban Board MVP

A minimal full-stack Kanban board MVP with:
- Backend: FastAPI (Python) with JSON file persistence
- Frontend: React (Vite) with drag-and-drop using @hello-pangea/dnd

## MVP description

- Entities:
  - Board: A single board named "Kanban" with three columns
  - Columns: Todo, In Progress, Done
  - Tasks: Cards with title and optional description
- Core flows:
  - View columns and tasks
  - Add a task to Todo
  - Drag and drop tasks to reorder within a column or move across columns
  - Edit/delete tasks (edit via API; basic UI focuses on add/move)
- Data model (backend):
  - Task: { id, title, description?, column_id, order }
  - Column: { id, name, position }
  - Board: { id, name }
- Persistence: JSON file `backend/data/data.json` for durability across restarts

## Prerequisites
- Python 3.10+
- Node.js 18+

## How to run

Backend:
1. Create and activate a virtual environment (optional but recommended)
2. Install dependencies
3. Start the API server

Frontend:
1. Install npm packages
2. Start the Vite dev server

The frontend will run on http://localhost:5173 and talk to the backend at http://localhost:8000 by default.

### Backend

- Env config: copy `backend/.env.example` to `backend/.env` (optional). Defaults are fine for local dev.
- Commands:

```bash
# from project root or backend/
cd backend
python3 -m venv .venv && source .venv/bin/activate  # optional
pip install -r requirements.txt
bash run.sh
```

API docs: http://localhost:8000/docs

Run tests:
```bash
cd backend
pytest -q
```

### Frontend

- Env config: copy `frontend/.env.example` to `frontend/.env` if you need to change the API URL.
- Commands:
```bash
cd frontend
npm install
npm run dev
```

Build and preview:
```bash
cd frontend
npm run build
npm run preview
```

## API overview

- GET /health -> { status: "ok" }
- GET /board -> board with columns and tasks grouped by column
- POST /tasks { title, description?, column_id? } -> create task (defaults to Todo)
- PATCH /tasks/{task_id} -> update title/description and/or move with { column_id, new_order }
- DELETE /tasks/{task_id}

## Notes
- This is an MVP: no authentication and no multi-user sync.
- JSON persistence is simple and not concurrent-safe; fine for local dev.
- For production, add a real database and auth.
