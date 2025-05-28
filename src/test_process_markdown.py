import unittest

from process_markdown import extract_title


class TestMarkdownToHtml(unittest.TestCase):
    def test_valid_heading_first_line(self):
        md = """
# Heading 1

This is **bolded** paragraph
text in a p
tag here
"""

        title = extract_title(md)
        self.assertEqual(title, 'Heading 1')

    def test_valid_heading(self):
        md = """

This is **bolded** paragraph

# Heading 1

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

        title = extract_title(md)
        self.assertEqual(title, 'Heading 1')

    def test_missing_heading(self):
        md = """

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

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

        # self.assertRaises(ValueError, extract_title, md)
        with self.assertRaises(ValueError) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), 'No title found in the Markdown document')



if __name__ == '__main__':
    unittest.main()

