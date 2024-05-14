#!/usr/bin/env python3
import os
import shutil



### THIS IS THE REAL ONE###



# Write a recursive function that copies all the contents of a directory to another directory.
#This should include all files and subdirectories. Here are some of the stdlib docs that might be helpful:

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


public_path = "../public"
static_path = "../static"

def init():
    # Clear "public" directory
    # _delete_public_()

    _copy_static_(static_path)
    return True



def _copy_static_(current_path):
    # Get a list of files and directories in the current path
    listdir = os.listdir(static_path)
    print(listdir)
    # Separate files from directories
    path_files = []
    path_dirs = []
    for l in listdir:
        path = os.path.join(current_path, l)
        path_files.append(path) if os.path.isfile(path) else path_dirs.append(path)
    print(f"{path_files=}")
    print(f"{path_dirs=}")








def _delete_public_():
    public_path = "../public"
    test_path = "../test_dir"
    if os.path.exists(public_path):
        # Delete it
        ### Test
        #shutil.copy(public_path, test_path)
        print(True)
        pass
    else:
        print(False)
        pass


    if os.path.exists(test_path):
        print(True)
        pass
    else:
        print(False)
        print("Making test path dir")
        os.mkdir(test_path)
        pass

    if os.path.exists(test_path):
        print("Removing test path")
        shutil.rmtree(test_path)
        pass


# from pathlib import Path
# /home/jenny/workspace/advent_of_code/2023/lib.py

if __name__ == "__main__":
    _copy_static_(public_path)
