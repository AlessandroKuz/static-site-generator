from copystatic import copy_files_recursively
from generate_html import generate_pages_recursive


def main():
    src = "static"
    dst = "public"
    verbose = False
    copy_files_recursively(src, dst, verbose=verbose)
    from_path = "content"
    template_path = "template.html"
    dest_path = "public"
    generate_pages_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
