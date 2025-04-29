import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        node = LeafNode(tag=None, value='Hello World')
        html = node.to_html()
        self.assertEqual('Hello World', html)

    def test_leaf_to_html_parent_node(self):
        with self.assertRaises(TypeError):
            LeafNode(tag='body', children=[LeafNode(value='Hello World')])

    def test_leaf_invalid_types_inheritance(self):
        with self.assertRaises(TypeError) as cm:
            LeafNode(tag=123, value='Hello World')
        self.assertEqual(str(cm.exception), "tag must be a string")
        with self.assertRaises(TypeError) as cm:
            LeafNode(value=123, tag=None)
        self.assertEqual(str(cm.exception), "value must be a string")
        with self.assertRaises(TypeError) as cm:
            LeafNode(props=123, tag=None, value='Hello World')
        self.assertEqual(str(cm.exception), "props must be a dictionary")

    def test_leaf_node_repr(self):
        tag = 'p'
        value = 'Hello World'
        node = LeafNode(tag=tag, value=value)
        expecting_string = f"LeafNode({tag}, {value}, None)"
        self.assertEqual(repr(node), expecting_string)

    def test_leaf_node_empty_string_tag(self):
        node = LeafNode(tag='', value='Hello World')
        self.assertIsNone(node.tag)

    def test_leaf_node_eq_inheritance(self):
        node = LeafNode(tag='p', value='Hello World')
        node2 = LeafNode(tag='p', value='Hello World')
        self.assertEqual(node, node2)

    def test_parent_node_repr(self):
        tag = 'body'
        node1 = LeafNode(tag='p', value='Hello World')
        node2 = LeafNode(tag='bold', value='Hi')
        node3 = LeafNode(tag=None, value='lorem ipsum')
        children = [node1, node2, node3]
        parent_node = ParentNode(tag=tag, children=children)
        expecting_string = f"ParentNode({tag}, {children}, None)"
        self.assertEqual(repr(parent_node), expecting_string)

    def test_parent_node_eq_inheritance(self):
        tag = 'body'
        node1 = LeafNode(tag='p', value='Hello World')
        children = [node1]
        node = ParentNode(tag=tag, children=children)
        node2 = ParentNode(tag=tag, children=children)
        self.assertEqual(node, node2)

    def test_parent_node_invalid_types_inheritance(self):
        with self.assertRaises(TypeError) as cm:
            ParentNode(tag=123, children=[LeafNode(tag=None, value='Hello World')])
        self.assertEqual(str(cm.exception), "tag must be a string")
        with self.assertRaises(TypeError) as cm:
            ParentNode(children=123, tag='body')
        self.assertEqual(str(cm.exception), "children must be a list")
        with self.assertRaises(TypeError) as cm:
            ParentNode(props=123, tag='body', children=[LeafNode(tag=None,value='Hello World')])
        self.assertEqual(str(cm.exception), "props must be a dictionary")

    def test_parent_node_to_html_no_tag(self):
        node1 = LeafNode(tag="p", value="Hello World")
        node2 = LeafNode(tag="bold", value="Hi")
        node3 = LeafNode(tag=None, value="lorem ipsum")
        children = [node1, node2, node3]

        parent_node = ParentNode(tag=None, children=children)
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "tag value cannot be None, empty or missing")

        parent_node = ParentNode(tag="", children=children)
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "tag value cannot be None, empty or missing")

    def test_parent_node_to_html_no_children(self):
        node = ParentNode(tag="body", children=None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "children value cannot be None, empty or missing")

        ParentNode(tag="body", children=[])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "children value cannot be None, empty or missing")

    def test_parent_node_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual("<div><span>child</span></div>", parent_node.to_html())

    def test_parent_node_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_to_html_with_nested_children(self):
        great_grandchild_node = LeafNode("b", "grandchild")
        grandchild_node = ParentNode("p", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>grandchild</b></p></span></div>",
        )

    def test_parent_node_to_html_with_multiple_children_and_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("i", "grandchild2")
        grandchild_node3 = LeafNode("code", "grandchild3")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2, grandchild_node3])

        grandchild_node4 = LeafNode('p', 'sample text')
        grandchild_node5 = LeafNode('a', 'sample link', {'href': 'https://boot.dev'})
        # TODO: Think of a way to handle self-closing elements
        grandchild_node6 = LeafNode(
            tag='img',
            value='',
            props={'src': 'https://boot.dev/images/sample_image.txt', 'alt': 'a sample image'},
        )
        grandchild_node7 = LeafNode(None, 'other sample text')
        child_node2 = ParentNode("div", [grandchild_node4, grandchild_node5, grandchild_node6, grandchild_node7])
        child_node3 = LeafNode(tag=None, value='raw text')
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        expecting_string = (
            '<div>'
                '<span>'
                    '<b>grandchild1</b>'
                    '<i>grandchild2</i>'
                    '<code>grandchild3</code>'
                '</span>'
                '<div>'
                    '<p>sample text</p>'
                    '<a href="https://boot.dev">sample link</a>'
                    '<img src="https://boot.dev/images/sample_image.txt" alt="a sample image"></img>'
                    'other sample text'
                '</div>'
                'raw text'
            '</div>'
        )
        self.assertEqual(parent_node.to_html(), expecting_string)


if __name__ == "__main__":
    unittest.main()
