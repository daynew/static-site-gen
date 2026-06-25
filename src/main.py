from textnode import TextNode, TextType
from generate import generate_page, generate_md
import os
import sys
import shutil


def copy_static(src: str, dest: str):
    if not os.path.exists(src):
        print(f"Error: {src} does not exist")
        sys.exit(1)
    if not os.path.isdir(src):
        print(f"Error: {src} must be a directory")

    if os.path.exists(dest):
        print(f"Deleting {dest}")
        shutil.rmtree(dest)
    print(f"Initializing {dest}")
    os.mkdir(dest)

    for file in os.listdir(src):
        src_file_path = os.path.join(src, file)
        dest_file_path = os.path.join(dest, file)

        if os.path.isfile(src_file_path):
            print(f"Copying {src_file_path} to {dest_file_path}")
            shutil.copy(src_file_path, dest_file_path)
        elif os.path.isdir(src_file_path):
            print(f"Recursively copying {src_file_path}")
            copy_static(src_file_path, dest_file_path)


def __main__():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("./static", "./docs")
    generate_md("./content", "./template.html", "./docs", basepath)


__main__()
