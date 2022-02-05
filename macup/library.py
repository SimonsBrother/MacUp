import os
import re
import shutil

DIRECTORY = 'DIRECTORY'
FILES = 'FILES'
BOTH = 'BOTH'


def traverseFileTree(ft_node, dir_func=tuple(), file_func=tuple(), use_child_as_parameter=False):
    """
    Traverses a FileTree and performs a function to each node.

    :param use_child_as_parameter: Boolean that indicates whether the child variable should be passed into functions.
    :param ft_node: A FileTree object, from which to traverse.
    :param dir_func: A tuple in the format tuple(function, tuple(parameters)). Applies to directories (and files if one
     is not supplied for them).
    :param file_func: A tuple in the format tuple(function, tuple(parameters)). Applies to files (and directories if one
     is not supplied for them).
    """

    if not (dir_func or file_func):
        raise ValueError("Both function parameters cannot be empty.")

    output = []
    for child in ft_node.children:

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


def getAll(type_, ft_node):
    """
    Returns a list of directories or files, depending on type, contained in a directory and their descendants.

    :param type_: FILES or DIRECTORY
    :param ft_node: A FileTree node to work from
    :return: All the FileTree nodes of the type_ in and under the filetree provided
    """

    def checkIfItem(ft):
        if type_ == DIRECTORY and ft.is_directory:
            return ft
        elif type_ == FILES and not ft.is_directory:
            return ft

    # Will contain None values
    unfiltered_items = traverseFileTree(ft_node, dir_func=(checkIfItem,), use_child_as_parameter=True)

    # Removes None values
    items = list(filter(lambda item: item is not None, unfiltered_items))
    return items


def graftItem(item_path, source, target):
    """
    Removes the source part from an item path, and concatenates it onto target
    :param item_path: The file/directory to be grafted from source directory to target directory
    :param source: The source directory
    :param target: The target directory
    :return: The grafted directory
    """

    match = re.match(str(source) + r'(.*)', str(item_path))
    truncated_item_path = match.group(1)  # Contains the directory without the source
    return str(target) + truncated_item_path


def buildDirectories(directories):
    """
    Ensures all the directories are present, adding ones that are not.

    :param directories: Collection of directories to make/check
    :return: Nothing
    """

    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def copyFiles(files, source, target, overwrite):
    """
    Copies the files to the target directory, checking if they already exist, overwriting them if told to.

    :param source: Source directory; note, this is not the directory the files are in, but the directory from which
    the backup originates from
    :param overwrite: Boolean value to overwrite already present files or not
    :param target: Target directory to which files will be copied
    :param files: Collection of file paths to be copied
    :return:
    """
    # Generate the new locations for each file
    new_file_paths = [graftItem(file, source, target) for file in files]

    # Copy files
    for i, new_file_path in enumerate(new_file_paths):
        if (not os.path.isfile(new_file_path)) or overwrite:  # If file doesn't exist or overwrite is true:
            shutil.copy(files[i], new_file_path)


def regexFilter(regexes, path):
    """
    Checks whether a certain FileTree node satisfies all the regular expressions provided.

    :param regexes: An iterable container containing regular expressions for the item name
    :param path: A FileTree node, who's file name will be compared against the regexes
    :return: True if the node path satisfies the regexes, False otherwise
    """
    # For every regular expression, apply it against the node's filename, then check they all return True
    filename = os.path.basename(path)
    return all([re.match(regex, filename) for regex in regexes])


def containsFilter(keywords, path):
    """
    Checks that a FileTree node contains all the keywords provided.
    This option is if the user does not know how to manipulate regexes.

    :param keywords: An iterable container of strings with which to ensure each is 'in' ft_node's filename
    :param path: A FileTree node
    :return: True if the node contains all the keywords, False otherwise
    """
    filename = os.path.basename(path)
    return all([keyword in filename for keyword in keywords])


def buildFilter(regexes, keywords, whitelist):
    """
    Builds the filter function to be passed to FileTree nodes; the filter function has to have one parameter.

    :param whitelist: If true, items fitting the filter are included, else discarded
    :param regexes: The regexes supplied by the user
    :param keywords: The keywords supplied by the user
    :return: filter function
    """

    def filter_(path):
        fits_filter = regexFilter(regexes, path) and containsFilter(keywords, path)

        if whitelist:
            return fits_filter
        else:
            return not fits_filter

    return filter_
