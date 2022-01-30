from macup.library import traverseFileTree
from macup.classes import FileTree


def return_true(node):
    return True


def output(node):
    print(node)
    return node


print(traverseFileTree(FileTree("",
                                filter_=return_true), dir_func=(output,), use_child_as_parameter=True))
