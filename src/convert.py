from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode
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
    blocks = []
    for block in text.split("\n\n"):
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)
    return blocks


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
                text = "\n".join(lines[1:-1]).strip()
                children.append(TextNode(text, TextType.TEXT))
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
                block = block.replace("\n", " ")
                children.extend(text_to_textnodes(block))
        result.append(BlockNode(type, children, props))
    return result


def block_nodes_to_html_nodes(block_nodes: list[BlockNode]) -> list[ParentNode]:
    html_nodes = []
    for block_node in block_nodes:
        match block_node.type:
            case BlockType.PARAGRAPH:
                tag = 'p'
                children = []
                for child in block_node.children:
                    children.append(text_node_to_html_node(child))
                html_nodes.append(ParentNode(tag, children))
            case BlockType.HEADING:
                tag = f"h{block_node.props['level']}"
                children = []
                for child in block_node.children:
                    children.append(text_node_to_html_node(child))
                html_nodes.append(ParentNode(tag, children))
            case BlockType.CODE:
                tag = "code"
                children = []
                for child in block_node.children:
                    children.append(text_node_to_html_node(child))
                code_node = ParentNode(tag, children)
                html_nodes.append(ParentNode('pre', [code_node]))
            case BlockType.QUOTE:
                tag = 'blockquote'
                children = []
                for child in block_node.children:
                    children.append(text_node_to_html_node(child))
                html_nodes.append(ParentNode(tag, children))
            case BlockType.UNORDERED_LIST:
                tag = 'ul'
                list_items = []
                for child in block_node.children:
                    content = text_node_to_html_node(child)
                    list_items.append(ParentNode('li', [content]))
                html_nodes.append(ParentNode(tag, list_items))
            case BlockType.ORDERED_LIST:
                tag = 'ol'
                list_items = []
                for child in block_node.children:
                    content = text_node_to_html_node(child)
                    list_items.append(ParentNode('li', [content]))
                html_nodes.append(ParentNode(tag, list_items))

    return ParentNode('div', html_nodes)


def markdown_to_html_node(markdown: str) -> list[HTMLNode]:
    blocks = markdown_to_blocks(markdown)
    block_nodes = blocks_to_block_nodes(blocks)
    return block_nodes_to_html_nodes(block_nodes)
