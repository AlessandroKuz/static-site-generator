class HTMLNode:
    def __init__(
            self, tag: str | None = None,
            value: str | None = None,
            children: list["HTMLNode"] | None = None,
            props: dict[str, str] | None = None) -> None:
        if tag is not None and not isinstance(tag, str):
            raise TypeError("tag must be a string")
        if value is not None and not isinstance(value, str):
            raise TypeError("value must be a string")
        if children is not None and not isinstance(children, list):
            raise TypeError("children must be a list")
        if props is not None and not isinstance(props, dict):
            raise TypeError("props must be a dictionary")

        self.tag: str = tag
        self.value: str = value
        self.children: list["HTMLNode"] = children
        self.props: dict[str, str] = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        attrs_string = ''.join([f' {key}="{val}"' for key, val in self.props.items() if key and val])
        return attrs_string

    def __eq__(self, other: "HTMLNode") -> bool:
        tag_is_equal = self.tag == other.tag
        value_is_equal = self.value == other.value
        children_is_equal = self.children == other.children
        props_is_equal = self.props == other.props
        return tag_is_equal and value_is_equal and children_is_equal and props_is_equal

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        if tag == '':
            tag = None
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("value can't be empty. All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

