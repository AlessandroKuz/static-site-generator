from copystatic import copy_files_recursively


def main():
    src = 'static'
    dst = 'public'
    copy_files_recursively(src, dst, verbose=True)

if __name__ == '__main__':
    main()
