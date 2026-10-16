# task-tracker-demo

A small command-line task tracker written in Python. Tasks are stored in a local
JSON file, so there is nothing to configure: no database, no server, no account.

## Requirements

- Python 3.11 or newer
- No third-party runtime dependencies (pytest is only needed for the tests)

Check your version first. On some systems `python3` still points to an older release:

```bash
python3 --version
```

If it prints something below 3.11, use a specific interpreter such as `python3.12`
in the commands below.

## Installation

```bash
git clone https://github.com/agi1clj/task-tracker-demo.git
cd task-tracker-demo

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e ".[test]"
```

This installs the `task-tracker` command into the virtual environment.

## Usage

```bash
task-tracker add "Buy groceries"
task-tracker add "Pay rent" --priority high
task-tracker list
task-tracker done 1
task-tracker delete 1
```

| Command | Description |
| --- | --- |
| `add TITLE [--priority low\|medium\|high]` | Add a new task (priority defaults to `medium`) |
| `list` | Show all tasks |
| `done ID` | Mark a task as completed |
| `delete ID` | Remove a task |

Priorities are `low`, `medium`, or `high`. Any other value is rejected with an
error. Tasks saved by older versions, which have no priority, are shown as `medium`.

Run `task-tracker --help` or `task-tracker <command> --help` for details.

### Example session

```console
$ task-tracker add "Read chapter 3"
Added task 1: Read chapter 3 (medium priority)
$ task-tracker add "Prepare lab report" --priority high
Added task 2: Prepare lab report (high priority)
$ task-tracker add "Email project group" --priority low
Added task 3: Email project group (low priority)
$ task-tracker done 1
Completed task 1: Read chapter 3
$ task-tracker list
  1  [x]  medium  Read chapter 3
  2  [ ]  high    Prepare lab report
  3  [ ]  low     Email project group
$ task-tracker delete 3
Deleted task 3: Email project group
```

### Where tasks are stored

Tasks are saved to `tasks.json` in the current directory. Use `--file` to choose
another location:

```bash
task-tracker --file ~/my-tasks.json list
```

`tasks.json` is listed in `.gitignore`, so your personal tasks are never committed.

## Running the tests

```bash
pytest
```

## Project structure

```text
task-tracker-demo/
├── task_tracker/
│   ├── __init__.py
│   ├── cli.py        # argument parsing and output
│   └── tasks.py      # Task model and JSON storage
├── tests/
│   └── test_tasks.py
├── pyproject.toml
└── README.md
```
