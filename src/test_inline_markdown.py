import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes
)
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


class TestExtractMarkdownFunctions(unittest.TestCase):
    def test_images_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(expected_result, images)

    def test_links_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(expected_result, links)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertListEqual( new_nodes, expected_result)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_invalid_input_provided(self):
        node = TextNode(
            "![image link](https://www.example.com/image.png)",
            TextType.TEXT,
        )
        with self.assertRaises(ValueError) as cm:
            split_nodes_image(node)
        self.assertEqual(str(cm.exception), "provided old_nodes is not of type list")

        invalid_list = ['hello', 123]
        with self.assertRaises(ValueError) as cm:
            split_nodes_image(invalid_list)
        self.assertEqual(str(cm.exception), f"an old_nodes list element is not of valid type (TextNode), instead got {type(invalid_list[0])}")

    def test_non_text_nested_nodes(self):
        node = TextNode(
            "here is how a markdown link should look like: ![link](https://www.example.com/image.png)",
            TextType.CODE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "here is how a markdown link should look like: ![link](https://www.example.com/image.png)",
                    TextType.CODE,
                )
            ],
            new_nodes,
        )

    def test_imageless_node(self):
        node = TextNode("here is a simple text node", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("here is a simple text node", TextType.TEXT)], new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode( "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(expected_result, new_nodes)

        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links2(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/) and another [second link](https://i.imgur.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/"
            ),
        ]
        self.assertListEqual( new_nodes, expected_result)

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode(
            "[link](https://www.example.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.example.com/"),
            ],
            new_nodes,
        )

    def test_invalid_input_provided(self):
        node = TextNode(
            "[link](https://www.example.com/)",
            TextType.TEXT,
        )
        with self.assertRaises(ValueError) as cm:
            split_nodes_link(node)
        self.assertEqual(str(cm.exception), "provided old_nodes is not of type list")

        invalid_list = ['hello', 123]
        with self.assertRaises(ValueError) as cm:
            split_nodes_link(invalid_list)
        self.assertEqual(str(cm.exception), f"an old_nodes list element is not of valid type (TextNode), instead got {type(invalid_list[0])}")

    def test_non_text_nested_nodes(self):
        node = TextNode(
            "here is how a markdown link should look like: [link](https://www.example.com/)",
            TextType.CODE,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "here is how a markdown link should look like: [link](https://www.example.com/)",
                    TextType.CODE,
                )
            ],
            new_nodes,
        )

    def test_linkless_node(self):
        node = TextNode("here is a simple text node", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("here is a simple text node", TextType.TEXT)], new_nodes)


class TestTextToTextNode(unittest.TestCase):
    def test_multiple_node_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_text_nodes(text)
        self.assertEqual(result, expected_result)

    def test_nested_nodes(self):
        text = "This is **text with _nested italic_** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text with _nested italic_", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_text_nodes(text)
        self.assertEqual(result, expected_result)

    def test_nested_nodes(self):
        """
        KEEP IN MIND: the following function is EXPECTED to FAIL
        when reworking the way that TextNodes are split
        - (current/old logic depends on delimiter order inside of ALLOWED_DELIMITERS constant)
        """
        text = "This is _**text with nested bold**_ with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        # expected_result = [
        #     TextNode("This is _", TextType.TEXT),
        #     TextNode("text with nested bold", TextType.ITALIC),
        #     TextNode("_ with an ", TextType.TEXT),
        #     TextNode("italic", TextType.ITALIC),
        #     TextNode(" word and a ", TextType.TEXT),
        #     TextNode("code block", TextType.CODE),
        #     TextNode(" and an ", TextType.TEXT),
        #     TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        #     TextNode(" and a ", TextType.TEXT),
        #     TextNode("link", TextType.LINK, "https://boot.dev"),
        # ]
        # result = text_to_text_nodes(text)
        # self.assertEqual(result, expected_result)

        with self.assertRaises(ValueError) as cm:
            text_to_text_nodes(text)
        self.assertEqual(str(cm.exception), 'provided old_nodes contains an invalid Markdown syntax, the number of "_" delimiters is odd.')
        # An error get raised because the following TextNodes have an odd number of "_".
        #     TextNode("This is _", TextType.TEXT),
        #     TextNode("_ with an ", TextType.TEXT),

    def test_empty_text(self):
        text = ""
        expected_result = []
        result = text_to_text_nodes(text)
        self.assertEqual(result, expected_result)

    def test_invalid_text_type(self):
        text = 123
        with self.assertRaises(ValueError) as cm:
            text_to_text_nodes(text)
        self.assertEqual(str(cm.exception), f"provide text has invalid type, found {type(text)} instead of str")


if __name__ == '__main__':
    unittest.main()
