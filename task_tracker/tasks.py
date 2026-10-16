"""Task model and JSON-backed storage."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

PRIORITIES = ("low", "medium", "high")
DEFAULT_PRIORITY = "medium"


class TaskNotFoundError(Exception):
    """Raised when no task exists with the requested id."""

    def __init__(self, task_id: int) -> None:
        super().__init__(f"No task with id {task_id}")
        self.task_id = task_id


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    priority: str = DEFAULT_PRIORITY

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            done=bool(data.get("done", False)),
            priority=str(data.get("priority", DEFAULT_PRIORITY)),
        )


class TaskStore:
    """Loads and saves tasks in a JSON file."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as file:
            data = json.load(file)
        return [Task.from_dict(item) for item in data]

    def save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=2)
            file.write("\n")

    def add(self, title: str, priority: str = DEFAULT_PRIORITY) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")
        priority = _validate_priority(priority)
        tasks = self.load()
        next_id = max((task.id for task in tasks), default=0) + 1
        task = Task(id=next_id, title=title, priority=priority)
        tasks.append(task)
        self.save(tasks)
        return task

    def complete(self, task_id: int) -> Task:
        tasks = self.load()
        task = _find(tasks, task_id)
        task.done = True
        self.save(tasks)
        return task

    def delete(self, task_id: int) -> Task:
        tasks = self.load()
        task = _find(tasks, task_id)
        tasks.remove(task)
        self.save(tasks)
        return task


def _find(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise TaskNotFoundError(task_id)


def _validate_priority(priority: str) -> str:
    normalized = priority.strip().lower()
    if normalized not in PRIORITIES:
        choices = ", ".join(PRIORITIES)
        raise ValueError(f"Invalid priority '{priority}'. Choose one of: {choices}")
    return normalized
