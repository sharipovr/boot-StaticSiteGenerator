from textnode import TextNode, TextType


def _text_type_value(text_type) -> str:
    return text_type.value if hasattr(text_type, "value") else text_type


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextType.TEXT nodes by a markdown delimiter into alternating TextNodes.

    Example:
        TextNode("a `b` c", TextType.TEXT) with delimiter="`" and text_type=TextType.CODE
        becomes: [TextNode("a ", TEXT), TextNode("b", CODE), TextNode(" c", TEXT)]
    """
    if delimiter is None or delimiter == "":
        raise ValueError("delimiter must be a non-empty string")

    new_nodes = []
    for node in old_nodes:
        node_type = _text_type_value(node.text_type)
        if node_type not in (TextType.TEXT.value, TextType.PLAIN.value):
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(
                f"Invalid markdown syntax: missing closing delimiter '{delimiter}' in '{node.text}'"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


