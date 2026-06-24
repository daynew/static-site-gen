
import unittest
from convert import text_node_to_html_node, text_to_textnodes, markdown_to_blocks, blocks_to_block_nodes
from textnode import TextNode, TextType
from blocks import BlockNode, BlockType


class TestConvert(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_to_html(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic_to_html(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a text node")

    def test_code_to_html(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_to_html(self):
        node = TextNode("This is a text node",
                        TextType.LINK, 'https://example.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props['href'], 'https://example.com')

    def test_image_to_html(self):
        node = TextNode("This is a text node",
                        TextType.IMAGE, 'https://example.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props['alt'], "This is a text node")
        self.assertEqual(html_node.props['src'], 'https://example.com')

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        actual = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(expected, actual)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocks_to_block_nodes(self):
        md = """
# Heading 1

```
Some code
in a block
```

>A nice quote

- item a
- item b

1. item a
2. item b

A paragraph with an [example link](https://example.com)
""".strip()
        blocks = markdown_to_blocks(md)
        block_nodes = blocks_to_block_nodes(blocks)
        heading_block = BlockNode(
            BlockType.HEADING, [TextNode("Heading 1", TextType.TEXT)])
        code_block = BlockNode(
            BlockType.CODE, [TextNode("Some code\nin a block", TextType.TEXT)])
        quote_block = BlockNode(
            BlockType.QUOTE, [TextNode("A nice quote", TextType.TEXT)])
        u_list_block = BlockNode(
            BlockType.UNORDERED_LIST, [
                TextNode("item a", TextType.TEXT),
                TextNode("item b", TextType.TEXT),])
        o_list_block = BlockNode(
            BlockType.ORDERED_LIST, [
                TextNode("item a", TextType.TEXT),
                TextNode("item b", TextType.TEXT),])
        paragraph_block = BlockNode(
            BlockType.PARAGRAPH, [
                TextNode("A paragraph with an ", TextType.TEXT),
                TextNode("example link", TextType.LINK, "https://example.com",)])

        expected = [
            heading_block,
            code_block,
            quote_block,
            u_list_block,
            o_list_block,
            paragraph_block,
        ]
        self.assertEqual(expected, block_nodes)


if __name__ == "__main__":
    unittest.main()
