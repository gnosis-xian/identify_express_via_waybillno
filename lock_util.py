import os

lock_file = "git.lock"

def locked():
    return os.path.exists(lock_file)

def create_lock():
    if os.path.exists(lock_file) is False:
        with open(lock_file, "w") as file:
            file.write("")

def remove_lock():
    if os.path.exists(lock_file):
        os.remove(lock_file)