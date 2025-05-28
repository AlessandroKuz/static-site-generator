

def extract_title(markdown: str) -> str:
    """
    Extracts the title of a Markdown file.
    :param markdown: the Markdown document from which to extract the title.

    :return: the extracted title.
    """
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith('# '):
            title: str = line[2:]
            return title
    raise ValueError('No title found in the Markdown document')
