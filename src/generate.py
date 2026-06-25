import os
from convert import markdown_to_html_node
from extract_markdown import extract_title


def generate_page(src_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {src_path} to {
          dest_path} using {template_path}")

    src_md = None
    template_content = None
    with open(src_path) as src_file:
        src_md = src_file.read()
    with open(template_path) as template_file:
        template_content = template_file.read()
    src_html = markdown_to_html_node(src_md).to_html()
    src_title = extract_title(src_md)
    template_html = template_content.replace(
        "{{ Title }}", src_title).replace("{{ Content }}", src_html)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(template_html)


def generate_md(src_path: str, template_path: str, dest_path: str):
    for filename in os.listdir(src_path):
        src_file_path = os.path.join(src_path, filename)
        if os.path.isfile(src_file_path) and filename.endswith(".md"):
            dest_file_path = os.path.join(dest_path, filename[:-3] + ".html")
            generate_page(src_file_path, template_path, dest_file_path)
        elif os.path.isdir(src_file_path):
            generate_md(src_file_path, template_path,
                        os.path.join(dest_path, filename))
