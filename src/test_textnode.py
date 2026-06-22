import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):

    def test_eq_url(self):
        node = TextNode("example site", TextType.LINK, "https://example.com")
        node2 = TextNode("example site", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_init_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(None, node.url)

    def test_eq_not_text(self):
        node = TextNode("example site", TextType.LINK, "https://example.com")
        node2 = TextNode("site", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_eq_not_type(self):
        node = TextNode("example site", TextType.IMAGE, "https://example.com")
        node2 = TextNode("example site", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_eq_not_url(self):
        node = TextNode("example site", TextType.LINK, "https://google.com")
        node2 = TextNode("example site", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected = f'TextNode(This is a text node, bold, None)'
        self.assertEqual(expected, f'{node}')

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


if __name__ == "__main__":
    unittest.main()
