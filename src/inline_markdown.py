import re

from textnode import TextNode, TextType


ALLOWED_DELIMITERS = {'**': TextType.BOLD, '*': TextType.ITALIC, '_': TextType.ITALIC, '```': TextType.CODE, '`': TextType.CODE}

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

    if delimiter not in ALLOWED_DELIMITERS.keys():
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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern: str = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    result: list[tuple[str, str]] = re.findall(pattern, text)
    return result

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern: str = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result: list[tuple[str, str]] = re.findall(pattern, text)
    return result

def process_split(old_nodes: list, node_type: str) -> list[TextNode]:
    if not isinstance(old_nodes, list):
        raise ValueError("provided old_nodes is not of type list")
    new_nodes = []
    match node_type:
        case "image":
            text_type = TextType.IMAGE
            exception_msg = "invalid markdown, image section not closed"
            extraction_func = extract_markdown_images
        case "link":
            text_type = TextType.LINK
            exception_msg = "invalid markdown, link section not closed"
            extraction_func = extract_markdown_links
        case _:
            raise ValueError("invalid node type")

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise ValueError(f"an old_nodes list element is not of valid type (TextNode), instead got {type(old_node)}")
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        extraction_tuple = extraction_func(original_text)
        if not extraction_tuple:
            new_nodes.append(old_node)
            continue

        for extraction_alt, extraction_link in extraction_tuple:
            split_pattern = f'{"!" if node_type == "image" else ""}[{extraction_alt}]({extraction_link})'
            sections = original_text.split(split_pattern, 1)
            if len(sections) != 2:
                raise ValueError(exception_msg)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], old_node.text_type))
            new_nodes.append(TextNode(extraction_alt, text_type, extraction_link))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes: list) -> list[TextNode]:
    return process_split(old_nodes, "image")

def split_nodes_link(old_nodes: list) -> list[TextNode]:
    return process_split(old_nodes, "link")

def text_to_text_nodes(text: str) -> list[TextNode]:
    if not isinstance(text, str):
        raise ValueError(f"provide text has invalid type, found {type(text)} instead of str")
    if not text:
        return []
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    images_are_present = len(extract_markdown_images(text)) > 0
    links_are_present = len(extract_markdown_links(text)) > 0

    if images_are_present:
        nodes = split_nodes_image(nodes)

    if links_are_present:
        nodes = split_nodes_link(nodes)
    
    for delimiter, text_type in ALLOWED_DELIMITERS.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    
    return nodes
