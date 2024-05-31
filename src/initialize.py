import os
import shutil
import re

from .block_markdown import markdown_to_html_node

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


# EXTRACT TITLE FUNCTION
# extract_title(markdown)

# Grab the text of the h1 header from the markdown file (The line that starts with a single #) and return it. If there is no h1 header, raise an exception. All pages need a single h1 header.

TITLE_REGEX = re.compile(r"^# (?P<title>.+)", re.MULTILINE)

def _extract_title(markdown):
    # Find line with the single #
    title = list(TITLE_REGEX.finditer(markdown))
    if len(title) != 1:
        raise ValueError("Markdown must have a single populated h1 header (title)")
    
    return title[0]["title"]



# GENERATE PAGE FUNCTION
# generate_page(from_path, template_path, dest_path)

# Print a message to the console that says something like "Generating page from from_path to dest_path using template_path".
# Read the markdown file at from_path and store the contents in a variable.
# Read the template file at template_path and store the contents in a variable.
# Use your markdown_to_html_node function and .to_html() method to convert the markdown file to HTML.
# Use the extract_title function to grab the title of the page.
# Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
# Write the new HTML to a file at dest_path. Be sure to create any necessary directories if they don't exist.
# Docs that may be helpful:

# open
# .read()
# .close()
# .replace()
# os.path.dirname
# os.makedirs
# .startswith()
# .split()
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    input_file = open(from_path)
    input = input_file.read()
    input_file.close()

    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    output_nodes = markdown_to_html_node(input)
    output_html = output_nodes.to_html()

    title = _extract_title(output_html)

    template.replace(f"{{ Title }}", title)
    template.replace(f"{{ Content }}", output_html)

    print("Completed page generation")

if __name__ == "__main__":
    from_path = "content/index.md"
    template = "template.html"
    dest_path = "public/index.html"
    generate_page(from_path, template, dest_path)
