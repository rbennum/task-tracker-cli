import json
import pytest

from task_cli.main import main


def test_verify_test_db_path(temp_db):
    # This will fail if the app is still pointing to your real AppData/Local folder
    assert "pytest" in str(temp_db) or "tmp" in str(temp_db).lower()


def test_add_task(temp_db, capsys):
    main(["add", "Buy milk"])
    captured = capsys.readouterr()

    assert "ID: 1" in captured.out
    assert "Description: Buy milk" in captured.out
    assert "Status: todo" in captured.out

    # Debug helper (bisa dihapus nanti)
    print("DB file used:", temp_db)
    print("Content after add:", temp_db.read_text(encoding="UTF-8"))

    data = json.loads(temp_db.read_text(encoding="UTF-8"))
    assert data["entries"][0]["description"] == "Buy milk"
    assert data["next_id"] == 2


def test_list_all_tasks(temp_db, capsys):
    main(["add", "Task 1"])
    main(["add", "Task 2"])
    capsys.readouterr()

    main(["list"])
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out


def test_list_filtered_tasks(temp_db, capsys):
    main(["add", "Todo Task"])
    data = json.loads(temp_db.read_text(encoding="UTF-8"))
    data["entries"][0]["status"] = "done"
    json.dump(data, temp_db.open("w", encoding="UTF-8"), indent=4)

    main(["list", "done"])
    out_done = capsys.readouterr().out
    assert "Todo Task" in out_done

    main(["list", "in-progress"])
    out_progress = capsys.readouterr().out
    assert "No tasks found" in out_progress


def test_update_task(temp_db, capsys):
    main(["add", "Old Title"])
    main(["update", "1", "New Title"])

    data = json.loads(temp_db.read_text())
    assert data["entries"][0]["description"] == "New Title"
    assert data["entries"][0]["created_at"] != data["entries"][0]["updated_at"]


def test_delete_task(temp_db, capsys):
    main(["add", "To be deleted"])
    main(["delete", "1"])

    data = json.loads(temp_db.read_text())
    assert len(data["entries"]) == 0
    assert "Successfully deleted task 1" in capsys.readouterr().out


@pytest.mark.parametrize(
    "command,expected", [("mark-in-progress", "in-progress"), ("mark-done", "done")]
)
def test_mark_commands(temp_db, command, expected):
    main(["add", "Status Test"])
    main([command, "1"])

    data = json.loads(temp_db.read_text())
    assert data["entries"][0]["status"] == expected


def test_task_not_found(temp_db, capsys):
    # Try to update ID 999 which doesn't exist
    main(["update", "999", "New"])
    assert "Task with ID 999 not found" in capsys.readouterr().out


def test_invalid_id_type(temp_db):
    # Argparse should catch this and exit
    with pytest.raises(SystemExit):
        main(["delete", "abc"])
