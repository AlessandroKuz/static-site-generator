import sys

from copystatic import copy_files_recursively
from generate_html import generate_pages_recursive


def main(basepath: str = '/') -> None:
    src = "static"
    dst = "docs"
    verbose = False
    copy_files_recursively(src, dst, verbose=verbose)
    from_path = "content"
    template_path = "template.html"
    generate_pages_recursive(from_path, template_path, dst, basepath)

if __name__ == "__main__":
    main(sys.argv[0])
