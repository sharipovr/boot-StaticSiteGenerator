import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_quote_and_lists_smoke(self):
        md = """
# Hello **world**

> a quote line
> and _another_

- first
- second with a [link](https://example.com)

1. one
2. two
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><h1>Hello <b>world</b></h1><blockquote>a quote line and <i>another</i></blockquote><ul><li>first</li><li>second with a <a href="https://example.com">link</a></li></ul><ol><li>one</li><li>two</li></ol></div>',
        )


if __name__ == "__main__":
    unittest.main()


