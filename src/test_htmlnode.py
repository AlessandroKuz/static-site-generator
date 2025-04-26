import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_url_optional(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_type_checks(self):
        # Test valid types
        h1 = HTMLNode('h1', 'My heading')
        p = HTMLNode("p", 'lorem ipsum')
        link = HTMLNode(tag="a", props={'href': 'https://boot.dev'})
        HTMLNode("body", children=[h1, p, link])

        # Test invalid tag type
        with self.assertRaises(TypeError) as cm:
            HTMLNode(tag=123)
        self.assertEqual(str(cm.exception), "tag must be a string")

        # Test invalid value type
        with self.assertRaises(TypeError) as cm:
            HTMLNode(value=123)
        self.assertEqual(str(cm.exception), "value must be a string")

        # Test invalid children type
        with self.assertRaises(TypeError) as cm:
            HTMLNode(children=1)
        self.assertEqual(str(cm.exception), "children must be a list")

        # Test invalid props type
        with self.assertRaises(TypeError) as cm:
            HTMLNode(props=1)
        self.assertEqual(str(cm.exception), "props must be a dictionary")

        # Test edge cases
        with self.assertRaises(TypeError) as cm:
            HTMLNode(1, 2, 3, 4)  # test all invalid types
        # The first error encountered (tag) should be raised
        self.assertEqual(str(cm.exception), "tag must be a string")

    def test_eq(self):
        node = HTMLNode("p", 'lorem ipsum')
        node2 = HTMLNode("p", 'lorem ipsum')
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = HTMLNode("p", 'lorem ipsum', children=[])
        node2 = HTMLNode("p", 'lorem ipsum')
        self.assertNotEqual(node, node2)

        node = HTMLNode("p", 'lorem ipsum', children=[])
        node2 = HTMLNode("body", children=[HTMLNode("p", 'lorem ipsum2')])
        self.assertNotEqual(node, node2)

        node = HTMLNode("p", 'lorem ipsum', children=[])
        node2 = HTMLNode("a", props={'href': 'https://boot.dev'})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        tag = "p"
        value = "lorem ipsum"
        node = HTMLNode(tag=tag, value=value)
        self.assertEqual(repr(node), f'HTMLNode({tag}, {value}, {None}, {None})')

        body_tag = "body"
        link_node = HTMLNode(tag='a', props={'href': 'https://boot.dev'})
        children = [node, link_node]
        body_node = HTMLNode(tag=body_tag, children=children)
        self.assertEqual(repr(body_node), f'HTMLNode({body_tag}, {None}, {children}, {None})')

        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )

    def test_to_html(self):
        self.assertRaises(NotImplementedError, HTMLNode.to_html, None)

    def test_props_to_html(self):
        props = {"rel": "stylesheet", "type": "text/css", "href": "styles.css"}
        expected_string = ' rel="stylesheet" type="text/css" href="styles.css"'
        node = HTMLNode("link", props=props)
        self.assertEqual(expected_string, node.props_to_html())

        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

        node = HTMLNode(
            "p",
            "Hello, world!",
        )
        expected_string = ''
        self.assertEqual(expected_string, node.props_to_html())

        node = HTMLNode(
            "p",
            "Hello, world!",
            props={'ciao': '', '': 'test'},
        )
        expected_string = ''
        self.assertEqual(expected_string, node.props_to_html())

        node = HTMLNode(
            "p",
            "Hello, world!",
            props={'': ''},
        )
        expected_string = ''
        self.assertEqual(expected_string, node.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode(tag='p', value='Hello World')
        html = node.to_html()
        self.assertEqual('<p>Hello World</p>', html)

    def test_leaf_to_html_text(self):
        node = LeafNode(value='Hello World')
        html = node.to_html()
        self.assertEqual('Hello World', html)

    def test_leaf_to_html_parent_node(self):
        with self.assertRaises(TypeError):
            LeafNode(tag='body', children=[LeafNode(value='Hello World')])


if __name__ == "__main__":
    unittest.main()
