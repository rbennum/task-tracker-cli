import pytest
import json
from pathlib import Path


@pytest.fixture
def temp_db(tmp_path: Path, monkeypatch):
    """Creates a temporary database file for testing."""
    fake_data_path = tmp_path / "task-cli" / "ranum"
    fake_db_file = fake_data_path / "database.json"
    fake_data_path.mkdir(parents=True, exist_ok=True)
    initial_data = {"next_id": 1, "entries": []}
    fake_db_file.write_text(
        json.dumps(initial_data, indent=4, ensure_ascii=False), encoding="UTF-8"
    )

    monkeypatch.setattr("task_cli.utils.DATA_PATH", fake_data_path)
    monkeypatch.setattr("task_cli.utils.DB_FILE", fake_db_file)

    # improper hax
    def fake_load_db(file_path: Path | None = None):
        path = file_path or fake_db_file
        try:
            return json.loads(path.read_text(encoding="UTF-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return {"next_id": 1, "entries": []}

    def fake_save_db(data: dict, file_path: Path | None = None):
        path = file_path or fake_db_file
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_file = path.with_suffix(".tmp")
        with open(temp_file, "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)
        import os

        os.replace(temp_file, path)

    monkeypatch.setattr("task_cli.utils.load_db", fake_load_db)
    monkeypatch.setattr("task_cli.utils.save_db", fake_save_db)

    return fake_db_file
