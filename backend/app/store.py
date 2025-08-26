import json
import os
from json import JSONDecodeError
from typing import Dict, Any
from threading import RLock

from .models import Board, Column, Task, BoardView

_DATA_FILE = os.environ.get("DATA_FILE", os.path.join(
    os.path.dirname(__file__), "..", "data", "data.json"))
_LOCK = RLock()


def _default_data() -> Dict[str, Any]:
    return {
        "board": {"id": "board-1", "name": "Kanban"},
        "columns": [
            {"id": "todo", "name": "Todo", "position": 0},
            {"id": "inprogress", "name": "In Progress", "position": 1},
            {"id": "done", "name": "Done", "position": 2},
        ],
        "tasks": [],
    }


def _load() -> Dict[str, Any]:
    with _LOCK:
        os.makedirs(os.path.dirname(_DATA_FILE), exist_ok=True)
        needs_init = not os.path.exists(
            _DATA_FILE) or os.path.getsize(_DATA_FILE) == 0
        if needs_init:
            with open(_DATA_FILE, "w") as f:
                json.dump(_default_data(), f)
        try:
            with open(_DATA_FILE, "r") as f:
                return json.load(f)
        except JSONDecodeError:
            # Reinitialize corrupt file
            with open(_DATA_FILE, "w") as f:
                json.dump(_default_data(), f)
            return _default_data()


def _save(data: Dict[str, Any]) -> None:
    with _LOCK:
        tmp_file = _DATA_FILE + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(data, f)
        os.replace(tmp_file, _DATA_FILE)


def get_board_view() -> BoardView:
    data = _load()
    return BoardView(
        board=Board(**data["board"]),
        columns=[Column(**c) for c in sorted(data["columns"],
                                             key=lambda c: c["position"])],
        tasks=[Task(**t) for t in data["tasks"]],
    )


def _next_order_for_column(data: Dict[str, Any], column_id: str) -> int:
    tasks = [t for t in data["tasks"] if t["column_id"] == column_id]
    if not tasks:
        return 0
    return max(t["order"] for t in tasks) + 1


def create_task(title: str, description: str | None, column_id: str | None) -> Task:
    data = _load()
    column_id = column_id or "todo"
    # ensure column exists
    if not any(c["id"] == column_id for c in data["columns"]):
        raise ValueError("Column does not exist")
    new_task = {
        "id": f"task-{len(data['tasks'])+1}",
        "title": title,
        "description": description,
        "column_id": column_id,
        "order": _next_order_for_column(data, column_id),
    }
    data["tasks"].append(new_task)
    _save(data)
    return Task(**new_task)


def find_task_index(data: Dict[str, Any], task_id: str) -> int:
    for i, t in enumerate(data["tasks"]):
        if t["id"] == task_id:
            return i
    raise KeyError("Task not found")


def _reindex_column_tasks(tasks: list[dict], column_id: str) -> None:
    col_tasks = [t for t in tasks if t["column_id"] == column_id]
    col_tasks.sort(key=lambda t: t["order"])  # ensure order
    for idx, t in enumerate(col_tasks):
        t["order"] = idx


def update_task(task_id: str, *, title: str | None = None, description: str | None = None,
                column_id: str | None = None, new_order: int | None = None) -> Task:
    data = _load()
    i = find_task_index(data, task_id)
    t = data["tasks"][i]

    if title is not None:
        t["title"] = title
    if description is not None:
        t["description"] = description

    if column_id is not None and column_id != t["column_id"]:
        # moving across columns
        if not any(c["id"] == column_id for c in data["columns"]):
            raise ValueError("Column does not exist")
        old_col = t["column_id"]
        t["column_id"] = column_id
        t["order"] = _next_order_for_column(data, column_id)
        _reindex_column_tasks(data["tasks"], old_col)

    if new_order is not None:
        # reorder within current column
        col_id = t["column_id"]
        col_tasks = [x for x in data["tasks"]
                     if x["column_id"] == col_id and x["id"] != t["id"]]
        # clamp
        new_order = max(0, min(new_order, len(col_tasks)))
        # rebuild orders placing t at new_order
        col_tasks.sort(key=lambda x: x["order"])
        rebuilt: list[dict] = []
        for idx in range(len(col_tasks) + 1):
            if idx == new_order:
                rebuilt.append(t)
            if idx < len(col_tasks):
                rebuilt.append(col_tasks[idx])
        # assign orders
        for idx, x in enumerate(rebuilt):
            x["order"] = idx

    _save(data)
    return Task(**t)


def delete_task(task_id: str) -> None:
    data = _load()
    i = find_task_index(data, task_id)
    col_id = data["tasks"][i]["column_id"]
    data["tasks"].pop(i)
    _reindex_column_tasks(data["tasks"], col_id)
    _save(data)
