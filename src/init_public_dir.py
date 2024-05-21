from email.mime import base
import os
import shutil

# Write a recursive function that copies all the contents of a directory to another directory.
# This should include all files and subdirectories. Here are some of the stdlib docs that might be helpful:

# os.path.exists
# os.listdir
# os.path.join
# os.path.isfile
# os.mkdir
# shutil.copy
# shutil.rmtree
# I'd recommend logging the path of each file you copy, so you can see what's happening.


# It should copy the contents of a "static" directory to a public directory in the root of your project.
# Make sure to delete the contents of the "public" directory before you start copying files into it so that each run of your program is idempotent.
# That's just a fancy word that means it can be run multiple times safely (won't create duplicates).


def generate():
    print("Generating public website...")
    src_dir = os.path.dirname(__file__)

    # Get to the root directory
    # base_dir = src_dir + "/../TEST_FOLDER_FOR_INIT"
    base_dir = os.path.join(src_dir, "..") # TODO: Can use pathlib for this part

    _reset_public_dir(base_dir)
    _copy_static_(base_dir)


def _reset_public_dir(base_dir):
    public_path = os.path.join(base_dir + "public")

    # Remove the old public directory, if applicable
    if os.path.exists(public_path):
        print(f"Old public directory exists, deleting: {public_path}")
        shutil.rmtree(public_path)

    # Create a new empy public directory
    print(f"Creating new public dir: {public_path}")
    os.mkdir(public_path)


def _copy_static_(base_dir, sub_dir=""):
    static_dir = "static"
    public_dir = "public"
    current_static_path = os.path.join(base_dir, static_dir, sub_dir)
    current_public_path = os.path.join(base_dir, public_dir, sub_dir)
    print(f"Copying from directory: {current_static_path}")

    # Get a list of files and directories in the current static path
    listdir = os.listdir(current_static_path)
    print(f"Items: {listdir}")
    # Separate files from directories
    path_files = []
    path_dirs = []
    print("\nGoing through each item...")
    for item in listdir:
        print(f"\nItem: {item}")
        item_static_path = os.path.join(current_static_path, item)
        if os.path.isfile(item_static_path):
            print("\t- Is a file")
            path_files.append(item)
        else:
            print("\t- Is a directory")
            path_dirs.append(item)

    print()
    print(f"{path_files=}")
    print(f"{path_dirs=}")

    # For each file, copy to the public dir
    for f in path_files:
        print(f"Copying file: {f}")
        shutil.copy(os.path.join(current_static_path, f), os.path.join(current_public_path, f))

    # For each directory, create that directory in the public dir and recursively copy that folder's contents
    for d in path_dirs:
        print(f"Creating directory: {d}")
        os.mkdir(os.path.join(current_public_path, d))
        _copy_static_(base_dir, os.path.join(sub_dir, d))
    pass

if __name__ == "__main__":
    generate()
