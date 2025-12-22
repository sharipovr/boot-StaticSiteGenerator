import os
import shutil
import sys

from generate_page import generate_pages_recursive


def _copy_directory_recursive(src_dir: str, dest_dir: str) -> None:
    """
    Recursively copy all contents of src_dir into an existing dest_dir.
    """
    for entry in os.listdir(src_dir):
        src_path = os.path.join(src_dir, entry)
        dest_path = os.path.join(dest_dir, entry)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"copied file: {src_path} -> {dest_path}")
            continue

        if os.path.isdir(src_path):
            os.mkdir(dest_path)
            print(f"created dir: {dest_path}")
            _copy_directory_recursive(src_path, dest_path)
            continue

        raise Exception(f"Unsupported file type: {src_path}")


def copy_directory_recursive(src_dir: str, dest_dir: str) -> None:
    """
    Delete the destination directory (if it exists), recreate it, and recursively
    copy all contents of src_dir into it.
    """
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    _copy_directory_recursive(src_dir, dest_dir)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    docs_dir = os.path.join(project_root, "docs")
    copy_directory_recursive(static_dir, docs_dir)

    template_path = os.path.join(project_root, "template.html")
    content_dir = os.path.join(project_root, "content")
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)


if __name__ == "__main__":
    main()
