import json

import pytest

from task_tracker.cli import main
from task_tracker.tasks import Task, TaskNotFoundError, TaskStore


@pytest.fixture
def store(tmp_path):
    return TaskStore(tmp_path / "tasks.json")


def test_load_returns_empty_list_when_file_is_missing(store):
    assert store.load() == []


def test_add_assigns_incrementing_ids(store):
    first = store.add("Write report")
    second = store.add("Review notes")

    assert first.id == 1
    assert second.id == 2
    assert [task.title for task in store.load()] == ["Write report", "Review notes"]


def test_add_strips_whitespace_from_title(store):
    task = store.add("  Buy milk  ")

    assert task.title == "Buy milk"


def test_add_rejects_empty_title(store):
    with pytest.raises(ValueError):
        store.add("   ")


def test_new_task_is_not_done(store):
    task = store.add("Write report")

    assert task.done is False


def test_complete_marks_task_as_done(store):
    task = store.add("Write report")

    store.complete(task.id)

    assert store.load()[0].done is True


def test_complete_unknown_task_raises(store):
    with pytest.raises(TaskNotFoundError):
        store.complete(42)


def test_delete_removes_task(store):
    first = store.add("Write report")
    store.add("Review notes")

    store.delete(first.id)

    assert [task.title for task in store.load()] == ["Review notes"]


def test_delete_unknown_task_raises(store):
    with pytest.raises(TaskNotFoundError):
        store.delete(42)


def test_ids_are_not_reused_after_deleting_last_task(store):
    store.add("Write report")
    second = store.add("Review notes")
    store.delete(second.id)

    third = store.add("Plan sprint")

    assert third.id == 2


def test_tasks_persist_between_store_instances(tmp_path):
    path = tmp_path / "tasks.json"
    TaskStore(path).add("Write report")

    reloaded = TaskStore(path).load()

    assert reloaded == [Task(id=1, title="Write report", done=False, priority="medium")]


def test_saved_file_is_readable_json(store):
    store.add("Write report")

    data = json.loads(store.path.read_text(encoding="utf-8"))

    assert data == [
        {"id": 1, "title": "Write report", "done": False, "priority": "medium"}
    ]


def test_cli_add_and_list(tmp_path, capsys):
    path = str(tmp_path / "tasks.json")

    assert main(["--file", path, "add", "Write report"]) == 0
    assert main(["--file", path, "list"]) == 0

    output = capsys.readouterr().out
    assert "Added task 1: Write report" in output
    assert "[ ]  medium  Write report" in output


def test_cli_list_when_empty(tmp_path, capsys):
    assert main(["--file", str(tmp_path / "tasks.json"), "list"]) == 0

    assert "No tasks yet." in capsys.readouterr().out


def test_cli_done_and_delete(tmp_path, capsys):
    path = str(tmp_path / "tasks.json")
    main(["--file", path, "add", "Write report"])

    assert main(["--file", path, "done", "1"]) == 0
    main(["--file", path, "list"])
    assert "[x]  medium  Write report" in capsys.readouterr().out

    assert main(["--file", path, "delete", "1"]) == 0
    main(["--file", path, "list"])
    assert "No tasks yet." in capsys.readouterr().out


def test_cli_reports_unknown_task(tmp_path, capsys):
    exit_code = main(["--file", str(tmp_path / "tasks.json"), "done", "7"])

    assert exit_code == 1
    assert "No task with id 7" in capsys.readouterr().err


def test_new_task_defaults_to_medium_priority(store):
    task = store.add("Write report")

    assert task.priority == "medium"


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_add_accepts_valid_priority(store, priority):
    store.add("Write report", priority)

    assert store.load()[0].priority == priority


def test_add_rejects_invalid_priority(store):
    with pytest.raises(ValueError, match="Invalid priority 'urgent'"):
        store.add("Write report", "urgent")

    assert store.load() == []


def test_task_without_priority_in_file_defaults_to_medium(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps([{"id": 1, "title": "Old task", "done": True}]), encoding="utf-8"
    )

    tasks = TaskStore(path).load()

    assert tasks == [Task(id=1, title="Old task", done=True, priority="medium")]


def test_cli_add_with_priority_and_list(tmp_path, capsys):
    path = str(tmp_path / "tasks.json")

    assert main(["--file", path, "add", "Write report", "--priority", "high"]) == 0
    assert main(["--file", path, "list"]) == 0

    assert "[ ]  high    Write report" in capsys.readouterr().out


def test_cli_rejects_invalid_priority(tmp_path, capsys):
    path = str(tmp_path / "tasks.json")

    exit_code = main(["--file", path, "add", "Write report", "--priority", "urgent"])

    assert exit_code == 1
    error = capsys.readouterr().err
    assert "Invalid priority 'urgent'" in error
    assert "low, medium, high" in error
