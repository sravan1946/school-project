import datetime
import json
import os
from pathlib import Path
import sys
import tabulate

PATH = Path(f"{os.getcwd()}/data")


def get_choice() -> int:
    print("""
        [0] Quit program
        [1] Add an elements to the list
        [2] Remove am element from the list
        [3] Mark as Completed/Uncompleted 
        [4] Display the current list
    """
    )
    try:
        return int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Try again.")
        return get_choice()

def file_exists(username: str) -> bool:
    try:
        open(f"{PATH}/{username}.json").close()
    except FileNotFoundError:
        return False
    else:
        return True

def maybe_create_file(username: str) -> None:
    if not PATH.exists():
        PATH.mkdir()
    try:
        open(f"{PATH}/{username}.json").close()
    except FileNotFoundError:
        open(f"{PATH}/{username}.json", "w").close()

def get_data(username) -> dict:
    with open(f"{PATH}/{username}.json") as f:
        d = f.read()
        if d == "":
            d = "{}"
        data = json.loads(d)
    return data

def write_data(dataobj, username) -> None:
    with open(f"{PATH}/{username}.json", "w+") as f:
        json.dump(dataobj, f)

def add_data(username: str) -> None:
    inp = input("Enter new TODO to be added: ")
    data = get_data(username)
    new_data = {"todo": inp, "status": False, "created_at": int(datetime.datetime.now().timestamp())}
    new_id = 1 if len(data) == 0 else max(int(x) for x in data.keys()) + 1
    data[str(new_id)] = new_data
    write_data(data, username)
    print("✅ Added to your TODO list.")
    return

def remove_data(username: str) -> None:
    data = get_data(username)
    if len(data) == 0:
        return print("❌ No data to remove.")
    display_data(username)
    inp = input("Enter the ID of the TODO to be removed: ")
    try:
        inp = int(inp)
    except ValueError:
        return print("❌ Invalid ID.")
    if inp not in range(1, len(data)+1):
        return print("❌ Invalid ID.")
    for i, (k, v) in enumerate(data.items()):
        if i+1 == inp:
            data.pop(k)
            break
    write_data(data, username)
    print("✅ Removed from TODO list.")
    return

def modify_data(username: str) -> None:
    data = get_data(username)
    if len(data) == 0:
        return print("❌ No data to modify.")
    display_data(username)
    inp = input("Enter the ID of the TODO to be modified: ")
    try:
        inp = int(inp)
    except ValueError:
        return print("❌ Invalid ID.")
    if inp not in range(1, len(data)+1):
        return print("❌ Invalid ID.")
    for i, (k, v) in enumerate(data.items()):
        if i+1 == inp:
            new_status = not v["status"]
            data[k]["status"] = new_status
            break
    write_data(data, username)
    print("✅ Modified TODO.")
    return

def quit_() -> None:
    return sys.exit("Thank you for using the program")

def display_data(username: str) -> None:
    data = get_data(username)
    if len(data) == 0:
        return print("❌ No data to display.")
    table = [
        [
            i + 1, v["todo"],
            "✅" if v["status"] else "❌",
            datetime.datetime.fromtimestamp(v["created_at"])
            ]
        for i, (k, v) in enumerate(data.items())]

    print(tabulate.tabulate(table, headers=["ID", "TODO", "Completed", "Created at"], tablefmt="fancy_grid"))
    return
