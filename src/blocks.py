from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(text: str) -> BlockType:
    lines = text.splitlines()

    if len(lines) == 1 and re.search(r"^#{1,6}\s([\w\d\s]+)", text):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    is_quote = True
    for line in lines:
        if re.search(r"^>", line) is None:
            is_quote = False
    if is_quote:
        return BlockType.QUOTE

    is_unordered_list = True
    for line in lines:
        if re.search(r"^-\s", line) is None:
            is_unordered_list = False
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    line_number = 1
    for line in lines:
        match = re.search(r"^(\d+)\.\s", line)
        if match is None or match.group(1) != str(line_number):
            is_ordered_list = False
            break
        line_number += 1
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
