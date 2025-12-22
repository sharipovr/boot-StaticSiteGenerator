import unittest

from inline_markdown import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_non_text_untouched(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_only_image(self):
        node = TextNode("![alt](url)", TextType.TEXT)
        self.assertListEqual([TextNode("alt", TextType.IMAGE, "url")], split_nodes_image([node]))

    def test_split_images_adjacent_images_no_empty_text_nodes(self):
        node = TextNode("![a](u1)![b](u2)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("a", TextType.IMAGE, "u1"), TextNode("b", TextType.IMAGE, "u2")],
            split_nodes_image([node]),
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_non_text_untouched(self):
        node = TextNode("already code", TextType.CODE)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_only_link(self):
        node = TextNode("[alt](url)", TextType.TEXT)
        self.assertListEqual([TextNode("alt", TextType.LINK, "url")], split_nodes_link([node]))

    def test_split_links_adjacent_links_no_empty_text_nodes(self):
        node = TextNode("[a](u1)[b](u2)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("a", TextType.LINK, "u1"), TextNode("b", TextType.LINK, "u2")],
            split_nodes_link([node]),
        )

    def test_split_links_does_not_treat_images_as_links(self):
        node = TextNode(
            "prefix ![img](img.png) and [link](https://example.com) suffix",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("prefix ![img](img.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" suffix", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_preserves_other_nodes(self):
        nodes = [
            TextNode("a [x](u) b", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("x", TextType.LINK, "u"),
                TextNode(" b", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            split_nodes_link(nodes),
        )


if __name__ == "__main__":
    unittest.main()


