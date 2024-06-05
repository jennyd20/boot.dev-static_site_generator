from pathlib import Path
from .initialize import generate_public_assets, generate_html_pages


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent

    # TODO: Best to set these as defaults and not hard-code them (can pass as args, for instance)
    dir_path_content = Path.joinpath(base_dir, "content")
    template_path = Path.joinpath(base_dir, "template.html")
    dir_path_dest = Path.joinpath(base_dir, "public")
    dir_path_static = Path.joinpath(base_dir, "static")

    # Reset the public directory and copy assets from the static dir
    print(f"Resetting the public assets in {dir_path_dest} using {dir_path_static}")
    generate_public_assets(dir_path_static, dir_path_dest)

    print(f"Generating all pages from {dir_path_content}")
    generate_html_pages(dir_path_content, template_path, dir_path_dest)
    print("Completed site generation")
