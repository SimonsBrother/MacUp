from macup.library import traverseFileTree
from macup.classes import FileTree


def output(node):
    print(node)
    return node


print(traverseFileTree(FileTree("/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir"),
                       dir_func=(output,), use_child_as_parameter=True))
