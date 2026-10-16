"""Command-line interface for the task tracker."""

from __future__ import annotations

import argparse
import sys

from task_tracker.tasks import (
    DEFAULT_PRIORITY,
    PRIORITIES,
    Task,
    TaskNotFoundError,
    TaskStore,
)

DEFAULT_FILE = "tasks.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task-tracker",
        description="A small command-line task tracker.",
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_FILE,
        help=f"path to the JSON file that stores tasks (default: {DEFAULT_FILE})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="add a new task")
    add_parser.add_argument("title", help="title of the task")
    add_parser.add_argument(
        "--priority",
        default=DEFAULT_PRIORITY,
        help=f"one of: {', '.join(PRIORITIES)} (default: {DEFAULT_PRIORITY})",
    )

    subparsers.add_parser("list", help="list all tasks")

    done_parser = subparsers.add_parser("done", help="mark a task as completed")
    done_parser.add_argument("id", type=int, help="id of the task")

    delete_parser = subparsers.add_parser("delete", help="delete a task")
    delete_parser.add_argument("id", type=int, help="id of the task")

    return parser


def format_task(task: Task) -> str:
    status = "x" if task.done else " "
    return f"{task.id:>3}  [{status}]  {task.priority:<6}  {task.title}"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = TaskStore(args.file)

    try:
        if args.command == "add":
            task = store.add(args.title, args.priority)
            print(f"Added task {task.id}: {task.title} ({task.priority} priority)")
        elif args.command == "list":
            tasks = store.load()
            if not tasks:
                print("No tasks yet.")
            for task in tasks:
                print(format_task(task))
        elif args.command == "done":
            task = store.complete(args.id)
            print(f"Completed task {task.id}: {task.title}")
        elif args.command == "delete":
            task = store.delete(args.id)
            print(f"Deleted task {task.id}: {task.title}")
    except (TaskNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
