from macup.library.backup import getAll, DIRECTORY
from macup.classes import FileTree

print(getAll(DIRECTORY, FileTree("/macup/tests/TestDir")))
