import os
from macup.library.constants import *


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

    def __init__(self, application: str, item_type: str, whitelist: bool, name=""):
        """
        :param application: Whether the filter applies to the entire path or just the filename.
        :param item_type: Whether the filter is applied to just files, just directories, or both.
        :param whitelist:
        """
        if application != FILENAMES and application != PATHS:  # Validate application
            raise ValueError(f"application value must either be '{FILENAMES}' or '{PATHS}', but got '{application}'.")
        if item_type != FILES and item_type != DIRECTORY and item_type != BOTH:
            raise ValueError(
                f"item_type value must be either '{FILES}', '{DIRECTORY}', or '{BOTH}', but got '{item_type}'.")

        self.name = name
        self.application = application
        self.item_type = item_type
        self.whitelist = whitelist

    def __repr__(self):
        return f"Filter(name='{self.name}', application='{self.application}'," \
               f" item_type='{self.item_type}', whitelist={self.whitelist})"


class RegexFilter(Filter):
    def __init__(self, regex, application: str, item_type: str, whitelist: bool, name=""):
        super().__init__(application, item_type, bool(whitelist), name)
        self.regex = regex

    def __repr__(self):
        return f"RegexFilter(name='{self.name}', application='{self.application}'," \
               f" item_type='{self.item_type}', whitelist={self.whitelist}, regex='{self.regex}')"


class KeywordFilter(Filter):
    def __init__(self, keyword, application: str, item_type: str, whitelist: bool, name=""):
        super().__init__(application, item_type, bool(whitelist), name)
        self.keyword = keyword

    def __repr__(self):
        return f"KeywordFilter(name='{self.name}', application='{self.application}'," \
               f" item_type='{self.item_type}', whitelist={self.whitelist}, keyword='{self.keyword}')"


class Configuration:
    """
    A class to store configuration data from a json file.
    """

    def __init__(self, name, source_dir, target_dir, regex_filters, keyword_filters, overwrite):
        """
        :param regex_filters: Either: a list of dicts, each containing data to make a RegexFilter
                or a list of RegexFilter objects.
        :param keyword_filters: Either: a list of dicts, each containing data to make a KeywordFilter,
                or a list of KeywordFilter objects.
                The filters are converted to their object if they are supplied as a dictionary.
        """

        self.name = name
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.overwrite = overwrite

        # Regex filters
        if not regex_filters:
            # If empty list
            self.regex_filters = []

        elif isinstance(regex_filters[0], RegexFilter):
            # If filters are objects
            self.regex_filters = regex_filters

        else:
            # If filters are dicts
            self.regex_filters = []
            # Parse regex filters, populate regex_filters
            for regex_filter in regex_filters:
                self.regex_filters.append(RegexFilter(regex_filter["regex"], regex_filter["application"],
                                                      regex_filter["item_type"], regex_filter["whitelist"],
                                                      regex_filter["name"]))

        # Keyword filters
        if not keyword_filters:
            # If empty list
            self.keyword_filters = []

        elif isinstance(keyword_filters[0], KeywordFilter):
            # If filters are objects
            self.keyword_filters = keyword_filters

        else:
            # If filters are dicts
            self.keyword_filters = []
            # Parse keyword filters, populate keyword_filters
            for keyword_filter in keyword_filters:
                self.keyword_filters.append(KeywordFilter(keyword_filter["keyword"], keyword_filter["application"],
                                                          keyword_filter["item_type"], keyword_filter["whitelist"],
                                                          keyword_filter["name"]))

    def __repr__(self):
        return f"Configuration(name='{self.name}', source_dir='{self.source_dir}', target_dir='{self.target_dir}', " \
               f"regex_filters={self.regex_filters}, keyword_filters={self.keyword_filters})"
