import shutil
from pathlib import Path


from blocks import markdown_to_html_node

def extract_title(markdown: str) -> str:
    """Extracts the title from the markdown file"""
    lines = markdown.split("\n")
    for line in lines:
        if line and line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("There is no title! Please make sure at least one heading is the title! i.e. # heading")

def generate_page(from_path: Path, template_path: Path, dest_path: Path, base_path: Path):
    """
    Creates the index.html page for the static site based off the given markdown files in the content folder
    and writes it to the proper folder for hosting
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file
    md = from_path.read_text()

    # Read template file
    template = template_path.read_text()

    # markdown to html conversions
    html_node = markdown_to_html_node(md)
    content = html_node.to_html()

    # extract title
    title = extract_title(md)

    # replace template placeholders with actual values
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    # replace all links
    html = html.replace('href="/', f'href="{base_path}')
    html = html.replace('src="/', f'src="{base_path}')

    # Ensure the directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # write to the destination file
    dest_path.write_text(html)

def copy_files(copy_dir: Path, write_dir: Path) -> None:
    """
    Copies files and directories from one directory to another. Basically the equivalent of
    ` cp -r copy_dir write_dir `
    """
    for path in copy_dir.iterdir():
        dest_path = write_dir / path.name
        if path.is_file():
            print(f"Copying {path}")
            shutil.copy(path, dest_path)
        elif path.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
            copy_files(path, dest_path)

def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path, base_path: Path):
    for path in dir_path_content.iterdir():
        if path.is_file() and path.suffix == ".md":
            dest_file = dest_dir_path / (path.stem + ".html")
            generate_page(path, template_path, dest_file, base_path)
        if path.is_dir():
            dest_dir_path_new = dest_dir_path / path.name
            dest_dir_path_new.mkdir(parents=True, exist_ok=True)
            generate_pages_recursive(path, template_path, dest_dir_path_new, base_path)
