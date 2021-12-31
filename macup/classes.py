import os


class FileData:
    """
    Stores important data about files or folders, and also generates a file tree.
    """

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.is_directory = os.path.isdir(path)
        if self.is_directory:
            # If the file is a folder, create a list of FileData objects of the files children.
            # This is done by getting the names of files in the folder, and adding the path of the current folder.
            # This results in the full path of each file in the folder, which is passed into the FileData constructor.
            # By recursively calling the FileData constructor, a file tree build of FileData classes is constructed.
            self.children = [FileData(os.path.join(path, child_name)) for child_name in os.listdir(path)]
