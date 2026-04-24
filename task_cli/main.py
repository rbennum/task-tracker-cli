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
    for entry in data["entries"]:
        utils.display_task(entry)
        print("\n")


def main():
    parser = argparse.ArgumentParser(description="Simple task_cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task_details", help="Task details")
    add_parser.set_defaults(func=add_task_cmd)

    # list
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=list_name_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
