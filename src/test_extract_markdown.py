import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links, extract_title


class TestExtractMarkdown(unittest.TestCase):

    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) [link](https://example.com)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")], matches)

    def test_extract_title(self):
        expected = "My Title"
        md = "# My Title\n## Subtitle"
        title = extract_title(md)
        self.assertEqual(expected, title)
