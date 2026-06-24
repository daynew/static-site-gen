from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        texts = node.text.split(delimiter)
        for i in range(0, len(texts)):
            if texts[i] == '':
                continue
            if i % 2 == 0:
                result.append(TextNode(texts[i], TextType.TEXT))
            else:
                result.append(TextNode(texts[i], text_type))

    return result


def split_nodes_image(old_nodes: list[TextNode]):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        images = extract_markdown_images(node.text)
        text = node.text
        for image_alt, image_link in images:
            image = f"![{image_alt}]({image_link})"
            texts = text.split(image, 1)
            if texts[0] != '':
                result.append(TextNode(texts[0], TextType.TEXT))
            result.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = texts[1] if len(texts) == 2 else ''
        if text != '':
            result.append(TextNode(text, TextType.TEXT))
    return result


def split_nodes_link(old_nodes: list[TextNode]):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        links = extract_markdown_links(node.text)
        text = node.text
        for link_text, link_url in links:
            link = f"[{link_text}]({link_url})"
            texts = text.split(link, 1)
            if texts[0] != '':
                result.append(TextNode(texts[0], TextType.TEXT))
            result.append(TextNode(link_text, TextType.LINK, link_url))
            text = texts[1] if len(texts) == 2 else ''
        if text != '':
            result.append(TextNode(text, TextType.TEXT))
    return result
