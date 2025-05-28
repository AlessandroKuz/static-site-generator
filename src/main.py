from copystatic import copy_files_recursively
from generate_html import generate_page


def main():
    src = 'static'
    dst = 'public'
    verbose = False
    copy_files_recursively(src, dst, verbose=verbose)
    from_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/index.html"
    generate_page(from_path, template_path, dest_path)

if __name__ == '__main__':
    main()
