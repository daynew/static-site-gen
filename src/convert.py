from textnode import TextNode, TextType
from htmlnode import LeafNode
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link


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
