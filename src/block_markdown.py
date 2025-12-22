from enum import Enum

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Split a full Markdown document into block strings.

    Blocks are separated by a blank line (double newline). Each returned block is
    stripped of leading/trailing whitespace, and empty blocks are removed.
    """
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped == "":
            continue
        blocks.append(stripped)
    return blocks


def block_to_block_type(block: str) -> BlockType:
    """
    Determine the type of a single markdown block.

    Assumptions:
        - Leading/trailing whitespace is already stripped.
    """
    lines = block.split("\n")

    # heading: 1-6 '#' then space
    if block.startswith("#"):
        i = 0
        while i < len(block) and block[i] == "#":
            i += 1
        if 1 <= i <= 6 and len(block) > i and block[i] == " ":
            return BlockType.HEADING

    # code block: starts and ends with ```
    if block.startswith("```") and block.endswith("```") and len(block) >= 6:
        return BlockType.CODE

    # quote: every line starts with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # unordered list: every line starts with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ordered list: lines start with '1. ', '2. ', ... incrementing by 1
    is_ordered = True
    for idx, line in enumerate(lines, start=1):
        if not line.startswith(f"{idx}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def _text_to_children(text: str):
    """
    Convert inline-markdown text into a list of HTMLNodes.
    """
    # Inside block elements, line breaks are treated like spaces (paragraph test expects this).
    normalized = " ".join(text.split("\n"))
    text_nodes = text_to_textnodes(normalized)
    return [text_node_to_html_node(n) for n in text_nodes]


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Convert a full markdown document to a single parent HTML node (<div>...</div>).
    """
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            block_nodes.append(ParentNode("p", _text_to_children(block)))
            continue

        if block_type == BlockType.HEADING:
            i = 0
            while i < len(block) and block[i] == "#":
                i += 1
            heading_text = block[i + 1 :]  # skip required space after hashes
            block_nodes.append(ParentNode(f"h{i}", _text_to_children(heading_text)))
            continue

        if block_type == BlockType.CODE:
            # Strip the triple-backtick fences, preserve content exactly (no inline parsing).
            content = block[3:-3]
            if content.startswith("\n"):
                content = content[1:]
            code_leaf = LeafNode("code", content)
            block_nodes.append(ParentNode("pre", [code_leaf]))
            continue

        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                # remove the leading '>' and an optional following space
                line = line[1:]
                if line.startswith(" "):
                    line = line[1:]
                stripped_lines.append(line)
            quote_text = "\n".join(stripped_lines)
            block_nodes.append(ParentNode("blockquote", _text_to_children(quote_text)))
            continue

        if block_type == BlockType.UNORDERED_LIST:
            items = [line[2:] for line in block.split("\n")]  # drop "- "
            li_nodes = [ParentNode("li", _text_to_children(item)) for item in items if item != ""]
            block_nodes.append(ParentNode("ul", li_nodes))
            continue

        if block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                # split once on ". " after the number
                _, item_text = line.split(". ", 1)
                items.append(item_text)
            li_nodes = [ParentNode("li", _text_to_children(item)) for item in items if item != ""]
            block_nodes.append(ParentNode("ol", li_nodes))
            continue

        raise Exception(f"Unhandled block type: {block_type}")

    return ParentNode("div", block_nodes)

