import unittest

from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_simple_code_block(self):
        my_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([my_node], "`", TextType.CODE)
        expecting_nodes = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expecting_nodes)

        my_node = TextNode("This is text with a ```code block``` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([my_node], "```", TextType.CODE)
        expecting_nodes = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expecting_nodes)

    def test_simple_italic_block(self):
        my_node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([my_node], "_", TextType.ITALIC)
        expecting_nodes = [TextNode("This is text with an ", TextType.TEXT), TextNode("italic block", TextType.ITALIC), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expecting_nodes)

        my_node = TextNode("This is text with an *italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([my_node], "*", TextType.ITALIC)
        expecting_nodes = [TextNode("This is text with an ", TextType.TEXT), TextNode("italic block", TextType.ITALIC), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expecting_nodes)

    def test_simple_bold_block(self):
        my_node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([my_node], "**", TextType.BOLD)
        expecting_nodes = [TextNode("This is text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expecting_nodes)

    def test_invalid_delimiter(self):
        my_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([my_node], "?", TextType.CODE)
        self.assertEqual(str(cm.exception), 'provided delimiter "?" is not supported.')

        my_node = TextNode("This is text", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([my_node], "text", TextType.CODE)
        self.assertEqual(str(cm.exception), 'provided delimiter "text" is not supported.')

    def test_invalid_delimiter_number(self):
        my_node = TextNode("This is text with a `broken `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([my_node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), 'provided old_nodes contains an invalid Markdown syntax, the number of "`" delimiters is odd.')

    def test_no_delimiter_in_text(self):
        my_node = TextNode("This is text without any code block", TextType.TEXT)
        result = split_nodes_delimiter([my_node], "`", TextType.CODE)
        self.assertEqual(result, [my_node])

    def test_bundled_delimiter(self):
        my_node = TextNode("This is text with weird `` code blocks", TextType.TEXT)
        result = split_nodes_delimiter([my_node], "`", TextType.CODE)
        expecting_nodes = [TextNode("This is text with weird ", TextType.TEXT), TextNode('', TextType.CODE), TextNode(" code blocks", TextType.TEXT)]
        self.assertEqual(result, expecting_nodes)

    def test_void_text(self):
        my_node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([my_node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("", TextType.TEXT)])

    def test_multiple_input_nodes(self):
        my_node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        my_node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([my_node1, my_node2], "`", TextType.CODE)
        expecting_nodes: list[TextNode] = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        expecting_result: list[TextNode] = expecting_nodes * 2  # Get a list of merged expecting nodes
        self.assertEqual(result, expecting_result)

    def test_multiple_nodes_with_different_delimiters(self):
        my_node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        my_node2 = TextNode("This is text with a *italic block* word", TextType.TEXT)
        my_node3 = TextNode("This is text with a _italic block_ word", TextType.BOLD)
        partial_result = split_nodes_delimiter([my_node1, my_node2, my_node3], "`", TextType.CODE)
        result = split_nodes_delimiter(partial_result, "*", TextType.ITALIC)
        expecting_first_nodes: list[TextNode] = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        expecting_second_nodes: list[TextNode] = [TextNode("This is text with a ", TextType.TEXT), TextNode("italic block", TextType.ITALIC), TextNode(" word", TextType.TEXT)]
        expected_result = expecting_first_nodes + expecting_second_nodes + [my_node3]
        self.assertEqual(result, expected_result)

    def test_multiple_delimiters_in_one_node(self):
        my_node = TextNode("This is text with a `code block` word and a new `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([my_node], "`", TextType.CODE)
        expected_result = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word and a new ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(result, expected_result)

        my_node = TextNode("This is text with a `code block` word and a new `code block` word a third `code block` final.", TextType.TEXT)
        result = split_nodes_delimiter([my_node], "`", TextType.CODE)
        expected_result = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word and a new ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word a third ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" final.", TextType.TEXT)]
        self.assertEqual(result, expected_result)

    def test_multiple_different_delimiters_in_one_node(self):
        my_node = TextNode("This is text with a `code block` word and a *italic block* word", TextType.TEXT)
        partial_result = split_nodes_delimiter([my_node], "`", TextType.CODE)
        result = split_nodes_delimiter(partial_result, "*", TextType.ITALIC)
        expecting_first_nodes: list[TextNode] = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE)]
        expecting_second_nodes: list[TextNode] = [TextNode(" word and a ", TextType.TEXT), TextNode("italic block", TextType.ITALIC), TextNode(" word", TextType.TEXT)]
        expected_result = expecting_first_nodes + expecting_second_nodes
        self.assertEqual(result, expected_result)

    def test_delimiter_at_the_end_of_sequence(self):
        my_node = TextNode("This is text with a `code block` word and a new `code block` word``", TextType.TEXT)
        result = split_nodes_delimiter([my_node], "`", TextType.CODE)
        expected_result = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word and a new ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT), TextNode("", TextType.CODE), TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
