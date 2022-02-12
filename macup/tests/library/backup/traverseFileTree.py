from macup.library.backup import traverseFileTree
from macup.classes import FileTree


def output(node):
    print(node)
    return node


print(traverseFileTree(FileTree("/macup/tests/TestDir"), dir_func=(output,),
                       use_child_as_parameter=True))
