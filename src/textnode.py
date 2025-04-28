from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        if not isinstance(text, str):
            raise TypeError('text must be a string')
        if not isinstance(text_type, TextType):
            raise TypeError('text_type must be a TextType')
        if url is not None and not isinstance(url, str):
            raise TypeError('url must be a string')

        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str = url
    
    def __eq__(self, other: "TextNode") -> bool:
        text_is_equal = self.text == other.text
        text_type_is_equal = self.text_type.value == other.text_type.value
        url_is_equal = self.url == other.url
        return text_is_equal and text_type_is_equal and url_is_equal
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    value = text_node.text
    props = None
    match text_node.text_type:
        case TextType.TEXT:
            tag = None
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props = {'href': text_node.url}
        case TextType.IMAGE:
            tag = "img"
            value = ''
            props = {'src': text_node.url, 'alt': text_node.text}
        case _:
            raise ValueError(f'Invalid TextNode type: {text_node.text_type}')
    node: LeafNode = LeafNode(tag=tag, value=value, props=props)
    return node
