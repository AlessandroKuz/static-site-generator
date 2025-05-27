import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
    def test_headings(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1></div>"
        self.assertEqual(html, expected)

        md = "## Heading 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h2>Heading 2</h2></div>"
        self.assertEqual(html, expected)

        md = "### Heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h3>Heading 3</h3></div>"
        self.assertEqual(html, expected)

        md = "#### Heading 4"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h4>Heading 4</h4></div>"
        self.assertEqual(html, expected)

        md = "##### Heading 5"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h5>Heading 5</h5></div>"
        self.assertEqual(html, expected)

        md = "###### Heading 6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected)

        # Extra test for weird but valid heading
        md = "### Heading 3 # with extra #"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h3>Heading 3 # with extra #</h3></div>"
        self.assertEqual(html, expected)

        # Extra test to make sure that headings >6 become paragraphs
        md = "####### Heading 7"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>####### Heading 7</p></div>"
        self.assertEqual(html, expected)

        # Mixed tag test
        md = """
        # this is an h1

        this is paragraph text

        ## this is an h2
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** __paragraph__
text in a p
tag here

This is another *paragraph* with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = ("<div><p>This is <b>bolded</b> <b>paragraph</b> text in a p tag here</p>"
                    "<p>This is another <i>paragraph</i> with <i>italic</i> text and <code>code</code> here</p></div>")
        self.assertEqual(html, expected)

    # test paragraphs with links and images
        md = """
This is an ![image](https://sample.com/image.png) paragraph
text in a p tag

This is another paragraph with a link to an [external website](https://www.test.com).

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = ('<div><p>This is an <img src="https://sample.com/image.png" alt="image"></img> paragraph text in a p tag</p>'
                    '<p>This is another paragraph with a link to an <a href="https://www.test.com">external website</a>.</p></div>')
        self.assertEqual(html, expected)



    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(html, expected)

    def test_quote(self):
        md = """
> This is a quote
> This is another quote
> This is a third quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote This is another quote This is a third quote</blockquote></div>"
        self.assertEqual(html, expected)

        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = """
1. This is an ordered list
2. This is the second item
3. This is the third item
4. This is the fourth item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>This is an ordered list</li><li>This is the second item</li><li>This is the third item</li><li>This is the fourth item</li></ol></div>"
        self.assertEqual(html, expected)

    def test_unordered_list(self):
        md = """
- This is an unordered list
- This is the second item
- This is the third item
- This is the fourth item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>This is an unordered list</li><li>This is the second item</li><li>This is the third item</li><li>This is the fourth item</li></ul></div>"
        self.assertEqual(html, expected)

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and **more** items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = ("<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol>"
                    "<li>This is an <code>ordered</code> list</li><li>with items</li><li>and <b>more</b> items</li></ol></div>")
        self.assertEqual(html, expected)

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "children value cannot be None, empty or missing")


    def test_sample_markdown_document(self):
        md = """
# Heading 1

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
This is text that _should_ remain
the **same** even with inline stuff
```

## Heading 2

> This is a quote
> This is another quote
> This is a third quote

1. This is an ordered list
2. This is the second item
3. This is the **third** item
4. This is the fourth item

### Heading 3

- This is an unordered list
- This is the `second` item
- This is the third item
- This is the _fourth_ item



"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_heading_node = "<h1>Heading 1</h1>"
        expected_text_node = ("<p>This is <b>bolded</b> paragraph text in a p tag here</p>"
                              "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>")
        expected_code_node = "<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre>"
        expected_heading2_node = "<h2>Heading 2</h2>"
        expected_quote_node = "<blockquote>This is a quote This is another quote This is a third quote</blockquote>"
        expected_ordered_list_node = ("<ol><li>This is an ordered list</li><li>This is the second item</li>"
                                      "<li>This is the <b>third</b> item</li><li>This is the fourth item</li></ol>")
        expected_heading3_node = "<h3>Heading 3</h3>"
        expected_unordered_list_node = ("<ul><li>This is an unordered list</li><li>This is the <code>second</code> item</li>"
                                        "<li>This is the third item</li><li>This is the <i>fourth</i> item</li></ul>")
        join_list = [
            expected_heading_node,
            expected_text_node,
            expected_code_node,
            expected_heading2_node,
            expected_quote_node,
            expected_ordered_list_node,
            expected_heading3_node,
            expected_unordered_list_node,
        ]
        expected_final_text = "".join(join_list)
        expected_final_node = f"<div>{expected_final_text}</div>"

        self.assertEqual(html, expected_final_node)




if __name__ == '__main__':
    unittest.main()
 
