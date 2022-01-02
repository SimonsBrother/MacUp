
def traverseFileTree(fileData, dir_func=tuple(), file_func=tuple(), use_child_as_parameter=False):
    """
    Traverses a FileData file tree and performs a function to each one.

    :param use_child_as_parameter: Boolean that indicates whether the child variable should be passed into functions.
    :param fileData: A FileData object, from which to traverse.
    :param dir_func: A tuple in the format tuple(function, tuple(parameters)). Applies to directories (and files if one
     is not supplied for them).
    :param file_func: A tuple in the format tuple(function, tuple(parameters)). Applies to files (and directories if one
     is not supplied for them).
    """

    if not (dir_func or file_func):
        raise ValueError("Both function parameters cannot be empty.")

    for child in fileData.children:

        if child.is_directory:  # Decides which function should be used
            function = dir_func if dir_func else file_func
        else:
            function = file_func if file_func else dir_func

        if use_child_as_parameter:  # Executes the function, handling what parameter is passed
            function[0](child)
        else:
            function[0](*function[1])

        if child.is_directory:  # The recursion must go on!
            traverseFileTree(child, dir_func, file_func, use_child_as_parameter)
