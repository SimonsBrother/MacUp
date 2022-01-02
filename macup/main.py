from macup.library import traverseFileTree
from macup.classes import FileData

starting_path = FileData("", (lambda x: True))


def printDir(fileData):
    print(f"DIRECTORY>>> {fileData.path}")


def printFile(fileData):
    print(f"FILE>>> {fileData.path}")


traverseFileTree(starting_path, dir_func=(printDir,), file_func=(printFile,), use_child_as_parameter=True)
