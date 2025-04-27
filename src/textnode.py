from enum import Enum


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
