from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    normalized_markdown = re.sub(r'[\t ]+\n', '\n', markdown)
    normalized_markdown = re.sub(r'\n{2,}', '\n\n', normalized_markdown)
    blocks: list[str] = normalized_markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def extract_number(line: str) -> int | None:
    match = re.match(r'^(\d+)\.', line)
    if match:
        return int(match.group(1))
    return None

def block_to_block_type(markdown_block: str) -> BlockType:
    lines = markdown_block.split('\n')

    is_ordered_list = True
    # TODO: at the end of the project update this value to -1 to allow 0. as a start for a ordered list -> update the related html generation code
    previous_num = 0
    for line in lines:
        number: int | None = extract_number(line)
        if number is None or number < previous_num or number != (previous_num + 1):
            is_ordered_list = False
            break  # if no number, list doesnt start with 0, or doesnt go up by one each line, then it is not a valid ordered list
        previous_num += 1
    if re.findall(r'^#{1,6} .*', lines[0]):
        return BlockType.HEADING
    elif len(lines) > 1 and markdown_block.startswith('```') and markdown_block.endswith('```'):
        return BlockType.CODE
    elif all([line.startswith('>') for line in lines]):
        return BlockType.QUOTE
    elif all([line.startswith('- ') for line in lines]):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
