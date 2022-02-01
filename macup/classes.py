import os


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
