import re


def markdown_to_blocks(markdown: str) -> list[str]:
    normalized_markdown = re.sub(r'[\t ]+\n', '\n', markdown)
    normalized_markdown = re.sub(r'\n{2,}', '\n\n', normalized_markdown)
    blocks: list[str] = normalized_markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks
