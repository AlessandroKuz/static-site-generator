import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # pattern: str = r'!\[([\w+ ]+)\]\(([\w+ :\/\/\.]+)\)'
    pattern: str = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    result: list[tuple[str, str]] = re.findall(pattern, text)
    return result

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # pattern: str = r"\[([\w+ ]+)\]\(([\w+ :\/\/\.@]+)\)"
    pattern: str = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result: list[tuple[str, str]] = re.findall(pattern, text)
    return result
