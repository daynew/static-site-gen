import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\]]*)\]\(([^\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"
    return re.findall(pattern, text)


def extract_title(markdown: str) -> str:
    match = re.search(r"^#\s(.*)", markdown)
    if match is None or match.group(1) is None or match.group(1).strip() == '':
        raise Exception("The markdown must have at least one heading")
    return match.group(1).strip()
