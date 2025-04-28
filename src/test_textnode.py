import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_missing_args(self):
        with self.assertRaises(TypeError) as cm:
           TextNode()
        self.assertEqual(
            str(cm.exception),
            "TextNode.__init__() missing 2 required positional arguments: 'text' and 'text_type'"
        )

        with self.assertRaises(TypeError) as cm:
            TextNode(text='prova')
        self.assertEqual(
            str(cm.exception),
            "TextNode.__init__() missing 1 required positional argument: 'text_type'",
        )

        with self.assertRaises(TypeError) as cm:
            TextNode(text_type=TextType.TEXT)
        self.assertEqual(
            str(cm.exception),
            "TextNode.__init__() missing 1 required positional argument: 'text'",
        )

    def test_url_optional(self):
        # Test case 1: Without URL
        node_without_url = TextNode(text="Hello World!", text_type=TextType.BOLD)
        self.assertIsNone(node_without_url.url)  # Verify url is None when not provided

        # Test case 2: With URL
        node_with_url = TextNode(
            text="boot.dev url", text_type=TextType.LINK, url="https://boot.dev"
        )
        self.assertEqual(
            node_with_url.url, "https://boot.dev"
        )  # Verify URL is set correctly

        # Additional validation
        self.assertIsNotNone(
            node_without_url.text
        )  # Verify text is still set even without URL
        self.assertEqual(
            node_with_url.text_type, TextType.LINK
        )  # Verify text_type is set correctly

    def test_type_checks(self):
        # Test valid types
        TextNode("valid text", TextType.TEXT)  # Should not raise
        TextNode("valid text", TextType.BOLD, "https://valid.url")  # Should not raise

        # Test invalid text type
        with self.assertRaises(TypeError) as cm:
            TextNode(123, TextType.TEXT)
        self.assertEqual(str(cm.exception), "text must be a string")

        # Test invalid text_type type
        with self.assertRaises(TypeError) as cm:
            TextNode("valid text", "invalid_type")
        self.assertEqual(str(cm.exception), "text_type must be a TextType")

        # Test invalid url type
        with self.assertRaises(TypeError) as cm:
            TextNode("valid text", TextType.LINK, 123)
        self.assertEqual(str(cm.exception), "url must be a string")

        # Test edge cases
        with self.assertRaises(TypeError) as cm:
            TextNode("", 123, [])  # Both text_type and url are wrong
        # The first error encountered (text_type) should be raised
        self.assertEqual(str(cm.exception), "text_type must be a TextType")

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("anchor text", TextType.LINK, 'www.boot.dev')
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        text = "This is a text node"
        text_type = TextType.TEXT
        node = TextNode(text, text_type)
        self.assertEqual(repr(node), f'TextNode({text}, {text_type.value}, {None})')


class TestTextToNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a italic text node")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code text node")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, 'https://boot.dev')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {'href': 'https://boot.dev'})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, 'https://boot.dev/images/sample.png')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://boot.dev/images/sample.png', 'alt': 'alt text'})

if __name__ == "__main__":
    unittest.main()
