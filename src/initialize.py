import os
import shutil
import re

from .block_markdown import markdown_to_html_node


# Copy the contents of a "static" directory to a public directory in the root of your project.
# Make sure to delete the contents of the "public" directory before you start copying files
# into it so that each run of your program is idempotent.
def generate_public_assets(base_dir):
    public_dir = os.path.join(base_dir, "public")

    print(f"Resetting the public directory: {public_dir}")
    # Remove the old public directory, if applicable
    if os.path.exists(public_dir):
        print(f"Deleting existing public dir")
        shutil.rmtree(public_dir)

    # Create a new empy public directory
    print(f"Creating new public dir")
    os.mkdir(public_dir)

    # Start copying all the static files starting at the top level
    _copy_static_(base_dir)


# Recursively copies all the contents of a directory to another directory, including files and subdirectories
def _copy_static_(base_dir, sub_dir=""):
    current_static_dir = os.path.join(base_dir, "static", sub_dir)
    current_public_dir = os.path.join(base_dir, "public", sub_dir)
    print(f"\nCopying from directory: {current_static_dir}")

    # Get a list of files and directories in the current static path
    listdir = os.listdir(current_static_dir)
    print(f"All items: {listdir}")

    # Separate files from directories
    path_files = []
    path_dirs = []
    for item in listdir:
        item_static_path = os.path.join(current_static_dir, item)
        if os.path.isfile(item_static_path):
            print(f"{item} - file")
            path_files.append(item)
        else:
            print(f"{item} - directory")
            path_dirs.append(item)
    print(f"{path_files=}")
    print(f"{path_dirs=}")

    # For each file, copy to the public dir
    for f in path_files:
        print(f"Copying file: {f}")
        shutil.copy(
            os.path.join(current_static_dir, f), os.path.join(current_public_dir, f)
        )

    # For each directory, create that directory in the public dir and recursively copy that folder's contents
    for d in path_dirs:
        print(f"Creating directory: {d}")
        os.mkdir(os.path.join(current_public_dir, d))
        _copy_static_(base_dir, os.path.join(sub_dir, d))
    pass


# Read the markdown file and grab its title.
# Convert the markdown to HTML.
# Insert the title and HTML into the template
def generate_html_page(from_path, template_path):
    with open(from_path) as input_file:
        input = input_file.read()

    title = _extract_title(input)

    with open(template_path) as template_file:
        template = template_file.read()

    output_html = markdown_to_html_node(input).to_html()
    return template.replace("{{ Title }}", title).replace("{{ Content }}", output_html)


TITLE_REGEX = re.compile(r"^# (?P<title>.+)", re.MULTILINE)


# Grab the text of the h1 header from the markdown file (The line that starts with a single #) and return it.
# If there is no h1 header, raise an exception. All pages need a single h1 header.
def _extract_title(markdown):
    # Find line with the single #
    title = list(TITLE_REGEX.finditer(markdown))
    if len(title) != 1:
        raise ValueError("Markdown must have a single populated h1 header (title)")

    return title[0]["title"]
