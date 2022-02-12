import macup.library.backup as mul
from macup.library.classes import FileTree


testdir = FileTree("/macup/tests/TestDir")
target = "/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder3/Sub Folder 2"

directories_to_copy = [mul.graftItem(directory.path, testdir.path, target) for directory in
                       mul.getAll(mul.DIRECTORY, testdir)]

mul.buildDirectories(directories_to_copy)
