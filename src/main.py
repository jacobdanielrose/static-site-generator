import shutil
from generate_page import copy_files, generate_pages_recursive
from pathlib import Path


def main():
    cwd = Path.cwd()
    public_dir = cwd / "public"
    static_dir = cwd / "static"
    template_path = cwd / "template.html"
    content_path = cwd / "content"

    # Clean up public directory
    if public_dir.exists():
        if public_dir.is_dir():
            shutil.rmtree(public_dir)
        else:
            # in case a public file is created instead of a directory
            public_dir.unlink()

    # Create the public directory
    public_dir.mkdir(parents=True, exist_ok=True)


    copy_files(static_dir, public_dir)

    generate_pages_recursive(content_path, template_path, public_dir)

if __name__ == "__main__":
    main()
