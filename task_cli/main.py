from task_cli import utils
import argparse


def add_task_cmd(args):
    data = utils.load_db()
    new_entry = {
        "id": data["next_id"],
        "description": args.task_details,
        "status": "todo",
        "created_at": utils.get_time(),
        "updated_at": utils.get_time(),
    }
    data["entries"].append(new_entry)
    data["next_id"] += 1
    utils.save_db(data)
    utils.display_task(new_entry)


def list_name_cmd(args):
    data = utils.load_db()
    status = args.status
    entries = data.get("entries", [])
    if status:
        entries = [e for e in entries if e.get("status") == status]

    if not entries:
        print(f"No tasks found" + (f" with status {status}") if status else "")
        return

    for entry in entries:
        utils.display_task(entry)
        print("\n")


def update_task_cmd(args):
    data = utils.load_db()
    entries = data.get("entries", [])
    target_id = args.id
    task_index = next(
        (i for i, item in enumerate(entries) if item["id"] == target_id), None
    )
    if task_index is not None:
        entries[task_index]["description"] = args.description
        entries[task_index]["updated_at"] = utils.get_time()
        data["entries"] = entries
        utils.display_task(entries[task_index])
        utils.save_db(data)
    else:
        print(f"Task with ID {target_id} not found")


def delete_task_cmd(args):
    data = utils.load_db()
    entries = data.get("entries", [])
    target_id = args.id
    task_index = next(
        (i for i, item in enumerate(entries) if item["id"] == target_id), None
    )
    if task_index is not None:
        deleted_task = entries.pop(task_index)
        data["entries"] = entries
        utils.save_db(data)
        print(
            f"Successfully deleted task {target_id}: '{deleted_task.get("description", "N/A")}'"
        )
    else:
        print(f"Task with ID {target_id} not found")


def mark_task_cmd(args):
    data = utils.load_db()
    entries = data.get("entries", [])
    target_id = args.id
    task_index = next(
        (i for i, item in enumerate(entries) if item["id"] == target_id), None
    )
    if task_index is not None:
        marker = "in-progress" if "in-progress" in args.command else "done"
        entries[task_index]["status"] = marker
        entries[task_index]["updated_at"] = utils.get_time()
        data["entries"] = entries
        utils.save_db(data)
        utils.display_task(entries[task_index])
    else:
        print(f"Task with ID {target_id} not found")


def main(args_list=None):
    parser = argparse.ArgumentParser(description="Simple task_cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task_details", help="Task details")
    add_parser.set_defaults(func=add_task_cmd)

    # list
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "status",
        choices=["todo", "in-progress", "done"],
        help="Filter by task status (todo, in-progress, and done)",
        nargs="?",
    )
    list_parser.set_defaults(func=list_name_cmd)

    # update
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("description", type=str, help="New task description")
    update_parser.set_defaults(func=update_task_cmd)

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to be deleted")
    delete_parser.set_defaults(func=delete_task_cmd)

    # mark-in-progress
    mark_progress_parser = subparsers.add_parser(
        "mark-in-progress", help="Marking a task as in progress"
    )
    mark_progress_parser.add_argument("id", type=int, help="Target task ID")
    mark_progress_parser.set_defaults(func=mark_task_cmd)

    # mark-done
    mark_done_parser = subparsers.add_parser("mark-done", help="Marking a task as done")
    mark_done_parser.add_argument("id", type=int, help="Target task ID")
    mark_done_parser.set_defaults(func=mark_task_cmd)

    args = parser.parse_args(args_list)
    args.func(args)


if __name__ == "__main__":
    main()
