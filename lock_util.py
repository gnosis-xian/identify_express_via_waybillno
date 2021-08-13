import os

def locked(current_lock_file):
    return os.path.exists(current_lock_file)

def create_lock(current_lock_file):
    if os.path.exists(current_lock_file) is False:
        with open(current_lock_file, "w") as file:
            file.write("")

def remove_lock(current_lock_file):
    if os.path.exists(current_lock_file):
        os.remove(current_lock_file)
