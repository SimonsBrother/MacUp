import os


class FileData:
    """
    Stores important data about files or folders, and generates a file tree according to a filter provided.
    """

    def __init__(self, path, filter_):
        """
        :param path: The full path of a folder or file.
        :param filter_: A function that returns a boolean result if a path matches a certain criteria.
        """
        self.path = path
        self.name = os.path.basename(path)
        self.is_directory = os.path.isdir(path)
        self.children = []
        if self.is_directory:
            # If the file is a folder, create a list of FileData objects of the files children.
            # This is done by getting the names of files in the folder, and adding the path of the current folder.
            # This results in the full path of each file in the folder.
            child_paths = [os.path.join(path, child_name) for child_name in os.listdir(path)]

            # By filtering the paths to be used according to a function, files can be whitelisted or blacklisted.
            for child_path in child_paths:
                if filter_(child_path):
                    # By recursively calling the FileData constructor, a file tree made of FileData classes is built.
                    self.children.append(FileData(child_path, filter_))
