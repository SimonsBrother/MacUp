
def traverseFileTree(file_tree, dir_func=tuple(), file_func=tuple(), use_child_as_parameter=False):
    """
    Traverses a FileTree and performs a function to each node.

    :param use_child_as_parameter: Boolean that indicates whether the child variable should be passed into functions.
    :param file_tree: A FileTree object, from which to traverse.
    :param dir_func: A tuple in the format tuple(function, tuple(parameters)). Applies to directories (and files if one
     is not supplied for them).
    :param file_func: A tuple in the format tuple(function, tuple(parameters)). Applies to files (and directories if one
     is not supplied for them).
    """

    if not (dir_func or file_func):
        raise ValueError("Both function parameters cannot be empty.")

    output = []
    for child in file_tree.children:

        if child.is_directory:  # Decides which function should be used
            function = dir_func if dir_func else file_func
        else:
            function = file_func if file_func else dir_func

        if use_child_as_parameter:  # Executes the function, handling what parameter is passed
            return_val = function[0](child)
        else:
            return_val = function[0](*function[1])

        output.append(return_val)

        if child.is_directory:  # The recursion must go on!
            output += traverseFileTree(child, dir_func, file_func, use_child_as_parameter)

    return output


def getAllDirectories(file_tree):
    """
    Returns a list of directories contained in a directory and their descendants.

    :param file_tree: A FileTree node to work from
    :return: All the directories in and under the filetree provided
    """

    def checkIfDirectory(fd):
        if fd.is_directory:
            return fd.path

    list_of_dirs = traverseFileTree(file_tree, dir_func=(checkIfDirectory,), use_child_as_parameter=True)

    dirs = list(filter(lambda dir_: dir_ is not None, list_of_dirs))
    return dirs
