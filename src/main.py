import os
import shutil

from generate_page import generate_page


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
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    copy_directory_recursive(static_dir, public_dir)

    from_path = os.path.join(project_root, "content", "index.md")
    template_path = os.path.join(project_root, "template.html")
    dest_path = os.path.join(public_dir, "index.html")
    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
