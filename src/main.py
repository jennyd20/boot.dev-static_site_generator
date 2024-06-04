import os
from .initialize import generate_public_assets, generate_html_page


if __name__ == "__main__":
    src_dir = os.path.dirname(__file__)
    base_dir = os.path.dirname(src_dir)  # TODO: Can use pathlib for this part

    # Reset the public directory and copy assets from the static dir
    generate_public_assets(base_dir)

    # TODO: Best to set these as defaults and not hard-code them (can pass as args, for instance?)
    from_path = os.path.join(base_dir, "content/index.md")
    template_path = os.path.join(base_dir, "template.html")
    dest_path = os.path.join(base_dir, "public/index.html")

    print(f"Generating site from {from_path} to {dest_path} using {template_path}")
    site_html = generate_html_page(from_path, template_path)

    # Write HTML to dest_path
    with open(dest_path, "w") as dest_file:
        dest_file.write(site_html)

    print("Completed site generation")
