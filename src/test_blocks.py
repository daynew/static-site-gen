import unittest
from blocks import BlockType, block_to_block_type


class BlocksTest(unittest.TestCase):

    def test_block_to_paragraph(self):
        text = """
a paragraph of
block text
""".strip()
        expected = BlockType.PARAGRAPH
        actual = block_to_block_type(text)
        self.assertEqual(expected, actual)

    def test_block_to_heading(self):
        text = """
# Heading 1
""".strip()
        expected = BlockType.HEADING
        actual = block_to_block_type(text)
        self.assertEqual(expected, actual)

    def test_block_to_code(self):
        text = """
```
Some code written
in a code block.
```
""".strip()
        expected = BlockType.CODE
        actual = block_to_block_type(text)
        self.assertEqual(expected, actual)

    def test_block_to_quote(self):
        text = """
>a quote of
>block text
""".strip()
        expected = BlockType.QUOTE
        actual = block_to_block_type(text)
        self.assertEqual(expected, actual)

    def test_block_to_unordered_list(self):
        text = """
- item a
- item b
""".strip()
        expected = BlockType.UNORDERED_LIST
        actual = block_to_block_type(text)
        self.assertEqual(expected, actual)

    def test_block_to_ordered_list(self):
        text = """
1. item a
2. item b
""".strip()
        expected = BlockType.ORDERED_LIST
        actual = block_to_block_type(text)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
