# Task CLI

A simple, lightweight command-line todo list application written in Python. It stores all tasks in a single JSON file.

Built as a learning project to practice argparse, pytest, and clean testing with temporary databases.

## Features

- Add new tasks
- List all tasks or filter by status (todo, in-progress, done)
- Update task description
- Delete tasks by ID
- Mark tasks as in-progress or done
- Persistent storage in JSON format
- Displays timestamps in local time
- Safe atomic saving using temporary files

## Installation

1. Clone the repository:
   git clone `https://github.com/yourusername/task-cli.git`
   cd task-cli

2. Install dependencies:
   pip install platformdirs

## Usage

Run the CLI using the module syntax:

`python -m task_cli <command> [arguments]`

### Examples

Add a task:
python -m task_cli add "Finish pytest chapter"

List all tasks:
python -m task_cli list

List only done tasks:
python -m task_cli list done

Update a task:
python -m task_cli update 1 "Finish pytest chapter and exercises"

Delete a task:
python -m task_cli delete 2

Mark as in-progress:
python -m task_cli mark-in-progress 1

Mark as done:
python -m task_cli mark-done 3

## Project Structure

```text
task-cli/
├── task_cli/
│   ├── __init__.py
│   ├── main.py          # CLI argument parsing and command logic
│   └── utils.py         # Database operations, time handling, and display
├── tests/
│   ├── conftest.py      # Shared pytest fixture for temporary DB
│   └── test_main.py     # Comprehensive test suite
├── README.md
└── requirements.txt     # (optional)
```

## Running Tests

Install test requirements:
`pip install pytest`

Run the full test suite:
`pytest`

Run with more details:
`pytest -v`

All tests run against an isolated temporary database, so they do not affect your real tasks.

## Requirements

- Python 3.13 (could use lower version, I wasn't thinking or anything when picking up this version)
- platformdirs

## Example Output

When you add a task:
ID: 1
Description: Finish pytest chapter
Status: todo
Created At: 2026-04-27 07:15 AM WIB
Updated At: 2026-04-27 07:15 AM WIB

## Testing Approach

- Uses pytest with tmp_path fixture for temporary storage
- Overrides load_db and save_db functions to ensure full isolation
- Covers all commands including success and error cases
- No real files are touched during testing

## Future Enhancements

- Migrate to Typer for modern CLI experience
- Add colored output with rich library
- Introduce proper Storage class for better dependency injection
- Support configuration file
- Add export / import functionality

## License

MIT License

---

Made with ❤️ while learning pytest and CLI development in Python.
