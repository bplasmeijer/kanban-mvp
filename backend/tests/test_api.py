import os
import tempfile
import importlib
from fastapi.testclient import TestClient


def make_client():
    # isolate data file per test run
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    os.environ["DATA_FILE"] = tmp.name
    # Import after setting env (import local package)
    from app import main as app_module  # type: ignore
    importlib.reload(app_module)
    return TestClient(app_module.app)


def test_health():
    client = make_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_move_task():
    client = make_client()

    # Create a task
    r = client.post("/tasks", json={"title": "Test task"})
    assert r.status_code == 201, r.text
    task = r.json()
    assert task["column_id"] == "todo"
    assert task["order"] == 0

    # Create another task to check ordering
    r2 = client.post("/tasks", json={"title": "Second"})
    assert r2.status_code == 201
    task2 = r2.json()
    assert task2["order"] == 1

    # Move second task to top (order 0)
    r3 = client.patch(f"/tasks/{task2['id']}", json={"new_order": 0})
    assert r3.status_code == 200
    # Verify board ordering
    board = client.get("/board").json()
    todo = [t for t in board["tasks"] if t["column_id"] == "todo"]
    todo.sort(key=lambda x: x["order"])  # ensure sorted
    assert [t["id"] for t in todo] == [task2["id"], task["id"]]

    # Move first task to inprogress at top
    r4 = client.patch(
        f"/tasks/{task['id']}", json={"column_id": "inprogress", "new_order": 0})
    assert r4.status_code == 200
    board = client.get("/board").json()
    inprog = [t for t in board["tasks"] if t["column_id"] == "inprogress"]
    inprog.sort(key=lambda x: x["order"])  # ensure sorted
    assert len(
        inprog) == 1 and inprog[0]["id"] == task["id"] and inprog[0]["order"] == 0

    # Delete the task
    r5 = client.delete(f"/tasks/{task['id']}")
    assert r5.status_code == 204
