import os
from macup.library.constants import *
from macup.library.filter import parseDictToFilter

class FileTree:
    """
    Stores important data about files or folders, and generates a file tree according to a filter provided.
    """

    def __init__(self, path, filter_=None, do_recursion=True):
        """
        :param path: The full path of a folder or file.
        :param filter_: A function that returns a boolean result if a path matches a certain criteria. All values are
        returned if left empty or passed None.
        """

        self.path = os.path.abspath(path)
        self.name = os.path.basename(path)
        self.is_directory = os.path.isdir(path)
        self.children = []
        self.filter = filter_
        if self.is_directory and do_recursion:
            # If the file is a folder, create a list of FileTree objects of the files children.
            # This is done by getting the names of files in the folder, and adding the path of the current folder.
            # This results in the full path of each file in the folder.
            child_paths = [os.path.join(path, child_name) for child_name in os.listdir(path)]

            # By filtering the paths to be used according to a function, files can be whitelisted or blacklisted.
            for child_path in child_paths:
                # If filter_ is None, the clause shorts, so filter_ is not called
                if filter_ is None or filter_(child_path):
                    # By recursively calling the FileTree constructor, a file tree made of FileTree classes is built.
                    self.children.append(FileTree(child_path, filter_))

    def __repr__(self):
        return f"{self.__class__.__name__}(path={self.path}, filter_={self.filter.__name__ if self.filter else None})"


class Filter:
    """
    Stores filter data.
    """

    def __init__(self, name: str, filter_type: str, data: str, application: str, item_type: str, whitelist: bool):
        """
        :param name: The name of the filter
        :param filter_type: The type of the filter (a constant from "library.constants")
        :param data: The data for the filter
        :param application: Whether the filter applies to the entire path or just the filename (a constant)
        :param item_type: Whether the filter is applied to just files, just directories, or both (a constant)
        :param whitelist: True means the file is to be copied if it matches this filter
        """

        # Validate filter type
        valid_filter_types = (REGEX, KEYWORD)
        if filter_type not in valid_filter_types:
            raise ValueError(f"application value must be one of {valid_filter_types}, but got '{filter_type}'.")

        # Validate application
        valid_applications = (FILENAMES, PATHS)
        if application not in valid_applications:
            raise ValueError(f"application value must be one of {valid_applications}, but got '{application}'.")

        # Validate item type
        valid_item_types = (FILES, DIRECTORY, BOTH)
        if item_type not in valid_item_types:
            raise ValueError(f"item_type value must be one of {valid_item_types}, but got '{item_type}'.")

        self.name = str(name)
        self.filter_type = filter_type
        self.data = str(data)
        self.application = application
        self.item_type = item_type
        self.whitelist = bool(whitelist)

    def __repr__(self):
        return f"Filter(name='{self.name}', filter_type='{self.filter_type}', data='{self.data}', " \
               f"application='{self.application}', item_type='{self.item_type}', whitelist='{self.whitelist}')"


class Configuration:
    """
    A class to store configuration data from a json file.
    """

    def __init__(self, name: str, source_dir: str, target_dir: str, filters, overwrite: bool):
        """
        :param name: Name of configuration
        :param source_dir: Directory to copy items from
        :param target_dir: Directory to copy items to
        :param filters: List of Filter objects or dicts representing filters
        :param overwrite: Whether or not to overwrite already existing files
        """

        self.name = name
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.overwrite = overwrite

        # Filters
        # If there are no filters
        if not filters:
            self.filters = []
        # Else, make sure the first is a Filter object or dict
        elif isinstance(filters[0], Filter):
            self.filters = filters
        elif isinstance(filters[0], dict):
            self.filters = [parseDictToFilter(dict_filter) for dict_filter in filters]
        else:
            raise ValueError(f"Filters must be a list of objects or a list of dicts, not {type(filters[0])}")

    def __repr__(self):
        return f"Configuration(name='{self.name}', source_dir='{self.source_dir}', target_dir='{self.target_dir}', " \
               f"keyword_filters={self.filters}, overwrite={self.overwrite})"
