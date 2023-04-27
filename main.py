from time import sleep
from utils import file_exists, maybe_create_file, get_choice, quit_, add_data, display_data, remove_data, modify_data

print("""
    Welcome to TODO maker!
    """
)

name = input("Enter your name to get started: ")
print("Checking if your data exist...")
sleep(2)
if not file_exists(name):
    print("File not found.")
    print("Creating new file...")
    maybe_create_file(name)
    sleep(3)
    print("File created successfully")
else:
    print("File found! Loading data...")

while True:
    c = get_choice()
    if c == 0:
        quit_()
    elif c == 1:
        add_data(name)
    elif c == 2:
        remove_data(name)
    elif c == 3:
        modify_data(name)
    elif c == 4:
        display_data(name)
    else:
        print("Invalid input. Try again.")