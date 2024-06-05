from pathlib import Path
import shutil
import re

from .block_markdown import markdown_to_html_node


# Copy the contents of a "static" directory to a public directory in the root of your project.
# Make sure to delete the contents of the "public" directory before you start copying files
# into it so that each run of your program is idempotent.
def generate_public_assets(dir_path_static, dir_path_dest):
    print(f"Resetting the public directory: {dir_path_dest}")

    # Remove the old public directory, if applicable
    if Path.exists(dir_path_dest):
        print(f"Deleting existing public directory")
        shutil.rmtree(dir_path_dest)

    # Create a new empy public directory
    print(f"Creating new public directory")
    dir_path_dest.mkdir()

    _copy_dir(dir_path_static, dir_path_dest)


def _copy_dir(from_dir, to_dir, file_filter=None):
    print(f"Copying contents of {from_dir} to the public directory")
    for root, dirs, files in from_dir.walk():
        subdir = root.relative_to(from_dir)
        dest_matching_dir_path = Path.joinpath(to_dir, subdir)
        for f in files:
            from_dir_file_path = Path.joinpath(root, f)
            if file_filter:
                # If a filter has been specified, do that rather than the default
                file_filter(f, from_dir_file_path, dest_matching_dir_path)
            else:
                # By default, just copy the file
                print(f"Copying file: {from_dir_file_path}")
                to_dir_file_path = Path.joinpath(dest_matching_dir_path, f)
                shutil.copy(from_dir_file_path, to_dir_file_path)
        for d in dirs:
            print(f"Creating subdirectory {d}")
            subdir_path = Path.joinpath(dest_matching_dir_path, d)
            subdir_path.mkdir()


TITLE_REGEX = re.compile(r"^# (?P<title>.+)", re.MULTILINE)


def generate_html_pages(dir_path_content, template_path, dir_path_dest):
    # Only copy MD files after converting to HTML
    def _check_md(file, from_path, to_path):
        if file.endswith(
            ".md",
        ):
            file_name = file.removesuffix(".md") + ".html"
            html_page = _generate_html_page(from_path, template_path)
            html_path = Path.joinpath(to_path, file_name)
            print(f"Creating {html_path}")
            html_path.write_text(html_page)

    _copy_dir(dir_path_content, dir_path_dest, _check_md)


# Read the markdown file and grab its title.
# Convert the markdown to HTML.
# Insert the title and HTML into the template
def _generate_html_page(file_path, template_path):
    # Read the input markdown file
    with open(file_path) as input_file:
        input = input_file.read()

    # Get the title of this page
    title_matches = list(TITLE_REGEX.finditer(input))
    if len(title_matches) != 1:
        raise ValueError("Markdown must have a single populated h1 header (title)")

    title = title_matches[0]["title"]

    # Read the template
    with open(template_path) as template_file:
        template = template_file.read()

    output_html = markdown_to_html_node(input).to_html()
    return template.replace("{{ Title }}", title).replace("{{ Content }}", output_html)
