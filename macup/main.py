from classes import FileData

starting_path = FileData("", (lambda x: True))


def traverseFileTree(base_filedata, indent=0, indent_char="-*"):
    for child in base_filedata.children:
        if child.is_directory:
            print(f"{indent_char * indent} DIRECTORY: {child.path}: {child.name}")
            traverseFileTree(child, indent + 1)
        else:
            print(f"{indent_char * indent} FILE: {child.path}: {child.name}")


traverseFileTree(starting_path)
