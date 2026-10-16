# AGENTS.md

Guidance for AI coding assistants working in this repository.

## Project

`task-tracker-demo` is a small Python CLI for managing a to-do list. Tasks are
stored in a local JSON file (`tasks.json` by default). It is used for teaching,
so readability matters more than cleverness.

- `task_tracker/tasks.py`: `Task` dataclass and `TaskStore` (JSON load/save, add, complete, delete)
- `task_tracker/cli.py`: `argparse` subcommands and console output; `main(argv)` is the entry point
- `tests/test_tasks.py`: pytest suite covering the store and the CLI

## Environment

- Python 3.11+. On macOS, `python3` may point to an older version; check with `python3 --version`.
- Set up and install:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -e ".[test]"
  ```

- Run the app: `task-tracker add "Title"`, `task-tracker list`, `task-tracker done 1`, `task-tracker delete 1`
- Run the tests: `pytest`

## Code style

- Follow the existing style: type hints, small functions, standard library only.
- Keep business logic in `tasks.py` and input/output in `cli.py`.
- Raise `TaskNotFoundError` or `ValueError` from the store; the CLI turns them into a message and exit code 1.
- Stored JSON must stay readable by older versions of the code where practical. When adding a field, give it a default when it is missing from the file.
- Update `README.md` when user-facing behaviour changes.

## Tests

- Every behaviour change needs tests in `tests/`.
- Use the `tmp_path` fixture or `--file` so tests never touch a real `tasks.json`.
- Run `pytest` before declaring work done. All tests must pass.

## Constraints

- Do not add dependencies. The runtime has none, and pytest is the only test dependency.
- Do not refactor or rename code unrelated to the task.
- Keep changes small and focused so they are easy to review.

## Git

- `main` is the default branch. Work on a feature branch named `feature/<short-description>`.
- Use Conventional Commits, for example `feat: ...`, `fix: ...`, `test: ...`, `docs: ...`.
- Never commit `.venv/`, caches, or `tasks.json`.
