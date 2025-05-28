import pathlib

from markdown_to_html import markdown_to_html_node
from process_markdown import extract_title


def generate_page(
        from_path: pathlib.Path | str,
        template_path: pathlib.Path | str,
        dest_path: pathlib.Path | str) -> None:
    """
    Generates an HTML page from a Markdown file.
    :param from_path: the path to the Markdown file to extract the content from.
    :param template_path: the path to the HTML template to use.
    :param dest_path: the path to the output HTML file.

    :return: None
    """
    if not (isinstance(from_path, pathlib.Path) or isinstance(from_path, str)):
        raise TypeError(f"from_path must be a pathlib.Path or str; instead got: {type(from_path)}")
    if not (isinstance(template_path, pathlib.Path) or isinstance(template_path, str)):
        raise TypeError(f"template_path must be a pathlib.Path or str; instead got: {type(template_path)}")
    if not (isinstance(dest_path, pathlib.Path) or isinstance(dest_path, str)):
        raise TypeError(f"dest_path must be a pathlib.Path or str; instead got: {type(dest_path)}")

    if isinstance(from_path, str):
        from_path = pathlib.Path(from_path)
    if isinstance(template_path, str):
        template_path = pathlib.Path(template_path)
    if isinstance(dest_path, str):
        dest_path = pathlib.Path(dest_path)

    # Check is provided paths exist and are valid
    if not from_path.exists():
        raise FileNotFoundError(f"{from_path.resolve()} does not exist")
    if not template_path.exists():
        raise FileNotFoundError(f"{template_path.resolve()} does not exist")

    if not dest_path.parent.exists():
        raise ValueError(f"{dest_path.parent.resolve()} does not exist")

    if not from_path.is_file():
        raise ValueError(f"{from_path.resolve()} is not a file")
    if not template_path.is_file():
        raise ValueError(f"{template_path.resolve()} is not a file")

    SUPPORTED_MD_EXTENSIONS = [".md", ".txt"]
    if from_path.suffix not in SUPPORTED_MD_EXTENSIONS:
        raise ValueError(
            f"{from_path.suffix} is not a markdown file; supported extensions: {','.join(SUPPORTED_MD_EXTENSIONS)}"
        )
    SUPPORTED_HTML_EXTENSIONS = ['.html', '.htm']
    if template_path.suffix not in SUPPORTED_HTML_EXTENSIONS:
        raise ValueError(
            f"{template_path.suffix} is not an HTML file; supported extensions: {','.join(SUPPORTED_HTML_EXTENSIONS)}"
        )

    # Start generating the HTML page
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as md_file:
        md_contents = md_file.read()
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    try:
        title = extract_title(template)
    except ValueError:
        title = "HTML Document"

    html = markdown_to_html_node(md_contents).to_html()

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)

    with open(dest_path, 'w') as html_file:
        html_file.write(template)

    print(f"Page generated successfully to {dest_path.resolve()}!")
