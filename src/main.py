import shutil
from generate_page import copy_files, generate_pages_recursive
from pathlib import Path
import sys

def main():
    if len(sys.argv) > 1:
        base_path = Path(sys.argv[1])
    else:
        base_path = Path("/")

    cwd = Path.cwd()
    docs_dir = cwd / "docs"
    static_dir = cwd / "static"
    template_path = cwd / "template.html"
    content_path = cwd / "content"

    # Clean up public directory
    if docs_dir.exists():
        if docs_dir.is_dir():
            shutil.rmtree(docs_dir)
        else:
            # in case a public file is created instead of a directory
            docs_dir.unlink()

    # Create the public directory
    docs_dir.mkdir(parents=True, exist_ok=True)

    copy_files(static_dir, docs_dir)

    generate_pages_recursive(content_path, template_path, docs_dir, base_path)

if __name__ == "__main__":
    main()
