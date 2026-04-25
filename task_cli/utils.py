from datetime import datetime, timezone
from platformdirs import user_cache_path
from pathlib import Path
import json
import os

# configure cache path
DATA_PATH = user_cache_path("task-cli", "ranum")
DB_FILE = DATA_PATH / "database.json"
JSON_OPTS = {"indent": 4, "sort_keys": True}


def get_time():
    return datetime.now(timezone.utc).isoformat()


def load_db(file_path: Path = DB_FILE):
    try:
        return json.loads(file_path.read_text(encoding="UTF-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"next_id": 1, "entries": []}


def save_db(data: dict, file_path: Path = DB_FILE):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_file = file_path.with_suffix(".tmp")
    with open(temp_file, "w", encoding="UTF-8") as f:
        json.dump(data, f, **JSON_OPTS)
    os.replace(temp_file, file_path)


def display_local_time(time: str):
    utc_dt = datetime.fromisoformat(time)
    local_dt = utc_dt.astimezone()
    return f"{local_dt.strftime('%Y-%m-%d %I:%M %p %Z')}"


def display_task(entry: dict):
    print(f"ID: {entry["id"]}")
    print(f"Description: {entry["description"]}")
    print(f"Status: {entry["status"]}")
    print(f"Created At: {display_local_time(entry["created_at"])}")
    print(f"Updated At: {display_local_time(entry["updated_at"])}")
