from htmlnode import *
from textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) == 1:
            new_nodes.append(node)
            continue

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, unmatched delimiter: '{delimiter}')")

        for i, part in enumerate(parts):
            if part:
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes
