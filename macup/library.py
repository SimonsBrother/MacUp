import os
import re


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


def graftDirectory(location, source, target):
    """
    Removes the source part from the directory, and concatenates it onto target
    :param location: The file/directory to be grafted from source directory to target directory
    :param source: The source directory
    :param target: The target directory
    :return: The grafted directory
    """

    truncated_dir = re.match(str(source) + r'(.*)', str(location)).group(1)  # Contains the directory without the source
    return str(target) + truncated_dir


def buildDirectories(directories):
    """
    Ensures all the directories are present, adding ones that are not.

    :param directories: Collection of directories to make/check
    :return: Nothing
    """

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
