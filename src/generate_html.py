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
        dest_path.parent.mkdir(parents=True, exist_ok=True)

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

def generate_pages_recursive(
        dir_path_content: pathlib.Path | str,
        template_path: pathlib.Path | str,
        dest_dir_path: pathlib.Path | str) -> None:
    """

    :param dir_path_content: the path of the directory containing the Markdown files.
    :param template_path: the path to the HTML template to use.
    :param dest_dir_path: the path to the output HTML files.

    :return: None
    """
    if not (isinstance(dir_path_content, pathlib.Path) or isinstance(dir_path_content, str)):
        raise TypeError(f"dir_path_content must be a pathlib.Path or str; instead got: {type(dir_path_content)}")
    if not (isinstance(template_path, pathlib.Path) or isinstance(template_path, str)):
        raise TypeError(f"template_path must be a pathlib.Path or str; instead got: {type(template_path)}")
    if not (isinstance(dest_dir_path, pathlib.Path) or isinstance(dest_dir_path, str)):
        raise TypeError(f"dest_dir_path must be a pathlib.Path or str; instead got: {type(dest_dir_path)}")

    if isinstance(dir_path_content, str):
        dir_path_content = pathlib.Path(dir_path_content)
    if isinstance(template_path, str):
        template_path = pathlib.Path(template_path)
    if isinstance(dest_dir_path, str):
        dest_dir_path = pathlib.Path(dest_dir_path)

    # Check is provided paths exist and are valid
    if not dir_path_content.exists():
        raise FileNotFoundError(f"{dir_path_content.resolve()} does not exist")
    if not template_path.exists():
        raise FileNotFoundError(f"{template_path.resolve()} does not exist")

    if not dest_dir_path.exists():
        dest_dir_path.mkdir(parents=True, exist_ok=True)

    if dir_path_content.is_file():
        raise ValueError(f"{dir_path_content.resolve()} is a file")
    if not template_path.is_file():
        raise ValueError(f"{template_path.resolve()} is not a file")

    SUPPORTED_HTML_EXTENSIONS = ['.html', '.htm']
    if template_path.suffix not in SUPPORTED_HTML_EXTENSIONS:
        raise ValueError(
            f"{template_path.suffix} is not an HTML file; supported extensions: {','.join(SUPPORTED_HTML_EXTENSIONS)}"
        )

    # Start generating the HTML page
    print(f"Generating all pages from {dir_path_content} to {dest_dir_path} using {template_path}")

    for item in dir_path_content.iterdir():
        if item.is_file():
            dest_path = f"{dest_dir_path}/{item.stem}{template_path.suffix}"
            generate_page(item, template_path, dest_path)
        else:
            new_dest_dir_path = dest_dir_path / item.name
            generate_pages_recursive(item, template_path, new_dest_dir_path)

    print(f"All pages generated successfully to {dest_dir_path.resolve()}!")
