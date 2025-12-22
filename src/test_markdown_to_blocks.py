import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_strips_and_drops_empty(self):
        md = "\n\n   \n\n# Heading\n\n\n\nParagraph\n\n   \n"
        self.assertEqual(markdown_to_blocks(md), ["# Heading", "Paragraph"])

    def test_markdown_to_blocks_preserves_internal_newlines(self):
        md = "a\nb\nc\n\nx"
        self.assertEqual(markdown_to_blocks(md), ["a\nb\nc", "x"])


if __name__ == "__main__":
    unittest.main()


