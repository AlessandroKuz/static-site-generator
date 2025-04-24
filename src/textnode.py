from enum import Enum


class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text: str, text_type: Enum, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other: object) -> bool:
        text_is_equal = self.text == other.text
        text_type_is_equal = self.text_type.value == other.text_type.value
        url_is_equal = self.url == other.url
        return text_is_equal and text_type_is_equal and url_is_equal
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
