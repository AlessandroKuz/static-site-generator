import unittest

from block_markdown import block_to_block_type, BlockType, markdown_to_blocks


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


class TestMarkdownBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        md = '# h1 heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

        md = '## h2 heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

        md = '### h3 heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

        md = '#### h4 heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

        md = '##### h5 heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

        md = '###### h6 heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_invalid_headings(self):
        md = '####### h7 invalid heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)  # Since its not a valid heading it will be treated as a simple paragrapsh

        md = 'not a #### h4 heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)  # Since its not a valid heading it will be treated as a simple paragrapsh

        md = 'random text'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = 'random text\n# h1 heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_code(self):
        md = '```\nrandom code block```'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.CODE)

        md = '```python\nprint("Hello World!")\n```'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.CODE)

    def test_invalid_code(self):
        md = '```random code block```'  # only one line
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = '``invalid code block``'  # incorrect number of ticks
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = 'sample text ```invalid code block```'  # doesnt start with 3 ticks
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = '```invalid code block``` other text'  # doesnt end with 3 ticks
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_quote(self):
        md = '> This is a simple quote'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)

        md = '> This is a quote\n> with multiple lines'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)

        md = '> This is a quote\n> with multiple lines\n> and a third line\n> and a fourth line for good measure'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)

    def test_invalid_quote(self):
        md = '> This is a quote\n> with multiple lines\n> and a third line\n> and a fourth line for good measure\nThis is not a quote'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = 'This is not a quote'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        md = '1. This is the first item'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)

        md = '1. This is the first item\n2. This is the second item\n3. This is the third item'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_invalid_ordered_list(self):
        md = '1. This is the first item\n3. This is the second item\nthis is a random text'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = '1. This is the first item\nthis is a random text\n2. This is the second item\n3. This is the third item'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_invalid_ordered_list2(self):
        """The following case is supposed to be VALID but it is not supported by the current implementation"""
        md = '0. This is the first item\n1. This is the second item\n2. This is the third item\nThis is not a list'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)  # Since ordered lists start with 1. and go up by one, this is not a valid ordered list

    def test_unordered_list(self):
        md = '- This is the first item'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

        md = '- This is the first item\n- This is the second item\n- This is the third item'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_invalid_unordered_list(self):
        md = '- This is the first item\n- This is the second item\nthis is a random text'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = '- This is the first item\nThis is random text\n- This is the second item\n- This is the third item'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = 'This is not a list'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = 'This is a simple paragraph'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = 'This is a paragraph\nwith multiple lines'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = 'This is a paragraph\nwith multiple lines\nand a third line'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)
        # a test_invalid_paragraph doesnt exist because its supposed to be the default case


if __name__ == "__main__":
    unittest.main()
