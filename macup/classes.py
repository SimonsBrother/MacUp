import os
from macup.library import FILENAMES, PATHS, FILES, DIRECTORY, BOTH


class FileTree:
    """
    Stores important data about files or folders, and generates a file tree according to a filter provided.
    """

    def __init__(self, path, filter_=None):
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
        if self.is_directory:
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
    def __init__(self, application: str, item_type: str, whitelist: bool):
        """
        :param application: Whether the filter applies to the entire path or just the filename.
        :param item_type: Whether the filter is applied to just files, just directories, or both.
        :param whitelist:
        """
        if application not in [FILENAMES, PATHS]:  # Validate application
            raise ValueError(f"Application value must either be '{FILENAMES}' or '{PATHS}', but got '{application}'.")
        if item_type not in [FILES, DIRECTORY, BOTH]:
            raise ValueError(f"Item type value must be either '{FILES}', '{PATHS}', or '{BOTH}', but got '{item_type}'.")

        self.application = application
        self.item_type = item_type
        self.whitelist = whitelist


class RegexFilter(Filter):
    def __init__(self, regex, application: str, item_type: str, whitelist: bool):
        super().__init__(application, item_type, whitelist)
        self.regex = regex


class KeywordFilter(Filter):
    def __init__(self, keyword, application: str, item_type: str, whitelist: bool):
        super().__init__(application, item_type, whitelist)
        self.keyword = keyword
