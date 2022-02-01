from macup.library import getAllDirectories
from macup.classes import FileTree


def return_true(node):
    return True


print(getAllDirectories(FileTree("",
                                 filter_=return_true)))
