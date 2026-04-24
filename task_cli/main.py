import argparse
import json
from platformdirs import user_cache_path


def save_name_cmd(args):
    print(f"Called: {args.command}")


def load_name_cmd(args):
    print(f"Called: {args.command}")


def main():
    # configure cache path
    DATA_PATH = user_cache_path("task-cli", "ranum")
    DB_FILE = DATA_PATH / "database.json"

    parser = argparse.ArgumentParser(description="Simple task_cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    save_parser = subparsers.add_parser("save", help="Save a new name")
    save_parser.add_argument("name", help="The name to store")
    save_parser.set_defaults(func=save_name_cmd)

    load_parser = subparsers.add_parser("load", help="Load a name")
    load_parser.set_defaults(func=load_name_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
