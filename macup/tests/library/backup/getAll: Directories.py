from macup.library.backup import getAll, DIRECTORY
from macup.library.classes import FileTree

print(getAll(DIRECTORY, FileTree("/macup/tests/TestDir")))
