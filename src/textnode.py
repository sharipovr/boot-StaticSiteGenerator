from enum import Enum

class TextType(Enum):
    # Boot.dev uses TextType.TEXT; keep PLAIN for backward compatibility.
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    PLAIN = "plain"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text_type}, {self.url})"


def text_node_to_html_node(text_node: "TextNode"):
    from leafnode import LeafNode

    text_type = text_node.text_type.value if hasattr(text_node.text_type, "value") else text_node.text_type

    if text_type in (TextType.TEXT.value, TextType.PLAIN.value):
        return LeafNode(None, text_node.text)
    if text_type == TextType.BOLD.value:
        return LeafNode("b", text_node.text)
    if text_type == TextType.ITALIC.value:
        return LeafNode("i", text_node.text)
    if text_type == TextType.CODE.value:
        return LeafNode("code", text_node.text)
    if text_type == TextType.LINK.value:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_type == TextType.IMAGE.value:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise Exception(f"Invalid text type: {text_node.text_type}")