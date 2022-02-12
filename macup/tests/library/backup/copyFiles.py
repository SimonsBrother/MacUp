import macup.library.backup as mul
from macup.classes import FileTree


testdir = FileTree("/macup/tests/TestDir/Folder1")
target = "/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder3"

# Build directories
directories_to_copy = [mul.graftItem(directory.path, testdir.path, target) for directory in
                       mul.getAll(mul.DIRECTORY, testdir)]
mul.buildDirectories(directories_to_copy)

# Copy files
files = mul.getAll(mul.FILES, testdir)
file_paths = [file.path for file in files]
mul.copyFiles(file_paths, testdir.path, target, True)
