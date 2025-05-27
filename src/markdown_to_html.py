
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_text_nodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> ParentNode | None:
    """
    Convert a Markdown document to an HTML node.
    """
    markdown = markdown.strip()
    blocks: list[str] = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children_nodes.append(html_node)

    return ParentNode(tag="div", children=children_nodes)

def block_to_html_node(block: str) -> LeafNode | ParentNode:
    block_type: BlockType = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return block_to_heading_node(block)
        case BlockType.PARAGRAPH:
            return block_to_paragraph_node(block)
        case BlockType.CODE:
            return block_to_code_node(block)
        case BlockType.QUOTE:
            return block_to_quote_node(block)
        case BlockType.ORDERED_LIST:
            return block_to_ordered_list_node(block)
        case BlockType.UNORDERED_LIST:
            return block_to_unordered_list_node(block)
        case _:
            raise ValueError(f"Invalid block type: {block_type}")

def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_text_nodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes

def block_to_heading_node(block: str) -> LeafNode:
    heading_number = block.split(' ')[0].count("#")
    heading_text = block[heading_number + 1:]  # +1 to account for the space
    tag = f"h{heading_number}"
    return LeafNode(tag=tag, value=heading_text)

def block_to_paragraph_node(block: str) -> LeafNode | ParentNode:
    block = block.replace("\n", " ")
    children = text_to_children(block)
    return ParentNode(tag="p", children=children)

def block_to_code_node(block: str) -> ParentNode:
    block = block.replace("```\n", "```")
    code_text = block.split("```")[1]
    text_node = TextNode(
        text=code_text,
        text_type=TextType.CODE,
    )
    code_node = text_node_to_html_node(text_node)
    pre_code_node = ParentNode(
        tag="pre",
        children=[code_node],
    )
    return pre_code_node

def block_to_quote_node(block: str) -> ParentNode:
    quotes = block.replace('> ', '').replace('\n', ' ')
    children = text_to_children(quotes)
    return ParentNode(tag="blockquote", children=children)

def process_html_lists(block: str, splitter_particle: str) -> list[ParentNode]:
    list_elements = block.split("\n")
    list_elements = [' '.join(node.split(splitter_particle)[1:]) for node in list_elements]
    # break down any eventual italic, bold or code strings
    html_nodes = []
    for list_element in list_elements:
        children = text_to_children(list_element)
        html_nodes.append(ParentNode(tag="li", children=children))

    return html_nodes

def block_to_ordered_list_node(block: str) -> ParentNode:
    list_nodes = process_html_lists(block, splitter_particle=". ")
    return ParentNode(tag="ol", children=list_nodes)

def block_to_unordered_list_node(block: str) -> ParentNode:
    list_nodes = process_html_lists(block, splitter_particle="- ")
    return ParentNode(tag="ul", children=list_nodes)
