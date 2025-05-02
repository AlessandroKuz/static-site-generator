import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        sample_markdown_document = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
        """
        result = markdown_to_blocks(sample_markdown_document)
        expected_result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks2(self):
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

    def test_markdown_to_blocks_newlines(self):
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

    def test_markdown_to_blocks_with_multiple_newlines(self):
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

    def test_empty_string(self):
        """Test that an empty string returns an empty list."""
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        """Test that a string with only whitespace returns an empty list."""
        self.assertEqual(markdown_to_blocks("   \n\n   \n   "), [])

    def test_single_block(self):
        """Test a markdown string with just one block and no separating newlines."""
        md = "This is a single block without any separating newlines"
        self.assertEqual(markdown_to_blocks(md), [md])

    def test_blocks_with_leading_trailing_whitespace(self):
        """Test blocks with leading/trailing whitespace are properly stripped."""
        md = """
        Block with leading spaces
        
        
        Another block with leading spaces
        """
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Block with leading spaces",
                "Another block with leading spaces"
            ]
        )

    def test_blocks_with_special_characters(self):
        """Test blocks containing special characters."""
        md = """
    Block 1 with * special # characters

    Block 2 with > special & characters
    """
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Block 1 with * special # characters",
                "Block 2 with > special & characters"
            ]
        )


if __name__ == "__main__":
    unittest.main()
