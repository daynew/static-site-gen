from textnode import TextNode, TextType
from htmlnode import LeafNode
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from blocks import BlockNode, BlockType, block_to_block_type
import re


def text_node_to_html_node(text_node: "TextNode") -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise ValueError(f'Cannot convert TextType.{
                             text_node.text_type.value.upper()} to LeafNode')


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    return nodes


def markdown_to_blocks(text: str) -> list[str]:
    return list(map(lambda line: line.strip(), text.split("\n\n")))


def blocks_to_block_nodes(blocks: list[str]) -> list[BlockNode]:
    result = []
    for block in blocks:
        type = block_to_block_type(block)
        props = {}
        children = []
        lines = block.splitlines()
        match type:
            case BlockType.HEADING:
                match = re.search(r"^(#{1,6}+)\s(.*)", block)
                props["level"] = len(match.group(1))
                text = match.group(2)
                children.extend(text_to_textnodes(text))
            case BlockType.CODE:
                text = "\n".join(lines[1:-1])
                children.extend(text_to_textnodes(text))
            case BlockType.QUOTE:
                quote_lines = []
                for line in lines:
                    match = re.search(r"^>\s?(.*)", line)
                    text = match.group(1) or ""
                    quote_lines.append(text)
                children.extend(text_to_textnodes("\n".join(quote_lines)))
            case BlockType.UNORDERED_LIST:
                for line in lines:
                    match = re.search(r"^-\s(.*)", line)
                    text = match.group(1) or ""
                    children.extend(text_to_textnodes(text))
            case BlockType.ORDERED_LIST:
                for line in lines:
                    match = re.search(r"^\d+\.\s(.*)", line)
                    text = match.group(1) or ""
                    children.extend(text_to_textnodes(text))
            case _:
                children.extend(text_to_textnodes(block))
        result.append(BlockNode(type, children))
    return result


def markdown_to_html_node(markdown):
    raise NotImplementedError()
