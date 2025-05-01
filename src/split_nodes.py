
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list[TextNode | None]:
    """
    At the moment the function does not support nested inline elements.
    TODO: Implement nested inline handling.

    :param old_nodes:
    :param delimiter:
    :param text_type:
    :return:
    """
    new_nodes = []

    if delimiter not in ['**', '*', '_', '```', '`']:
        raise ValueError(f'provided delimiter "{delimiter}" is not supported.')

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError(f'provided old_nodes contains an invalid Markdown syntax, the number of "{delimiter}" delimiters is odd.')

        node = old_node.text.split(delimiter)
        nodes = []

        if len(node) == 1:
            nodes.append(TextNode(node[0], old_node.text_type))
        elif (len(node) - 3) % 2 == 0:
            for i in range(0, len(node)):
                if i % 2 == 0:
                    nodes.append(TextNode(node[i], old_node.text_type))
                else:
                    nodes.append(TextNode(node[i], text_type))
        else:
            raise ValueError("Invalid node sequence length.")
        new_nodes.extend(nodes)

    return new_nodes

