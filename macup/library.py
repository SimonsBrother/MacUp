
def traverseFileTree(fileData, dir_func=tuple(), file_func=tuple()):
    """
    Traverses a FileData file tree and performs a function to each one.

    :param fileData: A FileData object, from which to traverse.
    :param dir_func: A tuple in the format tuple(function, tuple(parameters)). Applies to directories (and files if one
     is not supplied for them).
    :param file_func: A tuple in the format tuple(function, tuple(parameters)). Applies to files (and directories if one
     is not supplied for them).
    """

    if dir_func or file_func:  # Ensure at least one of the function parameters are filled
        for child in fileData.children:

            if child.is_directory:  # Directory logic
                if dir_func:
                    dir_func[0](*dir_func[1])  # Call function and unpack and pass parameters
                else:
                    file_func[0](*file_func[1])
                traverseFileTree(child)

            else:  # File logic
                if file_func:
                    file_func[0](*file_func[1])
                else:
                    dir_func[0](*dir_func[1])
