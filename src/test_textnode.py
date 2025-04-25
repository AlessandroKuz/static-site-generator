import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
