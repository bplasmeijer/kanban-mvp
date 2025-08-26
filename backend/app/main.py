from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import CreateTaskRequest, UpdateTaskRequest
from . import store

app = FastAPI(title="Kanban MVP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/board")
def get_board():
    return store.get_board_view()


@app.post("/tasks", status_code=201)
def create_task(req: CreateTaskRequest):
    try:
        t = store.create_task(req.title, req.description, req.column_id)
        return t
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, req: UpdateTaskRequest):
    try:
        t = store.update_task(
            task_id,
            title=req.title,
            description=req.description,
            column_id=req.column_id,
            new_order=req.new_order,
        )
        return t
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    try:
        store.delete_task(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
