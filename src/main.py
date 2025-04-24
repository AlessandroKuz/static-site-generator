from textnode import TextNode, TextType


def main():
    text = 'This is some anchor text'
    text_type = TextType.LINK
    url = 'https://www.boot.dev'
    my_text_node: TextNode = TextNode(text, text_type, url)
    print(my_text_node)


if __name__ == '__main__':
    main()

