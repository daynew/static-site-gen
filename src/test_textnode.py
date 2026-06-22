import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
