from enum import Enum
from textnode import TextNode
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class BlockNode():
    def __init__(self, type: BlockType, children: list[TextNode], props: dict[str, str] = {}):
        self.type = type
        self.children = children
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, BlockNode):
            return False
        if self.type != other.type:
            return False
        if self.children != other.children:
            return False
        return True

    def __repr__(self) -> str:
        children = map(lambda c: repr(c), self.children)
        return f"BlockNode({self.type.value}, {",".join(children)})"


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
