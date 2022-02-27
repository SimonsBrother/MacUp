from macup.library.backup import traverseFileTree
from macup.library.classes import FileTree


def output(node):
    print(node)
    return node


print(traverseFileTree(FileTree("/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir"), dir_func=(output,),
                       use_child_as_parameter=True))
